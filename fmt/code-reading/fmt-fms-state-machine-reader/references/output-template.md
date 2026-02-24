# FMT FMS State Machine Reader 输出模板

## 使用说明

- 目标：输出 FMS 状态机状态/模式语义、切换触发和关键转换路径，供日志分段与行为解释使用。
- 主交付工件（Primary Artifact）：`fms_state_semantics`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`fms_state_semantics`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] FMS 变体目录（vtol_fms/mc_fms/fw_fms）
- [ ] 关注阶段（过渡/返航/自动模式）
- [ ] 代码版本
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] fms_interface.c
- [ ] FMS.c/FMS_types.h 等生成代码
- [ ] 用户关注的异常模式切换现象（可选）
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 状态/模式字段语义表

- 说明：用中文说明并在首次出现附英文术语。
- 内容：

### 触发源清单

- 说明：列出 Pilot/GCS/Auto/Mission/INS 等输入源及影响字段。
- 内容：

### 关键转换路径

- 说明：整理 触发条件 -> 状态变化 -> 输出语义变化。
- 内容：

### 日志分段建议字段

- 说明：给下游 segmenter 推荐字段与注意事项。
- 内容：

## 关键事实（Facts）

- Fact-1：
- Fact-2：

## 关键推断（Inferences）

- Inference-1（置信度：高/中/低）：
- Inference-2（置信度：高/中/低）：

## 证据索引（Evidence Index）

- 代码证据：`path/to/file.c:line` -> 结论
- 代码证据：`path/to/file.h:line` -> 结论

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
