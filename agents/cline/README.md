# tinted-ui-tokens-skills on Cline (VS Code)

Cline reads project rules from `.clinerules` / `.cline/rules/*.md` and global rules
from `~/.cline/rules`.

## Install · 安装

A ready-to-use rule file is provided: [`.clinerules`](.clinerules). Drop it in
your project root, or copy it into a Cline rules directory:

```bash
# project root
cp .clinerules <your-project>/.clinerules

# or as a named rule (project / global)
cp .clinerules <your-project>/.cline/rules/tinted-ui-tokens-skills.md
cp .clinerules ~/.cline/rules/tinted-ui-tokens-skills.md
```

Make the engine available:

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ~/.cline/skills/tinted-ui-tokens-skills
```

## Use · 使用

Ask Cline:

> 用 #2563EB 出一套染色 Token 系统

Cline follows `INSTRUCTIONS.md`, runs `scripts/generate_tokens.py`, and shows the
outputs.
