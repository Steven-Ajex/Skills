# Skills

个人 Codex Skills 仓库，用于管理和同步我自定义的可复用技能（skills），方便在不同主机之间迁移和安装。

## 目录结构

本仓库按“每个技能一个目录”组织，技能目录内通常包含：

- `SKILL.md`：技能定义与触发/执行说明（必需）
- `agents/openai.yaml`：UI 元数据（推荐）
- `references/`：参考模板、检查清单、领域资料（按需）
- `scripts/`：可复用脚本（按需）
- `assets/`：模板/资源文件（按需）
- `design/`：该技能的设计说明与决策记录（仓库内归档用途，可选）

## 当前技能

### `code-architecture-reader`

通用工程代码架构解读技能。用于辅助阅读项目代码并输出：

- 架构与模块边界说明
- 关键调用链/数据流分析
- 设计优点与缺点（带代码证据）
- 分优先级的改进建议

特性：

- 中文输出
- 专业术语首次出现附英文注释
- 默认深度版分析结构（含不确定项与需确认问题）

## 安装到 Codex（本地）

将技能目录复制到本机 Codex skills 路径（通常是 `~/.codex/skills/public/`）：

```powershell
Copy-Item -Recurse -Force .\code-architecture-reader $HOME\.codex\skills\public\
```

如果你的 Codex 使用其他 skills 根目录，请改为对应路径。

安装后建议重启 Codex，以确保新技能被识别。

## 在新机器上同步

1. 克隆本仓库
2. 将需要的技能目录复制到目标机器的 Codex skills 路径
3. 重启 Codex

示例：

```powershell
git clone https://github.com/Steven-Ajex/Skills.git
Copy-Item -Recurse -Force .\Skills\code-architecture-reader $HOME\.codex\skills\public\
```

## 维护约定

- 技能目录名使用小写字母和连字符（hyphen-case）
- 优先保持 `SKILL.md` 简洁，把模板和详细资料放到 `references/`
- 新增或修改技能后，建议运行校验脚本（如 `quick_validate.py`）
