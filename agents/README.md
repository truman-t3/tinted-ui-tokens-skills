# Agent Compatibility · 各 Agent 接入索引

**tinted-ui-tokens（品牌色 UI 设计 Token）** is agent-agnostic: the engine
(`scripts/generate_tokens.py`) is plain Python, and the instructions live in
[`INSTRUCTIONS.md`](../INSTRUCTIONS.md) (paste-ready for any agent). This folder
holds the per-agent wiring — where to put the rule and how to invoke the engine.

`tinted-ui-tokens（品牌色 UI 设计 Token）` 与具体 agent 无关：引擎
（`scripts/generate_tokens.py`）是纯 Python，指令在
[`INSTRUCTIONS.md`](../INSTRUCTIONS.md)（可直接粘贴进任意 agent）。本目录给出
各 agent 的接入方式——规则文件放哪、引擎怎么调用。

| Agent | Rule / Command format | Install location | Doc |
| --- | --- | --- | --- |
| Claude Code | `SKILL.md` (skills) | `~/.claude/skills/tinted-ui-tokens/` | [claude-code](claude-code/) |
| Cursor | `.mdc` rule | `.cursor/rules/` or `~/.cursor/rules/` | [cursor](cursor/) |
| OpenAI Codex | `AGENTS.md` / `codex.md` | repo root or `~` | [codex](codex/) |
| Cline | `.clinerules` / `.cline/rules/*.md` | project or `~/.cline/rules/` | [cline](cline/) |
| Aider | `CONVENTIONS.md` (`--read`) | repo root | [aider](aider/) |
| WindSurf | `.windsurfrules` | repo root or `~` | [windsurf](windsurf/) |
| GitHub Copilot | `copilot-instructions.md` | `.github/` | [copilot](copilot/) |
| Gemini CLI | `GEMINI.md` | repo root or `~` | [gemini-cli](gemini-cli/) |

The engine requires **Python 3.10+** and has **no external dependencies**.
引擎需 **Python 3.10+**，**无外部依赖**。
