---
name: clm-requirement-trace-reader
description: 读取需求源(Simulink Requirements `.slreqx` / ReqIF `.reqifz`/`.reqif` / DOORS 导出 / Polarion 导出 / Jira 导出)与模型/状态机/测试用例的双向追溯链,生成"需求 ↔ 模型对象 ↔ 用例"三向矩阵、孤立条目(orphan)与断链(broken link)清单的专用只读技能。用于需要确认"哪条需求被实现了 / 哪些需求未覆盖 / 哪些链接已失效"时;不负责需求质量评审、不负责需求来源文档解读、不负责修改需求或模型、不负责设计测试用例。
---

# Control-Law-MBD: Requirement Trace Reader

## 目标

把"需求条目 + 它和模型对象/用例的链接"解析为可被工程师、评审与下游 skill 消费的三向矩阵,识别"孤立条目"(orphan,无任何向下链接)与"断链"(broken link,链接对象已不存在或路径变更),产出 `requirement_trace_map` 工件。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一需求源 + 单一模型(可选)+ 单一测试集(可选)范围内,完成需求条目清单、需求 ↔ 模型对象 ↔ 用例三向链接矩阵、orphan 与 broken link 识别,产出 `requirement_trace_map` 工件
2. 工具上下文(Tool Context)
   - 需求工具(Simulink Requirements / DOORS / ReqIF / Polarion / Jira / 自研)与版本
   - 需求源形态(`.slreqx` / `.reqifz` / `.reqif` / CSV / API 导出)
   - 链接存储形态(模型内嵌 / 外部存储 / Simulink Requirements 数据库 / 第三方索引)
   - 是否启用追溯审计(Traceability Audit)
   - 许可证可用性(无许可证时只能解析序列化文件)
3. 核心输入(Inputs)
   - 需求源路径或导出文件(必需)
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`(用于解析模型对象目标的有效性)
   - (推荐若涉及状态机)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`
   - (推荐若涉及用例)`clm-test-harness-builder` 的 `test_harness_plan`
4. 核心输出(Outputs)
   - 主交付工件:`requirement_trace_map`
   - 需求条目清单(ID / 标题 / 类型 / 优先级 / 状态)
   - 三向矩阵(需求 ↔ 模型对象 ↔ 用例)
   - 孤立条目(orphan)清单
   - 断链(broken link)清单
   - 反向追溯结论(模型对象/用例对应到哪条需求)
5. 完成判据(Definition of Done, DoD)
   - 需求条目清单完整(至少 ID / 标题 / 状态;可选优先级 / 类型)
   - 三向矩阵建立;每条链接给出"源(需求 ID)→ 目标(模型路径或用例 ID)"
   - 至少识别一条 orphan 或 broken link(若全部链接齐全则显式声明"无 orphan / broken")
   - 反向追溯至少给出一个模型对象/用例 → 需求 ID 的映射(若有上游模型/用例工件)
   - 工具上下文显式记录;链接存储形态与解析方法已声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留需求 ID、标题原文(若是英文/其他语言不翻译)

## 聚焦范围(只做这些)

1. 需求条目清单与基本元数据(ID / 标题 / 类型 / 优先级 / 状态)
2. 需求 → 模型对象链接(子系统 / 块 / Stateflow 状态/转移)
3. 需求 → 用例链接(测试用例 ID)
4. 反向追溯(模型对象 → 需求、用例 → 需求)
5. 孤立条目(orphan)识别
6. 断链(broken link)识别(目标对象不存在 / 路径变更 / 测试已删除)
7. 链接质量(是否有理由说明 / 是否已审计)

## 不负责

1. 需求质量评审(可读性 / 可测性 / 一致性)— 需求工程师职责
2. 需求源文档(策略文档 / 系统设计文档)解读 — 上游业务文档分析
3. 修改需求 / 模型 / 用例 — 走相关写操作 skill
4. 设计测试用例 → 走 `clm-test-harness-builder`
5. 覆盖率分析 → 走 `clm-coverage-gap-analyzer`(本 skill 只输出矩阵,不下"覆盖足够"结论)

## 推荐阅读顺序

1. 先看"工具与链接形态" — 决定解析方法与解析能力
2. 再抓"需求条目清单"(完整性优先)
3. 再抓"前向链接"(需求 → 模型 / 需求 → 用例)
4. 然后构造"反向追溯"(对照模型/用例工件)
5. 再做"orphan / broken link 扫描"
6. 最后审查"链接理由"(若需求工具支持记录链接理由)

## 执行步骤

1. **确认工具上下文**:需求工具与版本、链接存储形态、许可证
2. **抓需求条目清单**:遍历需求源,提取 ID / 标题 / 类型 / 优先级 / 状态
3. **抓前向链接**:对每条需求,列出指向的模型对象(子系统路径 / Stateflow 状态-转移)与测试用例(ID)
4. **构造反向追溯**:
   - 对照 `simulink_model_map` 中的子系统树,标注哪些子系统已被需求引用,哪些未被引用
   - 对照 `stateflow_semantics` 中的状态/转移,标注覆盖情况
   - 对照 `test_harness_plan` 中的用例 ID,标注哪些用例无对应需求
5. **orphan 识别**:
   - 无任何向下链接的需求(高/中优先级且 status = active 的尤其重要)
6. **broken link 识别**:
   - 链接的模型对象在 `simulink_model_map` 中不存在
   - 链接的状态/转移在 `stateflow_semantics` 中不存在
   - 链接的用例在 `test_harness_plan` 中不存在
7. **链接质量审查**:链接是否有理由说明、是否已审计、是否有"待评审"状态
8. **生成工件**:按 `references/output-template.md` 填充 `requirement_trace_map`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 需求条目清单(总数 + 按状态/优先级分布)
3. 三向矩阵(需求 ↔ 模型对象 ↔ 用例)
4. 反向追溯结论(模型对象覆盖率、用例覆盖率)
5. orphan 清单
6. broken link 清单
7. 链接质量审查表
8. 关键事实(Facts)、关键推断(Inferences)
9. 证据索引(需求源路径 + 需求 ID + 模型对象路径 + 用例 ID)
10. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的需求源
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
   - (推荐若涉及状态机)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`
   - (推荐若涉及用例)`clm-test-harness-builder` 的 `test_harness_plan`
2. 下游使用方
   - `clm-test-harness-builder`(消费需求 → 用例缺口 — 注意反馈环路)
   - `clm-coverage-gap-analyzer`(消费需求 → 模型对象矩阵作为覆盖路由依据之一)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `requirement_trace_map`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`traceability_index`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不评审需求质量 / 不解读需求源文档 / 不修改任何文件 / 不设计用例
   - 证据门禁:每条链接给出"需求 ID + 目标对象路径或用例 ID"
   - 工具上下文门禁:需求工具/版本/链接形态/许可证显式记录
   - 矩阵完整性纪律(Matrix Completeness Discipline):三向矩阵完整;orphan 与 broken link 显式声明(为零也要写)
   - 反向追溯纪律(Reverse Traceability Discipline):对照上游模型/用例工件,标注覆盖率;不假设"未引用 = 不需要"
   - 交接门禁:工件可被下游 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供需求源**:本 skill 无法运行,提示用户提供
   - **需求工具许可证缺失**:降级到从序列化文件(`.slreqx` / `.reqifz` / `.reqif` / CSV)解析,声明"部分高级查询不可用"
   - **需求源形态未识别**:列出已知支持形态,请用户提供格式说明或转换
   - **未提供 `simulink_model_map`**:跳过反向追溯章节(模型侧),只保留前向链接;在 `gaps` 中登记
   - **未提供 `test_harness_plan`**:跳过反向追溯章节(用例侧)
   - **链接对象路径在多个工件之间不一致**(如模型重命名后链接未更新):列入 broken link 而非硬猜
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出"需求覆盖足够 / 不足"的结论(由 `clm-coverage-gap-analyzer` 与编排技能聚合判定)

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,三向矩阵与 orphan/broken link 表直接套用
2. 交付前用 `references/checklist.md` 复核矩阵完整性、反向追溯、降级
3. 大型需求源:先输出"需求条目分布 + 矩阵汇总",再分章节列出 orphan 与 broken link

## 分析纪律

1. orphan 不等于"不重要" — 高优先级且 status = active 的 orphan 必须高亮
2. broken link 不等于"链接没用" — 可能是模型重命名 / 用例重组,需要修复而非删除
3. 不下"需求覆盖足够"的结论 — 这是 `clm-coverage-gap-analyzer` 的职责
4. 不评审需求本身的质量 — 仅审视链接结构
5. 反向追溯依赖上游工件;上游工件版本与需求源版本不一致时必须显式声明
