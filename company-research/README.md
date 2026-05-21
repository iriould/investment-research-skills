# Company Research / 公司尽调研究

一级市场 PE 投资公司尽调研究。加载公司资料，进行业务与技术深度分析，回答客户核心问题，生成投资研究报告。

## When to Use

用户说"公司研究"、"尽调"、"公司分析"、"投研"、"company research"、"due diligence"时使用。

## Quick Start

```
<公司名称> <资料目录路径>
```

示例：
```
智谱AI ./data/智谱AI/
```

## Workflow

| Step | 内容 | 说明 |
|------|------|------|
| 0 | 读取配置与协作模式 | 搜索工具、协作模式（本地/飞书） |
| 1 | 加载文档 | `doc_loader.py` 读取 PDF/DOCX/XLSX/CSV/JSON/TXT/MD |
| 2 | 内容精炼 | 提取公司基本信息、核心业务、财务数据、团队、技术 |
| 3 | 业务与技术深度分析 | 公司概况 → 业务分析 → 财务分析 → **核心技术深度分析** |
| 4 | 回答客户问题 | 分层回答：✅ 已解决 / ⚠️ 待确认 / ❌ 未涉及 |
| 5 | 生成报告 | 结构化投资研究报告 |

### Core Highlight: Tech Depth Analysis (Step 3.4)

技术驱动型公司尽调的核心环节，包含 5 个子维度：

1. **技术架构拆解** — 核心技术栈、架构模式、关键组件、数据流、技术选型理由
2. **技术护城河评估** — 核心壁垒、壁垒深度、可持续性、开源依赖风险
3. **研发能力评估** — 团队规模与背景、研发投入占比、迭代速度、CTO 履历
4. **技术差异化** — 与竞品的架构差异、优势体现、劣势和改进方向
5. **技术债务与风险** — 技术成熟度、扩展性瓶颈、路线依赖、安全合规

## Output

1. **公司画像** — 结构化的公司信息摘要
2. **业务与技术深度分析** — 业务分析 + 核心技术深度分析
3. **客户问题回答结果** — 分层回答（✅/⚠️/❌）
4. **核心洞察** — 5-8 个关键发现
5. **投资建议** — 建议推进/谨慎推进/暂缓推进/不建议推进

报告模板参考：`references/output-template.md`

## Prerequisite & Follow-up Skills

| 方向 | Skill | 说明 |
|------|-------|------|
| 前置 | [industry-research](../industry-research/) | 先了解行业背景，再研究公司更有针对性 |
| 后续 | [critical-questions](../critical-questions/) | 识别盲区、交叉验证、提出关键问题 |
| 后续 | [competitive-analysis](../competitive-analysis/) | 与竞对进行深度对比分析 |

## Configuration

首次运行时自动引导配置搜索工具和协作模式。详见 `references/search-policy.md` 和 `references/collaboration-policy.md`。

## File Structure

```
company-research/
├── SKILL.md                          # Skill 定义与工作流
├── references/
│   ├── collaboration-policy.md       # 协作模式选择规则
│   ├── lark-collaboration.md         # 飞书 CLI 操作指南
│   ├── methodology.md                # 投资研究方法论（证据分级、盲区类型、行业指标）
│   ├── output-template.md            # 报告输出模板
│   ├── red-flags.md                  # 红旗检查清单（6 大类）
│   └── search-policy.md              # 搜索工具路由策略
└── scripts/
    ├── config_manager.py             # 运行时配置读写
    └── doc_loader.py                 # 文档加载器（PDF/DOCX/XLSX/CSV/JSON/TXT/MD）
```

## Dependencies

`doc_loader.py` 依赖以下 Python 包（首次运行自动安装）：

```
pymupdf      # PDF 解析（自动检测 PPT 源 vs Word 源 PDF）
pillow       # 图像处理
pytesseract  # OCR
openpyxl     # Excel 读取（智能表分类：利润表/资产负债表/现金流量表/估值模型）
python-docx  # Word 文档读取
```



