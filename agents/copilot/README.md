# tinted-ui-tokens on GitHub Copilot

GitHub Copilot (in VS Code / Codespaces) reads `.github/copilot-instructions.md`.

## Install · 安装

Append a section to `.github/copilot-instructions.md`:

```bash
cat INSTRUCTIONS.md >> .github/copilot-instructions.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ./tinted-ui-tokens
```

## Use · 使用

Ask Copilot Chat:

> generate a tinted UI token system from #2563EB

Copilot follows the instructions, runs `scripts/generate_tokens.py`, and shows
`tokens.css` + `preview.html`.
