# clm-control-law-pattern-author 输出模板

## 使用说明

- 目标:输出标准控制律 pattern 的 Simulink 建模骨架,供工程师施工
- 主交付工件(Primary Artifact):`control_law_pattern_skeleton`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 只产出骨架,不直接修改模型;不给具体参数数值

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-control-law-pattern-author`
- `artifact_name`:`control_law_pattern_skeleton`
- `tool_context`:
  - Simulink 版本与目标库:
  - 目标采样时间(s):
  - 多速率边界(若有):
  - 数值形态(浮点 / 定点 + Q 格式):
  - 代码生成约束:
  - 项目级建模规范来源:
- `scope`(目标子系统路径或"新建"标记):
- `version_or_branch`:

## Pattern 选型说明

- `pattern_choice`:`pid` / `lqr` / `gain-scheduling` / `anti-windup` / `saturation` / `lead-lag` / `state-observer` / 其他
- 选型理由:
- 与替代方案的折中(为何不选 X):
- 关键依赖(需求 / 性能基线 / 既有结构):

## 端口契约(Port Contract)

| 端口 | 方向 | 信号名 | 类型 | 单位 | 备注 |
| --- | --- | --- | --- | --- | --- |
| `r` | In | `ref` | double | rad |  |
| `y` | In | `feedback` | double | rad |  |
| `u` | Out | `ctrl_cmd` | double | rad |  |

## 主拓扑(Main Topology)

```
Subsystem/
├─ ErrCalc:        r - y → e
├─ P:              Kp * e
├─ I:              Integrator(Ki * e), with Anti-Windup back-calc
├─ D:              Kd * d/dt(e), with low-pass filter (tau_filter)
├─ Sum:            P + I + D
├─ Saturation:     [u_min, u_max]
└─ Out u
```

Block 列表与连接(Block-by-Block):

| Block | 类型 | 关键参数 | 输入 | 输出 |
| --- | --- | --- | --- | --- |
| `ErrCalc` | Sum | `+ -` | `r`, `y` | `e` |
| `P` | Gain | `Kp` | `e` | `u_p` |
| `I` | Discrete-Time Integrator | `Ki * Ts`, Anti-Windup port | `e`, `u_track - u` | `u_i` |
| `D` | Filtered Derivative | `Kd`, `tau_filter` | `e` | `u_d` |
| `Sum_PID` | Sum | `+ + +` | `u_p`, `u_i`, `u_d` | `u_pre` |
| `Saturation` | Saturation Dynamic | `u_min`, `u_max` | `u_pre` | `u` |
| `BackCalc` | Sum | `- +` | `u_pre`, `u` | `u_track` |

## 参数对象声明(`Simulink.Parameter`)

| 参数名 | 类型 | 默认值占位 | Min / Max 占位 | Storage Class 建议 | 备注 |
| --- | --- | --- | --- | --- | --- |
| `Kp` | double | 1.0 | 0 / 100 | `Calibration`(可在线标定) |  |
| `Ki` | double | 0.1 | 0 / 50 | `Calibration` |  |
| `Kd` | double | 0.0 | 0 / 50 | `Calibration` |  |
| `tau_filter` | double | 0.05 | 0.001 / 1.0 | `Calibration` |  |
| `u_min` | double | -1.0 | -100 / 0 | `Calibration` |  |
| `u_max` | double | 1.0 | 0 / 100 | `Calibration` |  |
| `Kt_back` | double | 1.0 | 0 / 10 | `Calibration` | Anti-Windup 跟踪增益 |

## 采样时间与原子化(Sample Time & Atomicity)

- SampleTime:`Ts = 0.01 s`(显式,不继承)
- 原子化:`Atomic Subsystem`(决定代码生成函数边界)
- Function Packaging:`Reusable function` / `Nonreusable function`(取决于是否实例化多次)

## 抗饱和实现(Anti-Windup,若含积分器)

- 方案:`Back-calculation` / `Conditional Integration` / `Clamping` — 选择:`Back-calculation`
- 连接细节:
  - `u_track = (u_pre - u) * Kt_back`
  - 接入 `I` 块的 Tracking Input 端口
- 选择理由:数值稳定性 vs 实现复杂度

## 附属结构(Auxiliary,若适用)

- D 项滤波(低通):`tau_filter`
- 死区(Dead Zone,若需要):
- 速率限制(Rate Limiter,若需要):
- 限幅(Saturation):见主拓扑

## 集成步骤(Integration Steps)

1. 在 `<目标子系统路径或"新建"位置>` 创建 Atomic Subsystem,SampleTime 设为 `Ts`
2. 按"主拓扑"添加 Block 与连接
3. 在数据字典(`<dict_path.sldd>`)创建上述参数对象,采用建议的 Storage Class
4. 把参数对象绑定到 Block 参数(在 Block 的"Parameters"中输入参数名)
5. 配置 Atomicity 与 Function Packaging(用于代码生成)
6. 接入上层模型,连接 `r` / `y` / `u` 三端口
7. 运行 Model Advisor(High-Integrity 规范)做合规检查
8. 用 `clm-test-harness-builder` 设计测试 harness 与用例

## 风险登记(Risk Register)

| 风险 | 类别 | 等级(高/中/低) | 影响 | 缓解措施 | 回归点 |
| --- | --- | --- | --- | --- | --- |
| 数值稳定性 — Ki 过大导致积分发散 | 数值 | 中 |  | Min/Max 限定 + Anti-Windup |  |
| 与既有结构冲突 — 上层 Saturation 已存在 | 集成 | 中 |  | 与既有结构合并或替换 |  |
| 多速率边界 — 上层 100 Hz、本子系统 100 Hz 一致 | 采样 | 低 |  | 显式 SampleTime |  |
| 抗饱和死区 — Back-calculation 增益 Kt 过大引入振荡 | 数值 | 中 |  | Kt 留容差,文档化 |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 上游模型路径:`simulink_model_map > <Subsystem>` → 端口/采样时间约束
- 字典回引:`data_dictionary_map > Parameter > <name>` → 复用候选
- 需求回引:`requirement_trace_map > REQ-XX` → 控制目标

## 缺口与风险(Gaps & Risks)

- 缺口(例:数值形态未确认 / 多速率边界未确认 / 字典未提供):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / 评审(直接施工)
  - `clm-codegen-compliance-refactor`(关注:风险登记、与既有结构冲突)
  - `clm-test-harness-builder`(关注:端口契约 + 抗饱和触发场景)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的 Block / 参数 / 风险项:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未直接改模型 / 未给具体数值 / 未给调参建议
- [ ] 完整性:七项齐全(选型 + 端口 + 拓扑 + 参数 + 采样 + 集成 + 风险)
- [ ] 抗饱和纪律:含积分器时显式给出方案
- [ ] 工具上下文显式:版本/采样/数值形态/约束已记录
- [ ] 参数对象纪律:类型 + 占位 + Storage Class 建议,无具体数值
- [ ] 集成步骤可施工
- [ ] 交接可用性:工程师与下游 skill 可直接消费
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
