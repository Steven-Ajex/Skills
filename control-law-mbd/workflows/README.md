# Workflows（编排技能）

控制律 MBD **端到端编排型**技能（workflow skill）的容器目录。

## 1. 职责（What）

负责**协调 `model-reading/` / `model-authoring/` / `codegen-bridge/` / `verification/` 中的原子技能**,完成跨阶段任务,并在阶段之间做门禁检查（Gate Check）。

工作流技能**不替代**原子技能的专业判断,只决定:

- 调用顺序
- 是否进入下一阶段（基于上游工件是否满足门禁）
- 跨阶段结论的拼接与汇总（必须引用上游工件,不能绕开）

## 2. 规划 skill 列表

| Skill 名 | 最小任务单元 | 主要工件 | 状态 |
| --- | --- | --- | --- |
| `clm-control-law-mbd-pipeline` | 端到端:需求 → 模型解读 → 重构 → 代码生成 → 在环验证 → 部署交接 | `pipeline_status` + 各阶段原子工件汇总 | 已落地 |
| `clm-model-to-deploy-handoff` | Stage 5 合成 workflow:聚合 Stage 1-4 工件为可审计的"模型 → 部署"交接包 | `deploy_handoff_package` | 已落地 |

后续候选(Backlog):

- `clm-mbd-regression-comparison`(多版本模型对比)

> 编排技能严格只做顺序、门禁、汇总;阶段对应原子 skill 未落地时该阶段标记 `blocked`,本编排技能不"代行"原子 skill 的专业判断。

## 3. 不负责（Out of Scope）

- 任何**单阶段**专业判断(必须委派到对应原子技能)
- 替代用户决策(只汇总并提示,不擅自决定 trade-off)
- 嵌入式集成与飞行验证 → 转交 `fmt/workflows/fmt-flight-control-param-optimizer`

## 4. 编排门禁（Gate Checks，最低要求）

工作流技能进入下一阶段前必须检查:

1. 上游工件存在
2. `tool_context` 一致（Simulink/Coder 版本、模型形态匹配）
3. `scope` 匹配（模型路径 / `.sldd` / 生成代码 / 用例集合一致）
4. `facts` / `evidence_index` / `gaps` 字段齐全
5. 缺口是否 Blocking（阻断时不得进入下一阶段,需显式说明）

## 5. 与 `fmt/` 库的衔接

本目录的 `clm-control-law-mbd-pipeline` 是与 FMT 工作流的**自然交接点**:

- 输出给 FMT 的工件:`codegen_output_map` + `pil_hil_replay_findings`
- 接收 FMT 的工件:`control_performance_findings`(用于反哺模型层调参)
- 跨库工作流编排时,**两侧工作流均保持自身边界**,通过工件契约通信

## 6. 共同输出契约

工件必须满足 `../_meta/artifact-handoff-contract.md`,并额外包含:

- `pipeline_status`:各阶段 `pending` / `passed` / `blocked` 状态
- `unmet_gates`:未满足的门禁清单与原因
- `cross_library_handoff`:与 `fmt/` 工作流的交接记录(如适用)
