# Model Reading（模型理解）

控制律 MBD 模型/字典/需求**只读类**原子技能（atomic skill）的容器目录。

## 1. 职责（What）

负责把已存在的 MBD 资产**解读为可交接的工件**,不修改任何模型、字典或需求文件。

适用对象：

- Simulink `.slx` / `.mdl` 模型
- Stateflow 子图
- Simulink Data Dictionary（`.sldd`）与参数对象（`Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus`）
- Simulink Requirements / ReqIF 需求与追溯链

## 2. 规划 skill 列表

| Skill 名 | 最小任务单元 | 主要工件 | 状态 |
| --- | --- | --- | --- |
| `clm-simulink-model-reader` | 解读模型层级、子系统、信号流、采样时间 | `simulink_model_map` | 已落地 |
| `clm-stateflow-semantics-reader` | 解读状态/转移/事件/动作执行顺序 | `stateflow_semantics` | 已落地 |
| `clm-data-dictionary-reader` | 解读 `.sldd`、Bus、参数对象与作用域 | `data_dictionary_map` | 已落地 |
| `clm-requirement-trace-reader` | 解读需求与模型/用例的双向追溯链 | `requirement_trace_map` | 已落地 |

> 新增 skill 前请先对照 `../_meta/first-principles-skill-contract.md` 定义最小任务单元与工具上下文。

## 3. 不负责（Out of Scope）

- 任何**修改/重构**模型或字典 → 走 `../model-authoring/`
- Embedded Coder 配置审查与生成代码诊断 → 走 `../codegen-bridge/`
- 测试用例与覆盖率分析 → 走 `../verification/`
- 跨阶段端到端结论 → 走 `../workflows/`

## 4. 触发边界（When NOT to use）

- 任务目标包含写操作（修改 `.slx` / `.sldd` / 需求）
- 输入仅有生成代码而无对应模型源
- 无法获取 Simulink 工具链或模型许可证（应在工件 `gaps` 中显式登记并降级）

## 5. 共同输出契约

所有本目录 skill 的工件必须满足 `../_meta/artifact-handoff-contract.md` 的最低字段,并显式记录：

- `tool_context`：Simulink/Stateflow 版本、模型形态、许可证可用性
- `evidence_index`：模型路径 + 子系统路径 / 字典对象名 / 需求 ID
- `gaps`：模型缺失、版本不匹配、字典未引用等
