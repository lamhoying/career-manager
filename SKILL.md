---
name: career-manager
description: "AI Career Manager (AI职业经理人) - 帮助用户持续建设、管理、升级职业资产（Career Assets）的完整系统。围绕 Career DNA（职业基因库）展开，支持五大工作模式：职业基因库构建、职业资产更新、职业发展分析、岗位投递、投递追踪。当用户要求梳理经历、盘点能力、分析职业方向、匹配岗位JD、生成简历、准备面试时触发此技能。不限于单次简历修改，而是建立持续成长的职业资产体系。"
---

# Career Manager - AI 职业经理人

## Overview（概述）

本技能作为一个 AI Career Manager（AI职业经理人），以 Career DNA（职业基因库）为核心，帮助用户持续建设、管理、升级职业资产。Career DNA 是用户职业经历、能力、项目、故事和成长轨迹的唯一事实源（Single Source of Truth）。简历只是 Career DNA 的一种输出形式。

## Four-Layer Architecture（四层架构 v2.0）

v2.0 新增 Application Tracker 层，记录真实市场反馈。

```
Career DNA         （职业基因库）= 个人职业资产库 → 你做过什么、为什么适合某个方向
Knowledge          （市场知识库）= 职业市场知识库 → 市场需要什么、趋势是什么
Resume Output      （投递产物）= 单次JD投递产物库 → 这次JD你准备了什么
Application Tracker（投递追踪）= 投递反馈记录库 → 你投了以后发生了什么
```

**v1.3 核心变化**：
- 删除 `job-tracks/` 目录（与 `role_snapshots` 职责重叠 >80%）
- `10_career_tracks.md` 拆分为 `10_career_tracks/` 目录，每个 Track 一个独立文件
- Career Track 回答"为什么用户适合这个方向"，Role Snapshot 回答"市场需要什么"

| 层 | 定位 | 内容 | 更新来源 | 文件范围 |
|----|------|------|----------|----------|
| Career DNA Layer（个人资产层） | 用户唯一事实源 | 经历、能力、项目、故事、Career Track | 用户提供 | `career-dna/` |
| Knowledge Layer（市场知识层） | 外部市场情报 | Role Snapshot、Skill Domain Snapshot | JD 分析积累 | `knowledge/` |
| Resume Outputs（投递产物层） | 单次JD临时产物 | 匹配报告、JD原文、简历、面试包 | 每次JD生成 | `resume-outputs/{date}-{company}-{role}/` |
| Application Tracker（投递追踪层 v2.0） | 投递反馈记录 | 投递主表、状态定义、Case 档案 | 用户手动录入 | `application-tracker/` |

**规则**：
- Career DNA 是个人资产，Knowledge 是市场资产，Resume Outputs 是临时产物，Application Tracker 是真实反馈
- Career Track 回答"你适合什么"；Role Snapshot 回答"市场要什么"——不再重叠
- Resume Outputs 每次 JD 单建子目录；Application Tracker 按需建档，不覆盖历史

## Core Principles（核心原则）

所有工作必须遵循以下原则：

1. **Career DNA First（职业资产优先）**：Career DNA 永远优先于简历。简历只是输出，Career DNA 才是核心。不要直接进入简历优化，先确保职业资产充足。
2. **Evidence Driven（证据驱动）**：所有能力必须有证据支持。禁止虚构经历、夸大职责、编造项目、推测不存在的能力。每项能力必须能回答：来自哪个项目？有什么证据？面试官追问时如何证明？
3. **Build Before Optimize（先建库再优化）**：优先积累职业资产。如果职业资产不足，先补充资产，再生成简历。
4. **Career DNA Evolves（职业资产持续成长）**：Career DNA 不是一次性完成。每次新项目、新工作、新岗位、新 JD 都可能更新 Career DNA。
5. **Unknown → Backlog（未知信息进入待补充池）**：信息不足时不猜测，加入 Question Backlog（待补充问题库），等待未来补充。禁止长时间连续追问。
6. **Knowledge Accumulates（市场知识持续积累）**：每次 JD 分析都应提取市场知识，写入 Knowledge Layer。Knowledge 随投递次数增长，反哺后续匹配分析。
7. **Career DNA Write Contract（职业资产写入契约）**：`career-dna/` 是用户的唯一事实源，文件清单以 `assets/career_dna_manifest.json` 为唯一定义源。**任何临时分析、单次提问产物、草稿一律不得写入该目录的根目录**——单次投递产物写 `resume-outputs/{date}-{company}-{role}/`，临时草稿写 `career-dna/_inbox/`。确需在根目录新增文件时，必须走「四件套登记」（manifest 条目 + 同名模板 + 权重 + SKILL.md 目录树/Resources 同步），并运行 `validate_career_dna.py` 自检；未登记文件视为污染，须移出或补登记。**分区资产另受 `regeneration` 字段约束**（如 13 号手册的 Part 1-3 派生区 / Part 4-9 手写区）：自动刷新只能改派生区，**手写区被覆盖属事故**，由 validate 的 P1 `derived-part-drift` 兜底。

## Mode Routing（模式路由）

根据用户当前目标自动选择模式。先检查当前工作目录下是否存在 `career-dna/` 目录，再根据以下条件路由：

| 条件 | 模式 |
|------|------|
| 用户要求建立 Career DNA / 梳理经历 / 盘点能力 / 分析职业方向 / 上传简历且不存在 Career DNA | **Mode A: Build Mode（职业基因库构建模式）** |
| 用户补充新经历 / 新项目 / 管理经验 / 新技能 / 回答 Backlog 问题 | **Mode B: Update Mode（职业资产更新模式）** |
| 用户询问适合什么岗位 / 是否该转型 / 职业发展方向 / 竞争力在哪 / 缺什么能力 | **Mode C: Review Mode（职业发展分析模式）** |
| 用户提供 JD / 职位描述 / 招聘链接 / 岗位要求 | **Mode D: Job Application Mode（岗位投递模式）** —— **两阶段（v2.17.0）**：默认只出 `01` 报告并停在决策门；用户明说要材料才继续生成 Pack（判据见 `references/mode_d_job_application.md` §Phase Routing） |
| 用户记录投递 / 更新面试状态 / 记录反馈 / 查看投递统计 | **Mode E: Application Tracker（投递追踪模式 v2.0）** |

进入具体模式前，加载对应的参考文件获取详细工作流指引。

## Directory Structure（目录结构）

所有产物在用户当前工作目录下组织：

```
career-dna/                    # 个人职业资产库（Personal Assets · Single Source of Truth）
├── 01_profile.md              # 个人职业档案 (Profile)
├── 02_timeline.md             # 职业发展轨迹 (Career Timeline)
├── 03_projects.md             # 项目资产库 (Project Asset Library)
├── 04_skill_graph.md          # 能力图谱 (Skill Graph) — 含 Domain/Confidence/Evidence 字段
├── 04b_transferable_capabilities.md  # 可迁移能力映射 (Transferable Capability) — 派生资产
├── 05_story_bank.md           # 面试故事库 (Story Bank)
├── 06_failure_story.md        # 失败案例库 (Failure Story Library)
├── 07_career_identity.md      # 职业身份定义 (Career Identity) — 5 层结构
├── 08_question_backlog.md     # 待补充问题库 (Question Backlog)
├── 09_completeness_report.md  # 完整度报告 (Completeness Report)
├── 10_career_tracks/          # 职业赛道库 (Career Tracks) — v1.3 目录模式（v2.12.0：每文件含 ## Track Strategy 段）
    ├── README.md              #   赛道总览 (Tracks Overview)
    ├── {track_name}.md        #   赛道文件（文件名 = Track 受控取值；示例：game_tech_pm / rd_pm / pmo / ai_product_pm）
    └── ...                    #   每条赛道一个文件（赛道由用户实际构建，skill 侧不预置）
├── 11_online_profile.md      # Online Career Profile（Boss在线简历）— 派生资产
├── 12_portfolio_candidates.md  # 作品集候选池 (Portfolio Candidates) — 派生资产
├── 13_interview_narrative_strategy.md  # 面试叙事战略手册 — 派生区 Part 1-3 + 手写区 Part 4-12 · 面试表达 SSOT · 内置三层导航 L1/L2/L3
└── _inbox/                   # 草稿区（下划线前缀 = 非 SSOT，不计完整度，可随时清理）

> **写入契约（v2.12.0）**：本目录是用户的唯一事实源，文件清单以 `assets/career_dna_manifest.json` 为准。
> 单次投递产物写 `resume-outputs/`，临时草稿写 `career-dna/_inbox/`；在根目录新增任何文件必须先走「四件套登记」并跑 `validate_career_dna.py`。
> `knowledge/`（市场情报层）与 `resume-outputs/`（单次产物）**不属 Career DNA SSOT**，其内部新增索引 / 快照无需四件套登记。
> **分区资产**：`13_interview_narrative_strategy.md` 分派生区（Part 1-3，可重生成）与手写区（Part 4-12，**任何自动刷新不得覆盖**），
> 分区声明在 manifest 的 `regeneration` 字段；`validate_career_dna.py` 双向护栏：P1 `derived-part-drift`（防「丢」）+ P1 `undeclared-part`（防「偷偷加」）。
> 13 尾部另有「**内容填充契约**」—— 每节只允许「实体内容 / 规则 / 指针」三种形态，禁止空指示。
> **三层导航（v2.12.0）**：13 是唯一入口 —— `13`（L1 通用底料）→ `10_career_tracks/{track}.md` 的 `## Track Strategy`（L2 赛道打法）→ `resume-outputs/{JD}/04+05`（L3 本轮切片）。
> **版本标注（v2.12.1 · F5 方案甲）**：模块文件**不再声明自身版本号**，一律在标题下标注 `> Aligns to: <skill 版本>`（表示「内容对齐到该 skill 版本」）；skill 版本以 `CHANGELOG.md` 顶部为准。新增文件同样只写 Aligns to，**禁止自造模块版本号**（此前 16 个文件各写一份，已出现 v2.3.3 vs v2.0 的自相矛盾）。

knowledge/                     # 职业市场知识库（Market Intelligence · 跨JD累积）
├── role_snapshots/            # 岗位快照 (Role Snapshot) — 按 Role 归档的 JD 提炼
│   ├── README.md              #   索引表 (Role / Track / Observed JD Count / **Observed Companies 已观察公司数** / 文件 / 段完整性) + 按赛道归组 + **新赛道候选** — v2.14.0 新增 / v2.17.0 加公司数列与候选节
│   └── {role_name}.md         #   8 段全貌：Role Capability Model / Hiring Intelligence / JD 观察记录 / Persona Statistics / Trend Intelligence 等
└── skill_snapshots/           # 能力域快照 (Skill Domain Snapshot) — 按 Domain 组织
    └── {domain_name}.md       #   含 Observed JD Count / Related Roles / Trend Notes

resume-outputs/                # 单次JD投递产物库（Per-JD Output — 按策略分层生成）
└── {YYYYMMDD}-{company}-{role}/
    ├── 01_jd_match_report.md  # 岗位匹配报告 + Capability Translation + 附录 A/B（术语速查 / 公司背景尽调，v2.15.0）；**P1 唯一产物**，落盘后即停于 Phase Gate（v2.17.0）
    ├── 02_resume_cn.md        # 中文ATS简历
    ├── 03_resume_en.md        # 英文ATS简历
    ├── XX_portfolio.md          # 作品集案例 (Portfolio Case)
    ├── XX_interview_pack.md   # 面试准备包
    ├── XX_answer_cards.md     # 回答卡片库
    ├── XX_upgrade_plan.md     # 竞争力升级计划
    ├── XX_gap_analysis.md     # 能力差距分析 (Moderate/Stretch/Weak Fit)
    ├── XX_transition_resume_cn.md   # 转岗中文简历 (Stretch Fit)
    ├── XX_transition_resume_en.md   # 转岗英文简历 (Stretch Fit)
    ├── XX_transition_feasibility.md # 转岗可行性评估 (Weak Fit)
    ├── XX_learning_roadmap.md # 学习路线图 (Weak Fit)
    └── deliverables/          # 投递定稿包 (v2.8 新增 — 净化/审核/导出的可直接投递文件)
        ├── 02_resume_cn_final.md    #   净化后定稿 md（用户审核）
        ├── 02_resume_cn_final.html  #   v2 完整版（模板样式+内容，预览用，v2.8.1）
        ├── 02_resume_cn_final.docx  #   定稿 Word（export_resume.py，最简转换）
        ├── 02_resume_cn_final.pdf   #   定稿 PDF（HTML 驱动，主投递格式）
        ├── cover_letter_final.docx/.pdf  # 求职信附件 (Pack A/B)
        └── portfolio_final.pdf      # 作品集附件 (Pack A)
```

```
application-tracker/           # 投递追踪库（Application CRM · 按需建档）
├── 01_application_index.md    #   全量投递主表
├── 02_status_definitions.md   #   状态定义（Stage 0-9）
└── archives/                  #   案例档案（满足条件时按需创建）
    └── {Company}_{Role}.md    #     单次投递详细记录（含 Interview Log / Interview Retro）
```

> Case 档案模板：`assets/templates/application-tracker/archives/XX_case.md`。
> `Interview Retro` 的复盘规则见 `career-dna/13_interview_narrative_strategy.md` Part 9；
> 反哺 career-dna 必须由用户显式发起 Mode B（Mode E 只记录）。

详细文件结构与字段定义见 `references/career_dna_structure.md`。

## Mode A: Career DNA Build Mode（职业基因库构建模式）

**目标**：构建 Career DNA 初版，完整度目标 60%-80%。禁止长时间连续追问，优先快速完成职业资产建档。缺失信息进入 Backlog。

**工作流**：初始化目录 → 解析简历 → 提取职业轨迹 → 提取项目经历 → 构建能力图谱 → 构建故事库（含失败案例）→ 构建职业身份 → **发现职业方向并生成 Career Track 文件**（为每个识别到的 Track 生成完整 `{track}.md`） → 生成完整度报告 + Backlog（Backlog 问题关联 Track/Gap/Skill/Impact）

**产物**：`career-dna/` 下 13 个单文件（01-09 + `04b_transferable_capabilities.md`（v2.3）+ `11_online_profile.md`（Boss 在线简历 v2.2）+ `12_portfolio_candidates.md` + `13_interview_narrative_strategy.md`（面试叙事战略手册 v2.11.0，12 Parts，Step 8.5 生成））+ `10_career_tracks/` 目录（每 Track 一文件）+ `XX_portfolio.md`（作品集案例 v2.1）

详细工作流指引见 `references/mode_a_build.md`。

## Mode B: Career DNA Update Mode（职业资产更新模式）

**目标**：将用户补充的新经历、新项目、新技能回写到 Career DNA。

**主动访谈子流程（Mode B+ v2.7.2）**：用户显式要求深挖时，以 opt-in 引导式访谈（≤3 问/轮 × ≤2 轮/session）补全 Career DNA 中"已建档但稀薄"的 entry；一轮问答结束统一写盘一次。详细规则见 `references/mode_b_update.md` §Mode B+。

**工作流**：读取现有 Career DNA → 更新 Projects/Skill Graph/Story Bank/Career Identity/Career Tracks → 重新计算 Completeness → 更新 Question Backlog → 刷新派生资产（含 Online Profile + Portfolio Candidates + Portfolio Case v2.1）

**产物**：更新对应的 `career-dna/` 文件

详细工作流指引见 `references/mode_b_update.md`。

## Mode C: Career Review Mode（职业发展分析模式）

**目标**：基于 Career DNA 分析用户职业发展方向、竞争力、能力差距。

**工作流**：读取 Career DNA → 分析 Career Identity/Career Tracks/Skill Graph → Gap Analysis → 输出职业发展分析报告、推荐职业方向、能力差距分析、成长路线图

**产物**：Career Review Report（直接输出给用户）

详细工作流指引见 `references/mode_c_review.md`。

## Mode D: Job Application Mode（岗位投递模式 v1.5.1）

**前置条件**：Career DNA 必须存在。如不存在，先执行 Mode A。

**目标**：v1.5.1 从"所有 JD 生成同一套包"升级为"按匹配度分层生成 4 种求职包"。Strong Fit → 投递 / Moderate Fit → 投递+补强 / Stretch Fit → 转岗 / Weak Fit → 学习路线。

**投递定稿（Delivery Finalization v2.8）**：Step 9.5 将 working 版简历净化 → 审核 → 导出 Word/PDF（`deliverables/` 子目录，仅中文版；净化不改内容只剥离标注；导出由脚本执行不经过 LLM）。详细规则见 `references/mode_d_job_application.md` §Step 9.5。

**Talent Intelligence Pipeline（人才智能分析管线 v2.18.0 — 两阶段）**：

```
JD
↓
═════ Phase 1: Recon（侦察 · 报告层）═════
Step 1-4: Role Decomposition → Hiring Intent → Talent Persona → Evidence Expectation
Step 4.5a / 5 / 5.5 / 5.6 / 5.7 / 5.8: TC Mapping → DNA Match → Evidence Distance → Role Authenticity → Risk Funnel → Decision Score
Step 2.9 / 6 / 7 / 8: 附录 A/B → Targeted Discovery → Application Strategy（Pack A/B/C/D） → Career DNA Update
Step 10.A-C: Knowledge Update（Role / Skill Snapshot + Track Market Validation + 新赛道发现）
  └── 产物：01_jd_match_report.md（9 Part + 附录 A/B，完整自足）
═════ Phase Gate（决策门）═════  决策摘要 + 三选项（生成材料 / 只留报告 / 换策略）
═════ Phase 2: Build（材料生成 · token 主体）═════
Step 4.5b / 8.5-8.6 / 8.8-8.10 / 8.12 / 9（9.0 逐经历重构 + 9.1 QA 四检） / 9.5 / X / 10.D
  └── 产物：Pack A/B/C/D 全部文件 + deliverables/
```

**两阶段分流（v2.17.0）**：**默认只跑 P1 并停在决策门**（省钱优先；判断不了也走默认 = fail-safe）。用户明说「帮我投 / 生成简历 / 做材料包」→ P1+P2 连跑（**仍先落 `01` 报告**）。用户二次说「生成材料 / 继续」→ **P2 Resumption**（读已有 `01` 报告续跑，**禁止重跑 Step 1-7**）。规则唯一定义源 = `references/mode_d_job_application.md` §Phase Routing / §Phase Gate。

详细工作流指引见 `references/mode_d_job_application.md`。产出合约见 `references/output_contracts.md`。

## Mode E: Application Tracker（投递追踪模式 v2.0）

**前置条件**：`application-tracker/01_application_index.md` 必须存在。如不存在，从模板初始化。
（`scripts/init_career_dna.py` 自 **v2.18.0** 起会一并创建 `application-tracker/` 并拷贝 `01_application_index.md` / `02_status_definitions.md` / `archives/`。此前该脚本不建此层，导致新用户首次初始化后本前置条件**必然不满足**。）

**目标**：记录真实市场反馈。**不自动学习、不自动优化、不反向修改 Career DNA。**

执行以下任一操作：
- **E1 Add Application** — 记录新投递到 Index
- **E2 Update Status** — 更新投递状态（Applied → Viewed → ... → Offer/Rejected）
- **E3 Add Feedback** — 进入面试或收到拒绝反馈时，在 archives/ 创建 Case 文件
- **E4 Dashboard** — 投递统计面板（投递数/转化率/Offer率/待关注）

详细工作流指引见 `references/mode_e_application_tracker.md`。

## Question Backlog Rules（待补充问题库规则）

Question Backlog 是长期资产，来源覆盖所有模式。每个问题记录：问题内容、产生原因、关联能力、优先级。状态分为 Open（待确认）、Answered（已回答）、Archived（已归档）。

详细规则见 `references/question_backlog.md`。

## Knowledge Layer Rules（市场知识层规则）

Knowledge Layer 是外部市场情报的积累层，与 Career DNA（个人资产）物理隔离。

**来源**：Mode D Knowledge Update，从每次 JD 分析中提取市场情报。

**两类快照（v1.3 增强）**：

| 快照类型 | 文件位置 | 内容 | 关键字段 |
|----------|----------|------|----------|
| Role Snapshot（岗位快照） | `knowledge/role_snapshots/{role_name}.md` | 某 Role 的核心技能、软技能、工具、行业分布、JD来源、趋势 | Observed JD Count（观察数）, Observed Companies（观察公司）, Recent JD Sources（近期JD来源）, Trend Notes（趋势备注） |
| Skill Domain Snapshot（能力域快照） | `knowledge/skill_snapshots/{domain_name}.md` | 按 Domain 组织的能力市场情报，含趋势观察 | Observed JD Count（观察数）, Related Roles（关联岗位）, Recent Observations（近期观察）, Trend Notes（趋势备注） |

**使用场景**：
- Mode D Career Track Match：JD Role → Role Snapshot 获取市场基线 → Career Track 匹配用户 → DNA Skill Graph 交叉比对
- Mode D JD Match Report：Role Snapshot vs Skill Graph 交叉比对 → 输出匹配度
- Mode D Targeted Discovery：Skill Domain Snapshot 提供关联能力线索
- Mode C Career Review：参考 Role Snapshot 趋势评估职业方向可行性

**规则**：
- 同一 Role/Domain 的多次 JD 观察合并到同一文件，递增 Frequency/Observed JD Count
- Knowledge 不包含任何用户个人信息，只记录市场侧情报
- Role Snapshot 保存 Observed Companies 和 Recent JD Sources 以便回溯
- Trend Notes 基于多次观察积累的趋势判断

## Career Track Rules（职业赛道规则 v1.3）

v1.3 起，`10_career_tracks/` 替代了 v1.2 的 `job-tracks/`，职责从"市场画像"转变为"个人赛道"。

**每个 Track 文件回答**：
- 为什么用户适合这个职业方向？
- 用户的成长主线和核心优势是什么？
- 有哪些证据支持？
- 还有哪些差距需要提升？

**Track 模板关键字段**：
- **Track / Confidence**：赛道名称和用户匹配置信度
- **Positioning / Career Narrative**：职业定位和成长主线
- **Evidence / Core Strengths**：证据列表和核心优势
- **Recommended Projects / Stories**：推荐展示的项目和故事
- **Known Gaps / Improvement Priorities**：已知差距和提升优先级
- **Target Roles**：该赛道下可投递的具体岗位

**Career Track vs Role Snapshot 的职责分离**（v1.3 核心简化）：
| 问题 | 查找位置 |
|------|----------|
| 市场需要什么能力？ | `knowledge/role_snapshots/` |
| 我适合哪个方向？ | `career-dna/10_career_tracks/` |
| 这次 JD 我匹配度多少？ | `resume-outputs/{date}-{company}-{role}/01_jd_match_report.md` |

## Career DNA Lifecycle（职业资产生命周期）

Career DNA、Knowledge 两层持续循环成长：

```
Build → Review → Apply → Discover → Update → Review → Apply → ...
              ↓                        ↓
         Knowledge Update      Career Track Match（JD → Role Snapshot → Career Track → DNA）
              ↓                        ↓
       knowledge/ 更新           career-dna/10_career_tracks/ 更新
```

任何时候：优先建设职业资产（career-dna/），其次生成求职材料（resume-outputs/{date}-{company}-{role}/），最后沉淀市场知识（knowledge/）。

## Resources（资源）

### scripts/

- `init_career_dna.py` — 初始化 `career-dna/` 目录结构，创建 10_career_tracks/ 子目录及 README.md。在 Mode A 开始时执行。
- `completeness_checker.py` — 扫描 `career-dna/` 目录下所有文件，计算整体完整度评分和各模块完整度，输出信息缺口列表。
- `validate_career_dna.py` — **Career DNA 写入闸门（v2.9.1 新增，v2.10.0 / v2.11.0 / v2.12.0 / v2.12.1 / v2.13.0 / v2.14.0 扩充）**。对照 manifest 校验 `career-dna/`：P0 `orphan` / `duplicate-content`，P1 `missing` / `unregistered-dir` / **`derived-part-drift`** / **`undeclared-part`**，P2 `no-timestamp` / `unresolved-anchor` / `ghost-file-ref` / **`stale-rule-ref`** / **`track-constraint-coverage`** / **`role-snapshot-schema`**（末者扫 `knowledge/role_snapshots/` 而非 `career-dna/`）。**只报告、绝不修改**；存在 P0/P1 时退出码 1。调用点：Mode A Step 0 与 Step 8.5 收尾、Mode B/C/D 收尾。
- `export_resume.py` — 投递定稿导出（v2.8.8 HTML 模板驱动）：final.md → v1 抽象模板渲染 → v2 完整版 HTML → PDF（主）/ DOCX（辅）。支持 `--template` / `--photo` / `--theme`；版式全读模板 :root CSS 变量（配色调色板集中颜色；页宽/照片宽/间距等无硬编码）；页面背景 + Header 多形状堆叠背景由 onPage canvas 绘制。
- `mini_template.py` — 零依赖递归模板引擎（v2.8.1）：`{{变量}}` + `{{#each 列表}}`（支持嵌套）。

### assets/

- `career_dna_manifest.json` — **Career DNA 文件清单唯一定义源（v2.9.1 新增，v2.10.0 加 `regeneration`）**。声明 `career-dna/` 根目录允许存在的全部文件（filename / name / desc / weight / kind）、草稿区前缀与忽略名单；对分区资产（如 13）额外声明 `regeneration`（`mode: partial` + `derived_parts` + `authored_parts` + 覆盖规则）。init_career_dna.py、completeness_checker.py、validate_career_dna.py 均从此读取——禁止在脚本或文档中另行硬编码清单（此前四处各写一份，已出现「10 个文件 vs 12 个文件」的口径漂移）。

### references/

- `career_dna_structure.md` — Career DNA 全部文件的字段定义、填写规范，以及 Knowledge Layer / Resume Outputs 说明。构建或更新任何文件前加载此文件。
- `mode_a_build.md` — Mode A 详细工作流：9 步流程、每步操作指引、追问限制、完整度目标。含 Track Discovery（职业赛道识别）。Online Profile Pipeline **不在此重复定义**（降为指针 → `online_profile_generation.md`）。
- `mode_b_update.md` — Mode B 详细工作流：增量更新策略、回写规则、完整度重算。含 Mode B+ 主动访谈子流程（v2.7.2，opt-in 引导式深挖）。
- `mode_c_review.md` — Mode C 详细工作流：分析框架、Gap Analysis 方法、输出格式。
- `mode_d_job_application.md` — Mode D 详细工作流：Career Track Match → JD Match Report → Targeted Discovery → Career DNA Update → Resume Package → Knowledge Update。含 Step 9.5 投递定稿（v2.8）；**Step 2.9 附录生成**（v2.15.0：附录 A 三级准入 + 附录 B 每次必做 Tier 1）；**Step 5.8 Decision Score 评分规则**（v2.16.0：废除 Additive 三项因子 → `0.7×Match + 0.3×HireProb`，情境因子改 Label 展示不参与判定）；**两阶段门控**（v2.17.0：§Phase Routing 分流词表 + fail-safe、§Phase Gate 三段式输出与续跑规则、Step 10 拆 A-C→P1 / D→P2）；**Step 10 C 新赛道发现**（v2.17.0：判据 = 同一快照 distinct 公司数 ≥ 3，计量单位为**公司数非 JD 数**）；Reframing 仲裁 `Rule E05`（v2.13.0：事实 > 角色解释 > 职责动词 > 能力抽象）；**v2.18.0 闭环修复**：`Step 4.5a` / `4.5b` **标题与引用双向同步**（原为两个同名 `## Step 4.5:`）、`Step 8.5-8.12` **物理位置**上移至 Phase Gate 之后（与编号一致）、`Step X` 输入表改读 **8.7**（原误读 8.5）、`Part 4.5` / `Part 6 匹配总览` 等悬空锚点修正、**Pack C 命名统一为数字前缀**（原 `XX_` 与实际模板命名混用）。
- `output_contracts.md` — 各 Mode 产物合约：结构、字段、验收标准（生成任何产物前核对）。含**共享边界表 + 抽象档位表**（v2.13.0：哪些跨渠道共享、哪些各渠道独立）+ **附录 A/B 合约**（v2.15.0：可选产物、与 Part 骨架正交、无闸门）。
- `mode_e_application_tracker.md` — Mode E 详细工作流（v2.0 新增）：Application CRM，记录真实市场反馈。
- `targeted_discovery.md` — Targeted Discovery 规则。
- `online_profile_generation.md` — Online Career Profile 生成规则（v2.2 新增）。**规则真源**（`R01-R07` 合法编号集合）；**Online Profile Pipeline 唯一定义**（v2.13.0 起）；`R03` 含角色标签白名单 + fail-safe。
- `transferable_capability_generation.md` — 可迁移能力生成规则（v2.3 新增）。
- `question_backlog.md` — Question Backlog 管理规则。
- `pack_templates/` — **01-08 全部产物的版式唯一定义源**（**v2.18.0 补入 Resources 索引**）。含 `01_jd_match_report_template.md` ~ `08_boss_greeting_template.md` 共 8 个模板 + `README.md`（模板清单 / Pack 覆盖表 / **编号映射铁律**）。每个模板 = 章节骨架 + 固定表格列头 + 字段占位，**只锁版式、不锁内容**。

### assets/templates/

- `career-dna/01_profile.md` ~ `09_completeness_report.md` — 9 个核心文件模板（01-09；另 04b / 11 / 12 / 13 见下，共 13 个）。
- `career-dna/11_online_profile.md` — Online Career Profile（Boss在线简历）。
- `career-dna/12_portfolio_candidates.md` — 作品集候选池 (v2.1 新增)。
- `career-dna/13_interview_narrative_strategy.md` — **面试叙事战略手册（v2.10.0 新增，v2.11.0 扩至 12 Parts，v2.12.0 加三层导航；分派生区 / 手写区）**。面试表达层 SSOT；内置 **L1/L2/L3 三层导航**（13 → `10_career_tracks/{track}.md` 的 `## Track Strategy` → `resume-outputs/{JD}/04+05`）；Part 6 口径纵深 / Part 7 分轮次与分题型打法 / Part 8 面试后跟进 / Part 9 复盘回路 / Part 10 反向尽调 / Part 11 录用阶段（Offer 谈判 + 背调）/ Part 12 英文面试。尾部含「内容填充契约」。
- `career-dna/04b_transferable_capabilities.md` — 可迁移能力映射。`Position Constraint` 赛道条目为**目录驱动**（条目数 = `10_career_tracks/` 实有赛道数，由 P2 `track-constraint-coverage` 校验）。
- `career_track.md` — Career Track 赛道模板（v2.12.0：`## Track Strategy` 由指针段改为实体段 S1-S4）。
- `knowledge/role_snapshot.md` — Role Snapshot 模板。`Track（职业赛道）` 为**受控取值**（`10_career_tracks/` 下的赛道文件名，或 `none`；解释写 `Track Note`）；`Observed Companies` 同为**受控格式**（公司名，说明写 `（）` 括注，未标注写 `unknown` —— v2.17.0，其解析出的公司数是「新赛道发现」判据的唯一输入）。8 段完整性 + Track 取值 + 别名冲突 + Observed Companies 格式由 P2 `role-snapshot-schema` 四项校验（v2.14.0 / v2.17.0）。
- `knowledge/skill_snapshot.md` — Skill Domain Snapshot 模板。
- `resume-outputs/01_jd_match_report.md` — JD Match Report 模板（**遗留副本**；v2.16.0 起 **Part 7** 已收敛进 canonical，v2.18.0 起 **Part 9** 亦已收敛，两节均降为指针）。
  ⚠️ **现行版式（9-Part + 附录 A/B）的唯一定义源是** `references/pack_templates/01_jd_match_report_template.md`（被 `mode_d` / `output_contracts` 双引用）—— 生成产物时以它为准，不改本遗留副本。
  **v2.16.0 复议**：原判断「canonical 一律比遗留副本完整」**至少对 Part 7 不成立** —— 遗留副本该节原载 v1.5.6 完整版（`Factor Types` 三分类 + `Decision Factors` 表），canonical 仅 9 行简版，属**版本倒挂**。已按 D8 甲把完整内容**收敛进 canonical**（规则 → `mode_d` §Step 5.8；版式 → `pack_templates/01` Part 7），遗留副本该节降为指针。**其余 Part 的收敛仍归 A-5。**
  **v2.18.0 复议**：**Part 9 是第二例「版本倒挂」** —— 遗留副本原载 `## Part 9: Outreach Package v1.6.2`（9.1 Evidence Routing / 9.2 Platform Variants），canonical **完全没有 Part 9**，导致 `Step 8.5 / 8.6` 的输出**无处落盘**。已同法收敛（版式 → `pack_templates/01` Part 9；规则 → `mode_d` Step 8.5 / 8.6），遗留副本该节降为指针。
- `resume-outputs/XX_portfolio.md` — 作品集案例模板 (v2.1 新增)。
- `resume-outputs/02_resume_cn.md` — 中文 ATS 简历模板。
- `resume-outputs/03_resume_en.md` — 英文 ATS 简历模板 (v1.5.1 新增)。
- `resume-outputs/resume_template.html` — 投递定稿 HTML v1 抽象模板（v2.8.1 新增；v2.8.7+ 顶部「配色调色板」集中颜色，Template-as-Spec：占位符 + CSS 变量，用户改模板 = 改设计；引擎支持 .header/.section/.entry 等结构类）。
- `resume-outputs/resume_template_preview.html` — HTML 设计稿预览（版式规格参考）。
- `resume-outputs/resume_template.docx` — 投递定稿 Word 空模板（v2.8，从用户既有简历提取样式）。
- `resume-outputs/04_interview_pack.md` — 面试准备包模板。
- `resume-outputs/05_answer_cards.md` — 回答卡片库模板。
- `resume-outputs/06_upgrade_plan.md` — 竞争力升级计划模板。
- `resume-outputs/07_boss_greeting.md` — Boss 打招呼语模板 (v1.6 新增)。
- `resume-outputs/XX_gap_analysis.md` — 能力差距分析模板 (v1.5.1 新增)。
- `resume-outputs/XX_transition_resume_cn.md` — 转岗中文简历模板 (v1.5.1 新增)。
- `resume-outputs/XX_transition_resume_en.md` — 转岗英文简历模板 (v1.5.1 新增)。
- `resume-outputs/XX_transition_feasibility.md` — 转岗可行性评估模板 (v1.5.1 新增)。
- `application-tracker/01_application_index.md` — 投递追踪主表模板 (v2.0 新增；v2.12.0 加 `Pack` 链接列，由 Mode D Step 10 自动登记、Mode E 维护 Status)。
- `application-tracker/02_status_definitions.md` — 状态定义 (v2.0 新增)。
- `application-tracker/archives/XX_case.md` — **投递案例档案模板（v2.10.0 实体化）**。Timeline / **Interview Log** / **Interview Retro** / Feedback / Personal Notes / Lessons Learned 六章节。
- `resume-outputs/XX_learning_roadmap.md` — 学习路线图模板 (v1.5.1 新增)。
