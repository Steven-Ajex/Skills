---
name: fmt-control-loop-reader
description: 读取 FMT-Firmware 的主调度与控制闭环数据路径（sensor 到 INS、FMS、Controller、actuator）并梳理模块边界与执行顺序的专用技能。用于只需要理解 FMT 控制循环结构、任务节拍、topic 数据流、调用链入口时；不负责深入分析 FMS 状态机细节或控制器参数优化。
---

# FMT Control Loop Reader

## 目标

建立对 FMT 控制闭环执行顺序和数据流向的正确认识，输出一份“调度与数据路径地图”。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在单一机型变体与单一任务入口范围内，完成 FMT 控制闭环调度与数据路径（sensor -> INS -> FMS -> Controller -> actuator）的证据化梳理。
2. 核心输入（Inputs）
   - FMT-Firmware 代码路径（至少可读取 `src/task`、`src/module/sensor`、`src/model/*`）
   - 机型变体信息（`vtol` / `mc` / `fw`），未知时需显式标注 `unknown`
   - 任务入口或目标现象（如用户关注某条控制链路）
3. 核心输出（Outputs）
   - 主交付工件：`control_loop_map`
   - 控制循环顺序、模块边界、topic/MCN 数据路径、节拍关系与证据索引
   - 供下游使用的关注点（例如需要进一步查看的 FMS 状态字段或接口层 bus）
4. 完成判据（Definition of Done, DoD）
   - 至少一条完整闭环路径被串起来（入口 -> 关键模块 -> 输出）
   - 周期/节拍判断有代码证据，不靠经验猜测
   - 明确当前变体与未确认宏开关/条件分支
   - 区分事实（Fact）与推断（Inference）
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 聚焦范围（只做这些）

1. 主任务/定时器调度入口
2. 控制循环执行顺序
3. 关键 topic（MCN）数据流向
4. 模块边界（sensor / INS / FMS / Controller / actuator）
5. 周期（Period）与节拍关系

## 不负责

1. 深入解释 FMS 状态机转换条件
2. 深入解释 MBD 生成控制律内部结构
3. `mlog` 二进制解码
4. 参数优化建议

## 推荐阅读顺序（FMT-Firmware）

1. `src/task/vehicle/normal/task_vehicle.c`
2. `src/module/sensor/sensor_hub.c`
3. `src/model/ins/*/ins_interface.c`
4. `src/model/fms/*/fms_interface.c`
5. `src/model/control/*_controller/control_interface.c`
6. 执行器输出链路（如 `send_actuator_cmd()` 所在模块）

## 执行步骤

1. 先确认机型变体（`vtol` / `mc` / `fw`）和实际使用的 `control/fms/ins` 变体。
2. 从 `task_vehicle_entry()` 开始提取一轮循环执行顺序。
3. 标出每一步的输入、输出、调用对象、节拍条件。
4. 对关键 topic 建立“发布者 -> 订阅者”关系。
5. 标出可能影响时序判断的条件分支（如 HIL/SIH、宏开关）。

## 输出要求

输出内容至少包含：

1. 控制循环顺序图（文本版即可）
2. 模块职责表（sensor / INS / FMS / Controller / actuator）
3. topic 数据流清单（输入/输出）
4. 周期与节拍说明（含证据）
5. 不确定项（例如变体未确认、宏开关未确认）

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - 代码工程可读性与变体信息
2. 下游使用方（Downstream Consumers）
   - `fmt-mbd-interface-reader`
   - `fmt-fms-state-machine-reader`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `control_loop_map`
   - 工件至少包含：分析范围（scope）、关键事实（facts）、关键推断（inferences）、证据索引（evidence index）、缺口清单（gaps）、下游输入建议（next skill inputs）。
4. 共享规范（Shared Contracts）
   - 参考 `fmt/_meta/first-principles-skill-contract.md`
   - 参考 `fmt/_meta/artifact-handoff-contract.md`

## 质量门禁（Quality Gates）

1. 必过门禁（Mandatory Gates）
   - 边界门禁（Boundary Purity）：不输出超出本技能职责的确定性结论。
   - 证据门禁（Evidence Traceability）：关键结论必须能回链到代码路径行号或日志时间段。
   - 变体门禁（Variant Scope）：明确 `vtol/mc/fw` 适用范围，未知时标注 `unknown`。
   - 交接门禁（Handoff Usability）：输出可被下游技能直接消费，不只给散文式描述。
   - 时序门禁：凡是周期/节拍结论，必须指出触发条件或定时器/循环位置。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 变体未知时：允许输出“通用路径 + 变体差异待确认点”，但不下具体变体结论
   - 入口函数不明确时：先列候选入口并给出确认方法（任务注册/启动路径）
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：需要快速输出控制闭环地图时先读模板；提交给下游技能前再用清单复核时序与证据完整性。

## 证据标准

1. 所有结论附文件路径和行号。
2. 区分事实 (Fact) 与推断 (Inference)。
3. 遇到多变体实现时，明确当前分析对象，不混用。
