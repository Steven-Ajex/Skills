---
name: fmt-control-loop-reader
description: 读取 FMT-Firmware 的主调度与控制闭环数据路径（sensor 到 INS、FMS、Controller、actuator）并梳理模块边界与执行顺序的专用技能。用于只需要理解 FMT 控制循环结构、任务节拍、topic 数据流、调用链入口时；不负责深入分析 FMS 状态机细节或控制器参数优化。
---

# FMT Control Loop Reader

## 目标

建立对 FMT 控制闭环执行顺序和数据流向的正确认识，输出一份“调度与数据路径地图”。

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

## 证据标准

1. 所有结论附文件路径和行号。
2. 区分事实 (Fact) 与推断 (Inference)。
3. 遇到多变体实现时，明确当前分析对象，不混用。
