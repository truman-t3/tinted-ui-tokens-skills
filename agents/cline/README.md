# tinted-ui-tokens on Cline (VS Code)

Cline reads project rules from `.clinerules` / `.cline/rules/*.md` and global rules
from `~/.cline/rules`.

## Install · 安装

Copy the instruction into a Cline rule file:

```bash
# project rule
cp INSTRUCTIONS.md <your-project>/.cline/rules/tinted-ui-tokens.md

# or global rule
cp INSTRUCTIONS.md ~/.cline/rules/tinted-ui-tokens.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens ~/.cline/skills/tinted-ui-tokens
```

## Use · 使用

Ask Cline:

> 用 #2563EB 出一套染色 Token 系统

Cline follows `INSTRUCTIONS.md`, runs `scripts/generate_tokens.py`, and shows the
outputs.
