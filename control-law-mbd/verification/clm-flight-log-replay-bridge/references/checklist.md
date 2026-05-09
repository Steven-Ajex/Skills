# 检查清单(Checklist)

用于在交付 `clm-flight-log-replay-bridge` 输出前做快速复核。

## clm-flight-log-replay-bridge 专项检查

- [ ] 时间基准已声明(基准时刻 + 单位 + 漂移估计)
- [ ] 采样率归一化方法已声明;若降采样则混叠风险已评估
- [ ] 关键控制信号(参考 / 反馈 / 控制量 / 模式 / 关键传感器)的信号名映射齐全
- [ ] 单位一致性已逐信号核对;不一致时已给归一化方案
- [ ] 变体显式声明(`vtol`/`mc`/`fw`/`unknown`);`unknown` 必须有理由 + 影响
- [ ] 至少一段(若提供 `flight_phase_segments`)对应到测试场景
- [ ] 数据格式与喂入方式(`From Workspace` / `Test Sequence` / `Signal Builder` / `.mat` / `.csv`)已选型

## 跨库上下文(Cross-Library Context)

- [ ] `firmware_context`(FMT 侧:变体 / mlog 版本 / 信号 catalog)已记录
- [ ] `tool_context`(本库侧:目标采样率 / 数据形态 / 平台)已记录
- [ ] 两侧上下文各自保留,未互相覆盖
- [ ] 上下文不一致或缺失时已在 `gaps` 中登记

## 输入与范围

- [ ] `mlog_decode_summary` 已提供(必需上游);未提供时已阻断
- [ ] (推荐)`flight_phase_segments` 是否提供;未提供时分段索引已降级
- [ ] (推荐)`codegen_output_map` 是否提供;未提供时映射置信度已降级
- [ ] (可选)`test_harness_plan` 是否提供
- [ ] 输入缺口(Gaps)已列出

## 时间基准纪律(Timebase Discipline)

- [ ] 基准时刻已声明(`armed`/`takeoff`/用户指定 timestamp)
- [ ] 漂移估计已给出(若 mlog 时间戳与系统时间有偏移)
- [ ] 时间单位换算无误

## 信号映射纪律(Signal Mapping Discipline)

- [ ] 关键控制信号至少覆盖
- [ ] 未映射信号列入 `gaps` 而非默认零值或假设
- [ ] 经 `codegen_output_map` 中转(若提供)
- [ ] FMT 字段名 + 模型侧信号名两侧均保留原文

## 单位一致性纪律

- [ ] 角度(rad / deg)、速度(m/s / ft/s)、归一化(±1 / 物理量)逐信号核对
- [ ] 不一致时给出归一化方案
- [ ] 没有"假设默认单位"通过

## 变体纪律(Variant Discipline)

- [ ] 显式声明 `vtol`/`mc`/`fw`/`unknown`
- [ ] `unknown` 时有理由 + 影响声明
- [ ] 变体一致性传递到下游 skill

## 采样率纪律

- [ ] 目标采样率明确
- [ ] 重采样方法选型(零阶保持 / 线性插值 / 抗混叠 + 降采样)
- [ ] 降采样时混叠风险已评估

## 边界与纪律

- [ ] 没有解码 mlog / 没有做分段 / 没有做性能分析
- [ ] 没有做 PIL 回放对比
- [ ] 没有下调参建议
- [ ] 没有修改任何文件
- [ ] 没有下"飞行数据已可作回放基线"结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `flight_log_replay_dataset`
- [ ] 工件包含 `tool_context` / `firmware_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `signal_catalog` / `timebase` / `phase_index` / `replay_baseline_candidate`
- [ ] 下游 `clm-pil-hil-replay-analyzer` 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响段与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] mlog 字段名 / 模型侧信号名(英文)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
