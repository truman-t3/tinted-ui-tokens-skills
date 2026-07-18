# tinted-ui-tokens-skills on Aider

Aider reads conventions from `CONVENTIONS.md` (via `--read`) or `.aider.conf.yml`.

## Install · 安装

A ready-to-use convention file is provided: [`CONVENTIONS.md`](CONVENTIONS.md).

```bash
# launch Aider reading the provided file directly
aider --read CONVENTIONS.md

# or merge into an existing CONVENTIONS.md
cat CONVENTIONS.md >> CONVENTIONS.md
aider
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
```

## Use · 使用

In the Aider chat:

> generate a tinted UI token system from #2563EB

Aider runs `scripts/generate_tokens.py` and reports `tokens.css` + `preview.html`.
