# JD Match Report: [公司名] - [岗位名]

<!--
岗位匹配报告 (JD Match Report v1.6.2)
Career Decision Engine — 从"能力匹配"升级为"求职决策"。

Part 1: JD 原文归档
Part 2: 角色分析（Decomposition + Intent + Persona + Skill Weight）
Part 3: DNA 匹配（Score + Confidence + Track Validation）
Part 4: Evidence Distance（证据距离 D0-D4）
Part 5: Role Authenticity（角色真实性 v1.5.4 新增）
Part 6: Recruiter Risk Funnel（招聘漏斗风险 v1.5.4 新增）
Part 7: Decision Score（决策评分 v1.5.4 新增）
Part 8: Recommended Strategy（推荐策略）
-->

## Part 1: JD Original（JD 原文存档）

```
[用户提交的完整 JD 内容]
```

---

## Part 2: Role Analysis（角色分析 v1.5.4）

- **Role（岗位）**: [标准化名称]
- **Company（公司）**: [公司名]
- **Date（日期）**: [YYYY-MM-DD]
- **Track（赛道）**: [匹配的 Career Track]

### 2.1 Core Responsibilities（核心职能）
1. [职能1] — [一句话职责]
2. [职能2] — [一句话职责]
3. [职能3] — [一句话职责]
- **Ownership（责任级别）**: Lead / Partial Lead / Support
- **Scope（范围）**: 单项目 / 多项目 / 跨地域

### 2.2 Hiring Intent（招聘意图）
- **Explicit（显性要求）**: [JD 明文要求的硬性条件]
- **Implicit（隐性要求）**: [推理出的未写明要求]
- **Business Context（业务背景）**: [为什么招 — 扩张/替补/新业务]
- **Pain Point（痛点推断）**: [团队当前缺什么能力]

### 2.3 Skill Weight Analysis（能力权重分析）
| 能力 | 权重 | 来源 | 说明 |
|------|------|------|------|
| [能力1] | 35% | JD高频 + Snapshot高频 | Critical |
| [能力2] | 25% | JD明确要求 | High |
| [能力3] | 20% | Snapshot常见 | Medium |
| [能力4] | 15% | JD提及 | Low-Medium |
| [能力5] | 5% | JD提及非核心 | Low |

> 权重总和=100%。由 JD 措辞优先级 × Role Snapshot 频率 × 行业常识三维度推理。

### 2.4 Ideal Candidate（理想候选人画像）
> "[Natural-language：什么样的一个人？]"
- **Career Background（职业背景）**: [行业] / [N]年 [领域]
- **Typical Experience（典型经历）**: [经历1], [经历2], [经历3]
- **Preferred Traits（偏好特质）**: [特质1], [特质2], [特质3]

---

## Part 3: DNA Match Analysis（DNA 匹配分析 v1.5.4）

### 3.1 Match Summary（匹配概要）

| 维度 | 值 | 来源 |
|------|-----|------|
| **Overall Match Score（综合匹配度）** | → | → 3.2 最终 Overall |
| **Match Confidence（匹配置信度）** | → | → 3.3 最终 Match Confidence |
| **Application Strategy（求职策略）** | → | → 基于 Match Score 判定 |

> 摘要数值 = 各分项计算的最终结果。由系统运行时从 3.2/3.3/Part 7 引用填充，不做独立赋值。

### 3.2 Match Score Breakdown（匹配得分分解）

| 评分维度 | 权重 | 得分 | 加权 | 说明 |
|----------|------|------|------|------|
| **Hard Requirement Match（硬性要求匹配）** | 40% | 72 | 28.8 | 学历/语言/证书/年限逐项判定 |
| **Experience Match（经验匹配）** | 30% | 65 | 19.5 | 行业/场景/角色重叠度 |
| **Capability Match（能力迁移匹配 v1.5.4）** | 20% | 60 | 12.0 | D0=100%/D1=85%/D2=65%/D3=40%/D4=0% |
| **Industry Match（行业匹配）** | 10% | 50 | 5.0 | 同行业/同客户群/同业务场景 |
| **Overall** | **100%** | **65** | **65.3** | |

> 3.1 摘要 Match Score = 此行 Overall 值（65）。Hard Requirement Detail 明细值见下方。

#### Hard Requirement Detail（硬性要求明细）

| JD 要求 | 用户状态 | Score | 扣分来源 |
|---------|----------|-------|----------|
| 5年+ 相关经验 | 3年实践+2年相关 | 50 | 头衔不匹配(-25) / 年限不足(-25) |
| 工具技能 | 日常使用3年 | 90 | 角色等级差(-10) |
| 外语能力 | 团队协作2年 | 95 | 无正式等级证书(-5) |
| [硬性要求4] | [用户状态] | [XX] | [扣分原因] |

> Score = 100 - 各扣分项累加。最终 Hard Requirement Match = 各项 Score 均值。
> 扣分规则：头衔不匹配但经验存在→-20~30 / 年限差距→按比例-10~15/年 / 证书缺失→-10~20 / 完全缺失→Score=0

### 3.3 Match Confidence Breakdown（匹配置信度分解）

#### Scoring Reference（评分因子参考）

| 分量 | 公式 | 扣分条件 |
|------|------|----------|
| **Evidence Count（30%）** | (可用证据项数 / 总匹配能力数) × 100 | 总能力 < 3 项 → 直接扣 20 |
| **Evidence Quality（30%）** | (High×100 + Medium×60 + Low×30) / 总数 | Low 占比 > 50% → 直接 -15 |
| **Direct Relevance（25%）** | D0+D1 占比分级（>50%=85 / 30-50%=65 / <30%=45） | D3+D4 > 60% → 直接 -10 |
| **Evidence Stability（15%）** | 核心能力跨项目频次（3+=90 / 2=65 / 1=40） | 最高频次能力 ≠ 最高权重能力 → -5 |

#### Breakdown（因子分解）

| 置信度因素 | 权重 | 原始分 | 扣分 | 最终分 | 说明 |
|-----------|------|--------|------|--------|------|
| Evidence Count（证据数量） | 30% | 85 | 0 | 85 | 6/8 项能力有证据支撑 |
| Evidence Quality（证据质量） | 30% | 72 | 0 | 72 | 3 High / 4 Medium / 1 Low |
| Direct Relevance（直接相关性） | 25% | 65 | 0 | 65 | D0+D1 占比 50% → 65pt |
| Evidence Stability（证据稳定性） | 15% | 65 | 0 | 65 | 核心能力跨 2 项目 |
| **Match Confidence** | **100%** | | | **72** | 加权合计 → 填入 3.1 摘要

> Evidence Stability = 同能力是否被 3+ 独立项目证明。全部基于 DNA 内部证据，不依赖市场数据。

### 3.4 Track Validation（赛道验证）

| 验证链路 | 得分 | 说明 |
|----------|------|------|
| Career DNA → [Track Name] | 78 | 用户在该 Track 的 Track Confidence |
| [Track Name] → [Role] JD | 72 | Track Core Skills 与 JD 要求的覆盖比例 |
| **Triangulated Validation（三角验证）** | **Strong / Moderate / Weak** | |

> 三角验证：用户 ↔ Track ↔ JD，比直接 User→JD 匹配更稳定可靠。

---

## Part 4: Evidence Distance（证据距离 v1.5.4）

<!-- v1.5.3: Direct/Adjacent/Missing 三值；v1.5.4: D0-D4 五级距离 -->

### Distance Levels（距离等级）

| 级别 | 等级含义 | 定义 | 示例 |
|------|------|------|------|
| **D0** | Strong Direct（强力直接证据） | 完全同岗位 | Delivery Lead → Delivery Lead |
| **D1** | Functional Equivalent（职能等同） | 同职责 / 不同岗位 | [来源岗位A] → [目标职能B] |
| **D2** | Transferable Evidence（可转移证据） | 同能力域 / 不同场景 | 制造业流程建设 → 敏捷教练 |
| **D3** | Inferential Evidence（推理证据） | 需解释的映射 | 数据分析 → 数据方案落地 |
| **D4** | No Evidence（无证据） | 无可信映射 | ERP 系统 → CRM 项目 |

### 4.2 Evidence Matrix（证据分析矩阵 v1.5.6 合并版）

<!-- Distance + Strength 合并为单表，避免重复 -->

| JD 能力 | DNA 证据 | Distance | Strength | 说明 |
|---------|----------|:--:|:--:|------|
| [某能力] | 多团队沟通机制 | D1 | 5 | 主导+多项目验证+高相关 |
| 跨团队协调 | 跨部门协调实战 | D1 | 5 | 跨团队+量化结果 |
| 流程优化 | 传统团队流程改造 | D2 | 4 | 语境不同但方法可迁移 |
| 数据方案 | 数据分析项目 | D3 | 4 | 有实践，非 ToB 落地 |
| 客户培训 | 无 | D4 | 0 | — |

> Distance 回答"像不像"（D0-D4，Capability Score 内部映射 D0=100/D1=85/D2=65/D3=40/D4=0）。
> Strength 回答"硬不硬"（0-5，5=主简历主叙事，4=简历可写，3=面试补充，≤2=仅内部参考）。
> D3 必须附推理依据。

### 4.3 Strength Rules（强度使用规则 v1.5.6）

| Strength | 含义 | 材料投放 |
|:--:|------|------|
| **5** | 强证据（主导+跨团队+量化+近期+直接相关） | 主简历主叙事，面试开场故事 |
| **4** | 中强证据 | 简历主体，不抢第一叙事位 |
| **3** | 中证据 | Interview Pack / Answer Cards |
| **≤2** | 弱证据 | 仅内部参考 |
| **0** | 无证据 | 不写 |

> 评分维度（5 因子 × 0-2 分 → 0-10 → 0-5）见 `references/mode_d_job_application.md` Step 5.5。
> Evidence Strength 不进入 Match Score 主公式。

---

## Part 5: Role Authenticity（角色真实性 v1.5.4）

<!-- 招聘先看"你是谁"，再看"你做过什么" -->

### Authenticity Level（真实性等级）

| 等级 | 定义 | 示例 | 分数区间 |
|------|------|------|----------|
| **Level A** | 真实角色 — JD 与简历头衔一致 | Delivery Lead → Delivery Lead | 90+ |
| **Level B** | 相邻角色 — 同域不同岗 | [岗位A] / [岗位B] / [岗位C] | 70-89 |
| **Level C** | 能力相似 — 跨域可迁移 | 运营经理 / 制造业经理 | 40-69 |
| **Level D** | 跨赛道 — 需要转行 | 销售 / 客服 | 0-39 |

### Authenticity Assessment（真实性评估）

| JD Role | 用户最高相关头衔 | 等级 | Score | 判定依据 |
|---------|-------------|:--:|-------|----------|
| [Role A] | [相关头衔] | [A/B/C/D] | [XX] | [判定依据] |
| [Role B] | [相关头衔] | [A/B/C/D] | [XX] | [判定依据] |

### Hire Probability Adjustment（录用概率修正）

| JD Role | Match Score | Authenticity | Hire Probability |
|---------|:----------:|:----------:|:----------------:|
| [Role A] | 86 | 82 | **≈ 70** |
| [Role B] | 72 | 75 | **≈ 54** |
| [Role C] | 70 | 48 | **≈ 34** |

> **Hire Probability = Match Score × (Role Authenticity / 100)**
> 不直接修改 Match Score，而是作为乘法修正因子。

---

## Part 6: Recruiter Risk Funnel（招聘漏斗风险 v1.5.4）

<!-- v1.5.3 只有 High Risk Questions；v1.5.4 预测"卡在哪一关" -->

### Hiring Pipeline Stages（招聘阶段）

| 阶段 | 决策者 | 核心风险 | 判定依据 |
|------|--------|----------|----------|
| **ATS** | 系统 | 关键词缺失 | Hard Requirement 覆盖率 |
| **HR** | 招聘 | 履历不像 | Role Authenticity Level |
| **Hiring Manager** | 业务 | 深度不足 | Evidence Distance D2+D3 占比 |
| **Offer Committee** | 综合 | 不是最像那个人 | Authenticity + Gap Priority |

### Risk Assessment（风险评估）

| 阶段 | 风险 | 依据 |
|------|:--:|------|
| ATS | Low | Hard Req Coverage 85% |
| HR | **High** | Authenticity B，跨头衔需解释 |
| Hiring Manager | **High** | D2/D3 占比 40%，深度证据不足 |
| Offer | Medium | Gap P0 缺失可快速补 |

### Stage-Specific Countermeasures（阶段对策）

| 风险阶段 | 对策 |
|----------|------|
| ATS | 已覆盖 ✓ |
| HR | 简历标题用"原头衔 (相关域) → 目标岗位"定位 |
| Hiring Manager | 准备 2 个深度案例 + 1 个冲突处理场景 |
| Offer | 投递前补认证（预估 2-4 周可行） |

---

## Part 7: Decision Score（决策评分 v1.5.6）

<!-- 全部因子来自 JD + DNA，零市场假设 -->

### Factor Types（因子类型 v1.5.6）

| 类型 | 含义 | 示例因子 |
|------|------|----------|
| **Core（核心项）** | 直接参与计算的基础分 | Match Score |
| **Multiplier（乘数项）** | 以 Match 为基础做乘法修正 | Hire Probability（= Match × Authenticity/100） |
| **Additive（加分项）** | 有则加分，无则 0 | Location, Language, Industry |

### Decision Factors（决策因子）

| 因子 | 类型 | 权重 | 判定来源 | 示例 |
|------|:--:|:--:|------|:--:|
| **Match Score（匹配度）** | Core | 50% | → 3.2 Overall | 65 |
| **Hire Probability（录用概率）** | Multiplier | 25% | → Part 5 | 65 × 0.75 ≈ 49 |
| **Location Advantage（城市优势）** | Additive | 10% | 同城市=10pt | 10 |
| **Language Advantage（语言优势）** | Additive | 10% | 外语=10pt | 10 |
| **Industry Advantage（行业优势）** | Additive | 5% | 同行业=5pt | 5 |

> 公式：Decision = 0.5×Match + 0.25×HireProb + Location + Language + Industry
> 计算结果 → 填入 3.1 摘要。

### Decision Score（对比）

| 岗位 | Match(50%) | HireProb(25%) | Location(10%) | Language(10%) | Industry(5%) | **Decision** |
|------|:----:|:----:|:----:|:----:|:----:|:----:|
| [Role A] | 43 | 18 | 10 | 5 | 5 | **81** |
| [Role B] | 36 | 14 | 10 | 10 | 3 | **73** |
| [Role C] | 35 | 9 | 10 | 5 | 0 | **59** |

> Decision Score ≠ 匹配度。回答的是"综合条件下值不值得现在投"。表中数值为加权后的贡献值（原始分 × 权重百分比），非原始分数。

---

## Part 8: Recommended Strategy（推荐策略 v1.5.6）

### 8.0 Usable Evidence Summary（可用证据汇总 v1.5.6）

<!-- 从 Part 4 矩阵中提取 Strength ≥ 3 的证据，按 Strength 和 Distance 综合排序 -->

| 优先级 | 证据 | Distance | Strength | 来源 |
|------|------|:--:|:--:|------|
| **Top 1** | [主证据] | D1 | 5 | [来源项目] |
| **Top 2** | [次证据] | D1 | 5 | [来源项目] |
| **Top 3** | [补强证据] | D2 | 4 | [来源项目] |
| **Secondary** | [次要证据] | D2 | 4 | [来源项目] |

> Strength 5 → 主简历标题区 + 面试开场故事。Strength 4 → 简历主体补强。Strength 3 → Interview Pack。

### 8.1 Greeting Recommendation Summary（打招呼策略摘要 v1.6.3）

<!-- 供上游 Greeting 生成器直接消费，不回读整份报告 -->

- **Recommended Type（推荐类型）**: Type [A/B/C/D]
- **Alternative Type（备选类型）**: Type [A/B/C/D]
- **Recommended Reason（推荐理由）**: [一句话]
- **Alternative Reason（备选理由）**: [一句话]
- **Suggested Tone（建议语气）**: [直接 / 稳妥 / 克制 / 好奇心]

### 8.2 Gap Priority Matrix（缺口优先级矩阵）

| 缺口 | Impact（影响度） | Cost（补齐成本） | Priority（优先级） | 建议行动 |
|------|:---:|:---:|:---:|------|
| [认证A] | High | Low | **P0** | 2-4周考取 |
| [经验B] | High | High | **P1** | 6月积累实践 |
| [案例C] | Medium | High | **P2** | 主动争取项目 |

> - **P0**: High Impact + Low Cost → 立刻做
> - **P1**: High Impact + High Cost → 计划做
> - **P2**: Low/Medium Impact → 有余力再做

#### Detail Gaps（详细缺口）

| 缺失能力 | Skill Weight | Impact | Cost | Priority |
|----------|-------------|:------:|:----:|:--------:|
| [能力X] | 25% | High | Low | P0 |
| [能力Y] | 10% | Low | High | P2 |

### 8.3 Narrative Mapping（叙事映射 v2.6.1）

<!-- 叙事主线 = 07 Career Narrative + JD 适配角度 -->

**我的核心叙事**（来自 `07_career_identity` Layer 3 Career Narrative）：
[07 的核心职业叙事，如 "[状态A] → [状态B]" + 价值主张]

**JD 适配角度**（来自 Step 2 Hiring Intent + Step 3 Talent Persona）：
[JD 需要什么样的人，用什么角度切入]

**叙事主线**：
[一句话：将 07 核心叙事与 JD 适配角度结合的故事主线]

> 逻辑：我的核心叙事是「从 [起点] 到 [能力]」，JD 需要 [某特质] 的人，因此叙事主线为：「我是一个通过 [核心能力] 推动 [JD需要的结果] 的人」

### 8.4 Key Projects & Stories（推荐项目与故事）

| # | 项目/故事 | 匹配理由 | 涉及能力 |
|---|----------|----------|----------|
| 1 | [项目A] | [理由] | [能力] |
| 2 | [项目B] | [理由] | [能力] |

### 8.5 Application Advice（投递建议）
- **Hire Probability（录用概率）**: ≈ [XX]
- **是否建议投递**: 是 / 谨慎 / 否
- **策略建议**:
- **重点关注**:

### 8.6 Boss Greeting Input Pack（Boss 打招呼语素材包 v1.6.1）

<!-- 不做新分析，仅摘要素材给 07_boss_greeting.md 消费 -->

- **Greeting Objective（打招呼目标）**: Type A / B / C / D
- **Primary Hook（最强匹配点 — 来自 8.0 Top 1）**:
- **Supporting Evidence（辅证据 — 来自 8.0 Top 2）**:
- **Safe Evidence（安全区证据 — Type C 防翻车用）**:
- **Curiosity Bait（好奇心诱饵 — Type D 专用）**:
- **Avoid（不建议提）**:
- **Recommended Platform Priority**: Boss > 猎聘 > 邮件

---

## Part 9: Outreach Package（外联沟通包 v1.6.2）

<!--
从 Evidence Matrix 到 Platform Greeting 的桥梁层。
Part 4 分析证据 → Part 9 路由证据 → 07_boss_greeting 消费证据。
Greeting 不再自己选证据。
-->

### 9.1 Evidence Routing（证据路由 v1.6.2）

#### Candidate Pool（候选池）
从 Part 4 Evidence Matrix 提取 Strength ≥ 4 的全部证据。

#### Routing Rules（路由规则）

| 优先级 | 规则 | 逻辑 |
|:--:|------|------|
| **Rule 1** | Distance Priority（距离优先） | D0/D1 永远排最前，D2 次之，D3 仅作备选 |
| **Rule 2** | Role Relevance（角色相关度） | 与 JD Role 直接相关 → 升一级；仅间接相关 → 降一级 |
| **Rule 3** | Novelty Injection（新奇注入） | 若 Top2 证据过于同质化，允许插入 1 个 D2/D3 好奇心证据 — 仅作为第三证据 |

#### Routing Output（路由输出）

| 层级 | 选取规则 | 用途 |
|------|------|------|
| **Primary（主证据）** | Rule 1+2 最高分证据，通常 D0/D1 | Greeting 核心卖点，简历主叙事 |
| **Secondary（辅证据）** | Rule 1+2 次高分证据，D1/D2 | 补强匹配度，猎聘/邮件用 |
| **Curiosity（好奇心证据）** | Rule 3 注入，D2/D3 但 Strength≥4 | Boss Type D / LinkedIn 开场用 |

> Primary/Secondary 必须与 JD Role 直接相关。Curiosity 允许跨域，但仅在 Type D 中使用。

### 9.2 Platform Variants（平台变体 v1.6.2）

| 平台 | 目标 | 字数 | 结构 | 证据策略 |
|------|------|:--:|------|------|
| **Boss 直聘** | 让 HR 回复 | 60-120 | 一句价值 + 一个问题结尾 | Primary 证据 1 个 |
| **猎聘** | 建立专业感 | 150-250 | 背景 + 匹配点 + 交流意愿 | Primary + Secondary |
| **邮件** | 正式投递 | 300+ | 背景 + 项目 + 优势 + 附简历 | Primary + Secondary + 可选 Curiosity |
| **LinkedIn** | 建立关系（非求职硬推） | 80-120 | 轻量连接 + 行业共识 + 不附简历 | Curiosity 或 Primary 中最行业相关的 |

#### LinkedIn 参考结构

> Hi [Name],
>
> I noticed you're hiring [Role] at [Company]. I spent [N] years in [Industry/Domain], and your opening caught my attention.
>
> Would love to connect and learn more about what you're working on.
>
> Best,
> [Name]

> LinkedIn 连接消息不附简历、不开口就问"有没有机会"。目标是建立联系，不是推销。
