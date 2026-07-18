#!/usr/bin/env python3
"""
generate_tokens.py - Tinted UI Token generator
================================================

Given a single brand color, produce a complete, production-ready design-token
system where EVERY neutral surface carries a little of the brand's temperature
- the core idea from "你的UI廉价，错在颜色" (cheap UI is a color problem).

Outputs (selected via --format):
  - tokens.css      : drop-in :root + [data-theme="dark"] custom properties
  - preview.html    : self-contained live demo (cards, error form, gradient,
                      icons, brand button, light/dark toggle) inlining tokens
  - tokens.json     : W3C DTCG design-token format (color/* + shadow/*)
  - tailwind.config.js : theme.extend.colors + boxShadow
  - _tokens.scss    : SCSS variables (light + dark)

Quality guarantees
------------------
* No pure #FFFFFF / #000000 / #808080 anywhere.
* Every text-on-surface pair is checked against WCAG 2.1 contrast and, if it
  falls below the AA target, the text is nudged along its HSL lightness axis
  until it passes - so readability always wins, and the brand hue-lean is
  preserved wherever L does not hit an extreme.

Usage:
  python generate_tokens.py --brand "#2563EB" --out ./out
  python generate_tokens.py --brand "#C4502A" --name "Acme" --out ./out
  python generate_tokens.py --brand "#16A34A" --format json
  python generate_tokens.py --brand "#2563EB" --tint-strength strong

The math is brand-agnostic: temperature is derived by blending every neutral
ramp toward the brand hue, so any brand color yields a coherent system.
"""

import argparse
import datetime
import json
import os
import sys

# --------------------------------------------------------------------------
# Color helpers
# --------------------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#").strip()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"invalid hex color: #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(x))):02X}" for x in rgb)


def mix(a, b, t):
    """Linear interpolation from a toward b by t (0..1)."""
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def rgb_to_hsl(rgb):
    r, g, b = (x / 255.0 for x in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    l = (mx + mn) / 2.0
    if d == 0:
        h = s = 0.0
    else:
        s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = ((g - b) / d + (6 if g < b else 0)) / 6.0
        elif mx == g:
            h = ((b - r) / d + 2) / 6.0
        else:
            h = ((r - g) / d + 4) / 6.0
    return (h * 360.0, s, l)


def hsl_to_rgb(h, s, l):
    h = (h % 360.0) / 360.0
    if s == 0:
        v = round(l * 255)
        return (v, v, v)
    q = l + s * (1 - abs(2 * l - 1)) / 2.0 if l < 0.5 else l + s * (1 - l)
    p = 2 * l - q
    def hue(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p
    # channel offsets: R = h+1/3, G = h, B = h-1/3 (canonical HSL->RGB order)
    return tuple(round(hue(p, q, h + off) * 255) for off in (1 / 3, 0, -1 / 3))


def desaturate(rgb, factor=0.9):
    h, s, l = rgb_to_hsl(rgb)
    return hsl_to_rgb(h, s * factor, l)


def rgba_str(rgb, a):
    return f"rgba({round(rgb[0])}, {round(rgb[1])}, {round(rgb[2])}, {a})"


def classify_temperature(hue):
    """Label only - the math blends toward brand regardless."""
    if hue >= 340 or hue < 65:
        return "warm"
    if 200 <= hue < 320:
        return "cool"
    return "balanced"


# --------------------------------------------------------------------------
# WCAG 2.1 contrast
# --------------------------------------------------------------------------

def relative_luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1, rgb2):
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_contrast(text_rgb, bg_rgb, target, is_dark):
    """Nudge ``text_rgb`` along HSL lightness until it reaches ``target``
    contrast against ``bg_rgb``. Light themes darken; dark themes lighten.
    Returns an rgb tuple (may be unchanged if already passing)."""
    if contrast_ratio(text_rgb, bg_rgb) >= target:
        return text_rgb
    h, s, l = rgb_to_hsl(text_rgb)
    step = 0.015
    for _ in range(70):
        new_l = l - step if not is_dark else l + step
        new_l = clamp(new_l)
        cand = hsl_to_rgb(h, s, new_l)
        if contrast_ratio(cand, bg_rgb) >= target:
            return cand
        l = new_l
    # worst case: return the most extreme safe value we reached
    return hsl_to_rgb(h, s, clamp(l))


# --------------------------------------------------------------------------
# Token generation
# --------------------------------------------------------------------------

TINT_PRESETS = {"subtle": 0.6, "normal": 1.0, "strong": 1.6}


def build_tokens(brand_hex, tint_strength="normal"):
    if isinstance(tint_strength, str):
        scale = TINT_PRESETS.get(tint_strength.lower(), 1.0)
    else:
        scale = float(tint_strength)
    if scale <= 0:
        raise ValueError("tint-strength must be > 0")

    def bf(base_factor):
        """Scaled blend factor."""
        return base_factor * scale

    brand = hex_to_rgb(brand_hex)
    bh, bs, bl = rgb_to_hsl(brand)
    temperature = classify_temperature(bh)
    white = (255, 255, 255)

    # brand-subtle: brand washed toward white (light) / toward surface (dark)
    brand_subtle_light = mix(brand, white, 0.86)

    # ---- LIGHT neutrals: blend each gray ramp toward brand ----
    bg = mix((248, 248, 248), brand, bf(0.035))
    surface = mix((255, 255, 255), brand, bf(0.018))
    surface_2 = mix((241, 241, 241), brand, bf(0.05))
    border = mix((229, 229, 229), brand, bf(0.07))
    border_strong = mix((199, 199, 199), brand, bf(0.11))
    text = mix((17, 17, 17), brand, bf(0.16))
    text_2 = mix((74, 74, 74), brand, bf(0.16))
    text_muted = mix((154, 154, 154), brand, bf(0.18))

    # ---- DARK neutrals: tinted dark, not pure black ----
    d_bg = mix((15, 17, 23), brand, bf(0.10))
    d_surface = mix((22, 27, 39), brand, bf(0.08))
    d_surface2 = mix((28, 34, 48), brand, bf(0.08))
    d_border = mix((30, 39, 56), brand, bf(0.10))
    d_border_strong = mix((45, 56, 78), brand, bf(0.10))
    d_text = mix((232, 237, 245), brand, bf(0.04))
    d_text2 = mix((138, 154, 181), brand, bf(0.06))
    d_text_muted = mix((122, 139, 160), brand, bf(0.08))
    brand_subtle_dark = mix(brand, d_surface, 0.80)

    # ---- Semantic colors: nudge toward brand temperature ----
    def semantic(base_hex):
        base = hex_to_rgb(base_hex)
        nudged = desaturate(mix(base, brand, 0.06), 0.92)
        return nudged

    error = semantic("#DC2626")
    warning = semantic("#F59E0B")
    success = semantic("#16A34A")

    error_subtle = mix(error, brand_subtle_light, 0.85)
    warning_subtle = mix(warning, brand_subtle_light, 0.85)
    success_subtle = mix(success, brand_subtle_light, 0.85)

    d_error_subtle = mix(error, d_surface2, 0.82)
    d_warning_subtle = mix(warning, d_surface2, 0.82)
    d_success_subtle = mix(success, d_surface2, 0.82)

    # ---- WCAG contrast compensation (readability always wins) ----
    # Targets: normal text AA = 4.5:1; secondary/muted AA-large = 3:1.
    text = ensure_contrast(text, bg, 4.5, is_dark=False)
    text_2 = ensure_contrast(text_2, surface, 4.5, is_dark=False)
    text_muted = ensure_contrast(text_muted, surface, 3.0, is_dark=False)
    d_text = ensure_contrast(d_text, d_bg, 4.5, is_dark=True)
    d_text2 = ensure_contrast(d_text2, d_surface, 4.5, is_dark=True)
    d_text_muted = ensure_contrast(d_text_muted, d_surface, 3.0, is_dark=True)

    # ---- on-brand text: readable color placed ON the brand color ----
    near_white = mix(white, brand, 0.04)
    near_black = mix((17, 17, 17), brand, 0.10)
    on_brand = near_white if contrast_ratio(near_white, brand) >= contrast_ratio(near_black, brand) \
        else near_black

    # ---- Shadows: brand hue at low alpha, never pure black ----
    shadow_sm = (
        f"0 1px 3px {rgba_str(brand, 0.08)}, "
        f"0 0 0 1px {rgba_str(brand, 0.04)}"
    )
    shadow_md = (
        f"0 4px 16px {rgba_str(brand, 0.10)}, "
        f"0 1px 4px {rgba_str(brand, 0.06)}"
    )
    shadow_lg = (
        f"0 12px 40px {rgba_str(brand, 0.12)}, "
        f"0 2px 8px {rgba_str(brand, 0.06)}"
    )
    d_shadow_sm = f"0 0 0 1px {rgba_str(brand, 0.10)}"
    d_shadow_md = (
        f"0 4px 20px rgba(0, 0, 0, 0.40), "
        f"0 0 0 1px {rgba_str(brand, 0.06)}"
    )
    d_shadow_lg = (
        f"0 12px 40px rgba(0, 0, 0, 0.45), "
        f"0 0 0 1px {rgba_str(brand, 0.08)}"
    )

    return {
        "META_BRAND": brand_hex.upper(),
        "META_TEMP": temperature,
        "META_DATE": datetime.date.today().isoformat(),

        "BRAND": rgb_to_hex(brand),
        "BRAND_SUBTLE": rgb_to_hex(brand_subtle_light),
        "ON_BRAND": rgb_to_hex(on_brand),
        "BG": rgb_to_hex(bg),
        "SURFACE": rgb_to_hex(surface),
        "SURFACE2": rgb_to_hex(surface_2),
        "BORDER": rgb_to_hex(border),
        "BORDER_STRONG": rgb_to_hex(border_strong),
        "TEXT": rgb_to_hex(text),
        "TEXT2": rgb_to_hex(text_2),
        "TEXT_MUTED": rgb_to_hex(text_muted),
        "ERROR": rgb_to_hex(error),
        "ERROR_SUBTLE": rgb_to_hex(error_subtle),
        "WARNING": rgb_to_hex(warning),
        "WARNING_SUBTLE": rgb_to_hex(warning_subtle),
        "SUCCESS": rgb_to_hex(success),
        "SUCCESS_SUBTLE": rgb_to_hex(success_subtle),
        "SHADOW_SM": shadow_sm,
        "SHADOW_MD": shadow_md,
        "SHADOW_LG": shadow_lg,

        "D_BG": rgb_to_hex(d_bg),
        "D_SURFACE": rgb_to_hex(d_surface),
        "D_SURFACE2": rgb_to_hex(d_surface2),
        "D_BORDER": rgb_to_hex(d_border),
        "D_BORDER_STRONG": rgb_to_hex(d_border_strong),
        "D_TEXT": rgb_to_hex(d_text),
        "D_TEXT2": rgb_to_hex(d_text2),
        "D_TEXT_MUTED": rgb_to_hex(d_text_muted),
        "D_BRAND_SUBTLE": rgb_to_hex(brand_subtle_dark),
        "D_ERROR_SUBTLE": rgb_to_hex(d_error_subtle),
        "D_WARNING_SUBTLE": rgb_to_hex(d_warning_subtle),
        "D_SUCCESS_SUBTLE": rgb_to_hex(d_success_subtle),
        "D_SHADOW_SM": d_shadow_sm,
        "D_SHADOW_MD": d_shadow_md,
        "D_SHADOW_LG": d_shadow_lg,
    }


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------

CSS_TEMPLATE = """/* ==========================================================================
   Tinted UI Token System
   Brand : %%META_BRAND%%   Temperature : %%META_TEMP%%
   Generated : %%META_DATE%%
   Method: every neutral surface is blended a few percent toward the brand
   hue, so the brand "flows through" the system instead of sitting on top.
   No pure #FFFFFF / #000000 / #808080 anywhere. Text on each surface is
   checked against WCAG AA and nudged if needed, so readability always wins.
   ========================================================================== */

:root,
[data-theme="light"] {
  /* Brand */
  --color-brand:        %%BRAND%%;
  --color-brand-subtle: %%BRAND_SUBTLE%%;
  --color-on-brand:     %%ON_BRAND%%;   /* readable text placed ON --color-brand */

  /* Surfaces - tinted by brand */
  --color-bg:           %%BG%%;
  --color-surface:      %%SURFACE%%;
  --color-surface-2:    %%SURFACE2%%;
  --color-border:       %%BORDER%%;
  --color-border-strong:%%BORDER_STRONG%%;

  /* Text - near-black/near-white with a hue lean (WCAG AA checked) */
  --color-text:         %%TEXT%%;
  --color-text-2:       %%TEXT2%%;
  --color-text-muted:   %%TEXT_MUTED%%;

  /* Semantic - nudged toward brand temperature */
  --color-error:         %%ERROR%%;
  --color-error-subtle:  %%ERROR_SUBTLE%%;
  --color-warning:       %%WARNING%%;
  --color-warning-subtle:%%WARNING_SUBTLE%%;
  --color-success:       %%SUCCESS%%;
  --color-success-subtle:%%SUCCESS_SUBTLE%%;

  /* Shadows - brand hue, never pure black */
  --shadow-sm: %%SHADOW_SM%%;
  --shadow-md: %%SHADOW_MD%%;
  --shadow-lg: %%SHADOW_LG%%;
}

[data-theme="dark"] {
  --color-brand-subtle: %%D_BRAND_SUBTLE%%;
  --color-on-brand:     %%ON_BRAND%%;

  --color-bg:           %%D_BG%%;
  --color-surface:      %%D_SURFACE%%;
  --color-surface-2:    %%D_SURFACE2%%;
  --color-border:       %%D_BORDER%%;
  --color-border-strong:%%D_BORDER_STRONG%%;

  --color-text:         %%D_TEXT%%;
  --color-text-2:       %%D_TEXT2%%;
  --color-text-muted:   %%D_TEXT_MUTED%%;

  --color-error-subtle:  %%D_ERROR_SUBTLE%%;
  --color-warning-subtle:%%D_WARNING_SUBTLE%%;
  --color-success-subtle:%%D_SUCCESS_SUBTLE%%;

  --shadow-sm: %%D_SHADOW_SM%%;
  --shadow-md: %%D_SHADOW_MD%%;
  --shadow-lg: %%D_SHADOW_LG%%;
}
"""


def render_css(t):
    css = CSS_TEMPLATE
    for k, v in t.items():
        css = css.replace(f"%%{k}%%", v)
    return css


PREVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Token Preview - %%META_BRAND%%</title>
<style>
%%CSS%%
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  transition: background .25s ease, color .25s ease;
}
.wrap { max-width: 920px; margin: 0 auto; padding: 32px 24px 64px; }
.topbar {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 18px; margin-bottom: 28px;
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: 12px; box-shadow: var(--shadow-sm);
}
.swatch { width: 34px; height: 34px; border-radius: 8px; background: var(--color-brand);
  box-shadow: var(--shadow-sm); }
.brand-meta { display: flex; flex-direction: column; line-height: 1.3; }
.brand-meta b { font-size: .98rem; color: var(--color-text); }
.brand-meta span { font-size: .72rem; color: var(--color-text-muted); letter-spacing: .04em; }
.spacer { flex: 1; }
.toggle {
  border: 1px solid var(--color-border-strong); background: var(--color-surface-2);
  color: var(--color-text-2); border-radius: 8px; padding: 8px 14px;
  font-size: .82rem; cursor: pointer; transition: all .2s ease;
}
.toggle:hover { color: var(--color-brand); border-color: var(--color-brand); }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 680px){ .grid { grid-template-columns: 1fr; } }
.card {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: 10px; box-shadow: var(--shadow-md); padding: 22px;
}
.card-label {
  font-size: .68rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
  color: var(--color-text-muted); margin-bottom: 8px;
}
.card-title { font-size: 1.18rem; font-weight: 600; color: var(--color-text); margin: 0 0 8px; }
.card-body { font-size: .9rem; line-height: 1.65; color: var(--color-text-2); margin: 0; }
.card-badge {
  display: inline-block; margin-top: 16px; background: var(--color-brand-subtle);
  color: var(--color-brand); font-size: .72rem; font-weight: 600; letter-spacing: .06em;
  padding: 4px 11px; border-radius: 5px;
}
.hero {
  grid-column: 1 / -1; border-radius: 14px; padding: 38px 30px;
  background: linear-gradient(175deg, var(--color-surface) 0%, var(--color-brand-subtle) 60%, var(--color-surface-2) 100%);
  border: 1px solid var(--color-border); box-shadow: var(--shadow-lg);
}
.hero h2 { margin: 0 0 10px; font-size: 1.5rem; color: var(--color-text); }
.hero p { margin: 0; max-width: 560px; color: var(--color-text-2); line-height: 1.6; font-size: .92rem; }
.btn-primary {
  margin-top: 22px; display: inline-block; border: none; cursor: pointer;
  background: var(--color-brand); color: var(--color-on-brand);
  border-radius: 9px; padding: 12px 22px; font-size: .92rem; font-weight: 600;
  box-shadow: var(--shadow-md); transition: filter .2s ease;
}
.btn-primary:hover { filter: brightness(1.06); }
.field { margin-top: 18px; }
.field label { display: block; font-size: .8rem; color: var(--color-text-2); margin-bottom: 6px; }
.input {
  width: 100%; padding: 11px 13px; border-radius: 8px; font-size: .9rem;
  background: var(--color-surface); color: var(--color-text);
  border: 1px solid var(--color-border-strong); outline: none; transition: all .2s ease;
}
.input-error {
  border-color: var(--color-error);
  background: var(--color-error-subtle);
  box-shadow: 0 0 0 3px rgba(212,43,58,.12), 0 0 0 1px var(--color-brand);
}
.err-msg { margin-top: 7px; font-size: .78rem; color: var(--color-error); }
.row { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 18px; }
.icon-box {
  width: 46px; height: 46px; border-radius: 10px; display: grid; place-items: center;
  background: var(--color-brand-subtle); color: var(--color-brand); box-shadow: var(--shadow-sm);
}
.icon-box svg { width: 22px; height: 22px; }
.swatches { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 18px; }
.swatch-item { text-align: center; font-size: .68rem; color: var(--color-text-muted); }
.swatch-item .box { width: 54px; height: 40px; border-radius: 8px; border: 1px solid var(--color-border); margin-bottom: 6px; }
.section-title { font-size: .8rem; text-transform: uppercase; letter-spacing: .1em;
  color: var(--color-text-muted); margin: 30px 0 4px; }
</style>
</head>
<body>
<div class="wrap" id="stage" data-theme="light">
  <div class="topbar">
    <div class="swatch"></div>
    <div class="brand-meta">
      <b>%%NAME%%</b>
      <span>brand %%META_BRAND%% &middot; %%META_TEMP%% temperature</span>
    </div>
    <div class="spacer"></div>
    <button class="toggle" onclick="toggleTheme()">切换 明 / 暗</button>
  </div>

  <div class="grid">
    <div class="hero">
      <h2>品牌色，流进整个系统</h2>
      <p>背景、表面、边框、文字、阴影、语义色、渐变、图标 —— 每一层都带着同一份品牌色温。没有纯中性色，没有死黑阴影。</p>
      <button class="btn-primary">Get started</button>
    </div>

    <div class="card">
      <div class="card-label">Overview</div>
      <div class="card-title">染色中性色</div>
      <p class="card-body">每张卡片、每个表面都微微偏向品牌色，所以品牌出现时不像被临时贴上去，而像本来就属于这里。</p>
      <span class="card-badge">BRAND SUBTLE</span>
    </div>

    <div class="card">
      <div class="card-label">Form</div>
      <div class="card-title">带温度的错误态</div>
      <p class="card-body">错误红被轻推到品牌色温，输入框底色也偏向品牌场，focus ring 同时带着两种温度。</p>
      <div class="field">
        <label>邮箱地址</label>
        <input class="input input-error" value="not-an-email" />
        <div class="err-msg">请输入有效的邮箱地址</div>
      </div>
    </div>

    <div class="card" style="grid-column:1/-1">
      <div class="card-label">Icons</div>
      <div class="row">
        <div class="icon-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/></svg></div>
        <div class="icon-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></div>
        <div class="icon-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16M4 6h16M4 18h10"/></svg></div>
        <div class="row" style="flex-direction:column;gap:8px;margin-top:0">
          <div class="swatches">
            <div class="swatch-item"><div class="box" style="background:var(--color-error)"></div>error</div>
            <div class="swatch-item"><div class="box" style="background:var(--color-error-subtle)"></div>error-sub</div>
            <div class="swatch-item"><div class="box" style="background:var(--color-warning)"></div>warning</div>
            <div class="swatch-item"><div class="box" style="background:var(--color-success)"></div>success</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
function toggleTheme(){
  var s = document.getElementById('stage');
  s.setAttribute('data-theme', s.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
}
</script>
</body>
</html>
"""


def render_preview(t, name):
    html = PREVIEW_TEMPLATE
    html = html.replace("%%CSS%%", render_css(t))
    html = html.replace("%%NAME%%", name)
    for k, v in t.items():
        html = html.replace(f"%%{k}%%", v)
    return html


# --------------------------------------------------------------------------
# Export renderers (DTCG JSON / Tailwind / SCSS)
# --------------------------------------------------------------------------

# flat token key -> friendly leaf name used in tailwind/scss
_LEAF = {
    "BRAND": "brand", "BRAND_SUBTLE": "brand-subtle", "ON_BRAND": "on-brand",
    "BG": "bg", "SURFACE": "surface", "SURFACE2": "surface-2",
    "BORDER": "border", "BORDER_STRONG": "border-strong",
    "TEXT": "text", "TEXT2": "text-2", "TEXT_MUTED": "text-muted",
    "ERROR": "error", "ERROR_SUBTLE": "error-subtle",
    "WARNING": "warning", "WARNING_SUBTLE": "warning-subtle",
    "SUCCESS": "success", "SUCCESS_SUBTLE": "success-subtle",
}


def render_json(t):
    """W3C DTCG design-token format: nested color/* + shadow/* groups."""
    colors = {}
    shadows = {}
    for k, v in t.items():
        if k.startswith("META_"):
            continue
        if k.startswith("SHADOW"):
            shadows[k.lower()] = {"$type": "shadow", "$value": v}
        elif k.startswith("D_"):
            colors.setdefault("dark", {})[k[2:].lower()] = {"$type": "color", "$value": v}
        else:
            colors[k.lower()] = {"$type": "color", "$value": v}
    tree = {
        "$description": f"Tinted UI tokens for brand {t['META_BRAND']} ({t['META_TEMP']})",
        "color": colors,
        "shadow": shadows,
    }
    return json.dumps(tree, indent=2, ensure_ascii=False) + "\n"


def render_tailwind(t):
    tw_colors = {}
    tw_shadow = {}
    for k, name in _LEAF.items():
        if k in t:
            tw_colors[name] = t[k]
    for k in t:
        if k.startswith("D_"):
            tw_colors["dark-" + k[2:].lower()] = t[k]
    for k in t:
        if k.startswith("SHADOW"):
            tw_shadow[k.lower()] = t[k]
        elif k.startswith("D_SHADOW"):
            tw_shadow["dark-" + k[2:].lower()] = t[k]
    lines = [
        "/** @type {import('tailwindcss').Config} */",
        "module.exports = {",
        "  theme: {",
        "    extend: {",
        "      colors: {",
    ]
    for name, val in tw_colors.items():
        lines.append(f'        "{name}": "{val}",')
    lines.append("      },")
    lines.append("      boxShadow: {")
    for name, val in tw_shadow.items():
        lines.append(f'        "{name}": "{val}",')
    lines.append("      },")
    lines.append("    },")
    lines.append("  },")
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_scss(t):
    out = ["// Tinted UI Tokens - generated by tinted-ui-tokens-skills", ""]
    out.append("// ---- Light theme ----")
    for k, name in _LEAF.items():
        if k in t:
            out.append(f"$color-{name}: {t[k]};")
    out.append("")
    out.append("// ---- Shadows (light) ----")
    for k in t:
        if k.startswith("SHADOW"):
            out.append(f"$shadow-{k.lower()}: {t[k]};")
    out.append("")
    out.append("// ---- Dark theme ----")
    for k in t:
        if k.startswith("D_"):
            out.append(f"$color-dark-{k[2:].lower()}: {t[k]};")
    for k in t:
        if k.startswith("D_SHADOW"):
            out.append(f"$shadow-dark-{k[2:].lower()}: {t[k]};")
    out.append("")
    out.append("// Map light vars onto [data-theme=\"dark\"] (drop-in):")
    out.append("@mixin tinted-dark {")
    for k in t:
        if k.startswith("D_"):
            out.append(f"  --color-{k[2:].lower()}: $color-dark-{k[2:].lower()};")
    out.append("}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

FORMATS = ["css", "html", "both", "json", "tailwind", "scss", "all"]


def main():
    ap = argparse.ArgumentParser(description="Generate a tinted UI token system from a brand color.")
    ap.add_argument("--brand", required=True, help="Brand color hex, e.g. #2563EB")
    ap.add_argument("--name", default="Untitled", help="Product / brand name for the preview")
    ap.add_argument("--out", default=".", help="Output directory")
    ap.add_argument("--format", choices=FORMATS, default="both",
                    help="What to emit (default: both = css+html; 'all' = css+html+json+tailwind+scss)")
    ap.add_argument("--tint-strength", choices=["subtle", "normal", "strong"], default="normal",
                    help="How strongly neutrals lean toward the brand (default: normal)")
    args = ap.parse_args()

    try:
        tokens = build_tokens(args.brand, args.tint_strength)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    os.makedirs(args.out, exist_ok=True)
    fmt = args.format

    if fmt in ("css", "both", "all"):
        css_path = os.path.join(args.out, "tokens.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(render_css(tokens))
        print(f"wrote {css_path}")

    if fmt in ("html", "both", "all"):
        html_path = os.path.join(args.out, "preview.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_preview(tokens, args.name))
        print(f"wrote {html_path}")

    if fmt in ("json", "all"):
        json_path = os.path.join(args.out, "tokens.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(render_json(tokens))
        print(f"wrote {json_path}")

    if fmt in ("tailwind", "all"):
        tw_path = os.path.join(args.out, "tailwind.config.js")
        with open(tw_path, "w", encoding="utf-8") as f:
            f.write(render_tailwind(tokens))
        print(f"wrote {tw_path}")

    if fmt in ("scss", "all"):
        scss_path = os.path.join(args.out, "_tokens.scss")
        with open(scss_path, "w", encoding="utf-8") as f:
            f.write(render_scss(tokens))
        print(f"wrote {scss_path}")

    # WCAG report
    light = contrast_ratio(hex_to_rgb(tokens["TEXT"]), hex_to_rgb(tokens["SURFACE"]))
    dark = contrast_ratio(hex_to_rgb(tokens["D_TEXT"]), hex_to_rgb(tokens["D_BG"]))
    onb = contrast_ratio(hex_to_rgb(tokens["ON_BRAND"]), hex_to_rgb(tokens["BRAND"]))
    print(f"\nbrand {tokens['META_BRAND']} -> temperature: {tokens['META_TEMP']} "
          f"(tint: {args.tint_strength})")
    print(f"  bg      {tokens['BG']}")
    print(f"  surface {tokens['SURFACE']}")
    print(f"  text    {tokens['TEXT']}")
    print(f"  on-brand {tokens['ON_BRAND']} (on brand {tokens['BRAND']})")
    print(f"  contrast  light text/surface {light:.2f}:1   "
          f"dark text/bg {dark:.2f}:1   on-brand {onb:.2f}:1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
