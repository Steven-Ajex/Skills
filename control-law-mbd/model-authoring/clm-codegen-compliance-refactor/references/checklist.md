# 检查清单(Checklist)

用于在交付 `clm-codegen-compliance-refactor` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-codegen-compliance-refactor 专项检查

- [ ] 至少一个上游 finding 来源已提供
- [ ] 工具矩阵一致性结论已声明;不一致时已阻断
- [ ] 目标合规规范基线(High Integrity / MISRA / AUTOSAR / 公司规范 / 通用高完整性)已显式声明
- [ ] finding 聚合表按"模型对象路径"主键去重,多源 finding 已合并并保留来源标签
- [ ] 每条 finding 落到四类决策之一:`refactor` / `accept-residual` / `defer` / `cannot-fix-in-model`
- [ ] 每条 `refactor` 有最小重构步骤(逐 Block / 逐参数)
- [ ] 每条 `accept-residual` 有文档化理由 + 评审签字环节
- [ ] 每条 `defer` 有延迟原因 + 触发再评审条件
- [ ] 每条 `cannot-fix-in-model` 已转交给对应 skill(配置 / 嵌入式)

## 工具上下文(Tool Context)

- [ ] Simulink 版本与 Model Advisor 规则集已记录
- [ ] 数值形态(浮点 / 定点)已显式声明;定点形态时 Q 格式已记录
- [ ] 上游工件 `tool_context` 已汇总成"重构对象的工具矩阵"

## 风险与影响纪律

- [ ] 每条 `refactor` 含风险等级(高/中/低)
- [ ] 每条 `refactor` 含影响范围(本子系统 / 跨子系统 / 跨接口)
- [ ] 每条 `refactor` 含回归点(测试/覆盖率/PIL/HIL)
- [ ] 高风险条目单独标记

## 冲突识别

- [ ] (若有 `simulink_model_map`)重构是否影响其他对象已显式判断
- [ ] 与既有 pattern / 既有桥接层接口的冲突已列出
- [ ] 没有 `simulink_model_map` 时章节降级标签已传递

## 接受残留纪律(Residual Acceptance Discipline)

- [ ] `accept-residual` 决策不超过总数的合理比例(由项目质量门决定)
- [ ] 每条 `accept-residual` 文档化理由可被审计
- [ ] 高优先级 finding 不允许默认 `accept-residual`

## backlog 排序

- [ ] 高风险 + 高影响 + 易修复优先
- [ ] 排序依据(评分 / 矩阵)已说明
- [ ] 高风险条目单独列出

## 边界与纪律

- [ ] 没有直接修改模型(只产出方案)
- [ ] 没有审查 Coder 配置 / 没有做覆盖率分析 / 没有做存储类治理决策
- [ ] 没有给"已可投产"的结论
- [ ] 反馈环路(重构后由上游 skill 再次验证)已说明

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `compliance_refactor_diff`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `refactor_steps` / `risk_register`
- [ ] 工程师可直接施工
- [ ] 反馈环路给出再次验证 skill 列表

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响决策与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] Block 名 / 参数名 / 配置项名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
