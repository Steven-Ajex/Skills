# FMT Tuning Report Writer 输出模板

## 使用说明

- 目标：输出可执行、可验证、可追踪的参数优化报告和试飞验证计划（Test Card），不新增证据。
- 主交付工件（Primary Artifact）：`tuning_recommendation_report`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`tuning_recommendation_report`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 任务背景与目标
- [ ] 机型/版本/日志批次
- [ ] 本轮报告覆盖范围
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] 代码理解工件
- [ ] control_performance_findings
- [ ] 参数快照/当前参数列表
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 任务背景与范围

- 说明：说明机型、版本、日志来源、目标现象和本次分析边界。
- 内容：

### 证据摘要

- 说明：汇总代码侧与日志侧关键证据，明确缺口。
- 内容：

### 参数优化建议（分优先级）

- 说明：每条建议包含目标现象、参数、方向、预期效果、风险。
- 内容：

### 风险与副作用

- 说明：说明可能引入的耦合影响和安全风险。
- 内容：

### 试飞验证计划（Test Card）

- 说明：给出工况、观察项、通过条件、回退条件。
- 内容：

### 待补数据与下一轮动作

- 说明：列出仍需采集或验证的最小动作。
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
