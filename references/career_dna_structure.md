# Career DNA Structure Reference（职业基因库结构参考）

Career DNA 是用户职业经历的唯一事实源，由 10 个文件组成，存放在 `career-dna/` 目录下。以下为每个文件的字段定义、填写规范和示例格式。

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

## 07_career_identity.md — 职业身份库

```markdown
# 职业身份库 (Career Identity)

## 我是谁
（一段话总结职业身份，如"5年项目管理经验的交付型PM，擅长跨部门协调和复杂项目交付"）

## 职业标签
- [标签1]（如：项目管理）
- [标签2]（如：跨部门协作）
- [标签3]（如：敏捷交付）
- ...

## 核心竞争力
1. **[竞争力1]**：证据 → [项目/案例]
2. **[竞争力2]**：证据 → [项目/案例]
3. **[竞争力3]**：证据 → [项目/案例]

## 差异化优势
（相比同级别竞争者，独特优势是什么）

## 职业价值观
- [工作方式偏好]
- [团队风格偏好]
- [行业偏好]
```

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

v1.3 起从单文件 `10_career_tracks.md` 拆分为目录模式。每个 Track 一个独立 `.md` 文件。

### 目录结构

```
career-dna/10_career_tracks/
├── README.md                    # 赛道总览：列出所有 Track 及其 Confidence
├── project_manager.md           # 项目经理赛道
├── implementation_consultant.md # 实施顾问赛道
├── qa_manager.md                # QA Manager 赛道
└── ...                          # 更多赛道文件
```

### README.md — 赛道总览

```markdown
# Career Tracks Overview（赛道总览）

| Track | Confidence | Target Roles | Last Updated |
|-------|------------|-------------|--------------|
| Project Manager | 85 | 游戏研发PM, PMO, IT项目经理 | 2026-07 |
| Implementation Consultant | 70 | 实施顾问, 交付经理 | 2026-07 |
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
Known Gaps:      # 已知差距
Improvement Priorities: # 提升优先级 (短期/中期/长期)
Target Roles:    # 目标岗位列表
```

### v1.3 职责说明

Career Track（`10_career_tracks/`）与 Role Snapshot（`knowledge/role_snapshots/`）职责不同：

| 问题 | 查找位置 |
|------|----------|
| 用户适合这个方向吗？为什么？ | `10_career_tracks/{track}.md` |
| 市场上这个 Role 需要什么？趋势如何？ | `knowledge/role_snapshots/{role_name}.md` |

---

## 11_online_profile.md — 在线职业档案 (Online Career Profile v1.5)

### 概念

Online Profile 是 Career DNA 的派生资产（Derived Asset），不直接维护。由以下 DNA 文件自动推导生成：

| 来源文件 | 推导内容 |
|----------|----------|
| `07_career_identity.md` | Part 1 Personal Branding（Headline / Tags / Core Competencies 简介） |
| `01_profile.md` + `02_timeline.md` + `07_career_identity.md` | Part 2 Career Summary（300-500 字） |
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

### role_snapshots/{role_name}.md — 岗位快照 (v1.4 Talent Intelligence)

```markdown
# Role Snapshot: [Role Name]

## Hiring Intelligence（招聘情报 v1.4）
- **Common Hiring Intent**: [典型招聘意图]
- **Talent Persona**: [典型人才画像特征]
- **Typical Evidence**: [常见证据模式]
- **Career Background Distribution**: [职业背景分布]

## Trend Intelligence（趋势观察 v1.4）
- **Hiring Intent Trends**: [招聘意图趋势]
- **Talent Persona Trends**: [画像要求变化]
- **Evidence Trends**: [证据要求变化]
```

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

Domain 示例：
| Domain 文件 | 包含的 Skill |
|-------------|-------------|
| `project_management.md` | Stakeholder Management, Risk Management, Resource Planning |
| `testing.md` | Test Planning, Test Automation, QA Process |
| `business_analysis.md` | Requirements Gathering, Process Mapping, Stakeholder Analysis |
| `implementation_consulting.md` | Implementation Planning, Client Training, Go-Live Support |

### job-tracks/{role_name}.md — 赛道画像 (v1.2 新增)

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
