# 单体技能拆分分析（`fmt-flight-control-param-optimizer`）

## 1. 现状判断

当前单体技能覆盖了完整流程：

1. FMT 工程结构理解
2. 控制律代码理解（INS/FMS/Controller）
3. 日志系统理解（mlog/ulog）
4. 实飞日志解码与分析
5. 参数优化建议与报告输出

这对“首次搭建完整流程”是有效的，但在日常使用中会出现问题：

## 2. 为什么需要拆分

### 2.1 准确性问题（Trigger Accuracy）

单体技能的触发描述覆盖范围过大，容易在以下场景被误用：

- 只想看 FMS 状态机，却触发整套调参流程
- 只想解析 mlog，却加载大量控制律/调参内容
- 只想写报告，却带入解码与代码阅读流程

结果：

- 上下文浪费
- 回答焦点不稳
- 容易跳步（没完成前置分析就给调参建议）

### 2.2 专业性问题（Depth Dilution）

当一个 skill 同时负责“代码结构理解 + 日志格式解码 + 控制分析 + 报告写作”，每一段很容易写成泛化流程，而不是专业化流程。

例如：

- `mlog` 解码需要关注二进制格式细节（header/schema/msg framing）
- FMS 状态机分析需要关注模式/状态/触发条件的代码证据
- 控制性能分析需要关注分段、指标、饱和、估计延迟误判

这些关注点应由更小、更专的技能承担。

## 3. 拆分原则（最小能力单元）

采用“最小可复用能力（Minimum Reusable Capability）”作为拆分标准：

1. 一个 skill 只解决一个明确问题
2. 输入和输出边界清晰
3. 可独立使用，也可被更高层工作流组合
4. 不跨多个专业步骤给结论（如未解码日志就给调参建议）

## 4. 拆分后的结构（原子技能 + 编排技能）

### 4.1 原子技能（Atomic Skills）

代码理解层：

- `fmt-control-loop-reader`
- `fmt-mbd-interface-reader`
- `fmt-fms-state-machine-reader`
- `fmt-logging-pipeline-reader`

日志分析层：

- `fmt-mlog-decoder`
- `fmt-flight-log-segmenter`
- `fmt-control-performance-analyzer`
- `fmt-tuning-report-writer`

### 4.2 编排技能（Workflow Skill）

- `fmt-flight-control-param-optimizer`

职责变化：

- 从“做所有事”改为“决定顺序、协调步骤、拼接结论”
- 优先引导使用原子技能
- 只在完整任务时承担总控角色

## 5. 原单体技能能力映射表

| 原能力块 | 新技能归属 | 说明 |
|---|---|---|
| 调度与闭环路径梳理 | `fmt-control-loop-reader` | 聚焦主任务循环与 MCN 数据路径 |
| 接口层与生成代码分工 | `fmt-mbd-interface-reader` | 聚焦 `*_interface.c` 与 `lib/*.c` |
| FMS 状态机识别 | `fmt-fms-state-machine-reader` | 聚焦状态/模式/触发/输出 |
| mlog/ulog 日志链路 | `fmt-logging-pipeline-reader` | 聚焦记录机制与启停逻辑 |
| mlog 解码 | `fmt-mlog-decoder` | 聚焦 header/schema/record 解码 |
| 飞行阶段分段 | `fmt-flight-log-segmenter` | 聚焦 phase segmentation |
| 控制表现分析与证据提取 | `fmt-control-performance-analyzer` | 聚焦性能与根因候选 |
| 报告与试飞计划输出 | `fmt-tuning-report-writer` | 聚焦结构化输出 |
| 全流程串联 | `fmt-flight-control-param-optimizer` | 编排与集成 |

## 6. 拆分后的收益

1. 更容易精准触发（技能描述更窄）
2. 每个 skill 的专业性更强（边界更清晰）
3. 更适合后续扩展（例如增加“VTOL 过渡段专项分析”时不会污染其他技能）
4. 更利于测试与迭代（能单独优化某个环节）

## 7. 风险与控制

### 风险

- 技能数量增多，选择成本上升
- 原子技能之间可能出现边界重叠

### 控制措施

1. 保留编排技能作为入口
2. 在 `fmt/README.md` 维护技能分层与使用时机
3. 在每个 skill 中写清“输入/输出/不负责的部分”
4. 新增 skill 前先检查是否已有同类能力
