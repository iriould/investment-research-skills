# Industry Research / 行业研究

一级市场 PE 投资行业研究。分析行业定义与边界、市场规模、竞争格局、核心技术、价值链、政策监管、技术趋势，提炼投资逻辑。

## When to Use

用户说"行业研究"、"行业分析"、"行业调研"、"industry research"、"sector analysis"时使用。

## Quick Start

```
<行业名称或关键词>
```

示例：
```
AI推理引擎
新能源汽车动力电池
```

## Workflow

| Step | 内容 | 说明 |
|------|------|------|
| 0 | 读取配置与协作模式 | 搜索工具、协作模式（本地/飞书） |
| 1 | 行业定义与边界 | 行业分类、定义、边界界定 |
| 2 | 市场规模与增长 | TAM/SAM/SOM、增长驱动、增长预测 |
| 3 | 竞争格局地图 | 市场参与者分类、集中度、关键玩家画像 |
| 4 | **核心技术拆解** | 技术栈分解、架构模式、关键挑战、成熟度映射、开源 vs 专有 |
| 5 | 价值链分析 | 上中下游结构、价值分配、技术控制点 |
| 6 | 政策与监管 | 监管框架、政策趋势、技术监管 |
| 7 | 技术趋势 | 当前格局、新兴趋势、技术投资机会 |
| 8 | 投资逻辑提炼 | 投资机会、风险、技术投资逻辑、关键判断 |

### Core Highlight: Core Technology Decomposition (Step 4)

技术驱动型行业研究的核心步骤，包含 5 个子维度：

1. **技术栈分解** — 行业依赖的核心技术组件和层次（例：AI → 基础模型层 / 推理引擎层 / 应用层）
2. **架构模式** — 行业主流技术架构和设计范式
3. **关键技术挑战** — 当前技术瓶颈、攻关方向、突破可能带来的变革
4. **技术成熟度映射** — 各子领域在成熟度曲线上的位置，对投资时机的影响
5. **开源 vs 专有生态** — 核心开源项目影响力、专有技术壁垒、开源对商业化的影响

### Industry Canvas

提供一页纸行业画布模板，适合投委会快速讨论。参考：`references/industry-canvas.md`

## Output

1. **行业定义与边界** — 清晰的行业范围界定
2. **市场规模与增长** — 量化的市场数据和增长逻辑
3. **竞争格局地图** — 关键玩家和竞争态势
4. **核心技术拆解** — 技术栈、架构、挑战、成熟度、生态
5. **价值链分析** — 价值创造和分配，技术控制点
6. **政策与监管** — 监管框架和政策趋势
7. **技术趋势** — 技术演进方向和投资机会
8. **投资逻辑** — 投资机会、风险、关键判断

## Prerequisite & Follow-up Skills

| 方向 | Skill | 说明 |
|------|-------|------|
| 前置 | 无 | 行业研究是投研流程的起点 |
| 后续 | [company-research](../company-research/) | 基于行业理解，深入研究目标公司 |
| 后续 | [critical-questions](../critical-questions/) | 对行业研究中的不确定领域提出关键问题 |
| 后续 | [competitive-analysis](../competitive-analysis/) | 对行业中的关键竞对进行深度对比 |

## Configuration

首次运行时自动引导配置搜索工具和协作模式。详见 `references/search-policy.md` 和 `references/collaboration-policy.md`。

## File Structure

```
industry-research/
├── SKILL.md                          # Skill 定义与工作流
├── references/
│   ├── collaboration-policy.md       # 协作模式选择规则
│   ├── industry-canvas.md            # 一页纸行业画布模板
│   ├── lark-collaboration.md         # 飞书 CLI 操作指南
│   ├── search-policy.md              # 搜索工具路由策略
│   └── value-chain.md                # 价值链分析框架（结构、分配、技术控制点）
└── scripts/
    └── config_manager.py             # 运行时配置读写
```



