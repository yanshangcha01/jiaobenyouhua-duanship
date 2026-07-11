# AI 分镜脚本优化师 · Storyboard Optimizer

> 把文学剧本 / 故事描述，一键转化为**结构化、可拍摄、且能直接喂给 AI 绘图 / 视频工具**的分镜脚本。

[English](#english) | [中文](#中文)

---

## 中文

### 这是什么

一个轻量的命令行工具 + Python 库，帮助创作者快速产出专业级分镜脚本。它遵循影视工业标准，把"剧本 → 分镜"的繁琐过程自动化，并额外为每个镜头生成可直接用于 Midjourney / Stable Diffusion / 即梦 AI 等工具的**叙事式绘图提示词**。

核心理念（详见 [`GUIDE.md`](./GUIDE.md)）：

> **AI 分镜脚本优化师 = 半个影视导演 + 半个 AI 工程师 + 一个质量控制员**

### 特性

- 🎬 **结构化分镜**：标准字段（序号 / 时长 / 景别 / 镜头运动 / 画面描述 / 台词 / 音效 / 转场 / 备注）
- 🤖 **AI 驱动**：基于 OpenAI 兼容大模型，自动拆解镜头、补全专业术语
- 🖼️ **绘图提示词**：为每个镜头生成英文叙事式 `image_prompt`，开箱即可丢进 AI 绘图工具
- 🪄 **启发式降级**：未配置 API Key 也能跑，输出结构骨架，开箱即用
- 📦 **多格式导出**：Markdown（给人看）/ CSV（给表格）/ JSON（给程序）
- 🔌 **兼容性强**：支持 OpenAI 及任意 OpenAI 兼容端点（DeepSeek、通义、本地 Ollama 等）

### 安装

```bash
git clone https://github.com/your-org/ai-storyboard-optimizer.git
cd ai-storyboard-optimizer
pip install -e .
```

### 使用

```bash
# 基本用法（启发式模式，无需 Key）
storyboard examples/sample_script.txt

# 配置 AI（推荐）
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可替换为兼容端点
export OPENAI_MODEL="gpt-4o-mini"
storyboard examples/sample_script.txt -t "雨夜侦探" -s " film noir 黑色电影" -o board.md

# 其他格式
storyboard input.txt -f csv  -o board.csv
storyboard input.txt -f json -o board.json

# 从 stdin 读取
cat script.txt | storyboard -
```

作为 Python 库使用：

```python
from storyboard.generator import StoryboardGenerator
from storyboard.exporters import to_markdown

gen = StoryboardGenerator()  # 读取 OPENAI_API_KEY 环境变量
sb = gen.generate("夜色中，侦探走进酒吧。", title="雨夜侦探")
print(to_markdown(sb))
```

### 项目结构

```
ai-storyboard-optimizer/
├── src/storyboard/
│   ├── models.py        # 数据结构：Shot / Storyboard
│   ├── prompts.py       # 提示词模板（提示词万能公式）
│   ├── generator.py     # 生成核心（LLM + 启发式降级）
│   ├── exporters.py     # Markdown / CSV / JSON 导出
│   └── cli.py           # 命令行入口
├── examples/            # 示例脚本与输出
├── tests/               # 基础测试
├── GUIDE.md             # AI 分镜脚本优化师能力指南（必读）
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── pyproject.toml
```

### 路线图

- [ ] 角色一致性：基于 seed / 参考图锁定跨镜头视觉
- [ ] 分场式批量生成（多 Agent 协同）
- [ ] Web UI / 插件（剪映、Blender 预演联动）
- [ ] 更多语言与风格预设

---

## English

### What is this

A lightweight CLI + Python library that turns a literary script / story description into a
**structured, shootable storyboard** — and generates a narrative-style `image_prompt` per shot
that you can drop straight into Midjourney / Stable Diffusion / Dreamina.

### Install & Run

```bash
pip install -e .
export OPENAI_API_KEY="sk-..."
storyboard examples/sample_script.txt -t "Rainy Detective" -o board.md
```

No API key? It still runs in heuristic mode and emits a structural skeleton.

### License

MIT — see [LICENSE](./LICENSE).

---

## 致谢 / Acknowledgements

方法学参考《AI 分镜脚本优化师能力指南》（[`GUIDE.md`](./GUIDE.md)）。
