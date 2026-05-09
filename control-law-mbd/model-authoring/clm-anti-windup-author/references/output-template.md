# clm-anti-windup-author 输出模板

## 使用说明

- 目标:输出抗饱和(Anti-Windup)专项设计 — 选型、Kt 推导、连接 diff、MIMO 处置、性能预测
- 主交付工件(Primary Artifact):`anti_windup_design`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不重做 pattern 选型;不直接改模型;不给具体调参数值

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-anti-windup-author`
- `artifact_name`:`anti_windup_design`
- `tool_context`:
  - Simulink 版本与积分器 Block 类型:
  - 数值形态(浮点 / 定点):
  - 采样时间(Ts,s):
  - 内置 AW 端口可用?:
- `scope`(已有控制器路径 + 饱和约束):
- `version_or_branch`:

## 结构勘查(Structure Survey)

| 项 | 值 | 证据 |
| --- | --- | --- |
| 积分器位置 |  | `simulink_model_map > <path>` 或用户描述 |
| 积分器类型(BackwardEuler / Trapezoidal / 其他) |  |  |
| 饱和位置 |  |  |
| 饱和类型(静态 `u_min/u_max` / 动态) |  |  |
| 既有 AW 残留(若有) |  |  |
| 多通道?(单通道 / 多通道) |  |  |
| 通道间耦合估计(强 / 弱 / 未知) |  |  |

## 工件正文(Artifact Body)

### 1. 方案选型 + 折中

- 选型:`Back-calculation` / `Conditional Integration` / `Clamping` / 组合
- 选型理由:
- 与替代方案的折中:

| 候选方案 | 优点 | 缺点 | 是否选用 | 选用/不选用理由 |
| --- | --- | --- | --- | --- |
| Back-calculation |  |  |  |  |
| Conditional Integration |  |  |  |  |
| Clamping |  |  |  |  |

### 2. Kt 推导

- 推导方法:`Kt = 1/Kp` / `Tustin / Astrom 推导` / `优化拟合` / 经验值
- 推导过程(若选 Tustin / Astrom):
- 占位区间:`Kt ∈ [<lower>, <upper>]`
- 默认值占位:
- 选区间的理由:

### 3. 连接 diff(Connection Diff)

从既有结构 → 含 AW 结构的逐步变更:

| 步骤 | 操作 | 新增/修改 Block | 输入 | 输出 |
| --- | --- | --- | --- | --- |
| 1 | 增加 `Sum_track` | 新增 Sum | `u_pre`, `u` | `u_track = u_pre - u` |
| 2 | 增加 `Gain_Kt` | 新增 Gain | `u_track` | `u_track * Kt` |
| 3 | 接入积分器 Tracking 端口 | 修改积分器 | `Gain_Kt` 输出 | 反馈进积分器 |

总览:

```
[既有]: e → P + I + D → Sum → Saturation → u
[新增]:                                        ↓
                          Sum_track ← (u_pre, u)
                          Gain_Kt ← Sum_track
                          (回到 I 块的 Tracking 端口)
```

### 4. 多通道处置(若适用)

- 通道数:
- 通道间耦合估计:
- 处置:`per-channel(独立 AW)` / `coupled(耦合 AW)` / `projection(投影 AW)`
- 处置理由:
- 实现要点:

### 5. 性能预测(Performance Prediction)

| 维度 | AW 前 | AW 后(定性) | 影响因子 |
| --- | --- | --- | --- |
| 瞬态恢复时间 |  |  | Kt 大 → 更快 |
| 过冲(Overshoot) |  |  | Kt 大 → 减小;过大 → 振荡 |
| 残余 windup 风险 |  |  | Kt 太小 |
| 数值稳定性(Ts 相关) |  |  | Kt × Ts 量级 |

### 6. 风险登记(Risk Register)

| 风险 | 类别 | 等级(高/中/低) | 缓解措施 | 回归点 |
| --- | --- | --- | --- | --- |
| 与既有滤波相互作用 | 集成 |  |  |  |
| 与既有限速 / 死区 相互作用 | 集成 |  |  |  |
| 多通道误用单通道 AW | 设计 |  |  |  |
| 定点形态下 Kt 量化误差 | 数值 |  |  | 转 `clm-fixed-point-refactor` |
| Kt 过大引入振荡 | 数值 |  |  |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 模型证据:`simulink_model_map > <积分器路径>` → Block 类型
- 饱和证据:`<u_min / u_max 来源>` → 饱和约束

## 缺口与风险(Gaps & Risks)

- 缺口(例:饱和约束未提供 / 多通道耦合矩阵未提供 / 定点形态未确认):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / 评审(直接施工)
  - `clm-codegen-compliance-refactor`(关注:diff + 风险登记)
  - `clm-test-harness-builder`(关注:瞬态恢复 / 饱和触发场景)
  - `clm-fixed-point-refactor`(若涉及定点)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的参数 / Block / 风险项:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未重做 pattern / 未直接改模型 / 未给具体调参数值
- [ ] Kt 推导纪律:方法 + 占位 + 理由
- [ ] 多通道纪律:显式判定
- [ ] 性能预测纪律:至少一条定性判断
- [ ] 工具上下文显式
- [ ] 交接可用性:工程师可直接施工
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
