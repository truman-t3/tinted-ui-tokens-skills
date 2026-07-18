# tinted-ui-tokens-skills on WindSurf (Codeium)

WindSurf reads `.windsurfrules` from the project root (or global memories).

## Install · 安装

A ready-to-use rule file is provided: [`.windsurfrules`](.windsurfrules). Drop it
in your project root (or merge into an existing `.windsurfrules`):

```bash
cp .windsurfrules ./.windsurfrules

# or merge into an existing one
cat .windsurfrules >> .windsurfrules
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
```

## Use · 使用

Ask WindSurf:

> 用 #2563EB 出一套染色 Token 系统

WindSurf follows the appended instructions, runs `scripts/generate_tokens.py`, and
returns `tokens.css` + `preview.html`.
