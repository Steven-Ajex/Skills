---
name: clm-model-to-deploy-handoff
description: Pipeline Stage 5 的合成型 workflow skill — 把 Stage 1-4 产出的所有原子工件聚合成一份"模型 → 部署"交接包(版本声明、合规摘要、覆盖率与验证摘要、跨库接口契约、残留风险与文档化接受清单、回归点与下一步动作),供 release manager / 集成工程师 / FMT 维护方直接消费。用于"控制律模型已通过 Stage 4 验证、需要交付到嵌入式集成或 release"场景;不重做任何阶段的专业判断、不做具体改动、不替代 release 流程本身、不下"已可投产"结论(由用户基于本工件做最终决策)。
---

# Control-Law-MBD: Model-to-Deploy Handoff (Stage 5 Synthesis Workflow)

## 目标

把 `pipeline_status` + Stage 1-4 全部原子工件聚合为一份**可审计、可审查、可索引**的"模型 → 部署"交接包,产出 `deploy_handoff_package` 工件。本 skill 是 Stage 5,**不发现新事实、不做新决策**,只做"合成 + 索引 + 风险汇总 + 交付清单"。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一项目 + 单一交付里程碑(release / integration milestone)范围内,聚合 Stage 1-4 工件 + `pipeline_status`,生成可被 release manager / 集成工程师 / FMT 维护方直接消费的交接包,产出 `deploy_handoff_package` 工件
2. 工具上下文(Tool Context)
   - 由 Stage 1-4 工件的 `tool_context` 累加(本 skill 只校验一致性,不产生新上下文)
   - 项目级 release / 配置管理流程(若提供)
   - 跨库 FMT 端 `firmware_context`(若涉及)
3. 核心输入(Inputs)
   - **必需**:`clm-control-law-mbd-pipeline` 的 `pipeline_status`
   - **必需**:Stage 1-4 主要原子工件(`simulink_model_map` / `data_dictionary_map` / `coder_config_review` / `codegen_output_map` / `storage_class_governance` / `test_harness_plan` / `coverage_gap_report` / `pil_hil_replay_findings` 等,按 `pipeline_status` 索引取用)
   - **可选**:`requirement_trace_map` / `stateflow_semantics` / `anti_windup_design` / `compliance_refactor_diff` / `fixed_point_refactor_plan` / `flight_log_replay_dataset` 等
   - **可选**:项目 release 模板 / 集成对接清单
4. 核心输出(Outputs)
   - 主交付工件:`deploy_handoff_package`
   - 版本与配置声明(模型 + 字典 + 生成代码 + 工具版本)
   - 合规摘要(配置审查 / 命名 / 存储类 / 高完整性建模)
   - 验证摘要(用例集合 + 覆盖率 + PIL/HIL + 实飞对照)
   - 跨库接口契约(`bridge_layer_contract` 与 FMT 端核对状态)
   - 残留风险登记(含 `accept-residual` 文档化条目)
   - 回归点清单(下次改动需要重跑的 skill / 测试)
   - 工件索引表(与 `pipeline_status` 中的 artifact 表互引)
   - 下一步动作(给 release / 集成 / FMT 维护方)
5. 完成判据(Definition of Done, DoD)
   - 版本与配置声明完整(模型 + 字典 + 代码 + 至少 4 类工具版本:Simulink / Embedded Coder / Simulink Test / 任一覆盖率工具)
   - 合规摘要包含 Stage 3 全部三 skill 的关键结论
   - 验证摘要至少含覆盖率维度(Decision/Condition/MCDC) + PIL/HIL 通过判据评估
   - 跨库接口契约段含 `bridge_layer_contract` 与 FMT 端核对状态(`一致 / 差异 / 未核对`)
   - 残留风险按等级排序,`accept-residual` 条目含理由 + 文档位置 + 评审签字环节
   - 工件索引完整(每条索引可回链到 `pipeline_status` 中的 artifact)
   - 工具上下文一致性已校验(沿 Stage 1-4 矩阵)
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留模型路径 / 字典对象名 / 配置项原文 / 用例 ID / FMT 端字段名

## 聚焦范围(只做这些)

1. 版本与配置声明(模型/字典/代码/工具,可审计)
2. 合规摘要(配置审查 + 命名 + 存储类)
3. 验证摘要(用例 + 覆盖率 + PIL/HIL + 实飞对照)
4. 跨库接口契约段(`bridge_layer_contract` 与 FMT 端核对状态)
5. 残留风险登记 + `accept-residual` 文档化清单
6. 回归点清单(下次改动需要重跑的 skill / 测试)
7. 工件索引表(指向 `pipeline_status` 工件)
8. 下一步动作(release / 集成 / FMT 维护方)

## 不负责

1. 重做 Stage 1-4 的任何专业判断 — 只引用工件
2. 修改任何模型 / 字典 / 代码 / 配置
3. 替代 release 流程本身(版本管理 / 签发 / 部署执行)
4. 下"已可投产 / 已可交付"的最终结论 — 由用户基于本工件决策
5. 与 FMT 库做实际的接口适配 — 只声明状态,适配由两边工程师做

## 推荐合成顺序

1. 先做"工具矩阵一致性核对" — 不一致时阻断,要求 Stage 1-4 对齐
2. 再做"版本与配置声明" — 模型/字典/代码版本指纹
3. 再做"合规摘要" — Stage 3 工件汇总
4. 再做"验证摘要" — Stage 4 工件汇总
5. 再做"跨库接口契约段" — 与 FMT 维护方对齐状态
6. 再做"残留风险登记" — 按等级排序;`accept-residual` 文档化
7. 再做"回归点清单"
8. 最后做"工件索引"与"下一步动作"

## 执行步骤

1. **读取 `pipeline_status`**:确认所有 Stage 状态(`passed` / `passed_with_warnings` / `blocked` / `skipped`)
2. **工具矩阵一致性核对**:沿 Stage 1-4 工件的 `tool_context`;不一致时阻断
3. **版本与配置声明**:
   - 模型版本(git commit / 时间戳 / Model Advisor 报告)
   - 字典版本(`.sldd` 时间戳 / Reference Dictionary)
   - 生成代码版本(时间戳 + checksum)
   - 工具版本矩阵
4. **合规摘要**:
   - 从 `coder_config_review` 提取关键配置 + 风险结论
   - 从 `codegen_output_map` 提取代码生成形态 + 文件清单
   - 从 `storage_class_governance` 提取治理决策结果
5. **验证摘要**:
   - 从 `test_harness_plan` 提取用例集合
   - 从 `coverage_gap_report` 提取三维度覆盖率 + 缺口分类
   - 从 `pil_hil_replay_findings` 提取通过判据评估 + 退化信号
   - 从 `flight_log_replay_dataset`(若有)提取实飞对照
6. **跨库接口契约段**:
   - `codegen_output_map.bridge_layer_contract` 摘要
   - 与 FMT 端核对状态(`一致 / 差异 / 未核对`)
   - 差异条目转交建议
7. **残留风险登记**:
   - 聚合各上游 `risk_register`
   - 按等级(高 / 中 / 低)排序
   - `accept-residual` 条目独立列出 + 文档位置 + 评审签字
8. **回归点清单**:
   - 下次改动模型时哪些 skill / 测试需要重跑
   - 下次改动配置时哪些 skill 需要重跑
   - 下次升级工具版本时影响范围
9. **工件索引表**:每条工件回链到 `pipeline_status`
10. **下一步动作**:分给 release manager / 集成工程师 / FMT 维护方
11. **生成工件**:按 `references/output-template.md` 填充
12. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具矩阵一致性结论
2. 版本与配置声明
3. 合规摘要(Stage 3 三 skill 汇总)
4. 验证摘要(Stage 4 四 skill 汇总)
5. 跨库接口契约段(模型 → FMT + FMT → 模型)
6. 残留风险登记(含 `accept-residual` 文档化清单)
7. 回归点清单
8. 工件索引表
9. 下一步动作(分角色)
10. 关键事实(Facts)、关键推断(Inferences)
11. 缺口清单

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **必需**:`pipeline_status` + Stage 1-4 主要工件
   - (推荐)项目 release 模板 / 集成对接清单
2. 下游使用方
   - Release manager(版本签发与发布)
   - 集成工程师(嵌入式集成与回归)
   - FMT 维护方(接口适配与跨库验证)
   - 项目评审 / 审计(可追溯性)
3. 主交付工件
   - `deploy_handoff_package`
   - 字段:`tool_context_matrix`、`version_pin`、`compliance_summary`、`verification_summary`、`bridge_layer_status`、`risk_register`、`accept_residual_log`、`regression_points`、`artifact_index`、`next_actions`、`gaps`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`(第 4 节"编排技能边界规则",本 skill 是合成型 workflow)
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不重做专业判断 / 不修改任何文件 / 不替代 release 流程 / 不下"已可投产"结论
   - 工具矩阵一致性:Stage 1-4 工具上下文不一致时阻断
   - 完整性门禁:版本声明 + 合规摘要 + 验证摘要 + 风险登记 + 回归点 + 工件索引 + 下一步动作 七项齐全
   - 风险纪律(Risk Discipline):每条 `accept-residual` 必须含理由 + 文档位置 + 评审签字
   - 跨库纪律(Cross-Library Discipline):接口契约状态(`一致 / 差异 / 未核对`)显式声明
   - 工件索引纪律:每条索引可回链到 `pipeline_status`,不允许"断链"
   - 交接门禁:每条 `next_actions` 必须有"接收角色 + 截止条件"
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供 `pipeline_status`**:本 skill 阻断;先运行 `clm-control-law-mbd-pipeline`
   - **某 Stage 状态 = `blocked`**:在交接包中显式标注"未完成 Stage" + 阻断原因 + 下一步动作;**不**默认 release
   - **某 Stage 状态 = `passed_with_warnings`**:聚合所有 warning 进残留风险;`next_actions` 含"warnings 是否接受"决策点
   - **跨库接口契约未与 FMT 端核对**:状态标 `未核对`,转交清单含"约 FMT 维护方核对"动作
   - **工具矩阵不一致**:阻断,不生成交接包
2. 输出降级要求
   - 降级输出必须显式标注哪些段落基于不完整输入,以及置信度变化
   - 降级不等于跳步;不得给"已可投产"结论 — 让用户基于残留风险与 warning 决策

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,版本声明 / 合规摘要 / 验证摘要直接套用
2. 交付前用 `references/checklist.md` 复核完整性、风险纪律、跨库纪律、索引完整性
3. 大型项目:可分章节交付(version pin / compliance + verification / risk + next actions),但工件应聚合为单份

## 合成纪律

1. 不在本 skill 内重写专业结论 — 引用即可
2. `accept-residual` 不能"软批准" — 必须有具名评审签字环节
3. 工件索引必须可回链 — `pipeline_status` 中索引的 artifact 在本工件中必须可指
4. 跨库接口状态不允许"待补" — 至少标 `未核对` + 转交动作
5. 工具升级影响必须显式列出 — 工具版本是 release 决策的常见盲点
6. 不下"已可投产"结论 — 让用户决策;本 skill 只是把决策依据完整聚合
