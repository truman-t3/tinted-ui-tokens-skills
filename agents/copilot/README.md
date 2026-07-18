# tinted-ui-tokens-skills on GitHub Copilot

GitHub Copilot (in VS Code / Codespaces) reads `.github/copilot-instructions.md`.

## Install · 安装

A ready-to-use file is provided: [`copilot-instructions.md`](copilot-instructions.md).
Copy it to `.github/`, or merge its contents into an existing one:

```bash
mkdir -p .github
cp copilot-instructions.md .github/copilot-instructions.md

# or merge into an existing one
cat copilot-instructions.md >> .github/copilot-instructions.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
```

## Use · 使用

Ask Copilot Chat:

> generate a tinted UI token system from #2563EB

Copilot follows the instructions, runs `scripts/generate_tokens.py`, and shows
`tokens.css` + `preview.html`.
