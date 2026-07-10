# tinted-ui-tokens on Aider

Aider reads conventions from `CONVENTIONS.md` (via `--read`) or `.aider.conf.yml`.

## Install · 安装

Point Aider at the instruction file when launching:

```bash
aider --read INSTRUCTIONS.md
```

Or concatenate into an existing `CONVENTIONS.md`:

```bash
cat INSTRUCTIONS.md >> CONVENTIONS.md
aider
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ./tinted-ui-tokens
```

## Use · 使用

In the Aider chat:

> generate a tinted UI token system from #2563EB

Aider runs `scripts/generate_tokens.py` and reports `tokens.css` + `preview.html`.
