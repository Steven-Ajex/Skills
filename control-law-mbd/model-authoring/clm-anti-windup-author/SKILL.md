---
name: clm-anti-windup-author
description: 针对已有"含积分器的控制器"(或控制律 pattern 骨架)做抗饱和(Anti-Windup)专项设计的写操作类技能 — 不重新设计整条控制律,只输出抗饱和方案选型(Back-calculation / Conditional Integration / Clamping)、跟踪增益 Kt 推导、多通道耦合、性能预测与连接 diff。用于"控制器已存在但抗饱和缺失或不合理"场景;不重做 pattern 选型(转 `clm-control-law-pattern-author`)、不修改模型(只输出 diff)、不审查 Coder 配置、不设计测试用例。
---

# Control-Law-MBD: Anti-Windup Author

## 目标

针对一条**已有的含积分器控制律**,把"该用哪种抗饱和、Kt 取多少、多通道之间如何处理、瞬态性能影响如何"讲清楚,产出 `anti_windup_design` 工件。本 skill 比 `clm-control-law-pattern-author` 的 Anti-Windup 章节更深入、更专注于"事后补"或"专项重构"场景。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一含积分器控制器(单通道或多通道)+ 单一执行器饱和约束范围内,完成抗饱和方案选型、Kt 推导、连接 diff、性能预测,产出 `anti_windup_design` 工件
2. 工具上下文(Tool Context)
   - Simulink 版本与积分器 Block 类型(`Discrete-Time Integrator` / `Backward Euler` / `Trapezoidal` 等)
   - 数值形态(浮点 / 定点)
   - 采样时间(Ts)
   - 是否含 Anti-Windup 输入端口的内置积分器
3. 核心输入(Inputs)
   - 已有控制器路径(必需,Subsystem 或 pattern_skeleton 引用)
   - 执行器饱和约束(必需:`u_min` / `u_max` 或动态边界)
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`(用于端口/信号定位)
   - (推荐)`clm-control-law-pattern-author` 的 `control_law_pattern_skeleton`(若是新建场景)
   - (可选)性能目标(超调上限 / 恢复时间 / 过冲容忍)
   - (可选)闭环带宽与稳定裕度
4. 核心输出(Outputs)
   - 主交付工件:`anti_windup_design`
   - 方案选型 + 选型理由 + 与替代方案的折中
   - Kt 推导(方法 + 数值占位 + 理由)
   - 连接 diff(从既有结构 → 含 AW 结构)
   - 多通道耦合处置(若多通道)
   - 性能预测(瞬态恢复时间 / 残余 windup 风险 / 数值稳定性)
   - 风险登记(`risk_register`)
5. 完成判据(Definition of Done, DoD)
   - 方案选型已显式说明,与替代方案的折中已比较
   - Kt 给出方法(`Tustin 推导` / `Kp 比例式 Kt = 1/Kp` / `优化拟合` / `经验值`),且明确数值占位区间
   - 连接 diff 可被工程师按图施工(逐 Block / 逐信号)
   - 多通道时给出"独立 AW vs 耦合 AW"的处置
   - 性能预测含至少一条定性判断(恢复时间方向、过冲方向)
   - 工具上下文显式记录;数值形态(浮点/定点)显式声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留参数名 / 信号名 / Block 名(英文)原文

## 聚焦范围(只做这些)

1. 方案选型(Back-calculation / Conditional Integration / Clamping)
2. Kt(跟踪增益)推导
3. 连接 diff(从无 AW → 含 AW 的结构变更)
4. 多通道处置(独立 AW vs 耦合 AW vs MIMO 投影)
5. 性能预测(瞬态恢复 / 残余 windup / 数值稳定)
6. 与既有滤波 / 限速 / 死区 模块的相互作用

## 不负责

1. 重做 pattern 选型(PID/LQR 等) → 走 `clm-control-law-pattern-author`
2. 真实修改模型(只产出 diff)
3. 给具体调参数值 — 只给推导方法 + 占位区间
4. 审查 Coder 配置 → 走 `clm-embedded-coder-config-reviewer`
5. 设计测试用例 → 走 `clm-test-harness-builder`
6. 定点重构(若需要) → 走 `clm-fixed-point-refactor`(本 skill 在浮点假设下推导,定点形态时声明降级)

## 推荐设计顺序

1. 先看"积分器位置 + 饱和位置 + 之间的链路" — 决定方案可行性
2. 再选"方案"(三选一或组合)
3. 再推 Kt(最常见两种:`1/Kp` 或 `Tustin 等价时间常数`)
4. 再做"多通道处置" — 单通道直接,多通道需要看耦合
5. 再做"性能预测" — 瞬态、稳态、数值
6. 最后输出 diff 与风险

## 执行步骤

1. **确认工具上下文**:Simulink 版本、积分器 Block 类型、数值形态、采样时间、是否含内置 AW 端口
2. **结构勘查**:
   - 积分器位置(从 `simulink_model_map` 或 `control_law_pattern_skeleton`)
   - 饱和位置与饱和约束类型(静态 `u_min/u_max` 或动态)
   - 既有 AW 结构(若有,标注问题)
3. **方案选型**:
   - `Back-calculation`(推荐多数 PI/PID 场景):简洁、连续可调
   - `Conditional Integration`(推荐积分慢变 + 严格饱和场景):无 Kt 调参,但响应不连续
   - `Clamping`(推荐定点 / 简单场景):实现最简,瞬态性能可能差
   - 或组合(例:Back-calculation + Clamping 双保险)
4. **Kt 推导**:
   - `1/Kp` 法(简洁,适合 PI 简单结构)
   - `Tustin` / `Astrom 推导` 法(更严谨)
   - `优化拟合` 法(基于性能目标)
   - 给数值占位区间(例:`Kt ∈ [0.5/Kp, 2/Kp]`)与默认值
5. **连接 diff**:
   - 从"既有结构" → "含 AW 结构"逐步:
     - 增加 `Sum_track`:`u_track = u_pre - u`
     - 增加 `Gain_Kt`:`u_track * Kt`
     - 接入积分器 Tracking 端口
   - 给 Block 列表与连接表
6. **多通道处置**:
   - 独立 AW(`per-channel`):每通道独立结构,适合通道弱耦合
   - 耦合 AW(`coupled`):共享饱和向量与跟踪增益,适合 MIMO
   - 投影 AW(`projection`):用饱和方向投影回非饱和子空间,严谨但实现复杂
7. **性能预测**:
   - 瞬态恢复时间(定性,方向):AW 引入后是否更快
   - 过冲方向:是否减小
   - 残余 windup 风险:Kt 过大引入振荡 / 过小恢复慢
   - 数值稳定性:与 Ts 的相互作用
8. **风险登记**:
   - 与既有滤波 / 限速 / 死区 的相互作用
   - 多通道耦合误判
   - 定点形态下 Kt 量化误差
9. **生成工件**:按 `references/output-template.md` 填充
10. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 结构勘查(积分器/饱和/既有 AW)
3. 方案选型 + 折中
4. Kt 推导(方法 + 数值占位)
5. 连接 diff
6. 多通道处置(若适用)
7. 性能预测
8. 风险登记
9. 关键事实(Facts)、关键推断(Inferences)
10. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 已有控制器路径(必需)
   - 饱和约束(必需)
   - (推荐)`simulink_model_map` / `control_law_pattern_skeleton`
2. 下游使用方
   - 工程师 / 评审(直接施工)
   - `clm-codegen-compliance-refactor`(消费 diff 与风险)
   - `clm-test-harness-builder`(消费瞬态测试场景)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `anti_windup_design`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`pattern_choice`(此处 = AW 方案)、`structural_constraints`、`risk_register`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不重做 pattern 选型 / 不直接改模型 / 不给具体调参数值 / 不做定点重构
   - Kt 推导纪律(Tracking Gain Discipline):必须给方法 + 数值占位 + 理由,不能只给一个数值
   - 多通道纪律(MIMO Discipline):若多通道,必须显式判定独立/耦合/投影,不允许"按单通道处理"默认
   - 性能预测纪律:至少一条定性方向判断(瞬态/过冲/数值)
   - 工具上下文门禁:Simulink 版本、积分器类型、数值形态、Ts 显式记录
   - 交接门禁:diff 可被工程师施工
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供饱和约束**:阻断 — AW 设计的核心前提
   - **数值形态(浮点/定点)未确定**:在浮点假设下推导,显式标注"定点形态时 Kt 量化误差需另行评估"
   - **未提供 `simulink_model_map`**:结构勘查降级为"基于用户描述",置信度降低
   - **多通道但耦合矩阵未提供**:默认"假设弱耦合 → 独立 AW",显式声明假设
   - **既有结构含未知 AW 残留**:列入 `gaps`,提示先做结构勘查
2. 输出降级要求
   - 降级输出必须显式标注受影响段
   - 降级不等于跳步;不得越过本技能职责给出"AW 已生效"的结论 — 由测试与回放验证

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`
2. 交付前用 `references/checklist.md` 复核 Kt 纪律、MIMO 纪律、降级
3. MIMO 场景重点检查"独立/耦合/投影"决策链路

## 设计纪律

1. AW 选型不是品味问题 — 必须基于"积分器类型 + 饱和形态 + 数值形态"做证据化推导
2. Kt 不要只给一个数 — 给方法 + 占位区间 + 默认值
3. 多通道误用单通道 AW 是常见陷阱 — 必须显式判定耦合
4. AW 与"既有滤波/死区/限速"会相互作用 — 风险登记必须涵盖
5. 不在本 skill 内做"运行仿真验证 AW 工作"的结论 — 这是测试与回放 skill 的职责
