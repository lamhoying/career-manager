# Career Manager — AI 职业经理人

> 把你的 AI 助手变成私人 Career Manager：以 **Career DNA（职业基因库）** 为唯一事实源，持续建设、管理、升级你的职业资产，而不是每次都从零改简历。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.5.3-green.svg)](CHANGELOG.md)

---

## 这是什么

Career Manager 是一个 **AI 助手技能包（Skill）**，可运行于 WorkBuddy、Claude Code、OpenAI Codex、Cursor 等多种支持自定义指令 / 技能的 agent 环境。它围绕一个核心思想设计：

> **Career DNA = 你职业经历、能力、项目、故事与成长轨迹的唯一事实源（Single Source of Truth）。简历只是 Career DNA 的一种输出形式。**

传统做法是「每次看到 JD 就重写一遍简历」，信息是碎片化的、不可复用的。本技能把职业资产沉淀成一个可持续演进的系统，简历 / 面试材料 / 岗位匹配报告都从同一个事实源自动派生。

---

## 跨平台兼容性

本技能只依赖两样东西，因此可在任意 AI 助手中复用：

- **纯文本指令**：`SKILL.md` + `references/*.md` 都是 Markdown，不含任何平台专属 API 调用。
- **标准库 Python**：`scripts/*.py` 仅使用 `os / sys / re / pathlib / shutil / datetime` 等 Python 标准库，可在任意装有 Python 3 的环境直接运行。

没有写死的平台私有 SDK，没有平台专属路径依赖。各 agent 的差异只在于「如何加载这段指令」和「如何触发」，技能的内容本身完全通用。

---

## 核心能力（四大工作模式）

| 模式 | 名称 | 作用 |
|------|------|------|
| **A** | Career DNA 构建 | 首次梳理经历，搭建个人职业基因库（`career-dna/`） |
| **B** | 职业资产更新 | 日常经历沉淀，把新项目 / 新能力增量写入 DNA |
| **C** | 职业发展分析 | 盘点能力短板、规划成长路径、做转型可行性分析 |
| **D** | 岗位投递 | 粘贴 JD → 生成匹配报告、中英文简历、面试包、缺口分析与补强路线 |

配套能力：

- **市场知识库（Knowledge Layer）**：Role Snapshot / Skill Snapshot，把 JD 里的市场信号沉淀为可复用的行业情报。
- **可解释匹配引擎**：JD 匹配度按 4 个维度量化（硬性要求 40% / 经验 30% / 能力 20% / 行业 10%），并给出匹配置信度拆解。
- **在线职业档案派生**：从 Career DNA 自动生成 Boss / 猎聘等平台的在线简历文案。

---

## 触发场景（对话里这样开口）

- 「帮我梳理一下这几年的工作经历」
- 「把我刚做完的 XX 项目加进职业档案」
- 「分析一下我适合往游戏技术 PM 方向转吗」
- 「这是一段 JD，帮我匹配并生成中英文简历和面试准备」
- 「我投这个岗位还差什么，给我一份补强计划」

只要在对话中提到「职业 / 简历 / 能力盘点 / 岗位匹配 / 面试准备」相关意图，技能即会被触发。

---

## 安装方式

### 方式一：WorkBuddy

```bash
git clone <本仓库地址> career-manager
cp -R career-manager ~/.workbuddy/skills/career-manager
```

重启 WorkBuddy 即可在任意对话中触发。

> 路径说明：
> - **macOS**：`~/.workbuddy/skills/career-manager/`
> - **Windows / Linux**：`%USERPROFILE%/.workbuddy/skills/career-manager/`（或 `~/.workbuddy/skills/career-manager/`）

### 方式二：Claude Code

Claude Code 同样以 `SKILL.md` 的 `name` / `description` 作为技能声明，可直接识别本技能包：

```bash
git clone <本仓库地址> career-manager
cp -R career-manager ~/.claude/skills/career-manager    # 用户级
# 或放到项目级：<你的项目>/.claude/skills/career-manager
```

### 方式三：OpenAI Codex / 通用 agent

Codex 等没有原生的「技能包」概念，两种用法皆可：

1. 把 `SKILL.md` 的核心流程与 `scripts/` 用法写入你的 `AGENTS.md`（或 system prompt），让 agent 在对话中按指令执行；
2. 直接在对话里粘贴 `SKILL.md` 内容作为上下文，脚本通过其 shell 工具运行。

### 方式四：Cursor / Windsurf / Cline

将 `SKILL.md` 转换为对应工具的 rule 文件（如 `.cursor/rules/career-manager.mdc`）或自定义 command，脚本照常通过其终端运行。

### 方式五：从 Release 安装

在仓库的 **Releases** 页面下载 `career-manager.zip`，解压后将 `career-manager/` 文件夹复制到对应 agent 的技能目录即可（各 agent 的目录见上方各方式）。

---

## 目录结构

```
career-manager/
├── SKILL.md                      # 技能入口与核心指令（必含）
├── LICENSE                       # MIT 许可证
├── CHANGELOG.md                  # 版本历史
├── README.md                     # 本文件
├── scripts/                      # 可执行脚本（确定性逻辑）
│   ├── init_career_dna.py        # 初始化 Career DNA 目录结构
│   └── completeness_checker.py   # 完整度评分检查
├── references/                   # 按需加载的详细参考文档
│   ├── career_dna_structure.md   # DNA 结构与字段说明
│   ├── mode_a_build.md           # 模式 A 流程
│   ├── mode_b_update.md          # 模式 B 流程
│   ├── mode_c_review.md          # 模式 C 流程
│   ├── mode_d_job_application.md # 模式 D 流程
│   ├── output_contracts.md       # 产物格式契约
│   ├── question_backlog.md       # 待澄清问题库
│   └── targeted_discovery.md     # 定向挖掘提问库
└── assets/templates/             # 输出用模板（不进 context）
    ├── career-dna/               # DNA 各模块模板（01~11）
    ├── knowledge/                # 市场知识库模板
    └── resume-outputs/           # 投递产物模板
```

> **隐私说明**：本技能只包含「指令 + 空白模板 + 脚本」，不含任何个人职业数据。你的真实 Career DNA、Knowledge、Resume Outputs 会在你本地工作区生成，不会随技能包外泄。

---

## 使用流程（首次）

1. 在任意支持的 AI 助手中开启一个新任务，说：「帮我构建 Career DNA」。
2. 技能会调用 `init_career_dna.py` 在当前工作区生成 `career-dna/`、`knowledge/`、`resume-outputs/` 目录。
3. 按引导逐步填写经历、项目、能力、故事。
4. 之后每次有新材料，用模式 B 增量更新；要投岗位时用模式 D。

---

## 兼容性说明

- 从本仓库克隆的版本 **不含** `agent_created` 标记（那是 WorkBuddy 专属的可管理标记，其他 agent 会忽略）。若你只用 WorkBuddy 并希望用内置 Skill 管理功能编辑此技能，可在 `SKILL.md` frontmatter 加回一行 `agent_created: true`。
- 所有 `references/*.md` 与 `assets/templates/*.md` 均为纯 Markdown，可直接被任意 agent 读取。
- 本仓库不含任何写死的绝对路径（除各 agent 的可选技能安装目录 `skills/` 外），无平台私有依赖。

---

## 版本与更新

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。当前版本 **v1.5.3**。

---

## License

[MIT](LICENSE) © 2026 The Career Manager Authors
