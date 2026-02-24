# FMT Flight Log Segmenter 输出模板

## 使用说明

- 目标：输出可复现的飞行阶段分段与关键事件索引，为性能分析提供可靠的时间上下文。
- 主交付工件（Primary Artifact）：`flight_phase_segments`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`flight_phase_segments`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 单架次日志
- [ ] 机型变体（vtol/mc/fw）
- [ ] 时间轴连续片段范围
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] 已解码结构化日志
- [ ] FMS 状态语义（可选）
- [ ] ulog 事件文本（可选）
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 分段规则定义

- 说明：明确使用字段、阈值、条件和优先级。
- 内容：

### 飞行阶段时间轴

- 说明：列出阶段名、起止时间、证据信号。
- 内容：

### 关键事件索引

- 说明：记录模式切换、过渡、异常、降落等事件。
- 内容：

### 分段质量问题

- 说明：说明缺数据、状态跳变、边界模糊及影响。
- 内容：

### 下游观察窗口建议

- 说明：给 analyzer 标出重点时间段和注意事项。
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
