# Critical Questions / 关键问题识别与提出

对公司资料进行投资盲区识别、交叉验证、技术聚焦的关键问题提出。

## When to Use

用户说"识别盲区"、"提出关键问题"、"交叉验证"、"投研提问"、"关键问题"、"critical questions"时使用。也可在 company-research 之后自动推荐。

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
| 0 | 读取配置与协作模式 | 协作模式（本地/飞书） |
| 1 | 加载文档 | `doc_loader.py` 读取资料目录 |
| 2 | 投资盲区识别 | `blindspots.py` 自动检测 13 类盲区 |
| 3 | 交叉验证 | 数字一致性、逻辑一致性、证据强度、红旗检查 |
| 4 | 关键问题提出 | 按配比生成投决必知问题 |

### Core Highlight: Blindspot Detection Script

`blindspots.py` 是纯文本分析脚本（不调用 LLM），自动检测 7 大类 13 种盲区：

| 盲区类型 | 严重性 |
|----------|--------|
| 产品细节缺失 | 高 |
| 行业关键指标缺失 | 高 |
| 客户集中度风险 / 客户信息完全缺失 | 高 |
| 竞争格局模糊 / 竞争格局不完整 | 中 |
| 退出路径未讨论 | 高 |
| 创始人信息不足 | 中 |
| 技术架构缺失 | 高 |
| 技术性能指标缺失 | 高 |
| 技术壁垒证据缺失 | 高 |
| 研发投入信息缺失 | 中 |
| 技术路线风险未讨论 | 中 |

脚本自动识别行业，匹配行业关键指标。支持 8 个行业 + 通用模式：AI、SaaS、半导体、消费、制造、医疗、新能源、金融科技。

### Question Allocation

| 类别 | 配比 | 内容 |
|------|------|------|
| 技术问题 | 30% | 架构验证、性能核实、壁垒真实性、路线风险、研发能力 |
| 商业问题 | 20% | 模式可持续性、客户集中度、收入质量 |
| 内容问题 | 30% | 信息一致性、数据可靠性、逻辑闭环 |
| 盲区问题 | 20% | 资料未涉及的关键领域、行业必知但缺失的信息 |

### Cross-Validation

证据强度分为 4 级：

| 等级 | 标准 |
|------|------|
| 强证据 | 第三方验证 + 量化数据 |
| 中等证据 | 公司自述 + 部分佐证 |
| 弱证据 | 仅公司自述，无外部验证 |
| 无证据 | 仅有结论，无任何支撑 |

## Output

1. **盲区识别报告** — 所有检测到的盲区，按严重性排序
2. **交叉验证报告** — 不一致、证据不足、红旗信号
3. **关键问题清单** — 按配比和优先级排序（15-25 个问题）
4. **问题汇总表** — 序号、类别、严重性、标题

## Prerequisite & Follow-up Skills

| 方向 | Skill | 说明 |
|------|-------|------|
| 前置 | [company-research](../company-research/) | 先完成公司画像，再识别盲区更有针对性 |
| 后续 | [competitive-analysis](../competitive-analysis/) | 竞争相关问题可通过竞对分析深入 |
| 后续 | [company-research](../company-research/) | 发现重大信息缺口时可回到公司研究补充 |

## Configuration

首次运行时自动引导配置搜索工具和协作模式。详见 `references/search-policy.md` 和 `references/collaboration-policy.md`。

## File Structure

```
critical-questions/
├── SKILL.md                          # Skill 定义与工作流
├── references/
│   ├── collaboration-policy.md       # 协作模式选择规则
│   ├── industry-profiles.json        # 行业画像数据（8 行业 + 通用）
│   ├── lark-collaboration.md         # 飞书 CLI 操作指南
│   ├── search-policy.md              # 搜索工具路由策略
│   └── tech-question-framework.md    # 技术问题框架（5 类技术问题、优先级矩阵）
└── scripts/
    ├── blindspots.py                 # 盲区检测脚本（纯文本分析，无 LLM 调用）
    ├── config_manager.py             # 运行时配置读写
    └── doc_loader.py                 # 文档加载器
```

## Dependencies

`doc_loader.py` 和 `blindspots.py` 依赖以下 Python 包（首次运行自动安装）：

```
pymupdf      # PDF 解析
pillow       # 图像处理
pytesseract  # OCR
openpyxl     # Excel 读取
python-docx  # Word 文档读取
```



