# tinted-ui-tokens on WindSurf (Codeium)

WindSurf reads `.windsurfrules` from the project root (or global memories).

## Install · 安装

Append the instruction to `.windsurfrules`:

```bash
cat INSTRUCTIONS.md >> .windsurfrules
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ./tinted-ui-tokens
```

## Use · 使用

Ask WindSurf:

> 用 #2563EB 出一套染色 Token 系统

WindSurf follows the appended instructions, runs `scripts/generate_tokens.py`, and
returns `tokens.css` + `preview.html`.
