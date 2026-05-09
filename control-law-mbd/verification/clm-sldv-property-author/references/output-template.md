# clm-sldv-property-author 输出模板

## 使用说明

- 目标:输出 SLDV 形式化属性集 + Assumption + 证明策略 + Test Objective 配套
- 主交付工件(Primary Artifact):`sldv_property_set`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不替代需求工程师 / 不运行 SLDV / 不下"已证明"结论

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-sldv-property-author`
- `artifact_name`:`sldv_property_set`
- `tool_context`:
  - SLDV 版本:
  - 证明引擎:
  - Verification Subsystem 模式:
  - Property Proving + Test Generation 联用:
  - 许可证可用性:
- `scope`(被验对象 + 需求/约束清单来源):
- `version_or_branch`:

## 需求/约束筛选结论(Formalization Eligibility)

- 总条目数:
- 适合形式化(局部/可观测/断言式):
- 不适合(模糊语 / 全局性能 / 主观判断 等):
- 不适合条目转交建议:

## 工件正文(Artifact Body)

### 1. 属性表(Property Table)

| 属性 ID | 自然语言描述 | 形式化表达 | 作用域 | 期望结果 | 关联需求 / 故障 ID |
| --- | --- | --- | --- | --- | --- |
| P-SAF-01 | 当 IMU 故障时,系统在 100 ms 内进入安全模式 | `G ((imu_fault==true) -> F[0,100ms] (mode_status==SAFE))` | `Controller/SafetyMonitor` | proven | REQ-SAF-001 / F-IMU-01 |
| P-CTL-01 | 控制量始终落在 [u_min, u_max] | `G (u_min <= u_cmd <= u_max)` | `Controller/AttitudeLoop` | proven |  |
| P-MODE-01 | 不存在从 `Cruise` 直接到 `Hover` 的非法跳变 | `G !(state==Cruise && next_state==Hover)` | `ModeManager` | proven | REQ-MODE-005 |
| P-AW-01 | 饱和退出后 800 ms 内姿态误差恢复 | `G (saturation_exit -> F[0,800ms] (\|attitude_err\| < 1deg))` | `Controller/AttitudeLoop/AW` | falsifiable_expected | REQ-ATT-009(若反驳 → 测试反例) |

期望结果枚举:`proven` / `falsifiable_expected`(反例驱动测试) / `undecided_acceptable`(允许 SLDV 给 undecided)

### 2. Assumption 表(Assumption Table)

| Assumption ID | 描述 | 形式化表达 | 限制范围 | 与设计意图一致? |
| --- | --- | --- | --- | --- |
| A-IN-01 | 输入 `attitude_ref` 范围 | `G (-pi <= attitude_ref <= pi)` | 输入空间 | 是 |
| A-IN-02 | 模式信号互斥 | `G !(mode==HOVER && mode==CRUISE)` | 输入空间 | 是 |
| A-CFG-01 | 参数 `Kp_att` 范围 | `Kp_att in [0, 100]` | 参数空间 | 是 |

### 3. 证明策略(Proof Strategy)

| 属性 ID | 策略(Inductive / Bounded) | 步数 N(若 Bounded) | 选型理由 |
| --- | --- | --- | --- |
| P-SAF-01 | Bounded | 100 | 100 ms / Ts=10ms = 10 步 + 安全余量 |
| P-CTL-01 | Inductive | — | 输出范围属性可归纳证明 |
| P-MODE-01 | Inductive | — | Stateflow 转移可归纳证明 |
| P-AW-01 | Bounded | 80 | 800 ms / Ts=10ms = 80 步 |

多采样系统的最小公倍数采样选取:

### 4. 期望结果分类汇总

| 分类 | 数量 | 说明 |
| --- | --- | --- |
| `proven`(可证明) |  |  |
| `falsifiable_expected`(反例驱动) |  | 用作 SLDV 自动生成测试用例 |
| `undecided_acceptable`(允许 undecided) |  | 状态空间过大 / 时序复杂 |

### 5. Test Objective 配套(若涉及)

| Test Objective ID | 关联属性 ID(falsifiable_expected) | 期望反例形式 | 反例 → 测试用例 ID |
| --- | --- | --- | --- |
| TO-AW-01 | P-AW-01 | 找到饱和退出后 800 ms 内未恢复的输入轨迹 | 自动生成 → 转交 `clm-test-harness-builder` |

### 6. Verification Subsystem / Property Block 接入 Diff

```
ModelRoot/
├─ DUT/                       (被验对象)
└─ VerificationSubsystem/     (新增,独立模式)
   ├─ Properties/             (Proof Block 集合)
   │  ├─ P-SAF-01: Implies + Within
   │  ├─ P-CTL-01: Within
   │  └─ ...
   ├─ Assumptions/            (Assumption Block 集合)
   │  ├─ A-IN-01: Within
   │  ├─ A-IN-02: Implies
   │  └─ ...
   └─ TestObjectives/         (Test Objective Block,用于反例生成)
       └─ TO-AW-01
```

Block 列表:

| Block 类型 | 数量 | 备注 |
| --- | --- | --- |
| `Proof Objective` |  | 用于属性证明 |
| `Proof Assumption` |  | 用于限制输入空间 |
| `Test Objective` |  | 用于反例生成 |
| `Verification Subsystem` | 1 | 容器 |

### 7. 与其他 verification skill 的边界声明

- 与 `test_harness_plan`:常规功能用例由 harness builder 设计,本 skill 只覆盖可形式化的需求
- 与 `fault_injection_test_plan`:故障注入由专门 skill 设计,本 skill 的 P-SAF-* 系列与故障检测属性互补
- 与 `coverage_gap_report`:SLDV 运行后产生的覆盖将进入覆盖率分析,本 skill 不下覆盖结论

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 需求证据:`requirement_trace_map > REQ-SAF-001` → 形式化派生 P-SAF-01
- 故障证据:`fault_injection_test_plan > F-IMU-01` → P-SAF-01 关联
- 模型证据:`simulink_model_map > Controller/SafetyMonitor` → 作用域定位

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / 需求过于模糊 / 状态空间过大):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / DV 团队(运行 SLDV)
  - `clm-test-harness-builder`(消费 Test Objective 反例 → 生成测试用例)
  - `clm-coverage-gap-analyzer`(SLDV 运行后的覆盖)
  - `clm-codegen-compliance-refactor`(反驳的属性 → 模型重构)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的属性 ID / Assumption / 证明策略:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未替代需求 / 未运行 SLDV / 未修改模型 / 未下"已证明"结论
- [ ] 形式化纪律:每条属性 = 自然语言 + 形式化 + 作用域 + 期望
- [ ] Assumption 纪律:显式 + 限制范围
- [ ] 证明边界纪律:策略 + N 选型理由
- [ ] 期望结果分类:三类齐
- [ ] 边界声明:与其他 verification skill 显式
- [ ] 工具上下文显式

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
