# Contributing · 贡献指南

Thanks for wanting to improve **tinted-ui-tokens-skills**! This document is short
on purpose.

## How to contribute · 如何贡献

1. **Open an issue first** for anything non-trivial (new agent support, algorithm
   change, doc fix) so we can align before writing code.
2. **Fork & branch** from `main`: `git checkout -b fix/short-description`.
3. **Keep the skill agent-neutral.** The engine (`scripts/generate_tokens.py`)
   must stay identical across agents. Agent-specific differences live only in
   `agents/<agent>/` (rule-file location, install snippet).
4. **Run the local checks** before pushing:

   ```bash
   python scripts/validate_skill.py   # SKILL.md frontmatter (package_skill.py rules)
   python scripts/smoke_test.py       # generator smoke + extreme-color robustness + semantic sanity
   ```

   These are the exact checks CI runs (see `.github/workflows/validate.yml`), so
   "passes locally" == "passes CI". CI must stay green.

5. **Update docs together:** if you change the slug / skill name, update every
   reference in `SKILL.md`, `README.md`, `INSTRUCTIONS.md`, and all
   `agents/*/README.md`. Keep filenames and the repo slug in sync.

## Naming convention · 命名规范

- Repo slug, `SKILL.md` `name:`, and any bundled rule-file names must all share
  the same `tinted-ui-tokens-skills` base (hyphen-case). Don't let them drift.
- Keep `README.md` bilingual (中文 + English).

## Releasing · 发版

Maintainers bump the version in `CHANGELOG.md`, tag `vX.Y.Z` on `main`, and create
a GitHub Release. The license stays MIT.
