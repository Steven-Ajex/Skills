# clm-fixed-point-refactor 输出模板

## 使用说明

- 目标:输出浮点 → 定点重构方案 — 逐信号/逐参数 Q 格式、风险登记、AW 调整、验证步骤
- 主交付工件(Primary Artifact):`fixed_point_refactor_plan`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不直接改模型;不采集数值范围数据(消费已采到的)

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-fixed-point-refactor`
- `artifact_name`:`fixed_point_refactor_plan`
- `tool_context`:
  - Fixed-Point Designer 版本:
  - 目标硬件(Word Length / Endianness / Atomic Sizes):
  - 舍入模式(Floor / Round / Nearest):
  - 饱和模式(Saturate / Wrap):
  - 是否使用 Code Replacement Library:
  - 数值范围数据来源 + 覆盖度:
- `scope`(浮点模型路径 + 关注子系统):
- `version_or_branch`:

## 数值范围数据评审(Range Data Review)

| 信号 / 参数 | min | max | typical | 来源 | 覆盖度 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

总体覆盖度结论:

## 工件正文(Artifact Body)

### 1. 参数 Q 格式表(Static Parameters)

| 参数名 | 当前类型(浮点) | 数值范围 | 期望 Q 格式 | Word Length | Fraction Length | Signed | 选型理由 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Kp` | double | [0, 100] | `fixdt(1,16,8)` | 16 | 8 | 是 | 范围 < 256, 精度 1/256 |
| `Ki` | double | [0, 50] |  |  |  |  |  |
| `Kt` | double | [0.5/Kp, 2/Kp] |  |  |  |  | AW 跟踪增益,Kt < 1 须保 FL |

### 2. 信号 Q 格式表(Dynamic Signals)

| 信号名 | 来源 Block | 数值范围 | 期望 Q 格式 | Word Length | Fraction Length | Signed | 选型理由 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

反馈环路 Q 格式迭代记录:

| 环路 | 第 1 次 | 第 2 次 | 是否收敛 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 3. 溢出 / 饱和 / 量化风险登记

| 信号 / 参数 | 风险类型 | 等级(高/中/低) | 触发工况 | 缓解方案(增 WL / 加饱和 / 重缩放) | 备注 |
| --- | --- | --- | --- | --- | --- |
|  | 溢出 |  |  |  |  |
|  | 饱和漂移 |  |  |  |  |
|  | 量化误差(对截止频率) |  |  |  |  |
|  | 量化误差(对积分增益) |  |  |  |  |

量化误差对性能指标的估计:

| 性能指标 | 浮点 | 定点(估计) | 偏差 | 是否可接受 |
| --- | --- | --- | --- | --- |
| 零点 |  |  |  |  |
| 截止频率 |  |  |  |  |
| 积分增益 |  |  |  |  |

### 4. AW 定点调整(若涉及积分器)

- 上游 AW 设计参考:`anti_windup_design > <段>` 或 `control_law_pattern_skeleton > Anti-Windup`
- Kt 的 Q 格式:
- Kt < 1 时 Fraction Length 检查:
- 积分项保留位:
- 浮点 AW 假设下的推导是否仍成立:`是` / `否(需重新评估)`

### 5. 滤波器定点化(若涉及)

- IIR 滤波零点漂移评估:
- SOS 分解建议:
- FIR 直接形式系数量化:
- Levin 形式选用:

### 6. 缩放与规范化建议(Scaling & Normalization)

| 信号 | 当前范围 | 建议预缩放 | 输出恢复 | 收益 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 7. 验证步骤(Validation Steps)

1. **浮点 ↔ 定点对比仿真**:
   - 输入:相同激励(从 `test_harness_plan` 选取关键用例)
   - 比较:输出信号容差 ≤ 设定阈值
   - 阈值:
2. **覆盖率重做**:
   - 工具:Simulink Coverage / SLDV
   - 转交 `clm-coverage-gap-analyzer`
3. **PIL 验证**:
   - 平台:
   - 转交 `clm-pil-hil-replay-analyzer`
4. **回归点**:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 模型证据:`simulink_model_map > <信号路径>` → 当前类型
- 字典证据:`data_dictionary_map > Parameter > <name>` → 现状
- 范围数据:`<浮点仿真 / 飞行日志路径>` → min / max

## 缺口与风险(Gaps & Risks)

- 缺口(例:范围数据覆盖度低 / 目标硬件 Word Length 未定 / 字典未提供):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / 评审(直接施工)
  - `clm-codegen-compliance-refactor`(关注:风险登记 + backlog)
  - `clm-codegen-output-mapper`(定点改造后重新生成代码,核对类型映射)
  - `clm-test-harness-builder`(关注:浮点 ↔ 定点对比测试场景)
  - `clm-coverage-gap-analyzer`(关注:覆盖率重做)
  - `clm-pil-hil-replay-analyzer`(关注:PIL 验证)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的信号 / 参数 / 风险项:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未直接改模型 / 未采集范围 / 未重做 pattern / 未重做 AW
- [ ] 数值范围纪律:每条 Q 格式有依据
- [ ] Q 格式完整性:WL + FL + Signed + 表达原文
- [ ] 风险纪律:每条溢出风险有缓解方案
- [ ] AW 定点纪律:Kt 量化 + 积分位保留(若涉及)
- [ ] 验证纪律:浮点 ↔ 定点对比仿真
- [ ] 工具上下文显式
- [ ] 交接可用性

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
