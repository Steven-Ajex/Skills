# clm-fault-injection-test-author 输出模板

## 使用说明

- 目标:输出故障注入测试规划 — 故障矩阵、安全等级覆盖、需求映射
- 主交付工件(Primary Artifact):`fault_injection_test_plan`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 消费 FMEA/HARA/FTA 产物,不替代它们;不设计常规功能用例

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-fault-injection-test-author`
- `artifact_name`:`fault_injection_test_plan`
- `tool_context`:
  - Simulink Test 版本:
  - 故障注入框架:
  - 是否启用代码侧故障注入:
  - 安全等级标准(ASIL / DAL / SIL / 项目):
  - 许可证可用性:
- `scope`(被测对象 + 故障清单来源):
- `version_or_branch`:

## 故障清单对齐结论(Fault List Alignment)

- 来源:`<FMEA / HARA / FTA / 项目级故障表>`
- 总故障数:
- 按安全等级分布:`ASIL D=N` / `ASIL C=N` / `ASIL B=N` / `ASIL A=N`(或 DAL/SIL 对应)
- 字段完整性:`完整 / 部分(详见 gaps)`

## 工件正文(Artifact Body)

### 1. 故障矩阵(Fault Matrix,主表)

| 故障 ID | 安全等级 | 描述 | 注入点 | 注入方式 | 触发场景 | 期望降级行为 | 通过判据 | 复位策略 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-IMU-01 | ASIL D | IMU 角速率信号 Stuck-At | `imu_gyro_rad_s`(信号级) | Stuck-At(零值) | 巡航稳态 + 高速转弯 | `mode_status → SAFE`,执行器输出限幅 | `mode_status == SAFE` 在 `t < 100 ms`;输出 `\|u\| < u_max_safe` | 故障清除 + `mode_request==NORMAL` 后回到 `NORMAL`,`t < 500 ms` |
| F-ACT-01 | ASIL C | 执行器响应延迟漂移 | `actuator_cmd`(信号级) | Drift(线性增长) | 转换瞬态 | 增大 PID 跟踪误差容忍 | `\|attitude_err\| < 2 deg` 在 `t ∈ [1, 5] s` | 漂移消失后 `t < 1 s` 误差恢复 < 0.5 deg |
| F-MODE-01 | ASIL D | 模式跳变错误 | `mode_request`(模式级) | 模式跳变(`HOVER → CRUISE` 在不允许时) | 悬停时 `vel < 5 m/s` | 拒绝跳变,保持 `HOVER` | 转移日志 `transition_rejected==true`,模式不变 | 输入清除后下次合法跳变正常 |

注入方式枚举:

- `Stuck-At`:信号固定为某值(常用零值 / 最大值 / 中位)
- `Drift`:线性 / 指数 / 阶跃漂移
- `Spike`:瞬时高幅值
- `Inversion`:符号取反
- `Signal Loss`:信号丢失(NaN / 超时)
- `Bit-Flip`:特定位翻转(代码侧)
- `模式跳变`:Stateflow 强制跳到非法状态

### 2. 故障 ↔ 需求映射(Fault to Requirement)

| 故障 ID | 关联需求 ID | 覆盖类型(直接 / 间接) | 备注 |
| --- | --- | --- | --- |
| F-IMU-01 | REQ-SAF-001 | 直接 | IMU 故障检测要求 |

未覆盖的故障(列入 `gaps`):

### 3. 安全等级覆盖率(Safety Level Coverage)

| 安全等级 | 故障总数 | 已覆盖 | 覆盖率 % | 关键未覆盖 |
| --- | --- | --- | --- | --- |
| ASIL D / DAL A / SIL 4 |  |  | **必须 100%** |  |
| ASIL C / DAL B / SIL 3 |  |  |  |  |
| ASIL B / DAL C / SIL 2 |  |  |  |  |
| ASIL A / DAL D / SIL 1 |  |  |  |  |
| QM / DAL E / 无安全要求 |  |  |  |  |

### 4. 与 `test_harness_plan` 边界声明

- 故障专项 vs 常规功能用例的分工:
- 重复部分(若有)及说明:
- 合并 harness 时的注入点切换策略:

### 5. 复位策略汇总(Reset Strategy)

| 故障类型 | 单次故障复位 | 持续故障处置 | 残留状态清理 |
| --- | --- | --- | --- |
| 信号级 |  |  |  |
| 参数级 |  |  |  |
| 模式级 |  |  |  |
| 接口级 |  |  |  |

### 6. 工具/代码侧实施提示

- 注入框架:
- 注入实施方式(Test Sequence / S-Function / 代码补丁 / Fault Analyzer):
- 代码侧注入路径(若启用,参考 `codegen_output_map`):

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 故障来源:`FMEA-2026Q1.xlsx > F-IMU-01` → 描述 + 安全等级
- 模型证据:`simulink_model_map > <信号路径>` → 注入点定位
- 状态机证据:`stateflow_semantics > <状态/转移>` → 模式跳变故障
- 代码证据:`codegen_output_map > <文件:行号>` → 代码侧注入

## 缺口与风险(Gaps & Risks)

- 缺口(例:故障清单字段缺失 / 高等级故障未覆盖 / 注入框架不可用):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-test-harness-builder`(合并故障矩阵到统一 harness 设计)
  - `clm-coverage-gap-analyzer`(消费安全等级覆盖率作为额外覆盖维度)
  - `clm-pil-hil-replay-analyzer`(消费故障注入下的通过判据 + 复位策略)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的故障 ID / 安全等级 / 注入点:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未替代 FMEA/HARA/FTA / 未设计常规用例 / 未修改模型 / 未运行测试
- [ ] 故障矩阵完整性:六字段齐全
- [ ] 通过判据可机器判定
- [ ] 复位策略显式
- [ ] 安全等级覆盖纪律:高等级 100%
- [ ] 工具上下文显式
- [ ] 与 `test_harness_plan` 边界声明

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
