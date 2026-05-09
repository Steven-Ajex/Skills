# Control Law MBD Skills Library

面向**控制律设计与 MBD（Model-Based Design，基于模型的设计）模型开发**场景的专用 Codex skills 集合。

适用对象：使用 Simulink / Stateflow 等 MBD 工具链进行控制律建模、自动代码生成、并最终部署到嵌入式飞控/伺服平台的开发流程。

## 设计目标

1. 以最小能力单元（atomic capability）拆分技能，覆盖控制律 MBD 全生命周期的子环节
2. 通过组合（composition）形成端到端工作流（如：需求 → 模型 → 代码 → 在环验证）
3. 让后续新增控制律 MBD skills 可以按统一命名、目录和生命周期管理
4. 与 `fmt/` 库形成上下游协作：本库聚焦“模型侧 + 自动生成”，`fmt/` 聚焦“嵌入式集成 + 飞行验证”

## 目录组织（规划）

```text
control-law-mbd/
├─ README.md
├─ _meta/                 # 拆分分析、管理规则、契约（非技能目录）
├─ model-reading/         # MBD 模型/字典/需求解读类原子技能
├─ model-authoring/       # 控制律建模与重构类原子技能
├─ codegen-bridge/        # 自动代码生成与桥接层对接类原子技能
├─ verification/          # MIL/SIL/PIL/HIL 验证类原子技能
└─ workflows/             # 端到端编排型技能
```

各能力域的职责、规划 skill 列表、触发边界与输出契约,见对应子目录的 `README.md`:

- `model-reading/README.md`
- `model-authoring/README.md`
- `codegen-bridge/README.md`
- `verification/README.md`
- `workflows/README.md`

> 子目录已建立 placeholder。具体 skill 将按路线图逐步落地;新增前请先对照 `_meta/first-principles-skill-contract.md` 与 `_meta/repo-management.md`。

## 规划中的能力域

### 1. Model Reading（模型理解）

- 控制律 Simulink 模型层级与子系统边界解读
- Bus / 数据字典（Data Dictionary）与参数对象（Simulink.Parameter）映射梳理
- Stateflow 状态机模式切换语义提取
- 模型与需求（如 DOORS / ReqIF）双向追溯链分析

### 2. Model Authoring（建模与重构）

- 经典控制律结构（PID、LQR、增益调度、Anti-Windup 等）的标准化建模模板
- 模型重构以满足代码生成约束（无虚拟总线、定步长、合规子系统等）
- 模型规范检查（Model Advisor / 高完整性建模规范）落地

### 3. Codegen Bridge（自动代码生成与接口桥接）

- Embedded Coder 配置审查与代码生成约束诊断
- 生成代码与手写桥接层（如 FMT 的 MBD 接口）的契合点分析
- 参数 / 信号 / 总线在生成代码中的命名与存储类（Storage Class）治理

### 4. Verification（MIL / SIL / PIL / HIL）

- 测试用例从需求到测试 harness 的落地
- 覆盖率（Decision / Condition / MCDC）评估与缺口补齐
- PIL / HIL 数据回放与控制律性能基线对比

### 5. Workflows（编排）

- 端到端：需求理解 → 模型解读 → 重构 → 代码生成 → 在环验证 → 部署交接
- 与 `fmt/workflows/fmt-flight-control-param-optimizer` 的衔接：以飞行日志反哺模型调参

## 与既有库的关系

| 库 | 关注点 | 与本库的衔接 |
| --- | --- | --- |
| `fmt/code-reading/fmt-mbd-interface-reader` | 嵌入式侧 MBD 接口桥接层 | 本库的 `codegen-bridge/` 提供模型侧视角，二者共同构成完整接口契约 |
| `fmt/log-analysis/*` | 飞行日志分析与调参证据 | 输出的调参建议可回流至本库的模型层进行模型级修正 |
| `code-architecture-reader` | 通用工程代码架构解读 | 当 MBD 项目混合手写代码时使用 |
| `skill-capability-splitter` | 技能拆分元技能 | 新增本库 skill 前用于设计原子化边界 |

## 维护约定

- 技能目录名使用小写字母和连字符（hyphen-case），并以 `clm-` 前缀避免与 `fmt-` 等领域库冲突
  - 示例：`clm-simulink-model-reader`、`clm-embedded-coder-config-reviewer`
- 新增 skill 前先在 `_meta/` 沉淀拆分分析与第一性原理契约
- 优先保持 `SKILL.md` 简洁，把模板与详细资料放到各 skill 的 `references/`
- 新增或修改技能后，运行仓库根的校验脚本（如有）

## 入口文档

- `control-law-mbd/_meta/split-analysis.md`：从“控制律设计 MBD 全流程”出发的能力拆分分析
- `control-law-mbd/_meta/repo-management.md`：本库的命名、生命周期与版本管理规则
- `control-law-mbd/_meta/first-principles-skill-contract.md`：原子 skill 的第一性原理契约
- `control-law-mbd/_meta/artifact-handoff-contract.md`：工件交接契约（含与 `fmt/` 库的跨库衔接）
- `control-law-mbd/_meta/quality-scorecard.md`：质量评分卡

## 路线图（Roadmap）

- [x] `_meta/split-analysis.md`
- [x] `_meta/repo-management.md`
- [x] `_meta/first-principles-skill-contract.md`
- [x] `_meta/artifact-handoff-contract.md`
- [x] `_meta/quality-scorecard.md`
- [x] 五大能力域子目录 placeholder（`model-reading/` / `model-authoring/` / `codegen-bridge/` / `verification/` / `workflows/`）
- [x] 首批原子技能:`clm-simulink-model-reader`、`clm-embedded-coder-config-reviewer`
- [x] 第二批原子技能:`clm-stateflow-semantics-reader`、`clm-codegen-output-mapper`
- [x] 首个编排技能:`clm-control-law-mbd-pipeline`
- [x] 第三批原子技能:`clm-data-dictionary-reader`、`clm-test-harness-builder`
- [x] 第四批原子技能:`clm-coverage-gap-analyzer`、`clm-pil-hil-replay-analyzer`(Stage 4 Verification 三角齐)
- [x] 第五批原子技能:`clm-storage-class-governor`(Stage 3 Codegen Bridge 三角齐)、`clm-requirement-trace-reader`(Stage 1 Model Reading 四角齐)
- [x] 第六批原子技能:`clm-control-law-pattern-author`、`clm-codegen-compliance-refactor`(Stage 2 Model Authoring 解锁)
- [x] 第七批专精技能:`clm-anti-windup-author`(AW 专项)、`clm-fixed-point-refactor`(浮点→定点)、`clm-flight-log-replay-bridge`(反向跨库桥 FMT→模型回放)

> 共 16 个 skill 落地:Stage 1(4)+ Stage 2(4)+ Stage 3(3)+ Stage 4(4)+ Workflow(1)。
> 跨库双向闭环就绪:模型 → FMT 通过 `bridge_layer_contract`;FMT → 模型 通过 `flight_log_replay_dataset`。
