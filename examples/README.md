# Examples

Four brand colors, each run through `generate_tokens.py --format all`. Every folder is a
real, unedited generator output — nothing hand-tweaked.

| Folder | Brand | Temperature | on-brand contrast |
|--------|-------|-------------|-------------------|
| [`blue/`](blue/)     | `#2563EB` | cool     | 4.90:1 ✓ AA |
| [`green/`](green/)   | `#16A34A` | balanced | 5.12:1 ✓ AA |
| [`warm/`](warm/)     | `#C4502A` | warm     | 4.56:1 ✓ AA |
| [`violet/`](violet/) | `#7C3AED` | cool     | 5.37:1 ✓ AA |

Each folder contains all five export formats:

- `tokens.css` — CSS custom properties, light + `[data-theme="dark"]`
- `preview.html` — standalone light/dark preview page
- `tokens.json` — [DTCG](https://tr.designtokens.org/) design-token format
- `tailwind.config.js` — Tailwind theme extension
- `_tokens.scss` — SCSS variables

## Live gallery

Open [`index.html`](index.html) locally, or view the hosted version:
**https://truman-t3.github.io/tinted-ui-tokens-skills/examples/**

## Regenerate

```bash
python3 scripts/generate_tokens.py --brand "#2563EB" --name "Acme" --format all --out examples/blue
```
