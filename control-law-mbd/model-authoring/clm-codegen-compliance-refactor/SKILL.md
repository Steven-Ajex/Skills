---
name: clm-codegen-compliance-refactor
description: 把上游 skill 发现的"模型层不合规问题"(来自 coder_config_review / coverage_gap_report / storage_class_governance / control_law_pattern_skeleton 的风险登记 等)聚合为"模型层重构方案"的写操作类技能 — 输出每条 finding 的最小重构步骤、风险登记、回归点与排好优先级的 backlog。用于已有问题清单需要落到模型层重构动作时;不负责真实执行重构(只产出方案)、不负责审查 Coder 配置、不负责覆盖率分析、不负责存储类治理决策(只消费其 backlog)。
---

# Control-Law-MBD: Codegen Compliance Refactor

## 目标

把"散落在各上游工件里的模型层不合规问题"集中成一份可执行的重构方案,产出 `compliance_refactor_diff` 工件。本 skill **只产出方案**(diff 描述 + 重构步骤 + 风险登记),**不直接修改模型** — 由工程师按方案手工或脚本化施工。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一项目 + 单一目标合规规范(High Integrity / MISRA / AUTOSAR / 公司规范)范围内,把上游 finding 聚合并转化为模型层重构步骤,产出 `compliance_refactor_diff` 工件
2. 工具上下文(Tool Context)
   - Simulink 版本与 Model Advisor 规则集
   - 目标合规规范(High Integrity Modeling Guidelines / MAAB / MISRA Modeling / AUTOSAR / 公司规范)
   - 数值形态(浮点 / 定点)
   - 由上游工件 `tool_context` 累加形成"重构对象的工具矩阵"
3. 核心输入(Inputs)
   - 至少一个上游 finding 来源(必需,推荐多个):
     - `clm-embedded-coder-config-reviewer` 的 `coder_config_review`(配置层风险)
     - `clm-coverage-gap-analyzer` 的 `coverage_gap_report`(`needs-model-refactor` 类缺口)
     - `clm-storage-class-governor` 的 `storage_class_governance`(改造 backlog)
     - `clm-control-law-pattern-author` 的 `control_law_pattern_skeleton`(风险登记)
   - 目标合规规范(可选,缺省采用通用高完整性)
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`(用于评估重构的影响范围)
   - (可选)项目级建模规范文档
4. 核心输出(Outputs)
   - 主交付工件:`compliance_refactor_diff`
   - 重构条目清单(每条:来源 finding + 重构步骤 + 风险等级 + 影响范围 + 回归点 + 接受 / 拒绝 / 待评审)
   - 排好优先级的 backlog
   - 与既有结构冲突清单(若适用)
5. 完成判据(Definition of Done, DoD)
   - 每条 finding 至少给出"最小重构步骤"或显式"建议接受残留 + 理由"
   - 风险等级(高 / 中 / 低)+ 影响范围 + 回归点齐全
   - backlog 已排序;高风险条目单独标记
   - 工具矩阵一致性已校验,冲突时阻断
   - 数值形态影响(若涉及定点)显式列出
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留 Block 名 / 参数名 / 配置项名(英文)原文

## 聚焦范围(只做这些)

1. 聚合上游 finding(配置 / 覆盖率 / 存储类 / pattern 风险)
2. 把每条 finding 转化为模型层重构步骤(逐 Block / 逐子系统 / 逐参数)
3. 风险等级 + 影响范围 + 回归点
4. 与既有结构冲突识别
5. backlog 排序与高风险标记
6. 接受残留(`accept-residual`)的理由文档化(若有)

## 不负责

1. 真实修改模型(本 skill 只产出方案)
2. 审查 Coder 配置 → 走 `clm-embedded-coder-config-reviewer`
3. 覆盖率分析 → 走 `clm-coverage-gap-analyzer`
4. 存储类全局治理决策 → 走 `clm-storage-class-governor`
5. 设计新 pattern → 走 `clm-control-law-pattern-author`
6. 测试用例与覆盖率工具运行 → 走 `verification/`

## 推荐重构顺序

1. 先看"工具矩阵一致性" — 上游工件不一致时阻断
2. 再做"finding 聚合与去重" — 同一 Block 在多个上游被命中时合并
3. 再判定"修复 vs 接受残留" — 部分 finding 可接受,但必须有文档化理由
4. 再设计"最小重构步骤" — 优先模型层最小改动,避免破坏既有结构
5. 再识别"与既有结构冲突" — 重构是否影响其他子系统/参数/接口
6. 最后排序"backlog" — 高风险 + 易修复优先

## 执行步骤

1. **校验工具矩阵**:对照上游工件 `tool_context`,Simulink/Coder 版本 + 数值形态一致;不一致阻断
2. **基线声明**:目标合规规范(High Integrity / MISRA / AUTOSAR / 公司规范),显式
3. **finding 聚合**:
   - 按"模型对象路径"做主键去重
   - 同一对象多 finding 合并,保留各自来源标签
4. **逐条 finding 转化**:
   - 决策枚举:`refactor` / `accept-residual` / `defer`(推迟) / `cannot-fix-in-model`(需配置层 / 嵌入式侧解决)
   - 若 `refactor`:给最小重构步骤(逐 Block 或逐参数)
   - 若 `accept-residual`:给文档化理由 + 哪个评审环节签字
   - 若 `defer`:给延迟原因 + 触发再评审的条件
   - 若 `cannot-fix-in-model`:转交给对应 skill(配置 / 嵌入式)
5. **风险与影响**:每条 `refactor` 给等级 + 影响范围 + 回归点
6. **冲突识别**:对照 `simulink_model_map`,标注重构是否影响其他对象
7. **backlog 排序**:高风险 + 高影响 + 易修复优先
8. **生成工件**:按 `references/output-template.md` 填充
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具矩阵一致性结论
2. 目标合规规范声明
3. finding 聚合表(按模型对象主键)
4. 逐条决策表(`refactor` / `accept-residual` / `defer` / `cannot-fix-in-model`)
5. 重构步骤(最小改动)
6. 风险与影响表
7. 与既有结构冲突清单
8. 排序 backlog(优先级 + 高风险标记)
9. 关键事实(Facts)、关键推断(Inferences)
10. 证据索引(上游工件回引 + 模型对象路径)
11. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 至少一个上游 finding 来源(必需)
   - (推荐)`simulink_model_map`(影响范围)
   - (可选)项目级建模规范
2. 下游使用方
   - 工程师 / 评审(直接按方案施工)
   - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
   - 上游 skill 反馈环路:重构后再次运行 `clm-embedded-coder-config-reviewer` / `clm-coverage-gap-analyzer` / `clm-storage-class-governor` 验证
3. 主交付工件
   - `compliance_refactor_diff`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`refactor_steps`、`risk_register`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`(第 4 节"原子技能边界规则")
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不直接改模型 / 不审查 Coder 配置 / 不做覆盖率分析 / 不做存储类治理决策(只消费 backlog)
   - 证据门禁:每条决策给出"上游工件回引(类型 + 段)"
   - 工具矩阵一致性:不一致时阻断
   - 决策完整性:每条 finding 落到四类决策之一,带步骤或理由
   - 风险纪律(Risk Discipline):每条 `refactor` 必须有等级 + 影响范围 + 回归点
   - 冲突识别纪律:重构是否影响其他对象必须显式判断(若有 `simulink_model_map`)
   - 接受残留纪律(Residual Acceptance Discipline):`accept-residual` 必须有文档化理由 + 评审签字环节
   - 交接门禁:工件可被工程师与下游 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供任何上游 finding**:本 skill 阻断;提示先运行 `clm-embedded-coder-config-reviewer` 等
   - **上游 `tool_context` 不一致**:阻断;先要求上游对齐
   - **未提供目标合规规范**:声明采用"通用高完整性建议"作为基线
   - **未提供 `simulink_model_map`**:冲突识别章节降级,标注"未与模型结构核对",置信度低
   - **数值形态(浮点/定点)未确定**:阻断对定点相关 finding 的重构步骤
2. 输出降级要求
   - 降级输出必须显式标注受影响决策与置信度变化
   - 降级不等于跳步;不得越过本技能职责给"已可投产"的结论 — 由工程师施工 + 上游 skill 反馈环路验证

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,finding 聚合表与 backlog 直接套用
2. 交付前用 `references/checklist.md` 复核决策完整性、风险纪律、接受残留纪律、降级
3. 大型项目:先输出"工具矩阵 + 基线声明 + 聚合表",再分批给重构步骤(按优先级)

## 重构纪律

1. 不做"应该改成 X"式的孤立建议 — 必有步骤 + 风险 + 影响 + 回归点
2. 不假设"上游 finding 一定要修" — 部分可 `accept-residual`,但必须文档化
3. 不把"配置层 / 嵌入式侧应解决的问题"硬塞到模型层 — 标 `cannot-fix-in-model` 并转交
4. 重构步骤优先"最小改动" — 拆出新 Block 比改既有 Block 风险通常更高,但具体由影响评估决定
5. 反馈环路:重构后必须由对应上游 skill 再次验证(由编排技能或工程师驱动),本 skill 不下"重构成功"结论
