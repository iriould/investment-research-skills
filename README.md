# PE/VC Investment Research Skills

一级市场股权投资（PE/VC）研究 Claude Code / Codex 技能集——公司尽调、行业研究、竞对分析、关键问题识别。支持本地 Markdown 与飞书协作双模式。

## Skills Overview

| Skill | 中文名 | 用途 | 触发关键词 |
|-------|--------|------|-----------|
| [industry-research](./industry-research/) | 行业研究 | 行业全景、市场规模、投资逻辑提炼 | "行业研究", "industry research" |
| [company-research](./company-research/) | 公司尽调研究 | 公司画像、业务与技术深度分析、投资报告 | "公司研究", "尽调", "due diligence" |
| [competitive-analysis](./competitive-analysis/) | 竞对分析 | 六维画像对比、技术深度子维度、威胁评估 | "竞对分析", "competitive analysis" |
| [critical-questions](./critical-questions/) | 关键问题识别 | 盲区检测、交叉验证、投决必知问题提出 | "识别盲区", "关键问题", "critical questions" |

## Recommended Workflow

```
industry-research ──→ company-research ──→ critical-questions
                                    └──→ competitive-analysis
```

1. **行业研究**先行——建立行业认知框架
2. **公司尽调**深入——构建公司画像，深度分析业务与技术
3. **关键问题**或**竞对分析**跟进——识别盲区、验证壁垒、评估竞争威胁

## Installation

Install all skills globally:

```bash
npx skills add iriould/investment-research-skills --skill '*' -g
```

Install for a specific agent:

```bash
npx skills add iriould/investment-research-skills --skill '*' -g -a codex
npx skills add iriould/investment-research-skills --skill '*' -g -a claude-code
```

Install a single skill:

```bash
npx skills add iriould/investment-research-skills --skill company-research -g
npx skills add iriould/investment-research-skills --skill industry-research -g
```

After installation, restart your agent session so the skill list is refreshed.

## Configuration

首次运行时，skill 会引导配置以下选项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `primary_search_tools` | 通用搜索工具 | `auto` |
| `technical_search_tools` | 技术搜索工具 | `auto` |
| `search_language_bias` | 搜索语言偏好 | `zh-first` |
| `collaboration_mode` | 协作模式（local / lark） | `ask` |
| `lark_reference_mode` | 飞书参考模式 | `ask` |

配置文件位置：`config/investment-research-config.json`（每个 skill 自身目录下）。

## Collaboration Modes

| 模式 | 输入 | 输出 |
|------|------|------|
| 本地模式 | 本地文件目录 | 本地 Markdown 文件 |
| 飞书协作模式 | 本地文件 + 飞书云文档 | 飞书云文档 + 本地备份 |

飞书协作模式需要 [lark-cli](https://github.com/iriould/lark-cli) 工具。如果飞书工具不可用，自动回退到本地模式。

## Shared Infrastructure

以下文件在 4 个 skill 中各保留一份完整副本，确保每个 skill 可独立安装运行：

- `references/collaboration-policy.md` — 协作模式选择规则
- `references/lark-collaboration.md` — 飞书 CLI 操作指南
- `references/search-policy.md` — 搜索工具路由策略
- `scripts/config_manager.py` — 运行时配置读写

## Dependencies

`doc_loader.py`（company-research 和 critical-questions 使用）依赖以下 Python 包，首次运行时自动安装：

```
pymupdf
pillow
pytesseract
openpyxl
python-docx
```

## Project Structure

```
investment-research-skills/
├── README.md
├── LICENSE
├── .gitignore
│
├── company-research/
│   ├── README.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── collaboration-policy.md
│   │   ├── lark-collaboration.md
│   │   ├── methodology.md
│   │   ├── output-template.md
│   │   ├── red-flags.md
│   │   └── search-policy.md
│   └── scripts/
│       ├── config_manager.py
│       └── doc_loader.py
│
├── competitive-analysis/
│   ├── README.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── collaboration-policy.md
│   │   ├── comparison-framework.md
│   │   ├── lark-collaboration.md
│   │   ├── search-policy.md
│   │   └── search-sources.md
│   └── scripts/
│       └── config_manager.py
│
├── critical-questions/
│   ├── README.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── collaboration-policy.md
│   │   ├── industry-profiles.json
│   │   ├── lark-collaboration.md
│   │   ├── search-policy.md
│   │   └── tech-question-framework.md
│   └── scripts/
│       ├── blindspots.py
│       ├── config_manager.py
│       └── doc_loader.py
│
└── industry-research/
    ├── README.md
    ├── SKILL.md
    ├── references/
    │   ├── collaboration-policy.md
    │   ├── industry-canvas.md
    │   ├── lark-collaboration.md
    │   ├── search-policy.md
    │   └── value-chain.md
    └── scripts/
        └── config_manager.py
```

## License

MIT


