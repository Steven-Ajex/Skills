---
name: clm-storage-class-governor
description: 在已有"字典对象清单 + 配置审查 + 模型对象 ↔ 生成代码映射"三类工件的基础上,做项目级的存储类(Storage Class)治理:逐对象给出治理决策(保持/调整/重命名/迁移)、命名一致性、标定可达性(Calibration Accessibility)、与桥接层接口约定(Linkage Contract)的合规性,产出 `storage_class_governance` 工件的专用决策类技能。用于"参数/信号/Bus"在跨模型/跨字典/跨生成代码中需要统一治理时;不负责审查 Embedded Coder 配置(转 `clm-embedded-coder-config-reviewer`)、不负责建立模型 ↔ 代码映射(转 `clm-codegen-output-mapper`)、不修改模型/字典/代码本身。
---

# Control-Law-MBD: Storage Class Governor

## 目标

把"字典里的对象 + 配置项倾向 + 生成代码实际形态"汇总成项目级的存储类治理建议,产出可被工程师直接采纳为治理改造单的 `storage_class_governance` 工件。本 skill 是**决策类**(Decision-Class)技能 — 它**不发现新事实**,而是基于上游事实做治理决策。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一项目范围内,基于上游字典/配置/映射工件,完成参数/信号/Bus 的存储类治理决策、命名一致性审查、标定可达性审查,产出 `storage_class_governance` 工件
2. 工具上下文(Tool Context)
   - 由上游工件的 `tool_context` 累加形成"治理对象的工具矩阵"
   - 公司级 / 项目级标定与命名规范(若提供)
   - 嵌入式侧约束(对接 FMT 接口层时的命名前缀 / 链接段)
   - 本 skill 不直接消费 Simulink 许可证,但建议在执行前确认上游工件的工具上下文一致
3. 核心输入(Inputs)
   - (强烈推荐)`clm-data-dictionary-reader` 的 `data_dictionary_map`
   - (强烈推荐)`clm-codegen-output-mapper` 的 `codegen_output_map`
   - (推荐)`clm-embedded-coder-config-reviewer` 的 `coder_config_review`
   - (可选)项目级标定与命名规范文档
   - (可选跨库)FMT 的 `mbd_boundary_map`(`fmt-mbd-interface-reader`)用于核对接口层期望
4. 核心输出(Outputs)
   - 主交付工件:`storage_class_governance`
   - 逐对象治理决策表(保持 / 调整 / 重命名 / 迁移作用域)
   - 命名一致性审查表
   - 标定可达性(Calibration Accessibility)审查表
   - 桥接层接口约定核对(Linkage Contract Audit)
   - 治理改造 backlog(优先级 + 影响 + 回归点)
5. 完成判据(Definition of Done, DoD)
   - 至少覆盖 `Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus` 三类对象
   - 每个待治理对象给出"当前 Storage Class + 当前命名 + 治理决策 + 期望 Storage Class + 期望命名 + 影响 + 回归点"
   - 命名前缀/后缀冲突已识别;跨字典命名冲突已结合作用域判定
   - 桥接层接口约定核对结论已声明(若提供 FMT `mbd_boundary_map`)
   - 工具上下文一致性已校验,冲突时阻断治理结论
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留对象名 / Storage Class 名 / 命名前缀-后缀 / 字典对象路径原文

## 聚焦范围(只做这些)

1. 项目级 Storage Class 治理决策(对每个对象:保持 / 调整 / 重命名 / 迁移作用域)
2. 命名一致性(前缀/后缀/全大写参数/驼峰信号 等)
3. 标定可达性(Calibration Accessibility:外部能否读写、能否在线标定)
4. 桥接层接口约定(链接段 / extern / volatile / 命名空间)
5. 改造 backlog 与回归点

## 不负责

1. 审查 Embedded Coder 配置 → 走 `clm-embedded-coder-config-reviewer`
2. 建立模型 ↔ 代码映射 → 走 `clm-codegen-output-mapper`
3. 解读字典对象本身 → 走 `clm-data-dictionary-reader`
4. 修改字典 / 模型 / 代码 → 走 `model-authoring/`
5. 真实的标定参数刷写(嵌入式侧实施)

## 推荐治理顺序

1. 先看"工具矩阵一致性" — 上游工件版本 / 形态不一致时阻断,要求上游对齐
2. 再看"项目级规范" — 若提供命名/存储类规范,以此为基线;否则采用通用建议并显式声明
3. 再看"对象级决策" — 先 Parameter,再 Signal,再 Bus(因为 Bus 影响多个 Parameter/Signal)
4. 再看"桥接层接口约定" — 若提供 FMT 端工件,核对接口期望是否被满足
5. 最后排序"改造 backlog" — 高风险/高影响优先

## 执行步骤

1. **校验工具矩阵**:对照上游工件 `tool_context`,Simulink/Coder 版本与字典形态一致;不一致时阻断治理结论
2. **基线选择**:若提供项目规范则采用之;否则声明采用"通用高完整性建议"
3. **逐对象决策**(Parameter / Signal / Bus):
   - 抽取当前 Storage Class、当前命名、生成代码侧实际全局变量
   - 决策枚举:`keep`(保持)/ `adjust`(调整 Storage Class)/ `rename`(重命名)/ `migrate`(迁移作用域:Top ↔ Reference Dictionary 等)
   - 每条决策给出"期望 + 影响 + 回归点"
4. **命名一致性**:
   - 前缀/后缀分组扫描
   - 跨字典同名对象结合作用域判定为"冲突 / 仅是同名 / 故意复用"
5. **标定可达性**:
   - `ImportedExtern` / `ExportedGlobal` 决定外部读写
   - 自定义 Storage Class(`Calibration` / `Tunable` 类)决定在线标定
   - 给出每个对象的可达性结论
6. **桥接层接口约定核对**(若提供 FMT `mbd_boundary_map`):
   - 接口层期望的链接段 / extern / 命名前缀
   - 与本治理决策的差异显式列出
7. **改造 backlog**:
   - 按优先级(高/中/低)+ 影响范围 + 回归点排序
   - 高风险项目(影响多个 ECU 接口或破坏标定流程)单独标记
8. **生成工件**:按 `references/output-template.md` 填充 `storage_class_governance`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具矩阵一致性结论
2. 治理基线声明(项目规范 / 通用高完整性建议)
3. 逐对象决策表(三类对象)
4. 命名一致性审查表
5. 标定可达性审查表
6. 桥接层接口约定核对(若适用)
7. 改造 backlog(优先级 / 影响 / 回归点)
8. 关键事实(Facts)、关键推断(Inferences)
9. 证据索引(对象路径 + 上游工件回引)
10. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - (强烈推荐)`data_dictionary_map`
   - (强烈推荐)`codegen_output_map`
   - (推荐)`coder_config_review`
   - (可选)项目级规范文档
   - (跨库可选)FMT `mbd_boundary_map`
2. 下游使用方
   - `clm-codegen-compliance-refactor`(消费改造 backlog 作为重构 PR 输入)
   - `clm-control-law-mbd-pipeline`(编排技能)
   - `fmt-mbd-interface-reader`(跨库:核对接口层契合)
3. 主交付工件
   - `storage_class_governance`
   - 字段:`tool_context`(汇总自上游)、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`naming_and_storage_class_table`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不审查配置 / 不建立映射 / 不解读字典 / 不修改任何文件
   - 证据门禁:每条治理决策给出"上游工件回引(`data_dictionary_map` 段 + `codegen_output_map` 段)"
   - 工具矩阵一致性:上游 `tool_context` 不一致时阻断,不给治理结论
   - 决策完整性:每条决策必须含 `keep/adjust/rename/migrate` + 期望 + 影响 + 回归点
   - 基线显式:治理基线(项目规范 / 通用建议)必须显式声明
   - 桥接纪律:若涉及 FMT,接口层期望与治理决策的差异必须显式列出
   - 交接门禁:工件可被 `clm-codegen-compliance-refactor` 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供 `data_dictionary_map`**:本 skill 阻断;提示先运行 `clm-data-dictionary-reader`
   - **未提供 `codegen_output_map`**:本 skill 阻断或降级为"模型侧决策预案"(标注未与生成代码核对,置信度低)
   - **上游 `tool_context` 不一致**:阻断治理决策;先要求上游对齐
   - **未提供项目规范**:声明采用"通用高完整性建议"作为基线
   - **未提供 FMT 工件**:跳过桥接层核对章节;在 `gaps` 中登记
2. 输出降级要求
   - 降级输出必须显式标注受影响决策与置信度变化
   - 降级不等于跳步;不得越过本技能职责直接给"已可执行改造"的结论 — 需 `clm-codegen-compliance-refactor` 接力

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,逐对象决策表与改造 backlog 直接套用
2. 交付前用 `references/checklist.md` 复核决策完整性、桥接纪律、降级策略
3. 大型项目:先输出"工具矩阵 + 基线声明 + 桥接纪律小结",再分批输出对象级决策

## 治理纪律

1. 不做"应该改成 X"式的孤立建议 — 每条决策必须含影响与回归点
2. 不在没有 `codegen_output_map` 的情况下给"会破坏代码生成"的强结论
3. 不假设"项目规范一定可行" — 与现状冲突时优先标注,由工程师决断
4. 不替代 `clm-codegen-compliance-refactor` 的"模型层重构"职责 — 本 skill 输出 backlog,执行者另选
5. 跨库交接时,接口层期望(FMT 端)与本库治理决策的差异显式列出,不擅自调和
