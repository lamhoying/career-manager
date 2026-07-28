# Mode D: Job Application Mode（岗位投递模式 v1.4）

## Trigger（触发条件）

用户提供以下任一信息：
- JD（Job Description）
- 职位描述
- 招聘链接
- 岗位要求

## Preconditions（前置条件）

`career-dna/` 目录必须已存在。如不存在，先执行 Mode A（Career DNA Build Mode）。

## Objective（目标 v1.4）

从 JD 关键词提取升级为 Talent Persona Inference（人才画像推理）。不仅分析 JD"要什么技能"，更要推理"要什么样的人、为什么招、怎样证明匹配"。

## Talent Intelligence Pipeline（人才智能分析管线 v1.4）

```
JD
↓
Step 1: Role Decomposition（岗位能力拆解）
    └── 输出：Core Functions / Responsibilities / Expected Ownership
↓
Step 2: Hiring Intent Analysis（招聘意图分析）
    └── 输出：Explicit / Implicit Requirements / Business Context
↓
Step 3: Talent Persona Inference（人才画像推理）
    └── 输出：Ideal Candidate / Career Background / Typical Experience / Preferred Traits
↓
Step 4: Evidence Expectation Analysis（证据需求分析）
    └── 输出：Critical Evidence / Expected Stories / Expected Results
↓
Step 5: DNA Match Analysis（基因库匹配分析 v1.4.2）
    └── Persona Match(35%) + Evidence Match(35%) + Capability Match(30%)
↓
Step 5.5: Capability Translation Analysis（能力迁移分析 v1.4.4）
    └── Direct Match(100%) / Adjacent Match(60%) / Missing(0%) / Mapping Boundary
↓
Step 6: Targeted Discovery（定向证据发现）
    └── 基于 Evidence Expectation + Match Gaps 定向追问
↓
Step 7: Career DNA Update（职业资产回写）
Step 8: Resume Package（求职材料包）
Step 9: Knowledge Update（知识更新 → 沉淀 Talent Persona/Evidence Expectation 到 knowledge/）
```

---

## Step 1: Role Decomposition（岗位能力拆解）

### 目标

对 JD 进行深层次拆解，不仅识别技能标签，更要理解岗位的核心职能和期望责任级别。

### 拆解维度

从 JD 中分析：

| 维度 | 说明 | 示例 |
|------|------|------|
| **Core Functions（核心职能）** | 这个岗位在公司里承担什么角色 | 交付执行者 / 客户对接窗口 / 项目 Owner |
| **Responsibilities（核心职责）** | 具体的日常工作和关键任务 | 项目排期和进度管理 / 客户需求调研 / 团队协调 |
| **Expected Ownership（期望责任级别）** | 独立执行？带人？跨部门推动？ | Lead（独立负责完整项目）/ Support（辅助） |
| **Reporting Structure Hint（管理层级暗示）** | 向谁汇报？带不带团队？ | 向 VP 汇报 → 高级别 |
| **Scope Hint（范围暗示）** | 单项目？多项目？跨地域？ | 多项目并行 → 需要强资源协调能力 |

### 输出格式

```yaml
Role: [标准化 Role 名称]
Core Functions: [核心职能描述]
Responsibilities:
  - [职责1]
  - [职责2]
Expected Ownership: [Lead / Partial Lead / Support]
Management Scope: [带团队 / 独立执行 / 辅助]
Project Scope: [单项目 / 多项目 / 跨地域]
```

---

## Step 2: Hiring Intent Analysis（招聘意图分析）

### 目标

超越 JD 字面意思，推理公司真正的招聘动机——为什么招这个人？要解决什么问题？

### 分析维度

| 维度 | 说明 | 分析方式 |
|------|------|----------|
| **Explicit Requirements（显性要求）** | JD 明文写出的要求 | 直接提取 |
| **Implicit Requirements（隐性要求）** | JD 没写出但可推理的要求 | 从 JD 上下文 + Role Snapshot Trend + 行业常识推理 |
| **Business Context（业务背景）** | 招这个人的业务原因 | 从公司阶段（扩张？替补？新业务？）推理 |
| **Pain Point（痛点推断）** | 团队当前缺什么能力 | 从 JD 高频强调或特殊要求推理 |

### 输出格式

```yaml
Explicit Requirements: [显性要求列表]
Implicit Requirements: [隐性要求列表]
Business Context: [业务背景推理]
Pain Point: [团队痛点推断]
Hiring Reason: [新设岗位 / 替补离职 / 业务扩张 / 项目需求]
```

---

## Step 3: Talent Persona Inference（人才画像推理）

### 目标

基于 Role Decomposition + Hiring Intent + Role Snapshot，推理出理想候选人的完整画像——不只是一串技能，而是一个有职业背景、有典型经历、有特质的人。

### 推理维度

| 维度 | 说明 |
|------|------|
| **Ideal Candidate（理想候选人）** | Natural-language 描述：什么样的人？ |
| **Career Background（职业背景）** | 典型来自什么行业、什么岗位、几年经验 |
| **Typical Experience（典型经历）** | 应该经历过什么项目、做过什么角色 |
| **Preferred Traits（偏好特质）** | 独立性强？沟通力强？推动力强？ |

### 输出格式（Human-readable 自然语言输出, not keyword list 非关键词列表）

```yaml
Ideal Candidate:
  "具有项目交付经验，能独立面对客户，具备需求梳理和推进能力的实施型人才"
Career Background:
  - 来自 [行业]
  - [N] 年以上 [领域] 经验
Typical Experience:
  - [典型经历1]
  - [典型经历2]
Preferred Traits:
  - [特质1]
  - [特质2]
```

---

## Step 3.5: Skill Weight Analysis（能力权重分析 v1.4.1）

### 目标

从 JD 措辞、Role Snapshot 频率、行业常识三个维度推理各能力的相对重要性，输出带权重的能力列表。

### 推理三维度

| 维度 | 权重来源 | 评分逻辑 |
|------|----------|----------|
| **JD 措辞优先级** | JD 文本 | "必须/要求" > "优先" > "熟悉/了解"；首段出现 > 中段 > 尾段 |
| **Role Snapshot 频率** | `knowledge/role_snapshots/{role_name}.md` Skill Frequency | 频率 ≥ 80% → 3pt, 50-80% → 2pt, < 50% → 1pt |
| **行业常识** | 基于 Evidence Expectation 推理 | Critical Evidence 对应的能力自动 +1pt |

### 输出格式

```yaml
Skill Weights:
  - 能力: Stakeholder Management
    Weight: 35%
    Reasoning: JD 高频出现 + Role Snapshot 频率 90% + Critical Evidence 对应
  - 能力: Project Delivery
    Weight: 25%
    Reasoning: JD 明确要求（必须）
  - 能力: Risk Management
    Weight: 20%
    Reasoning: Role Snapshot 频率 75%
  - 能力: Data Analysis
    Weight: 10%
    Reasoning: JD 提及但非核心
```

### 用途

- Step 5 DNA Match 时：Gap 按能力权重加权评分（Critical + 高权重缺失 = 严重 Gap）
- Skill Graph Gap 优先级排序：权重越高的能力，Evidence Count = 0 时越致命
- 未来 v1.5 Skill Mapping（技能映射引擎）：直接使用权重表作为映射输入

---

## Step 4: Evidence Expectation Analysis（证据需求分析 v1.5.2 内部推理）

### 目标

从 Talent Persona 反向推理面试官期望的证据类型。**v1.5.2 不单独写入报告 Part 5**（与 Evidence Mapping 3.5 重复），作为 Step 5 DNA Match 中 Evidence Quality 评定的内部推理依据。

### 推理维度（v1.4.1 结构化 / v1.5.2 Internal Use Only）

### 目标

从 Talent Persona 反向推理——面试官会问什么来验证候选人？简历和面试中需要展示什么证据？

### 推理维度（v1.4.1 结构化）

| 维度 | 说明 |
|------|------|
| **Critical Evidence（关键证据）** | 必须在简历/面试中展示的证据，缺一不可 |
| **Expected Ownership（期望责任级别）** | 该证据应展现的责任层级：Owner(独立负责) / Lead(主导) / Support(辅助) |
| **Expected Scope（期望范围）** | 该证据应展现的影响范围：Global(跨组织) / Department(跨团队) / Team(团队内) |
| **Expected Impact（期望影响）** | 该证据应展现的业务影响类型：Revenue / Efficiency / Delivery / Quality |
| **Expected Stories（预期案例）** | 面试官可能问的项目案例类型 |
| **Evidence Risks（证据风险）** | 用户可能缺乏的证据区域，附关联能力权重 |

### 输出格式（v1.4.1 结构化）

```yaml
Critical Evidence:
  - 证据项: Cross-team Coordination
    Importance: Critical
    Expected Ownership: Lead
    Expected Scope: Department
    Expected Impact: Efficiency
    Interview Question: "请举一个跨部门推动项目的例子"
  - 证据项: Client-facing Delivery
    Importance: High
    Expected Ownership: Owner
    Expected Scope: Global
    Expected Impact: Revenue
    Interview Question: "如何处理客户现场的需求变更？"
Expected Stories:
  - 案例类型: 需求调研案例 → 期望 Ownership: Lead / Scope: Department
  - 案例类型: 客户培训案例 → 期望 Ownership: Owner / Scope: Global
Evidence Risks:
  - 证据薄弱区域: 跨组织推动经验 → 缺失影响: High（对应能力权重 35%）
  - 证据薄弱区域: 量化交付数据 → 缺失影响: Medium（对应能力权重 20%）
```

**Evidence Scoring Rule（证据评分规则）**：
- Ownership (Owner=3, Lead=2, Support=1) + Scope (Global=3, Dept=2, Team=1) + Impact (Revenue=3, Efficiency=2, Delivery=2, Quality=1) = Evidence Score
- ≥7pt = Strong Evidence / 4-6pt = Moderate / ≤3pt = Weak

---

## Step 5: DNA Match Analysis（基因库匹配分析）

### 目标

将 Talent Persona + Evidence Expectation 与 Career DNA 交叉比对，输出匹配度。v1.4 的匹配更精准——不是比技能列表，而是比画像+证据。

### 读取的数据源

- `career-dna/04_skill_graph.md` — 能力图谱
- `career-dna/03_projects.md` — 项目资产
- `career-dna/05_story_bank.md` — 故事库
- `career-dna/07_career_identity.md` — 职业身份
- `career-dna/10_career_tracks/{track}.md` — Career Track
- `career-dna/02_timeline.md` — 职业轨迹
- `knowledge/role_snapshots/{role_name}.md` — Role Snapshot

### 匹配维度（v1.5.2 升级为 4 维度）

| 匹配维度 | 权重 | 说明 |
|----------|------|------|
| **Hard Requirement Match（硬性要求匹配）** | 40% | 学历/语言/证书/年限 — 逐项给分 0-100（v1.5.3 颗粒化），终结 ✓/△/✗ 三值判定 |
| **Experience Match（经验匹配）** | 30% | 行业/场景/角色重叠度 — Career Background vs Ideal Candidate |
| **Capability Match（能力迁移匹配 v1.5.4）** | 20% | D0=100% / D1=85% / D2=65% / D3=40% / D4=0%（v1.5.4 升级：五级证据距离替代 Direct/Adjacent/Missing） |
| **Industry Match（行业匹配）** | 10% | 同行业/同客户群/同业务场景 — 从 Role Snapshot Industries 判定 |

**Hard Requirement 评分逻辑（v1.5.3 颗粒化）**：
逐项给分 0-100，替代旧的 ✓/△/✗ 三值判定。每项附「扣分来源」说明。

扣分规则：
- 头衔不匹配但经验存在 → 扣 20-30（Adjacent-style）
- 年限差距 → 按比例扣（差1年扣10-15）
- 证书缺失但能力存在 → 扣 10-20
- 完全缺失 → Score = 0

最终 Hard Requirement Match = ∑(各项 Score) / 项数。

### Match Confidence 计算（v1.5.6 公式+扣分收紧）

**Match Confidence = Evidence Count(30%) + Evidence Quality(30%) + Direct Relevance(25%) + Evidence Stability(15%)**

| 分量 | 计算方式 | 扣分条件 |
|------|----------|----------|
| **Evidence Count（证据数量）** | (可用证据项数 / 总匹配能力数) × 100 | 总能力 < 3 项 → 直接扣 20 |
| **Evidence Quality（证据质量）** | (High×100 + Medium×60 + Low×30) / 总数 | Low 占比 > 50% → 直接 -15 |
| **Direct Relevance（直接相关性）** | D0+D1 占比（>50%=85 / 30-50%=65 / <30%=45） | D3+D4 > 60% → 直接 -10 |
| **Evidence Stability（证据稳定性）** | 核心能力跨项目频次（3+=90 / 2=65 / 1=40） | 最高频次能力 ≠ 最高权重能力 → -5 |

> Evidence Stability 替代 Market Validation。全部基于 DNA 内部证据。

### Track Validation 计算（v1.5.2 新增）

三角验证链路：用户 ↔ Track ↔ JD

- **DNA→Track**: 取 `10_career_tracks/{track}.md` 的 Track Confidence
- **Track→JD**: Track Core Skills 在 JD 中的覆盖比例（覆盖数/总数）
- **Triangulated**: 两段均 ≥ 70 → Strong / 一段 < 70 → Moderate / 两段均 < 70 → Weak

### 写入文件

`resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md`（使用 v1.5.4 8-Part 模板）

---

## Step 5.5: Evidence Distance Analysis（证据距离分析 v1.5.4）

### 目标

替代 v1.4.4 的 Direct/Adjacent/Missing 三值分类，升级为 D0-D4 五级证据距离。解决"两个 Adjacent 距离完全不同但都被标为 Adjacent"的问题。

### 距离等级

| 级别 | 等级含义 | 判定条件 | 内部映射 | 需附依据 |
|:--:|------|------|:--:|:--:|
| **D0** | Strong Direct（强力直接） | JD能力=DNA能力（同岗位同名） | 100 | |
| **D1** | Functional Equivalent（职能等同） | 同职责/不同岗位（核心流程一致） | 85 | 职责分析 |
| **D2** | Transferable Evidence（可转移） | 同能力域/不同场景（方法论相同） | 65 | 场景对比 |
| **D3** | Inferential Evidence（推理证据） | 推理映射（需解释为什么） | 40 | 必须附推理 |
| **D4** | No Evidence（无证据） | 无证据或 Speculative | 0 | |

**升级规则**：
- D3 必须附推理依据（1-2句），否则强制降为 D4
- D0-D4 为对外展示等级名，百分数不直接对用户展示
- Speculative Match 禁止规则不变

### Evidence Coverage 计算（v1.5.3 + v1.5.4 升级）

对每个 JD 能力拆分子证据项，分别判定 D0-D4，汇总计算：

```
Coverage = (D0子证据数×100 + D1×85 + D2×65 + D3×40 + D4×0) / 总子证据数
```

### 输出

写入 `01_jd_match_report.md` Part 4 Evidence Distance Mapping 表。

### Evidence Strength 判定（v1.5.5 新增）

#### 目标

在 Distance 映射完成后，评估每条证据的强度——能不能进主简历？能不能打面试？

#### 评分维度

| 维度 | 说明 |
|------|------|
| Ownership（主导程度） | 主导=2pt / 参与=1pt / 无=0pt |
| Scope（覆盖范围） | 跨团队=2pt / 单团队=1pt / 单人=0pt |
| Impact（结果影响） | 有量化=2pt / 有过程=1pt / 无=0pt |
| Recency（时效性） | 1年内=2pt / 1-4年=1pt / 4年+=0pt |
| Relevance（相关性） | 直接=2pt / 间接=1pt / 不相关=0pt |

#### 映射规则

- 总分 9-10 → Strength 5：主简历主证据，面试开场故事
- 总分 7-8 → Strength 4：简历可写，适合补强
- 总分 5-6 → Strength 3：面试补充，不作主打
- 总分 3-4 → Strength 2：内部参考，不建议写进简历
- 总分 1-2 → Strength 1：极弱证据
- 总分 0 → Strength 0：不写

#### 联动规则

- Strength 5 证据 → 优先进入 Interview Pack 开场故事
- Strength ≤ 2 → 不进入主简历，仅内部参考
- **Evidence Strength 不进入 Match Score 公式**，仅影响材料投放策略

#### 输出

写入 `01_jd_match_report.md` Part 4.5 Evidence Strength Mapping 表。

### 输出格式

以下情况**强制归入 D4，不可建立任何 Distance**：

| 拒绝类型 | 示例 |
|----------|------|
| 跨行业跳跃（行业不相关） | 客服经验 → 架构师职责 |
| 无证据关联（无项目支撑） | 财务经验 → Unity 开发 |
| 领域无交集 | 设计经验 → DevOps |

---

## Step 5.6: Role Authenticity Inference（角色真实性推理 v1.5.4）

### 目标

判断用户的职业身份与 JD 岗位的接近程度。招聘先看"你是谁"，再看"你做过什么"。

### 判定逻辑

1. 提取用户在 `07_career_identity.md` 和 `02_timeline.md` 中的最近岗位头衔
2. 与 JD Role 对比：
   - 同岗位 → Level A (90+)
   - 同域不同岗 → Level B (70-89)
   - 跨域可迁移 → Level C (40-69)
   - 跨赛道 → Level D (0-39)
3. 根据 Track Confidence 和 Evidence Distance D0/D1 占比微调 ±10

### 输出

写入 `01_jd_match_report.md` Part 5（含 Authenticity Assessment + Hire Probability 修正）。

---

## Step 5.7: Recruiter Risk Funnel（招聘漏斗风险 v1.5.4）

### 目标

预测候选人在招聘 4 阶段中的通过风险，回答"为什么投了没面试"。

### 判定逻辑

| 阶段 | 判定依据 |
|------|----------|
| **ATS** | Hard Requirement Coverage — < 70% → High Risk |
| **HR** | Role Authenticity Level — C/D → High, B → Medium |
| **Hiring Manager** | Evidence Distance D2+D3 占比 — > 40% → High |
| **Offer Committee** | Gap Priority P0 数量 — ≥ 2 → High |

### 输出

写入 `01_jd_match_report.md` Part 6（含风险评估表 + 阶段对策）。

---

## Step 5.8: Decision Score（决策评分 v1.5.4）

### 目标

不只看"匹配度"，更看"值不值得现在投"。全部因子来自 JD+DNA。

### 公式

**Decision Score = 0.5×Match + 0.25×HireProbability + Location + Language + Industry**

- Match = Part 3.2 Overall Match Score（0-100）
- Hire Probability = Match × (Role Authenticity / 100)（来自 Step 5.6）
- Location = JD城市=用户城市→10pt
- Language = 外语能力→10pt | 方言优势→10pt（取最高）
- Industry = 同行业→5pt（来自 Role Snapshot Industries 比对）

### 输出

写入 `01_jd_match_report.md` Part 7。

---

## Step 6: Targeted Discovery（定向证据发现）

**目的**：基于 Evidence Expectation 的 Evidence Risks 和 DNA Match 的 Gaps，定向追问。

**规则**：---

## Step 6: Targeted Discovery（定向证据发现）

**目的**：基于 Evidence Expectation 的 Evidence Risks 和 DNA Match 的 Gaps，定向追问。

**规则**：
- 只追问 3-10 个高价值问题
- 优先追问 Critical Evidence 覆盖缺失
- 利用 Talent Persona 提供的 Preferred Traits 作为追问方向

详细规则见 `references/targeted_discovery.md`。

---

## Step 7: Application Strategy Decision（求职策略决策 v1.5.1）

### 目标

基于 Overall Match Score + Capability Translation 结果，判定求职策略，选择对应的 Package。

### 策略判定

| Strategy（策略） | Match Score | 适用场景 | Package |
|------------------|-------------|----------|---------|
| **Strong Fit（强匹配）** | ≥ 80 | Persona + Evidence + Capability 三项均高 | Pack A |
| **Moderate Fit（中等匹配）** | 60-79 | 两项以上中等，有可补强的 Gap | Pack B |
| **Stretch Fit（拉伸匹配）** | 40-59 | Adjacent 占比高，跨方向转岗申请 | Pack C |
| **Weak Fit（弱匹配）** | < 40 | 匹配度极低，不建议直接投递 | Pack D |

### 边界升级/降级规则

- Adjacent 占比 > 60% 且 Match Score ≥ 40 → **升为 Stretch Fit**
- Missing 中含有 Skill Weight > 30% 的 Critical 缺失 → **降一档**
- 用户已明确"只投这个方向" → 不降档

### 策略输出

写入 `resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md` Part 6 匹配总览新增一行：

```yaml
Application Strategy（求职策略）: Strong Fit / Moderate Fit / Stretch Fit / Weak Fit
Package（生成包）: Pack A / B / C / D
```

---

## Step 8: Career DNA Update（职业资产回写）

同 v1.3 逻辑，新增 v1.4 更新：
- 更新 `10_career_tracks/{track}.md` 的 **Market Validation / Matched Hiring Intent / Evidence Strength**

---

## Step 9: Resume Package（求职材料包 v1.5.1）

按 Step 7 的策略决定生成哪套文件。详细产出合约见 `references/output_contracts.md`。

### Pack A: Strong Fit — 投递包（Match ≥ 80）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | 完整 JD 分析 + Capability Translation |
| 2 | `02_resume_cn.md` | 中文 ATS 简历 |
| 3 | `03_resume_en.md` | 英文 ATS 简历 |
| 4 | `04_interview_pack.md` | 面试准备包 |
| 5 | `05_answer_cards.md` | 回答卡片库 |
| 6 | `06_upgrade_plan.md` | 竞争力升级计划 |

### Pack B: Moderate Fit — 投递+补强包（Match 60-79）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | 完整 JD 分析 |
| 2 | `02_resume_cn.md` | 中文 ATS 简历 |
| 3 | `03_resume_en.md` | 英文 ATS 简历 |
| 4 | `04_interview_pack.md` | 面试准备包 |
| 5 | `05_answer_cards.md` | 回答卡片库 |
| 6 | `06_gap_analysis.md` | **能力差距分析（v1.5.1 新增）** |
| 7 | `07_upgrade_plan.md` | 升级计划 |

### Pack C: Stretch Fit — 转岗包（Match 40-59）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | 完整 JD 分析 |
| 2 | `02_transition_resume_cn.md` | **转岗中文简历** — 突出 Adjacent Match 可迁移能力 |
| 3 | `03_transition_resume_en.md` | **转岗英文简历** |
| 4 | `04_capability_translation.md` | 能力迁移分析报告（基于 Part 6.5） |
| 5 | `05_gap_analysis.md` | 能力差距分析 |
| 6 | `06_interview_pack.md` | 面试准备包（含转岗高频问题） |
| 7 | `07_upgrade_plan.md` | 升级计划 |

### Pack D: Weak Fit — 学习路线包（Match < 40）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | JD 分析 |
| 2 | `02_gap_analysis.md` | 能力差距分析 |
| 3 | `03_transition_feasibility.md` | 转岗可行性评估 |
| 4 | `04_learning_roadmap.md` | 学习路线图 |

> Pack D 不生成简历和面试包，避免硬包装。

---

## Step X: Boss Greeting Generation（Boss 打招呼语生成 v1.6.1）

### 目标

将 v1.5.6 最终收敛结果压缩为一条可诱导 HR 回复的首条消息。不重新计算分数。

### 输入字段（仅读取 v1.5.6 收敛值）

| 输入 | 来源 |
|------|------|
| Match Score + Decision Score | `01_jd_match_report.md` 3.1 |
| Greeting Objective + Primary Hook + Safe Evidence + Curiosity Bait | `01_jd_match_report.md` 8.5 |
| 可用证据 Top1/Top2 | `01_jd_match_report.md` 8.0 |
| HR 风险阶段 | `01_jd_match_report.md` Part 6 |

### Greeting Objective 选择（v1.6.1 升级）

| 条件 | Objective | 版本 |
|------|-----------|------|
| Decision ≥ 80 + HR 风险 Low | Type A: Build Connection | Version A |
| Decision 60-79 + HR 风险 Low-Medium | Type B: Prove Value | Version B |
| Authenticity C/D 或 HR 风险 High | Type C: Break Risk | Version C |
| 有技术亮点 / AI 项目 / 独特经历 | Type D: Spark Curiosity | Version D |
| Match < 40 | 不生成 | — |

### Evidence Selection 规则（v1.6.1 新增）

从 `01_jd_match_report.md` 8.0 Usable Evidence Summary 自动选取：
- Top 1（主证据）：Strength=5 + Distance≤D1
- Top 2（辅证据）：Strength≥4，与 Top 1 不重复
- 备选（Type B 用）：8.0 Secondary
- 安全区（Type C 用）：8.5 Safe Evidence
- 好奇心诱饵（Type D 用）：8.0 中 D2/D3 但 Strength 最高的证据（制造意外感）

### 平台变体（v1.6.1 新增）

| 平台 | 字数上限 | 策略 |
|------|:--:|------|
| Boss 直聘 | 150 字 | 速读友好，一句话价值 + 一个问题结尾诱导回复 |
| 猎聘 | 200 字 | 半正式，简要匹配 + 行动邀请 |
| 邮件 | 300 字 | 正式商务，完整介绍 + 附简历 |

### 生成规则

- 禁止使用报告术语（Match Score / Confidence / Risk Funnel 等）
- 每条消息以一个问题结尾（诱导 HR 回复）
- 禁止大段经历陈述（首条消息不是简历摘要）
- 不使用弱证据代替 Top1/Top2

### 输出

`resume-outputs/{YYYYMMDD}-{company}-{role}/07_boss_greeting.md`

---

## Step 8.5: Evidence Routing Engine（证据路由引擎 v1.6.2）

### 目标

在生成 Greeting 前先对可用证据做路由分层。解决"跨域证据被选为岗位钩子"的问题。

### 路由规则

| 优先级 | 规则 | 操作 |
|:--:|------|------|
| **Rule 1** | Distance Priority | 对 Part 4 中 Strength≥4 的证据按 D0>D1>D2>D3 排序 |
| **Rule 2** | Role Relevance | 从 Part 2.1 Core Responsibilities 和 2.4 Ideal Candidate 提取关键词，与证据名做语义匹配。直接相关→升一级，仅间接相关→降一级 |
| **Rule 3** | Novelty Injection | 若 Primary+Secondary 均来自同一能力域，从 D2/D3 中选 Strength 最高作为 Curiosity（仅第三位） |

### 输出

写入 `01_jd_match_report.md` Part 9.1 Evidence Routing。

---

## Step 8.6: Platform Strategy（平台策略 v1.6.2）

### 目标

不同平台目标不同，不只是长度不同。

### 平台逻辑

| 平台 | 核心目标 | 禁止事项 |
|------|------|------|
| **Boss 直聘** | 让 HR 回复（非介绍自己） | 不用长段经历 / 不附简历 |
| **猎聘** | 建立专业感 | 不"一句话勾引" |
| **邮件** | 正式投递 | 不"反问一句"结尾 |
| **LinkedIn** | 建立关系（非求职硬推） | 不提求职 / 不附简历 / 不评估匹配度 |

### Boss 直聘专属规则

- 60-120 字，结构：1 句价值证明 + 1 个反问
- 证据策略：Part 9.1 Primary 证据 1 个
- 不以"期待您的回复"结尾 → 以诱导性问题结尾

### LinkedIn 专属规则

- 英文为主，80-120 字
- 结构：自我介绍 → 关注点 → 连接邀请
- 证据策略：Curiosity 或 Primary 中最行业相关的
- 不附简历

### 输出

写入 `01_jd_match_report.md` Part 9.2。

---

## Step 8.8: Greeting Strategy Selection（打招呼策略选择 v1.6.3）

### 目标

在 Evidence Routing 和 Platform Strategy 完成之后，输出推荐 Type + 备选 Type + 结构化推荐理由。不再输出全部 Type 版本。

### 推荐方案选择规则

| 条件 | Recommended Type |
|------|:--:|
| Decision ≥ 80 + HR Low + Primary Distance ≤ D1 | Type A |
| Decision 60-79 + HR Low-Medium | Type B |
| Authenticity C/D 或 HR High | Type C |
| Primary 中 Curiosity 证据 Strength=5 且与 Role 有关联 | Type D |

### 备选方案选择规则

| 推荐 Type | 常用备选 Type | 切换逻辑 |
|:--:|:--:|------|
| Type A | Type D | 主推太泛时，备选走好奇心破局 |
| Type B | Type D | 证据够但不惊艳，备选制造意外 |
| Type C | Type B | 转行风险高，备选先证明价值 |
| Type D | Type B | 好奇心强但 HR 偏保守时兜底 |

### 推荐理由必须结构化

```yaml
Why Recommended:
  - Match Basis: [Decision Score + Authenticity]
  - Evidence Basis: [Primary 证据 + Distance]
  - Risk Basis: [HR 风险 + 是否可控]

Why Alternative:
  - Switch Condition: [何时切换]
  - Difference: [语气/证据/策略差异]
```

---

## Step 8.9: Greeting Humanization（打招呼语人味化 v1.6.3）

### 目标

去"模型腔"和"报告腔"，让消息更像真人。

### 人味化规则

| 规则 | 说明 |
|------|------|
| 句子更短 | Boss 60-120字，语句短于 25 个字 |
| 不用AI连接词 | 避免"同时""此外""基于""因此""从而" |
| 不用总结腔 | 不写成简历摘要或报告段落 |
| 自然问句结尾 | 轻问题促回复 |
| 不堆材料 | 1 主证据 + 至多 1 辅证据 |
| 不用过度自夸 | 用"比较接近""之前做过"替代"主导""高度匹配" |
| 开头不模板 | 不说"我有X年经验，在X做过X" |

### 输出

写入 `07_boss_greeting.md` Recommended Greeting + Alternative Greeting。

---

## Step 8.10: Recommended / Alternative Output（推荐/备选输出 v1.6.3）

### 输出规则

- 每平台仅输出 2 个版本（Recommended + Alternative）
- 每个版本附 Why Recommended / Why Alternative
- 附 Tone Notes + Do Not Say
- 不输出全部 Type 版本 / 内部评分术语

### 输出

写入 `07_boss_greeting.md` 完整文件。

---

## Step 10: Knowledge Update（知识更新）

### A. 更新 knowledge/role_snapshots/{role_name}.md（v1.4.1 增强）

1. 更新 **Common Hiring Intent**：基于本次 Hiring Intent Analysis 合并更新（典型招聘意图）
2. 更新 **Talent Persona**：基于本次 Talent Persona Inference 合并更新（典型画像特征）
3. 更新 **Typical Evidence**：基于本次 Evidence Expectation（含 Ownership/Scope/Impact）合并更新
4. 更新 **Career Background Distribution**：本 Role 常见职业背景分布
5. 更新 **Skill Weight Baseline**（v1.4.1 新增）：基于多次 Skill Weight Analysis 累积各能力的平均权重
6. 更新 **Hiring Intent Trends / Talent Persona Trends / Evidence Trends**（≥3 次观察后）

### B. 更新 knowledge/skill_snapshots/{domain_name}.md（v1.4.1 增强）

每个 Skill 更新：

1. 更新 **Aliases**（v1.4.1 新增）：如 JD 中出现该 Skill 的新表述，追加到 Aliases 列表（去重）
2. 更新 **Typical Evidence**：含 Ownership/Scope/Impact 三维度的典型证据形式
3. 更新 **Business Meaning**：该 Skill 在业务中的价值解释
4. 更新 **Related Hiring Intent**：该 Skill 关联哪类招聘意图
5. 更新 **Typical Results**：该 Skill 的典型成果量化方式
6. 更新 **Typical Ownership**：基于多次 Evidence Expectation 的 Expected Ownership 均值

### C. 更新 career-dna/10_career_tracks/{track}.md（v1.4.2 增强）

1. 重新计算 **Track Confidence Breakdown**：Evidence Strength / Role Snapshot Validation / Market Demand 三分量
2. 更新 **Validation Status**：基于 JD 频率和覆盖比例判定 Validated / Emerging / Uncertain
3. 更新 **Market Validation**：本次 JD 是否验证了该 Track 的市场需求
4. 更新 **Matched Hiring Intent**：哪些 Hiring Intent 被本次 JD 覆盖
5. 更新 **Evidence Strength**：基于 Evidence Expectation 评估证据强度（Strong / Moderate / Weak）
6. 更新 **Market Demand Signals / Recent JD Coverage / Market Signal**

### Knowledge Update 逻辑总结（v1.4.2）

```
JD
↓
Talent Persona → Role Snapshot（Skill Weight Baseline + Persona Statistics）
    ↓
Evidence Expectation → Skill Snapshot（Typical Evidence + Aliases + Ownership 均值）
    ↓
Career Track（Track Confidence Breakdown + Market Validation + Recent JD Coverage）
```

---

## Important Rules（重要规则 v1.4）

1. **JD 不只是技能列表**。每个 JD 背后有 Hiring Intent、Talent Persona、Evidence Expectation 三层深度信息。
2. **Talent Persona 优先于技能匹配**。先推理"要什么样的人"，再做"能力匹配"。
3. **Evidence 是连接器**。Talent Persona → Evidence Expectation → Career DNA Evidence 形成完整证据链。
4. **JD Match Report 是完整分析档案**。保存 6 部分完整推理过程，不只存匹配结果。
5. **Knowledge 层积累推理结果**。Role Snapshot 不只记录职责，更记录 Hiring Intent 和 Talent Persona 的趋势。
6. **resume-outputs 按次隔离**。`{YYYYMMDD}-{company}-{role}/` 子目录。
7. **Targeted Discovery 严格控制**。最多 10 个问题，不长时间盘问。
