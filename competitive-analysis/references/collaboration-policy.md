# 协作模式配置策略

本文档定义 investment-research standalone skill 的本地 / 飞书协作模式选择规则。协作模式应像搜索工具一样可配置、可记忆，避免每次运行都重复询问。

## 配置来源

协作配置按以下优先级读取：

1. `config/investment-research-config.json` 中保存的选择
2. 本 skill 运行期配置中的 `collaboration_mode`、`lark_reference_mode`
3. 如果仍未配置、为空或值为 `ask`，首次运行时询问用户，并写入本 skill 运行期配置

运行期配置文件建议结构见 `search-policy.md`。

## 协作模式

`collaboration_mode` 支持以下值：

- `local`：默认本地模式，只输出 Markdown 文件
- `lark`：默认飞书协作模式，输出飞书云文档并保留本地备份
- `ask`：首次运行时询问用户，保存选择后后续自动沿用

首次询问时建议使用简短问题：

> 本 skill 后续默认使用哪种协作模式？选择“本地模式”会生成本地 Markdown；选择“飞书协作模式”会读写飞书云文档并保留本地备份。

用户选择后，通过 `scripts/config_manager.py` 写入 `config/investment-research-config.json`。如果目录或文件不存在，创建它；如果文件已有搜索配置，只更新协作相关字段，保留其他字段。

推荐使用脚本读写配置：

```bash
python scripts/config_manager.py get
python scripts/config_manager.py set --collaboration-mode "local" --lark-reference-mode "ask"
```

## 飞书资料读取偏好

`lark_reference_mode` 支持以下值：

- `ask`：使用飞书协作时，每次询问是否读取飞书参考资料
- `always`：默认询问用户提供飞书 URL、token 或关键词，并尝试读取资料
- `never`：不主动读取飞书资料，除非用户明确提供飞书链接或要求读取

即使 `collaboration_mode` 为 `lark`，以下操作仍需要用户确认：

- 写入已有飞书文档
- 发送飞书消息
- 覆盖或删除任何飞书内容

## 回退规则

如果飞书工具不可用、权限不足、读取失败或写入失败：

1. 明确说明失败原因
2. 回退到本地 Markdown 输出
3. 保留报告内容，不因飞书失败中断研究流程
4. 如需用户处理权限，给出最小必要操作建议

## 子代理约束

并行搜索或分析子代理不得执行飞书写入、发送消息或最终报告发布。子代理只返回结构化分析结果，由主代理统一决定输出方式并执行最终写入。






