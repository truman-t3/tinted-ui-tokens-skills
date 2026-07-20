# Tinted UI Tokens skills · 品牌色 UI 设计 Token skills

When the user wants to generate UI color tokens, a design system, CSS variables,
or a branded theme from a brand color (or wants to fix a "cheap-looking" flat UI):

1. Collect the brand hex (ask if missing).
2. Run: `python scripts/generate_tokens.py --brand <hex> --name <name> --out <dir>`
3. Present `tokens.css` + `preview.html`, and state the detected temperature.
4. Optional flags: `--format {css,html,both,json,tailwind,scss,all}` also emits
   DTCG JSON / Tailwind / SCSS; `--tint-strength {subtle,normal,strong}` scales
   the tint; `--color-on-brand` is produced automatically (readable text/icon
   color on the brand button).

Method: every neutral surface (background, surface, border, text, shadow,
semantic color, gradient, icon) carries 2–3% of the brand hue — never pure
`#FFFFFF` / `#000000` / `#808080`.

Full instructions: `INSTRUCTIONS.md`
Repo: https://github.com/truman-t3/tinted-ui-tokens-skills
