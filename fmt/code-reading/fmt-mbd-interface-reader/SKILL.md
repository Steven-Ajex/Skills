---
name: fmt-mbd-interface-reader
description: 读取 FMT-Firmware 中 INS/FMS/Controller 的接口桥接代码与 MBD 生成代码边界（`*_interface.c` vs `lib/*.c`），梳理参数绑定、bus 定义、topic 映射和模型调用入口的专用技能。用于需要准确理解控制律代码结构而非调度全局或日志分析时。
---

# FMT MBD Interface Reader

## 目标

搞清楚 FMT 控制律模块里“接口层做什么、生成代码层做什么”，避免把桥接逻辑和控制律逻辑混在一起分析。

## 聚焦范围（只做这些）

1. `*_interface.c` 职责边界
2. `lib/*.c` / `*.h` 生成代码入口与主要文件角色
3. 参数组定义与参数绑定（`PARAM_GROUP_DEFINE` / `param_link_variable`）
4. `MLOG_BUS_DEFINE` 与 bus 输出映射
5. 模型 `init/step` 调用位置

## 不负责

1. 完整飞行阶段划分
2. `mlog` 解码
3. 控制性能定量分析
4. 最终调参建议

## 适用对象

1. `src/model/ins/<variant>/`
2. `src/model/fms/<variant>_fms/`
3. `src/model/control/<variant>_controller/`

## 执行步骤

1. 选定变体目录后，先读 `*_interface.c`。
2. 提取：
   - 输入 topic（`MCN_DECLARE` / `mcn_subscribe`）
   - 输出 topic（`MCN_DEFINE` / `mcn_publish`）
   - 参数组定义与绑定
   - 日志总线定义与记录点
   - `*_init()` / `*_step()` 调用
3. 再读 `lib/` 下文件，标出：
   - 生成代码主入口函数
   - 状态/参数/数据文件职责（`*_types.h`, `*_data.c`, `*_private.h`）
4. 标记“接口层可见逻辑”和“生成代码内部逻辑”的边界。

## 输出要求

至少包含：

1. 接口层 vs 生成代码层职责对照表
2. 输入/输出 topic 与 bus 映射表
3. 参数组与关键参数绑定路径
4. 模型 `init/step` 调用链
5. 隐藏复杂度清单（需要进入生成代码才能确认的内容）

## 分析纪律

1. 不把 `*_interface.c` 中的 glue code 当成控制律本体。
2. 不对生成代码内部状态机/控制器细节做无证据推断。
3. 优先给结构化映射，再给评价。
