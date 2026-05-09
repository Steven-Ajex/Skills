# 检查清单(Checklist)

用于在交付 `clm-gain-scheduling-author` 输出前做快速复核。

## clm-gain-scheduling-author 专项检查

- [ ] 基础 pattern 引用清晰(已有 `control_law_pattern_skeleton` 或 Subsystem 路径)
- [ ] 每个调度变量含:信号名 + 类型 + 范围 + 选型理由
- [ ] 工况网格定义完整;每维度离散点 + 边界点齐全
- [ ] 网格密度选择有理由(关键工况点 + 边界 + 插值密度平衡)
- [ ] 调度表结构(1-D / N-D + 维度顺序)显式
- [ ] 插值方式(线性 / 平直 / 三次样条 / 最近邻)显式
- [ ] 边界外推策略(Clip / Linear Extrap / Hold)显式
- [ ] 调度切换平滑机制(bumpless transfer)显式给出,不允许默认
- [ ] 多通道处置(独立 / 共享 / MIMO)显式判定
- [ ] 接入 diff 可施工(每个增益从 Constant 改为 Lookup Table 输出)
- [ ] `Simulink.LookupTable` 声明含数据占位 + Storage Class 建议
- [ ] 风险登记含 bumpless / 边界外推 / 调度变量噪声 / 定点插值精度

## 工具上下文(Tool Context)

- [ ] Simulink 版本与 Lookup Table Block 类型已记录
- [ ] 数值形态(浮点 / 定点)显式声明;定点时已声明转交 `clm-fixed-point-refactor`
- [ ] 采样时间 + 调度更新率已记录
- [ ] 是否使用 `Simulink.LookupTable` 对象已声明

## 输入与范围

- [ ] 基础 pattern 引用已记录
- [ ] 调度变量集合已记录;未提供时已阻断
- [ ] 工况网格已提供;未提供时已阻断或降级
- [ ] (可选)上游工件 / 项目级调度规范 是否提供
- [ ] 输入缺口(Gaps)已列出

## 调度变量纪律

- [ ] 变量数 ≤ 3 优先(若 > 3 已说明理由)
- [ ] 选型理由含:飞行包线相关性 + 噪声敏感性 + 可观测性
- [ ] 调度变量噪声前置滤波已考虑

## 工况网格纪律

- [ ] 网格密度选择有理由
- [ ] 边界点必含
- [ ] 关键工况点显式标注

## bumpless 纪律

- [ ] bumpless transfer 机制(一阶低通 / 渐变 / Slew Rate Limit)显式
- [ ] 与积分项的相互作用(若涉及)已说明
- [ ] 没有默认假设"插值会自动平滑"

## 多通道纪律

- [ ] 显式判定独立 / 共享 / MIMO
- [ ] 默认按"独立"时已声明假设

## 边界与纪律

- [ ] 没有重做基础 pattern / 没有修改模型 / 没有给具体数值 / 没有采集工况点
- [ ] 没有给"调度已可投产"结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `gain_scheduling_skeleton`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `pattern_choice` / `scheduling_variables` / `grid_definition` / `lookup_structure` / `risk_register`
- [ ] 工程师可直接施工
- [ ] 风险登记可被 `clm-codegen-compliance-refactor` 直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响段与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 调度变量名 / 参数名 / Block 名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
