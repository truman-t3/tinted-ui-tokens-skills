# tinted-ui-tokens-skills on Gemini CLI (Google)

Gemini CLI reads a `GEMINI.md` memory file from the working directory or your home.

## Install · 安装

A ready-to-use memory file is provided: [`GEMINI.md`](GEMINI.md). Drop it in your
working directory or home (or merge into an existing `GEMINI.md`):

```bash
cp GEMINI.md ./GEMINI.md

# or merge into an existing one
cat GEMINI.md >> GEMINI.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
```

## Use · 使用

In a Gemini CLI session:

> generate a tinted UI token system from #2563EB

Gemini runs `scripts/generate_tokens.py` and returns `tokens.css` + `preview.html`.
