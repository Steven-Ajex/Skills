# FMT Skills Library

面向 `FMT-Firmware` / FMT 飞控开发场景的专用 Codex skills 集合。

设计目标：

1. 以最小能力单元（atomic capability）拆分技能，减少误触发和上下文污染
2. 通过组合（composition）形成完整工作流（如控制参数优化）
3. 让后续新增 FMT skills 可以按统一命名、目录和生命周期管理

## 目录组织

```text
fmt/
├─ README.md
├─ _meta/                 # 拆分分析、管理规则、路线图（非技能目录）
├─ code-reading/          # 代码理解类原子技能
├─ log-analysis/          # 日志解码/分段/分析/报告类原子技能
└─ workflows/             # 编排型技能（组合多个原子技能）
```

## 技能分层（当前版本）

### 1. Code Reading（代码理解）

- `fmt-control-loop-reader`
  负责主调度与闭环数据路径（sensor -> INS -> FMS -> Controller -> actuator）
- `fmt-mbd-interface-reader`
  负责接口桥接层与 MBD 生成代码分工、参数绑定、bus 映射
- `fmt-fms-state-machine-reader`
  负责 FMS 状态机/模式切换逻辑与输出语义
- `fmt-logging-pipeline-reader`
  负责 `mlog/ulog` 嵌入式日志记录链路

### 2. Log Analysis（日记/飞行日志分析）

- `fmt-mlog-decoder`
  负责 `mlog` 二进制日志头/消息流/schema 解码
- `fmt-flight-log-segmenter`
  负责飞行阶段分段与关键事件索引
- `fmt-control-performance-analyzer`
  负责控制表现与调参证据提取
- `fmt-tuning-report-writer`
  负责报告与试飞验证计划输出

### 3. Workflow（组合编排）

- `fmt-flight-control-param-optimizer`
  端到端编排技能。用于完整任务（代码理解 + 日志理解 + 分析 + 调参建议）。

## 使用建议（什么时候用原子技能 vs 编排技能）

优先使用原子技能：

- 你只需要解决一个子问题（例如只想看 FMS 状态机）
- 你已经有现成解码数据，只差性能分析
- 你希望减少上下文、提高回答准确性

使用编排技能：

- 你要从代码理解一路走到参数优化报告
- 你需要一个完整流程但不确定先从哪一步开始

## 安装方式（选择性安装）

复制你需要的单个技能目录到本机 Codex skills 路径（通常 `~/.codex/skills/public/`）：

```powershell
Copy-Item -Recurse -Force .\fmt\code-reading\fmt-control-loop-reader $HOME\.codex\skills\public\
```

或复制编排型技能：

```powershell
Copy-Item -Recurse -Force .\fmt\workflows\fmt-flight-control-param-optimizer $HOME\.codex\skills\public\
```

安装后重启 Codex。

## 后续扩展入口

新增 FMT skill 前先看：

- `fmt/_meta/split-analysis.md`
- `fmt/_meta/repo-management.md`
