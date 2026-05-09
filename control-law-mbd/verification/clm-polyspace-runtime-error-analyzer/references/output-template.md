# clm-polyspace-runtime-error-analyzer 输出模板

## 使用说明

- 目标:解读 Polyspace 报告 + 模型侧根因反推 + 闭环路由
- 主交付工件(Primary Artifact):`polyspace_runtime_error_findings`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不运行 Polyspace / 不修改代码或模型 / 不替代 code review

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-polyspace-runtime-error-analyzer`
- `artifact_name`:`polyspace_runtime_error_findings`
- `tool_context`:
  - Polyspace 版本(Code Prover / Bug Finder / 联用):
  - 报告形态:
  - 启用规则集:
  - 目标硬件(Word Length / Endianness):
  - 是否启用并发分析:
  - 许可证可用性:
- `scope`(Polyspace 报告路径 + 生成代码目录):
- `version_or_branch`:

## 上游工件回引(Upstream Artifacts)

- `codegen_output_map`(强烈推荐):
- `simulink_model_map`(推荐):
- `data_dictionary_map`(推荐):
- `fixed_point_refactor_plan`(若涉及):
- `storage_class_governance`(若涉及):
- `sldv_property_set`(若涉及):

## 工件正文(Artifact Body)

### 1. 严重度分布(Severity Distribution)

| 严重度 | 数量 | 已分析比例 % | 备注 |
| --- | --- | --- | --- |
| Red(已证有错) |  |  | 必须逐条分析 |
| Orange(可能有错) |  |  | 视项目特异性筛选(标准已声明) |
| Green(已证无错) |  |  | 视情况覆盖 |
| Gray(不可达 / 不适用) |  |  | 视情况覆盖 |

错误类型分布:

| 类型 | 数量 | 关键条目 ID |
| --- | --- | --- |
| Overflow |  |  |
| Divide-by-Zero |  |  |
| Out-of-Bounds Array (OOB) |  |  |
| Uninitialized Variable |  |  |
| Dead Code |  |  |
| Concurrency / Race Condition |  |  |
| 其他 |  |  |

### 2. 错误清单(Finding Table,主表)

| Finding ID | 类型 | 严重度 | 代码位置(文件:行号) | 涉及函数 / 变量 | 模型侧根因(经 codegen_output_map) | 闭环路由 | 关联 skill |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PSF-001 | Overflow | Red | `controller_data.c:42` | `Kp_att * err` | 模型 `Controller/AttitudeLoop/P`,Kp_att 类型上限不足 | refactor-model | `clm-fixed-point-refactor` |
| PSF-002 | Divide-by-Zero | Orange | `controller.c:128` | `1/denom` | `denom` 范围未约束;模型层未加保护 | refactor-model + adjust-config(诊断等级) | `clm-codegen-compliance-refactor` |
| PSF-003 | OOB | Red | `lookup.c:55` | `LUT[idx]` | 索引信号未限幅;模型层 saturation 缺失 | refactor-model | `clm-codegen-compliance-refactor` |
| PSF-004 | Dead Code | Orange | `controller.c:201` | 互斥分支 | 已知 unreachable(条件互斥) | accept-residual | DV 评审签字 |
| PSF-005 | Concurrency | Orange | `globals.c:18` | 全局变量 | 任务调度互斥未保证;`out-of-mbd-scope` (RTOS 配置) | out-of-mbd-scope | 配置管理审批 |

闭环路由枚举:`refactor-model` / `adjust-config` / `accept-residual` / `out-of-mbd-scope`

### 3. 模型侧根因反推汇总(Root Cause Inference)

| 根因类别 | 涉及 finding 数 | 关联模型对象 | 转交建议 |
| --- | --- | --- | --- |
| 类型/范围不严(数据字典) |  | `data_dictionary_map > Parameter > Kp_att` | `clm-storage-class-governor` + `clm-codegen-compliance-refactor` |
| 模型层缺少保护(saturation / 限幅) |  | `Controller/AttitudeLoop` | `clm-codegen-compliance-refactor` |
| 配置过松(诊断等级) |  | `coder_config_review > Diagnostics` | `clm-embedded-coder-config-reviewer` |
| 定点形态溢出 |  | 待 Q 格式重审 | `clm-fixed-point-refactor` |
| 不可达分支(已知互斥) |  | 文档化即可 | accept-residual |
| MBD 范围外(RTOS / 链接) |  | — | 配置管理审批 |

### 4. 闭环路由汇总(Closure Routing)

| 路由 | finding 数 | 备注 |
| --- | --- | --- |
| refactor-model |  | 转 `clm-codegen-compliance-refactor` 主入口 |
| adjust-config |  | 转 `clm-embedded-coder-config-reviewer` 后续动作 |
| accept-residual |  | 文档化 + 评审签字 |
| out-of-mbd-scope |  | 需配置管理审批,MBD 项目慎用 |

`accept-residual` 独立清单:

| Finding ID | 接受理由 | 文档位置 | 评审签字环节 | 复核条件 |
| --- | --- | --- | --- | --- |
| PSF-004 | 条件互斥代码 | DV-2026Q1 | DV 评审 | 模型重构后再评估 |

`out-of-mbd-scope` 独立清单:

| Finding ID | 转交对象 | 审批要求 | 备注 |
| --- | --- | --- | --- |
| PSF-005 | 嵌入式集成团队 + RTOS 配置 | 配置管理审批 | RTOS 任务调度互斥配置 |

### 5. Polyspace 设置审查(Settings Audit)

| 维度 | 当前设置 | 期望 | 判断 | 依据 |
| --- | --- | --- | --- | --- |
| Code Prover / Bug Finder 启用 |  |  | 适中 / 过严 / 过松 |  |
| MISRA C 子集 |  |  |  |  |
| CWE / CERT C 启用 |  |  |  |  |
| 并发分析 |  |  |  |  |
| Stub 模型(Library / OS) |  |  |  |  |

误报 / 漏检 风险:

项目特异性建议:

### 6. 与其他 skill 的关联(Cross-Skill Associations)

| 关联 skill | 共同关注点 | 印证 / 纠正 / 互补 |
| --- | --- | --- |
| `clm-fixed-point-refactor` | 定点 Overflow | 互补 — 重构在前,Polyspace 验证在后 |
| `clm-storage-class-governor` | 存储类访问越界 | 互补 — 治理决策影响代码访问模式 |
| `clm-sldv-property-author` | 控制量在范围(P-CTL-01) | 印证 / 纠正 — Polyspace finding 与 SLDV 属性同关注点,反例可对照 |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 报告证据:`polyspace_report.html#PSF-001` → 严重度 + 类型
- 代码证据:`controller_data.c:42` → 涉及变量
- 模型证据:`codegen_output_map > controller_data.c:42 Kp_att` → 模型对象 → 字典对象

## 缺口与风险(Gaps & Risks)

- 缺口(例:报告形态未识别 / `codegen_output_map` 缺失 / 目标硬件未确认):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-codegen-compliance-refactor`(消费 `refactor-model` 路由)
  - `clm-embedded-coder-config-reviewer`(消费 `adjust-config` 路由)
  - `clm-fixed-point-refactor`(若涉及定点 Overflow)
  - `clm-storage-class-governor`(若涉及访问越界)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的 finding ID / 路由 / 模型对象:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未运行 Polyspace / 未改文件 / 未替代 code review / 未解释 MISRA 规则
- [ ] 严重度纪律:Red + Orange 已覆盖
- [ ] 反推纪律:经 `codegen_output_map` 中转或降级标识
- [ ] 闭环路由纪律:四枚举之一,审批要求显式
- [ ] 设置审查纪律:严格度判断有依据
- [ ] 工具上下文显式
- [ ] 没有给"已通过 Polyspace 门"结论

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
