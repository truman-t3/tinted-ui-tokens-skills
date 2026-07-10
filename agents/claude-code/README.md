# tinted-ui-tokens on Claude Code

Claude Code supports the same `SKILL.md` format as WorkBuddy, so the repo's root
`SKILL.md` drops in directly — no conversion needed.

## Install · 安装

Clone the repo into your user-level skills directory:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ~/.claude/skills/tinted-ui-tokens
```

That's it. Claude Code auto-discovers the skill and reads `SKILL.md` (frontmatter
`name` + `description` drive when it triggers).

## Use · 使用

Ask naturally, e.g.:

> 用 `#2563EB` 出一套染色 Token 系统

Claude Code runs `scripts/generate_tokens.py` and shows `preview.html` + `tokens.css`.

## Alternative: `/command`

If you prefer a slash command, copy `SKILL.md` body into
`~/.claude/commands/tinted-ui-tokens.md` (frontmatter optional). Then invoke with
`/tinted-ui-tokens #2563EB`.
