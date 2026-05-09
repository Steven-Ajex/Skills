# 检查清单(Checklist)

用于在交付 `clm-anti-windup-author` 输出前做快速复核。

## clm-anti-windup-author 专项检查

- [ ] 方案选型(Back-calculation / Conditional Integration / Clamping 或组合)已显式说明
- [ ] 与替代方案的折中已比较
- [ ] Kt 给出方法(`1/Kp` / `Tustin` / `优化拟合` / 经验值)+ 数值占位区间 + 默认值
- [ ] 连接 diff 可被工程师按图施工(逐 Block + 逐信号)
- [ ] 多通道时已判定独立 / 耦合 / 投影 AW,未默认按单通道处理
- [ ] 性能预测含至少一条定性判断(瞬态恢复 / 过冲方向 / 数值稳定)
- [ ] 与既有滤波 / 限速 / 死区 的相互作用已纳入风险登记

## 工具上下文(Tool Context)

- [ ] Simulink 版本与积分器 Block 类型已记录
- [ ] 数值形态(浮点 / 定点)显式声明;定点时已声明降级或转交 `clm-fixed-point-refactor`
- [ ] 采样时间(Ts)已记录
- [ ] 是否含内置 AW 端口已声明

## 输入与范围

- [ ] 已有控制器路径已记录
- [ ] 饱和约束(`u_min` / `u_max` 或动态边界)已记录;未提供时已阻断
- [ ] (可选)上游工件 / 性能目标 是否提供
- [ ] 输入缺口(Gaps)已列出

## Kt 推导纪律

- [ ] 不只是给单一数值
- [ ] 推导方法显式
- [ ] 占位区间合理(常见 `Kt ∈ [0.5/Kp, 2/Kp]`)

## 多通道纪律(MIMO Discipline)

- [ ] 多通道时显式判定独立/耦合/投影
- [ ] 单通道时显式声明
- [ ] 假设弱耦合时已声明假设

## 边界与纪律

- [ ] 没有重做 pattern 选型 / 没有直接改模型 / 没有给具体调参数值 / 没有做定点重构
- [ ] 没有下"AW 已生效"结论(由测试 / 回放验证)

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `anti_windup_design`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `pattern_choice` / `structural_constraints` / `risk_register`
- [ ] 工程师可直接施工
- [ ] 风险登记可被 `clm-codegen-compliance-refactor` 直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响段与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 参数名 / 信号名 / Block 名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
