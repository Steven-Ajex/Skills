# 检查清单(Checklist)

用于在交付 `clm-stateflow-semantics-reader` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-stateflow-semantics-reader 专项检查

- [ ] Chart 属性(Decomposition、初始化语义、Action Language)已记录
- [ ] 状态层级树(含 Exclusive / Parallel 标记)已给出
- [ ] 至少一条完整状态切换路径"源 → 触发条件 → 转移动作 → 目标"被串起
- [ ] 动作类型(`entry` / `during` / `exit` / `condition_action` / `transition_action`)被显式区分
- [ ] 早晚绑定(Early Return Logic)与 Super Step 行为已记录
- [ ] 转移优先级与默认转移已记录

## 工具上下文(Tool Context)

- [ ] Stateflow / Simulink 版本已确认或标注 `unknown`
- [ ] Chart 属性(Decomposition、Execute at Init、Super Step)已记录
- [ ] Action Language(MATLAB / C)已记录
- [ ] 许可证可用性已记录;无许可证时降级路径已声明

## 输入与范围

- [ ] 模型路径与 Chart 路径已记录
- [ ] 用户关注的状态/事件/转移已确认(或采用默认)
- [ ] 加密 / 受保护 Chart 已在 `gaps` 中登记
- [ ] 输入缺口(Gaps)及其影响已列出

## 证据与结论

- [ ] 每条结论给出"Chart 路径 + 状态/转移名"
- [ ] 已区分事实(Fact)与推断(Inference)
- [ ] `condition_action` 与 `transition_action` 未混用
- [ ] 未越权给出 Simulink 顶层结构或代码生成结论
- [ ] Parallel(AND) Decomposition 下每个并行状态的默认转移单独列出

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `stateflow_semantics`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs`
- [ ] 状态/事件名与跨库(`fmt-fms-state-machine-reader`)对接的命名一致性已检查
- [ ] 下游 skill (`clm-test-harness-builder` / `clm-coverage-gap-analyzer` / `clm-requirement-trace-reader`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 状态名/事件名/变量名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
