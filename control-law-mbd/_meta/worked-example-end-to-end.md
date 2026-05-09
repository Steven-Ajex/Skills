# 端到端 Worked Example:VTOL 姿态环 Anti-Windup 改造

本文档用一个具体场景演示 `control-law-mbd/` 库 16 个 skill 的串联、阶段门禁、跨库工件交接以及反馈环路。**它不是教程,而是契约的具体化** — 用来验证(并向使用者展示)各 skill 的输入/输出与边界在真实任务下是否能闭合。

## 1. 场景背景

某 VTOL 项目在悬停 → 巡航转换段反复出现姿态超调,实飞日志显示:执行器在转换瞬态饱和 4-6 s,姿态环积分项继续累积,饱和退出后控制量长时间不回中,导致"反向超调"。

任务目标:

1. 评估现有控制律(MBD 浮点模型 + Embedded Coder 生成)是否含合规的 Anti-Windup
2. 设计 AW 改造(若缺失或不合理)
3. 评估改造对生成代码、覆盖率、嵌入式接口的影响
4. 用 FMT 实飞日志作 PIL 回放,对照基线
5. 与 FMT 库形成闭环:接口契约 + 实飞验证

工具上下文:

- **本库侧**:Simulink R2023b、Embedded Coder R2023b、Fixed-Point Designer R2023b、Simulink Test R2023b、目标硬件 ARM Cortex-M7、`Word Length = 32`(浮点)
- **FMT 侧**:`firmware_context = { variant: vtol, mlog_version: v3, signal_catalog: ./catalog.json }`

## 2. 端到端流水线总览

```
Stage 1                Stage 2                Stage 3              Stage 4              跨库
Model Reading       Model Authoring        Codegen Bridge       Verification         FMT
─────────────       ───────────────        ──────────────       ────────────         ────
simulink-           anti-windup-           embedded-coder-      test-harness-        flight-log-replay-
  model-reader       author                 config-reviewer      builder              bridge ◄──
stateflow-          codegen-               codegen-output-      coverage-gap-          (mlog_decode_summary)
  semantics-reader   compliance-            mapper               analyzer
data-dictionary-     refactor              storage-class-       pil-hil-replay-
  reader            (fixed-point-           governor             analyzer ──►
requirement-         refactor 备选)                              (control_perf_findings)
  trace-reader

                                Workflow
                       clm-control-law-mbd-pipeline
                       (顺序 / 门禁 / 汇总 / 跨库 handoff)
```

## 3. 编排技能驱动的逐阶段执行

`clm-control-law-mbd-pipeline` 接到任务后,先解析任务 → 裁剪阶段 → 串行执行。下面按阶段展示:**输入工件 / 调用的 skill / 产出工件 / 关键门禁结果**。

### Stage 1:Model Reading(模型 / Stateflow / 字典 / 需求)

**输入**:`model.slx`、`design.sldd`、`requirements.slreqx`、变体 = `vtol`

**调用顺序与产出**:

| 顺序 | Skill | 产出工件(示例字段) |
| --- | --- | --- |
| 1.1 | `clm-simulink-model-reader` | `simulink_model_map`:子系统树含 `Controller/AttitudeLoop`(Atomic);多速率边界 `400 Hz / 100 Hz`;含 Stateflow `ModeManager` |
| 1.2 | `clm-stateflow-semantics-reader` | `stateflow_semantics`:Decomposition=Exclusive;状态 `Hover → Transition → Cruise`,转移 T2 在 `mode_request==CRUISE` 下 |
| 1.3 | `clm-data-dictionary-reader` | `data_dictionary_map`:`Kp_att`/`Ki_att`/`Kd_att` 在 Top.sldd,`Storage Class = ExportedGlobal`;**风险**:`Storage Class = Auto` 的 4 个对象,需治理 |
| 1.4 | `clm-requirement-trace-reader` | `requirement_trace_map`:`REQ-ATT-005 (Anti-Windup 必备)` 已链接到 `Controller/AttitudeLoop`;**orphan**:`REQ-ATT-009 (转换瞬态恢复时间 < 800 ms)` 未链任何对象 |

**Stage 1 退出门禁**:

- ✅ 工具上下文齐全(Simulink/Stateflow R2023b)
- ✅ `simulink_model_map` 与 `data_dictionary_map` 范围一致(同一 `model.slx`)
- ⚠️ 警告(Non-Blocking):`REQ-ATT-009` orphan,提示 Stage 4 必须额外构造对应用例

进入 Stage 2。

### Stage 2:Model Authoring(AW 设计 + 重构方案)

**关键决策点**:从 Stage 1 看,`Controller/AttitudeLoop` 含积分器但无 Anti-Windup。优先用专精 `clm-anti-windup-author`(而非整个 `pattern-author` 重做)。

**输入**:`simulink_model_map`(端口约束)、`u_min/u_max`(从字典)、性能目标(REQ-ATT-009:恢复时间 < 800 ms)

**调用顺序与产出**:

| 顺序 | Skill | 产出工件(关键字段) |
| --- | --- | --- |
| 2.1 | `clm-anti-windup-author` | `anti_windup_design`:方案=Back-calculation;Kt 推导=`1/Kp` 法,占位区间 `Kt ∈ [0.5/Kp_att, 2/Kp_att]`;多通道处置=`per-channel` 独立 AW(roll/pitch/yaw 通道弱耦合);连接 diff:增 `Sum_track` + `Gain_Kt` + 接积分器 Tracking 端口;**风险**:与既有 `RateLimiter` 相互作用待评估 |
| 2.2 | `clm-codegen-compliance-refactor` | `compliance_refactor_diff`:聚合 Stage 1 风险(`Storage Class = Auto` 的 4 个对象)+ AW 改造步骤;决策:全部 `refactor`;backlog 优先级:AW 接入(高)→ Storage Class 调整(中)→ orphan 需求补 link(中) |

**注**:浮点已满足目标硬件,本场景不调用 `clm-fixed-point-refactor`(在工件中标 `skipped:目标硬件含 FPU`)。

**Stage 2 退出门禁**:

- ✅ AW 设计的 `risk_register` 已含 `RateLimiter 相互作用`,Stage 4 必须覆盖该工况
- ✅ Refactor backlog 排序完成
- ⚠️ 警告:工程师须按 `compliance_refactor_diff > refactor_steps` 手工施工;本编排技能**不下"已可投产"结论**,仅交接方案

进入 Stage 3。

### Stage 3:Codegen Bridge(配置审查 / 代码映射 / 存储类治理)

**前置假设**:工程师已按 Stage 2 方案改完模型,并重新生成代码(`./generated/`)。

**调用顺序与产出**:

| 顺序 | Skill | 产出工件(关键字段) |
| --- | --- | --- |
| 3.1 | `clm-embedded-coder-config-reviewer` | `coder_config_review`:Code Interface = `Reusable function`;Storage Class:`ExportedGlobal` for `Kp_att`,符合期望;**警告**:`MISRA Modeling` 未启用,但项目尚未要求 |
| 3.2 | `clm-codegen-output-mapper` | `codegen_output_map`:`Controller/AttitudeLoop` ↔ `controller.c:128 controller_step()`;`Kp_att` ↔ `controller_data.c:42 Kp_att`;**`bridge_layer_contract`**:Step 入口签名 + extern 命名前缀 = 空(默认),供 FMT 端核对 |
| 3.3 | `clm-storage-class-governor` | `storage_class_governance`:逐对象决策表;命名一致性 OK;桥接核对(下文跨库段)发现差异 |

**Stage 3 退出门禁**:

- ✅ 模型时间戳与代码时间戳一致(Stage 3.2 校验)
- ✅ `bridge_layer_contract` 字段齐全,可供 FMT 接力
- ⚠️ 警告:命名前缀差异(下文跨库段处置)

**首个跨库 handoff(模型 → FMT)** 触发:

```
codegen_output_map.bridge_layer_contract  ─►  fmt-mbd-interface-reader 期望
{
  step_entry: "controller_step(Inputs_t*, Outputs_t*)",
  globals_prefix: "",   ◄── 与 FMT 接口层期望 "clm_" 不一致
  type_header: "rtwtypes.h"
}
```

`storage_class_governance` 桥接核对段:**FMT 端接口层期望命名前缀 `clm_`,本治理决策为空**;差异显式列入 backlog,**编排技能不擅自调和** — 由工程师与 FMT 维护方决定:在治理决策中加前缀,或在 FMT 接口层 wrapper 中适配。

进入 Stage 4。

### Stage 4:Verification(测试 harness / 覆盖率 / PIL 回放 + 反向跨库桥)

#### 4.1 调用 `clm-test-harness-builder`

**输入**:`simulink_model_map`、`stateflow_semantics`、`requirement_trace_map`、`anti_windup_design`、`codegen_output_map`(用于 SIL)

**产出**:`test_harness_plan` 的关键用例:

| 用例 ID | 分组 | 通过判据(可机器判定) |
| --- | --- | --- |
| TC-EQ-01 | 等价类 | `\|attitude_err\| < 0.5 deg`,`t ∈ [1.0, 5.0] s` |
| TC-BD-01 | 边界 | 大角度阶跃下不溢出执行器,settling time `< 200 ms` |
| TC-SF-01 | 状态切换 | `Hover → Transition` 转移在 `mode_request==CRUISE` 后 `< 100 ms` 完成 |
| TC-AW-01 | AW 瞬态(派生自 `anti_windup_design.risk_register`) | 持续饱和 4 s 后退出,姿态恢复至 `\|err\| < 1 deg` 的时间 `< 800 ms`(对接 REQ-ATT-009) |
| TC-AW-02 | AW × RateLimiter 相互作用 | RateLimiter 触发 + 饱和共存时无死锁 |
| TC-FI-01 | 故障注入 | (按需求层补) |

**重要**:`TC-AW-01` 解决了 Stage 1 标记的 `REQ-ATT-009` orphan(把它链接到新建的 AW 用例)— 反馈环路第一次显现,**Stage 1 的需求工件应被更新**(由工程师驱动,不由编排技能自动改)。

#### 4.2 调用 `clm-coverage-gap-analyzer`

**输入**:运行 Simulink Coverage 后的报告 `coverage_report.html`

**产出**:`coverage_gap_report` 关键缺口:

| GP-ID | 模型对象 | 维度 | 分类 | 闭环路径 |
| --- | --- | --- | --- | --- |
| GP-01 | `Controller/AttitudeLoop/AW/BackCalc` | Decision | unexercised | 用例增补 → `clm-test-harness-builder` 等价类分组(已涵盖,只需补激励变体) |
| GP-02 | `FaultMonitor/Limiter` 互斥分支 | MCDC | unreachable | 显式接受 + 文档化(条件互斥) |
| GP-03 | `Active.Cruise → Hover` 反向转移 | Transition | unexercised | 用例增补 → 状态切换分组,**新增 TC-SF-02** |

#### 4.3 调用 `clm-flight-log-replay-bridge`(反向跨库桥)

**输入**:FMT 端 `mlog_decode_summary`(已由 `fmt-mlog-decoder` 产出)+ `flight_phase_segments`(已由 `fmt-flight-log-segmenter` 产出)+ 本库 `codegen_output_map`(信号名映射中转表)

**关键设计点**:`firmware_context` 与 `tool_context` 双侧保留;变体 `vtol` 显式声明;单位逐信号核对(姿态 rad,速度 m/s);采样率从 mlog 200 Hz → 目标 400 Hz 用零阶保持。

**产出**:`flight_log_replay_dataset` 关键段:

| 段 | 时间窗 | 飞行段 | 映射的测试场景 | 用途 |
| --- | --- | --- | --- | --- |
| SEG-01 | t∈[120, 145] s | transition | TC-AW-01 | 基线对比(主用) |
| SEG-02 | t∈[60, 75] s | hover | TC-EQ-01 | 激励 + 基线 |

**未映射信号**(列入 `gaps`):FMT 端 `mlog.aux_temp` 字段在模型侧无对应,影响小 → 文档化后忽略。

#### 4.4 调用 `clm-pil-hil-replay-analyzer`

**输入**:`flight_log_replay_dataset`(SEG-01 作为基线)+ PIL 采集数据(用户已采)+ `test_harness_plan`(通过判据)+ `codegen_output_map`(SIL→PIL 一致性)

**产出**:`pil_hil_replay_findings`:

- **时间对齐**:交叉相关法,残差 ≤ 8 ms(< 1 sample @ 100 Hz),不降级
- **采样率**:PIL = 1000 Hz,基线 = 400 Hz(经 1.3 中归一化),线性插值,无混叠风险
- **通过判据评估**:

| 用例 ID | 评估 | 偏差量化 |
| --- | --- | --- |
| TC-AW-01 | **PASS** | 恢复时间 = 580 ms(目标 < 800 ms);`\|err\|` 峰值 = 0.7 deg |
| TC-AW-02 | PASS | RateLimiter 与 AW 共存,无死锁 |
| TC-EQ-01 | PASS |  |
| TC-SF-01 | NA | 该用例数据未被 PIL 覆盖(本批数据不含模式切换),原因明确 |

- **退化信号**:无退化(对照基线 SEG-01 实飞)
- **跨库 cross_library_findings**:本工件输出至 `fmt-control-performance-analyzer`,声明命名 / 单位 / 变体一致

**Stage 4 退出门禁**:

- ✅ 关键判据(TC-AW-01)PASS
- ⚠️ TC-SF-01 = NA,**Non-Blocking**:用户决定是否在下一批 PIL 采数中补
- ✅ 无退化信号

### Stage 5:Deploy Handoff

`clm-model-to-deploy-handoff` 在 backlog,本场景下编排技能将该阶段标记 `blocked(skill 待建)`,要求工程师手工生成交接清单。

## 4. 编排技能产出的 `pipeline_status` 摘要

```yaml
artifact_name: pipeline_status
task_id: vtol-att-aw-retrofit-2026q2
tool_matrix:
  consistency: ok
  details: { Simulink: R2023b, EmbeddedCoder: R2023b, FxPDesigner: R2023b, SimulinkTest: R2023b }

stages:
  Stage1_ModelReading:    { status: passed,  artifacts: [simulink_model_map, stateflow_semantics, data_dictionary_map, requirement_trace_map] }
  Stage2_ModelAuthoring:  { status: passed,  artifacts: [anti_windup_design, compliance_refactor_diff], skipped: [fixed_point_refactor: target has FPU] }
  Stage3_CodegenBridge:   { status: passed,  artifacts: [coder_config_review, codegen_output_map, storage_class_governance] }
  Stage4_Verification:    { status: passed_with_warnings, artifacts: [test_harness_plan, coverage_gap_report, flight_log_replay_dataset, pil_hil_replay_findings] }
  Stage5_DeployHandoff:   { status: blocked, reason: "clm-model-to-deploy-handoff 待建" }

gate_log:
  - { gate: G1.out, result: pass,    note: "REQ-ATT-009 orphan 已在 Stage 4 通过 TC-AW-01 闭合" }
  - { gate: G3.out, result: warn,    note: "FMT 接口层命名前缀差异" }
  - { gate: G4.out, result: pass,    note: "TC-SF-01 = NA, Non-Blocking" }

unmet_gates:
  - { gate: G5.in,  reason: "Stage 5 skill 待建" }

cross_library_handoff:
  outbound:
    - { artifact: codegen_output_map.bridge_layer_contract, to: fmt-mbd-interface-reader,  status: ack_with_diff(命名前缀) }
    - { artifact: pil_hil_replay_findings,                  to: fmt-control-performance-analyzer, status: handed_off }
  inbound:
    - { artifact: mlog_decode_summary,    from: fmt-mlog-decoder,         consumed_by: flight-log-replay-bridge }
    - { artifact: flight_phase_segments,  from: fmt-flight-log-segmenter, consumed_by: flight-log-replay-bridge }
  context_preservation:
    firmware_context: { variant: vtol, mlog_version: v3 }   # 保留,未被 tool_context 覆盖
    tool_context:     { simulink: R2023b, target_hw: cortex-m7 }

risk_register:
  - { id: R-01, src: Stage2.anti_windup_design, level: medium, item: "AW × RateLimiter 相互作用",        regression_point: TC-AW-02 (Stage 4 已覆盖) }
  - { id: R-02, src: Stage3.bridge_diff,         level: medium, item: "FMT 接口前缀差异",                 regression_point: 工程师决策 }

next_actions:
  - 工程师按 compliance_refactor_diff 施工(Stage 2 → Stage 3 反馈环路:再次运行 Stage 3 验证)
  - 与 FMT 维护方对齐命名前缀,落入下一轮 storage_class_governance
  - 计划下一批 PIL 数据补 TC-SF-01
  - 等待 clm-model-to-deploy-handoff 落地以完成 Stage 5
```

## 5. 反馈环路演示

本场景至少展示 3 类反馈环路 — 由编排技能识别并提示,**但施工与再验证由工程师驱动**(不在编排技能内自动循环):

1. **Stage 1 ↔ Stage 4(需求 ↔ 用例)**:Stage 1 报出 `REQ-ATT-009` orphan,Stage 4 的 `test_harness_plan` 新增 TC-AW-01 闭合;工程师施工后应回到 Stage 1 重新运行 `clm-requirement-trace-reader` 验证 link 已建立。
2. **Stage 2 → Stage 3(改完模型 → 重生代码)**:`compliance_refactor_diff` 含若干 `refactor` 项,施工后必须重新生成代码并重跑 Stage 3 三 skill。
3. **Stage 3 ↔ FMT**(命名前缀差异):`storage_class_governance` 桥接段标差异,与 FMT 维护方对齐后再回到 Stage 3 验证。

## 6. 经验教训(从这次 worked example 提炼)

针对 16 个 skill 的契约设计,本场景验证了以下设计决策的必要性:

| 设计决策 | 验证场景 |
| --- | --- |
| 工件含 `tool_context`(第一性原理契约第 2 项) | Stage 3 模型/代码时间戳一致性核对避免了"用旧代码做映射"的常见错误 |
| `unreachable` 缺口需推断证据(coverage 边界) | GP-02 是否可接受需要"条件互斥"代码证据,不允许默认接受 |
| AW Kt 只给方法 + 占位 | 工程师在 PIL 中调出实际 Kt = 0.85 / Kp_att,落在占位区间内,本 skill 不抢占工程师调试空间 |
| 跨库 `firmware_context` / `tool_context` 双侧保留 | flight-log-replay-bridge 的变体 `vtol` 跨库传递,避免了下游误用 mc/fw 规则 |
| 编排技能不下"已可投产"结论 | Stage 5 因 deploy-handoff skill 待建,标记 blocked;**这是正确的失败模式**,而非伪通过 |
| `accept-residual` 必须文档化 | GP-02 默认接受需理由 + 评审签字,避免审计漏洞 |
| `Storage Class = Auto` 不假设结果 | Stage 1 已显式标 4 个对象需治理,Stage 5 治理完成后桥接核对就有依据了 |

## 7. 与本 worked example 配套的工件命名约定

为便于审计与回放,本任务中所有工件文件名建议:

```
artifacts/<task_id>/<stage>-<seq>-<artifact_name>.json
artifacts/vtol-att-aw-retrofit-2026q2/
├─ 1.1-simulink_model_map.json
├─ 1.2-stateflow_semantics.json
├─ 1.3-data_dictionary_map.json
├─ 1.4-requirement_trace_map.json
├─ 2.1-anti_windup_design.json
├─ 2.2-compliance_refactor_diff.json
├─ 3.1-coder_config_review.json
├─ 3.2-codegen_output_map.json
├─ 3.3-storage_class_governance.json
├─ 4.1-test_harness_plan.json
├─ 4.2-coverage_gap_report.json
├─ 4.3-flight_log_replay_dataset.json
├─ 4.4-pil_hil_replay_findings.json
└─ 0-pipeline_status.json   ◄── 由编排技能产出,索引以上工件
```

## 8. 不演示的场景(留给后续 worked examples)

为保持本文档聚焦,以下场景**有意未覆盖**,可作为后续 worked example 的素材:

1. **浮点 → 定点改造**(`clm-fixed-point-refactor` 主线场景):目标硬件无 FPU 时
2. **故障注入与残留风险接受**:覆盖率含较多 `accept-residual`
3. **从零 pattern 设计**(`clm-control-law-pattern-author` 主线):新建控制律子系统
4. **多变体并行**(`vtol` + `mc` + `fw` 共享一套 skill 集合):桥接层多 wrapper

## 9. 索引(本 example 触及的所有 skill)

| 阶段 | Skill | 在本 example 中的作用 |
| --- | --- | --- |
| Stage 1 | `clm-simulink-model-reader` | 模型层级 + 多速率 |
| Stage 1 | `clm-stateflow-semantics-reader` | ModeManager 转移语义 |
| Stage 1 | `clm-data-dictionary-reader` | Storage Class 现状 + 风险 |
| Stage 1 | `clm-requirement-trace-reader` | REQ-ATT-009 orphan 暴露 |
| Stage 2 | `clm-anti-windup-author` | AW 选型 + Kt + MIMO |
| Stage 2 | `clm-codegen-compliance-refactor` | 聚合改造 backlog |
| Stage 2 | `clm-control-law-pattern-author` | (未触发,场景为重构而非新建) |
| Stage 2 | `clm-fixed-point-refactor` | (跳过,目标硬件含 FPU) |
| Stage 3 | `clm-embedded-coder-config-reviewer` | 配置审查 |
| Stage 3 | `clm-codegen-output-mapper` | 模型 ↔ 代码映射 + bridge_layer_contract |
| Stage 3 | `clm-storage-class-governor` | 治理决策 + 桥接核对 |
| Stage 4 | `clm-test-harness-builder` | 用例骨架 + 闭合 orphan |
| Stage 4 | `clm-coverage-gap-analyzer` | 缺口路由 |
| Stage 4 | `clm-flight-log-replay-bridge` | FMT 实飞日志 → 回放数据集 |
| Stage 4 | `clm-pil-hil-replay-analyzer` | PIL vs 基线 + 跨库 handoff |
| Workflow | `clm-control-law-mbd-pipeline` | 顺序 / 门禁 / 汇总 / 跨库 |

— END —
