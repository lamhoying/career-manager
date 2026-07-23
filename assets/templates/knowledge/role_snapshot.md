# Role Snapshot（岗位快照）: [Role Name]

<!--
岗位快照 (Role Snapshot) — Knowledge Layer（市场资产），不含用户个人信息。
v1.3: Observed Companies / Recent JD Sources / Trend Notes
v1.4: Common Hiring Intent / Talent Persona / Typical Evidence / Career Background Distribution / Hiring Intent Trends / Talent Persona Trends / Evidence Trends
-->

- **Track（职业赛道）**: [该岗位所属的职业方向，如 Project Management]
- **Aliases（别名）**: [该岗位的其他常见名称]
- **Observed JD Count（已观察JD数）**: 0
- **Observed Companies（已观察公司）**: [已观察到的公司列表]
- **Recent JD Sources（近期JD来源）**: [最近 JD 来源，格式 YYYY-MM Company Role]
- **Core Skills（核心技能）**: [核心技能列表]
- **Soft Skills（软技能）**: [软技能列表]
- **Tools（工具）**: [常见工具/平台/系统]
- **Industries（行业）**: [该岗位出现的行业]

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
| QA Lead | Project Delivery（项目交付） | [N] | High |
| QA Lead | Stakeholder Management（干系人管理） | [N] | High |
| Test Manager | QA Process（质控流程） | [N] | High |
| Implementation Consultant | Requirement Analysis（需求分析） | [N] | Medium |

> 注意：此表记录市场规律，不绑定任何用户数据。Confidence ≥ High 的可在 Adjacent Match 中作为加分参考。

## Trend Intelligence（趋势观察 v1.4）

- **Hiring Intent Trends（招聘意图趋势）**: [≥3 次观察后，招聘意图变化趋势]
- **Talent Persona Trends（人才画像趋势）**: [≥3 次观察后，画像要求变化]
- **Evidence Trends（证据趋势）**: [≥3 次观察后，证据要求变化]
- **Trend Notes**（通用趋势）: [如 AI Tools ↑ / Data Analysis ↑]
