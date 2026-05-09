# 检查清单(Checklist)

用于在交付 `clm-fixed-point-refactor` 输出前做快速复核。

## clm-fixed-point-refactor 专项检查

- [ ] 关键信号 / 参数的 Q 格式已选型,每条含 Word Length + Fraction Length + Signed/Unsigned + 数值范围依据
- [ ] 没有"经验值"或"约定俗成"作为 Q 格式依据
- [ ] 溢出 / 饱和 / 量化风险已识别,高风险信号有缓解方案
- [ ] 量化误差对关键性能指标(零点 / 截止频率 / 积分增益)的影响已估计
- [ ] (若涉及积分器)AW 在定点形态下的调整已说明:Kt 量化 + 积分位保留
- [ ] (若涉及滤波器)零点漂移 / SOS 分解 / Levin 形式 已评估
- [ ] 缩放 / 规范化建议已给出
- [ ] 验证步骤至少含"浮点 ↔ 定点对比仿真"

## 工具上下文(Tool Context)

- [ ] Fixed-Point Designer 版本已确认或标注 `unknown`
- [ ] 目标硬件(Word Length / Endianness)已记录;Word Length 未定时已阻断
- [ ] 舍入模式(Floor / Round / Nearest)与饱和模式(Saturate / Wrap)的全局规则已记录
- [ ] 是否使用 Code Replacement Library 已声明
- [ ] 数值范围数据来源(浮点仿真 / 飞行日志 / 设计上限)与覆盖度已声明

## 输入与范围

- [ ] 浮点模型路径已记录
- [ ] 目标硬件已记录
- [ ] 数值范围数据已提供;未提供时已阻断
- [ ] (可选)`simulink_model_map` / `data_dictionary_map` / `control_law_pattern_skeleton` / `anti_windup_design` 是否提供
- [ ] 输入缺口(Gaps)已列出

## 数值范围纪律(Range Data Discipline)

- [ ] 每条 Q 格式有数值范围依据(min / max / typical)
- [ ] 范围数据覆盖度已声明
- [ ] 覆盖度低的信号 Q 格式标注"待覆盖确认"
- [ ] 未给定范围的信号没有给出确定性 Q 格式

## Q 格式完整性

- [ ] 每条给出 Word Length + Fraction Length + Signed/Unsigned
- [ ] 每条给出 Q 格式表达原文(如 `fixdt(1,16,12)`)
- [ ] 反馈环路 Q 格式已迭代(非单次扫描)

## AW 定点纪律(若涉及)

- [ ] Kt 的 Q 格式选择(`Kt < 1` 时 Fraction Length 是否够)已说明
- [ ] 积分项保留位(防止小增量被量化截断)已说明
- [ ] 浮点 AW 假设下的推导是否仍成立已声明

## 滤波器纪律(若涉及)

- [ ] IIR 滤波零点漂移已评估
- [ ] SOS 分解 / Levin 形式 是否需要 已声明
- [ ] FIR 直接形式系数量化已审视

## 验证纪律

- [ ] 浮点 ↔ 定点对比仿真已纳入验证步骤
- [ ] 覆盖率重做(`clm-coverage-gap-analyzer`)已纳入
- [ ] PIL 验证(`clm-pil-hil-replay-analyzer`)已纳入
- [ ] 容差与基准已声明

## 边界与纪律

- [ ] 没有直接改模型 / 没有采集数值范围 / 没有重做 pattern / 没有重做 AW 设计 / 没有审查 Coder 配置
- [ ] 没有下"定点改造已通过验证"结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `fixed_point_refactor_plan`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `pattern_choice` / `structural_constraints` / `refactor_steps` / `risk_register`
- [ ] 工程师可直接施工
- [ ] 风险登记可被 `clm-codegen-compliance-refactor` 直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响 Q 格式与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 信号名 / 参数名 / Q 格式表达保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
