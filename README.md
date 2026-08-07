# Career Manager — AI 职业经理人

> 把你的 AI 助手变成私人 Career Manager：以 **Career DNA（职业基因库）** 为唯一事实源，持续建设、管理、升级你的职业资产，而不是每次看到 JD 都从零重写简历。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v2.7.1-green.svg)](CHANGELOG.md)
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

## 四层架构

v1.3 起职责收敛，v2.0 进一步扩展为清晰的四层，彻底分离「个人资产 / 市场情报 / 单次产物 / 投递追踪」：

| 层 | 定位 | 回答的问题 | 内容 | 更新来源 |
|----|------|-----------|------|----------|
| **Career DNA**（个人资产层） | 你的唯一事实源 | 我做过什么、为什么适合某方向 | 经历 / 能力 / 项目 / 故事 / Career Track | 你提供 |
| **Knowledge**（市场知识层） | 外部市场情报 | 市场需要什么、趋势是什么 | Role Snapshot、Skill Domain Snapshot | JD 分析累积 |
| **Resume Outputs**（投递产物层） | 单次 JD 临时产物 | 这次 JD 我准备了什么 | 匹配报告 / 简历 / 面试包 | 每次 JD 生成 |
| **Application Tracker**（投递追踪层） | 投递反馈记录 | 我投了以后发生了什么 | 投递主表 / 状态定义 / Case 档案 | 用户手动录入 |

关键规则：Career DNA 是**个人资产**，Knowledge 是**市场资产**，Resume Outputs 是**临时产物**，Application Tracker 是**反馈记录**；Career Track 回答「你适合什么」，Role Snapshot 回答「市场要什么」——两者不再重叠。每次投递单建子目录（`{日期}-{公司}-{岗位}/`），不覆盖历史记录。

---

## 核心原则

1. **Career DNA First（资产优先）**：Career DNA 永远优先于简历。先确保职业资产充足，再生成简历，不要一上来就优化排版。
2. **Evidence Driven（证据驱动）**：所有能力必须有证据支持。禁止虚构经历、夸大职责、编造项目。每项能力必须能回答：来自哪个项目？有什么证据？面试官追问时如何证明？
3. **Build Before Optimize（先建库再优化）**：资产不足时先补充，再产出。
4. **Career DNA Evolves（持续成长）**：不是一次性工程。每次新项目、新岗位、新 JD 都可能更新 DNA。
5. **Unknown → Backlog（未知进待补充池）**：信息不足不猜测，写入 Question Backlog，等待未来补充；禁止长时间连续追问。
6. **Knowledge Accumulates（知识累积）**：每次 JD 分析都提取市场信号写入 Knowledge Layer，随投递次数增长，反哺后续匹配。

---

## 五大工作模式

技能根据用户目标自动路由（先检查当前目录是否存在 `career-dna/`，再决定模式）：

| 模式 | 名称 | 触发场景 | 产出 |
|------|------|----------|------|
| **A** | **Career DNA 构建** | 首次梳理经历 / 盘点能力 / 分析职业方向 | 完整个人职业基因库（`career-dna/`） |
| **B** | **职业资产更新** | 补充新项目 / 新能力 / 回答 Backlog 问题 | DNA 增量更新，不重复建设 |
| **C** | **职业发展分析** | 我适合什么岗位 / 该不该转型 / 竞争力在哪 / 缺什么 | 能力盘点、成长路径、转型可行性 |
| **D** | **岗位投递** | 粘贴 JD / 招聘链接 / 岗位要求 | 匹配报告、中英简历、面试包、缺口分析与补强路线 |
| **E** | **投递追踪** | 录入投递 / 更新面试状态 / 记录反馈 / 看统计 | 投递主表、状态流转、Case 档案、转化看板 |

---

## 关键能力

- **可解释匹配引擎（Explainable Match Engine）**：JD 匹配度按 4 个维度量化——
  - 硬性要求 **40%** / 经验 **30%** / 能力映射 **20%** / 行业 **10%**
  - 并给出**匹配置信度拆解**（Count Quality / Quality / Consistency / Recency 四维）与证据来源，而非黑盒打分。
- **证据强度（Evidence Strength）**：每条证据按 5 维度评分（Ownership / Scope / Impact / Recency / Relevance），总分映射到 Strength 0–5，决定它该写进**主简历**、放进**面试包**，还是仅作**内部参考**——杜绝「什么都敢往简历上写」。
- **职业决策引擎（Career Decision Engine）**：用 Evidence Distance（D0–D4）、Role Authenticity（A–D）、Recruiter Risk Funnel 与 Decision Score，把「该不该投这个岗位」变成可解释的判断，而非拍脑袋。
- **市场知识库（Knowledge Layer）**：Role Snapshot / Skill Snapshot 把 JD 里的市场信号沉淀为可复用行业情报，越投越准。
- **在线职业档案派生**：从 Career DNA 自动生成 Boss / 猎聘等平台的在线简历文案（`11_online_profile.md`）。v2.2 重构为严格映射 Boss 字段的「Boss 在线简历」，由 Profile Positioning Engine（Primary/Secondary/Adjacent Track + Universal Strengths）驱动；v2.3 接入可迁移能力层。
- **可迁移能力映射（Transferable Capability Mapping，v2.3）**：在 Skill Graph 与 Role Snapshot 之间插入能力转换层（`04b_transferable_capabilities.md`），回答「同一个能力在不同岗位应如何不同表达」。新增 `transferable_capability_generation.md`（Source A 自发现 / Source B JD 反馈增强），配合 Expression Intent + Position Constraint，确保生成文案「该写什么、不该写什么」。
- **职业身份重构（Career Identity Reframe，v2.5）**：`07_career_identity.md` 升级为 5 层 Identity-First 结构（Professional Identity / Career Positioning / Career Narrative / Capability Priority / Non-Positioning Statement），明确「起点经历是能力形成路径，不是身份」。Pipeline 新增 Identity Resolution 步骤锁定身份，配合 R01–R04 硬规则（07 为唯一身份来源、经历仅作证据、Experience Reframing 把原始岗位/动词重写为能力视角表达）。
- **能力迁移翻译（Capability Translation）**：把你的经历映射到目标岗位要求，区分 Direct / Adjacent / Missing 三类，禁止编造不存在的匹配。
- **岗位沟通产物生成（Outreach / Boss Greeting Generation）**：由匹配报告驱动的 JD 级即时沟通文案，不只是简历。核心是一套**决策 + 人味化**管线——
  - **打招呼目标（Greeting Objective）**：按岗位与匹配度选 Type A 建联 / Type B 证明价值 / Type C 化解顾虑 / Type D 激发好奇，不同目标对应不同结尾策略；
  - **证据路由（Evidence Routing）**：从 Strength≥4 的证据池按「距离优先 / 角色相关 / 新奇注入」三条规则分层为 Primary / Secondary / Curiosity，杜绝把 AI 项目误选为 PM 岗位钩子；
  - **平台策略（Platform Variants）**：同一匹配结论在 Boss 直聘（诱导 HR 回复，60–120 字）、猎聘（建立专业感，150–250 字）、邮件（正式投递，300+ 字附简历）、LinkedIn（建立关系，80–120 字不提求职）四平台各自生成不同目标版本；
  - **人味化（Humanization）**：7 条规则（短句 / 不用 AI 词 / 自然问句 / 不堆材料 / 不模板开头等）让文案更像真人；每平台仅出「推荐 + 备选」两个版本，附 Why / Tone Notes / Do Not Say。
- **作品集发现与生成（Portfolio Discovery & Output，v2.1）**：从 Career DNA 自动发现、验证并生成作品集案例——不再只写简历，而是把「最值得讲的项目」沉淀为结构化 Portfolio Case。
  - **候选池（Portfolio Candidates）**：4 项 Discovery Rules 筛选项目，7 维 Validation（背景 / 角色 / 问题 / 方案 / 行动 / 成果 / 能力）判定 Readiness ≥ 70% Ready / < 70% Need More Evidence；5 维 Potential Score 排序。
  - **案例模板（Portfolio Case）**：8 字段结构化（概览 / 背景 / 角色 / 问题 / 方案 / 行动 / 成果 / 能力体现），从 DNA 严格映射、不自由发挥；Mode A 构建 / Mode B 更新 / Mode D 投递时自动联动（投递时按 JD 推荐 Top 3 最佳案例）。
- **投递追踪系统（Application Tracker，v2.0）**：v1.x 解决「我该怎么投」，v2.0 解决「我投了以后发生了什么」。录入投递（Index）、更新状态（Stage 0 Planned → Stage 7 Offer / Stage 8 Rejected）、登记面试反馈 / 拒绝原因（archives/）、查看转化与 Offer 率看板——形成「分析 → 决策 → 投递 → 反馈」的完整闭环。
- **简历 / 面试证据管线（ATS Evidence Pipeline，v2.6–v2.7）**：把「重写整份简历」拆成可审计、可解释的步骤——Mode D 先从 `07` 锁定职业身份（Resume Identity Lock, Step 4.5）、用 `04b` 做能力映射（Capability Mapping）选经历；每条经历经 Experience Reframing 拆分为 **Profile Reframing**（在线档案，高抽象允许）与 **ATS Reframing**（简历，受 **E01–E04 证据保全规则**约束，禁止夸大职级 / 权限）；ATS 输出为三层结构（Capability Interpretation → JD Mapping → ATS Evidence Output）；最终由 **Step 9.1 Resume QA Layer**（QA-1 身份漂移 / QA-2 能力缺失 / QA-3 D3 过度包装 / QA-4 身份回退）把关，并由 **Step 9.0 逐经历重构循环**逐项生成。面试材料（故事 / 回答卡片）同样从 `07` Career Narrative + `04b` 能力优先级派生（Step 8.12 Narrative Alignment）。

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
│   ├── mode_e_application_tracker.md # 模式 E 流程（投递追踪）
│   ├── online_profile_generation.md # 在线档案生成（Profile Positioning Engine）
│   ├── transferable_capability_generation.md # 可迁移能力生成（v2.3）
│   ├── output_contracts.md       # 产物格式契约
│   ├── question_backlog.md       # 待澄清问题库
│   └── targeted_discovery.md     # 定向挖掘提问库
└── assets/templates/             # 输出用模板（不进 context）
    ├── career-dna/               # DNA 各模块模板（01~12）
    │   ├── 01_profile.md         #   个人职业档案
    │   ├── 02_timeline.md        #   职业发展轨迹
    │   ├── 03_projects.md        #   项目资产库
    │   ├── 04_skill_graph.md     #   能力图谱（Domain/Confidence/Evidence）
    │   ├── 04b_transferable_capabilities.md # 可迁移能力映射（v2.3 派生资产）
    │   ├── 05_story_bank.md      #   面试故事库
    │   ├── 06_failure_story.md   #   失败案例库
    │   ├── 07_career_identity.md #   职业身份库（v2.5 Identity-First 5 层）
    │   ├── 08_question_backlog.md#   待补充问题库
    │   ├── 09_completeness_report.md # 完整度报告
    │   ├── 10_career_tracks/     #   职业赛道库（每赛道一文件）
    │   ├── 11_online_profile.md  #   在线职业档案（派生资产）
    │   └── 12_portfolio_candidates.md # 作品集候选池（v2.1 派生资产）
    ├── knowledge/                # 市场知识库模板
    │   ├── role_snapshot.md      #   岗位快照
    │   └── skill_snapshot.md     #   能力域快照
    ├── application-tracker/      # 投递追踪库模板（v2.0）
    │   ├── 01_application_index.md   # 全量投递主表
    │   ├── 02_status_definitions.md  # 统一状态定义
    │   └── archives/README.md        # Case 档案（按需建档）
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
        ├── XX_transition_feasibility.md # 转岗可行性评估
        └── XX_portfolio.md        #   作品集案例（v2.1 派生资产）
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

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。当前版本 **v2.7.1**。近期重点：

- **v2.7.1**：P0–P3 全面升级——新增 Step 9.1 Resume QA Layer（QA-1 身份漂移 / QA-2 能力缺失 / QA-3 D3 过度包装 / QA-4 身份回退）+ Step 9.0 逐经历重构循环（Per-Experience Engine Loop）+ Step 8.12 Narrative Strength（叙事强度 0–20）+ Mode C Step 7 Track Strategy Engine；并清理残留在模板/参考文件中的 PII 痕迹。
- **v2.7**：P3 规则合并（14→7 条：R02 身份推导禁止 / R03 角色解释 / R04 能力优先 / R05–R07）+ Mode B/C 同步读取 07(5 层)/04b + Gap Analysis / Upgrade Plan 叙事对齐 07 + Mode C Step 6 市场信号复盘。
- **v2.6.4**：ATS 三层输出结构（Capability Interpretation → JD Mapping → ATS Evidence Output）+ 系统评估（架构 7.5/10、规则覆盖 9/10）。
- **v2.6.2–v2.6.3**：Experience Reframing 拆分为 Profile Reframing（在线档案，高抽象允许）与 ATS Reframing（简历，证据绑定）+ **E01–E04 证据保全规则**，并接入 Pipeline 生成前强制闸门。
- **v2.6.1**：叙事对齐——面试故事 / 回答卡片注入 07 Career Narrative + 04b 能力优先级。
- **v2.6**：Mode D 集成 07+04b——Step 4.5 Resume Identity Lock + 能力驱动简历生成（Capability Mapping）。
- **v2.5.5**：全量 PII 脱敏（7 个模板/参考文件中的具体岗位名、公司名、领域术语替换为 `[XX]`/`[Track名称]` 占位符）+ 拼写修复。
- **v2.5**：职业身份重构（v2.5）— `07_career_identity.md` 5 层 Identity-First 结构 + Identity Resolution + R01–R04 硬规则 + Experience Reframing（R04）。
- **v2.3**：可迁移能力映射（Transferable Capability Mapping）— 新增 `04b_transferable_capabilities.md` 与 `transferable_capability_generation.md`，Online Profile 接入能力转换层。
- **v2.2**：在线档案重构（Boss 在线简历 v2.2）— `11_online_profile.md` 严格映射 Boss 字段 + 新增 `online_profile_generation.md`（Profile Positioning Engine）。
- **v2.1.2**：全量质量审计（40 文件，修复 17 处问题：架构命名、破损模板引用、编码损坏）。
- **v2.1.1**：作品集模板重写（STAR+ → 真 Portfolio，As-Is/To-Be 流程）+ Potential Score 5 维排序。
- **v2.1**：作品集发现与生成（Portfolio Discovery & Output）——新增 `12_portfolio_candidates.md` + `XX_portfolio.md`，Mode A/B/D 全链路联动。
- **v2.0**：投递追踪系统（Application Tracker）——新增 `application-tracker/` 层与 **Mode E**，记录真实市场反馈，形成「分析→决策→投递→反馈」闭环。
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
