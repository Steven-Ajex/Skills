# clm-embedded-coder-config-reviewer 输出模板

## 使用说明

- 目标:输出 Embedded Coder 配置集的逐项审查结果,支持下游 `codegen-bridge/` 内其他 skill 与跨库 `fmt-mbd-interface-reader` 引用
- 主交付工件(Primary Artifact):`coder_config_review`
- 默认中文输出;专业术语首次出现附英文注释(English Annotation)

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-embedded-coder-config-reviewer`
- `artifact_name`:`coder_config_review`
- `tool_context`:
  - Embedded Coder / Simulink Coder 版本:
  - 目标硬件(Word Length、Endianness、Atomic Sizes):
  - 求解器(Type、Step Size、Tasking Mode):
  - 是否启用 SIL/PIL:
  - 代码替换库(Code Replacement Library):
  - 许可证可用性:
- `scope`(模型路径 / ConfigSet 名称):
- `version_or_branch`:
- 期望基线来源(公司规范 / 高完整性建议 / 自定义):

## 范围与假设(Scope & Assumptions)

- [ ] 目标 ConfigSet 已确定
- [ ] 期望基线已声明
- [ ] 是否参与生成代码交叉验证
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 模型路径
- [ ] ConfigSet 名称
- [ ] 期望基线文档(若有)
- [ ] (可选)生成代码目录
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. Code Interface(代码接口)

| 配置项 | 当前值 | 期望值 | 风险(高/中/低) | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Function Packaging |  |  |  |  |  |  |
| Step Function 形态 |  |  |  |  |  |  |
| Reentrant |  |  |  |  |  |  |
| I/O Args 风格 |  |  |  |  |  |  |

### 2. Storage Class(存储类)

| 配置项 | 当前值 | 期望值 | 风险 | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Default Parameter Behavior |  |  |  |  |  |  |
| Default Storage Class |  |  |  |  |  |  |
| Inlined Parameters |  |  |  |  |  |  |
| Custom Storage Class |  |  |  |  |  |  |

### 3. Hardware Implementation(目标硬件)

| 配置项 | 当前值 | 期望值 | 风险 | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Word Length |  |  |  |  |  |  |
| Endianness |  |  |  |  |  |  |
| Atomic Integer / Float Size |  |  |  |  |  |  |

### 4. Solver(求解器)

| 配置项 | 当前值 | 期望值 | 风险 | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Type |  |  |  |  |  |  |
| Step Size |  |  |  |  |  |  |
| Tasking Mode(SingleTasking / MultiTasking) |  |  |  |  |  |  |

### 5. Optimization(优化)

| 配置项 | 当前值 | 期望值 | 风险 | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Reusable Subsystems |  |  |  |  |  |  |
| Pass-by Pointer |  |  |  |  |  |  |
| Loop Unrolling |  |  |  |  |  |  |
| Conditional Input Branch Execution |  |  |  |  |  |  |

### 6. Report & Diagnostics(报告与诊断)

| 配置项 | 当前值 | 期望值 | 风险 | 影响 | 修复路径 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- |
| Generation Report |  |  |  |  |  |  |
| Code Replacement Library |  |  |  |  |  |  |
| MISRA / AUTOSAR(如适用) |  |  |  |  |  |  |
| 代码生成 Diagnostic 等级 |  |  |  |  |  |  |

### 7. 关键标记小结

- Step Function 形态(单 step / 多 rate / model_step、model_step0 / model_step1):
- 是否 Reentrant:
- 文件打包形态(Single file / 模块化分文件 / 共享 utility 文件):
- 是否生成 Makefile / 仅生成代码:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 配置项证据:`get_param('<model>', 'RTWGenerateMakefile')` → 当前值:'on'
- 配置项证据:`configSet.xml > Solver/SolverType` → 当前值:'Fixed-step'

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / 期望基线未提供 / 目标硬件未确认 / 多 ConfigSet 未指定):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-codegen-output-mapper`(关注:Step Function 形态 + 文件打包形态 + 存储类策略)
  - `clm-storage-class-governor`(关注:Default Storage Class、Inlined Parameters、Custom Storage Class 现状)
  - `clm-codegen-compliance-refactor`(关注:模型层重构 backlog)
  - `fmt-mbd-interface-reader`(跨库:Step Function 形态 + 文件打包形态对接 FMT 接口层)
- 建议关注的配置项 / 子系统 / 信号:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度(Boundary Purity):未越权下"生成代码不合规"或全局治理结论
- [ ] 证据可追溯(Evidence Traceability):每条结论给出配置项原名 + 来源
- [ ] 工具上下文显式(Tool Context Explicitness):版本 / 目标硬件 / 求解器 / 许可证已记录
- [ ] 风险标注(Risk Discipline):每条偏差有风险等级 + 影响维度
- [ ] 交接可用性(Handoff Usability):下游 skill 可直接使用本输出
- [ ] 失败/降级说明完整:输入缺口、受影响结论、置信度变化已标注

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
