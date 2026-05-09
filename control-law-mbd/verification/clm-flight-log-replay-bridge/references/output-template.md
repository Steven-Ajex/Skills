# clm-flight-log-replay-bridge 输出模板

## 使用说明

- 目标:把 FMT 解码工件转化为模型侧 MIL/SIL/PIL/HIL 回放可消费的激励数据集
- 主交付工件(Primary Artifact):`flight_log_replay_dataset`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 是**反向跨库桥** — 与 `bridge_layer_contract`(模型 → FMT)互为方向

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-flight-log-replay-bridge`
- `artifact_name`:`flight_log_replay_dataset`

## 跨库上下文(Cross-Library Context)

`firmware_context`(FMT 侧):

- 变体(`vtol`/`mc`/`fw`/`unknown`):
- mlog 版本:
- 信号 catalog 来源:
- 架次 ID / 飞行编号:

`tool_context`(本库侧):

- 目标平台(Simulink Real-Time / HIL / MIL):
- 目标采样率(Hz):
- 目标数据形态(`.mat` / `.csv` / `Test Sequence`):

两侧上下文一致性结论:`双侧保留,无相互覆盖` / `存在冲突(详见 gaps)`

## 上游工件回引(Upstream Artifacts)

- `mlog_decode_summary`:`<artifact_id 或文件路径>`(必需)
- `flight_phase_segments`:`<artifact_id 或文件路径>`(可选)
- `codegen_output_map`:`<artifact_id 或文件路径>`(可选)
- `test_harness_plan`:`<artifact_id 或文件路径>`(可选)

## 范围与假设(Scope & Assumptions)

- [ ] 单架次 / 单变体范围
- [ ] 是否含 segment
- [ ] 是否含信号映射依据
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 解码工件路径
- [ ] 分段工件路径(若有)
- [ ] 信号映射上游(若有)
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 时间基准对齐(Timebase Alignment)

- 基准时刻:`armed` / `takeoff` / 用户指定 timestamp
- 单位:`s` / `ms` / `us`
- 漂移估计:`<= X ms over flight`
- 是否需要校正:

### 2. 信号名映射表(Signal Name Mapping)

| 类别 | FMT 端字段名 | 单位(FMT) | 模型侧信号名 | 单位(模型) | 中转 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 参考 |  |  |  |  | `codegen_output_map > <path>` |  |
| 反馈 |  |  |  |  |  |  |
| 控制量 |  |  |  |  |  |  |
| 模式 |  |  |  |  |  |  |
| 关键传感器 |  |  |  |  |  |  |

未映射的关键信号(列入 `gaps`):

| 类别 | FMT 端字段 | 失败原因 | 替代方案 |
| --- | --- | --- | --- |
|  |  |  |  |

### 3. 单位一致性核对(Unit Consistency)

| 信号 | FMT 单位 | 模型单位 | 一致? | 归一化方案(若不一致) |
| --- | --- | --- | --- | --- |
| 姿态角 | rad | rad |  |  |
| 速度 | m/s | m/s |  |  |
| 归一化油门 | 0-1 | 0-1 |  |  |

### 4. 采样率归一化(Sampling Rate Normalization)

| 来源采样率(Hz) | 目标采样率(Hz) | 重采样方法 | 混叠风险评估 |
| --- | --- | --- | --- |
|  |  | 零阶保持 / 线性插值 / 抗混叠 + 降采样 |  |

### 5. 分段索引 + 场景标注(Phase Index + Scenario Tagging)

| 段 ID | 时间窗 [t_start, t_end] | 飞行段(takeoff/cruise/transition/landing/fault) | 映射的测试场景 | 用途(激励 / 基线 / 兼用) |
| --- | --- | --- | --- | --- |
| SEG-01 |  | takeoff |  |  |
| SEG-02 |  | cruise |  |  |
| SEG-03 |  | transition |  |  |

### 6. 数据格式与喂入方式选型(Feed-in Format)

- 平台:
- 喂入方式:`From Workspace` / `Test Sequence` / `Signal Builder` / `.mat` / `.csv` / 自定义
- 选型理由:
- 输出文件清单与字段约定:

| 输出文件 | 字段 | 单位 | 频率 | 用途 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 7. 回放基线候选(Replay Baseline Candidate)

- 用作"基线对比"的段(供下游 `clm-pil-hil-replay-analyzer`):
- 通过判据建议(可由 `test_harness_plan` 复用):
- 通过判据数值容差需要的额外考量(若飞行数据本身存在测量噪声):

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- mlog 字段证据:`mlog_decode_summary > IMU_data.gyro` → 对应模型 `imu_gyro_rad_s`
- 分段证据:`flight_phase_segments > SEG-02 transition` → t∈[120s, 145s]
- 映射证据:`codegen_output_map > controller_data.c:42 imu_gyro_rad_s` → 模型信号

## 缺口与风险(Gaps & Risks)

- 缺口(例:关键信号缺失 / mlog 时间戳异常 / 变体未确认 / 单位不一致):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-pil-hil-replay-analyzer`(关注:replay_baseline_candidate + 通过判据建议)
  - `clm-test-harness-builder`(关注:分段索引 → 场景标注作为基线用例补充)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`,跨库 `cross_library_handoff` 段)
- 跨库下游(FMT 端):
  - `fmt-control-performance-analyzer`(本工件的 `replay_baseline_candidate` 与 FMT 实飞分析对照)
- 建议关注的段 / 信号 / 用例:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未解码 / 未分段 / 未做性能分析 / 未做 PIL 对比 / 未给调参建议
- [ ] 时间基准纪律:基准 + 漂移 + 单位三项齐全
- [ ] 信号映射纪律:关键信号覆盖,未映射列入 gaps
- [ ] 单位一致性:逐信号核对,不一致有归一化方案
- [ ] 变体纪律:显式声明,unknown 有理由 + 影响
- [ ] 跨库纪律:firmware_context 与 tool_context 双侧保留
- [ ] 采样率纪律:降采样混叠风险已评估
- [ ] 交接可用性:`clm-pil-hil-replay-analyzer` 可直接消费

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`(尤其第 8 节"跨库工件衔接")
- `../../_meta/quality-scorecard.md`
