# CHANGELOG

## v2.1.2 — 2026-07-30

### Quality Audit Fix（全量审计修复 v2.1.2）

全量审计 40 个文件，修复 17 个问题（6 严重 + 5 中等 + 6 轻微）。

**严重修复**：
- SKILL.md: "Three-Layer" → "Four-Layer"（与"四层架构"对齐）
- output_contracts.md: 删除不存在模板 `04_capability_translation.md` 引用
- mode_d_job_application.md: 标题版本 v1.4 → v1.6.3 + 删除重复 Step 6
- 08_question_backlog.md: 修复 HTML 注释块破损导致的孤立内容
- mode_b_update.md + mode_c_review.md: `10_career_tracks.md`（单文件）→ `10_career_tracks/`（目录）4处

**中等修复**：
- SKILL.md Resources: 补齐缺失的 04_interview_pack / 05_answer_cards / 06_upgrade_plan / 07_boss_greeting
- 01_jd_match_report.md: 删除 Part 7 底部残留旧版表
- 07_boss_greeting.md + 12_portfolio_candidates.md: 编码损坏字符修复
- output_contracts.md: 标题版本更新

**轻微修复**：
- SKILL.md: 目录树 `└──` 重复使用
- mode_a_build.md: 映射表底部重复行删除
- 02_resume_cn.md: 旧单文件路径修复
- career_dna_structure.md: `02_ats_resume.md` → `02_resume_cn.md` + 重复 section 标记 [Historical]

### 文件变更

共 11 个文件修改。

---

## v2.1.1 — 2026-07-30

### Portfolio Template Rewrite + Gap Detail + Potential Score

**XX_portfolio.md 重写** — 从 STAR+ 升级为真正的 Portfolio：
- 问题→影响结构化表
- 业务流程分析（As-Is / To-Be 对比流程图）
- 项目推进过程（阶段1-4 递进叙事）
- 成果分层展示
- ✓ 列表能力体现
- 可迁移价值 + 使用建议
- Portfolio vs STAR Story 对照注释

**Mode A 映射表升级** — 从单列转向三列（主来源/备选来源/提取规则），对齐新模板的 8 个字段。

**Portfolio Gap Detail** — question_backlog.md [Portfolio] 规则增强：缺什么→怎么补→预计提升。

**Potential Score 预留** — 12_portfolio_candidates.md 新增 5 维 Potential Score 定义（v2.1.2 正式启用）。

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/XX_portfolio.md` | 完全重写 |
| `references/mode_a_build.md` | 映射表升级 |
| `references/question_backlog.md` | Portfolio Gap Detail 追加 |
| `assets/templates/career-dna/12_portfolio_candidates.md` | Potential Score 追加 |

---

## v2.1 — 2026-07-30

### Portfolio Discovery & Output（作品集发现与生成 v2.1）

**核心管线**：Career DNA → Portfolio Discovery → Validation → Output。不新增 Mode F，全链路复用 Mode A/B/D。

```
Mode A: 构建时 → 发现 + 验证 + 生成 Portfolio Case
Mode B: 更新时 → 刷新派生资产 + Portfolio Gaps → Backlog
Mode D: 投递时 → Portfolio Selection 推荐最佳案例
```

### 新增：12_portfolio_candidates.md

- 4 项 Discovery Rules（项目/角色/行动/结果，3 项以上入围）
- 7 维 Validation（背景/角色/问题/方案/行动/成果/能力）
- Readiness ≥ 70% Ready / < 70% Need More Evidence

### 新增：XX_portfolio.md

- 8 字段 Portfolio Case 模板（概览/背景/角色/问题/方案/行动/成果/能力体现）
- 每字段严格从 DNA 映射，不自由发挥

### Mode A 新增 Step 12

- Portfolio Discovery → Validation → Output → Gap to Backlog

### Mode B 联动

- Step 4.5 派生资产刷新扩展（+ Portfolio Candidates + Portfolio Case）
- Step 5 反馈新增 Portfolio 候选池更新情况

### Mode D 联动

- Resume Package 新增 Portfolio Selection（从 Ready 项目推荐与本 JD 最匹配的 Top 3）

### Question Backlog 扩展

- 新增 [Portfolio] 分类规则：缺口项目自动生成追问，回写后触发重新评分

### 文件变更

| 文件 | 类型 |
|------|------|
| `assets/templates/career-dna/12_portfolio_candidates.md` | **新增** |
| `assets/templates/resume-outputs/XX_portfolio.md` | **新增** |
| `references/mode_a_build.md` | Step 12 追加 |
| `references/mode_b_update.md` | Step 4.5/5 扩展 |
| `references/question_backlog.md` | [Portfolio] 分类规则 |
| `references/mode_d_job_application.md` | Portfolio Selection |
| `SKILL.md` | 目录 + Mode 概述 + Resources |

---

## v2.0.1 — 2026-07-28

### SKILL.md 架构集成补全

v2.0 新增了 Mode E 和 application-tracker/，但 SKILL.md 中 3 处遗漏：

- **frontmatter description**: "四大工作模式" → "五大工作模式"（+投递追踪）
- **架构图**: 三层架构 → 四层架构（+Application Tracker Layer）
- **Mode Routing 表**: 新增 Mode E 触发规则行
- **代码块**: 修复 `application-tracker/` 目录树缺少开口 ` ``` ` 的 stray fence bug

### 文件变更

| 文件 | 变更 |
|------|------|
| `SKILL.md` | frontmatter + 架构 + 路由表 + 目录树修复 |

---

## v2.0 — 2026-07-28

### Application Tracker（投递追踪系统 · MVP）

**核心转变**：v1.x 解决"我应该怎么投"，v2.0 解决"我投了以后发生了什么"。

```
v1.x: Career Decision Engine（分析 + 决策）
v2.0: Application CRM（记录 + 追踪）
```

### 新增：application-tracker/ 目录

| 文件 | 用途 |
|------|------|
| `01_application_index.md` | 全量投递主表（一次性浏览所有投递状态） |
| `02_status_definitions.md` | 统一状态定义（Stage 0: Planned → Stage 7: Offer / Stage 8: Rejected） |
| `archives/{Company}_{Role}.md` | 案例档案（按需建档：进入 HR 面 / 收到拒绝反馈 / 用户标记） |

### 新增：Mode E — Application Tracker

4 个子操作：
- **E1 Add Application** — 新投递录入 Index
- **E2 Update Status** — 状态流转更新
- **E3 Add Feedback** — 面试反馈/拒绝原因登记到 archives/
- **E4 Dashboard** — 投递统计面板（转化率 / Offer率 / 待关注）

### 明确排除（v2.1+ 再做）

- 不自动根据投递结果优化简历
- 不分析哪种 Greeting 转化率高
- 不自动推荐赛道
- 不反向修改 Career DNA / Match Score / Track Confidence

### 文件变更

| 文件 | 类型 |
|------|------|
| `assets/templates/application-tracker/01_application_index.md` | **新增** |
| `assets/templates/application-tracker/02_status_definitions.md` | **新增** |
| `assets/templates/application-tracker/archives/README.md` | **新增** |
| `references/mode_e_application_tracker.md` | **新增** |
| `SKILL.md` | 目录 + Mode E + Resources |

---

## v1.6.3 — 2026-07-27

### Greeting Humanization（打招呼语人味化 + 策略决策 v1.6.3）

**核心改造**：从"系统写 4 种版本文案让用户挑"升级为"系统先做策略决策 → 出推荐方案 + 备选方案 + 结构化推荐理由 → 文案更像真人"。

### 新增 Step 8.8/8.9/8.10

- **8.8 Greeting Strategy Selection**: 推荐 Type + 备选 Type 选择规则 + 结构化推荐理由（Match Basis / Evidence Basis / Risk Basis）
- **8.9 Greeting Humanization**: 7 条人味化规则（句子短 / 不用AI词 / 自然问句 / 不堆材料 / 不模板开���等）
- **8.10 Recommended/Alternative Output**: 每平台仅出 2 个版本 + Why + Tone Notes + Do Not Say

### Boss Greeting 模板重组

`07_boss_greeting.md` 改为双版本结构 + 决策层：
- Greeting Strategy（推荐/备选 Type + Why + 切换条件）
- Recommended Greeting + Alternative Greeting
- Tone Notes（避免词/推荐词/句式规则）
- Do Not Say（5 条禁止清单）

### 联动

- `01_jd_match_report.md` Part 8 新增 Greeting Recommendation Summary
- `output_contracts.md` Boss Greeting 契��更新（双版本/禁出项）

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/07_boss_greeting.md` | 完全重构为双版本+策略+人味化 |
| `references/mode_d_job_application.md` | Step 8.8/8.9/8.10 新增 |
| `references/output_contracts.md` | Boss Greeting 契约更新 |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 8.1 新增 + Part 8 重新编号 |

---

## v1.6.2 — 2026-07-27

### Evidence Routing + Platform Strategy（证据路由 + 平台策略）

**核心问题**：v1.6.1 的 Greeting 直接从 8.0 选证据 → AI 项目可能被选为 PM 岗位钩子 → HR 困惑。v1.6.2 新增 Evidence Routing Engine 做路由分层，Greeting 不再自己选证据。

### 新增 Part 9: Outreach Package

`01_jd_match_report.md` Part 8 之后新增：

**9.1 Evidence Routing（证据路由）**：
- Candidate Pool：从 Part 4 提取 Strength≥4 的全部证据
- 3 条路由规则：Distance Priority / Role Relevance / Novelty Injection
- 3 层输出：Primary（主证据）/ Secondary（辅证据）/ Curiosity（好奇证据）

**9.2 Platform Variants（平台变体 v1.6.2）**：
- 平台从"长度不同"升级为"目标不同"
- Boss 直聘：让 HR 回复，60-120 字，Primary 单证据 + 反问
- 猎聘：建立专业感，150-250 字，Primary+Secondary
- 邮件：正式投递，300+ 字，附简历
- **新增 LinkedIn**：建立关系，80-120 字，不附简历不提求职

### 新增 Step 8.5/8.6

- Step 8.5: Evidence Routing Engine
- Step 8.6: Platform Strategy

### 联动

- `07_boss_greeting.md` Evidence Source 改为引用 Part 9.1 路由结果
- Platform Variants 表同步更新为 v1.6.2 四平台版本

```
v1.6.1: JD → Match → Greeting（直接生成）
v1.6.2: JD → Match → Evidence Matrix → Evidence Routing → Platform Strategy → Greeting
```

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | Part 9 新增（9.1+9.2） |
| `references/mode_d_job_application.md` | Step 8.5 + 8.6 新增 |
| `assets/templates/resume-outputs/07_boss_greeting.md` | Evidence Source + Platform Variants 更新 |

---

## v1.6.1 — 2026-07-27

### Boss Greeting: Objective-Driven Rewrite（打招呼语升级 v1.6.1）

**核心转变**：从「展示经历」到「诱导 HR 回复」。v1.6 的 3 个版本本质是 JD 摘要，v1.6.1 升级为 4 种 Objective + 3 平台变体。

### 新增：Greeting Objective（打招呼目标）

| 类型 | 目标 | 结尾策略 |
|------|------|------|
| Type A: Build Connection | 让 HR 回复 | 匹配点 + 轻量行动邀请 |
| Type B: Prove Value | 证明值得聊 | 证据点 + 反问 JD 需求 |
| Type C: Break Risk | 先化解顾虑 | 承认差异 + 突出迁移 |
| Type D: Spark Curiosity | 让 HR 追问 | 悬念 + 追问对方现状 |

### 新增：Evidence Selection（证据自动选择）

从 8.0 Usable Evidence Summary 自动选取 Top1/Top2/安全区/好奇心诱饵，按 Objective 类型匹配。不再随机抽亮点。

### 新增：Platform Variants（平台变体）

| 平台 | 字数 | 策略 |
|------|:--:|------|
| Boss 直聘 | 150 字 | 速读，一个问题结尾 |
| 猎聘 | 200 字 | 半正式，匹配 + 行动邀请 |
| 邮件 | 300 字 | 正式商务，附简历 |

### 联动

- `01_jd_match_report.md` 8.5 Input Pack 字段升级（+Objective + Curiosity Bait + Platform Priority）
- `mode_d_job_application.md` Step X 全量重写

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/07_boss_greeting.md` | 完全重写 |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 8.5 字段升级 |
| `references/mode_d_job_application.md` | Step X 全量重写 |

---

## v1.6 — 2026-07-27

### Boss Greeting Generation（Boss 直聘打招呼语 v1.6）

**核心定位**：由 v1.5.6 最终收敛结果驱动的 JD 级即时沟通产物。不新增分析维度。

### 新增：07_boss_greeting.md

3 个版本，全部基于 Usable Evidence Summary 和 Decision Score 生成：

| 版本 | 适用场景 | 语气 |
|------|----------|------|
| Version A: Standard | Moderate Fit / HR 高风险 | 稳妥 |
| Version B: Match-Driven | Match Score 较高 | 匹配点到证据 |
| Version C: Strong | Strong Fit + HR 低风险 | 主动直接 |

**生成规则**：
- 仅引用 Strength ≥ 4 的证据（不引用弱证据）
- 不使用报告术语（Match Score / Confidence 等）
- 每条消息 ≤ 4 句
- Weak Fit 不生成

### 新增：Step X: Boss Greeting Generation

`mode_d_job_application.md` Step 9 Resume Package 之后插入。

### 联动

- `01_jd_match_report.md` Part 8 新增 8.5 Boss Greeting Input Pack（推荐语气/最强匹配点/可引用证据/不建议提）
- `output_contracts.md` 新增 07_boss_greeting.md 产物定义

### 不改

- `career-dna/11_online_profile.md` — 长期档案，不参与即时沟通
- `career-dna/10_career_tracks/*.md` — 方向结构不变

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/07_boss_greeting.md` | **新增** |
| `references/mode_d_job_application.md` | Step X 新增 |
| `references/output_contracts.md` | Boss Greeting 契约定义 |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 8.5 Boss Greeting Input Pack |

---

## v1.5.6 — 2026-07-27

### Output Quality & Convergence（输出质量收敛 v1.5.6）

v1.5.5 报告存在摘要值与正文值不一致、Confidence 计算口径偏宽、Part 4/4.5 表格重复等问题。v1.5.6 做一个纯粹的质量收敛，不新增分析维度。

**修复 1：摘要-正文值统一来源**
- 3.1 Match Summary 改为引用型（值 → 来源列），不独立填值
- 3.2/3.3/Part 7 底部增加收敛线，标注"计算值 → 填入 3.1"

**修复 2：Match Confidence 计算口径收紧**
- 3.3 新增 Scoring Reference（评分因子参考表）：每个分量明确公式 + 扣分条件
- 3.3 Breakdown 表从宽松占位符改为具体示例（原始分/扣分/最终分三列）
- mode_d Step 5 Confidence 同步扣分条件

**修复 3：Decision Score 因子分类**
- Part 7 新增 Factor Types（Core/Multiplier/Additive 三类）
- 明确公式构成和每项因子的类型标签

**修复 4：Part 4 / Part 4.5 表格合并**
- Part 4 改为 Evidence Matrix 合并表（Distance + Strength 同表）
- Part 4.5 删除独立映射表，仅保留 Strength Rules
- Part 8 新增 8.0 Usable Evidence Summary（可用证据 Top3 / Secondary）

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | 3.1 来源化 / 3.2/3.3 收敛线 / 3.3 评分因子+扣分表 / Part 4 合并矩阵 / Part 4.5 缩小 / Part 7 因子分类 / Part 8 可用证据汇总 |
| `references/mode_d_job_application.md` | Step 5 Confidence 扣分条件同步 |

---

## v1.5.5 — 2026-07-26

### Evidence Strength Upgrade（证据强度升级）

**核心目标**：v1.5.4 解决了"像不像"（Evidence Distance），v1.5.5 补充解决"硬不硬"（Evidence Strength）。同样都能映射，但这条证据能不能写进主简历？能不能拿去打面试？

### 新增 Part 4.5: Evidence Strength

`01_jd_match_report.md` 新增独立章节：

**5 维度评分**（0-2 分/维度，总分 0-10 → Strength 0-5）：
- Ownership（主导程度）: 主导=2 / 参与=1 / 无=0
- Scope（覆盖范围）: 跨团队=2 / 单团队=1 / 单人=0
- Impact（结果影响）: 有量化=2 / 有过程=1 / 无=0
- Recency（时效性）: 1年内=2 / 1-4年=1 / 4年+=0
- Relevance（相关性）: 直接=2 / 间接=1 / 不相关=0

**Strength 使用规则**：
- Strength 5 �� 主简历标题区 + 面试开场故事
- Strength 4 → 简历主体，适合补强
- Strength 3 → Interview Pack / Answer Cards
- Strength ≤ 2 → 仅内部参考，不写进外部材料

**关键设计**: Evidence Strength 不进入 Match Score 公式，仅决定材料投放策略。

### DNA 模板联动

- `03_projects.md`: 每个项目追加 Evidence Strength 字段块
- `05_story_bank.md`: 每个故事追加 Strength 评级
- `09_completeness_report.md`: 新增 Strength Coverage 覆盖率统计

### mode_d 推理联动

- Step 5.5 末尾追加 Evidence Strength 判定逻辑 + 联动规则

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | Part 4.5 新增 |
| `assets/templates/career-dna/03_projects.md` | 项目追加 Strength 字段 |
| `assets/templates/career-dna/05_story_bank.md` | 故事追加 Strength 字段 |
| `assets/templates/career-dna/09_completeness_report.md` | 新增 Strength Coverage |
| `references/mode_d_job_application.md` | Step 5.5 末尾追加 Strength 判定 |

---

## v1.5.4 — 2026-07-25

### Career Decision Engine（求职决策系统）

**核心转变**：从"能力匹配报告"升级为"求职决策报告"。3 Parts → 8 Parts。

```
v1.5.3: 能不能做 / 匹配多少 / 缺什么能力 / 怎么包装
v1.5.4: 能不能拿面试 / 招聘方信不信 / 卡在哪一关 / 包装后成功率多少
```

### 新增 Part 4: Evidence Distance（证据距离 D0-D4）

- D0 Strong Direct / D1 Functional Equivalent / D2 Transferable / D3 Inferential / D4 No Evidence
- 替代 Direct/Adjacent/Missing 三值，解决"两个 Adjacent 距离完全不同"
- D0-D4 对外展示等级名，百分数内化

### 新增 Part 5: Role Authenticity（角色真实性）

- Level A-D 四级判定职业身份接近度
- Hire Probability = Match × (Authenticity/100)

### 新增 Part 6: Recruiter Risk Funnel（招聘漏斗风险）

- ATS / HR / Hiring Manager / Offer Committee 四阶段风险预测 + 对策

### 新增 Part 7: Decision Score（决策评分）

- Decision = 0.5×Match + 0.25×HireProbability + Location + Language + Industry
- 全部因子来自 JD+DNA，零市场假设

### 删除 Market Validation / Market Gap / Observed JD Count

- Match Confidence: Market Validation → Evidence Stability（DNA内部证据稳定性）
- Decision Score: Market Gap → Hire Probability

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | 完全重写（3 Parts→8 Parts） |
| `references/mode_d_job_application.md` | Step 5 Conf+公式 + Step 5.5 D0-D4 + Step 5.6/5.7/5.8 新增 |

---

## v1.5.3 — 2026-07-23

### Scoring Granularity Enhancement（评分颗粒度增强）

v1.5.2 完成了 Explainable Match Engine 结构重构，v1.5.3 进一步细化三个模块的评分颗粒度。

### 优化 1：Hard Requirement Scoring 颗粒化

**`01_jd_match_report.md` Part 3.2 Hard Requirement Detail**：
- 从 `✓/△/✗` 三值判定升级为 `Score(0-100) + 扣分来源` 四列
- 每项附扣分原因（头衔不匹配-25 / 年限不足-25 / 证书缺失-10）
- Hard Requirement Match = 各项 Score 均值，而非三值均值

**`mode_d_job_application.md` Step 5**：
- 新增 Hard Requirement 评分逻辑（扣分规则：头衔/年限/证书/完全缺失 4 类）

### 优化 2：Evidence Mapping Coverage %

**`01_jd_match_report.md` Part 3.5 Evidence Mapping**：
- 新增 Coverage（覆盖率）列：`(Direct×100 + Adjacent×60) / 总子证据数`
- 每个 JD 能力拆分为子证据项，分 Direct/Adjacent/Missing 三列并列展示
- Resume Builder 可根据 Missing 列自动判定需补充什么

**`mode_d_job_application.md` Step 5.5**：
- 新增 Evidence Coverage 计算逻辑（子证据拆解 + 汇总公式）

### 优化 3：Skill Gap Priority Matrix

**`01_jd_match_report.md` Part 3.6 Skill Gaps**：
- 新增 Gap Priority Matrix（P0/P1/P2 三级）
- Priority = f(Impact, Cost)
  - P0: High Impact + Low Cost → 立刻做
  - P1: High Impact + High Cost → 计划做
  - P2: Low/Medium Impact → 有余力再做
- 附建议行动列，可直接驱动 06_upgrade_plan.md 生成

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | 3.2 Hard Req + 3.5 Evidence Mapping + 3.6 Skill Gaps 三处升级 |
| `references/mode_d_job_application.md` | Step 5 评分逻辑 + Step 5.5 Coverage 逻辑 |
| `references/output_contracts.md` | v1.5.3 说明更新 |

---

## v1.5.2 — 2026-07-23

### Explainable Match Engine（可解释匹配引擎）

**核心目标**：补齐 Explainability（65→90）和 Score Credibility（60→90）。不增加新分析能力，只重构报告让学生、面试官、AI自己都能看懂"70分是怎么来的"。

### 重构：JD Match Report 从 6 Parts → 3 Parts

| 旧 | 新 | 操作 |
|----|-----|------|
| Part 1: JD Original | Part 1: JD Original | 保留 |
| Part 2+3+4+4.5 | Part 2: Role Analysis | 压缩为 4 个子模块 |
| Part 5: Evidence Expectation | ❌ 删除 | 与 Evidence Mapping 重复 |
| Part 6: DNA Match Analysis | Part 3: DNA Match Analysis | 重构为 7 个子模块 |

**Part 2 Role Analysis 保留字段**：
- 2.1 Core Responsibilities + Ownership + Scope
- 2.2 Hiring Intent（Explicit/Implicit/Business Context/Pain Point）
- 2.3 Skill Weight Analysis（能力权重表）
- 2.4 Ideal Candidate（画像 + 职业背景 + 典型经历 + 偏好特质）

### 新增：Match Score Breakdown（4 维度替代旧 3 维度）

| 维度 | 权重 | 说明 |
|------|------|------|
| Hard Requirement Match（硬性要求匹配） | 40% | 学历/语言/证书/年限逐项判定（附明细表 ✓△✗） |
| Experience Match（经验匹配） | 30% | 行业/场景/角色重叠度 |
| Capability Match（能力迁移匹配） | 20% | Direct+Adjacent+Missing（同 v1.4.4） |
| Industry Match（行业匹配） | 10% | 同行业/同客户群 |

### 新增：Match Confidence Breakdown

**Match Confidence = Evidence Count(30%) + Evidence Quality(30%) + Direct Relevance(25%) + Market Validation(15%)**

区分"匹配度"和"可信度"——两个70分的岗位，一个 8 证据 Confidence 85，一个 1 证据 Confidence 40。

### 新增：Track Validation（三角验证）

```
用户 ↔ Track ↔ JD
```

比直接 User→JD 匹配更稳定。

### 重组：Evidence Mapping

整合旧的 Capability Translation + Evidence Coverage → 单表呈现（JD能力/DNA证据/映射类型/证据质量/Gap），减少翻页。

### 删除：Part 5 Evidence Expectation

与 Evidence Mapping 3.5 高度重复，删除后报告从 ~8 页压缩到 ~5 页。

### 修改：mode_d_job_application.md

- Step 4 标记为 Internal Use Only（不写入报告）
- Step 5 匹配维度从 3 维升级为 4 维
- Step 5 新增 Match Confidence 计算 + Track Validation 计算

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | 完全重写（238→145 行，净减 39%） |
| `references/mode_d_job_application.md` | Step 4 内部化 + Step 5 4维度 + Confidence + Track Validation |
| `references/output_contracts.md` | v1.5.2 结构说明追加 |

---

## v1.5.1 — 2026-07-22

### Application Strategy Decision（求职策略决策 v1.5.1）

**核心变化**：从"所有 JD 生成同一套包"升级为"按匹配度分层生成 4 种求职包"。

```
v1.5: 80分 → 一套包 / 30分 → 同一套包  ❌
v1.5.1: 80分 → 投递包 / 60分 → 投递+补强包 / 45分 → 转岗包 / 20分 → 学习路线包 ✓
```

Career Manager 从"简历生成器"→"职业决策系统"。

### 新增：Application Strategy Decision（Step 7）

`mode_d_job_application.md` Step 6 Targeted Discovery 之后插入：

| Strategy | Match Score | Package | 说明 |
|----------|-------------|---------|------|
| Strong Fit（强匹配） | ≥ 80 | Pack A | 投递包（6文件） |
| Moderate Fit（中等匹配） | 60-79 | Pack B | 投递+补强包（7文件，含Gap Analysis） |
| Stretch Fit（拉伸匹配） | 40-59 | Pack C | 转岗包（7文件，含Transition Resume） |
| Weak Fit（弱匹配） | < 40 | Pack D | 学习路线包（4文件，不生成简历） |

边界规则：Adjacent占比>60% + ≥40分 → 升为Stretch；Missing中含Critical(>30%) → 降一档；用户指定方向→不降档。

### 新增：英文简历默认生成

- `03_resume_en.md` — English ATS Resume，不是中文翻译，是直接编写的 ATS 优化英文简历
- 默认随 Strong/Moderate Fit 包生成，不需要用户额外要求

### 新增：7 个模板文件

| 文件 | 用途 | 适用 Pack |
|------|------|:--:|
| `03_resume_en.md` | 英文 ATS 简历 | A, B |
| `XX_gap_analysis.md` | 能力差距分析（Gap+补齐预估+影响评估） | B, C, D |
| `XX_transition_resume_cn.md` | 转岗中文简历（突出 Adjacent Match） | C |
| `XX_transition_resume_en.md` | 转岗英文简历 | C |
| `XX_transition_feasibility.md` | 转岗可行性评估（三维度评分+推荐路径） | D |
| `XX_learning_roadmap.md` | 学习路线图（3阶段+里程碑+资源推荐） | D |

### 新增：output_contracts.md（产出合约）

`references/output_contracts.md` — 4 个 Pack 的完整文件映射表 + 数据来源，确保产出可预期。

### 修改

- `02_ats_resume.md` → 重命名为 `02_resume_cn.md`
- `SKILL.md`: Mode D + 目录结构 + Resources 全面更新
- `career_dna_structure.md`: Resume Outputs 结构更新

### 文件变更

| 文件 | 类型 |
|------|------|
| `assets/templates/resume-outputs/02_ats_resume.md` | **重命名为 02_resume_cn.md** |
| `assets/templates/resume-outputs/03_resume_en.md` | **新增** |
| `assets/templates/resume-outputs/XX_gap_analysis.md` | **新增** |
| `assets/templates/resume-outputs/XX_transition_resume_cn.md` | **新增** |
| `assets/templates/resume-outputs/XX_transition_resume_en.md` | **新增** |
| `assets/templates/resume-outputs/XX_transition_feasibility.md` | **新增** |
| `assets/templates/resume-outputs/XX_learning_roadmap.md` | **新增** |
| `references/output_contracts.md` | **新增** |
| `references/mode_d_job_application.md` | 修改 |
| `SKILL.md` | 修改 |
| `references/career_dna_structure.md` | 修改 |

---

## v1.5 — 2026-07-22

### Online Career Profile（在线职业档案 v1.5）

**核心变化**：将 Boss 简历从"每次 JD 生成一次"的投递产物中移除，改为 Career DNA 的派生资产（Derived Asset）永久维护。

```
v1.4: Boss 简历 = resume-outputs/03_boss_resume.md（每次 JD 重新生成）
v1.5: Boss 简历 → career-dna/11_online_profile.md（DNA 更新时自动同步）
```

### 新增：11_online_profile.md（在线职业档案）

Career DNA 的派生资产，5 部分结构：

| Part | 内容 | 数据来源 |
|------|------|----------|
| Part 1: Personal Branding | Headline + 职业标签 + 核心竞争力 | `07_career_identity.md` |
| Part 2: Career Summary | 300-500 字职业简介 | `01` + `02` + `07` |
| Part 3: Core Competencies | 能力标签（Confidence ≥ 60） | `04_skill_graph.md` |
| Part 4: Highlight Projects | 代表项目 | `03_projects.md` + `10_career_tracks/` |
| Part 5: Target Tracks | Primary/Secondary/Supporting 分级 | `10_career_tracks/` |

**派生规则**：来源 DNA 文件更新 → 自动重新生成 Online Profile，避免双维护。

### 删除：03_boss_resume.md

从 `resume-outputs/` 删除。剩余文件编号前移（04→03, 05→04, 06→05）。

### 修改：07_career_identity.md

新增 3 个字段为 Online Profile 提供元数据：
- Branding Keywords（品牌关键词）
- Personal Headline（个人一句话定位）
- Career Summary（职业简介 300-500 字）

### 修改：career_track.md

新增 Online Positioning（在线展示定位）：Primary / Secondary / Supporting Track 分级。

### 修改：Mode A / Mode B

- Mode A Step 11：自动推导生成 `11_online_profile.md`
- Mode B Step 4.5：DNA 更新后自动刷新派生资产

### 修改：架构位置

| 改动 | 文件 |
|------|------|
| 目录结构 | `SKILL.md` |
| 结构定义 | `references/career_dna_structure.md` |
| Mode D Resume Package | 去 boss_resume 行，编号前移 |
| Resources 模板列表 | `SKILL.md` |
| init 脚本 | `scripts/init_career_dna.py`（+11_online_profile） |
| 完整度检查 | `scripts/completeness_checker.py`（+11, 权重 3） |

### 文件变更清单

| 文件 | 类型 |
|------|------|
| `assets/templates/career-dna/11_online_profile.md` | **新增** |
| `assets/templates/career-dna/07_career_identity.md` | 修改 |
| `assets/templates/career_track.md` | 修改 |
| `assets/templates/resume-outputs/03_boss_resume.md` | **删除** |
| `SKILL.md` | 修改 |
| `references/career_dna_structure.md` | 修改 |
| `references/mode_a_build.md` | 修改 |
| `references/mode_b_update.md` | 修改 |
| `references/mode_d_job_application.md` | 修改 |
| `scripts/init_career_dna.py` | 修改 |
| `scripts/completeness_checker.py` | 修改 |

---

## v1.4.4 — 2026-07-21

### Capability Translation（能力迁移分析）

**核心命题**：从"Match: 75%"升级为解释"为什么 75 分"，将匹配评分从关键词重叠模式升级为能力迁移推理。

```
v1.4.3: Skill Match = 关键词在Skill Graph中是否存在
v1.4.4: Capability Match = Direct(100%) + Adjacent(60%) + Missing(0%) 加权计算
```

### 新增：Part 6.5 Capability Translation Analysis（能力迁移分析）

`01_jd_match_report.md` Part 6 新增 4 个子区块：

- **Direct Match（直接匹配）**：JD Skill = DNA Skill，同名能力直通 → 100% 计入
- **Adjacent Match（迁移匹配）**：JD Skill ≈ DNA Skill，不同名但证据链可迁移 → 60% 计入，附推理过程 + 映射置信度
- **Missing Match（缺失匹配）**：无可信迁移路径 → 0%，记录原因
- **Mapping Boundary Check（映射边界检查）**：明确拒绝 Speculative Match（跨行业跳跃 / 无证据关联）

### 新增：Step 5.5 Capability Translation（能力迁移推理）

`mode_d_job_application.md` Step 5 和 Step 6 之间插入，定义完整推理规则：

**Adjacent Match 判定规则（4条）**：
1. 同一 Domain（域内迁移）→ Confidence 70-85
2. Related Skills（关联能力）→ Confidence 60-75
3. 业务场景交叉（工作交叉）→ Confidence 50-65
4. Skill Snapshot Alias 命中 → Confidence 80-90

**Speculative Match 禁止规则**：跨行业跳跃、无证据关联、领域无交集 → 强制归入 Missing

### 修改：Match Score 计算

`Skill Match(30%)` 改为 `Capability Match(30%)`，计算公式：
```
Capability Score = (Direct数量×100 + Adjacent数量×60 + Missing数量×0) / 总JD能力数
```

### 新增：Common Capability Transitions（常见能力迁移路径 P1）

`role_snapshot.md` 新增市场观察模块，基于多次 JD 分析积累的常见迁移路径：
- QA Lead → Project Delivery / Stakeholder Management
- Implementation Consultant → Requirement Analysis
- 附观察次数 + 置信度，用于 Adjacent Match 加分参考

### 不改的文件

- `04_skill_graph.md` — 保持职责清晰：用户能力（静态事实）
- `career_track.md` — 保持职责清晰：赛道适合度（个人资产）
- `question_backlog.md` — 不需要绑定 Capability Translation

### 文件变更

| 文件 | 变更 |
|------|------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | Skill→Capability + Part 6.5 新增 |
| `references/mode_d_job_application.md` | 匹配维度改 + Step 5.5 新增 + 管线图更新 |
| `assets/templates/knowledge/role_snapshot.md` | Common Capability Transitions（P1） |

---

## v1.4.3 — 2026-07-20

### Bilingual Readability Enhancement（中英双语可读性增强）

纯文本可读性升级，不影响任何架构、功能、文档实质内容。

**修改范围**：对全文件进行扫描，为缺少中文注释的英文术语补充中英释义。主要覆盖：

- **文档/模板标题**：`Overview` → `Overview（概述）` 等 4 处
- **模板字段名**：`Track` → `Track（职业赛道）` / `Frequency` → `Frequency（出现频率）` 等 30+ 处
- **表格列标题**：`Evidence Count` → `Evidence Count（证据数）` / `Expected Ownership` → `Expected Ownership（期望责任级别）` 等 12+ 处
- **行文中的字段/概念列表**：`Hiring Intent / Talent Persona / Evidence Expectation` → 加入中文，共 8 处
- **枚举值/状态值**：`Validated / Emerging / Uncertain` → `Validated（已验证）/ Emerging（新兴）/ Uncertain（不确定）` 等 3 处
- **章节标题**：`Part 1: JD Metadata` → `Part 1: JD Metadata（JD元信息）` 等 8 处

**修改文件**（11个）：

| 文件 | 改动类型 |
|------|----------|
| `SKILL.md` | 标题 + 字段列表 |
| `references/mode_d_job_application.md` | 行内注释 + 概念引用 |
| `references/career_dna_structure.md` | 文档标题 + Part 名称 + 字段列表 |
| `references/question_backlog.md` | 表格列标题 + 字段列表 |
| `CHANGELOG.md` | 概念列表 + 章节标题 |
| `assets/templates/career-dna/04_skill_graph.md` | 表格列标题 (12+列) |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 表格列标题 + 枚举值 |
| `assets/templates/career_track.md` | 模板标题 + 枚举值 + 列标题 |
| `assets/templates/knowledge/role_snapshot.md` | 模板标题 + 字段名 (9个) |
| `assets/templates/knowledge/skill_snapshot.md` | 模板标题 + 字段名 (12+个) |

**不受影响**：架构、工作流、推理逻辑、目录结构、脚本 — 全部不变。

---

## v1.4.2 — 2026-07-20

### Explainable Intelligence Upgrade（可解释智能升级）

核心目标：让系统能解释**每一个评分、每一个推荐、每一个 Gap 的依据**，从"AI觉得如此"变成"AI能说明依据"。

### P0: Score Explainability Layer（评分可解释层）

**04_skill_graph.md 重构 Confidence 计算逻辑**：
- 从单维 `Evidence Count × Recency` 升级为 `Evidence Count Quality(40pt) + Evidence Quality(30pt) + Recency(30pt) + Consistency Bonus(+5pt)` 四维分解
- 新增 Evidence Quality（证据质量: 角色/量化/认可）、Evidence Consistency（证据一致性: 多项目持续展现）、Evidence Recency（证据时效性）
- 新增 Confidence 计算逻辑说明和评分标准表

**career_track.md 新增 Track Confidence Breakdown（赛道置信度分解）**：
- Track Confidence = Evidence Strength(40%) + Role Snapshot Validation(35%) + Market Demand(25%) 三分量
- 每个分量附计算方式和评分解读
- Market Intelligence（市场情报）新增 Validation Status（验证状态） / Recent JD Coverage（近期JD覆盖率） / Market Signal（市场信号）

**01_jd_match_report.md 新增 Score Breakdown（评分分解） + Evidence Basis（证据基础）**：
- Score Breakdown 表格：Persona/Evidence/Skill 三匹配的得分×权重×加权得分完整展开
- 新增 Score Confidence（评分置信度）和 Evidence Basis（证据数量/质量/缺失项）
- 缺失证据按 Skill Weight 排序，权重越高的缺失影响越大

### P0: Question Backlog JD Binding（问题库 JD 上下文绑定）

**08_question_backlog.md 新增 Triggered By 字段**：
- Triggered By JD / Role / Company / Track 四个 JD 上下文绑定
- 实现溯源：每个 Backlog 问题可追溯至触发它的具体 JD

**references/question_backlog.md 新增规则 7**：
- JD 绑定生成链路：Evidence Gap → Backlog Question → 自动绑定 JD 上下文
- 作用：同 Track 聚合展示、公司优先级排序、数据溯源、职业成长任务池

### P1: Career Track Market Validation Engine（市场验证引擎）

**mode_a_build.md Step 9.2 升级**：
- Track Confidence 从单数字升级为三分量加权计算（Evidence × 40% + Role Validation × 35% + Market Demand × 25%）
- 新增 Market Demand 分级（≥10JD=90pt / 5-9=70pt / <5=50pt）

**mode_d_job_application.md Knowledge Update C 增强**：
- 新增 Track Confidence Breakdown 重新计算
- 新增 Validation Status 更新（Validated / Emerging / Uncertain）
- 新增 Recent JD Coverage / Market Signal

### P1: Persona Statistics（画像统计层）

**role_snapshot.md 新增 Persona Statistics 区块**：
- Experience Frequency（典型经历频率: 含趋势 ↑↓→）
- Career Background Frequency（职业背景分布频率）
- Trait Frequency（偏好特质频率）
- ≥5 次观察后生成，将 Talent Persona 从 AI 总结升级为统计结论

### 文件变更清单

| 文件 | 变更类型 | 优先级 |
|------|----------|--------|
| `assets/templates/career-dna/04_skill_graph.md` | Confidence 四维分解 + Quality/Consistency/Recency | P0 |
| `assets/templates/career_track.md` | Track Confidence Breakdown + Market Validation v1.4.2 | P0 |
| `assets/templates/resume-outputs/01_jd_match_report.md` | Score Breakdown（评分分解） + Evidence Basis（证据基础） | P0 |
| `assets/templates/career-dna/08_question_backlog.md` | Triggered By JD/Role/Company/Track | P0 |
| `references/question_backlog.md` | 规则 7: JD 绑定生成 | P0 |
| `references/mode_a_build.md` | Step 9.2 Confidence 三分量升级 | P1 |
| `references/mode_d_job_application.md` | Knowledge Update C 增强 + 逻辑总结更新 | P1 |
| `assets/templates/knowledge/role_snapshot.md` | Persona Statistics | P1 |

---

## v1.4.1 — 2026-07-20

### Evidence Intelligence Enhancement（证据智能增强）

v1.4 的 Talent Intelligence 管线已覆盖 Hiring Intent（招聘意图） / Talent Persona（人才画像） / Evidence Expectation（证据期望），但三个关键推理链尚未闭环。v1.4.1 补齐这三个链路，为 v1.5 Skill Mapping Engine（技能映射引擎）提供稳定地基。

### 新增：Skill Weight Analysis（能力权重分析）

- `01_jd_match_report.md` 新增 Part 4.5：从 JD 措辞 × Role Snapshot 频率 × 行业常识三维度推理各能力权重，输出总和 100% 的权重表
- `references/mode_d_job_application.md` 新增 Step 3.5：Skill Weight Analysis 推理逻辑 + 输出格式
- 用途：DNA Match Gap 按权重加权评分 → 未来 Skill Mapping 判断"缺什么最严重"

### 新增：Evidence Expectation 结构化

- `01_jd_match_report.md` Part 5 重写：Critical Evidence 表格新增 Expected Ownership / Expected Scope / Expected Impact 三维度 + Evidence Scoring Rule
- `references/mode_d_job_application.md` Step 4 推理维度更新：新增 Ownership(Owner/Lead/Support) × Scope(Global/Dept/Team) × Impact(Revenue/Efficiency/Delivery/Quality)
- Evidence Score = Ownership + Scope + Impact（3-9pt）

### 新增：Skill Snapshot Alias（能力快照别名）

- `assets/templates/knowledge/skill_snapshot.md`：每个 Skill 新增 Aliases 字段（JD 中的同义表述）
- Alias 示例：Stakeholder Management → 跨部门沟通, 资源协调, 项目推动, 组织协调
- 用途：v1.5 Skill Mapping 的同义词映射基础

### Knowledge Update 增强

- Role Snapshot 新增 Skill Weight Baseline 累积
- Skill Snapshot 新增 Aliases 自动合并 + Typical Ownership 均值统计
- Knowledge Update 逻辑总结更新

### 文件变更

| 文件 | 变更类型 |
|------|----------|
| `assets/templates/resume-outputs/01_jd_match_report.md` | Part 4.5 新增 + Part 5 重写 |
| `references/mode_d_job_application.md` | Step 3.5 新增 + Step 4 结构化 + Knowledge Update 更新 |
| `assets/templates/knowledge/skill_snapshot.md` | 每个 Skill 新增 Aliases 字段 |

---

## v1.4 — 2026-07-20

### Talent Intelligence Upgrade（人才画像智能分析升级）

**核心转变**：从 JD Keyword Extraction（关键词提取）升级为 Talent Persona Inference（人才画像推理）。

不新增顶层目录，保持 `career-dna/` / `knowledge/` / `resume-outputs/` 结构稳定。改的是**推理逻辑、模板结构、知识沉淀内容**。

```
v1.3.1: JD → 职责 → 技能 → 简历
v1.4:   JD → 招聘意图 → 人才画像 → 证据要求 → DNA匹配 → 简历生成
```

### 新增：Mode D 人才智能分析管线（4 个新步骤）

**Step 1: Role Decomposition（岗位能力拆解）**
- 从技能列表升级为 Core Functions / Responsibilities / Expected Ownership 三层拆解

**Step 2: Hiring Intent Analysis（招聘意图分析）**
- 推理 Explicit / Implicit Requirements / Business Context / Pain Point

**Step 3: Talent Persona Inference（人才画像推理）**
- 输出 Ideal Candidate natural-language 描述 / Career Background / Typical Experience / Preferred Traits

**Step 4: Evidence Expectation Analysis（证据需求分析）**
- 输出 Critical Evidence / Expected Stories / Expected Results / Evidence Risks

**Step 5 DNA Match Analysis 升级**：
- 匹配从 Skill Match 单一维度升级为 Persona Match(35%) + Evidence Match(35%) + Skill Match(30%)

### 修改：JD Match Report 重构为 6 部分

```
Part 1: JD Original（JD 原文）
Part 2: Role Decomposition（岗位拆解）
Part 3: Hiring Intent（招聘意图）
Part 4: Talent Persona（人才画像）
Part 5: Evidence Expectation（证据需求）
Part 6: DNA Match Analysis（匹配分析）
```

### 修改：Knowledge Layer 增强（Role + Skill Snapshot）

**role_snapshot.md (v1.4 增强)**：
- `Hiring Intelligence` 区块：Common Hiring Intent（常见招聘意图） / Talent Persona（人才画像） / Typical Evidence（典型证据） / Career Background Distribution（职业背景分布）
- `Trend Intelligence` 区块：Hiring Intent Trends / Talent Persona Trends / Evidence Trends

**skill_snapshot.md (v1.4 增强)**：
- 每个 Skill 新增 `Talent Intelligence` 区块：Typical Evidence / Business Meaning / Related Hiring Intent / Typical Results / Typical Ownership

### 修改：Career Track 增强

- `career_track.md` 新增 Market Intelligence 区块：Market Validation / Matched Hiring Intent / Market Demand Signals / Evidence Strength

### 修改：Question Backlog 增强

- 新增 Related Hiring Intent / Related Evidence 字段
- 支持从 Evidence Expectation 的 Evidence Risks 自动生成 Backlog 问题

### 修改：Knowledge Update Logic

从 `JD → Skills → Snapshot` 升级为：
```
JD → Talent Persona → Role Snapshot（Hiring Intent + Talent Persona）
JD → Evidence Expectation → Skill Snapshot（Typical Evidence + Business Meaning）
```

### 文件变更清单

| 文件 | 变更类型 |
|------|----------|
| `references/mode_d_job_application.md` | 完全重写：9 步流程 + Talent Intelligence Pipeline |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 完全重写：6 部分结构 |
| `assets/templates/knowledge/role_snapshot.md` | 修改：新增 Hiring Intelligence + Trend Intelligence |
| `assets/templates/knowledge/skill_snapshot.md` | 修改：每个 Skill 新增 Talent Intelligence 区块 |
| `assets/templates/career_track.md` | 修改：新增 Market Intelligence 区块 |
| `assets/templates/career-dna/08_question_backlog.md` | 修改：新增 Hiring Intent / Evidence 字段 |
| `references/question_backlog.md` | 修改：问题格式更新 v1.4 |
| `SKILL.md` | 修改：Mode D 完全重写 |
| `references/career_dna_structure.md` | 修改：Knowledge Layer v1.4 结构 |

### v1.4 验收标准

同一份 JD "实施顾问"，系统应输出：
```yaml
人才画像: 有项目推进经历、能独立面对客户、具备需求梳理能力、能承担交付责任
核心证据: 需求调研案例、客户培训案例、项目交付案例
招聘意图: 寻找能够独立交付项目的人
```

---

## v1.3.1 — 2026-07-20

### 修复：Mode A Career Track Discovery 空壳 + Backlog 闭环 + 路径修正

**问题 1**：`references/mode_a_build.md` 中 Step 1 和 Step 9 仍引用旧的单文件路径 `career-dna/10_career_tracks.md`，与 v1.3 的目录模式不一致。

**问题 2**：Mode A Step 9 Career Track Discovery 只写"识别 2-4 个方向"就结束，没有实际生成 `{track}.md` 文件，导致发现方向和创建 Track 之间断开。

**问题 3**：Question Backlog 只有 `发现 → 记录 → 结束` 的单向流，没有关联到 Track / Gap / Skill，以后无法自动按优先级排序。

### 修改：mode_a_build.md

- Step 1：文件数量描述修正为 `"9 个模板文件 + 10_career_tracks/ 目录"`
- 工作流标题：`"9 步工作流"` → `"10 步工作流"`
- Step 9 完全重写为 5 个子步骤（9.1-9.5）：识别 Track → Confidence 评估 → 生成完整 `{track}.md` → 更新 README → 关联 Backlog
- 新增规则：Track 文件必须生成，信息不足标注 `[待补充]` 记入 Backlog，不阻塞
- Important Rules 新增：规则 5（Track 文件必须生成）、规则 6（Backlog 问题必须关联 Track）

### 修改：SKILL.md

- Mode A 工作流描述更新：明确"发现职业方向并生成 Career Track 文件"
- 产物描述更新：`"9 个文件 + 10_career_tracks/ 目录"`

### 修改：Question Backlog 闭环

- `references/question_backlog.md`：问题格式新增 4 个字段 — Track / Related Gap / Related Skill / Potential Impact
- 新增字段说明表 + Impact 估算参考
- Open → Answered 流转新增 Track 回写步骤
- 新增规则 6：关联 Track 优先排序（按 Impact 降序 + Track Confidence 升序）
- `08_question_backlog.md` 模板同步更新

### 文件变更

| 文件 | 变更类型 |
|------|----------|
| `references/mode_a_build.md` | Step 1/9/10 + 规则重写 |
| `SKILL.md` | Mode A 产物/工作流修正 |
| `references/question_backlog.md` | 问题格式 + 流转 + 规则 6 |
| `assets/templates/career-dna/08_question_backlog.md` | 模板更新 |

---

## v1.3 — 2026-07-18

### 职责收敛：消除 job-tracks 与 role_snapshots 的重叠

**核心目标**：不再增加新模块，而是进行职责收敛（Responsibility Consolidation）。

v1.2 中 `job-tracks/` 与 `knowledge/role_snapshots/` 均在维护岗位画像、职责、技能、统计，职责重叠超过 80%。v1.3 彻底删除 `job-tracks/`，将个人赛道回归 Career DNA。

**本质变化**：
```
V1.2: 市场画像(Job Tracks) + 市场画像(Role Snapshots) → 重叠
V1.3: 个人赛道(Career Tracks) + 市场画像(Role Snapshots) → 互补
```

### 删除：job-tracks/ 目录

整个 `job-tracks/` 目录及模板 `track_profile.md` 被删除。其市场统计数据已转移到 `knowledge/role_snapshots/`，其 Role 特征描述已转移到 `career-dna/10_career_tracks/`。

### 重构：10_career_tracks 从单文件改为目录

```
v1.2: career-dna/10_career_tracks.md  (单文件)
v1.3: career-dna/10_career_tracks/     (目录)
      ├── README.md                    (赛道总览)
      ├── project_manager.md          (项目经理赛道)
      ├── implementation_consultant.md (实施顾问赛道)
      └── ...                         (更多赛道文件)
```

每个 Track 文件回答"为什么用户适合这个方向"，而非"市场需要什么"。

### 新增：Career Track 模板

`assets/templates/career_track.md` — 包含 Track / Confidence / Positioning / Career Narrative / Evidence / Core Strengths / Recommended Projects / Recommended Stories / Known Gaps / Improvement Priorities / Target Roles。

### 增强：Knowledge Layer 模板

**role_snapshot.md (v1.3 增强)**：
- 新增 Observed Companies（已观察到的公司列表）
- 新增 Recent JD Sources（最近 JD 来源，格式 YYYY-MM Company Role）
- 新增 Trend Notes（基于多次观察的趋势判断）
- 新增 Company Distribution 表

**skill_snapshot.md (v1.3 增强)**：
- 每个 Skill 新增 Observed JD Count
- 新增 Related Roles / Recent Observations（最近观察记录）
- 新增 Trend Notes（基于累计数据的趋势判断）

### 修改：Mode D 工作流程

- 删除所有 job-tracks/ 相关逻辑
- Step 1 重写为 Career Track Match：JD → Role Snapshot 获取市场基线 → Career Track 匹配 → DNA Skill Graph 交叉比对
- Step 4 Career DNA Update 增加 Career Track 更新（Confidence / Evidence / Known Gaps / Improvement Priorities）
- Step 6 Knowledge Update 增加 Career Track 更新步骤

### 修改：JD Match Report 模板

`01_jd_match_report.md` 从单一的匹配分析模板重构为四个部分：
1. **JD Metadata** — Company / Role / Date / Source / Track
2. **Original JD** — 完整 JD 原文存档（用于回溯）
3. **AI Extracted Summary** — Core Responsibilities / Must Have / Nice To Have / Tools / Keywords / Risk Factors
4. **Match Analysis** — Match Score / Strengths / Gaps / 推荐项目/故事 / High Risk Questions / ATS Keywords

### 修改：Resume Outputs 命名规则

子目录命名从 `{YYYYMMDD}_{company}_{role}` 改为 `{YYYYMMDD}-{company}-{role}`（连字符分隔）。

### 文件变更清单

| 文件 | 变更类型 |
|------|----------|
| `SKILL.md` | 修改：三层架构去 Job Tracks、目录结构更新、Mode D 流程更新、Knowledge/Career Track Rules 重写 |
| `references/mode_d_job_application.md` | 完全重写：去 job-tracks、Career Track Match 流程、JD Match Report 四部分结构 |
| `references/career_dna_structure.md` | 修改：10_career_tracks 目录模式、External Knowledge Layer v1.3、删 Track Profile、新增 Resume Outputs 结构 |
| `assets/templates/career_track.md` | 新增：Career Track 赛道模板 |
| `assets/templates/knowledge/role_snapshot.md` | 修改：新增 Observed Companies / Recent JD Sources / Trend Notes |
| `assets/templates/knowledge/skill_snapshot.md` | 修改：新增 Observed JD Count / Related Roles / Recent Observations / Trend Notes |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 修改：新增 JD Metadata / Original JD / AI Extracted Summary |
| `assets/templates/career-dna/10_career_tracks.md` | 删除 |
| `assets/templates/job-tracks/` | 整个目录删除 |
| `scripts/init_career_dna.py` | 修改：9 个单文件 + 10_career_tracks/ 目录 + README.md，去 job-tracks |
| `scripts/completeness_checker.py` | 修改：支持 directory 模式检查 10_career_tracks/ |

### V2 规划（暂未实现）

- `role_library/`, `skill_library/`, `ontology/`, `career_recommendation_engine/`, `career_path_prediction/`

---

## v1.2 — 2026-07-17

### 重大重构：四层分离（职责解耦）

v1.2 明确将资产分离为四层，每层有清晰的职责边界：

```
Career DNA = 个人职业资产库    (career-dna/)
Knowledge = 职业市场知识库    (knowledge/)
Job Tracks = 岗位赛道画像库    (job-tracks/)
Resume Outputs = 单次JD投递产物  (resume-outputs/{date}_{company}_{role}/)
```

**关键变更**：
- Job Tracks（原名 JD Track）职责大幅简化：仅保存 Role 级别市场画像，不保存用户个人数据
- Resume Outputs 从单层文件改为按日期+公司+岗位子目录隔离，每次投递独立
- Mode D 流程重构：Track Match → JD Match Report → Resume Package → Knowledge Update

### 新增：Track Match（赛道匹配）

Mode D Step 1 新增 Track Match 步骤，解析 JD 后先识别 Role，定位/创建对应 Track Profile，获得市场基线后再做匹配分析。

### 新增：JD Match Report（岗位匹配报告）

新增 `resume-outputs/{date}_{company}_{role}/01_jd_match_report.md`，合并原来独立的 JD Analysis 和 Match Analysis，作为所有后续求职材料的唯一数据源。包含：Match Score / Strengths / Gaps / Recommended Projects / Recommended Stories / High Risk Questions / ATS Keywords。

### 修改：Skill Snapshots 改为 Domain 模式

`knowledge/skill_snapshots/` 从按单个 Skill 归档（如 `stakeholder_management.md`）改为按 Domain 归档（如 `project_management.md`），一个 Domain 文件下包含多个 Skill，支持 Skill 间关联关系追踪。

### 修改：Job Tracks 改为 Role 模式 + 减负

`job-tracks/` 文件命名从 `{company}_{role}.md` 改为 `{role_name}.md`（如 `project_manager.md`）。模板从 `jd_track.md` 重命名为 `track_profile.md`。移除：Match Score / Recommended Projects / Recommended Stories / Gap Analysis / 面试风险 / 投递建议。保留：Track / Aliases / Core Responsibilities / Must Have Skills / Nice To Have Skills / Common Tools / Industries / Observed JD History。

### 修改：Resume Outputs 改为子目录模式

`resume-outputs/` 从单层文件改为 `{YYYYMMDD}_{company}_{role}/` 子目录结构，每次投递创建独立子目录。模板文件加编号前缀（01-06），新增 `01_jd_match_report.md`。

### 修改：Skill Graph 新增字段

`04_skill_graph.md` 新增 Domain（能力域）和 Related Skills（关联能力）字段，用于 Skill Domain Snapshot 同步。

### 修改：Career Tracks 增强字段

`10_career_tracks.md` 新增 Positioning（职业定位）、Core Strengths（核心优势）、Recommended Projects（推荐项目）、Recommended Stories（推荐故事）、Target Roles（目标岗位）字段，为 JD Match Report 和简历生成提供数据源。

### 修改：Mode D 工作流程重构

```
原 v1.1: JD Analysis → DNA Match Analysis → Targeted Discovery → Career DNA Update → JD Track Builder → Application Package → Knowledge Update
新 v1.2: Track Match → JD Match Report → Targeted Discovery → Career DNA Update → Resume Package → Knowledge Update
```

### 文件变更清单

| 文件 | 变更类型 |
|------|----------|
| `SKILL.md` | 修改：三层架构、四层产物定义、Mode D 流程重构、目录结构更新、Knowledge/Job Tracks Rules |
| `references/mode_d_job_application.md` | 完全重写：6 步新流程 + Track Match + JD Match Report + 子目录模式 |
| `references/career_dna_structure.md` | 修改：04_skill_graph Domain/Related Skills、10_career_tracks v1.2 字段、External Knowledge Layer v1.2、新增 Track Profile / Resume Outputs 结构 |
| `assets/templates/knowledge/skill_snapshot.md` | 完全重写：Domain 模式 |
| `assets/templates/job-tracks/jd_track.md` | 删除 → 替换为 `track_profile.md` |
| `assets/templates/job-tracks/track_profile.md` | 新增：Role 级别市场画像 |
| `assets/templates/resume-outputs/01_jd_match_report.md` | 新增：岗位匹配报告 |
| `assets/templates/resume-outputs/02-06_*.md` | 重命名：加编号前缀，02_ats_resume 和 03_boss_resume 增加 Track 引用 |
| `assets/templates/career-dna/04_skill_graph.md` | 修改：新增 Domain、Related Skills 字段、Domain 映射参考 |
| `assets/templates/career-dna/10_career_tracks.md` | 修改：新增 Positioning、Core Strengths、Recommended Projects、Recommended Stories、Target Roles |

### V2 规划（暂未实现）

- `role_library/` — 角色知识库
- `skill_library/` — 能力知识库
- `ontology/` — 职业本体论
- `career_recommendation_engine/` — 职业推荐引擎
- `career_path_prediction/` — 职业路径预测

---

## v1.1 — 2026-07-11

### 新增：Knowledge Layer（职业市场知识层）

引入双层架构，将个人资产与市场资产物理隔离：

- **Career DNA Layer（职业资产层）**：用户个人经历、能力、项目、故事 — 存放在 `career-dna/`
- **Knowledge Layer（市场知识层）**：外部市场情报、岗位快照、能力快照 — 存放在 `knowledge/`

新增目录：
- `knowledge/role_snapshots/` — 岗位快照 (Role Snapshot)
- `knowledge/skill_snapshots/` — 能力快照 (Skill Snapshot)

新增模板文件：
- `assets/templates/knowledge/role_snapshot.md`
- `assets/templates/knowledge/skill_snapshot.md`

### 新增：Mode D Step 7 — Knowledge Update（知识更新）

Mode D 工作流从 6 步扩展为 7 步，新增最后一步：

```
Step 1: JD Analysis（岗位分析）
Step 2: DNA Match Analysis（基因库匹配分析）← 重命名，原 JD Match Analysis
Step 3: Targeted Discovery（定向证据发现）
Step 4: Career DNA Update（职业资产回写）
Step 5: JD Track Builder（岗位专属画像生成）
Step 6: Application Package Generator（求职材料生成）
Step 7: Knowledge Update（知识更新）← 新增
```

Step 7 从 JD 中提取 Role / Track / Skills / Tools / Keywords，更新到 Knowledge Layer。

### 新增：Skill Graph 置信度字段

`career-dna/04_skill_graph.md` 新增 4 个字段：

| 字段 | 说明 |
|------|------|
| Evidence | 证据来源列表 |
| Evidence Count | 证据数量 |
| Confidence | 置信度评分 (0-100) |
| Last Verified | 最近验证时间 (YYYY-MM) |

这些字段用于 Role Snapshot vs Skill Graph 交叉比对，以及 Targeted Discovery 追问优先级判断。

### 修改：Targeted Discovery 新增 Role Snapshot 引用

Targeted Discovery 新增第三个数据源：Role Snapshot。

追问逻辑升级：

```
JD 要求 → Role Snapshot 中存在？ → DNA 有证据？ → 进入追问
```

优先级从 4 级扩展为 5 级，新增基于 Role Snapshot 的隐性能力发现。

### 修改：中英双语释义

全文件增加中英双语标注，提高可读性：
- 目录结构注释增加英文名
- Mode 路由表增加中文名
- 字段表格增加英文列名
- 步骤名称增加中文释义

### 文件变更清单

| 文件 | 变更类型 |
|------|----------|
| `SKILL.md` | 修改：新增 Two-Layer Architecture、Knowledge Layer Rules、Principle 6、Mode D 7步、中英释义 |
| `references/mode_d_job_application.md` | 修改：Step 2 重命名、新增 Step 7 Knowledge Update、新增 Role Snapshot 引用 |
| `references/targeted_discovery.md` | 修改：新增 Role Snapshot 引用源、追问逻辑升级、优先级扩展为 5 级 |
| `references/career_dna_structure.md` | 修改：04_skill_graph 新增字段、新增 External Knowledge Layer 章节 |
| `assets/templates/career-dna/04_skill_graph.md` | 修改：新增 Evidence/Evidence Count/Confidence/Last Verified 字段 |
| `assets/templates/knowledge/role_snapshot.md` | 新增 |
| `assets/templates/knowledge/skill_snapshot.md` | 新增 |
| `scripts/init_career_dna.py` | 修改：新增 knowledge/ 目录创建 |

### V2 规划（暂未实现）

以下功能将在 V2 版本中实现：
- `role_library/` — 角色知识库
- `skill_library/` — 能力知识库
- `ontology/` — 职业本体论
- `career_recommendation_engine/` — 职业推荐引擎
- `career_path_prediction/` — 职业路径预测

---

## v1.0 — 2026-07-10

### 初始版本

Career Manager 技能首发版本，包含完整的四大工作模式：

- **Mode A: Career DNA Build Mode（职业基因库构建模式）** — 9 步工作流，构建 10 个 Career DNA 文件
- **Mode B: Career DNA Update Mode（职业资产更新模式）** — 增量回写，完整度重算
- **Mode C: Career Review Mode（职业发展分析模式）** — 职业方向分析、能力差距分析、成长路线图
- **Mode D: Job Application Mode（岗位投递模式）** — 6 步工作流，JD 匹配 + 求职材料生成

初始文件结构：
- `career-dna/` — 10 个职业资产文件
- `job-tracks/` — 岗位专属分析库
- `resume-outputs/` — 5 个求职材料文件
- `scripts/init_career_dna.py` — 初始化脚本
- `scripts/completeness_checker.py` — 完整度检查脚本
- `references/` — 7 个详细参考文件
- `assets/templates/` — 16 个模板文件
