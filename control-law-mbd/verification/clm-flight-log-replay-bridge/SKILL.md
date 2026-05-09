---
name: clm-flight-log-replay-bridge
description: 把 FMT 实飞日志(由 fmt-mlog-decoder / fmt-flight-log-segmenter 产出的解码与分段工件)转化为可直接喂给 MIL/SIL/PIL/HIL 回放的"激励数据集"的反向跨库桥技能。负责时间基准与采样率归一化、信号名映射(FMT 端 ↔ 模型端,通过 codegen_output_map 中转)、变体声明、分段索引与场景标注;产出 `flight_log_replay_dataset` 工件。用于"用真实飞行数据反哺模型侧验证"场景;不解码 FMT 日志(转 fmt-mlog-decoder)、不做飞行段控制性能分析(转 fmt-control-performance-analyzer)、不做 PIL/HIL 回放对比本身(转 clm-pil-hil-replay-analyzer)、不修改任何模型或代码。
---

# Control-Law-MBD: Flight Log Replay Bridge

## 目标

把"FMT 端已经解码、已经分段的实飞日志"转化为"模型侧可以作为激励/对比基线的数据集",并显式把 FMT 端的"信号名/单位/变体/firmware_context"映射到模型侧的"信号名/单位/tool_context",让 `clm-pil-hil-replay-analyzer` 能开箱使用,产出 `flight_log_replay_dataset` 工件。本 skill 是**反向跨库桥** — 与 `bridge_layer_contract`(模型 → FMT)互为方向。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一架次(single flight)/ 单一变体(`vtol`/`mc`/`fw`)+ 单批解码工件范围内,完成时间基准/采样率归一化、信号名映射、分段索引、变体声明,产出 `flight_log_replay_dataset` 工件
2. 工具上下文(Tool Context)
   - **本库侧(model-side)**:Simulink Test / Simulink Real-Time / 自研 HIL 平台、目标采样率、目标时间基准
   - **FMT 侧(firmware-side)**:`firmware_context`(从 FMT 工件继承,含 mlog/ulog 版本、变体、信号 catalog)
   - 两侧上下文必须各自保留,不互相覆盖
3. 核心输入(Inputs)
   - **必需**:FMT 端解码工件 — `fmt-mlog-decoder` 的 `mlog_decode_summary` 或类似
   - **必需**:FMT 端信号 catalog(从 mlog_decode_summary 或独立提供)
   - **推荐**:FMT 端 `fmt-flight-log-segmenter` 的 `flight_phase_segments`(分段索引)
   - **推荐(模型侧)**:`clm-codegen-output-mapper` 的 `codegen_output_map`(用作信号名映射的中转表)
   - **可选**:`clm-test-harness-builder` 的 `test_harness_plan`(确定哪些用例需要实飞数据作激励 / 基线)
   - **可选**:用户指定的"用例 → 飞行段"映射偏好
4. 核心输出(Outputs)
   - 主交付工件:`flight_log_replay_dataset`
   - 时间基准与采样率归一化记录
   - 信号名映射表(FMT 端 ↔ 模型侧;通过 `codegen_output_map` 中转)
   - 单位一致性核对结果
   - 变体声明(`vtol`/`mc`/`fw`/`unknown`)
   - 分段索引 + 场景标注(每段对应哪个测试场景)
   - 数据格式声明(`.mat` / `.csv` / `From Workspace` 直接喂 / `Test Sequence` 数据集)
   - 缺口清单(信号缺失 / 单位不确定 / 时间戳异常)
5. 完成判据(Definition of Done, DoD)
   - 时间基准已声明(基准时刻 + 单位 + 漂移估计)
   - 采样率归一化方法已声明(零阶保持 / 线性插值 / 抗混叠);若不一致则混叠风险已评估
   - 至少覆盖关键控制信号(参考 / 反馈 / 控制量 / 模式)的信号名映射
   - 单位一致性已逐信号核对
   - 变体显式;不允许 `unknown` 静默通过(必须显式声明 `unknown` 并标注影响)
   - 至少一段(若提供 `flight_phase_segments`)对应到一个测试场景;否则在 `gaps` 中登记
   - 跨库 `tool_context` / `firmware_context` 双侧保留
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留 FMT 端 mlog 字段名、模型侧信号名原文(英文)

## 聚焦范围(只做这些)

1. 时间基准对齐(基准选择 + 漂移估计 + 单位转换)
2. 采样率归一化(目标采样率 + 重采样方法 + 混叠风险)
3. 信号名映射(FMT 端 ↔ 模型侧;经 `codegen_output_map` 中转)
4. 单位一致性(rad / deg / m / m/s / 归一化等)
5. 变体声明与传递
6. 分段索引与场景标注(实飞段 → 测试场景)
7. 数据格式与喂入方式选型(`From Workspace` / `Signal Builder` / `Test Sequence` / `.mat` / `.csv`)
8. 跨库工件交接段

## 不负责

1. 解码 FMT 日志 → 走 `fmt-mlog-decoder`
2. 飞行分段 → 走 `fmt-flight-log-segmenter`
3. 飞行段控制性能分析 → 走 `fmt-control-performance-analyzer`
4. PIL/HIL 回放对比本身 → 走 `clm-pil-hil-replay-analyzer`(本 skill 只产出"激励数据集",不做对比)
5. 调参建议 → 走 `fmt-tuning-report-writer`
6. 修改任何模型 / 代码 / 日志原始文件

## 推荐处理顺序

1. 先做"两侧上下文核对" — `firmware_context`(变体 / mlog 版本 / 信号 catalog)与 `tool_context`(目标采样率 / 数据格式) 各自完整
2. 再做"时间基准对齐" — 基准选择 + 漂移估计 + 单位
3. 再做"信号名映射" — 关键信号优先,通过 `codegen_output_map` 中转
4. 再做"单位一致性核对" — 单位不一致是常见踩坑点
5. 再做"采样率归一化" — 与目标平台一致
6. 再做"分段索引 → 场景标注" — 把飞行段映射到测试场景
7. 最后选"喂入方式" — 平台决定(Simulink Real-Time 偏 `From Workspace`;HIL 偏 `Test Sequence`;MIL 简单测试偏 Signal Builder)

## 执行步骤

1. **校验跨库上下文**:
   - `firmware_context`:变体、mlog 版本、信号 catalog
   - `tool_context`:目标采样率、数据形态、平台
   - 不一致或缺失时,在 `gaps` 中登记
2. **时间基准对齐**:
   - 选基准时刻(常见:`armed`、`takeoff`、用户指定 timestamp)
   - 估计漂移(若 mlog 时间戳与系统时间有偏移)
   - 单位换算(秒 / 毫秒 / 微秒)
3. **信号名映射**:
   - 关键信号清单(参考、反馈、控制量、模式、传感器)
   - 经 `codegen_output_map` 把 FMT 字段名 ↔ 模型侧信号名连起来
   - 无映射的关键信号列入 `gaps`
4. **单位一致性核对**:
   - 角度(rad vs deg)、速度(m/s vs ft/s)、归一化(±1 vs 物理量)
   - 不一致时给出归一化方案
5. **采样率归一化**:
   - 目标采样率(从 `tool_context` 或用户)
   - 方法选型:零阶保持(适合命令信号) / 线性插值(适合连续信号) / 抗混叠 + 降采样
   - 混叠风险(若降采样)
6. **分段索引 → 场景标注**:
   - 飞行段(从 `flight_phase_segments`):起飞 / 巡航 / 转换 / 降落 / 故障
   - 映射到测试场景(从 `test_harness_plan`):瞬态 / 边界 / 模式切换 / 故障注入
   - 每段标注用作"激励" / "对比基线" / "兼用"
7. **数据格式与喂入方式选型**:
   - 平台决定:Simulink Real-Time → `From Workspace`;HIL 系统 → `Test Sequence`;MIL → Signal Builder / Lookup
   - 输出文件清单与字段约定
8. **生成跨库交接段**:`firmware_context` 与 `tool_context` 双侧保留;变体一致性显式声明
9. **生成工件**:按 `references/output-template.md` 填充
10. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 跨库上下文核对(`firmware_context` + `tool_context`)
2. 时间基准对齐方法 + 漂移估计 + 单位
3. 信号名映射表(FMT ↔ 模型侧)
4. 单位一致性核对表
5. 采样率归一化方法 + 混叠风险
6. 分段索引 + 场景标注表
7. 数据格式与喂入方式选型
8. 关键事实(Facts)、关键推断(Inferences)
9. 证据索引(mlog 字段路径 + 模型信号路径 + 飞行段时间窗)
10. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **跨库必需**:`fmt-mlog-decoder` 的 `mlog_decode_summary`
   - **跨库推荐**:`fmt-flight-log-segmenter` 的 `flight_phase_segments`
   - **本库推荐**:`clm-codegen-output-mapper` 的 `codegen_output_map`
   - (可选)`clm-test-harness-builder` 的 `test_harness_plan`
2. 下游使用方
   - `clm-pil-hil-replay-analyzer`(消费"激励数据集"作为 PIL/HIL 回放输入或基线对比)
   - `clm-test-harness-builder`(消费"分段索引 → 场景标注"作为基线用例补充)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `flight_log_replay_dataset`
   - 字段:`tool_context`(本库侧)、`firmware_context`(FMT 侧)、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`signal_catalog`、`timebase`、`phase_index`、`replay_baseline_candidate`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`(尤其第 8 节"跨库工件衔接")
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不解码 mlog / 不做分段 / 不做性能分析 / 不做 PIL 对比 / 不下调参建议 / 不修改任何文件
   - 时间基准纪律(Timebase Discipline):基准选择 + 漂移估计 + 单位三项齐全
   - 信号映射纪律(Signal Mapping Discipline):至少覆盖关键控制信号;未映射信号列入 `gaps` 而非默认零值
   - 单位一致性纪律:不允许"假设默认单位"通过;不一致时给归一化方案
   - 变体纪律(Variant Discipline):必须显式声明变体;`unknown` 必须有理由 + 影响声明
   - 跨库纪律(Cross-Library Discipline):`firmware_context` 与 `tool_context` 双侧保留,不互相覆盖
   - 采样率纪律:降采样时混叠风险已评估
   - 交接门禁:`clm-pil-hil-replay-analyzer` 可直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供 `mlog_decode_summary`**:阻断;转交 `fmt-mlog-decoder`
   - **未提供 `flight_phase_segments`**:可继续工作,但分段索引降级为"全段单一基线",场景标注章节显式降级
   - **未提供 `codegen_output_map`**:信号名映射只能从 FMT 端 catalog + 用户描述推断;置信度降级
   - **变体未确认**:声明 `unknown` + 影响(部分映射可能失效),让下游决定是否继续
   - **mlog 时间戳异常 / 漂移过大**:在 `gaps` 中登记,提示先做时间基准修正
   - **关键信号缺失**:列入 `gaps`,提示在 FMT 端补录或用替代信号
2. 输出降级要求
   - 降级输出必须显式标注受影响段(信号映射 / 分段 / 喂入方式)与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出"飞行数据已可作回放基线"的最终结论(由 `clm-pil-hil-replay-analyzer` 在对比阶段决定)

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,信号映射表与分段索引表直接套用
2. 交付前用 `references/checklist.md` 复核时间基准、单位、变体、跨库纪律
3. 多飞行架次场景:每架次单独输出工件,不合并(架次间 `firmware_context` 可能不同)

## 桥接纪律

1. 不要在本 skill 内"解释"飞行现象 — 那是 `fmt-control-performance-analyzer` 的职责
2. 单位一致性不能默认 — 角度的 rad/deg、速度的 m/s/(km/h)、归一化的 ±1 vs 物理量,任意一处错就毁掉回放
3. 变体声明不能省 — `vtol/mc/fw` 的 mlog 字段集与控制律结构差别大
4. 跨库上下文双侧保留 — `firmware_context` 不要被 `tool_context` 覆盖,反之亦然
5. 不下"飞行数据已可作回放基线"的最终结论 — 由 `clm-pil-hil-replay-analyzer` 在对比阶段决定
