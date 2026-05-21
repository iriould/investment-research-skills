# 飞书协作模式操作指南

> 本文档是 investment-research standalone skill 飞书协作模式的详细操作手册。所有飞书操作通过 `lark-cli` 命令行执行，不引入 Python 飞书 SDK 依赖。

---

## 1. 流程对比

```
本地模式：
  用户 → 本地文件目录 → doc_loader.py → 精炼 → 盲区 → 交叉验证 → 问题 → 回答 → 报告 → 本地 Markdown

飞书协作模式：
  用户 → 本地文件目录 ─┐
       → 飞书云文档 ───┤→ 合并内容 → 精炼 → 盲区 → 交叉验证 → 问题 → 回答 → 报告
                         │                                              ↓
                         │                                    ┌─ 写入已有飞书文档（append）
                         │                                    ├─ 创建新飞书文档 + 发送链接
                         │                                    └─ 本地 Markdown 备份
```

**关键差异**：
- 输入：飞书协作模式可同时使用本地文件和飞书云文档
- 输出：飞书协作模式增加了飞书云文档输出选项
- 中间步骤（精炼→盲区→交叉验证→问题→回答）：两种模式完全一致

---

## 2. lark-cli 命令速查表

仅列出投研场景需要的命令。完整命令说明请参考对应的 lark skill。

### 读取飞书文档

```bash
# 获取文档内容（默认 XML 格式）
lark-cli docs +fetch --api-version v2 --doc "文档URL或token"

# 获取 Markdown 格式（更易转换为纯文本）
lark-cli docs +fetch --api-version v2 --doc "文档URL或token" --doc-format markdown

# 只看目录结构
lark-cli docs +fetch --api-version v2 --doc "文档URL或token" --scope outline --max-depth 3

# 按关键词定位
lark-cli docs +fetch --api-version v2 --doc "文档URL或token" --scope keyword --keyword "营收|毛利率"
```

> 参考 skill：`lark-doc`（路径 `~/.agents/skills/lark-doc/`）

### 搜索云文档

```bash
# 关键词搜索
lark-cli drive +search --query "行业研究" --as user --doc-types docx

# 最近编辑的文档
lark-cli drive +search --mine --edited-since 7d --doc-types docx --as user

# 搜索结果格式化输出
lark-cli drive +search --query "投研" --as user --format pretty
```

> 参考 skill：`lark-drive`（路径 `~/.agents/skills/lark-drive/`）

### 创建飞书文档

```bash
# 创建 XML 文档（推荐，支持富文本 block）
lark-cli docs +create --api-version v2 --content '<title>标题</title><h1>内容</h1>'

# 创建到指定文件夹
lark-cli docs +create --api-version v2 --parent-token fldcnXXXX --content '<title>标题</title><p>内容</p>'
```

> 参考 skill：`lark-doc`（路径 `~/.agents/skills/lark-doc/`），必读 `references/lark-doc-xml.md`

### 更新飞书文档

```bash
# 追加内容到文档末尾
lark-cli docs +update --api-version v2 --doc "文档URL或token" --command append --content '<XML内容>'
```

> 参考 skill：`lark-doc`（路径 `~/.agents/skills/lark-doc/`），必读 `references/lark-doc-update.md`

### 发送消息

```bash
# 发送 Markdown 消息给用户（P2P）
lark-cli im +messages-send --user-id <用户open_id> --markdown "消息内容"

# 发送纯文本消息
lark-cli im +messages-send --user-id <用户open_id> --text "消息内容"
```

> 参考 skill：`lark-im`（路径 `~/.agents/skills/lark-im/`），必读 `references/lark-im-messages-send.md`

---

## 3. 报告 Markdown → 飞书 DocxXML 转换规则

投研报告从 Markdown 转换为飞书 DocxXML 时，需遵循以下映射规则。XML 格式支持 callout、grid、checkbox 等富文本 block，表达能力远强于 Markdown。

> 详细的 XML 语法规则请参考 `lark-doc` skill 的 `references/lark-doc-xml.md`。

### 标题映射

| Markdown | DocxXML |
|----------|---------|
| `# 一级标题` | `<title>一级标题</title>`（文档标题，每篇唯一） |
| `## 二级标题` | `<h1>二级标题</h1>` |
| `### 三级标题` | `<h2>三级标题</h2>` |
| `#### 四级标题` | `<h3>四级标题</h3>` |

### 表格映射

Markdown 表格 → `<table>` 标签：

```markdown
| 指标 | 2023 | 2024 |
|------|------|------|
| 营收 | 1亿 | 3亿 |
```

转换为：

```xml
<table>
  <thead>
    <tr><th>指标</th><th>2023</th><th>2024</th></tr>
  </thead>
  <tbody>
    <tr><td>营收</td><td>1亿</td><td>3亿</td></tr>
  </tbody>
</table>
```

### Callout 映射（高亮框）

投研报告中以下内容应使用 `<callout>` 而非普通段落：

| 内容类型 | callout emoji | 颜色建议 |
|----------|--------------|---------|
| 投资亮点 | `emoji="star"` | `background-color="#f0f9ff"` |
| 风险警示 | `emoji="warning"` | `background-color="#fff3f3"` |
| 关键数字 | `emoji="bulb"` | `background-color="#f5f5f5"` |
| 待确认事项 | `emoji="question"` | `background-color="#fff8e6"` |

示例：

```xml
<callout emoji="star" background-color="#f0f9ff">
  <p><b>投资亮点</b></p>
  <ul><li>技术领先：VST延迟8ms，业界领先</li><li>2026年营收目标2亿+</li></ul>
</callout>
```

### 状态标签映射

| Markdown 状态 | DocxXML 表达 |
|---------------|-------------|
| ✅ 已解决 | `<callout emoji="check_mark"><p>✅ 已解决：...</p></callout>` |
| ⚠️ 待确认 | `<callout emoji="warning"><p>⚠️ 待确认：...</p></callout>` |
| ❌ 未涉及 | `<callout emoji="cross_mark"><p>❌ 未涉及：...</p></callout>` |

### 列表映射

```markdown
- 项目1
- 项目2
```

转换为：

```xml
<ul>
  <li>项目1</li>
  <li>项目2</li>
</ul>
```

有序列表同理，使用 `<ol>` + `<li seq="auto">`。

### 投资建议映射

| 建议 | DocxXML 表达 |
|------|-------------|
| 建议推进 | `<callout emoji="check_mark" background-color="#f0f9ff"><p><b>建议：建议推进</b></p><p>...</p></callout>` |
| 谨慎推进 | `<callout emoji="warning" background-color="#fff8e6"><p><b>建议：谨慎推进</b></p><p>...</p></callout>` |
| 暂缓推进 | `<callout emoji="cross_mark" background-color="#fff3f3"><p><b>建议：暂缓推进</b></p><p>...</p></callout>` |
| 不建议推进 | `<callout emoji="cross_mark" background-color="#ff4d4f"><p><b>建议：不建议推进</b></p><p>...</p></callout>` |

---

## 4. 飞书文档 URL/token 识别与提取规则

### URL 格式识别

| URL 格式 | 示例 | Token 类型 | 处理方式 |
|----------|------|-----------|----------|
| `/docx/TOKEN` | `https://xxx.feishu.cn/docx/doxcnXXXX` | `file_token` | URL 中 token 直接使用 |
| `/doc/TOKEN` | `https://xxx.feishu.cn/doc/doccnXXXX` | `file_token` | URL 中 token 直接使用 |
| `/sheets/TOKEN` | `https://xxx.feishu.cn/sheets/shtcnXXXX` | `file_token` | URL 中 token 直接使用 |
| `/wiki/TOKEN` | `https://xxx.feishu.cn/wiki/wikcnXXXX` | `wiki_token` | **不能直接使用**，需先查询 |

### wiki 链接特殊处理

wiki 链接中的 token 不是 file_token，必须先查询真实 obj_token：

```bash
# 第一步：查询 wiki 节点信息
lark-cli wiki spaces get_node --params '{"token":"wikcnXXXX"}'

# 第二步：从返回结果中提取
# - node.obj_type → 文档类型（docx/doc/sheet/bitable/slides）
# - node.obj_token → 真实的文档 token

# 第三步：用真实 token 读取文档
lark-cli docs +fetch --api-version v2 --doc <obj_token>
```

### 从用户输入中提取 token

用户可能提供：
- 完整 URL：直接提取路径中的 token 部分
- 短 token：直接使用
- 文档名称描述：使用 `drive +search` 搜索

---

## 5. 云文档搜索策略

### 搜索场景与命令组合

| 用户意图 | 命令 |
|----------|------|
| "找一下上次写的行业研究SOP" | `lark-cli drive +search --query "行业研究SOP" --as user --doc-types docx` |
| "我最近编辑的投研文档" | `lark-cli drive +search --mine --edited-since 7d --doc-types docx --as user` |
| "找张三创建的BP" | `lark-cli drive +search --query "BP 商业计划书" --creator-ids <张三的open_id> --as user` |
| "最近一周打开过的文档" | `lark-cli drive +search --opened-since 7d --as user` |

### 搜索结果处理

1. 执行搜索命令，获取结果列表
2. 展示搜索结果（标题、URL、类型、最后编辑时间）给用户
3. 用户确认目标文档后，提取 token/URL
4. 使用 `docs +fetch` 读取文档内容

### 搜索结果格式化

```bash
# 使用 pretty 格式方便展示
lark-cli drive +search --query "投研" --as user --format pretty
```

输出示例：
```
edit_time                  title                     type     url
2026-04-23T16:51:38+08:00  投研Agent                 DOCX     https://my.feishu.cn/wiki/RrJ4wwu6ii...
2026-04-24T16:43:58+08:00  行业研究SOP               DOCX     https://my.feishu.cn/wiki/Z8paw9xYYi...
```

---

## 6. 错误处理与回退策略

### lark-cli 认证失败

**症状**：命令返回 `authentication failed` 或 `token expired`

**处理**：
1. 提示用户运行 `lark-cli auth login` 重新认证
2. 如果是 bot 身份失败，检查 `lark-cli config init` 是否完成
3. 认证失败时回退到本地模式，不影响核心投研流程

### 文档不存在

**症状**：`docs +fetch` 返回 `document not found`

**处理**：
1. 确认 URL/token 是否正确（注意 wiki 链接需先查询）
2. 如果是搜索找到的文档，可能权限不足导致无法访问
3. 提示用户提供正确的文档 URL

### 权限不足

**症状**：`permission denied` 或 `forbidden`

**处理**：
1. 检查身份类型：用户资源需 `--as user`，bot 资源需 `--as bot`
2. 提示用户确认文档是否已共享给当前身份
3. 如果是写入操作失败，提示用户确认是否有编辑权限
4. 权限不足时回退到本地模式输出

### lark-cli 未安装

**症状**：`lark-cli --version` 命令失败

**处理**：
1. 自动跳过飞书协作模式，使用本地模式
2. 不影响任何核心投研功能

### 创建文档后发送链接失败

**症状**：文档创建成功但 `im +messages-send` 失败

**处理**：
1. 文档已创建成功，URL 可从 `docs +create` 返回值中获取
2. 直接将 URL 展示给用户，提示手动复制
3. 同时本地保存 Markdown 备份





