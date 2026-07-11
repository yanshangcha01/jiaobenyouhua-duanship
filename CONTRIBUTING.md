# 贡献指南 / Contributing

感谢你考虑为 **AI 分镜脚本优化师** 贡献力量！

## 如何参与

1. Fork 本仓库并创建分支：`git checkout -b feature/your-idea`
2. 安装开发依赖：`pip install -e .`
3. 运行测试：`python -m pytest tests/` 或 `python tests/test_basic.py`
4. 提交改动并 Push，发起 Pull Request

## 代码规范

- 使用 `src/storyboard/` 包结构，新增能力请保持模块单一职责
- 提示词相关改动请同步更新 `GUIDE.md` 与 `prompts.py`
- 保持中文注释与文档，对外 API 命名使用英文
- 提交信息建议遵循：`feat:` / `fix:` / `docs:` / `chore:` 前缀

## 议题反馈

- Bug 与功能建议请在 Issues 中描述清楚复现步骤与预期行为
- 欢迎补充不同风格 / 平台的分镜预设模板

## 行为准则

请保持友善、专业的交流氛围，尊重每一位贡献者。
