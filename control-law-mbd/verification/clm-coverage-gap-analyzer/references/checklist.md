# 检查清单(Checklist)

用于在交付 `clm-coverage-gap-analyzer` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-coverage-gap-analyzer 专项检查

- [ ] Decision / Condition / MCDC 三维度各自给出覆盖率 % 与缺口清单
- [ ] 至少一条缺口被分类到四类之一(`unreachable` / `unexercised` / `unstable` / `needs-model-refactor`)
- [ ] `unreachable` 缺口给出可达性反向推断证据(不基于"运行未达到"判定)
- [ ] 每条 `unexercised` 缺口指向 `test_harness_plan` 中具体用例分组
- [ ] 每条 `needs-model-refactor` 缺口指向 `clm-codegen-compliance-refactor` 的 backlog
- [ ] `unstable` / Filter 抑制的缺口审查理由可审查;不可审查时升级为正式缺口
- [ ] 状态/转移覆盖(若涉及 Stateflow)对照 `stateflow_semantics`,标注未覆盖的非平凡转移

## 工具上下文(Tool Context)

- [ ] 覆盖率工具(Simulink Coverage / SLDV / Polyspace / 第三方)与版本已确认或标注 `unknown`
- [ ] 报告形态(HTML / XML / cvt / 自定义)已记录
- [ ] 维度配置(是否启用 MCDC / Stateflow Coverage)已记录
- [ ] Filter 状态已记录;Filter 大量启用时已审查可审查性
- [ ] 许可证可用性已记录

## 输入与范围

- [ ] 覆盖率报告路径与被测对象路径已记录
- [ ] (可选)`test_harness_plan` / `simulink_model_map` / `stateflow_semantics` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## Filter 审查

- [ ] 每条 Coverage Filter 列出"过滤对象 + 理由 + 是否可审查"
- [ ] 不可审查的 Filter 已升级为缺口
- [ ] 没有把"100% 覆盖率(含大量 Filter)"当成"测试充分"

## 闭环路由

- [ ] 用例增补、模型重构、显式接受三类路由汇总已给出
- [ ] 显式接受的残留有"理由 + 文档化要求"
- [ ] 没有越权给"已通过覆盖率门"的结论

## 边界与纪律

- [ ] 没有真实运行覆盖率工具
- [ ] 没有重写 `clm-test-harness-builder` 的用例设计(只指向分组)
- [ ] 没有修改模型

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `coverage_gap_report`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `coverage_breakdown`
- [ ] 缺口位置(模型对象路径)与 `test_harness_plan` 的覆盖维度字段可对接
- [ ] 下游 skill (`clm-test-harness-builder` / `clm-codegen-compliance-refactor` / `clm-pil-hil-replay-analyzer`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] Block 路径 / Decision/Condition ID 保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
