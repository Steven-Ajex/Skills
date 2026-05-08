# clm-test-harness-builder 输出模板

## 使用说明

- 目标:输出 Simulink Test 测试 harness 与用例骨架,支持下游覆盖率分析与 PIL/HIL 回放对比
- 主交付工件(Primary Artifact):`test_harness_plan`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 只设计计划,不真实运行测试

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-test-harness-builder`
- `artifact_name`:`test_harness_plan`
- `tool_context`:
  - Simulink Test 版本:
  - 求解器(Solver Type / Step Size):
  - 采样时间继承:
  - 是否启用 SIL:
  - 激励/观察机制:
  - 许可证可用性:
- `scope`(被测对象路径 + 测试目标):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 被测对象边界已界定
- [ ] 测试目标已声明
- [ ] 是否提供 `simulink_model_map` / `stateflow_semantics` / `requirement_trace_map` / `codegen_output_map`
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 被测对象路径
- [ ] 测试目标
- [ ] 上游工件清单
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. Harness 结构

- 包装方式:`Test Harness Block` / `Subsystem 包装` / `Model-level Harness`
- 激励源:`Signal Builder` / `Test Sequence` / `MATLAB-based` / `From Workspace`
- 观察点:`Test Assessment` / `verify` 调用 / Scope Sink

```
Harness/
├─ Stim/                  [激励源]
├─ DUT/                   [被测对象,引用至 model.slx > Path/To/Subsystem]
└─ Assess/                [Test Assessment / verify 调用]
```

### 2. 用例表(Test Cases)

| 用例 ID | 分组 | 目标 | 激励 | 期望 | 通过判据 | 覆盖维度 |
| --- | --- | --- | --- | --- | --- | --- |
| TC-EQ-01 | 等价类 |  |  |  |  |  |
| TC-BD-01 | 边界 |  |  |  |  |  |
| TC-SF-01 | 状态切换 |  |  |  |  |  |
| TC-FI-01 | 故障注入 |  |  |  |  |  |
| TC-BL-01 | 性能基线 |  |  |  |  |  |

通过判据示例(可机器判定):

- 数值:`max(|attitude_err|) < 0.5 deg`,持续 `t ∈ [1.0, 5.0] s`
- 状态序列:`Standby → Manual → Auto`,转移在 `mode_request==AUTO` 后 `< 100 ms` 完成
- 时间窗:`step response settling time < 200 ms` 在 `t ∈ [0, 1] s` 内

### 3. 需求 → 用例矩阵

| 需求 ID | 关联用例 ID | 覆盖类型(直接/间接) | 备注 |
| --- | --- | --- | --- |
|  |  |  |  |

未覆盖的需求(列入 `gaps`):

### 4. 状态切换用例派生(若涉及 Stateflow)

| 状态路径(源 → 目标) | 触发条件 | 转移动作 | 用例 ID |
| --- | --- | --- | --- |
| `Standby → Manual` |  |  | TC-SF-01 |

依据:`stateflow_semantics` 中的转移表,至少覆盖一条非平凡转移。

### 5. SIL/PIL 准备清单(若适用)

- [ ] 生成代码版本与模型时间戳一致(参考 `codegen_output_map.tool_context`)
- [ ] 目标硬件已确认(Word Length / Endianness)
- [ ] Step Function 入口签名与 harness 接口对接(参考 `codegen_output_map.bridge_layer_contract`)
- [ ] 激励源在 SIL 形态下(From Workspace / S-Function)已可用
- [ ] 通过判据数值容差对应定点/浮点形态做了调整

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 被测对象:`model.slx > Controller/AttitudeLoop`
- 需求引用:`REQ-ATT-005` → `TC-EQ-01`
- 状态路径:`stateflow_semantics > Active.AttitudeCtrl: Standby → Auto` → `TC-SF-01`

## 缺口与风险(Gaps & Risks)

- 缺口(例:需求工件缺失 / Stateflow 工件缺失 / SIL 接口未就绪):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-coverage-gap-analyzer`(关注:用例集合 + 状态/转移覆盖)
  - `clm-pil-hil-replay-analyzer`(关注:基线用例 + 通过判据数值容差)
- 建议关注的用例 ID / 需求 ID / 状态路径:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未运行测试 / 未配置覆盖率 / 未修改模型
- [ ] 证据可追溯:每条用例可回链到被测对象 + 测试目标
- [ ] 工具上下文显式:Simulink Test 版本、SIL 状态已记录
- [ ] 用例完整性:五项字段齐全
- [ ] 通过判据可机器判定
- [ ] 交接可用性:下游 skill 可直接使用
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
