# 在线职业档案 (Online Career Profile v1.5)

<!--
Online Career Profile（在线职业档案）— v1.5 新增
Career DNA 的派生资产（Derived Asset），不直接维护。

由以下 DNA 文件自动推导生成：
  01_profile.md        → Career Summary
  02_timeline.md       → Career Summary
  03_projects.md       → Highlight Projects
  04_skill_graph.md    → Core Competencies
  07_career_identity.md → Personal Branding / Headline / Career Summary
  10_career_tracks/    → Target Tracks

派生逻辑：用户更新以上任一文件 → 系统自动重新生成此文件。
不需要"每次 JD 重新写一次 Boss 简历"。
-->

- **Last Generated（最近生成）**: [YYYY-MM-DD]
- **Source Files Version**: 01=[填], 02=[填], 03=[填], 04=[填], 07=[填], 10=[填]

---

## Part 1: Personal Branding（职业品牌）

<!-- 来源：07_career_identity.md -->

### Headline（职业一句定位）
> "[角色]｜[行业]｜[差异化]"

### Professional Tags（职业标签）
- [标签1]
- [标签2]
- [标签3]
- [标签4]
- [标签5]

### Core Competencies（核心竞争力简介）
[1-2 句总结，来源：07_career_identity 的核心竞争力列表]

---

## Part 2: Career Summary（职业简介）

<!-- 来源：01_profile + 02_timeline + 07_career_identity，300-500 字 -->
<!-- 用于 Boss 直聘「自我介绍」/ LinkedIn「About」 -->

[一段 300-500 字的职业旅程叙述，涵盖：
- 职业起点和关键转折
- 核心能力域和代表性成果
- 当前定位和下一步方向]

---

## Part 3: Core Competencies（核心能力标签）

<!-- 来源：04_skill_graph.md，提取 Confidence ≥ 60 的能力，按 Confidence 降序排列 -->

| 能力 | Domain（域） | Confidence（置信度） |
|------|-------------|---------------------|
| [能力1] | [域1] | [XX] |
| [能力2] | [域2] | [XX] |
| [能力3] | [域3] | [XX] |
| [能力4] | [域4] | [XX] |
| [能力5] | [域5] | [XX] |

---

## Part 4: Highlight Projects（代表项目）

<!-- 来源：03_projects.md + 10_career_tracks 的 Recommended Projects -->

| # | 项目 | 角色 | 亮点 | 涉及能力 |
|---|------|------|------|----------|
| 1 | [项目名] | [角色] | [一句话亮点] | [能力列表] |
| 2 | [项目名] | [角色] | [一句话亮点] | [能力列表] |
| 3 | [项目名] | [角色] | [一句话亮点] | [能力列表] |

---

## Part 5: Target Tracks（目标方向）

<!-- 来源：10_career_tracks/，按 Confidence 降序，取 Top 3 -->

- **Primary Track（主赛道）**: [Track Name] — Confidence: [XX]
- **Secondary Track（副赛道）**: [Track Name] — Confidence: [XX]
- **Supporting Track（支持赛道）**: [Track Name] — Confidence: [XX]

---

## Multi-View（多视图 V2 预留）

<!-- 未来从同一份 Online Profile 生成不同平台的视图，而非独立维护 -->

### Boss Version（Boss 直聘版）
[从 Part 1-5 自动精简为 Boss 格式]

### LinkedIn Version（领英英文版）
[从 Part 1-5 自动翻译适配英文]

### Headhunter Version（猎头版）
[从 Part 1-5 自动提炼为猎头推荐语]
