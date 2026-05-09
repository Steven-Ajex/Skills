---
name: clm-polyspace-runtime-error-analyzer
description: 解读 Polyspace Code Prover / Bug Finder 报告(运行时错误:Overflow / Divide-by-Zero / Out-of-Bounds Array / Uninitialized Variable / Dead Code / Concurrency Issue 等),逐条做"代码侧分类 + 模型侧根因反推 + 闭环路由(模型重构 / 配置调整 / accept-residual)"的专用只读分析技能。用于已有 Polyspace 报告需要做缺陷归因与闭环时;不真实运行 Polyspace、不修改代码或模型、不替代手工 code review、不做 MISRA C / CWE 规则审查(那是 Polyspace Bug Finder 自身的产出,本 skill 消费)。
---

# Control-Law-MBD: Polyspace Runtime Error Analyzer

## 目标

把 Polyspace 报告里的"代码侧运行时错误"对接到"模型侧根因",并把每条 finding 路由到具体闭环动作,产出 `polyspace_runtime_error_findings` 工件。本 skill 的核心价值是**把代码侧问题反推回模型侧**(因为 MBD 项目的源头是模型),让工程师不只在生成代码上打补丁。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一 Polyspace 报告 + 单一生成代码目录范围内,完成运行时错误的代码侧分类、模型侧根因反推、闭环路由,产出 `polyspace_runtime_error_findings` 工件
2. 工具上下文(Tool Context)
   - Polyspace 版本(Code Prover / Bug Finder / 联用)
   - 报告形态(HTML / PSCV / API 导出 / 自定义)
   - 启用的规则集(Code Prover 抽象解释 / Bug Finder 缺陷查找 / MISRA C / CWE / CERT C)
   - 目标硬件(Word Length / Endianness)— 影响溢出判定
   - 是否启用并发分析(Concurrency / Race Condition)
   - 许可证可用性
3. 核心输入(Inputs)
   - **必需**:Polyspace 报告路径
   - **必需**:生成代码目录(用于代码定位)
   - **强烈推荐**:`clm-codegen-output-mapper` 的 `codegen_output_map`(代码 → 模型反向追溯的核心)
   - **推荐**:`clm-simulink-model-reader` 的 `simulink_model_map`(模型对象定位)
   - **推荐**:`clm-data-dictionary-reader` 的 `data_dictionary_map`(参数类型 / 范围)
   - (可选)`clm-fixed-point-refactor` 的 `fixed_point_refactor_plan`(若涉及定点溢出)
   - (可选)项目级 RTE(Runtime Error)接受规范
4. 核心输出(Outputs)
   - 主交付工件:`polyspace_runtime_error_findings`
   - 错误清单(每条:错误 ID / 错误类型 / 代码位置 / 严重度 / 模型侧根因 / 闭环路由)
   - 错误类型分布(Overflow / Divide-by-Zero / OOB / Uninitialized / Dead Code / Concurrency / 其他)
   - 模型侧根因反推(指向具体子系统 / 参数对象 / 数据字典)
   - 闭环路由表(模型重构 / 配置调整 / accept-residual / 代码层修复 — 注:MBD 项目通常不允许直接改代码,必须改模型重新生成)
   - Polyspace 设置审查(是否过严 / 过松)
5. 完成判据(Definition of Done, DoD)
   - 至少覆盖报告中的 `Red`(已证有错)与 `Orange`(可能有错)级别条目
   - 每条错误给出:错误类型 + 代码位置(文件:行号) + 严重度 + 模型侧根因 + 闭环路由
   - 模型侧根因反推必须经 `codegen_output_map` 中转(无中转时降级为"建议根因",置信度低)
   - 闭环路由四枚举:`refactor-model`(改模型重新生成) / `adjust-config`(改 Embedded Coder 配置) / `accept-residual`(文档化接受 + 评审签字) / `out-of-mbd-scope`(代码侧手工修复,需配置管理审批)
   - Polyspace 设置审查给出"过严 / 适中 / 过松"判断 + 依据
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留代码文件名 / 函数名 / 变量名 / 错误 ID 原文

## 聚焦范围(只做这些)

1. 错误分类(Code Prover 抽象解释 / Bug Finder 缺陷类型)
2. 严重度评估(Red / Orange / Green / Gray)
3. 模型侧根因反推(经 `codegen_output_map`)
4. 闭环路由(`refactor-model` / `adjust-config` / `accept-residual` / `out-of-mbd-scope`)
5. Polyspace 设置审查(规则集 / 严格度)
6. 与定点重构 / 存储类治理的关联(若涉及)
7. 与 SLDV 形式化属性的对照(对相同关注点的不同手段对比)

## 不负责

1. 真实运行 Polyspace(用户已运行)
2. 修改代码或模型(本 skill 只做分析与路由)
3. 替代手工 code review(本 skill 只看 Polyspace 报告)
4. MISRA C / CWE / CERT C 规则审查的具体规则解释(那是 Polyspace 输出,本 skill 直接引用)
5. 设计形式化属性 → 走 `clm-sldv-property-author`
6. 真实 Bug 调试(由工程师做)

## 推荐分析顺序

1. 先看"工具上下文与规则集" — 决定 finding 口径
2. 再看"严重度分布" — 优先看 Red,再看 Orange
3. 再做"代码侧分类" — Polyspace 自动分类 + 项目特异性补充
4. 再做"模型侧根因反推" — 经 `codegen_output_map` 中转
5. 再做"闭环路由" — `refactor-model` 优先(MBD 项目),其次 `adjust-config`,再次 `accept-residual`,最后 `out-of-mbd-scope`(需审批)
6. 最后做"Polyspace 设置审查" — 是否过严 / 过松

## 执行步骤

1. **确认工具上下文**:Polyspace 版本、规则集、目标硬件、并发分析是否启用、许可证
2. **报告解析**:加载报告并按严重度分组(Red / Orange / Green / Gray)
3. **代码侧分类**:每条 finding 标 Polyspace 内置类型(Overflow / Divide-by-Zero / OOB / Uninitialized / Dead Code / Concurrency / 其他)
4. **模型侧根因反推**:
   - 通过 `codegen_output_map.model_to_code_map` 找代码位置 → 模型对象
   - 反推可能的模型根因(数据字典类型不当 / 参数范围不严 / 模型结构问题 / 配置问题)
   - 无 `codegen_output_map` 时降级为"建议根因",置信度低
5. **闭环路由**:对每条 finding 选 `refactor-model` / `adjust-config` / `accept-residual` / `out-of-mbd-scope` 之一
   - `refactor-model`:转 `clm-codegen-compliance-refactor`,backlog 含具体重构步骤
   - `adjust-config`:转 `clm-embedded-coder-config-reviewer`,backlog 含配置项调整
   - `accept-residual`:文档化理由 + 评审签字环节
   - `out-of-mbd-scope`:代码层手工修复,需配置管理审批(MBD 项目通常不推荐)
6. **关联其他 skill**:
   - 若错误为定点 Overflow,关联 `fixed_point_refactor_plan`
   - 若错误为存储类访问越界,关联 `storage_class_governance`
   - 若错误对应已设计的 SLDV 属性,关联 `sldv_property_set`(对照同关注点的不同手段)
7. **Polyspace 设置审查**:
   - 规则集是否过严(误报多)/ 过松(漏检多)/ 适中
   - 项目特异性建议
8. **生成工件**:按 `references/output-template.md` 填充
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 严重度分布(`Red` / `Orange` / `Green` / `Gray` 数量)
3. 错误清单(主表)
4. 模型侧根因反推汇总
5. 闭环路由汇总(四枚举数量分布)
6. Polyspace 设置审查
7. 与其他 skill 的关联(`fixed-point-refactor` / `storage-class-governor` / `sldv-property-author`)
8. 关键事实(Facts)、关键推断(Inferences)
9. 证据索引(代码文件:行号 + 模型对象路径)
10. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **必需**:Polyspace 报告
   - **必需**:生成代码目录
   - (强烈推荐)`codegen_output_map`
   - (推荐)`simulink_model_map` / `data_dictionary_map`
   - (可选)`fixed_point_refactor_plan` / `storage_class_governance` / `sldv_property_set`
2. 下游使用方
   - `clm-codegen-compliance-refactor`(消费 `refactor-model` 路由 → 模型重构 backlog)
   - `clm-embedded-coder-config-reviewer`(消费 `adjust-config` 路由 → 配置调整 backlog)
   - `clm-fixed-point-refactor`(消费溢出类 finding,若涉及定点)
   - `clm-storage-class-governor`(消费访问越界类 finding,若涉及存储类)
   - `clm-control-law-mbd-pipeline`(汇总)
3. 主交付工件
   - `polyspace_runtime_error_findings`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`finding_table`、`severity_distribution`、`closure_routing`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不运行 Polyspace / 不修改代码或模型 / 不替代 code review / 不解释 MISRA 规则
   - 严重度纪律(Severity Discipline):至少覆盖 Red 与 Orange 级别;Green / Gray 视情况
   - 反推纪律(Root Cause Discipline):每条 finding 必须经 `codegen_output_map` 中转或显式标"无中转,根因为建议"
   - 闭环路由纪律:每条 finding 落到四枚举之一;`out-of-mbd-scope` 必须有审批要求声明
   - 设置审查纪律:规则集严格度判断有依据(不只是主观判断)
   - 工具上下文门禁:Polyspace 版本 / 规则集 / 目标硬件 / 许可证显式
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供 Polyspace 报告**:本 skill 阻断;提示用户先运行 Polyspace
   - **报告形态未识别**:列出已知支持形态,请用户提供格式说明或转换
   - **未提供 `codegen_output_map`**:模型侧根因反推降级为"建议根因",置信度低
   - **未提供 `simulink_model_map`**:模型对象路径定位降级
   - **目标硬件未确认**(影响 Overflow 判定):标 Overflow 类 finding 为"待目标硬件确认"
2. 输出降级要求
   - 降级输出必须显式标注受影响 finding 与置信度变化
   - 降级不等于跳步;不得给"已无运行时错误"或"已通过 Polyspace 门"的最终结论(由编排技能 / 工程师聚合判定)

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,错误清单与闭环路由表直接套用
2. 交付前用 `references/checklist.md` 复核反推纪律、路由纪律、设置审查
3. 大型报告(> 100 finding)按严重度分批输出

## 分析纪律

1. MBD 项目优先 `refactor-model`,不优先 `out-of-mbd-scope` — 后者破坏 MBD 一致性
2. `accept-residual` 需要具名评审签字 — Polyspace 的 Orange 不等于"可接受"
3. 定点 Overflow / 数组越界 等高频 finding 转专项 skill — 本 skill 只做路由
4. Polyspace 报告 ≠ 完美 — 误报存在,设置审查必不可少
5. 不下"已通过 Polyspace 门"结论 — 由编排技能基于覆盖与残留风险判定
6. 与 SLDV 属性对照(若有):同一关注点(如"控制量在范围内")可能既有 Polyspace finding 又有 SLDV 属性 → 互相印证或互相纠正
