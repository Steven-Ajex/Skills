---
name: clm-fixed-point-refactor
description: 把已有的浮点(Floating-Point)Simulink 模型重构为定点(Fixed-Point)模型的方案输出技能 — 基于 Fixed-Point Designer 与目标硬件约束,逐信号/逐参数选择 Q 格式(Word Length + Fraction Length),识别溢出(Overflow)/饱和(Saturation)/量化(Quantization)风险,给出缩放/规范化建议与定点化抗饱和调整,产出验证步骤与回归点。用于"目标嵌入式平台无 FPU 或追求确定性算力"场景下的浮点 → 定点改造;不修改模型(只产出方案)、不替代仿真数据采集、不审查 Coder 配置、不下"定点已通过验证"的结论。
---

# Control-Law-MBD: Fixed-Point Refactor

## 目标

把"浮点模型 + 目标硬件约束 + 信号数值范围数据"转化为可施工的定点重构方案,产出 `fixed_point_refactor_plan` 工件。本 skill 是"定点改造的设计阶段" — 它不替工程师"跑仿真采集范围",但要求工程师把"基于浮点仿真采到的数值范围"作为输入。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一浮点模型 + 单一目标硬件约束 + 单一组数值范围数据(Range Data)范围内,完成逐信号/逐参数 Q 格式选型、风险识别、缩放建议、抗饱和调整、验证步骤,产出 `fixed_point_refactor_plan` 工件
2. 工具上下文(Tool Context)
   - Simulink Fixed-Point Designer 版本
   - 目标硬件(Target Hardware:Word Length 8/16/32、Endianness、Atomic Integer/Float Sizes)
   - 是否使用代码替换库(Code Replacement Library)对定点算子做映射
   - 是否含定点饱和模式(Saturate / Wrap)与舍入模式(Floor / Round / Nearest)的全局规则
   - 数值范围数据来源(浮点仿真 / 飞行日志 / 设计上限)及覆盖度
3. 核心输入(Inputs)
   - 浮点模型路径(必需)
   - 目标硬件描述(必需:Word Length、Endianness)
   - 数值范围数据(必需:每个关键信号 / 参数的 min / max / typical)
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`(信号流与子系统层级)
   - (推荐)`clm-data-dictionary-reader` 的 `data_dictionary_map`(参数对象的现状)
   - (可选)`clm-control-law-pattern-author` 的 `control_law_pattern_skeleton`(控制律结构,影响 AW 定点调整)
   - (可选)`clm-anti-windup-author` 的 `anti_windup_design`(若有,需要定点化重审)
   - (可选)项目级定点规范
4. 核心输出(Outputs)
   - 主交付工件:`fixed_point_refactor_plan`
   - 逐信号/逐参数 Q 格式表(Word Length + Fraction Length + Signed/Unsigned + 选型理由)
   - 溢出 / 饱和 / 量化风险登记
   - 缩放与规范化建议(scaling / normalization)
   - AW 定点调整(若涉及积分器)
   - 验证步骤与回归点
5. 完成判据(Definition of Done, DoD)
   - 至少覆盖关键信号 / 参数(用户指定或全模型扫描)的 Q 格式
   - 每条 Q 格式给出"Word Length + Fraction Length + Signed/Unsigned + 数值范围依据"
   - 溢出风险已识别;高风险信号有缓解方案(增加 Word Length / 加饱和 / 重缩放)
   - 量化误差(Quantization Error)对关键性能指标(零点、截止频率、积分增益)的影响已估计
   - AW 在定点形态下的调整(Kt 量化、积分项保留位)已说明(若涉及 AW)
   - 验证步骤可施工(浮点 ↔ 定点对比仿真、覆盖率重做、PIL 验证)
   - 工具上下文显式记录;数值范围数据覆盖度已声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留信号名 / 参数名 / Q 格式表达(如 `fixdt(1,16,12)`)原文

## 聚焦范围(只做这些)

1. 逐信号 / 逐参数 Q 格式选型(Word Length / Fraction Length / Signed)
2. 溢出 / 饱和 / 量化风险识别与缓解
3. 缩放(Scaling)与规范化(Normalization)建议
4. AW 在定点形态下的调整(Kt 量化、积分位保留)
5. 滤波器(IIR / FIR)定点化的特别处理(零点漂移)
6. 验证步骤与回归点(浮点 ↔ 定点对比、覆盖率、PIL)

## 不负责

1. 真实修改模型(只产出方案)
2. 采集数值范围数据(用户工程实施;本 skill 消费已采到的范围)
3. 重做 pattern 选型 → 走 `clm-control-law-pattern-author`
4. 设计 AW 方案 → 走 `clm-anti-windup-author`(本 skill 仅做定点调整)
5. 审查 Coder 配置 → 走 `clm-embedded-coder-config-reviewer`
6. 设计测试用例 → 走 `clm-test-harness-builder`

## 推荐设计顺序

1. 先看"工具上下文 + 目标硬件 + 数值范围数据覆盖度" — 后两者决定方案精度
2. 再做"参数 Q 格式选型" — 先参数(静态)再信号(动态)
3. 再做"信号 Q 格式选型" — 沿信号流;有反馈环路时迭代
4. 再做"风险扫描" — 溢出 / 饱和 / 量化误差对性能影响
5. 再做"AW 定点调整"(若有积分器) — Kt 量化 + 积分位保留
6. 再做"缩放 / 规范化建议"
7. 最后写"验证步骤" — 浮点 ↔ 定点对比、覆盖率、PIL

## 执行步骤

1. **确认工具上下文**:Fixed-Point Designer 版本、目标硬件 Word Length、舍入与饱和模式、数值范围来源
2. **数值范围数据评审**:
   - 每个信号 / 参数是否有 min / max / typical
   - 覆盖度(浮点仿真覆盖了多少飞行包线)
   - 缺口列入 `gaps`,该信号的 Q 格式标注"待覆盖确认"
3. **参数 Q 格式选型**:静态参数依据 min / max + 项目精度要求
4. **信号 Q 格式选型**:沿信号流,反馈环路用最大覆盖范围估计;特别处理积分器输出
5. **溢出风险**:对每个边界信号给出"是否会溢出 + 在何种工况下 + 缓解(增加 Word Length / 加饱和 / 重缩放)"
6. **量化误差**:估计对关键性能指标(零点、截止频率、积分增益)的影响
7. **AW 定点调整**(若涉及):
   - Kt 的 Q 格式选择(尤其是 `Kt < 1` 时 Fraction Length 要够)
   - 积分项保留位(防止小增量被量化截断)
8. **滤波器定点化**(若涉及):零点漂移、Levin 形式、SOS 分解
9. **缩放 / 规范化**:输入信号是否需要预缩放(避免 Word Length 浪费),输出是否需要恢复
10. **验证步骤**:
    - 浮点 ↔ 定点对比仿真(同输入同 baseline,信号差异容差)
    - 覆盖率重做(`clm-coverage-gap-analyzer`)
    - PIL 验证(`clm-pil-hil-replay-analyzer`)
11. **风险登记**:回归点
12. **生成工件**:按 `references/output-template.md` 填充
13. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 数值范围数据覆盖度声明
3. 逐参数 Q 格式表
4. 逐信号 Q 格式表
5. 溢出 / 饱和 / 量化风险登记
6. AW 定点调整(若涉及)
7. 滤波器定点化(若涉及)
8. 缩放与规范化建议
9. 验证步骤
10. 关键事实(Facts)、关键推断(Inferences)
11. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 浮点模型路径(必需)
   - 目标硬件(必需)
   - 数值范围数据(必需)
   - (推荐)`simulink_model_map` / `data_dictionary_map`
   - (可选)`control_law_pattern_skeleton` / `anti_windup_design`
2. 下游使用方
   - 工程师 / 评审(施工)
   - `clm-codegen-compliance-refactor`(消费风险登记 + 重构 backlog)
   - `clm-codegen-output-mapper`(定点改造后重新生成代码,核对类型映射)
   - `clm-test-harness-builder`(消费"浮点 ↔ 定点对比" 测试场景)
   - `clm-pil-hil-replay-analyzer`(消费 PIL 验证步骤)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `fixed_point_refactor_plan`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`pattern_choice`(此处 = "fixed-point")、`structural_constraints`、`refactor_steps`、`risk_register`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不直接改模型 / 不采集数值范围 / 不重做 pattern / 不重做 AW 设计 / 不审查 Coder 配置
   - 数值范围纪律(Range Data Discipline):每条 Q 格式必须有数值范围依据;无范围数据的信号不允许给出确定性 Q 格式
   - Q 格式完整性:每条给出 Word Length + Fraction Length + Signed/Unsigned + 理由
   - 风险纪律:每条溢出风险有缓解方案
   - AW 定点纪律(若涉及):Kt 量化 + 积分位保留必须显式说明
   - 验证纪律:验证步骤至少含"浮点 ↔ 定点对比仿真"
   - 工具上下文门禁:Fixed-Point Designer 版本、目标硬件、舍入/饱和模式显式记录
   - 交接门禁:可被工程师施工与下游 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供数值范围数据**:阻断 — 这是 Q 格式选型的硬前提
   - **数值范围覆盖度低**:每条受影响 Q 格式标注"待覆盖确认",建议补充覆盖飞行包线
   - **目标硬件 Word Length 未确定**:阻断;Word Length 是 Q 格式上限
   - **未提供 `data_dictionary_map`**:参数对象的现状只能从模型本身抓,置信度降低
   - **未提供 AW 设计**:若模型含积分器,提示先做 AW 设计或在浮点 AW 假设下推导(显式声明)
2. 输出降级要求
   - 降级输出必须显式标注受影响 Q 格式与置信度变化
   - 降级不等于跳步;不得给"定点改造已可投产"的结论 — 由验证步骤完成

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`
2. 交付前用 `references/checklist.md` 复核范围数据纪律、Q 格式完整性、AW 调整、验证纪律
3. 大型模型:先输出"参数 Q 格式 + 关键信号 Q 格式",再分批补完信号

## 改造纪律

1. 没有数值范围数据,就没有 Q 格式 — 不要"经验给出 Q12"
2. Word Length 不是越大越好 — 与目标硬件匹配是性能/可移植性前提
3. 反馈环路的 Q 格式需要迭代 — 不是从输入到输出走一遍就定的
4. AW Kt 量化误差是常见踩坑点 — `Kt < 1` 时 Fraction Length 不够会导致 AW 失效
5. 滤波器定点化 ≠ 直接改 Q 格式 — IIR 滤波的零点漂移要单独评估
6. 不下"定点已通过验证"结论 — 这是 `verification/` skill 的职责
