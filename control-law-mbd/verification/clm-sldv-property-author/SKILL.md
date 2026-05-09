---
name: clm-sldv-property-author
description: 把"需求条目 / 安全约束 / 故障检测要求"转化为可被 Simulink Design Verifier(SLDV)证明的形式化属性(Verification Subsystem 与 Proof Block 设计)的写操作类技能 — 输出每条属性的形式化表达、作用域(对象路径)、期望结果(`proven` / `falsified` / `undecided`)、合理证明边界(Inductive vs Bounded)、配套的 Test Objective(若需反例驱动测试)。用于"已有需求/安全约束需要做形式化证明"场景;不替代需求工程师写需求、不真实运行 SLDV(只产出属性集)、不修改模型(只输出 diff)、不下"已证明"结论(由 SLDV 运行结果判定)。
---

# Control-Law-MBD: SLDV Property Author

## 目标

把"需求 / 安全约束 / 故障检测要求"翻译成可被 SLDV(Simulink Design Verifier)证明的形式化属性(Property),并为每条属性给出作用域、期望结果、证明边界(Inductive / Bounded Step)与配套 Test Objective(若需反例驱动测试),产出 `sldv_property_set` 工件。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一被验对象(Subsystem / 模型)+ 单一需求/约束清单范围内,完成形式化属性集合(Property Set)、作用域、期望结果、证明边界设置、Test Objective 配套设计,产出 `sldv_property_set` 工件
2. 工具上下文(Tool Context)
   - SLDV(Simulink Design Verifier)版本
   - 目标证明引擎(Model Checking / SAT / SMT)
   - 是否使用 Verification Subsystem 模式(独立验证子系统)
   - 是否启用 Property Proving + Test Generation 联用
   - 许可证可用性(SLDV 许可证缺失时降级到属性表设计)
3. 核心输入(Inputs)
   - **必需**:需求 / 安全约束清单(可来自 `requirement_trace_map`、FMEA/HARA、项目级安全约束)
   - **必需**:被验对象路径
   - **推荐**:`clm-simulink-model-reader` 的 `simulink_model_map`(对象边界定位)
   - **推荐若涉及状态机**:`clm-stateflow-semantics-reader` 的 `stateflow_semantics`(状态相关属性)
   - **推荐**:`clm-fault-injection-test-author` 的 `fault_injection_test_plan`(故障检测属性)
   - (可选)项目级形式化验证规范
4. 核心输出(Outputs)
   - 主交付工件:`sldv_property_set`
   - 属性集合(每条:ID + 自然语言描述 + 形式化表达 + 作用域 + 期望结果 + 证明边界)
   - 配套 Verification Subsystem / Proof Block / Assumption Block 结构
   - 假设(Assumption)清单(限制证明范围的输入约束)
   - Test Objective(若需反例驱动测试用例生成)
   - 证明边界策略(Inductive Step / Bounded Step + 步数)
   - 与 `test_harness_plan` / `coverage_gap_report` 的边界声明
5. 完成判据(Definition of Done, DoD)
   - 至少覆盖项目高优先级需求 / ASIL/DAL 高等级安全约束
   - 每条属性给出"自然语言描述 + 形式化表达 + 作用域 + 期望结果"
   - 每条 Assumption 显式声明(限制了哪些输入空间)
   - 证明边界(Inductive / Bounded + 步数)显式;Bounded 时给出选 N 的理由
   - 期望结果分类:`proven`(可证明) / `falsifiable_expected`(用作反例生成 → Test Objective) / `undecided_acceptable`(允许 SLDV 给 undecided 的属性)
   - 与常规验证的边界声明显式
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留属性 ID / 信号名 / 状态名 / Block 名(英文)原文

## 聚焦范围(只做这些)

1. 形式化属性的设计与表达(Functional / Safety / Liveness / Deadlock-Freedom 等)
2. Property Block / Verification Subsystem 结构
3. Assumption(输入约束)清单
4. 证明边界策略(Inductive vs Bounded + 步数选型)
5. 期望结果分类(`proven` / `falsifiable_expected` / `undecided_acceptable`)
6. Test Objective 配套(用 SLDV 反例驱动测试)
7. 与 `test_harness_plan` / `coverage_gap_report` / `fault_injection_test_plan` 的边界

## 不负责

1. 替代需求工程师写需求(本 skill 消费需求清单)
2. 真实运行 SLDV(只产出属性集)
3. 修改模型(只输出 Property/Assumption Block 接入 diff)
4. 下"已证明"或"已反驳"结论(由 SLDV 运行结果判定)
5. 替代常规功能/故障注入测试(走 `clm-test-harness-builder` / `clm-fault-injection-test-author`)
6. 详细 Bug 调试 — SLDV 反例由工程师调试

## 推荐设计顺序

1. 先识别"哪些需求 / 约束适合形式化" — 局部、可观测、可写成时序逻辑或断言的最适合
2. 再写"自然语言 → 形式化表达"映射 — 每条属性单独
3. 再设计"Assumption" — 没有合理 Assumption,SLDV 会爆搜状态空间
4. 再选"证明边界" — Inductive 优先(全证),Bounded 用于复杂系统(N 步反例)
5. 再分类"期望结果" — `proven` / `falsifiable_expected` / `undecided_acceptable`
6. 最后写"Test Objective 配套"(若用 SLDV 自动生成测试)

## 执行步骤

1. **确认工具上下文**:SLDV 版本、证明引擎、是否用 Verification Subsystem 模式、许可证
2. **需求/约束筛选**:
   - 从输入清单中筛出适合形式化的条目(局部、可观测、断言式)
   - 不适合的条目(如"系统应稳定运行"等模糊语)显式排除并转交其他验证手段
3. **形式化表达**:
   - 对每条属性写 G(globally) / F(eventually) / U(until) / X(next) 等时序逻辑或简单断言
   - 表达式语法:Simulink 函数 / `assertion()` / Stateflow 时序逻辑
4. **Assumption 清单**:
   - 输入信号范围 / 类型 / 互斥关系
   - 没有 Assumption 时 SLDV 会爆状态空间;必须显式
5. **证明边界**:
   - Inductive Step:全证
   - Bounded Step + 步数:浅层证(给 N 选型理由,常见 30/100/300)
   - 多采样系统选最小公倍数采样
6. **期望结果分类**:每条属性标 `proven` / `falsifiable_expected` / `undecided_acceptable`
7. **Test Objective 配套**(若涉及):为 `falsifiable_expected` 属性写对应 Test Objective(SLDV 自动生成反例 → 测试用例)
8. **Property Block 接入 diff**:Verification Subsystem 中 Block 列表与连接
9. **生成工件**:按 `references/output-template.md` 填充
10. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 需求/约束筛选结论(适合 / 不适合)
3. 属性集合(主表)
4. Assumption 清单
5. 证明边界策略
6. 期望结果分类汇总
7. Test Objective 配套(若适用)
8. Verification Subsystem / Property Block 接入 diff
9. 与其他 verification skill 的边界声明
10. 关键事实(Facts)、关键推断(Inferences)
11. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **必需**:需求/约束清单
   - **必需**:被验对象路径
   - (推荐)`simulink_model_map` / `stateflow_semantics` / `requirement_trace_map` / `fault_injection_test_plan`
2. 下游使用方
   - 工程师 / 评审 / DV 团队(运行 SLDV)
   - `clm-test-harness-builder`(消费 Test Objective 反例 → 自动生成的用例)
   - `clm-coverage-gap-analyzer`(消费 SLDV 运行后的覆盖维度)
   - `clm-codegen-compliance-refactor`(消费 SLDV 反驳的属性 → 模型重构 backlog)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `sldv_property_set`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`property_table`、`assumption_table`、`proof_strategy`、`test_objective_table`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不替代需求工程师 / 不运行 SLDV / 不修改模型 / 不下"已证明"结论
   - 形式化纪律(Formalization Discipline):每条属性含自然语言描述 + 形式化表达 + 作用域;不允许只有自然语言
   - Assumption 纪律:必须显式;无 Assumption 时 SLDV 状态空间爆炸
   - 证明边界纪律:Inductive / Bounded + 步数显式;Bounded 时 N 选型有理由
   - 期望结果纪律:每条属性必须分类(`proven` / `falsifiable_expected` / `undecided_acceptable`)
   - 边界声明纪律:与 `test_harness_plan` / `fault_injection_test_plan` 不重复
   - 工具上下文门禁:SLDV 版本 / 证明引擎 / 许可证显式
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供需求/约束清单**:阻断;形式化的硬前提
   - **SLDV 许可证缺失**:属性集仍可设计;实施阶段降级为"理论方案",标注需 SLDV 才能验证
   - **需求过于模糊**(如"系统应稳定运行"):显式排除,转交其他验证手段(常规仿真 / 用户走查)
   - **未提供 `simulink_model_map`**:作用域定位降级为"建议路径"
   - **未提供 `stateflow_semantics` 但需求涉及状态机**:状态相关属性降级或提示先做 Stage 1
   - **被验对象规模过大**:Bounded Step 步数下调,显式标注证明强度降级
2. 输出降级要求
   - 降级输出必须显式标注受影响属性
   - 降级不等于跳步;不得给"已证明"结论 — 由 SLDV 运行结果判定

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,属性表与 Assumption 表直接套用
2. 交付前用 `references/checklist.md` 复核形式化纪律、Assumption、证明边界
3. 大规模需求清单:先输出筛选结论,再分批落实属性

## 设计纪律

1. 不是所有需求都适合形式化 — 模糊需求要显式排除
2. 没有 Assumption 的属性几乎不可证 — Assumption 越精,证明越快
3. Bounded Step 不是万能 — 反例可能在 N+1 步出现,选 N 必须有理由
4. `falsifiable_expected` 是设计意图(用 SLDV 反例生成测试)— 不是失败,要显式标注
5. 不下"SLDV 证明通过 / 失败"结论 — 由实际运行决定;本 skill 只是产出属性集
6. 与常规测试的边界必须显式 — 形式化与常规测试互补,不互相替代
