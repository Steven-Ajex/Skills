# clm-gain-scheduling-author 输出模板

## 使用说明

- 目标:输出增益调度建模骨架 — 在已有基础 pattern 上加调度结构
- 主交付工件(Primary Artifact):`gain_scheduling_skeleton`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不重做基础 pattern;不修改模型;不给具体调度表数值

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-gain-scheduling-author`
- `artifact_name`:`gain_scheduling_skeleton`
- `tool_context`:
  - Simulink 版本与 Lookup Table 类型(`Lookup Table` / `Lookup Table (n-D)` / `Prelookup + Interpolation` / `Direct`):
  - 数值形态(浮点 / 定点 + Q 格式):
  - 采样时间(s):
  - 调度更新率(可与控制律不同):
  - 是否使用 `Simulink.LookupTable` 对象:
- `scope`(基础 pattern 路径 + 调度范围):
- `version_or_branch`:

## 基础 Pattern 引用

- 上游工件 / Subsystem 路径:
- 增益清单(将被调度化):

| 增益名 | 当前类型 | 当前值占位 | 调度后查表维度 |
| --- | --- | --- | --- |
| `Kp` | Scalar | 1.0 |  |
| `Ki` | Scalar | 0.1 |  |
| `Kd` | Scalar | 0.0 |  |
| `K_state(LQR)` | Matrix |  |  |

## 工件正文(Artifact Body)

### 1. 调度变量声明(Scheduling Variables)

| 变量名 | 信号源 | 类型 | 范围 | 单位 | 选型理由 | 噪声前置滤波 |
| --- | --- | --- | --- | --- | --- | --- |
| `velocity_mps` |  | double | [0, 80] | m/s | 与气动包线强相关 | 一阶低通 1 Hz |
| `altitude_m` |  | double | [0, 5000] | m | 高度对气动密度影响 | 高度滤波 0.5 Hz |
| `mass_kg` |  | double | [50, 80] | kg | 起飞 vs 着陆质量差 | 否(慢变) |

### 2. 工况网格(Operating Grid)

| 调度变量 | 网格点 | 单位 | 边界点已含? | 关键工况点 |
| --- | --- | --- | --- | --- |
| `velocity_mps` | [0, 5, 15, 30, 50, 80] | m/s | 是 | 5 m/s(转换) / 30 m/s(巡航) |
| `altitude_m` | [0, 500, 1500, 3000, 5000] | m | 是 |  |

总网格规模:6 × 5 = 30 个调度点(若 2-D);若加 mass_kg → 30 × 3 = 90(N-D 数据量爆炸警告)

### 3. 调度表结构(Lookup Structure)

- 维度数:`1-D` / `2-D` / `N-D`
- 维度顺序:
- 表对象选型:
  - `Simulink.LookupTable` 对象(推荐,可标定)
  - 或 inline LookupTable Block(简洁但不可标定)

| 增益 | 表名 | 维度 | 网格大小 | 数据占位(供工程师填) |
| --- | --- | --- | --- | --- |
| `Kp` | `LUT_Kp` | 2-D | 6 × 5 | 待飞行测试/系统辨识填入 |
| `Ki` | `LUT_Ki` | 2-D | 6 × 5 | 同上 |
| `Kd` | `LUT_Kd` | 2-D | 6 × 5 | 同上 |

### 4. 插值方式 + 边界外推策略

- 插值方式:`Linear` / `Flat (定点推荐)` / `Cubic Spline` / `Nearest Neighbor`
- 边界外推:`Clip` / `Linear Extrap` / `Hold`
- 选型理由:

### 5. 调度切换平滑机制(Bumpless Transfer)

- 选型:`一阶低通滤波(切换后增益)` / `Slew Rate Limit(增益变化率)` / `渐变切换(混合两组增益)`
- 滤波时间常数 / 渐变时长:
- 与积分项的相互作用(若涉及 PID):
  - 切换前后积分项是否需要重置 / 平移
  - 实现方式:

### 6. 多通道处置(Multi-Channel Handling)

- 通道数:
- 选型:`per-channel(独立查表)` / `shared scheduling vars(共享变量)` / `MIMO 调度矩阵`
- 选型理由:

### 7. 接入 Diff(Connection Diff)

从基础 pattern → 调度版的 Block 级变更:

| 步骤 | 操作 | 修改/新增 Block | 输入 | 输出 |
| --- | --- | --- | --- | --- |
| 1 | 增加 `LUT_Kp` Lookup Table 2-D | 新增 | `velocity_mps`, `altitude_m` | `Kp_scheduled` |
| 2 | 修改 `P` 块的 Gain 来源 | 修改 | `Kp_scheduled` | `u_p` |
| 3 | 增加 bumpless 滤波器 | 新增 | `Kp_scheduled` | `Kp_filtered` |
| 4 | (类似步骤 1-3 应用于 `Ki`、`Kd`) |  |  |  |

### 8. 参数对象声明(`Simulink.LookupTable` 模板)

| 对象名 | 类型 | 维度 | 数据占位 | Breakpoints | Storage Class 建议 |
| --- | --- | --- | --- | --- | --- |
| `LUT_Kp` | Simulink.LookupTable | 2-D | `nan(6,5)` (待填) | `velocity_grid`, `altitude_grid` | `Calibration` |
| `velocity_grid` | Simulink.Breakpoint | 1-D | `[0,5,15,30,50,80]` | — | `Calibration` |
| `altitude_grid` | Simulink.Breakpoint | 1-D | `[0,500,1500,3000,5000]` | — | `Calibration` |

### 9. 风险登记(Risk Register)

| 风险 | 类别 | 等级(高/中/低) | 缓解措施 | 回归点 |
| --- | --- | --- | --- | --- |
| Bumpless transfer 失效引起增益突变 | 数值/动态 | 中 | 一阶低通 / 渐变切换 + AW 联动 | 瞬态用例 |
| 边界外推导致工况外控制不稳 | 安全 | 高 | Clip + 显式饱和 | 边界用例 |
| 调度变量噪声引起增益抖动 | 数值 | 中 | 前置滤波 + 滞回 | 噪声扫描用例 |
| 定点插值精度损失 | 数值 | 中 | 转 `clm-fixed-point-refactor` 评估 |  |
| 网格点之间增益变化率过大导致系统不稳 | 设计 | 高 | 加密网格 / 平滑增益剖面 | 调度点扫描 |
| N-D 表数据量爆炸(若 > 3 维) | 实现 | 中 | 减维 / 分段 |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 基础 pattern 证据:`control_law_pattern_skeleton > <增益清单>` 或模型路径
- 调度变量证据:`simulink_model_map > <信号路径>` → 信号源
- 字典证据(若有):`data_dictionary_map > <参数对象>` → 现状

## 缺口与风险(Gaps & Risks)

- 缺口(例:基础 pattern 未提供 / 调度变量缺失 / 工况网格缺失):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / 评审(直接施工)
  - `clm-codegen-compliance-refactor`(关注:风险登记 + N-D 表实现)
  - `clm-test-harness-builder`(关注:工况网格作为测试场景)
  - `clm-fixed-point-refactor`(若涉及定点)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的调度变量 / 网格点 / 风险项:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未重做基础 pattern / 未直接改模型 / 未给具体数值
- [ ] 调度变量纪律:信号 + 类型 + 范围 + 理由
- [ ] 工况网格纪律:边界 + 关键点 + 密度理由
- [ ] bumpless 纪律:显式机制
- [ ] 多通道纪律:独立 / 共享 / MIMO 显式
- [ ] 工具上下文显式
- [ ] 接入 diff 可施工
- [ ] 风险登记完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
