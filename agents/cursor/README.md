# tinted-ui-tokens on Cursor

Cursor reads rules from `.cursor/rules/` (project) or `~/.cursor/rules/` (global).
A ready-to-use rule file is provided: [`tinted-ui-tokens.mdc`](tinted-ui-tokens.mdc).

## Install · 安装

Copy the rule into your rules directory:

```bash
# project scope
cp tinted-ui-tokens.mdc <your-project>/.cursor/rules/

# or global scope
cp tinted-ui-tokens.mdc ~/.cursor/rules/
```

Also make the engine available — clone the repo or copy `scripts/generate_tokens.py`
so Cursor can run it:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ~/.cursor/skills/tinted-ui-tokens
```

## Use · 使用

The rule has `alwaysApply: false`; invoke by mentioning the task, e.g.:

> generate a tinted UI token system from #2563EB

Cursor follows the instruction, runs `scripts/generate_tokens.py`, and returns
`tokens.css` + `preview.html`.
