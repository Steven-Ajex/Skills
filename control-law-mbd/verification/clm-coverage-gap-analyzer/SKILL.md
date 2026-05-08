---
name: clm-coverage-gap-analyzer
description: 解读 Simulink Coverage / SLDV(Simulink Design Verifier) / Polyspace / 第三方覆盖率工具的报告,从 Decision / Condition / MCDC 三个维度分析覆盖率缺口、对缺口分类(可达/未激活/不稳定/需要模型重构),并把缺口路由回 `clm-test-harness-builder`(增补用例)或 `clm-codegen-compliance-refactor`(模型层重构)的专用只读分析技能。用于已有覆盖率报告需要做缺口分析与闭环建议时;不负责真实运行覆盖率工具、不负责设计测试用例本身、不负责修改模型。
---

# Control-Law-MBD: Coverage Gap Analyzer

## 目标

把覆盖率报告里"哪些 Decision / Condition / MCDC 维度没满足"和"为什么没满足"讲清楚,并指向具体的闭环路径(增补用例 vs 模型重构 vs 显式接受残留),产出 `coverage_gap_report` 工件。本 skill 不重复 `clm-test-harness-builder` 的用例设计工作,只输出"补哪一类用例"的指向。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一被测对象 + 单一覆盖率报告范围内,完成 Decision / Condition / MCDC 三维度缺口分析与闭环路径分类,产出 `coverage_gap_report` 工件
2. 工具上下文(Tool Context)
   - 覆盖率工具(Simulink Coverage / SLDV / Polyspace / 第三方)与版本
   - 报告形态(HTML / XML / `.cvt` / 自定义)
   - 覆盖率维度(Decision / Condition / MCDC / Lookup Table / Saturation 等)
   - 是否启用过滤(Coverage Filter)与过滤理由
   - 许可证可用性
3. 核心输入(Inputs)
   - 覆盖率报告路径(必需)
   - 被测对象路径(必需,与报告对应)
   - (强烈推荐)`clm-test-harness-builder` 的 `test_harness_plan`(用于把缺口指回具体用例分组)
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`(用于解读"哪个子系统未覆盖")
   - (推荐若涉及状态机)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`(状态/转移覆盖路由)
4. 核心输出(Outputs)
   - 主交付工件:`coverage_gap_report`
   - 三维度覆盖率细分(`coverage_breakdown`)
   - 缺口清单(每条:位置 + 维度 + 分类 + 闭环路径)
   - 闭环路由表(用例增补 / 模型重构 / 显式接受)
5. 完成判据(Definition of Done, DoD)
   - 三维度(Decision / Condition / MCDC)各自给出覆盖率 % 与缺口清单
   - 至少一条缺口被分类到以下四类之一:`unreachable`(不可达) / `unexercised`(可达但未激活) / `unstable`(不稳定 / Filter 已抑制) / `needs-model-refactor`(模型层不利于覆盖)
   - 每条缺口给出闭环路径(指向 `clm-test-harness-builder` 用例分组,或 `clm-codegen-compliance-refactor` 重构,或显式接受 + 理由)
   - Coverage Filter 过滤记录显式列出,过滤理由可审查
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留覆盖率报告中的 Block 路径、Decision/Condition ID 原文

## 聚焦范围(只做这些)

1. Decision / Condition / MCDC 覆盖率细分
2. 模型对象级缺口(Subsystem / Block / Stateflow State / Transition)
3. 缺口分类(`unreachable` / `unexercised` / `unstable` / `needs-model-refactor`)
4. Coverage Filter 过滤审查
5. 闭环路由(用例增补 / 模型重构 / 显式接受)
6. 与 `test_harness_plan` 用例分组的对接

## 不负责

1. 真实运行覆盖率工具(用户工程实施)
2. 设计测试用例本身 → 走 `clm-test-harness-builder`(本 skill 只指向用例分组)
3. 修改模型 → 走 `model-authoring/`
4. PIL/HIL 数据回放与基线对比 → 走 `clm-pil-hil-replay-analyzer`
5. 需求源文档解读 → 走 `clm-requirement-trace-reader`

## 推荐分析顺序

1. 先看"工具与维度配置" — 确认报告口径(是否含 MCDC、是否含 Stateflow Coverage、是否启用 Filter)
2. 再看"顶层覆盖率 %" — 整体水位
3. 再看"未覆盖对象清单"(Block / State / Transition)
4. 对每条缺口判定可达性(`unreachable` 必须给推断证据)
5. 对每条可达缺口路由到用例分组(等价类 / 边界 / 状态切换 / 故障注入)
6. 最后审查 Coverage Filter:每条 Filter 都需要文档化的理由

## 执行步骤

1. **确认工具上下文**:覆盖率工具与版本、报告形态、维度、Filter 状态、许可证
2. **解析覆盖率细分**:按 Decision / Condition / MCDC 抓取顶层 % 与未覆盖对象
3. **缺口分类**:对每条缺口判定 `unreachable` / `unexercised` / `unstable` / `needs-model-refactor`,并给出依据
4. **闭环路由**:
   - `unexercised` → 指向 `clm-test-harness-builder` 的具体用例分组(等价类/边界/状态切换/故障注入)
   - `needs-model-refactor` → 指向 `clm-codegen-compliance-refactor`(模型层 backlog)
   - `unreachable` → 列出推断依据,提议显式接受 + 文档化
   - `unstable` → 检查 Filter 理由是否可审查,不可审查时升级为缺口
5. **Filter 审查**:列出所有 Coverage Filter,每条记录"过滤对象 + 理由 + 是否可审查"
6. **状态/转移覆盖**(若涉及 Stateflow):对照 `stateflow_semantics`,标注未覆盖的非平凡转移
7. **生成工件**:按 `references/output-template.md` 填充 `coverage_gap_report`
8. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 三维度覆盖率细分表(`coverage_breakdown`)
3. 缺口清单(位置 + 维度 + 分类 + 闭环路径)
4. Coverage Filter 审查表
5. 状态/转移覆盖表(若适用)
6. 闭环路由汇总(用例增补 / 模型重构 / 显式接受)
7. 关键事实(Facts)、关键推断(Inferences)
8. 证据索引(报告路径 + 模型对象路径)
9. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的覆盖率报告与被测对象
   - (强烈推荐)`clm-test-harness-builder` 的 `test_harness_plan`
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
   - (推荐)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`
2. 下游使用方
   - `clm-test-harness-builder`(消费"用例增补"路由 — 注意:这是反馈环路,通常由编排技能决定是否回到 harness 设计)
   - `clm-codegen-compliance-refactor`(消费"模型重构"路由作为 backlog)
   - `clm-pil-hil-replay-analyzer`(消费"已显式接受的残留覆盖" — 在回放分析中提示这些位置不应有新规约)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `coverage_gap_report`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`coverage_breakdown`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不真实运行覆盖率工具 / 不重写用例 / 不修改模型
   - 证据门禁:每条结论给出"覆盖率报告路径 + 模型对象路径(或 Decision/Condition ID)"
   - 工具上下文门禁:工具与版本、维度、Filter 状态、许可证显式记录
   - 缺口分类纪律(Gap Classification Discipline):每条缺口必须落到四类之一,不允许"未分类";`unreachable` 必须有推断证据
   - Filter 审查纪律(Filter Audit Discipline):Filter 不可审查时升级为缺口,不允许默认接受
   - 闭环路由纪律:每条 `unexercised` 缺口必须指向 `test_harness_plan` 中具体用例分组
   - 交接门禁:工件可被下游 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供覆盖率报告**:本 skill 无法运行,提示用户先运行覆盖率工具
   - **报告形态未识别**:列出已知支持形态(Simulink Coverage HTML / cvt、SLDV、Polyspace),请用户提供格式说明或转换
   - **未提供 `test_harness_plan`**:可继续工作,但闭环路由降级为"分组建议"而非具体用例 ID
   - **未提供 `simulink_model_map` / `stateflow_semantics`**:模型对象/状态对照降级,在 `gaps` 中登记
   - **覆盖率 = 100% 但 Filter 大量启用**:不接受默认结论,要求 Filter 审查可审查性
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出"已通过覆盖率门"的结论(由编排技能或工程师决定)

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,缺口清单与闭环路由表直接套用
2. 交付前用 `references/checklist.md` 复核分类纪律、Filter 审查、降级
3. 大型模型 / Stateflow 比例高:先输出 Decision/Condition 主表,再单独下钻 Stateflow 状态/转移覆盖

## 分析纪律

1. `unreachable` 不能基于"运行结果未达到"判定 — 必须给出可达性的反向推断(如条件互斥代码)
2. Coverage Filter 不是"无害默认值" — 每一条都需要可审查理由
3. 不把"覆盖率 = 100%"等同为"测试充分" — 仍要看 MCDC 与状态切换覆盖
4. 不在本 skill 内重写 `clm-test-harness-builder` 的用例设计 — 只指向分组
5. 跨 skill 交接时,缺口位置(模型对象路径)与 `test_harness_plan` 中的"覆盖维度"字段必须可对接
