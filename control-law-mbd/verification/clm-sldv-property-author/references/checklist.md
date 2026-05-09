# 检查清单(Checklist)

用于在交付 `clm-sldv-property-author` 输出前做快速复核。

## clm-sldv-property-author 专项检查

- [ ] 至少覆盖项目高优先级需求 / 高安全等级约束
- [ ] 每条属性含:自然语言描述 + 形式化表达 + 作用域 + 期望结果
- [ ] 每条 Assumption 显式声明,限制了哪些输入空间
- [ ] 证明边界(Inductive / Bounded + 步数)显式;Bounded 时 N 选型有理由
- [ ] 每条属性分类:`proven` / `falsifiable_expected` / `undecided_acceptable`
- [ ] Test Objective 配套(若涉及 `falsifiable_expected`)
- [ ] Verification Subsystem / Property Block 接入 diff 可施工
- [ ] 模糊需求(如"系统应稳定运行")已显式排除并转交其他验证手段

## 工具上下文(Tool Context)

- [ ] SLDV 版本已确认或标注 `unknown`
- [ ] 证明引擎(Model Checking / SAT / SMT)已记录
- [ ] 是否使用 Verification Subsystem 模式已记录
- [ ] 是否启用 Property Proving + Test Generation 联用已声明
- [ ] 许可证可用性已记录;无许可证时降级到属性表设计已声明

## 输入与范围

- [ ] 需求/约束清单已提供;未提供时已阻断
- [ ] 被验对象路径已记录
- [ ] (可选)`simulink_model_map` / `stateflow_semantics` / `requirement_trace_map` / `fault_injection_test_plan` 是否提供
- [ ] 输入缺口(Gaps)已列出

## 形式化纪律(Formalization Discipline)

- [ ] 每条属性的形式化表达不只是自然语言重述
- [ ] 时序逻辑算子(G/F/U/X)使用一致
- [ ] 表达式语法明确(Simulink 函数 / `assertion()` / Stateflow 时序逻辑)

## Assumption 纪律

- [ ] 每条属性的 Assumption 显式列出
- [ ] Assumption 限制了输入空间(防止 SLDV 状态空间爆炸)
- [ ] Assumption 与设计意图一致(不是"为了证而证")

## 证明边界纪律

- [ ] Inductive / Bounded 已选型
- [ ] Bounded 步数 N 选型有理由(常见 30 / 100 / 300)
- [ ] 多采样系统的最小公倍数采样已考虑

## 期望结果纪律

- [ ] 每条属性分类
- [ ] `falsifiable_expected` 显式标记为设计意图(反例生成),非失败
- [ ] `undecided_acceptable` 有合理性说明(状态空间过大 / 时序复杂等)

## 边界与纪律

- [ ] 没有替代需求工程师写需求
- [ ] 没有真实运行 SLDV
- [ ] 没有修改模型
- [ ] 没有下"已证明"或"已反驳"结论
- [ ] 没有替代常规功能/故障注入测试
- [ ] 与 `test_harness_plan` / `fault_injection_test_plan` 边界声明显式

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `sldv_property_set`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `property_table` / `assumption_table` / `proof_strategy` / `test_objective_table`
- [ ] 工程师 / DV 团队可直接运行 SLDV
- [ ] 反驳的属性可被 `clm-codegen-compliance-refactor` 直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响段与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 属性 ID / 信号名 / 状态名 / Block 名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
