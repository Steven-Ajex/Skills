# Model Authoring（建模与重构）

控制律 MBD **写操作类**原子技能（atomic skill）的容器目录。

## 1. 职责（What）

负责按标准控制律结构与代码生成约束**输出建模骨架或模型修改方案**,产物可被工程师直接采纳或作为重构 PR 的基础。

适用对象：

- 新建控制律子系统（PID / LQR / 增益调度 / Anti-Windup / 抗饱和 / 滤波 / 限幅）
- 既有模型重构以满足高完整性建模规范、Model Advisor 检查、代码生成约束

## 2. 规划 skill 列表

| Skill 名 | 最小任务单元 | 主要工件 | 状态 |
| --- | --- | --- | --- |
| `clm-control-law-pattern-author` | 输出标准控制律结构建模骨架与参数清单 | `control_law_pattern_skeleton` | 已落地 |
| `clm-codegen-compliance-refactor` | 把上游 finding 聚合为模型层重构方案 | `compliance_refactor_diff` | 已落地 |
| `clm-anti-windup-author` | 抗饱和(AW)专项设计:选型 + Kt 推导 + MIMO 处置 + 性能预测 | `anti_windup_design` | 已落地 |
| `clm-fixed-point-refactor` | 浮点 → 定点重构方案:Q 格式 + 风险登记 + 验证步骤 | `fixed_point_refactor_plan` | 已落地 |
| `clm-gain-scheduling-author` | 增益调度专项:调度变量 + 工况网格 + LookupTable + bumpless transfer | `gain_scheduling_skeleton` | 已落地 |

后续候选(Backlog):

- `clm-state-observer-author`(进一步专精)

> 两个 skill 均**只产出方案 / 骨架**,不直接修改模型。施工由工程师按方案手工或脚本化实施。

## 3. 不负责（Out of Scope）

- 单纯的模型解读与工件交接 → 走 `../model-reading/`
- Embedded Coder 配置项调整 → 走 `../codegen-bridge/`
- 测试用例与覆盖率改造 → 走 `../verification/`
- 跨阶段串联（重构 → 代码生成 → 验证） → 走 `../workflows/`

## 4. 触发边界（When NOT to use）

- 没有明确的需求/性能目标作为重构依据(应先走需求追溯)
- 缺少 `model-reading/` 的工件,导致重构无证据基础
- 用户只想"看看模型",并未授权写操作

## 5. 共同输出契约

所有本目录 skill 的工件必须满足 `../_meta/artifact-handoff-contract.md` 的最低字段,并额外包含：

- `pattern_choice` 或 `refactor_steps`：决策与步骤说明
- `risk_register`：重构对功能/性能的潜在影响
- `next_skill_inputs`：建议下游 `codegen-bridge/` 与 `verification/` 复用的字段
