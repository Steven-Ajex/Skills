# FMT Control Loop Reader 输出模板

## 使用说明

- 目标：输出 FMT 控制闭环调度与数据路径地图，支持后续接口层阅读、状态机阅读和调参报告引用。
- 主交付工件（Primary Artifact）：`control_loop_map`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`control_loop_map`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 机型变体（vtol/mc/fw）
- [ ] 入口任务（如 task_vehicle）
- [ ] 宏开关/运行模式假设
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] 代码路径
- [ ] 任务入口函数
- [ ] 用户关注链路（姿态/高度/速度/执行器）
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 控制循环顺序图

- 说明：按一轮循环顺序写出：触发条件 -> 函数/模块 -> 输入 -> 输出 -> 下一步。
- 内容：

### 模块职责边界

- 说明：列出 sensor / INS / FMS / Controller / actuator 的职责与边界，标注不确定项。
- 内容：

### MCN/Topic 数据流

- 说明：按 发布者 -> 订阅者 方式整理关键 topic 或 bus。
- 内容：

### 周期与节拍关系

- 说明：给出周期/节拍判断及证据，注明条件分支。
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
