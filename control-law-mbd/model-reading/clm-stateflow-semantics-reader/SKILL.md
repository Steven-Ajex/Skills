---
name: clm-stateflow-semantics-reader
description: 读取 Stateflow Chart 内部状态、转移、事件、动作及执行顺序的专用只读技能,聚焦"模式切换/状态机语义"。用于需要理解控制律里某个 Chart 在做什么、什么条件下切换状态、动作执行顺序如何;不负责 Simulink 模型层级解读、不负责数据字典解读、不负责修改 Chart、不负责代码生成结论。
---

# Control-Law-MBD: Stateflow Semantics Reader

## 目标

在不修改任何 Chart 的前提下,把指定 Stateflow Chart 的状态/转移/事件/动作执行顺序解读清楚,产出一份可被工程师 review、被下游 skill 引用的"状态机语义"工件。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一 Stateflow Chart 范围内,完成状态层级、转移、事件、动作执行顺序的证据化梳理,产出 `stateflow_semantics` 工件
2. 工具上下文(Tool Context)
   - Stateflow / Simulink 版本
   - Chart 分解方式(Decomposition:Exclusive(OR)、Parallel(AND))
   - 执行模式(Execute (enter) Chart At Initialization、Initialize Outputs Every Time Chart Wakes Up)
   - 早晚绑定(Early Return Logic / Super Step)
   - 数据作用域(Local / Input / Output / Parameter / Constant)
   - 许可证可用性(无许可证时只能从 `.slx` / `.mdl` 文本侧解析,部分语义查询不可用)
3. 核心输入(Inputs)
   - Simulink 模型路径(必需)
   - 目标 Chart 路径(必需,例如 `model.slx > ModeManager`)
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map`(从中获取 Chart 端口与外部信号上下文)
   - (可选)用户关注的状态、事件或转移条件
4. 核心输出(Outputs)
   - 主交付工件:`stateflow_semantics`
   - 状态层级树、转移表、事件清单、动作执行顺序、数据作用域表、证据索引
5. 完成判据(Definition of Done, DoD)
   - 状态层级与 Decomposition 已明确(Exclusive vs Parallel)
   - 至少一条完整状态切换路径"源状态 → 触发条件 → 转移动作 → 目标状态"被串起
   - 动作类型(`entry` / `during` / `exit` / 转移上的 condition action / transition action)被显式区分
   - 早晚绑定与 Super Step 行为被显式记录
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留状态名、事件名、变量名原文

## 聚焦范围(只做这些)

1. 状态层级与 Decomposition(Exclusive(OR) / Parallel(AND))
2. 转移(Transition):源、目标、`event[condition]{condition_action}/transition_action`
3. 事件(Event):本地、输入、输出、广播
4. 动作类型与执行顺序(`entry` / `during` / `exit` / `on event`)
5. 数据作用域(Local / Input / Output / Parameter / Constant)及类型
6. 早晚绑定(Early Return Logic)、Super Step 行为、Chart 初始化语义
7. Junction(History Junction、Connective Junction)的语义

## 不负责

1. Simulink 模型顶层结构与子系统层级 → 走 `clm-simulink-model-reader`
2. `.sldd` 数据字典深入解读 → 走 `clm-data-dictionary-reader`
3. 需求与状态机的追溯链 → 走 `clm-requirement-trace-reader`
4. 代码生成 → 走 `codegen-bridge/`
5. 修改 Chart → 走 `model-authoring/`
6. 测试用例与覆盖率 → 走 `verification/`

## 推荐阅读顺序

1. 先看 Chart 属性(Decomposition、Execute (enter) at Init、Super Step、Action Language MATLAB vs C)
2. 再看顶层状态(默认转移指向何处)
3. 逐层下钻,记录每个状态的 `entry` / `during` / `exit` 动作
4. 再看转移表(优先级、条件、动作)
5. 再看事件清单(谁广播、谁监听)
6. 最后看数据(作用域、类型、初值)

## 执行步骤

1. **确认工具上下文**:Stateflow 版本、Chart 属性(Decomposition、Action Language、初始化语义)、许可证可用性
2. **抓 Chart 属性**:Decomposition、是否 Super Step、是否 Execute at Init、Action Language(MATLAB or C)
3. **抓状态层级**:从默认转移开始,递归列出状态树,标注每个 sub-chart 的 Decomposition
4. **抓动作**:对每个状态记录 `entry` / `during` / `exit`,保留 MATLAB/C 语法原文
5. **抓转移**:对每条转移记录"源 → 目标"、`event`、`condition`、`condition_action`、`transition_action`、优先级
6. **抓事件**:列出事件清单,标注 `Local` / `Input` / `Output`,以及 `Broadcast` 触发点
7. **抓数据**:列出数据,标注作用域、类型、初值、范围(Min/Max)
8. **重建一条切换路径**:从某个起始状态出发,挑一个常见触发条件,串起完整切换路径作为示例
9. **生成工件**:按 `references/output-template.md` 填充 `stateflow_semantics`
10. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. Chart 属性小结(Decomposition、初始化语义、Action Language)
2. 状态层级树(含 Exclusive / Parallel 标记)
3. 转移表(源、目标、事件、条件、动作、优先级)
4. 事件清单
5. 数据作用域表
6. 至少一条完整状态切换路径示例
7. 关键事实(Facts)、关键推断(Inferences,带置信度)
8. 证据索引(Chart 路径 + 状态/转移名)
9. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖(Upstream Dependencies)
   - 用户提供的模型路径与 Chart 路径
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
2. 下游使用方(Downstream Consumers)
   - `clm-requirement-trace-reader`(把状态/事件回链到需求)
   - `clm-test-harness-builder`(消费状态切换路径作为测试用例骨架)
   - `clm-coverage-gap-analyzer`(消费状态/转移作为覆盖率维度)
   - `clm-control-law-mbd-pipeline`(编排技能)
   - `fmt-fms-state-machine-reader`(跨库:本工件的 Chart 语义 ↔ FMT 嵌入式侧的状态机解读)
3. 主交付工件(Primary Artifact)
   - `stateflow_semantics`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范(Shared Contracts)
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁(Boundary Purity):不输出 Simulink 顶层结构、不输出代码生成结论、不修改 Chart
   - 证据门禁(Evidence Traceability):每条结论给出"Chart 路径 + 状态/转移名"
   - 工具上下文门禁:Stateflow 版本、Chart 属性、许可证状态显式记录
   - 语义纪律门禁(Semantic Discipline):动作类型(`entry` / `during` / `exit`)与转移动作(`condition_action` / `transition_action`)被显式区分,不混用
   - 交接门禁:工件可被下游 skill 直接消费
2. 自检建议(Self Check)
   - 使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **无 Stateflow 许可证**:降级到从 `.slx` 解压的 XML 解析状态/转移文本;声明"无法运行 Chart 仿真 / 部分语义查询不可用"
   - **Chart 加密 / 受保护**:列入 `gaps`,无法解析时不要硬猜
   - **Chart 过大**:先输出顶层状态层级,再按用户指定状态下钻
   - **Action Language 混用**:显式标注 MATLAB / C,不混用语法假设
   - **未提供 `simulink_model_map`**:可继续工作,但 Chart 外部端口/信号上下文降级
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出 Simulink 顶层结构或代码生成结论

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架
2. 交付前用 `references/checklist.md` 复核语义纪律、证据、降级
3. 跨库交接(对接 `fmt-fms-state-machine-reader`)前重点检查事件/状态命名一致性

## 分析纪律

1. 不把"状态名"误作"行为结论",必须回到 `entry` / `during` / `exit` 与转移动作
2. 不混用 `condition_action`(条件触发动作)与 `transition_action`(转移完成动作) — 二者执行时机不同
3. 不假设默认转移路径可全局唯一 — Parallel(AND) Decomposition 下每个并行状态有自己的默认转移
4. 早晚绑定(Early Return Logic)与 Super Step 行为必须显式记录,否则会误判转移连锁
5. 跨库交接保留两侧工具/固件上下文,事件名/状态名一致性必须显式声明
