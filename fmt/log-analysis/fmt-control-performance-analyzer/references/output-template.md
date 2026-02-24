# FMT Control Performance Analyzer 输出模板

## 使用说明

- 目标：输出分层控制性能分析结论（INS/FMS/Controller/Actuator），形成现象到证据再到候选根因的链条。
- 主交付工件（Primary Artifact）：`control_performance_findings`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`control_performance_findings`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 单架次或单阶段窗口
- [ ] 机型变体
- [ ] 参数快照可用性状态
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] 已解码结构化日志
- [ ] 分段结果与事件索引
- [ ] 参数快照（可选但推荐）
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 分析范围与前置检查

- 说明：确认分段、时间轴、关键信号、参数快照状态。
- 内容：

### 现象清单（按严重度）

- 说明：记录振荡、超调、延迟、饱和等现象。
- 内容：

### 证据链

- 说明：按 现象 -> 时间段 -> 信号 -> 阶段/模式 上下文 写明证据。
- 内容：

### 候选根因分层

- 说明：按估计器/FMS/控制器/执行器/传感器分层归因。
- 内容：

### 候选参数方向与验证建议

- 说明：仅给方向级建议，注明置信度和待验证项。
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
