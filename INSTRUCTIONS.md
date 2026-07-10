# Tinted UI Tokens — Skill Instructions · 技能指令

> Agent-neutral instruction set for **tinted-ui-tokens（染色 UI 设计令牌）**.
> Paste this file's contents into your agent's rule / memory / command file
> (see [`agents/`](agents/) for per-agent wiring). The engine is
> `scripts/generate_tokens.py` — pure Python standard library, runs anywhere
> Python 3.10+ is available (Windows / macOS / Linux).
>
> 这是与具体 agent 无关的「技能指令」。把本文件内容粘贴进你所用 agent 的规则 /
> 记忆 / 命令文件即可（各 agent 接入方式见 [`agents/`](agents/)）。引擎脚本
> `scripts/generate_tokens.py` 仅用 Python 标准库，Python 3.10+ 任意系统可跑。

## What it does · 它能做什么

Turn one brand color (hex) into a complete, production-ready **brand-tinted
design-token system**. No pure neutral colors anywhere (`#FFFFFF`, `#000000`,
`#808080`): every background, surface, border, text layer, shadow, semantic
color, gradient, and icon picks up a few percent of the brand's temperature, so
the UI reads as "designed" instead of "assembled".

输入一个品牌色（hex），自动生成一套完整、可直接上线的「染色中性色」设计 Token
系统。任何地方都不使用纯中性色（`#FFFFFF` / `#000000` / `#808080`）：每一个背景、
表面、边框、文字层级、阴影、语义色、渐变与图标，都带上一小撮品牌色的温度。

Method distilled from the essay 《你的UI廉价，错在颜色》.

## When to use · 何时使用

- User provides a brand color / hex and wants a design system, CSS variables, or a theme.
  · 用户提供品牌色 / hex，并想要一套设计系统、CSS 变量或主题。
- User wants to make an existing UI look more premium ("my UI looks cheap").
  · 用户想让现有 UI 显得更高级（"我的界面看起来很廉价"）。
- User asks for tokens for light + dark mode, semantic colors, or a branded palette.
  · 用户需要明 / 暗双模式、语义色或品牌化配色的 Token。
- User wants a quick visual proof (preview) of a color direction.
  · 用户想要某个配色方向的快速可视化预览。

## Workflow · 工作流

### 1. Collect the minimum input · 收集最小输入

Only the brand color is required. Ask for it if missing:
只需要品牌色。若缺失则询问：

- **Brand color** (hex like `#2563EB`) — defines the system's temperature.
  · 品牌色（如 `#2563EB`）——决定系统的温度。
- Optional: product / brand name (preview label only).
  · 可选：产品 / 品牌名（仅作预览页标签）。
- Optional: output directory (default current working directory).
  · 可选：输出目录（默认当前工作目录）。

Do not over-ask. One hex is enough to produce the whole system.
不要追问过多。一个 hex 就足以生成整套系统。

### 2. Run the generator · 运行生成器

Run the script with the managed or system Python:
用托管或系统 Python 运行脚本：

```bash
python scripts/generate_tokens.py --brand "#2563EB" --name "Acme" --out "./out"
```

Flags · 参数：

- `--brand` (required): any hex color. · 必填，任意 hex 颜色。
- `--name` (optional): label shown in the preview header. · 预览页顶部标签。
- `--out` (optional): output folder, created if missing. · 输出目录，自动创建。
- `--format css|html|both` (optional, default `both`). · 输出格式。

Outputs · 产物：

- `tokens.css` — drop-in `:root` + `[data-theme="dark"]` custom properties.
  · 即用的 `:root` 与 `[data-theme="dark"]` 自定义属性。
- `preview.html` — self-contained live demo with a light / dark toggle.
  · 自包含实时预览（明 / 暗切换）。

The script prints the detected temperature (warm / cool / balanced) and key values.
脚本会打印检测到的温度（暖 / 冷 / 中性）与关键数值。

### 3. Present the result · 呈现结果

Show `preview.html` (opens in a browser / preview panel) and `tokens.css`. Tell
the user the detected temperature and that every neutral is brand-tinted. Offer
to regenerate with a different brand color or to hand-tune specific tokens.
展示 `preview.html`（在浏览器 / 预览面板打开）与 `tokens.css`，说明检测到的温度与
"所有中性色均被染色"这一事实。可主动提议换品牌色重生成，或手动微调个别 Token。

### 4. Hand-tuning (optional) · 手动微调（可选）

Consult [`references/principles.md`](references/principles.md) before editing. Common tweaks:
改之前先读 [`references/principles.md`](references/principles.md)。常见调整：

- More/less tint: change the blend factor in `build_tokens()` (e.g. `bg` uses `0.035`).
  · 染色强弱：改 `build_tokens()` 的混合系数（`bg` 用 `0.035`）。
- Semantic nudge strength: the `0.06` mix factor in `semantic()`.
  · 语义色偏移幅度：`semantic()` 里的 `0.06` 混合系数。

## Output contract · 输出约定

`tokens.css` defines, for `:root` / `[data-theme="light"]` and `[data-theme="dark"]`:
`tokens.css` 为 `:root` / `[data-theme="light"]` 与 `[data-theme="dark"]` 定义：

- `--color-brand`, `--color-brand-subtle`
- `--color-bg`, `--color-surface`, `--color-surface-2`, `--color-border`, `--color-border-strong`
- `--color-text`, `--color-text-2`, `--color-text-muted`
- `--color-error` / `-subtle`, `--color-warning` / `-subtle`, `--color-success` / `-subtle`
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`

No pure `#FFFFFF`, `#000000`, or `#808080` is emitted anywhere.
任何位置都不会输出纯 `#FFFFFF`、`#000000` 或 `#808080`。

## References · 参考

- [`references/principles.md`](references/principles.md) — design rules the generator enforces, plus the grayscale test.
  · 生成器遵循的设计原则，以及去饱和灰度测试。
