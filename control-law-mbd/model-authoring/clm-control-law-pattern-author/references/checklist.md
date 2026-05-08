# 检查清单(Checklist)

用于在交付 `clm-control-law-pattern-author` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-control-law-pattern-author 专项检查

- [ ] Pattern 选型说明 + 与替代方案的折中已显式说明
- [ ] 端口契约(输入/输出端口表)已给出
- [ ] 主拓扑(Block 列表 + 端口 + 信号连接)已给出
- [ ] 所有可调参数用 `Simulink.Parameter` 声明,含类型 / 默认值占位 / Min/Max 占位 / Storage Class 建议
- [ ] 采样时间(SampleTime)显式给出且不依赖继承(若上层多速率)
- [ ] 原子化策略(是否 Atomic Subsystem)已说明,与代码生成约束一致
- [ ] (若 pattern 含积分器)抗饱和(Anti-Windup)实现已显式给出方案 — Back-calculation / Conditional Integration / Clamping
- [ ] 附属结构(滤波 / 死区 / 速率限制)已给出(若 pattern 要求)
- [ ] 集成步骤逐步可施工(无"开始建模"等模糊语)
- [ ] 风险登记(`risk_register`)至少含数值稳定性、与既有结构冲突、多速率边界、抗饱和死区四类

## 工具上下文(Tool Context)

- [ ] Simulink 版本与目标库已确认或标注 `unknown`
- [ ] 目标采样时间 + 多速率边界已记录
- [ ] 数值形态(浮点 / 定点;若定点 Word/Fraction Length)已显式声明
- [ ] 代码生成约束(Embedded Coder 默认 / 高完整性 / MISRA / AUTOSAR)已记录
- [ ] 项目级控制律建模规范来源(若有)已声明

## 输入与范围

- [ ] Pattern 选型已确认
- [ ] 目标子系统路径或"新建"标记已确认
- [ ] (可选)`simulink_model_map` / `data_dictionary_map` / `requirement_trace_map` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 边界与纪律

- [ ] 没有直接修改模型(只产出骨架)
- [ ] 没有给具体参数数值(只给占位)
- [ ] 没有给调参建议
- [ ] 没有审查 Coder 配置 / 没有设计测试用例
- [ ] Anti-Windup 不是事后补(若有积分器)

## 完整性纪律(Completeness Discipline)

- [ ] 至少七项齐全:pattern 选型 + 端口契约 + 主拓扑 + 参数对象 + 采样时间 + 集成步骤 + 风险登记
- [ ] 七项中任一缺失已在 `gaps` 中显式登记并降级

## 数值与采样纪律

- [ ] 数值形态(浮点 vs 定点)未明确时已阻断
- [ ] 采样时间未明确时已阻断
- [ ] 多速率系统下 SampleTime 显式给出而非继承

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `control_law_pattern_skeleton`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `pattern_choice` / `structural_constraints` / `risk_register`
- [ ] 下游 skill / 工程师可直接施工
- [ ] 风险登记可被 `clm-codegen-compliance-refactor` 直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出(端口/参数置信度降级)
- [ ] 已标注受影响骨架部分与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] Block 名 / 参数名 / 信号名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
