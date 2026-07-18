#!/usr/bin/env python3
"""
smoke_test.py - generator smoke + robustness tests for tinted-ui-tokens-skills.

Runs the exact CI generator checks locally so that "passes CI" stays equivalent
to "passes ``python scripts/smoke_test.py``". No external dependencies
(Python standard library only).

Checks
------
1. Chromatic brands (cool / warm / balanced) each produce a non-empty
   ``tokens.css`` + ``preview.html`` via the real CLI.
2. Every ``--color-*`` value emitted is a valid 6-digit hex.
3. Semantic-color sanity on a blue brand: error / warning / success are three
   distinct colors and ``error`` is reddish (guards the HSL->RGB channel-mapping
   regression that once made a blue brand emit a blue "error" color).
4. Extreme / degenerate brands (pure black / white / gray, short hex, lowercase)
   do NOT crash and still emit valid hex. Pure-neutral brands legitimately have
   no hue to tint with, so pure neutrals in their output are acceptable here -
   we only assert robustness, not the "no pure neutral" contract.
5. Invalid input is rejected with a non-zero exit code.

Usage
-----
    python scripts/smoke_test.py
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEN = HERE / "generate_tokens.py"

# brand -> expected temperature label (None = don't assert the label)
CHROMATIC = {
    "#2563EB": "cool",
    "#C4502A": "warm",
    "#16A34A": "balanced",
}
EXTREME = ["#000000", "#FFFFFF", "#808080", "#abc", "#0a0a0a"]
INVALID = ["#12", "nope", "#GGGGGG", ""]

HEX_RE = re.compile(r"--color-[\w-]+:\s*(#[0-9a-fA-F]{6})\b")
ANY_COLOR_RE = re.compile(r"--color-[\w-]+:\s*([^;]+);")


def run_gen(brand, out_dir, extra=None):
    cmd = [sys.executable, str(GEN), "--brand", brand, "--name", "CI", "--out", str(out_dir)]
    if extra:
        cmd += extra
    return subprocess.run(cmd, capture_output=True, text=True)


def assert_valid_hex(css, brand):
    # Every --color-* value must be a valid 6-digit hex (shadows are separate vars).
    for m in ANY_COLOR_RE.finditer(css):
        val = m.group(1).strip()
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", val):
            raise AssertionError(f"[{brand}] non-hex --color value: {val!r}")


def grab(css, var):
    m = re.search(rf"--color-{var}:\s*(#[0-9a-fA-F]{{6}})", css)
    assert m, f"--color-{var} not found"
    return m.group(1)


def check_chromatic():
    with tempfile.TemporaryDirectory() as td:
        for brand, temp in CHROMATIC.items():
            out = Path(td) / brand.lstrip("#")
            r = run_gen(brand, out)
            assert r.returncode == 0, f"[{brand}] generator failed: {r.stderr}"
            css = out / "tokens.css"
            html = out / "preview.html"
            assert css.is_file() and css.stat().st_size > 0, f"[{brand}] tokens.css missing/empty"
            assert html.is_file() and html.stat().st_size > 0, f"[{brand}] preview.html missing/empty"
            text = css.read_text(encoding="utf-8")
            assert_valid_hex(text, brand)
            if temp:
                assert f"Temperature : {temp}" in text, \
                    f"[{brand}] expected temperature '{temp}' in tokens.css header"
            print(f"  OK chromatic {brand} ({temp}) -> {css.stat().st_size}B css, {html.stat().st_size}B html")


def check_semantic():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "sem"
        assert run_gen("#2563EB", out, ["--format", "css"]).returncode == 0
        css = (out / "tokens.css").read_text(encoding="utf-8")
        err, warn, succ = grab(css, "error"), grab(css, "warning"), grab(css, "success")
        assert len({err.lower(), warn.lower(), succ.lower()}) == 3, \
            f"semantic colors collapsed: error={err} warning={warn} success={succ}"
        r, g, b = int(err[1:3], 16), int(err[3:5], 16), int(err[5:7], 16)
        assert r > g and r > b, \
            f"error color {err} is not reddish (r={r} g={g} b={b}); HSL->RGB mapping may be broken"
        print(f"  OK semantic: error={err} warning={warn} success={succ}")


def check_extreme():
    with tempfile.TemporaryDirectory() as td:
        for brand in EXTREME:
            out = Path(td) / re.sub(r"\W", "_", brand)
            r = run_gen(brand, out, ["--format", "css"])
            assert r.returncode == 0, f"[{brand}] extreme brand crashed: {r.stderr}"
            css = (out / "tokens.css")
            assert css.is_file() and css.stat().st_size > 0, f"[{brand}] tokens.css missing/empty"
            assert_valid_hex(css.read_text(encoding="utf-8"), brand)
            print(f"  OK extreme  {brand} -> no crash, valid hex")


def check_invalid():
    with tempfile.TemporaryDirectory() as td:
        for brand in INVALID:
            r = run_gen(brand, Path(td) / "x")
            assert r.returncode != 0, f"invalid brand {brand!r} unexpectedly succeeded"
            print(f"  OK invalid  {brand!r} -> rejected (exit {r.returncode})")


def main():
    print("smoke_test: chromatic brands")
    check_chromatic()
    print("smoke_test: semantic sanity")
    check_semantic()
    print("smoke_test: extreme / degenerate brands")
    check_extreme()
    print("smoke_test: invalid input rejection")
    check_invalid()
    print("\nPASS: generator smoke + robustness tests OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"\nFAIL: {e}", file=sys.stderr)
        sys.exit(1)
