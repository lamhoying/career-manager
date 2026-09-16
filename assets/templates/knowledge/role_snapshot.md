# Role Snapshot（岗位快照）: [Role Name]

<!--
岗位快照 (Role Snapshot) — Knowledge Layer（市场资产），不含用户个人信息。
v1.3: Observed Companies / Recent JD Sources / Trend Notes
v1.4: Common Hiring Intent / Talent Persona / Typical Evidence / Career Background Distribution / Hiring Intent Trends / Talent Persona Trends / Evidence Trends
-->

- **Track（职业赛道）**: [**受控取值** —— 只允许两种形态：① 命中已登记赛道 → 填 `10_career_tracks/` 下的赛道文件名（**不含 .md**），如 game_tech_pm / rd_pm / pmo / ai_product_pm；② 未命中 → 填 none。**禁止写散文 / 禁止双语括注 / 禁止斜杠并列**，否则无法按赛道归组（v2.14.0）]
- **Track Note（赛道说明）**: [可选。自由文本解释一律写这里 —— 子域限定（如「美术管线子域」）/ 为何 none / 与哪些赛道交叉参考。**取值与说明分离**：Track 只放受控值，理由放本字段]
- **Aliases（别名）**: [该岗位的其他常见名称]
- **Observed JD Count（已观察JD数）**: 0
  <!-- 数字开头即可计数；口径说明（如「同一公司同批次」）写括注，不影响计数。本字段**不是**新赛道判据（判据用公司数）。 -->
- **Observed Companies（已观察公司）**: [**受控格式 v2.17.0** —— 只放**公司名**，多家用 ` · ` 或 `+` 分隔；每家的说明写在紧跟其后的 `（）` 括注内（证码 / 城市 / 隶属 / 规模），**括注内容不计入公司计数**、括注内提及的关联方（母公司 / 客户）**不算独立观察**；JD 未标注公司 → 写受控值 `unknown`（**不计入**），推断理由写括注。**禁止**把说明写成 ` · ` 分隔的平铺串（会被解析成另一家公司 → 误触发「新赛道发现」）。本字段解析出的**不同公司数**＝「新赛道发现」判据的唯一输入（`references/mode_d_job_application.md` §Step 10 C 第 7 条），并由 P2 `role-snapshot-schema` 第 ④ 项校验 —— **取值与说明分离**，同 `Track` / `Track Note` 的思路]
- **Recent JD Sources（近期JD来源）**: [最近 JD 来源，格式 YYYY-MM Company Role]
- **Core Skills（核心技能）**: [核心技能列表]
- **Soft Skills（软技能）**: [软技能列表]
- **Tools（工具）**: [常见工具/平台/系统]
- **Industries（行业）**: [该岗位出现的行业]

## Role Capability Model（岗位能力模型 v2.3）

<!-- 该岗位在市场上的核心能力要求。用于 Transferable Capability 的 Target Keywords 映射。 -->

| 核心能力 | 市场权重 | 典型市场表达 | 来源 JD 数 |
|------|:--:|------|:--:|
| [能力1] | High | [市场中常见的表达] | [N] |
| [能力2] | High | [市场中常见的表达] | [N] |
| [能力3] | Medium | [市场中常见的表达] | [N] |
| [能力4] | Medium | [市场中常见的表达] | [N] |

> Role Capability Model 是 Transferable Capability Mapping 的目标语言来源。

## Hiring Intelligence（招聘情报 v1.4）

- **Common Hiring Intent（常见招聘意图）**: [从多次 JD 分析积累的典型招聘意图]
- **Talent Persona（典型人才画像）**: [基于多次 JD 融合的典型画像特征]
- **Typical Evidence（常见证据模式）**: [该 Role 面试中常见的证据类型]
- **Career Background Distribution（职业背景分布）**: [该 Role 常见的前置经验和行业背景]
- **Last Updated**: [YYYY-MM]

## JD 观察记录 (JD Observation Log)

| 日期 | 公司 | 行业 | 招聘意图 | 新增 Skills | 新增 Tools | 备注 |
|------|------|------|----------|-------------|------------|------|

## 能力频率统计 (Skill Frequency)

| 能力 | 出现次数 | 频率 |
|------|----------|------|

## 公司分布 (Company Distribution)

| 公司 | 观察次数 | 行业 |
|------|----------|------|

## Persona Statistics（画像统计层 v1.4.2）

<!-- ≥5 次 JD 观察后开始生成，以 Observed JD Count 为分母，将 Talent Persona 从 AI 总结升级为统计结论 -->

### Experience Frequency（典型经历频率）

| 经历类型 | 出现次数 | 频率 | 趋势 |
|----------|----------|------|------|
| 需求分析经验 | 26/28 | 93% | → 稳定 |
| 项目交付经验 | 22/28 | 79% | ↑ 上升 |
| 客户培训经验 | 18/28 | 64% | → 稳定 |

### Career Background Frequency（职业背景分布频率）

| 背景来源 | 出现次数 | 频率 |
|----------|----------|------|
| 乙方 IT 咨询 | 15/28 | 54% |
| 甲方 IT 部门 | 10/28 | 36% |
| 实施/交付团队 | 8/28 | 29% |

### Trait Frequency（偏好特质频率）

| 特质 | 出现次数 | 频率 |
|------|----------|------|
| 独立性强 | 20/28 | 71% |
| 沟通力强 | 18/28 | 64% |

## Common Capability Transitions（常见能力迁移路径 v1.4.4）

<!--
市场观察：基于多次 JD 分析观察到的常见能力迁移路径。
仅记录市场侧规律（行业惯例），不包含用户个人信息。
用于 Capability Translation 的 Adjacent Match 判定参考。
-->

| 来源背景 | 常迁移能力 | 观察次数 | 置信度 |
|----------|-----------|----------|--------|
| [来源岗位A] | [可迁移能力A]（[能力说明]） | [N] | High |
| [来源岗位B] | [可迁移能力B]（[能力说明]） | [N] | High |
| [来源岗位C] | [可迁移能力C]（[能力说明]） | [N] | High |
| [来源岗位D] | [可迁移能力D]（[能力说明]） | [N] | Medium |

> 注意：此表记录市场规律，不绑定任何用户数据。Confidence ≥ High 的可在 Adjacent Match 中作为加分参考。

## Trend Intelligence（趋势观察 v1.4）

- **Hiring Intent Trends（招聘意图趋势）**: [≥3 次观察后，招聘意图变化趋势]
- **Talent Persona Trends（人才画像趋势）**: [≥3 次观察后，画像要求变化]
- **Evidence Trends（证据趋势）**: [≥3 次观察后，证据要求变化]
- **Trend Notes**（通用趋势）: [如 AI Tools ↑ / Data Analysis ↑]
