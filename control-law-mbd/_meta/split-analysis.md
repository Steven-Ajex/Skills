# 单体技能拆分分析（`clm-control-law-mbd-pipeline`）

## 1. 现状判断

如果以一个单体 skill 覆盖“控制律 MBD 模型开发”，它要承担的能力链路如下：

1. 控制需求与接口契约理解（含与系统设计、空气动力、整机的边界）
2. Simulink 模型结构与子系统层级解读
3. Stateflow 状态机/模式切换语义解读
4. 数据字典（Data Dictionary）/ Bus / `Simulink.Parameter` 等参数对象解读
5. 控制律结构（PID / LQR / 增益调度 / Anti-Windup / 滤波 / 限幅 / 抗饱和等）建模与重构
6. 模型规范检查（Model Advisor、高完整性建模规范、代码生成约束）落地
7. Embedded Coder 配置审查与生成代码诊断
8. 生成代码与手写桥接层（如 FMT 接口层）契合点分析
9. 存储类（Storage Class）/ 命名 / 参数标定的治理
10. MIL / SIL / PIL / HIL 验证用例与 harness
11. 覆盖率（Decision / Condition / MCDC）评估与缺口补齐
12. 飞行/台架数据回放与控制律性能对比
13. 部署与版本交接

这是“一锅炖”的状态：对完整流程演示有效，对日常使用会带来与 `fmt-flight-control-param-optimizer` 同类的问题。

## 2. 为什么需要拆分

### 2.1 准确性问题（Trigger Accuracy）

单体 skill 触发面过宽，容易在以下场景被误用：

- 只想读懂某子系统的信号流，却被拉入完整 MBD 流程
- 只想审查 Embedded Coder 配置，却带入建模重构与覆盖率分析
- 只想做 PIL 数据回放对比，却带入需求追溯与代码生成诊断

后果与 FMT 库一致：上下文浪费、回答焦点不稳、跳步给结论。

### 2.2 专业性问题（Depth Dilution）

MBD 流程的每个阶段都有强专业性，混在一个 skill 里很容易降级为泛化叙述：

- Simulink 模型解读关注层级、虚拟/非虚拟子系统、原子单元（Atomic Subsystem）、采样时间一致性
- Stateflow 语义关注状态/转移/事件/动作执行顺序与早绑定/晚绑定差异
- 数据字典关注作用域、版本、与 `.sldd` 的引用关系
- 代码生成关注存储类、内联参数、结构化代码、可重入与栈/堆约束
- 验证关注覆盖率工具链（SLDV / Polyspace 等）的真实假阴/假阳模式

这些关注点应由更小、更专的技能承担。

### 2.3 跨工具/跨阶段错位

MBD 流程跨工具（Simulink、Stateflow、Embedded Coder、SLDV、Polyspace、SIL/PIL/HIL 平台）。单体 skill 难以稳定保持工具上下文，容易把“模型层规则”用到“代码生成层”，或把“PIL 现象”当作“模型缺陷”。

## 3. 拆分原则（最小能力单元）

延续 `fmt/` 库的原则，结合 MBD 特性补充：

1. 一个 skill 只解决一个明确问题
2. 输入和输出边界清晰（含工具上下文：模型 `.slx` / 字典 `.sldd` / 生成代码 / 测试 harness / 覆盖率报告 / 回放数据）
3. 可独立使用，也可被更高层工作流组合
4. 不跨多个专业步骤给结论（如未审查代码生成配置就给“生成代码不合规”的结论）
5. 工具维度强相关时单独拆 skill（如“Embedded Coder 配置审查”和“覆盖率缺口分析”不混用）

## 4. 拆分后的结构（原子技能 + 编排技能）

### 4.1 原子技能（Atomic Skills）

模型理解层（Model Reading）：

- `clm-simulink-model-reader`
  解读模型层级、子系统、信号流、采样时间与原子单元
- `clm-stateflow-semantics-reader`
  解读 Stateflow 状态/转移/事件/动作执行顺序
- `clm-data-dictionary-reader`
  解读 `.sldd`、Bus、`Simulink.Parameter` / `Simulink.Signal` 与作用域
- `clm-requirement-trace-reader`
  解读需求与模型的双向追溯链（含 ReqIF / Simulink Requirements）

建模与重构层（Model Authoring）：

- `clm-control-law-pattern-author`
  按标准控制律结构（PID / LQR / 增益调度 / Anti-Windup / 抗饱和）输出建模骨架
- `clm-codegen-compliance-refactor`
  按高完整性建模规范与代码生成约束重构模型

代码生成与桥接层（Codegen Bridge）：

- `clm-embedded-coder-config-reviewer`
  审查 Embedded Coder 配置与代码生成诊断
- `clm-codegen-output-mapper`
  生成代码与手写桥接层（如 FMT 接口层）的映射梳理
- `clm-storage-class-governor`
  参数/信号/总线的存储类、命名、标定治理

验证层（Verification）：

- `clm-test-harness-builder`
  从需求到测试 harness 的落地（MIL / SIL）
- `clm-coverage-gap-analyzer`
  Decision / Condition / MCDC 覆盖率缺口分析
- `clm-pil-hil-replay-analyzer`
  PIL / HIL 数据回放与控制律性能基线对比

### 4.2 编排技能（Workflow Skill）

- `clm-control-law-mbd-pipeline`
  端到端编排：需求 → 模型解读 → 重构 → 代码生成 → 在环验证 → 部署交接

职责变化：

- 从“做所有事”改为“决定顺序、协调步骤、拼接结论”
- 优先引导使用原子技能
- 跨阶段结论必须引用上游工件（Artifact）

## 5. 原单体能力映射表

| 原能力块 | 新技能归属 | 说明 |
| --- | --- | --- |
| 模型层级与信号流解读 | `clm-simulink-model-reader` | 聚焦层级、子系统、采样时间一致性 |
| Stateflow 模式语义 | `clm-stateflow-semantics-reader` | 聚焦状态机执行顺序与事件 |
| 数据字典与参数对象 | `clm-data-dictionary-reader` | 聚焦 `.sldd` 与作用域/引用 |
| 需求追溯 | `clm-requirement-trace-reader` | 聚焦 ReqIF / Simulink Requirements |
| 控制律标准结构建模 | `clm-control-law-pattern-author` | 聚焦 PID/LQR/增益调度等模板 |
| 高完整性与代码生成重构 | `clm-codegen-compliance-refactor` | 聚焦 Model Advisor 落地 |
| Embedded Coder 配置审查 | `clm-embedded-coder-config-reviewer` | 聚焦代码生成配置诊断 |
| 生成代码与桥接层映射 | `clm-codegen-output-mapper` | 聚焦与手写代码契合点 |
| 存储类与标定治理 | `clm-storage-class-governor` | 聚焦命名/作用域/标定 |
| 测试 harness 构建 | `clm-test-harness-builder` | 聚焦从需求到 harness |
| 覆盖率缺口分析 | `clm-coverage-gap-analyzer` | 聚焦 Decision/Condition/MCDC |
| PIL/HIL 数据回放对比 | `clm-pil-hil-replay-analyzer` | 聚焦性能基线 |
| 全流程串联 | `clm-control-law-mbd-pipeline` | 编排与集成 |

## 6. 拆分后的收益

1. 触发更精准（每个 skill 描述更窄、工具上下文更明确）
2. 专业性更强（建模、代码生成、验证三段不互相稀释）
3. 与 `fmt/` 库形成稳定上下游：本库输出“模型侧 + 生成代码契约”，`fmt/` 输出“嵌入式集成 + 飞行验证”
4. 易于扩展：新增“频域设计 skill”、“故障注入测试 skill”不会污染现有 skill

## 7. 风险与控制

### 风险

- 技能数量较多，选择成本上升
- 模型层与代码生成层边界容易模糊（同一规则会被两个 skill 引用）
- 跨工具 skill 之间可能出现工件字段不一致

### 控制措施

1. 保留 `clm-control-law-mbd-pipeline` 作为统一入口
2. 在 `control-law-mbd/README.md` 维护技能分层与使用时机
3. 在每个 skill 中写清“输入 / 输出 / 不负责的部分 / 工具上下文”
4. 通过 `_meta/artifact-handoff-contract.md` 强制工件字段一致
5. 新增 skill 前对照 `_meta/repo-management.md` 决策“新增”还是“扩展”
