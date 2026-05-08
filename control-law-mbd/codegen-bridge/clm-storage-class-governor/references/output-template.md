# clm-storage-class-governor 输出模板

## 使用说明

- 目标:输出项目级存储类治理决策、命名一致性审查、标定可达性审查与改造 backlog
- 主交付工件(Primary Artifact):`storage_class_governance`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 是**决策类**技能 — 不发现新事实,基于上游工件做治理决策

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-storage-class-governor`
- `artifact_name`:`storage_class_governance`
- `tool_context`(汇总自上游):
  - Simulink 版本:
  - Embedded Coder 版本:
  - 字典形态:
  - 项目规范来源(公司规范 / 通用建议):
- `scope`(模型路径 + 字典路径 + 生成代码目录):
- `version_or_branch`:

## 上游工件回引(Upstream Artifacts)

- `data_dictionary_map`:`<artifact_id 或文件路径>`
- `codegen_output_map`:`<artifact_id 或文件路径>`
- `coder_config_review`(若有):
- 项目规范文档(若有):
- FMT `mbd_boundary_map`(若涉及跨库):

## 工具矩阵一致性结论

| 维度 | 来源工件 | 值 | 一致性结论 |
| --- | --- | --- | --- |
| Simulink 版本 |  |  |  |
| Embedded Coder 版本 |  |  |  |
| 字典形态 |  |  |  |
| 模型 vs 代码时间戳 |  |  |  |

总结:`一致(继续治理)` / `冲突(阻断治理决策,要求上游对齐)`

## 治理基线声明

- 基线类型:`公司规范 vYY.MM` / `项目规范 <文档名>` / `通用高完整性建议`
- 关键条款:

## 工件正文(Artifact Body)

### 1. 逐对象治理决策 — Parameter

| 对象名 | 当前 Storage Class | 当前命名 | 决策 | 期望 Storage Class | 期望命名 | 影响范围 | 回归点 | 上游证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | keep / adjust / rename / migrate |  |  |  |  | `data_dictionary_map > Design Data > <obj>`;`codegen_output_map > <file:line>` |

### 2. 逐对象治理决策 — Signal

| 对象名 | 当前 Storage Class | 当前命名 | 决策 | 期望 | 影响 | 回归点 | 上游证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

### 3. 逐对象治理决策 — Bus

| 对象名 | 当前命名 | 字段一致性 | 决策 | 期望 | 影响 | 回归点 | 上游证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

### 4. 命名一致性审查(Naming Consistency)

| 命名分组(前缀/后缀) | 期望规则 | 违例对象 | 违例数量 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

跨字典同名审查:

| 同名对象 | 字典 A 作用域 | 字典 B 作用域 | 判定(冲突 / 仅同名 / 故意复用) | 处置 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 5. 标定可达性审查(Calibration Accessibility)

| 对象名 | 外部读写 | 在线标定 | 期望 | 不一致? | 处置 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 6. 桥接层接口约定核对(若涉及 FMT)

| 接口期望项 | FMT 端值(`mbd_boundary_map`) | 本治理决策值 | 一致? | 差异处理 |
| --- | --- | --- | --- | --- |
| 链接段(Linkage Section) |  |  |  |  |
| extern / volatile 修饰 |  |  |  |  |
| 命名前缀 |  |  |  |  |
| 命名空间 |  |  |  |  |

### 7. 改造 backlog(Refactor Backlog)

| ID | 描述 | 关联对象 | 优先级 | 影响范围 | 回归点 | 高风险标记 | 接收 skill |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RF-001 |  |  | 高 |  |  | 是 / 否 | `clm-codegen-compliance-refactor` |
| RF-002 |  |  | 中 |  |  |  | `clm-codegen-compliance-refactor` |
| RF-003 |  |  | 低 |  |  |  |  |

高风险项目说明:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 字典证据:`data_dictionary_map > Parameter > Kp_att` → 当前 Storage Class = ExportedGlobal
- 代码证据:`codegen_output_map > controller_data.c:42` → 当前命名 = `Kp_att`
- FMT 接口期望(若有):`mbd_boundary_map > AttitudeCtrl.linkage` → extern + 命名前缀 `clm_`

## 缺口与风险(Gaps & Risks)

- 缺口(例:上游工件缺失 / 工具矩阵冲突 / 项目规范缺失):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-codegen-compliance-refactor`(关注:改造 backlog 高优先级条目)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
  - `fmt-mbd-interface-reader`(跨库:接口期望差异,需要嵌入式侧确认)
- 建议关注的对象 / backlog ID:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未审查配置 / 未建立映射 / 未解读字典 / 未修改文件
- [ ] 证据可追溯:每条决策给出上游工件回引
- [ ] 工具矩阵一致性:无冲突或已阻断
- [ ] 决策完整性:四类决策 + 期望 + 影响 + 回归点
- [ ] 基线显式
- [ ] 桥接纪律:差异显式列出
- [ ] 交接可用性:下游 skill 可直接消费
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
