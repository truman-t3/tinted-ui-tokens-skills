# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [1.4.0] - 2026-07-18

### Added
- **WCAG 2.1 contrast auto-check + compensation.** Every text-on-surface pair
  is measured with the relative-luminance formula; if it falls below AA
  (4.5:1 normal / 3:1 muted) the text is nudged along its HSL lightness axis
  until it passes — so readability always wins and the brand hue-lean is kept
  wherever lightness does not hit an extreme. The CLI prints the final three
  contrast ratios (light / dark / on-brand).
- **`--color-on-brand` token.** A readable text/icon color to place ON
  `--color-brand` (tinted near-white or near-black, never pure `#FFF`/`#000`),
  auto-chosen by contrast. Used by the new primary button in `preview.html`.
- **Adjustable tint strength.** `--tint-strength subtle|normal|strong` scales
  every blend factor uniformly (0.6 / 1.0 / 1.6) — stronger brand presence
  without editing code. WCAG compensation still runs afterwards.
- **Industry export formats.** `--format` now also emits W3C DTCG
  `tokens.json`, `tailwind.config.js`, and `_tokens.scss`; `all` = css + html +
  json + tailwind + scss. `css` / `html` / `both` stay backward compatible.
- **Numeric golden-value regression test.** `scripts/smoke_test.py` now locks 9
  key tokens for `#2563EB` (normal) to exact hex values and asserts the three
  critical WCAG AA contrast pairs (>= 4.5:1), catching silent numeric drift
  like the old HSL→RGB channel-mapping bug.

## [1.3.1] - 2026-07-18

### Fixed
- Dark-mode topbar title text in `preview.html` was invisible because
  `.brand-meta b` only inherited `color` from `body`; the inherited value
  resolved against the light theme and stayed dark on the dark card surface.
  Added explicit `color: var(--color-text);` so the title re-resolves in dark
  mode and remains readable.
- Regenerated `assets/preview.png` from the fixed `preview.html` so the README
  preview now shows a legible title in both light and dark halves.
- Updated the English and Chinese README preview captions to note the title
  legibility in both themes, keeping the two sections synchronized.

## [1.2.0] - 2026-07-18

### Added
- `scripts/smoke_test.py` — a shared generator smoke + robustness test run by
  both CI and contributors, so "passes locally" == "passes CI". Covers
  cool/warm/balanced brands, valid-hex assertions, semantic sanity, invalid-input
  rejection, and **extreme/degenerate brands** (pure black/white/gray, short and
  lowercase hex) which must not crash.
- Ready-to-use native rule files for every remaining agent — copy in, no
  hand-assembly: `agents/codex/AGENTS.md`, `agents/aider/CONVENTIONS.md`,
  `agents/windsurf/.windsurfrules`, `agents/cline/.clinerules`,
  `agents/copilot/copilot-instructions.md`, `agents/gemini-cli/GEMINI.md`
  (Cursor already shipped `tinted-ui-tokens-skills.mdc`).
- `assets/preview.svg` — a faithful light + dark preview (built from the real
  `#2563EB` token values), embedded in both README language sections.

### Changed
- CI (`validate.yml`) now delegates to `scripts/smoke_test.py` instead of inline
  bash, adding extreme-color robustness coverage.
- Per-agent READMEs and the `agents/` index now point at the ready-made rule
  files.
- `CONTRIBUTING.md` local-check instructions corrected to reference both
  `validate_skill.py` and `smoke_test.py`.

## [1.1.0] - 2026-07-18

### Added
- `LICENSE` (MIT) — the repository now ships an explicit license file (README
  already declared MIT; the file was missing).
- `CHANGELOG.md` — release history.
- `CONTRIBUTING.md` — contribution guidelines.

### Changed
- `SKILL.md` `name:` synced from `tinted-ui-tokens` to `tinted-ui-tokens-skills`
  so it matches the repository slug.
- Cursor rule file renamed `tinted-ui-tokens.mdc` → `tinted-ui-tokens-skills.mdc`
  to match the slug; the Cursor README references were updated accordingly.

## [1.0.0] - 2026-07-11

### Added
- Initial release: brand-agnostic tinted design-token generator
  (`scripts/generate_tokens.py`).
- `SKILL.md` (WorkBuddy / Claude Code) plus `INSTRUCTIONS.md` (agent-neutral
  core instructions).
- Cross-agent wiring docs under `agents/` for Claude Code, Cursor,
  OpenAI Codex, Cline, Aider, WindSurf, GitHub Copilot, and Gemini CLI.
- `references/principles.md` distilling the essay 《你的UI廉价，错在颜色》.
- GitHub Actions CI (`validate.yml`) running frontmatter + smoke + semantic
  sanity checks.
- Bilingual README with a cross-agent compatibility table.
