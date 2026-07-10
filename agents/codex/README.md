# tinted-ui-tokens on OpenAI Codex (Codex CLI)

Codex reads instruction files `AGENTS.md` / `codex.md` from the working directory
and can execute shell commands (including the Python engine).

## Install · 安装

Append the skill instructions to your `AGENTS.md` (repo root) — or create one:

```bash
cat INSTRUCTIONS.md >> AGENTS.md
```

Make the engine available (clone the repo so `scripts/generate_tokens.py` resolves):

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ./tinted-ui-tokens
```

## Use · 使用

In a Codex session, ask:

> generate a tinted UI token system from #2563EB and show me the preview

Codex runs the script and returns `tokens.css` + `preview.html`. Codex executes
the command directly, so no extra wiring is needed beyond the `AGENTS.md` entry.
