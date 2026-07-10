# tinted-ui-tokens on Gemini CLI (Google)

Gemini CLI reads a `GEMINI.md` memory file from the working directory or your home.

## Install · 安装

Append the instruction to `GEMINI.md`:

```bash
cat INSTRUCTIONS.md >> GEMINI.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ./tinted-ui-tokens
```

## Use · 使用

In a Gemini CLI session:

> generate a tinted UI token system from #2563EB

Gemini runs `scripts/generate_tokens.py` and returns `tokens.css` + `preview.html`.
