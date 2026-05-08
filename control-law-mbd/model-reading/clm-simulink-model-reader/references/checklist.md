# 检查清单(Checklist)

用于在交付 `clm-simulink-model-reader` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-simulink-model-reader 专项检查

- [ ] 至少串起一条完整"输入端口 → 子系统链 → 输出端口"路径
- [ ] 采样时间(Sample Time)结论指向具体 Block / Subsystem 与值,不依赖默认假设
- [ ] 原子子系统(Atomic Subsystem)与虚拟子系统(Virtual Subsystem)被显式区分
- [ ] 多速率边界(Multirate Boundary)已标注
- [ ] Mask 子系统的参数面板与初始化代码出处已记录
- [ ] 引用模型(Model Reference)与库链接(Library Link)已列出指向

## 工具上下文(Tool Context)

- [ ] Simulink / Stateflow 版本已确认或标注 `unknown`
- [ ] 模型形态(`.slx` / `.mdl`)已记录
- [ ] 许可证可用性已记录;无许可证时降级路径(模型源解析)已声明
- [ ] `.sldd` 绑定关系已记录(若未绑定亦显式说明)

## 输入与范围

- [ ] 模型路径与版本/分支已记录
- [ ] 用户关注链路或子系统已确认(或采用顶层默认)
- [ ] 加密 / 受保护子系统已在 `gaps` 中登记
- [ ] 输入缺口(Gaps)及其影响已列出

## 证据与结论

- [ ] 关键结论均有"模型路径 + 子系统路径"证据(如 `model.slx > Controller/AttitudeLoop/PID`)
- [ ] 已区分事实(Fact)与推断(Inference)
- [ ] 未把 Subsystem 名当成语义结论,语义结论均回到内部 Block 与端口
- [ ] 未越权给出 Stateflow 语义或代码生成结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `simulink_model_map`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs`
- [ ] 子系统层级树包含 Atomic / Virtual / Model Reference 标记
- [ ] 下游 skill (`clm-stateflow-semantics-reader` / `clm-data-dictionary-reader` / `clm-codegen-output-mapper`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出,而不是跳步给终局结论
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作(获取许可证 / 提供 `.sldd` / 解锁子系统 等)

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 子系统名 / 信号名 / 参数名 / Bus 名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
