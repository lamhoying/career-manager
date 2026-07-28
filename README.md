# Career Manager — AI 职业经理人

> 把你的 AI 助手变成私人 Career Manager：以 **Career DNA（职业基因库）** 为唯一事实源，持续建设、管理、升级你的职业资产，而不是每次看到 JD 都从零重写简历。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.6.3-green.svg)](CHANGELOG.md)
[![Cross-Agent](https://img.shields.io/badge/agent-agnostic-brightgreen.svg)](#跨平台兼容性)

---

## 为什么需要它

大多数人的职业资产是**碎片化、不可复用**的：

- 每次看到心仪 JD，就在旧简历上东改西改，改完就忘；
- 投递十几次，每段经历被讲成十几个互相矛盾的版本；
- 想转行 / 晋升时，说不清自己「到底会什么、凭什么适合」；
- 面试被追问细节就露怯，因为故事从没被认真沉淀过。

Career Manager 不帮你「美化一份简历」，而是帮你建立一个**可持续演进的职业资产系统**。简历、面试材料、岗位匹配报告，都从同一个事实源（Career DNA）自动派生——你只维护一次，到处复用。

---

## 这是什么

Career Manager 是一个 **AI 助手技能包（Skill）**，可运行于 WorkBuddy、Claude Code、OpenAI Codex、Cursor 等多种支持自定义指令 / 技能的 agent 环境。它围绕一个核心思想设计：

> **Career DNA = 你职业经历、能力、项目、故事与成长轨迹的唯一事实源（Single Source of Truth）。简历只是 Career DNA 的一种输出形式。**

传统做法是「每次看到 JD 就重写一遍简历」，信息是碎片化的、不可复用的。本技能把职业资产沉淀成一个可持续演进的系统：

```
你真实做过的事 ──写入──▶ Career DNA（事实源）
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
       中文 / 英文简历    JD 匹配报告    面试包 / 回答卡片
       在线档案(Boss等)   缺口分析/补强    转岗可行性评估
```

---

## 三层架构

v1.3 起职责收敛为清晰的三层，彻底分离「个人资产 / 市场情报 / 单次产物」：

| 层 | 定位 | 回答的问题 | 内容 | 更新来源 |
|----|------|-----------|------|----------|
| **Career DNA**（个人资产层） | 你的唯一事实源 | 我做过什么、为什么适合某方向 | 经历 / 能力 / 项目 / 故事 / Career Track | 你提供 |
| **Knowledge**（市场知识层） | 外部市场情报 | 市场需要什么、趋势是什么 | Role Snapshot、Skill Domain Snapshot | JD 分析累积 |
| **Resume Outputs**（投递产物层） | 单次 JD 临时产物 | 这次 JD 我准备了什么 | 匹配报告 / 简历 / 面试包 | 每次 JD 生成 |

关键规则：Career DNA 是**个人资产**，Knowledge 是**市场资产**，Resume Outputs 是**临时产物**；Career Track 回答「你适合什么」，Role Snapshot 回答「市场要什么」——两者不再重叠。每次投递单建子目录（`{日期}-{公司}-{岗位}/`），不覆盖历史记录。

---

## 核心原则

1. **Career DNA First（资产优先）**：Career DNA 永远优先于简历。先确保职业资产充足，再生成简历，不要一上来就优化排版。
2. **Evidence Driven（证据驱动）**：所有能力必须有证据支持。禁止虚构经历、夸大职责、编造项目。每项能力必须能回答：来自哪个项目？有什么证据？面试官追问时如何证明？
3. **Build Before Optimize（先建库再优化）**：资产不足时先补充，再产出。
4. **Career DNA Evolves（持续成长）**：不是一次性工程。每次新项目、新岗位、新 JD 都可能更新 DNA。
5. **Unknown → Backlog（未知进待补充池）**：信息不足不猜测，写入 Question Backlog，等待未来补充；禁止长时间连续追问。
6. **Knowledge Accumulates（知识累积）**：每次 JD 分析都提取市场信号写入 Knowledge Layer，随投递次数增长，反哺后续匹配。

---

## 四大工作模式

技能根据用户目标自动路由（先检查当前目录是否存在 `career-dna/`，再决定模式）：

| 模式 | 名称 | 触发场景 | 产出 |
|------|------|----------|------|
| **A** | **Career DNA 构建** | 首次梳理经历 / 盘点能力 / 分析职业方向 | 完整个人职业基因库（`career-dna/`） |
| **B** | **职业资产更新** | 补充新项目 / 新能力 / 回答 Backlog 问题 | DNA 增量更新，不重复建设 |
| **C** | **职业发展分析** | 我适合什么岗位 / 该不该转型 / 竞争力在哪 / 缺什么 | 能力盘点、成长路径、转型可行性 |
| **D** | **岗位投递** | 粘贴 JD / 招聘链接 / 岗位要求 | 匹配报告、中英简历、面试包、缺口分析与补强路线 |

---

## 关键能力

- **可解释匹配引擎（Explainable Match Engine）**：JD 匹配度按 4 个维度量化——
  - 硬性要求 **40%** / 经验 **30%** / 能力映射 **20%** / 行业 **10%**
  - 并给出**匹配置信度拆解**（Count Quality / Quality / Consistency / Recency 四维）与证据来源，而非黑盒打分。
- **证据强度（Evidence Strength）**：每条证据按 5 维度评分（Ownership / Scope / Impact / Recency / Relevance），总分映射到 Strength 0–5，决定它该写进**主简历**、放进**面试包**，还是仅作**内部参考**——杜绝「什么都敢往简历上写」。
- **职业决策引擎（Career Decision Engine）**：用 Evidence Distance（D0–D4）、Role Authenticity（A–D）、Recruiter Risk Funnel 与 Decision Score，把「该不该投这个岗位」变成可解释的判断，而非拍脑袋。
- **市场知识库（Knowledge Layer）**：Role Snapshot / Skill Snapshot 把 JD 里的市场信号沉淀为可复用行业情报，越投越准。
- **在线职业档案派生**：从 Career DNA 自动生成 Boss / 猎聘等平台的在线简历文案（`11_online_profile.md`）。
- **能力迁移翻译（Capability Translation）**：把你的经历映射到目标岗位要求，区分 Direct / Adjacent / Missing 三类，禁止编造不存在的匹配。
- **岗位沟通产物生成（Outreach / Boss Greeting Generation）**：由匹配报告驱动的 JD 级即时沟通文案，不只是简历。核心是一套**决策 + 人味化**管线——
  - **打招呼目标（Greeting Objective）**：按岗位与匹配度选 Type A 建联 / Type B 证明价值 / Type C 化解顾虑 / Type D 激发好奇，不同目标对应不同结尾策略；
  - **证据路由（Evidence Routing）**：从 Strength≥4 的证据池按「距离优先 / 角色相关 / 新奇注入」三条规则分层为 Primary / Secondary / Curiosity，杜绝把 AI 项目误选为 PM 岗位钩子；
  - **平台策略（Platform Variants）**：同一匹配结论在 Boss 直聘（诱导 HR 回复，60–120 字）、猎聘（建立专业感，150–250 字）、邮件（正式投递，300+ 字附简历）、LinkedIn（建立关系，80–120 字不提求职）四平台各自生成不同目标版本；
  - **人味化（Humanization）**：7 条规则（短句 / 不用 AI 词 / 自然问句 / 不堆材料 / 不模板开头等）让文案更像真人；每平台仅出「推荐 + 备选」两个版本，附 Why / Tone Notes / Do Not Say。

---

## 触发场景（对话里这样开口）

- 「帮我梳理一下这几年的工作经历」
- 「把我刚做完的 XX 项目加进职业档案」
- 「分析一下我适合往游戏技术 PM 方向转吗」
- 「这是一段 JD，帮我匹配并生成中英文简历和面试准备」
- 「我投这个岗位还差什么，给我一份补强计划」

只要在对话中提到「职业 / 简历 / 能力盘点 / 岗位匹配 / 面试准备」相关意图，技能即会被触发。

---

## 跨平台兼容性

本技能只依赖两样东西，因此可在任意 AI 助手中复用：

- **纯文本指令**：`SKILL.md` + `references/*.md` 都是 Markdown，不含任何平台专属 API 调用。
- **标准库 Python**：`scripts/*.py` 仅使用 `os / sys / re / pathlib / shutil / datetime` 等 Python 标准库，可在任意装有 Python 3 的环境直接运行。

没有写死的平台私有 SDK，没有平台专属路径依赖。各 agent 的差异只在于「如何加载这段指令」和「如何触发」，技能的内容本身完全通用。

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
├── scripts/                      # 可执行脚本（确定性逻辑，仅标准库）
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
    │   ├── 01_profile.md         #   个人职业档案
    │   ├── 02_timeline.md        #   职业发展轨迹
    │   ├── 03_projects.md        #   项目资产库
    │   ├── 04_skill_graph.md     #   能力图谱（Domain/Confidence/Evidence）
    │   ├── 05_story_bank.md      #   面试故事库
    │   ├── 06_failure_story.md   #   失败案例库
    │   ├── 07_career_identity.md #   职业身份库
    │   ├── 08_question_backlog.md#   待补充问题库
    │   ├── 09_completeness_report.md # 完整度报告
    │   ├── 10_career_tracks/     #   职业赛道库（每赛道一文件）
    │   └── 11_online_profile.md  #   在线职业档案（派生资产）
    ├── knowledge/                # 市场知识库模板
    │   ├── role_snapshot.md      #   岗位快照
    │   └── skill_snapshot.md     #   能力域快照
    └── resume-outputs/           # 投递产物模板
        ├── 01_jd_match_report.md #   岗位匹配报告
        ├── 02_resume_cn.md       #   中文 ATS 简历
        ├── 03_resume_en.md       #   英文 ATS 简历
        ├── 04_interview_pack.md  #   面试准备包
        ├── 05_answer_cards.md    #   回答卡片库
        ├── 06_upgrade_plan.md     #   竞争力升级计划
        ├── 07_boss_greeting.md   #   Boss 直聘 / 平台打招呼语（策略+双版本）
        ├── XX_gap_analysis.md     #   能力差距分析
        ├── XX_transition_resume_cn.md   # 转岗中文简历
        ├── XX_transition_resume_en.md   # 转岗英文简历
        └── XX_transition_feasibility.md # 转岗可行性评估
```

> **隐私说明**：本技能只包含「指令 + 空白模板 + 脚本」，不含任何个人职业数据。你的真实 Career DNA、Knowledge、Resume Outputs 会在你本地工作区生成，不会随技能包外泄。

---

## 使用流程（首次）

1. 在任意支持的 AI 助手中开启一个新任务，说：「帮我构建 Career DNA」。
2. 技能会调用 `init_career_dna.py` 在当前工作区生成 `career-dna/`、`knowledge/`、`resume-outputs/` 目录。
3. 按引导逐步填写经历、项目、能力、故事（证据驱动，禁止虚构）。
4. 之后每次有新材料，用模式 B 增量更新；要投岗位时用模式 D，自动生成分层投递物料。

---

## 兼容性说明

- 从本仓库克隆的版本 **不含** `agent_created` 标记（那是 WorkBuddy 专属的可管理标记，其他 agent 会忽略）。若你只用 WorkBuddy 并希望用内置 Skill 管理功能编辑此技能，可在 `SKILL.md` frontmatter 加回一行 `agent_created: true`。
- 所有 `references/*.md` 与 `assets/templates/*.md` 均为纯 Markdown，可直接被任意 agent 读取。
- 本仓库不含任何写死的绝对路径（除各 agent 的可选技能安装目录 `skills/` 外），无平台私有依赖。

---

## 版本与更新

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。当前版本 **v1.6.3**。近期重点：

- **v1.6.3**：打招呼语人味化 + 策略决策（Greeting Strategy 推荐/备选 + 7 条人味化规则 + 每平台双版本 + Why/Tone/Do-Not-Say）。
- **v1.6.2**：证据路由 + 平台策略（Evidence Routing 三层输出 + 四平台变体，新增 LinkedIn；Greeting 不再自己选证据）。
- **v1.6.1**：打招呼语目标驱动重写（4 种 Objective + 证据自动选择 + 三平台变体）。
- **v1.6**：新增 Boss 直聘打招呼语生成（07_boss_greeting.md，由匹配报告与 Decision Score 驱动）。
- **v1.5.6**：输出质量收敛（摘要-正文值统一、匹配置信度口径收紧、决策评分因子分类）。
- **v1.5.5**：证据强度升级（5 维度评分 + 材料投放策略）。
- **v1.5.4**：可解释匹配引擎（4 维匹配 + 置信度拆解 + 三角验证）。

---

## License

[MIT](LICENSE) © 2026 The Career Manager Authors
