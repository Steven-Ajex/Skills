---
name: fmt-mbd-interface-reader
description: 读取 FMT-Firmware 中 INS/FMS/Controller 的接口桥接代码与 MBD 生成代码边界（`*_interface.c` vs `lib/*.c`），梳理参数绑定、bus 定义、topic 映射和模型调用入口的专用技能。用于需要准确理解控制律代码结构而非调度全局或日志分析时。
---

# FMT MBD Interface Reader

## 目标

搞清楚 FMT 控制律模块里“接口层做什么、生成代码层做什么”，避免把桥接逻辑和控制律逻辑混在一起分析。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在单一控制律模块（INS/FMS/Controller 的某一变体目录）内，完成接口桥接层与 MBD 生成代码层的职责划分与数据映射梳理。
2. 核心输入（Inputs）
   - 目标模块目录（如 `src/model/fms/vtol_fms/`）
   - `*_interface.c` 与 `lib/` 生成代码文件可读
   - 变体信息与任务关注点（参数绑定、bus 映射或模型入口）
3. 核心输出（Outputs）
   - 主交付工件：`mbd_boundary_map`
   - 接口层 vs 生成代码层职责对照、topic/bus 映射、参数绑定路径、模型 `init/step` 调用链
   - 需要进入生成代码进一步确认的隐藏复杂度清单
4. 完成判据（Definition of Done, DoD）
   - 接口层与生成代码层边界已明确，未混淆 glue code 与控制律本体
   - 至少一条参数绑定路径和一条 bus/topic 映射路径可回链到代码
   - 对生成代码内部未验证部分显式标注为待确认项
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

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

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - `fmt-control-loop-reader`（推荐）或用户指定的目标模块路径
2. 下游使用方（Downstream Consumers）
   - `fmt-fms-state-machine-reader`
   - `fmt-control-performance-analyzer`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `mbd_boundary_map`
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
   - 边界门禁：不把 `*_interface.c` 中的适配逻辑写成“控制律算法结论”。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 若生成代码文件过大：先输出文件角色地图（`*_types.h`/`*_data.c`/入口函数）再逐步下钻
   - 若模块变体未确认：并列列出候选目录差异，不混合字段语义
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：在需要区分 interface glue code 与控制律本体时加载模板；输出前用清单检查边界纯度。

## 分析纪律

1. 不把 `*_interface.c` 中的 glue code 当成控制律本体。
2. 不对生成代码内部状态机/控制器细节做无证据推断。
3. 优先给结构化映射，再给评价。
