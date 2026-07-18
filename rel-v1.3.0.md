## What's New / 新增内容

- **README「一键安装」区**：按 8 个 agent（Claude Code / Cursor / OpenAI Codex / Cline / Aider / WindSurf / GitHub Copilot / Gemini CLI）列出复制即用的安装命令，clone 仓库后直接把规则文件指向对应 agent 即可。
- **真实浏览器渲染预览图** `assets/preview.png`：明暗双主题并排实拍（品牌色 `#2563EB`），比 SVG 更直观。

### 这个 skill 是做什么的
输入**一个品牌色**，自动生成一整套「染色中性色」设计 Token 系统（`tokens.css` + `preview.html`，明暗双主题）。核心原则：**任何地方都不出现纯 `#FFFFFF` / `#000000` / `#808080`**——每个背景、表面、边框、文字层级、阴影、语义色都带上一小撮品牌色的温度，让 UI 不再显廉价。

### 为什么用
- 品牌无关：任意 hex，不是写死的两套配色。
- 跨 agent：引擎是纯 Python 脚本，指令是一份可直接粘贴的 Markdown，已为 8 个主流 AI 编程 agent 备好现成规则文件。
- 零依赖：仅 Python 标准库，无需 `pip install`。
- 免费：MIT 协议。

### 适合谁
设计师 / 前端 / 团队 —— 想快速拿到高级、统一品牌感的配色，又不想手调几十个灰阶。

```bash
git clone https://github.com/truman-t3/tinted-ui-tokens-skills ./tinted-ui-tokens-skills
python ./tinted-ui-tokens-skills/scripts/generate_tokens.py --brand "#2563EB" --name "Acme" --out "./out"
```

完整历史见 CHANGELOG.md。
