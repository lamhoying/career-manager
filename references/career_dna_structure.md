# Career DNA Structure Reference（职业基因库结构参考）

Career DNA 是用户职业经历的唯一事实源（Single Source of Truth），文件清单**以 `assets/career_dna_manifest.json` 为唯一定义源**：9 个核心文件（01-09）+ 4 个派生资产（04b / 11 / 12 / 13）+ 1 个目录型模块（`10_career_tracks/`）。以下为每个文件的字段定义、填写规范和示例格式。

---

## 写入契约（Write Contract v2.10.0）

`career-dna/` 根目录**只允许存在 manifest 中已登记的文件**。约束对象是「未登记文件」，不是「禁止新增」——职业资产本应持续成长（Core Principle #4），但新增必须走正规登记。

| 场景 | 正确落点 | 说明 |
|------|----------|------|
| 单次投递产物（JD 分析 / 简历 / 面试包 / 差距分析） | `resume-outputs/{YYYYMMDD}-{company}-{role}/` | 一次性，不进 SSOT |
| 某次提问生成的临时分析、草稿、策略稿 | `career-dna/_inbox/` | 下划线前缀 = 非 SSOT，不计完整度，可随时清理 |
| 确需长期保留的新资产 | `career-dna/` 根目录 **+ 四件套登记** | 见下 |
| 已有资产的更新 | 直接改对应文件 | 改完跑 `validate_career_dna.py` |

**新增文件的四件套登记**（缺一不可，且随 skill 版本号发布）：

1. 在 `assets/career_dna_manifest.json` 增加条目（`filename` / `name` / `desc` / `weight` / `kind`）
2. 在 `assets/templates/career-dna/` 提供同名模板
3. 给出权重（派生资产档 4-6；纯生成物填 `weight: 0` 并在 `desc` 注明理由，如 09）
4. 同步 `SKILL.md` 的目录树、Mode A 产物计数与 Resources 清单

**自检**：`python3 scripts/validate_career_dna.py <career-dna目录>` —— 只报告不修改；有 P0/P1 时退出码 1。检出项：P0 orphan（未登记文件）/ P0 duplicate-content（跨文件长段落逐字重复）/ P1 missing / P1 unregistered-dir / P2 派生资产缺时间戳。

---

---

## 01_profile.md — 个人职业档案

```markdown
# 个人职业档案 (Profile)

## 基础信息
- **姓名**：
- **当前岗位**：
- **工作年限**：
- **所在城市**：
- **联系方式**：（可选，不强制收集）

## 教育背景
| 时间 | 学校 | 专业 | 学历 | 备注 |
|------|------|------|------|------|

## 语言能力
| 语言 | 水平 | 证据（如证书/使用场景） |
|------|------|------------------------|

## 资格认证
| 认证名称 | 颁发机构 | 获得时间 | 有效期 |
|----------|----------|----------|--------|

## 其他
- **可接受工作地点**：
- **求职状态**：（在职/离职/观望）
```

---

## 02_timeline.md — 职业发展轨迹

```markdown
# 职业发展轨迹 (Career Timeline)

## 时间线总览

| # | 起止时间 | 公司 | 部门 | 岗位 | 离职原因 |
|---|----------|------|------|------|----------|

## 晋升路径

### [公司名]
- 入职岗位 → 当前岗位
- 晋升记录：
  - [时间] [岗位A] → [岗位B]（原因：晋升/转岗/组织调整）

## 职业轨迹分析
- **行业轨迹**：
- **职能轨迹**：
- **管理轨迹**：
- **关键转折点**：
```

---

## 03_projects.md — 项目资产库

每个项目按以下结构记录：

```markdown
# 项目资产库 (Project Asset Library)

## 项目 1：[项目名称]

### 基本信息
- **时间**：[起止时间]
- **公司**：
- **角色/岗位**：
- **项目规模**：（团队人数、预算、周期）
- **项目背景**：（1-2句话说明为什么做这个项目）

### 职责与贡献
- **核心职责**：
- **具体贡献**：（用动词开头，量化结果）
  1. 做了什么 → 产出了什么 → 效果如何
  2. ...

### 成果
- **量化成果**：（数字、百分比、金额、时间）
- **定性成果**：（认可、评价、影响）

### 可复用证据
- **数据**：
- **文档**：
- **案例**：
- **推荐人**：（可选）

### 标签
- **涉及能力**：[能力1, 能力2, ...]
- **项目类型**：[交付/管理/转型/创新/...]
```

---

## 04_skill_graph.md — 能力图谱

```markdown
# 能力图谱 (Skill Graph)

## 核心能力

| 能力 (Skill) | Domain（域） | 等级 (Level) | Evidence（证据来源） | Evidence Count | Confidence | Last Verified | Related Skills（关联能力） |
|---------------|-------------|-------------|---------------------|----------------|------------|---------------|--------------------------|

### 能力等级定义 (Level Definition)
- **Expert（专家）**：能独立主导，能教导他人，有多次成功实践
- **Proficient（熟练）**：能独立完成，有2次以上实践
- **Familiar（熟悉）**：能辅助完成，有1次实践
- **Aware（了解）**：知道概念，无独立实践

### Confidence 等级参考 (Confidence Reference)
| Confidence | 含义 | 证据要求 |
|------------|------|----------|
| 85-100 | 高置信 | Evidence Count >= 3，最近 6 个月内验证 |
| 60-84 | 中置信 | Evidence Count = 2，最近 12 个月内验证 |
| 30-59 | 低置信 | Evidence Count = 1，验证时间可能较久 |
| 0-29 | 待确认 | Evidence Count = 0，应进入 Backlog |

## 能力分类 (Skill Categories)

### 硬技能 (Hard Skills)
| 能力 | 等级 | Evidence | Evidence Count | Confidence | Last Verified | 应用场景 |
|------|------|----------|----------------|------------|---------------|----------|

### 软技能 / 管理能力 (Soft Skills / Management)
| 能力 | 等级 | Evidence | Evidence Count | Confidence | Last Verified | 应用场景 |
|------|------|----------|----------------|------------|---------------|----------|

### 领域知识 (Domain Knowledge)
| 领域 | 深度 | Evidence | Evidence Count | Confidence | Last Verified |
|------|------|----------|----------------|------------|---------------|

## 能力缺口 (Skill Gaps)
- [列出明显缺失的关键能力]
```

### v1.2 字段说明

| 字段 | 类型 | 版本 | 说明 |
|------|------|------|------|
| Domain | 文本 | v1.2 | 该 Skill 所属的能力域，用于 Skill Domain Snapshot 同步 |
| Related Skills | 文本列表 | v1.2 | 与该 Skill 关联的其他 Skill，用于内部关联 + Domain Snapshot 交叉引用 |
| Evidence | 文本列表 | v1.1 | 证据来源，记录该能力来自哪些项目/案例 |
| Evidence Count | 整数 | v1.1 | 证据数量，用于快速判断证据强度 |
| Confidence | 整数 (0-100) | v1.1 | 置信度评分，基于证据数量、证据质量、最近验证时间综合评估 |
| Last Verified | 日期 (YYYY-MM) | v1.1 | 最近一次验证该能力证据的时间 |

**Confidence 与 Role Snapshot / Domain Snapshot 的关系**：
- Role Snapshot vs Skill Graph 交叉比对时，Confidence 是核心判断字段
- Skill Graph 中 Domain 字段与 `knowledge/skill_snapshots/{domain_name}.md` 对齐
- Confidence < 60 的能力在 Mode D Targeted Discovery 中优先追问

---

## 04b_transferable_capabilities.md — 可迁移能力映射

将 Skill Graph 的能力条目转换为各目标 Track 的岗位语言。不是新的能力库，是 Skill Graph → 岗位语言的解释器。

| 字段 | 类型 | 说明 |
|------|------|------|
| Capability Map | 列表（TC001-TC[n]） | 每条一个能力 → 岗位语言的完整映射 |
| Source Capability | 引用 Skill Graph | 来源能力名称 / Domain / Confidence / Evidence |
| Core Abstraction | 文本（1 句） | 去岗位标签化的底层能力抽象 |
| Transferable Keywords | 按 Track 分组 | 每个目标 Track 的 2-3 个关键词 + 示例表达 |
| Forbidden Translation | 列表 | 该能力不应出现的错误表达方式 |
| Evidence Strength | 表 | Skill Graph Confidence / Transfer Confidence / JD Verified |

**派生资产**：Skill Graph 变更时 Mode B Step 4.5 自动刷新。

---

## 05_story_bank.md — 面试故事库

每个故事按 STAR 结构记录：

```markdown
# 面试故事库 (Story Bank)

## 故事 1：[故事标题]

### 类型
[STAR案例 / 管理案例 / 冲突案例 / 项目案例 / 高光案例]

### STAR 结构
- **Situation（情境）**：
- **Task（任务）**：
- **Action（行动）**：（具体做了什么，用"我"开头）
- **Result（结果）**：（量化结果 + 定性影响）

### 适用问题
- [这个故事可以回答哪些面试问题]

### 关键能力标签
- [能力1, 能力2, ...]

### 风险提示
- [追问时可能暴露的弱点，以及应对策略]
```

---

## 06_failure_story.md — 失败案例库

```markdown
# 失败案例库 (Failure Story Library)

## 案例 1：[案例标题]

### 失败经历
- **时间**：
- **项目/情境**：
- **发生了什么**：（客观描述）

### 教训总结
- **根本原因**：
- **直接原因**：

### 风险复盘
- **影响范围**：
- **止损措施**：

### 成长反思
- **学到了什么**：
- **后来如何避免同类问题**：（如有后续实践证据）

### 适用面试问题
- [面试官问"最大的失败"时如何使用此案例]
```

---

## 07_career_identity.md — 职业身份定义

定义用户的职业人格与市场定位。不是简历摘要，而是强制覆盖经历的「身份定义层」。5 层结构：

| 层 | 说明 |
|------|------|
| Professional Identity | 第一人称身份陈述（起点经历是路径，不是身份） |
| Career Positioning | Primary/Secondary/Emerging 市场定位 |
| Career Narrative | 核心职业问题 + 解决方式 + 价值主张 |
| Capability Priority | 04b 的 Tier A/B/C 权重标注（Online Profile 排序依据） |
| Non-Positioning Statement | 声明经历来源 ≠ 职业定位（**条件化 + 收录标注**：每条带 `（收录于 Layer 2: 条目名 / none）`；Online Profile 必须遵守） |

---

## 08_question_backlog.md — 待补充问题库

```markdown
# 待补充问题库 (Question Backlog)

## Open（待确认）

### Q1: [问题内容]
- **产生原因**：
- **关联能力/文件**：
- **优先级**：High / Medium / Low
- **来源模式**：Build / Update / Review / Job Application
- **状态**：Open

## Answered（已回答）

### Q1: [问题内容]
- **回答**：
- **回答时间**：
- **已回写到**：[文件名]
- **状态**：Answered

## Archived（已归档）
（不再需要回答的问题）
```

---

## 09_completeness_report.md — 完整度报告

```markdown
# 完整度报告 (Completeness Report)

## 整体完整度
- **评分**：[XX]%
- **等级**：[A/B/C/D]

## 各模块完整度

| 模块 | 完整度 | 状态 |
|------|--------|------|
| Profile | XX% | ✅/⚠️/❌ |
| Timeline | XX% | ✅/⚠️/❌ |
| Projects | XX% | ✅/⚠️/❌ |
| Skill Graph | XX% | ✅/⚠️/❌ |
| Story Bank | XX% | ✅/⚠️/❌ |
| Failure Story | XX% | ✅/⚠️/❌ |
| Career Identity | XX% | ✅/⚠️/❌ |
| Career Tracks | XX% | ✅/⚠️/❌ |

## 信息缺口
1. [缺口1] → 影响：[哪个模块/能力]
2. [缺口2] → 影响：[哪个模块/能力]

## 建议补充项
1. [建议1]（优先级：High）
2. [建议2]（优先级：Medium）

## 生成时间
[YYYY-MM-DD HH:MM]
```

---

## 10_career_tracks/ — 职业赛道库 (v1.3 目录模式)

v1.3 起从「单文件」拆分为「目录模式」（原先所有赛道写在同一个 10_career_tracks.md 里）。每个 Track 一个独立 Markdown 文件。

### 目录结构

```
career-dna/10_career_tracks/
├── README.md                    # 赛道总览：列出所有 Track 及其 Confidence
├── {track_name}.md              # 赛道文件（文件名 = Track 受控取值）
│                                #   示例：game_tech_pm / rd_pm / pmo / ai_product_pm
└── ...                          # 每条赛道一个文件（赛道由 Mode A 实际构建，skill 侧不预置）
```

### README.md — 赛道总览

```markdown
# Career Tracks Overview（赛道总览）

| Track | Confidence | Target Roles | Last Updated |
|-------|------------|-------------|--------------|
| [Track A] | [XX] | [目标岗位A], [目标岗位B], [目标岗位C] | [YYYY-MM] |
| [Track B] | [XX] | [目标岗位D], [目标岗位E] | [YYYY-MM] |
```

### {track}.md — 单个 Career Track 文件

使用 `assets/templates/career_track.md` 模板，包含：

```yaml
Track:           # 赛道名称
Confidence:      # 用户在该赛道的整体匹配置信度 (0-100)

Positioning:     # 一句话职业定位
Career Narrative: # 成长主线（一段话描述）

Evidence:        # 支持证据表格
Core Strengths:  # 核心优势 (3-5)
Recommended Projects: # 推荐展示项目
Recommended Stories:  # 推荐面试故事
Track Strategy:  # 赛道策略段（v2.12.0）— S1 定位变体 / S2 Self-Intro 框架 / S3 Project Priority / S4 Story Mapping
Known Gaps:      # 已知差距
Improvement Priorities: # 提升优先级 (短期/中期/长期)
Target Roles:    # 目标岗位列表
```

> **`## Track Strategy` 段（v2.12.0）**：由 Mode C Step 7 生成，**写在本文件内**（废除独立文件写法）。
> 与上方 `Recommended Projects` / `Recommended Stories` **分工不重叠**：上方是「可用清单」（哪些可用），
> 本段是「排序与场景绑定」（怎么用）—— 其项目 / 故事栏**只写条目标题，禁止粘贴正文**。
> `Gap Mitigation` **不在本段建列**（避免与 `Known Gaps` / `Improvement Priorities` 双份维护），改为指向那两段。
> 该段自带 `Last Generated`；文件头 `Last Updated` 语义不同（赛道置信度重评时间），不随之改动。

### v1.3 职责说明

Career Track（`10_career_tracks/`）与 Role Snapshot（`knowledge/role_snapshots/`）职责不同：

| 问题 | 查找位置 |
|------|----------|
| 用户适合这个方向吗？为什么？ | `10_career_tracks/{track}.md` |
| 市场上这个 Role 需要什么？趋势如何？ | `knowledge/role_snapshots/{role_name}.md` |

---

## 11_online_profile.md — 在线职业档案 (Online Career Profile)

### 概念

Online Profile 是 Career DNA 的派生资产（Derived Asset），不直接维护。由以下 DNA 文件自动推导生成：

| 来源文件 | 推导内容 |
|----------|----------|
| `07_career_identity.md` | Pipeline Step 2 Personal Positioning（Layer 2 每条带 `Track`〔赛道映射〕 + Layer 5 每条带 `收录于 Layer 2`〔方向同一性〕） |
| `01_profile.md` + `02_timeline.md` | Timeline 提取（年限/公司/岗位序列） |
| `04_skill_graph.md` | Part 3 Core Competencies（Confidence ≥ 60 的能力） |
| `03_projects.md` + `10_career_tracks/` | Part 4 Highlight Projects |
| `10_career_tracks/` | Part 5 Target Tracks（Primary/Secondary/Supporting） |

### 派生规则

- 任何时候更新以上 6 个 DNA 文件 → 自动重新生成 `11_online_profile.md`
- 如果来源文件某字段未填 → 对应区块标记 `[待补充]`
- 不需要用户手动维护 Online Profile

### 用途

- Boss 直聘个人主页
- 猎聘个人档案
- LinkedIn Profile
- 脉脉个人页
- 猎头推荐语

---

## 12_portfolio_candidates.md — 作品集候选池 (Portfolio Candidates)

**派生资产**。从 `03_projects.md` 中筛选可对外展示的案例并按展示价值排序；生成 `XX_portfolio.md` 时优先取材于此。

| 字段 | 说明 |
|------|------|
| Candidate | 候选案例名（对应 03_projects 条目） |
| Display Value | 对目标 Track 的展示价值（High / Medium / Low） |
| Evidence Strength | 证据强度（与 04b 口径一致） |
| Target Track | 适用赛道 |
| Format | 适合的呈现形式（文档 / 图表 / 演示） |

---

## 13_interview_narrative_strategy.md — 面试叙事战略手册

**派生 + 手写分区资产 · 面试表达层 SSOT**。整合 07 的身份叙事、05 的故事评分、02 的时间线事实与 03 的量化证据，形成一份跨 JD 通用的面试作战手册。

| Part | 内容 | 主要来源 | 区 |
|------|------|----------|:--:|
| Part 1 | 核心叙事主线 / 三大支柱 / 底层视角 / 叙事弧线 | 07 Layer 1-3 | 派生 |
| Part 2 | 离职故事话术（逐段话术 + 叙事逻辑 + 核心原则） | 02 时间线事实 | 派生 |
| Part 3 | 职业赛道转变叙事（主转变 / 次转变 / 应对结构） | 07 Layer 1/5 + 04b | 派生 |
| Part 4 | 面试三阶段：自我介绍结构 / STAR + 升维收束 / 反问清单 | 05 + 04b | 手写 |
| Part 5 | 通用战术：数字引用卡 / 语言切换 / 状态管理 | 03 | 手写 |
| Part 6 | 口径一致性与追问纵深（三层纵深模型 / 核心主张纵深卡 / 交叉校验表 / 追问防御） | 03 / 04_skill_graph / 04b / 07 | 手写 |
| Part 7 | 分轮次与分题型打法（7.1 谁面我 / 7.2 跨轮次一致性 / 7.3 每轮三件事 / 7.4 考什么形式） | 方法论 | 手写 |
| Part 8 | 面试后跟进与推进（时间轴 / 感谢信 ×3 / 催进度公式 / 失联处置 / 口头 Offer） | 方法论 | 手写 |
| Part 9 | 复盘回路（复盘四问 / 沉淀规则 / 卡壳点归因 / 落点） | 方法论 | 手写 |
| Part 10 | 反向尽调（三维度 / 情报→反问转化公式 / 结论落点 / 红线） | 方法论 | 手写 |
| Part 11 | 录用阶段（Offer 谈判四原则 / 三场景示范句 / 背调四份材料 / 红线） | 方法论 | 手写 |
| Part 12 | 英文面试准备（四件套材料规格 / 语言能力表述 / 卡壳处置 / 口径要求） | 方法论 | 手写 |

### 分区规则（v2.11.0 · 不得违反）

| 区 | Part | 写入规则 |
|:--:|------|------|
| **派生区** | Part 1-3 | 由上游文件推导。源文件变化即重生成，**禁止手写** |
| **手写区** | Part 4-12 | 方法论与战术，**推不出来**。只在用户显式要求时编辑，**任何自动刷新不得覆盖** |

- `validate_career_dna.py` 以 manifest 的 `regeneration` 字段为准，**双向护栏**：
  P1 `derived-part-drift` 校验声明的 12 个 Part 标题是否齐全（防「丢」—— 手写区被自动刷新覆盖，此事故肉眼不可见）；
  P1 `undeclared-part` 校验文中是否多出未声明的 Part（防「偷偷加」—— 新增 Part 忘记登记）。
- Mode B Step 4.5 刷新 13 时**只重生成 Part 1-3**。

**内容填充契约**：本手册每一节只允许三种形态 —— **实体内容**（可直接用的话术/模板/表）、**规则**（禁止/必须/判定）、**指针**（内容按生命周期住在别处）。第四种「空指示」（叫你准备 X，既无方法也无落点）**是缺陷**。判据：这次投递结束后会作废的内容，就不该住在本手册。详见 13 尾部「内容填充契约」小节。

**职责边界**：

- 本文件是**跨 JD 长期资产**（面试战术与行业无关），因此归位 career-dna 而非单次投递目录；单次 JD 的定制策略仍由 `resume-outputs/{JD}/04_interview_pack.md` + `resume-outputs/{JD}/05_answer_cards.md` 承担。
- 引用关系：13 是**底料**，04/05 是**切片**。Mode D 生成 04/05 时必须先读 13 **全 12 Parts**，禁止绕过它从 07/05 重新拼装通用话术。
- Part 2 的离职话术是唯一 SSOT；`02_timeline.md` 只保留时间线事实与指针。
- **生成与修改权限**：Mode A Step 8.5 首次生成（派生区自动 + 手写区一次成型）；Mode B Step 4.5 增量刷新（**仅派生区**）；Mode D **可回写手写区 Part 4-12**（跨 JD 通用战术），**不可覆盖派生区、不可新建文件、不可新增未登记的 Part**（见 `references/mode_d_job_application.md` Step 8 写入契约）。
- **数字必须可溯源**：Part 5 数字引用卡的每一项都要能在 03 / 05 找到出处，禁止估算或夸大；Part 6 纵深卡「出处」列指向的文件必须真实存在（validate P2 `unresolved-anchor` 校验）。
- **口径唯一**：Part 6.3 交叉校验表是全库规模类数字的统一口径来源；与 core（03 / 05）冲突时**只改本手册**，不得反向改 core。
- **不重复原则**：Part 7 是**打法视角**，与 `01_jd_match_report.md` Part 6 的**风险视角**分工不同，不得互相复制；Part 7（含 7.4 分题型）/ 8 的通用方法不在 `04` 重复，`04` §7.1 / §8 只填本轮实际。
- **后续阶段的分工**：Part 10 反向尽调（尽调**输入**）与 Part 4 阶段三（反问**输出**）互补；Part 11 录用阶段（通用谈判原则与背调口径）只落 `application-tracker/archives/`，`04` 只记本轮实际；Part 12 英文面试只定义**规格与规则**，本轮英文稿落 `04` §10。
- **记录落点**：Part 9 的单次面试记录写在 `application-tracker/archives/{Company}_{Role}.md`，本文件只存方法论。

---

## External Knowledge Layer v1.3（外部市场知识层）

### 概念

v1.3 职责收敛：删除 `job-tracks/`，消除与 `role_snapshots` 的重叠。仅保留两层市场资产：

```
Knowledge（市场知识库）= 市场资产 → 市场需要什么、趋势是什么
    ├── Role Snapshot      → 按 Role 的市场画像（含公司/来源/趋势）
    └── Skill Domain Snapshot → 按 Domain 的能力市场情报（含关联/趋势）
```

| 维度 | Career DNA | Knowledge |
|------|-----------|-----------|
| 定位 | 用户唯一事实源 + 个人赛道 | 外部市场情报 |
| 内容 | 经历、能力、Career Track | Role Snapshot, Skill Domain Snapshot |
| 来源 | 用户提供 + JD 匹配回写 | JD 分析积累 |
| 目录 | `career-dna/` | `knowledge/` |
| 包含个人信息 | 是 | 否 |

### 目录结构 (v1.4)

```
knowledge/
├── role_snapshots/            # 岗位快照 (Role Snapshot) — 按 Role 归档
│   └── {role_name}.md         #   v1.4: 含 Hiring Intelligence（招聘情报） / Talent Persona（人才画像） / Evidence Trends（证据趋势）
└── skill_snapshots/           # 能力域快照 (Skill Domain Snapshot) — 按 Domain 组织
    └── {domain_name}.md       #   v1.4: 含 Typical Evidence（典型证据） / Business Meaning（业务价值） / Related Hiring Intent（关联招聘意图）
```

### role_snapshots/{role_name}.md — 岗位快照 (v2.14.0)

> **模板真源**：`assets/templates/knowledge/role_snapshot.md` —— 本段与模板保持同步，生成 / 更新前以模板为准。
> 全篇共 **8 段**（下方全列）。此前本 spec 只列 `Hiring Intelligence` + `Trend Intelligence` 两段，**漏了 6 段** ——
> 这是 2026-07-20 ~ 09-02 期间 7 个旧实例缺段的直接上游原因（生成器读 spec 就会产出漂移实例）。
> `Track` 为**受控取值**（赛道文件名 或 `none`），解释写 `Track Note` —— 见 `references/mode_d_job_application.md` Step 10 A。
> `Observed Companies` 同为**受控格式**（公司名，` · `/`+` 分隔，说明写 `（）` 括注，未标注写 `unknown`）——
> 其解析出的**不同公司数**是「新赛道发现」判据的唯一输入（见 `references/mode_d_job_application.md` §Step 10 C 第 7 条），
> 由 P2 `role-snapshot-schema` 第 ④ 项校验。

```markdown
# Role Snapshot（岗位快照）: [Role Name]

- **Track（职业赛道）**: [受控取值 —— `10_career_tracks/` 下赛道文件名（不含 .md）或 none]
- **Track Note（赛道说明）**: [解释：子域限定 / 为何 none / 交叉参考]
- **Aliases（别名）**: [该岗位的其他常见名称]
- **Observed JD Count（已观察JD数）**: 0
- **Observed Companies（已观察公司）**: [受控格式 —— 公司名（` · ` 分隔）；说明写 `（）` 括注，不计入计数；未标注公司写 `unknown`]
- **Recent JD Sources（近期JD来源）**: [YYYY-MM Company Role]
- **Core Skills（核心技能）**: [核心技能列表]
- **Soft Skills（软技能）**: [软技能列表]
- **Tools（工具）**: [常见工具 / 平台 / 系统]
- **Industries（行业）**: [该岗位出现的行业]

## Role Capability Model（岗位能力模型 v2.3）
| 核心能力 | 市场权重 | 典型市场表达 | 来源 JD 数 |
（Transferable Capability 的 Target Keywords 来源）

## Hiring Intelligence（招聘情报 v1.4）
- **Common Hiring Intent** / **Talent Persona** / **Typical Evidence** / **Career Background Distribution** / **Last Updated**

## JD 观察记录 (JD Observation Log)
| 日期 | 公司 | 行业 | 招聘意图 | 新增 Skills | 新增 Tools | 备注 |

## 能力频率统计 (Skill Frequency)
| 能力 | 出现次数 | 频率 |

## 公司分布 (Company Distribution)
| 公司 | 观察次数 | 行业 |

## Persona Statistics（画像统计层 v1.4.2）
（≥5 次 JD 观察后生成）
### Experience Frequency（典型经历频率）
### Career Background Frequency（职业背景分布频率）
### Trait Frequency（偏好特质频率）

## Common Capability Transitions（常见能力迁移路径 v1.4.4）
| 来源背景 | 常迁移能力 | 观察次数 | 置信度 |

## Trend Intelligence（趋势观察 v1.4）
- **Hiring Intent Trends** / **Talent Persona Trends** / **Evidence Trends** / **Trend Notes**
```

**空段 ≠ 缺段**：`Observed JD Count = 0` 的新建快照允许各段只有表头或占位符，但 **8 个段标题必须齐全**（由 P2 `role-snapshot-schema` 校验；已存在的旧实例走迁移白名单，随下次 JD 观察自然补齐）。

### skill_snapshots/{domain_name}.md — 能力域快照 (v1.4 Talent Intelligence)

```markdown
# Skill Domain Snapshot: [Domain Name]

## [Skill Name 1]
### Talent Intelligence（人才智能 v1.4）
- **Typical Evidence**: [典型证据]
- **Business Meaning**: [业务价值]
- **Related Hiring Intent**: [关联招聘意图]
- **Typical Results**: [典型成果量化]
- **Typical Ownership**: [Owner / Lead / Support]
```

### [Historical] skill_snapshots/{domain_name}.md — 能力域快照 (v1.3 增强)

```markdown
# Skill Domain Snapshot: [Domain Name]

## [Skill Name 1]
- **Frequency**: 0
- **Observed JD Count**: 0
- **Related Roles**: [Roles]
- **Related Skills**: [Skills]
- **Recent Observations**: [YYYY-MM Company Role]
- **Industries**: [Industries]
- **Trend Notes**: [趋势]
```

### Resume Outputs 结构 (v1.5.1)

```
resume-outputs/{YYYYMMDD}-{company}-{role}/
├── 01_jd_match_report.md  — JD原文 + Capability Translation + 匹配分析
├── 02_resume_cn.md        — 中文 ATS 简历 (v1.5.1 重命名)
├── 03_resume_en.md        — 英文 ATS 简历 (v1.5.1 新增)
├── XX_interview_pack.md   — 面试准备包
├── XX_answer_cards.md     — 回答卡片库
├── XX_upgrade_plan.md     — 升级计划
├── XX_gap_analysis.md     — 能力差距分析 (v1.5.1 新增 / Moderate+Stretch+Weak)
├── XX_transition_resume_cn.md   — 转岗中文简历 (v1.5.1 新增 / Stretch)
├── XX_transition_resume_en.md   — 转岗英文简历 (v1.5.1 新增 / Stretch)
├── XX_transition_feasibility.md — 转岗可行性 (v1.5.1 新增 / Weak)
└── XX_learning_roadmap.md — 学习路线图 (v1.5.1 新增 / Weak)
```
> v1.5.1: Application Strategy Decision → 4 种策略 (Strong/Moderate/Stretch/Weak) 分层生成不同文件集合。
> 产出合约见 `references/output_contracts.md`。

### 01_jd_match_report.md — 岗位匹配报告 (v1.3 增强)

> ⚠️ **版式以 `references/pack_templates/01_jd_match_report_template.md` 为唯一定义源**
> （现行 **9-Part** + **附录 A/B**）；下方 Part 1-4 为 **v1.3 历史描述**，仅供追溯，**勿据此生成**。
> 附录生成规则见 `references/mode_d_job_application.md` **Step 2.9**；产物合约见 `references/output_contracts.md`。

新增三部分：JD Metadata / Original JD / AI Extracted Summary，保留完整 JD 上下文用于回溯。

**Part 1: JD Metadata（JD元信息）** — Company（公司） / Role（岗位） / Date（日期） / Source（来源） / Track（赛道）
**Part 2: Original JD（JD原文）** — 完整 JD 原文存档
**Part 3: AI Extracted Summary（AI提取摘要）** — Core Responsibilities（核心职责） / Must Have Skills（硬性要求） / Nice To Have（加分项） / Tools（工具） / Keywords（关键词） / Risk Factors（风险点）
**Part 4: Match Analysis（匹配分析）** — Match Score（匹配度） / Strengths（优势） / Gaps（缺口） / Recommended Projects（推荐项目） / Stories（推荐故事） / High Risk Questions（高风险问题） / ATS Keywords（关键词）

### 交叉引用规则 (v1.3)

| 场景 | 引用方向 | 说明 |
|------|----------|------|
| Mode D Career Track Match | JD Role → Role Snapshot → Career Track → Skill Graph | 市场基线 + 个人赛道 + 能力核查 |
| Mode D JD Match Report | Role Snapshot vs Skill Graph + Career Track | 市场要求 vs 个人能力 + 赛道匹配 |
| Mode D Targeted Discovery | Skill Domain Snapshot → Skill Graph | 关联能力线索 → 追问 |
| Mode C Career Review | Role Snapshot Trend Notes → Career Track Confidence | 市场趋势 vs 个人赛道信心 |

### V2 规划（暂未实现）

- `role_library/` — 角色知识库（结构化 Role 定义）
- `skill_library/` — 能力知识库（结构化 Skill 定义）
- `ontology/` — 职业本体论（Role-Skill-Industry 关系图）
- `career_recommendation_engine/` — 职业推荐引擎
- `career_path_prediction/` — 职业路径预测

### [Historical] skill_snapshots/{domain_name}.md — 能力域快照 (v1.2 Domain 模式)

v1.2 起从按单个 Skill 归档改为按 Domain 归档。一个 Domain 文件下包含多个 Skill。

```markdown
# Skill Domain Snapshot: [Domain Name]

## [Skill Name 1]
- **Frequency**: 0
- **Related Roles**: [该能力出现在哪些 Role 的 JD 中]
- **Related Skills**: [经常与此能力一起出现的关联能力]
- **Industries**: [该能力在哪些行业中被要求]

## [Skill Name 2]
...
```

Domain 命名示例（**示例取值，非文件引用**）：
| Domain 名 | 包含的 Skill |
|-------------|-------------|
| project_management | Stakeholder Management, Risk Management, Resource Planning |
| testing | Test Planning, Test Automation, QA Process |
| business_analysis | Requirements Gathering, Process Mapping, Stakeholder Analysis |
| implementation_consulting | Implementation Planning, Client Training, Go-Live Support |

> ⚠️ 上表是 **Domain 命名示范**（写入 `04_skill_graph` 的 Domain 字段值），**不是文件引用**。
> 实际文件名一律 `{domain_name}.md`，置于 `knowledge/skill_snapshots/` 下。
> 本处**刻意不使用反引号包文件名** —— 否则 `ghost-file-ref` 扫描扩面到 `references/` 时会
> 把示例名误判为幽灵引用（审计报告 C6）。

### [Historical] job-tracks/{role_name}.md — 赛道画像 (v1.2 新增；**v1.3 已删除该目录**)

> ⚠️ **本节为历史结构说明，非现行形态**。`job-tracks/` 目录已由 **v1.3 删除**，其职责并入
> `career-dna/10_career_tracks/{track}.md`（见上一节）。保留本节仅为追溯 v1.2 的数据模型，
> 与同区段 `### [Historical] skill_snapshots/...` 的标记方式保持一致。

Track Profile 是 Role 级别的市场画像，仅保存市场侧数据。

```markdown
# Track Profile: [Role Name]

- **Track**: [所属赛道]
- **Aliases**: [该 Role 的其他常见名称]
- **Observed JD Count**: 0
- **Observed Companies**: [已观察到的公司列表]
- **Core Responsibilities**: [核心职责列表]
- **Must Have Skills**: [硬性要求技能列表]
- **Nice To Have Skills**: [加分项技能列表]
- **Common Tools**: [常见工具/平台/系统]
- **Industries**: [该 Role 出现的行业分布]
- **Last Updated**: [YYYY-MM]
```

### resume-outputs/{date}\_{company}\_{role}/ — 单次投递产物 (v1.2 新结构)

v1.2 起按日期+公司+岗位子目录隔离每次投递：

```
resume-outputs/{YYYYMMDD}-{company}-{role}/
├── 01_jd_match_report.md  — 岗位匹配报告
├── 02_resume_cn.md        — 中文 ATS 简历 (v1.5.1 重命名)
├── 03_interview_pack.md   — 面试准备包 (v1.5 编号前移)
├── 04_answer_cards.md     — 回答卡片库 (v1.5 编号前移)
└── 05_upgrade_plan.md     — 竞争力升级计划 (v1.5 编号前移)
```

### Resume Outputs 01_jd_match_report.md — 岗位匹配报告 (v1.2 新增)

合并 JD Analysis + DNA Match Analysis，是后续所有材料的唯一数据源。

```yaml
Company: [公司名]
Role: [岗位名]
Track: [所属赛道]
Industry: [行业]
Match Score: [XX%]
Must Have Coverage: [XX%]
Nice To Have Coverage: [XX%]
```

包含：Strengths（优势） / Gaps（缺口） / Recommended Projects（推荐项目） / Recommended Stories（推荐故事） / High Risk Questions（高风险问题） / ATS Keywords（关键词） / Application Advice（投递建议）

### 交叉引用规则 (v1.2 更新)

| 场景 | 引用方向 | 说明 |
|------|----------|------|
| Mode D Track Match | JD Role → Track Profile | 识别 Role 后定位对应 Track Profile |
| Mode D JD Match Report | Track Profile + Role Snapshot → Skill Graph | 市场基线 + 市场情报 vs 个人能力 |
| Mode D Targeted Discovery | Role Snapshot → Skill Graph | Role Snapshot 高频能力在 Skill Graph Confidence < 60 触发追问 |
| Mode C Career Review | Track Profile → Career Tracks | 参考 Track Profile 的 Role 特征评估职业方向可行性 |

### V2 规划（暂未实现）

以下目录将在 V2 版本中实现：
- `role_library/` — 角色知识库（结构化 Role 定义）
- `skill_library/` — 能力知识库（结构化 Skill 定义）
- `ontology/` — 职业本体论（Role-Skill-Industry 关系图）
- `career_recommendation_engine/` — 职业推荐引擎
- `career_path_prediction/` — 职业路径预测
