# FMT Mlog Decoder 输出模板

## 使用说明

- 目标：输出 mlog 解码摘要、schema 和完整性评估，并给下游分段/性能分析提供可用信号目录。
- 主交付工件（Primary Artifact）：`mlog_decode_summary`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`mlog_decode_summary`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 日志文件名与批次
- [ ] FMT mlog 版本/代码分支
- [ ] 导出格式（CSV/Parquet-ready）
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] mlog*.bin
- [ ] mlog 格式源码线索
- [ ] 目标字段或导出需求
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 解码摘要

- 说明：记录版本、bus 数量、参数组数量、时间范围。
- 内容：

### schema 清单

- 说明：列出重点 bus、字段类型、时间戳字段来源。
- 内容：

### records 解码完整性

- 说明：说明成功率、损坏/截断范围、恢复范围。
- 内容：

### 结构化导出说明

- 说明：给出字段名、类型、导出路径/格式。
- 内容：

### 下游可用性清单

- 说明：说明 segmenter/analyzer 所需信号是否齐全。
- 内容：

## 关键事实（Facts）

- Fact-1：
- Fact-2：

## 关键推断（Inferences）

- Inference-1（置信度：高/中/低）：
- Inference-2（置信度：高/中/低）：

## 证据索引（Evidence Index）

- 日志证据：`t=[start,end]` + 信号名 -> 结论
- 日志证据：事件索引/阶段 -> 结论

## 缺口与风险（Gaps & Risks）

- 缺口：
- 风险：
- 降级策略：

## 下游输入建议（Next Skill Inputs）

- 推荐下游技能：
- 建议关注字段/信号/路径：
- 需要补充的数据或确认项：

## 质量门禁自检（简表）

- [ ] 边界纯度（Boundary Purity）：没有越权给下游/上游结论
- [ ] 证据可追溯（Evidence Traceability）：关键结论可回链到代码/日志证据
- [ ] 交接可用性（Handoff Usability）：下游技能可直接使用本输出
- [ ] 失败/降级说明完整：输入缺口、受影响结论、置信度变化已标注

## 共享规范引用

- `fmt/_meta/first-principles-skill-contract.md`
- `fmt/_meta/artifact-handoff-contract.md`
- `fmt/_meta/quality-scorecard.md`
