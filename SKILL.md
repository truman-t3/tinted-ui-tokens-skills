---
name: tinted-ui-tokens-skills
slug: tinted-ui-tokens-skills
displayName: 品牌色 UI 设计 Token skills
version: 1.4.1
description: "从一个品牌色生成完整、可直接上线的设计 Token 系统：让每一个中性表面（背景、边框、文字、阴影、语义色、渐变、图标、暗色模式）都带上一小撮品牌色的温度，而不是使用纯中性色。当用户想用品牌色 / hex 生成、构建或设计 UI 颜色 Token、设计系统、CSS 变量、染色配色或品牌主题，或想通过修正扁平中性色让现有 UI 显得更高级时使用。触发语示例：给我生成一套设计Token、用这个品牌色出一套配色、UI颜色太廉价了、生成染色中性色系统、build a design system from #XXXXXX、tinted neutral palette。"
agent_created: true
---

# Tinted UI Tokens skills（品牌色 UI 设计 Token skills）

## Overview

Turn one brand color into a full design-token system where the brand "flows
through" the interface instead of sitting on top of it. The core technique (from
the essay 《你的UI廉价，错在颜色》) is: **never use pure neutral colors** —
blend 2–3% of the brand hue into every background, surface, border, text layer,
shadow, semantic color, gradient and icon. The result reads as "designed" rather
than "assembled".

The bundled generator (`scripts/generate_tokens.py`) is brand-agnostic: it
derives the temperature by blending each neutral ramp toward the given brand
hue, so it works for any color, not just the two palettes in the original essay.

### Cross-agent · 跨 agent

This skill is **agent-agnostic**. WorkBuddy and Claude Code read this `SKILL.md`
directly. For every other agent (Cursor, OpenAI Codex, Cline, Aider, WindSurf,
GitHub Copilot, Gemini CLI), the same instructions live in
[`INSTRUCTIONS.md`](INSTRUCTIONS.md) and are wired in via the docs under
[`agents/`](agents/) — each agent only differs in where its rule file goes. The
engine (`scripts/generate_tokens.py`) is identical everywhere. See the
`Cross-Agent Compatibility` table in `README.md`.

> 中文：本技能与具体 agent 无关。WorkBuddy 与 Claude Code 直接读取本 `SKILL.md`；
> 其余 agent（Cursor、OpenAI Codex、Cline、Aider、WindSurf、GitHub Copilot、Gemini CLI）
> 使用 [`INSTRUCTIONS.md`](INSTRUCTIONS.md) 中的同一份指令，并按 [`agents/`](agents/)
> 下的文档接入——差异只在规则文件的位置。引擎（`scripts/generate_tokens.py`）各处一致。
> 详见 `README.md` 的「跨 Agent 兼容性」表。

> 中文：内置生成器（`scripts/generate_tokens.py`）是品牌无关的——它把每条中性色阶朝给定品牌色相方向混合，从而推导出整套系统的温度，因此对任意颜色都适用，而不局限于原文中的两套配色。

## When to use · 何时使用

- User provides a brand color / hex and wants a design system, CSS variables, or a theme.
  · 用户提供品牌色 / hex，并想要一套设计系统、CSS 变量或主题。
- User wants to make an existing UI look more premium ("my UI looks cheap").
  · 用户想让现有 UI 显得更高级（"我的界面看起来很廉价"）。
- User asks for tokens for light + dark mode, semantic colors, or a branded palette.
  · 用户需要明 / 暗双模式、语义色或品牌化配色的 Token。
- User wants a quick visual proof (preview) of a color direction.
  · 用户想要某个配色方向的快速可视化预览。

## Workflow

### 1. Collect the minimum input

Only the brand color is required. Ask for it if missing:

- **Brand color** (hex like `#2563EB`). This defines the system's temperature.
- Optional: **product / brand name** (used only as a label in the preview).
- Optional: output directory (default to the current working directory).

Do not over-ask. One hex is enough to produce the whole system.

### 2. Run the generator

Use Python 3.10+ (on WorkBuddy use the managed runtime; on other agents use any
system `python` / `python3`):

```bash
python scripts/generate_tokens.py --brand "#2563EB" --name "Acme" --out "./out"
```

- `--brand` (required): any hex color.
- `--name` (optional): label shown in the preview header.
- `--out` (optional): output folder, created if missing.
- `--format css|html|both|json|tailwind|scss|all` (optional, default `both`).
  `json` = W3C DTCG tokens, `tailwind` = `tailwind.config.js`, `scss` = SCSS
  variables, `all` = css + html + json + tailwind + scss.
- `--tint-strength subtle|normal|strong` (optional, default `normal`): how
  strongly every neutral leans toward the brand hue.

The script writes `tokens.css` (drop-in `:root` + `[data-theme="dark"]`
custom properties) and `preview.html` (self-contained live demo with a
light/dark toggle). It also prints the detected temperature (warm / cool /
balanced) and key values.

### 3. Present the result

Use `present_files` to show `preview.html` (opens in the live preview panel) and
`tokens.css`. Tell the user the detected temperature and that every neutral is
brand-tinted. Offer to regenerate with a different brand color or to hand-tune
specific tokens.

### 4. Hand-tuning (optional)

To explain or adjust a value, consult `references/principles.md` (the "why"
behind each token) before editing. Common tweaks:

- More/less tint: pass `--tint-strength subtle|normal|strong` (no code edit
  needed). `strong` scales every blend factor up for a bolder brand presence.
- Semantic nudge strength: the `0.06` mix factor in `semantic()`.
- Contrast: every text-on-surface pair is auto-checked against WCAG AA and
  nudged if needed — so you normally never have to fix readability by hand.

## Output contract

`tokens.css` defines, for `:root` / `[data-theme="light"]` and
`[data-theme="dark"]`:

- `--color-brand`, `--color-brand-subtle`, `--color-on-brand`
  (readable text/icon color to place ON `--color-brand`)
- `--color-bg`, `--color-surface`, `--color-surface-2`, `--color-border`,
  `--color-border-strong`
- `--color-text`, `--color-text-2`, `--color-text-muted`
- `--color-error` / `-subtle`, `--color-warning` / `-subtle`,
  `--color-success` / `-subtle`
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`

No pure `#FFFFFF`, `#000000`, or `#808080` is emitted anywhere. Every
text-on-surface pair passes WCAG AA (auto-checked + nudged if needed).

## References

- `references/principles.md` — the design rules the generator enforces, plus the
  grayscale test for validating a system.
