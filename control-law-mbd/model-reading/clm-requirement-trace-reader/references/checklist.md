# 检查清单(Checklist)

用于在交付 `clm-requirement-trace-reader` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-requirement-trace-reader 专项检查

- [ ] 需求条目清单完整(至少 ID / 标题 / 状态;可选优先级 / 类型)
- [ ] 三向矩阵(需求 ↔ 模型对象 ↔ 用例)已建立
- [ ] orphan 清单已显式给出(零条也写"无 orphan")
- [ ] broken link 清单已显式给出(零条也写"无 broken")
- [ ] 反向追溯结论(若有上游模型/用例工件)已给出
- [ ] 高优先级且 status = active 的 orphan 已高亮

## 工具上下文(Tool Context)

- [ ] 需求工具(Simulink Requirements / DOORS / ReqIF / Polarion / Jira / 自研)与版本已确认或标注 `unknown`
- [ ] 需求源形态(`.slreqx` / `.reqifz` / `.reqif` / CSV / API 导出)已记录
- [ ] 链接存储形态(模型内嵌 / 外部 / 数据库)已记录
- [ ] 许可证可用性已记录;无许可证时降级到序列化文件解析的路径已声明

## 输入与范围

- [ ] 需求源路径已记录
- [ ] (可选)`simulink_model_map` / `stateflow_semantics` / `test_harness_plan` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 矩阵完整性纪律(Matrix Completeness Discipline)

- [ ] 每条链接给出"需求 ID + 目标对象路径或用例 ID"
- [ ] 矩阵无遗漏(对每条需求至少声明"无链接"或"链接到 X")
- [ ] 多目标链接(一条需求 → 多个对象)清晰列出
- [ ] 多源链接(多条需求 → 一个对象)清晰列出

## 反向追溯纪律(Reverse Traceability Discipline)

- [ ] 模型对象覆盖率已计算(若有 `simulink_model_map`)
- [ ] 用例覆盖率已计算(若有 `test_harness_plan`)
- [ ] 无引用的对象/用例已列出,但**未**判定为"不需要"
- [ ] 上游工件版本与需求源版本不一致时已显式声明

## 链接质量审查

- [ ] 链接是否有理由说明(若工具支持)已记录
- [ ] 链接审计状态(已审计 / 待评审 / 未审计)已记录
- [ ] 已标注链接质量与改进建议(转交需求工程师 / 评审环节)

## 边界与纪律

- [ ] 没有评审需求本身的质量(可读性 / 可测性 / 一致性)
- [ ] 没有解读需求源文档
- [ ] 没有修改任何文件
- [ ] 没有设计用例
- [ ] 没有给"需求覆盖足够 / 不足"的结论(由 `clm-coverage-gap-analyzer` 与编排技能聚合判定)

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `requirement_trace_map`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `traceability_index`
- [ ] 下游 skill (`clm-test-harness-builder` / `clm-coverage-gap-analyzer`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 需求 ID / 标题保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
