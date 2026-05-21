# 搜索工具配置与路由策略

本文档定义 investment-research standalone skill 的统一搜索策略。所有行业研究、公司研究、竞对分析、关键问题识别流程都应优先遵循本策略，而不是绑定某个固定搜索工具。

## 配置来源

搜索配置按以下优先级读取：

1. `config/investment-research-config.json` 中保存的选择
2. 本 skill 运行期配置中的 `primary_search_tools`、`technical_search_tools`、`search_language_bias`
3. 如果仍未配置、为空或值为 `ask`，首次运行时询问用户，并写入本 skill 运行期配置
4. 如果值为 `auto`，自动使用当前代理环境（Claude Code / Codex）中已配置、已授权、可调用的搜索工具

运行期配置文件建议结构：

```json
{
  "primary_search_tools": "auto",
  "technical_search_tools": "auto",
  "search_language_bias": "zh-first",
  "collaboration_mode": "local",
  "lark_reference_mode": "ask"
}
```

如果配置文件不存在，或相关值为 `ask` / 空值，应只询问用户一次，并通过 `scripts/config_manager.py` 写入 `config/investment-research-config.json`。后续运行自动沿用，除非用户明确要求修改配置。若用户选择 `auto`，也写入配置，表示后续默认自动使用当前环境已配置搜索工具。

推荐使用脚本读写配置：

```bash
python scripts/config_manager.py get
python scripts/config_manager.py set --primary-search-tools "auto" --technical-search-tools "auto" --search-language-bias "zh-first"
```

## 搜索工具选择

- `primary_search_tools` 用于行业、公司、融资、市场规模、政策、竞对、客户评价等通用搜索。
- `technical_search_tools` 用于技术文档、开源项目、代码仓库、API、SDK、benchmark、技术评测等搜索。
- `search_language_bias` 控制查询词语言：
  - `zh-first`：中文资料优先，必要时补英文资料
  - `en-first`：英文资料优先，必要时补中文资料
  - `auto`：根据公司/行业/市场区域判断

当配置为具体工具名列表时，优先按列表顺序使用。若某工具不可用、未授权、报错或响应过慢，记录失败原因并切换到下一个可用工具。不要因为单个搜索工具失败而中断整个投研流程。

当配置为 `auto` 时：

1. 优先使用用户当前代理环境（Claude Code / Codex）中已配置的搜索工具。
2. 对中文 PE/VC 前期研究，优先选择适合中文网页、新闻、产业数据库、创投媒体和政策资料的工具。
3. 对海外公司或全球市场，优先选择英文网页和全球资料覆盖更好的工具。
4. 对技术信息，优先选择能读取技术文档、代码仓库、开源项目和 benchmark 的工具。

## 证据标准

所有关键事实都必须记录：

- 来源名称或 URL
- 发布时间；无法确认发布时间时记录获取日期
- 可信度：高 / 中 / 低
- 判断类型：事实 / 推断 / 待验证

优先级建议：

1. 公司官方文件、监管披露、招股书、年报、审计材料
2. 权威行业报告、政府/协会数据、头部咨询机构报告
3. 主流媒体、创投媒体、第三方评测、客户访谈
4. 社交媒体、论坛、二手转载，仅作为低可信线索

## 并行搜索约束

并行搜索子代理只负责只读证据收集，不负责写最终报告、写飞书文档、发送消息或请求用户确认。

每个搜索子代理必须有明确边界：

- 最多围绕 1 个主题或 1 个公司搜索
- 默认最多执行 3-5 个查询
- 搜索失败时返回已有发现和信息缺口
- 不能无限追加查询词
- 最终必须返回结构化结果

子代理返回格式：

```markdown
## 搜索主题

## 已执行查询

## 关键发现

| 事实 | 来源 | 时间 | 可信度 | 备注 |
|------|------|------|--------|------|

## 信息缺口

## 建议补查
```

主代理负责综合所有搜索结果，形成投资判断和最终报告。






