# tinted-ui-tokens-skills on OpenAI Codex (Codex CLI)

Codex reads instruction files `AGENTS.md` / `codex.md` from the working directory
and can execute shell commands (including the Python engine).

## Install · 安装

A ready-to-use rule file is provided: [`AGENTS.md`](AGENTS.md). Drop it in your
repo root, or merge its contents into an existing `AGENTS.md`:

```bash
# use the provided file as-is
cp AGENTS.md ./AGENTS.md

# or merge into an existing one
cat AGENTS.md >> AGENTS.md
```

Make the engine available (clone the repo so `scripts/generate_tokens.py` resolves):

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
```

## Use · 使用

In a Codex session, ask:

> generate a tinted UI token system from #2563EB and show me the preview

Codex runs the script and returns `tokens.css` + `preview.html`. Codex executes
the command directly, so no extra wiring is needed beyond the `AGENTS.md` entry.
