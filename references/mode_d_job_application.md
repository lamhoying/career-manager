# Mode D: Job Application Mode（岗位投递模式）

> Aligns to: v2.19.0
## Trigger（触发条件）

用户提供以下任一信息：
- JD（Job Description）
- 职位描述
- 招聘链接
- 岗位要求

## Phase Routing（两阶段分流 v2.17.0）

Mode D 拆为 **两阶段 + 一道决策门**：**默认停在门后**（省钱优先），用户明确要材料才连跑。

| Phase | 名称 | 范围 | 产物 |
|---|---|---|---|
| **P1** | **Recon（侦察 · 报告层）** | Step 1 / 2 / **2.9** / 3 / 3.5 / 4 / 4.5a(TC Mapping) / 5 / 5.5 / 5.6 / 5.7 / 5.8 / 6 / 7 / 8 / **10.A-C** | `01_jd_match_report.md`（9 Part + 附录 A/B，**完整自足**）+ `career-dna/` 与 `knowledge/` 回写 |
| — | **Phase Gate（决策门）** | 无步骤，只有输出协议（见 §Phase Gate） | 决策摘要 + 三选项 |
| **P2** | **Build（材料生成 · token 主体）** | Step **4.5b(Identity Lock 重执行)** / 8.5 / 8.6 / 8.8 / 8.9 / 8.10 / 8.12 / 9 / 9.0 / 9.1 / 9.5 / X / **10.D** | Pack A/B/C/D 全部文件 + `deliverables/` |

> **`Step 4.5a` / `Step 4.5b` 拆分（v2.18.0）**：本文件原有两个同名 `## Step 4.5:` 节 —— a = Transferable Capability Mapping 属 **P1**；b = Resume Identity Lock 属 **P2 入口（重执行）**。v2.18.0 已把**正文章节标题**同步为 `4.5a` / `4.5b`（此前只改了引用侧、标题侧未同步，导致 `§Step 4.5` 定位撞车）。**编号只做后缀区分，顺序不变**。

**分流规则（入口判定 · 词表）**：

| 用户话语 | 动作 |
|---|---|
| 「看看这个 JD / 分析一下 / 匹配度怎么样 / 帮我了解这家公司」 | **P1 only** → 出报告后停在 Gate |
| 「帮我投这个 / 生成简历 / 做材料包 / 出一份简历投 XX」 | **P1 + P2 连跑**（一步到位通道） |
| 「生成材料 / 继续 / 出 Pack B」且 `01` 报告已存在 | **P2 Resumption**（见 §Phase Gate 续跑规则） |
| **无法判断** | **默认 P1 only**（fail-safe）+ 一句话告知「如需材料请说『生成材料包』」 |

> **fail-safe 方向 = 省钱优先**（与 `R03` 的「无该赛道条目 → 禁角色标签、禁补写」同源：不确定时选保守侧）。
> **一步到位通道仍先落 `01` 报告再生成材料** —— 产物一个不少，只是不停下阻塞。
> **禁止**凭「用户以前要过材料」推断本次也要 —— 判定只看**本次**话语。

## Preconditions（前置条件）

`career-dna/` 目录必须已存在。如不存在，先执行 Mode A（Career DNA Build Mode）。

## Objective（目标 v1.4）

从 JD 关键词提取升级为 Talent Persona Inference（人才画像推理）。不仅分析 JD"要什么技能"，更要推理"要什么样的人、为什么招、怎样证明匹配"。

## Talent Intelligence Pipeline（人才智能分析管线 v2.17.0）

```
JD
↓
═════════════ Phase 1: Recon（侦察 · 报告层）═════════════
Step 1    Role Decomposition（岗位能力拆解）
Step 2    Hiring Intent Analysis（招聘意图分析）
Step 2.9  Appendix Generation（附录 A 术语速查 / 附录 B 公司背景尽调）
Step 3    Talent Persona Inference（人才画像推理）
Step 3.5  Skill Weight Analysis（能力权重分析）
Step 4    Evidence Expectation Analysis（证据需求分析）
Step 4.5a Transferable Capability Mapping（可迁移能力映射）
Step 5    DNA Match Analysis → Match Confidence / Track Validation
Step 5.5  Evidence Distance Analysis（证据距离 → D0-D4）
Step 5.6  Role Authenticity Inference（角色真实性 → HireProbability 的折扣因子）
Step 5.7  Recruiter Risk Funnel（招聘漏斗风险）
Step 5.8  Decision Score（0.7×Match + 0.3×HireProb）
Step 6    Targeted Discovery（定向证据发现 —— 向【用户】补证据，不是决策门）
Step 7    Application Strategy Decision → Pack A/B/C/D
Step 8    Career DNA Update（career-dna 唯一回写口）
Step 10.A-C Knowledge Update（Role / Skill Snapshot + Track Market Validation + 新赛道发现）
    └── 产物：resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md（9 Part + 附录 A/B）
═════════════ Phase Gate（决策门）═════════════
    决策摘要 + 三选项（生成材料 / 只留报告 / 换策略）—— 详见 §Phase Gate
═════════════ Phase 2: Build（材料生成 · token 主体）═════════════
Step 4.5b Resume Identity Lock（【重执行】：从 07 锁身份 —— 身份锚点不可落盘，须在新上下文重建）
Step 8.5 / 8.6 / 8.8 / 8.9 / 8.10 / 8.12（证据路由 → 平台策略 → 策略选择 → 人味化 → 推荐/备选 → 叙事对齐）
Step 9    Capability-Driven Resume Generation（能力驱动简历生成）
    └── 9.0 Per-Experience Engine Loop（逐经历重构循环 → 逐段 E01-E04）
    └── 9.1 Resume QA Layer（QA-1~QA-4 四检 → 全部通过才输出）
Step 9.5  Delivery Finalization（opt-in：用户说「要投了」才净化 / 审核 / 导出 deliverables/）
Step X    Boss Greeting Generation（Boss 打招呼语生成）
Step 10.D 投递索引登记（Status = Planned）
    └── 产物：Pack A/B/C/D 全部文件
```

> **`01` 报告是自足的**：P2 的全部输入都能从「`01` 报告 + `career-dna/` 文件」恢复 ——
> Skill Weight → Part 2.3｜Hiring Intent → 2.2｜Talent Persona → 2.4｜Capability Translation → Part 4｜
> Evidence Expectation → 4.1｜Track Validation → 3.4｜Portfolio → 8.6｜Greeting 素材 → 8.7｜Greeting 策略 → 8.1。
> 故 **P2 无需重跑 Step 1-7**（续跑规则见 §Phase Gate）。
> **v2.17.0 顺带修正**：旧图把 `Step 7` 标成「Career DNA Update」、`Step 8` 标成「Resume Generation」、`Step 9` 标成「Knowledge Update」——
> 与实际章节编号（7 = Application Strategy / 8 = Career DNA Update / 9 = Resume Generation / 10 = Knowledge Update）**整体错位一位**。本图按实际章节名重写。

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

## Step 2.9: Appendix Generation（附录生成 —— 术语速查 / 公司背景尽调 v2.15.0）

### 目标

**两个附录，两种分寸，同一个判据 ——「是否随 JD 变」**：

| 附录 | 判据推论 | 分寸 |
|---|---|---|
| **附录 A** JD 专业名词 | 同 track 内**高度重复**（通用词每份都会撞） | **收窄准入 + 指针复用**（少写，不是写到别处） |
| **附录 B** 公司背景尽调 | **基本不重复**（每家公司的赛道 / 阶段 / 岗位位置都不同） | **每次必做 + 只分深度** |

**版式骨架**（表头 / 列头 / 占位符）见 `pack_templates/01_jd_match_report_template.md` 附录区 —— **本节只写生成规则，不重述版式**（避免多定义点）。

> ⚠️ 附录用 `附录 A/B` 命名，与 `Part 1-9` **正交** —— **不改 Part 编号、不进 Part 骨架**。

---

### A. 附录 A 生成（JD 专业名词）

**判据 = 「是否产生决策信息」，不是「是不是专业词」。** 三级准入：

| 级 | 准入判据 | 处理 |
|:--:|---|---|
| **A 级** 门槛判定型 | 该术语构成 JD **硬性要求 / 加分项** | **必写**，且必须有「用户现状」列（✓ / ⚠️ 可迁移 / ✗ 缺） |
| **B 级** 陌生领域扫盲型 | 用户对该 **track / 行业无背景**、术语构成理解障碍 | **仅该 track 首次出现时写一次** |
| **C 级** 纯释义型 | 该词**已出现在 Career DNA 的能力描述中** | **禁写** |

**C 级判据的执行方式（关键）**：查 `04_skill_graph.md` / `04b_transferable_capabilities.md` 的能力描述文本 ——
**Career DNA 就是「已知词表」**。凡其中已出现的词（如 5 年 QA 视角下的「功能测试 / 回归测试 / 测试用例」），解释它等于零增益。
→ **不新建术语库、不加闸门、不加维护钩子**（符合「不新增定义点」原则）。

**同 track 复用规则（根治「同 track 重复生成」）**：

1. 先检索 `resume-outputs/` 下**同 track** 的历史 `01_jd_match_report.md`（Track 字段 / 头部注释的 Track 标注）；
2. 有历史报告 → 附录 A 只写 **① 一行复用指针**（形如「通用术语已在 `resume-outputs/{先前日期}-{公司}-{岗位}/01 附录 A` 解释」）+ **② 本批新增术语**；通用词**不重抄**；
3. 无历史报告 → 按三级准入全量筛选，但**总条数 ≤20**。

**形态约束**：列宽 ≤3 列 ｜ ≤20 条（不含笔误对照）｜ 分组名按实际内容生成（禁留空组）｜ 笔误对照**独立成节**（它是 Part 1 逐字存档的配套，不属术语解释，故不计入 20 条）。

---

### B. 附录 B 生成（公司背景尽调）

**目的**：为投递决策补上**公司侧维度** —— 让用户判断「**这家公司值不值得去**」+「**这个岗位在这家公司意味着什么**」。

> **为什么每次必做**：投递是不可逆的时间投入（备材料 / 面试 / 可能的入职后不匹配），
> **单份 JD 恰恰是信息最少、风险最高的场景**。故**「条数」只决定深度，不决定做不做**。

#### B.1 边界（四处，禁止互相复制）

| 承载体 | 职责 |
|---|---|
| `13` §10.1 尽调三维度 | 查什么 / 从哪查（**通用清单**，不随 JD 变） |
| `01 Part 2.2` Business Context | **结论一行**（claim）→ 指向附录 B（evidence）；**反向禁止** |
| `01 Part 7` Decision Score | **投递建议**（Fit → Pack）—— 但**纯能力导向**，公司维度缺席 |
| **附录 B** | 本次查到了什么 + 由此推出什么（**论证**） |

> ⚠️ **附录 B 不产出第二个「投 / 不投」结论** —— 否则与 Part 7 重复，且可能相反。
> 末尾只写一行「**对 Part 7 的影响**」（加强 / 削弱 / 无关），**不改分数、不改 Pack**。

#### B.2 深度分级（取代「做不做」的开关）

| Tier | 何时 | 内容 |
|:--:|---|---|
| **Tier 1**（每次必有 · 下限） | **所有 JD 报告，含 Pack C/D** | 四项决策摘要（≈15 行） |
| **Tier 2**（值得深挖） | 满足任一升级条件 | Tier 1 + 五层调查 + 组织信号 + 四算子 + 口径冲突留痕 |
| **Tier 3**（同公司复投） | 同公司 ≥2 次投递 | Tier 2 + **时点对比**（上次 vs 本次变化） |

**Tier 1 四项**（缺一不可）：① 公司往哪走（三时态锚点**简版**，锚点缺一 → 写「阶段未定」）② 岗位在哪一层（基本盘 / 增长 / 故事）③ JD 组织信号（发布者 + ≥1 处信号）④ 对 Part 7 的影响。

**升级条件 → Tier 2**：同公司 / 同批次 ≥2 份 JD ｜ JD 与业务阶段有**需解释的关联**（转型 / 跨界 / 新业务线）｜ 非知名企业需外查 ｜ 用户明确要求。

**兜底**：公司信息查不到时**允许写「未获取」**，但**必须显式写出**。
⚠️ **Tier 1 第 3 项（JD 自身信号）永不适用兜底** —— 零成本可得，缺席即失职。**这一条是「每次必做」能成立的前提**（否则退化为「查不到 → 不写 → 又变回条件触发」）。

#### B.3 查什么（5 层）与怎么推理（4 算子）—— 完整清单见附录区注释

- **5 层**：①身份 ②规模 ③财务 ④市场 ⑤**组织信号层**（★ 最高价值 —— 前四层靠外部检索（有成本 / 有时效），第⑤层**直接从 JD 读**：零成本、绝对准确、别人查不到）
- **4 算子**：① 三时态锚点法 ② 三层结构（「谁供养谁」）③ **JD 信号交叉印证**（前提认知：**JD 是组织的自白书**；五类信号 = 频率 / 时态 / 文本复制 / 发布者 / 内部矛盾）④ 否定性证据（**必须同时写反面**）
- **五条纪律**（红线）：每条判定挂锚点 ｜ 口径冲突并列留痕 ｜ 查不到写「未获取」｜ 只用公开信息 + JD 交叉印证 ｜ 数据标时点

> 具体字段表与信号读法见 `pack_templates/01_jd_match_report_template.md` 附录 B 区（唯一版式定义源）。

#### B.4 同公司复用（不建库）

同公司二次投递时：**复用上次附录 B 的公司侧事实层**（身份 / 规模 / 财务 / 市场）并改指针，
但 **Tier 1 第 2、3 项（岗位在哪一层 / JD 组织信号）每次必写** —— 它们**随 JD 变**，复用即错误。

> **不建 `knowledge/company_snapshots/`**：事实层重复一次的成本，低于新建资产层的维护成本 + 漂移风险。
> 升级判据：同公司投递 **≥3 次** 或需跟踪季度变化时，再评估。
> ⚠️ 与 `role_snapshot` 的分工：后者是**按岗位**（跨公司），公司快照是**按公司**（跨岗位）—— 二者**正交**，不可混用。

---

### C. 输出

- 附录直接追加在 `01_jd_match_report.md` **Part 8 之后**（不改 Part 编号）；
- 收尾自检按 `01` 模板「收尾检查」块执行（附录 A 条数 / C 级 / Tier 1 四项 / 锚点 / 无第二结论）；
- **不新增闸门** —— 附录落在 `resume-outputs/`（**非 Career DNA SSOT**），现有 `validate_career_dna.py` 扫 `career-dna/`，扩展扫描范围成本 > 收益。

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

## Step 4.5a: Transferable Capability Mapping（可迁移能力映射 v2.3）

**目标**：将 JD 要求的岗位语言映射到用户的实际能力。

**流程**：
1. 提取 Step 2 Role Decomposition 中 JD 要求的核心能力
2. 查询 `knowledge/role_snapshots/{role}.md` 的 Role Capability Model
3. 调用 `career-dna/04b_transferable_capabilities.md` 查找匹配项
4. 对每个 JD 能力输出匹配结论：
   - Direct：用户有此能力的直接 Transferable Keywords
   - Adjacent：用户能力通过 Transferable 可转换，记录转换路径
   - Missing：用户无此能力且无相邻能力可转

**输出**：写入 JD Match Report Part 4 Evidence Matrix 的 Capability Match 列。

---

## Step 4.5b: Resume Identity Lock（简历身份锁定 v2.6）

> **Phase：P2 入口前置动作（重执行）** —— 身份锚点（本节输出）**不是可落盘产物**，而是后续步骤的锚点，
> 故 P2 续跑时**必须在新一轮上下文里重新执行本节**（读 `07_career_identity.md` 锁身份，成本极低）。
> P1 阶段在 Step 5 之前执行过本节，那是为 Match 判定服务；**P2 重执行是为生成服务**，两者不互替。

### 目标

在进入 DNA Match 和简历生成流程之前，从 `07_career_identity` 强制锁定职业身份。**后续所有步骤（Step 5-10）的简历生成必须以本步骤的身份为唯一锚点。**

### 输入

| 来源 | 提取内容 |
|------|------|
| `07_career_identity` Layer 1 | Professional Identity |
| `07_career_identity` Layer 2 | Career Positioning（Primary） |
| `07_career_identity` Layer 5 | Non-Positioning Statement |

### 输出

```yaml
Resume Identity Lock:
  职业身份: [07 Layer 2 Primary Positioning]
  禁止表达: [07 Layer 5 全部条目]
  身份来源: 07（禁止从 Timeline / 岗位历史推导）
```

> **K4 交叉指针（v2.19.0）**：本结构与 `references/online_profile_generation.md` §Identity Resolution
> 是**同一身份**在两个渠道的应用（本处 = ATS 简历渠道，那里 = Online Profile 渠道）。
> **定义在 `07`**（头部已声明「07 是 Identity 的唯一定义源」），两处均为**渠道级应用** —— 刻意不合并，
> 依据 `references/output_contracts.md` 的跨渠道边界（「共享 = Identity 07」）。

### 硬约束

- 简历中的「职业定位」「个人总结」「核心能力」必须以本步骤的身份为唯一来源
- 禁止从 Timeline 的岗位频次推导职业身份
- 禁止从 JD 反推「我应该是什么身份」
- 07 Layer 5 中列出的原始岗位不得出现在简历的身份表达层（仅可作为事实信息在「公司·岗位」行出现）

### Identity Lock vs Role Tailoring（v2.6）

Resume Identity Lock 锁定的是「职业身份的核心名词」，不是简历上的每一个字：

- **锁定**：Career Positioning 的核心词（如 "项目管理"、"交付驱动"）
- **不锁定**：JD 适配的修饰语（如 "技术背景的" + JD 岗位名）
- **不锁定**：「求职意向」行（直接填 JD 岗位名，不填 07 Positioning）
- **不锁定**：经历描述中 JD 关键词的自然融入

规则：身份核心名词来自 07，语境措辞来自 JD，经历证据来自 03/04b。三层各司其职。

---

## Step 5: DNA Match Analysis（基因库匹配分析 v2.6）

### 目标

将 Talent Persona + Evidence Expectation 与 Career DNA 交叉比对，输出匹配度。v2.6 输入新增 Step 4.5b Resume Identity Lock → 约束匹配解释方向（身份核心名词不可由 Timeline 覆盖）。

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

`resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md`

> **版式实体模板**：`references/pack_templates/01_jd_match_report_template.md`（9-Part 骨架 + 表格列头 + 字段占位）。01 报告所有 Part 内容由本 Step + 后续 Step 逐步填充；模板只锁版式、不锁内容。全 Pack 模板索引见 `references/pack_templates/README.md`。

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

> **唯一定义源（v2.19.0）**：本节的「评分维度 + 映射规则 + 联动规则」是 **Evidence Strength 评分口径的唯一定义源**。
> `assets/templates/career-dna/03_projects.md` 的 `### Evidence Strength` 表只承载**结果**，口径以本处为准。
> （沿用本项目既有惯例：规则唯一定义源在 mode_d，版式/资产侧只放结果或指针。）

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

写入 `01_jd_match_report.md` **Part 4.2 Evidence Matrix 的 `Strength` 列**。

> **v2.18.0 澄清**：历史上曾有独立的 `Part 4.5 Evidence Strength Mapping` 节，已在早期版本**合并进 Part 4**（独立映射表删除、仅保留 Strength 规则）。canonical Part 4 现存 `4.1 / 4.2 / 4.3`，**无 4.5** —— 故落点为 4.2 的 Strength 列。

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

## Step 5.8: Decision Score（决策评分 v2.16.0 —— 本步是评分规则的唯一定义源）

### 目标

不只看"匹配度"，更看"值不值得现在投"。全部因子来自 JD+DNA。

### 公式（v2.16.0 改写）

**Decision Score = 0.7 × Match + 0.3 × HireProbability**

展开（代入 `HireProbability = Match × Role Authenticity / 100`，见 Step 5.6）：

**Decision Score = Match × (0.7 + 0.3 × Role Authenticity / 100)**

- Match = Part 3.2 Overall Match Score（0-100）
- Hire Probability = Match × (Role Authenticity / 100)（来自 Step 5.6）
- Role Authenticity = `Role Authenticity Inference` 的 Level 对应分值（A 90+ / B 70-89 / C 40-69 / D 0-39）

**语义**：把 Match 按「**用户的职业身份与 JD 岗位的接近程度**」加权 —— 身份越接近，折扣越小：

| Role Authenticity | 折扣系数 | Decision |
|:--:|:--:|---|
| 100%（同岗位 · Level A 顶格） | 无折扣 | = Match |
| 75%（同域不同岗 · Level B） | ×0.925 | 0.925 × Match |
| 50%（跨域可迁移 · Level C） | ×0.85 | 0.85 × Match |
| 0%（跨赛道 · Level D） | ×0.70 | 0.70 × Match |

> **术语澄清（v2.16.0）**：`Role Authenticity` 指的是「**用户的职业身份与 JD 岗位的接近程度**」（Step 5.6，Level A-D），**不是**「岗位真实性 / 该 JD 是否虚假」。本步折扣语义据此表述，勿反向解释为「招聘意图真伪」。

**无附加项、无常数项** → 档位阈值恢复语义：**≥80 强烈建议投 / 60-79 建议投 / <60 谨慎**。

### Factor Types（因子类型 v2.16.0）

| 类型 | 含义 | 本版因子 |
|------|------|----------|
| **Core（核心项）** | 直接参与计算的基础分 | Match Score（权重 70%） |
| **Multiplier（乘数项）** | 以 Match 为基础做乘法修正 | Role Authenticity（经 HireProbability 进入，权重 30%） |
| **Additive（加分项）** | **v2.16.0 废除 —— 本版已无 Additive 因子** | — |

### Additive 废除原因（三项各有归属，剥离不丢信息）

| 原因子 | 病 | 信息归属 |
|---|---|---|
| **Language** | **双计**（`Hard Requirement Match` 40% 说明中已含「语言」且逐项给分，Decision 再 +10）+ **白送**（JD 未提外语仍 +10 —— 实测 7 份无外语要求 JD 全部加满） | `Hard Requirement Match` **独占**（逐项颗粒化，精度高于「全给 / 全不给」的开关） |
| **Industry** | **双计**（`Match` 4 维度已含独立维度 `Industry Match 10%`）+ **口径矛盾**（Match 说「部分相关 45」/ Decision 说「无关 0」） | `Industry Match` **独占**，口径矛盾随之消失 |
| **Location** | **零方差**（实测 12/12 全 +10，方差 0.00）= 常数项，不改变排序、只平移分数 | 筛选阶段已完成（用户只投目标城市），无需二次计分 |

> **常数项的实质危害不是排序错乱，而是绝对档位失准**：Location + Language = 20 分常数 → **实际门槛从 60 降到 40**。
> 实证：`Match 63 / HireProb 35` → 能力侧 `0.5×63 + 0.25×35 = 40.25`，靠 +20 凑到 60.25 即判「建议投」。

### Situational Factors（情境因子 —— 展示项，不参与判定）

三项剥离后改为 **Label 展示**（**非 Score**，仅作 tie-breaker 与投递成本提示）：

| 因子 | 展示形式 | 依据来源 |
|---|---|---|
| Location | 「同城 ✓」/「异地（需考虑搬迁 / 通勤）」 | 不量化 |
| Language | 「JD 要求 + 已达标」/「涉外增量优势」/「不相关」 | 要求部分归 `Hard Requirement Match` |
| Industry | 「同行」/「相邻」/「无关」 | 归 `Match` 的 `Industry Match` |

**硬约束**：情境因子**不得折回总分、不得参与档位判定、不得给分值位**。
（这是「加列 / 加字段必须同时加维护钩子」的反向应用：既然它不参与判定，就不该拥有分值。）

### 输出

写入 `01_jd_match_report.md` Part 7 —— **必须展示 `Match × Role Authenticity` 拆解**（Part 7 版式见 `references/pack_templates/01_jd_match_report_template.md`，**本步为规则唯一定义源，该模板为版式唯一定义源**）。

> **v2.16.0 起不再要求展示「剔除附加项后的纯能力盘面」** —— 新公式下已无附加项可剔。改为强制展示 `Match × Role Authenticity` 拆解。

---

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

写入 `resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md` **Part 3.1 Match Summary** 的两个字段：

```yaml
Application Strategy（求职策略）: Strong Fit / Moderate Fit / Stretch Fit / Weak Fit
Package（生成包）: Pack A / B / C / D
```

---

## Step 8: Career DNA Update（职业资产回写）

同 v1.3 逻辑，新增 v1.4 更新：
- 更新 `10_career_tracks/{track}.md` 的 **Market Validation / Matched Hiring Intent / Evidence Strength**

**写入契约（v2.10.0）**：本步骤是 Mode D 唯一允许回写 `career-dna/` 的环节，且只能更新**已登记文件**（清单见 `assets/career_dna_manifest.json`）。若 Targeted Discovery 挖出的是「跨 JD 通用的面试战术」，回写到 `13_interview_narrative_strategy.md`；若是「本次 JD 专用策略」，留在 `resume-outputs/{JD}/`，**不得**在 career-dna 根目录新建文件。

⚠️ **回写 13 的硬边界**：**只允许改 Part 4-12（手写区），禁止覆盖 Part 1-3（派生区）** —— 派生区是从 07/02/05/03/04b 推导出来的，手工改写会在下次刷新时被覆盖，或直接造成口径冲突。回写后运行 `python3 scripts/validate_career_dna.py <career-dna目录>` 自检：报 P1 `derived-part-drift` = 分区标题丢失（手写区被吃掉）；报 P1 `undeclared-part` = 有 Part 未登记入 manifest。**不得在 13 里新建未登记的 Part**。

---

## Phase Gate（决策门 v2.17.0）

> **本段是 Gate 协议的规则唯一定义源**；`SKILL.md` 与 `references/output_contracts.md` 只写指针，不复制本协议。

P1 结束（`01` 报告落盘 + Step 8 / 10.A-C 回写完成）后，**必须停下**并输出以下三段，然后等待用户决策：

```
① 决策摘要（约 5 行）
   Match {score} / HireProbability {x} / Decision {档位}
   一句话结论：建议投 / 谨慎 / 不建议
   建议 Pack：Pack {X}（{N} 个文件）—— 依据 01 Part 8 Application Advice

② 可选动作（三选一）
   (a) 生成 Pack {X}          ← 默认推荐，回「生成材料」即可
   (b) 只保留报告，不生成材料
   (c) 换策略生成（如 Match 建议 Pack B，改做 Pack C / 只要 gap_analysis）

③ 一个提示（条件出现）
   若 Step 6 有未回填的追问 → 「生成材料前建议先补答 {N} 个问题，否则简历会带 [待补充]」
```

**禁止**在 Gate 处重复 Part 1-9 的论证、重复一次「投 / 不投」结论（与附录 B 的边界纪律同源：**一个结论只出现一次**）。

### 续跑规则（防重跑 · 幂等）

**状态载体 = 文件系统**（不引入新状态文件）：

| 判定 | 依据 |
|---|---|
| P1 完成 | 存在 `resume-outputs/{YYYYMMDD}-{company}-{role}/01_jd_match_report.md` |
| P2 已启动 | `application-tracker/01_application_index.md` 存在该 Company + Role 行（由 Step 10.D 登记） |
| P2 完成 | 该 Pack 应产出的文件齐备（对照 `references/output_contracts.md` 清单） |

1. 用户二次说「生成材料 / 继续 / 出 Pack B」→ 识别为 **P2 Resumption**：**先读已有 `01` 报告**作为输入，**禁止重跑 Step 1-7**
2. **仅当**用户显式说「重新分析 / JD 变了 / 这份 JD 换了」→ 才重跑 P1（并覆盖 `01` 报告）
3. P2 内已存在文件 → **增量重生成该文件**，不删其他 Pack 产物（保留用户可能已改的内容）
4. **P1 后不生成材料 ≠ 失败**：此时产物只有 `01` 报告 + 知识回写，目录**不登记**投递索引（「分析过」≠「要投」，见 Step 10.D）

### 三个「停」不是同一件事

| 机制 | 性质 | 层次 |
|---|---|---|
| Step 6 Targeted Discovery | **补输入**（向用户追问证据，3-10 题） | P1 内部 |
| **Phase Gate** | **做决策**（要不要生成材料） | P1 / P2 之间 |
| Step 9.5 Delivery Finalization | **定稿导出**（opt-in：「我要投了」） | P2 内部 |

> 用户若在 P1 说「别问了，直接出报告」→ 跳过 Step 6，未答问题转为 Gate 第 ③ 段的条件提示。

---

> **Step 8.x 编号说明（v2.18.0）**：本段步骤编号为 `8.5 / 8.6 / 8.8 / 8.9 / 8.10 / 8.12` —— **`8.7` 与 `8.11` 无对应步骤**（历史版本记录无删除项，属历史跳号；**不补编号**，避免与历史留痕不符）。
> ⚠️ 与 `01_jd_match_report_template.md` 的 **Part 8.x**（报告章节编号，`8.0`–`8.7` 连续）**是两套独立体系，勿混**。

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

写入 `07/08_boss_greeting.md`（编号随 Pack：A=07 / B=08）Recommended Greeting + Alternative Greeting。

---

## Step 8.10: Recommended / Alternative Output（推荐/备选输出 v1.6.3）

### 输出规则

- 每平台仅输出 2 个版本（Recommended + Alternative）
- 每个版本附 Why Recommended / Why Alternative
- 附 Tone Notes + Do Not Say
- 不输出全部 Type 版本 / 内部评分术语

### 输出

写入 `07/08_boss_greeting.md`（编号随 Pack：A=07 / B=08）完整文件。

---

## Step 8.12: Narrative Alignment（叙事对齐 v2.6.1）

### 目标

在生成面试和回答材料之前，将 `07_career_identity` Career Narrative + `04b` Capability Priority 对齐到 JD 语境。

### 输入

| 来源 | 内容 |
|------|------|
| Step 4.5b Resume Identity Lock | 职业身份 + 禁止表达 |
| `07_career_identity` Layer 3 | Career Narrative（核心叙事） |
| `07_career_identity` Layer 4 | Capability Priority（Tier A/B/C） |
| Step 2 Hiring Intent + Step 3 Talent Persona | JD 需要什么样的人 |

### 输出

```yaml
Narrative Alignment:
  核心叙事: [07 Layer 3]
  JD 适配角度: [JD 需要什么角度]
  叙事主线: [07 核心叙事 + JD 适配 — 一句话]
  Tier A Stories: [按 Narrative Strength 排序的 Story Bank 条目]
  面试身份框架: [07 Professional Identity 的一句话变体 — 适配 JD 语境]

Narrative Strength（叙事强度 v2.7.1）:
  评估维度:
    - Problem-Solution Arc: 是否有清晰的问题→解决→结果线（0-5）
    - Memorability: 是否能让面试官记住（0-5）
    - STAR Completeness: Situation/Task/Action/Result 完整度（0-5）
    - Identity Alignment: 是否强化 07 Career Narrative（0-5）
  总分: [0-20]
  用途: 面试故事排序（Interview Pack + Answer Cards）
```

### 规则

- Narrative Mapping → 写入 `01_jd_match_report.md` Part 8.3
- Tier A Stories → 按 Narrative Strength 总分排序（非 TC 优先级），应用于 `04_interview_pack.md`
- 面试身份框架 → 应用于 `05_answer_cards.md` 的回答框架
- **通用叙事底料 → 先读 `13_interview_narrative_strategy.md` 全部 12 个 Part**，再做 JD 适配。**禁止绕过 13 从 07/05 重新拼装通用话术**——13 是底料，`04`/`05` 是切片。逐 Part 映射：
  - Part 1-5 → `04` §1-§5 与 `05` 的通用框架
  - **Part 6（口径纵深卡）→ `04` §5 风险题 + `05` 风险卡**：数字与规模口径**必须逐字对齐 13 Part 6.3 交叉校验表**，禁止在本轮临时加码
  - **Part 7（分轮次与分题型打法）→ `04` §7.1**：只填本轮实际情况（几轮 / 谁面 / 形式），通用打法不在 `04` 重复；7.4 分题型的「考什么形式」映射到 `04` §7 的「形式」列
  - **Part 8（面试后跟进）→ `04` §8**：只记本轮实际动作与回应，通用方法不在 `04` 重复
  - **Part 9（复盘回路）→ 落 `application-tracker/archives/{Company}_{Role}.md`**，不进 `04`
  - **Part 10（反向尽调）→ `04` §7.2「本轮定制反问」** + 公司业务/阶段判断：**结论**落 `01` **Part 2.2**、**论证**落 `01` **附录 B**；通用调研方法不在 `04` 重复（附录 B 生成规则见 Step 2.9）
  - **Part 11（录用阶段 / Offer 谈判与背调）→ 落 `application-tracker/archives/{Company}_{Role}.md`**，**不进 `04`**（`04` 只记本轮实际谈判过程与结果）
  - **Part 12（英文面试准备）→ `04` §10**（条件必填：JD 明确要求英语工作语言时）；卡壳处置话术与语言能力表述不在 `04` 重复
- Step 9 简历生成前必须先完成本步骤

---

## Step 9: Capability-Driven Resume Generation（能力驱动简历生成 v2.6.4）

> **Phase：P2** —— 本节及 9.0 / 9.1 属材料生成层，须在 Gate 放行后执行；续跑时**从 `01` 报告取输入，不重跑 Step 1-7**。

### 生成顺序（不可逆）

```
Step 4.5b: Resume Identity Lock
    ↓ 确定职业身份（核心名词来自 07，不可变）
Step 3.5: Skill Weight（JD 关键词提取）
    ↓ 确定 JD 需要什么能力 + ATS 关键词
04b → Capability Interpretation（v2.6.4 第一层）
    ↓ 每条经历：原始岗位 → 角色解释 + 形成 TC + 关键证据
04b + Evidence Distance D0-D4 → JD Mapping（v2.6.4 第二层）
    ↓ JD 要求 ← TC ← 证据 ← D0-D4 距离 → 匹配写法方向
03_projects
    ↓ 按 04b TC 关联度筛选证据
02_timeline
    ↓ 补充时间线和公司信息（辅助输入，不驱动身份）
ATS Evidence Output（v2.6.4 第三层）
    ↓ 基于前两层中间产物 + E01-E04 检查 → 生成简历
→ 生成简历
```

### Capability Mapping（v2.6 新增）

JD 中的每项关键要求，必须映射到 04b 的 TC：

| JD 要求 | 映射方式 | 结果 |
|------|------|------|
| [JD要求A] | → 找 04b 中匹配的 TC 编号 | TC001 → 在 03 中搜索 TC001 关联的案例作为证据 |
| [JD要求B] | → 找 04b 中匹配的 TC 编号 | TC002 → 03 中 TC002 关联的案例覆盖多个原始岗位 |

**不是**按 JD 关键词去 Timeline 中搜索岗位名匹配的经历，而是按 TC 编号去 03 的 TC 映射字段找证据。

### Step 9.0: Per-Experience Engine Loop（逐经历重构循环 v2.7.1）

对 Timeline 中的每条经历，不直接写入简历，而是依次执行以下循环。Reframing 在此循环中作为生成引擎而非事后检查。

```
对于每条经历：
  1. Capability Interpretation
     → 输出该经历的 角色解释 + 形成 TC + 关键证据
  2. JD Mapping
     → 输出 JD 要求 ← TC ← D距离 → 写法方向
  3. 基于 JD Mapping 的「写法方向」生成该段简历文本
     → Direct(D0-D1)：肯定语气
     → Adjacent(D2-D3)：可迁移语气
     → D4：跳过，不写入简历
  4. E01-E04 单段检查 → 通过则追加到简历 → 不通过则重写该段
```

只有全部经历生成完毕且通过 E01-E04 后，进入 Step 9.1 Resume QA Layer。

### Capability Interpretation（角色解释层 v2.6.4）

**每段工作经历在放入 ATS 简历前，必须生成一个中间结构化产物：**

```yaml
Capability Interpretation:
  原始岗位: [合同岗位名称]
  公司: [公司名]
  时间段: [YYYY.MM - YYYY.MM]
  角色解释: [该岗位在能力体系中承担的角色 — 来自 R03 Role Interpretation]
  形成能力:
    - TC001: [该 TC 在此经历中的具体体现]
    - TC002: [体现]
  关键证据: [03 中该经历的量化结果摘录]
```

**规则**：
- 角色解释**必须是角色标签**（取自 04b 该 TC 在**本赛道** `Position Constraint.推荐` 的既有措辞），**不得写成职责描述**（「负责 / 参与…」式句子）
- 形成能力必须能在 03 中找到对应 Evidence
- 此层作为 JD Mapping 的输入，不直接进入简历

### JD Mapping（JD 匹配映射层 v2.6.4）

**对每个 Capability Interpretation，映射到 JD 要求 + Evidence Distance：**

```yaml
JD Mapping:
  JD 要求: [JD 中的具体能力要求]
  对应 TC: [TC001 / TC002]
  证据距离: [D0 / D1 / D2 / D3 — 来自 Step 5.5 Evidence Distance Analysis]
  匹配写法方向:
    Direct(D0-D1): "已验证"
    Adjacent(D2-D3): "可迁移"
    Missing(D4): 不写入简历
  JD 措辞映射: [JD 原文关键词列表 — 用于 ATS 关键词密度]
```

**规则**：
- 每条 JD 要求至少映射一个 Capability Interpretation
- D0-D1 直接用肯定语气（"主导/负责"）；D2 从可迁移角度写（"在 [原始场景] 中承担的 [角色] 职责，形成了可迁移至 [JD场景] 的 [能力]"）；D3 简化为辅助证据；D4 不出现在简历中
- 此层输出作为 ATS Evidence Output 的生成指令

### ATS Evidence Output（ATS 证据输出层 v2.6.4）

基于 Capability Interpretation + JD Mapping 中间产物 + E01-E04 检查，生成 ATS 简历文本。

**生成顺序**：
1. 取 Capability Interpretation 的「角色解释」→ 作为工作内容的叙事视角
2. 取 JD Mapping 的「匹配写法方向」→ 决定语气（已验证/可迁移）
3. 取 JD Mapping 的「JD 措辞映射」→ 融入关键词密度
4. E01-E04 检查 → 通过后输出

### ATS Keyword Preservation（v2.6）

Capability Mapping 与 ATS Keyword Extraction 是并行层，不替代：

- **Step 3.5 Skill Weight** → 提取 JD 原始措辞 → 融入简历关键词密度（如 "[某关键词A]"、"[某关键词B]"、"[某关键词C]"）
- **Step 4.5a → 04b TC 映射** → 决定证据选取 + 经历叙事方向（如 "TC001 对应案例3"）
- 两者在简历中同时生效：TC 控制「选什么经历、怎么写」，JD 关键词控制「用什么词写」

### ATS Reframing（v2.6.2 新增）

**ATS Resume 的 Experience Reframing 与 Online Profile 是两种不同机制。**

| 维度 | Profile Reframing | ATS Reframing |
|------|------|------|
| 目标 | 建立职业身份（Identity Construction） | 证明岗位匹配（Evidence Optimization） |
| 输出 | 职业形象（Identity） | JD 证据（Evidence） |
| 核心问题 | 我是谁 | 为什么录用我 |
| 推理链 | Experience→Capability→Identity | Experience→Capability→JD |
| 可抽象程度 | 高 | 中 |
| 是否允许职业包装 | 可以（如 "跨组织协调推动者"） | 很少（必须有可追溯证据） |
| 是否允许职责升级 | 不允许 | 不允许 |
| 验证标准 | 市场定位是否成立 | 面试追问是否能回到原始事实 |

**ATS Reframing Pipeline**：

```
Experience（原始事实）
    ↓
Capability（能力抽象 — 来自 04b TC）
    ↓
JD Mapping（JD 要求 → 对应 TC → 对应证据）
    ↓
Evidence（JD 语言 + 可追溯事实）
```

注意：ATS 推理链不到 Identity 层。不生成「职业形象」，只生成「能力证据」。

（补充：`Step 4.5b` 仍会把 `07` Layer 2 Career Positioning 作为 **headline 的约束层** —— 它约束「不许写成什么」（否定集），而 headline 的正面措辞仍由能力证据产出。故本句与 Step 4.5b 不矛盾：**Identity 是约束，不是叙事驱动源**。）

#### Evidence Preservation Rules（E01-E04 v2.6.2）

##### Rule E01 — Traceability（可追溯性）

每一条 ATS 描述必须可追溯回 `02_timeline`、`03_projects`、`04_skill_graph`、`04b` 中的原始证据。

- 通过：面试追问「请具体讲讲」→ 可回到真实经历
- 不通过：追问后只能继续编 → FAIL

##### Rule E02 — Perspective Not Authority（视角可改，级别不可改）

Reframing 允许改变视角，不允许改变责任等级。

- 允许：[原始岗位 A] → [能力视角角色名]（实际干过）
- 不允许：[原始岗位 A] → [更高级别头衔]（级别变了）

##### Rule E03 — Capability Not Authority Upgrade（能力可升级，权限不可升级）

Reframing 允许能力抽象，不允许权限升级。

- 允许：[某操作] → [某管理能力]（能力抽象）
- 不允许：[参与讨论] → [决策负责人]（权限升级）

##### Rule E04 — Interviewer Traceability（面试追溯性）

所有 Reframing 后的描述必须能回答面试官追问：「请具体讲讲当时是怎么做的」。

- 追问能回到真实经历 → PASS
- 追问只能继续编 → FAIL

##### Rule E05 — Reframing Arbitration（层级仲裁顺序 v2.13.0）

当同一段经历在多个层级同时产出候选表达时，按**固定优先级**取用；高优先级层已给出表达时，低优先级层**不得覆盖**。

| 优先级 | 层 | 表达性质 | 举例 |
|:--:|---|---|---|
| 1（最高） | **事实层** | 岗位名 / 公司 / 时间段 | 原样保留，不可改写 |
| 2 | **角色解释层** | 角色级标签（白名单来源见 `R03`） | 该岗位在能力体系中的角色标签 |
| 3 | **职责动词层** | 职责动词升级 | 参与 → 建立 / 负责 → 主导 |
| 4（最低） | **能力抽象层** | 能力维度概括 | 交付节奏控制 / 组织协同 |

- **事实层永不参与竞争** —— 它不与其他层争，只作为**不可改写的边界**存在。
- **角色解释层可用时优先于职责动词层**；两层**不冲突**（可同现于一句：角色标签作主语 + 升级后的动词作谓语）。
- 低优先级层**不得反向覆盖**高优先级层；冲突时以高优先级为准。
- 各层均受 `E01`/`E04` 约束：任一层的表达都必须可追溯回原始证据。
- 若角色解释层**无合法来源**（见 `R03` 的 fail-safe）→ 该层**空缺**，由职责动词层承接，**不得**用能力抽象层冒充角色标签。

### Resume Identity Lock（v2.6）

```
简历身份锁定规则：
- 简历第一段「职业定位」= Step 4.5b 的职业身份核心名词（来自 07）
- 「求职意向」行 = JD 岗位名（不填 07 Positioning）
- Timeline 中的原始岗位名称仅作为「公司·岗位」行的事实信息
- 工作内容描述以 Capability Identity 关键词为主语
- 任何从 Timeline 自动推断「我是XX岗位」的行为 → 阻断
- 07 Layer 5 中列出的原始岗位不得出现在简历的身份表达层
```

### Step 9.1: Resume QA Layer（简历自检层 v2.7.1）

简历生成后、输出前，执行四项检查。任一不通过 → 重写对应段落。

#### QA-1: Identity Drift Check（身份漂移检查）

检查简历中是否存在与 Step 4.5b Identity Resolution 冲突的表达。
- Headline/第一段中是否出现 07 Layer 5 禁止表达 → 是则替换
- 工作经历中是否从 Timeline 自动推断身份 → 是则重写

#### QA-2: Capability Gap Check（能力缺失检查）

检查 JD 要求的 Top 3 关键能力是否在简历中有对应证据。
- 缺失 → 标记 `[缺证据]`，不编造

#### QA-3: D3 Over-Packaging Check（D3 过度包装检查）

检查 D3 级别的 Adjacent Match 在简历中的表达是否超过「可迁移」语气。
- 出现「主导/负责」等 Direct 语气 → 降级为「参与/协助」

#### QA-4: Identity Regression Check（身份回退检查）

检查简历尾部是否退化成原始岗位叙事。
- 最后一段工作经历如回到「负责 [某操作]」流水账 → 重写为能力视角

### Pack 策略（v2.6 更新）

按 Step 7 的策略决定生成哪套文件。详细产出合约见 `references/output_contracts.md`；**各产物文件的章节骨架模板见 `references/pack_templates/`（01-08 实体模板，含编号映射规则，见其中 README）**。生成时按 Pack 实际编号落盘——Boss Greeting 在 Pack A = `07`，Pack B = `08`，禁止写死 07。

**v2.12.0**：简历生成前，先读取对应 Track 文件的 `## Track Strategy` 段（`career-dna/10_career_tracks/{track}.md`），使用其中 **S1 Recommended Positioning / S2 Self-Intro Script / S3 Project Priority / S4 Story Mapping** 作为生成指令。（v2.12.0 起废除独立的 `{track}_strategy.md` 写法。）

**所有 Pack 中的简历生成，必须先执行 Step 4.5b Resume Identity Lock。简历中的「职业定位」段统一来自 07，不由 JD 或 Timeline 自动推导。**

### Pack A: Strong Fit — 投递包（Match ≥ 80）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | 完整 JD 分析 + Capability Translation |
| 2 | `02_resume_cn.md` | 中文 ATS 简历 |
| 3 | `03_resume_en.md` | 英文 ATS 简历 |
| 4 | `04_interview_pack.md` | 面试准备包 |
| 5 | `05_answer_cards.md` | 回答卡片库 |
| 6 | `06_upgrade_plan.md` | 竞争力升级计划 |

> **Pack A 附加产物**：`07_boss_greeting.md`（Boss 打招呼语，Step X 生成；版式见 `pack_templates/08_boss_greeting_template.md`，编号映射见其 README）。

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

> **Pack B 附加产物**：`08_boss_greeting.md`（Boss 打招呼语，Step X 生成；B 多一个 06_gap_analysis → greeting 顺位 08）。

### Pack C: Stretch Fit — 转岗包（Match 40-59）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | 完整 JD 分析 |
| 2 | `02_transition_resume_cn.md` | **转岗中文简历** — 突出 Adjacent Match 可迁移能力 |
| 3 | `03_transition_resume_en.md` | **转岗英文简历** |
| 4 | `04_transition_feasibility.md` | 转岗可行性评估（含 Capability Translation 能力迁移分析） |
| 5 | `05_gap_analysis.md` | 能力差距分析 |
| 6 | `06_learning_roadmap.md` | 学习路线图 |
| 7 | `07_interview_pack.md` | 面试准备包（+ 转岗高频问题） |

> **落盘命名规则（v2.18.0 定论）**：产物**一律数字前缀**，编号 = **本 Pack 清单顺位**；`XX_*` **只是模板文件名**（模板跨 Pack 复用，故它自身编号不固定）。Pack D 同此规则。
> 依据：Pack A/B 存量实例一律数字前缀（`02_resume_cn` / `06_gap_analysis` / `08_boss_greeting`…），且 `XX_*` 与数字混用会在 Pack C/D 产生两套候选名。

### Pack D: Weak Fit — 学习路线包（Match < 40）

| # | 文件 | 用途 |
|---|------|------|
| 1 | `01_jd_match_report.md` | JD 分析 |
| 2 | `02_gap_analysis.md` | 能力差距分析 |
| 3 | `03_transition_feasibility.md` | 转岗可行性评估 |
| 4 | `04_learning_roadmap.md` | 学习路线图 |

> Pack D 不生成简历和面试包，避免硬包装。

### Portfolio Selection（作品集推荐 v2.1）

在生成 Interview Pack 之前，从 `12_portfolio_candidates.md` 中推荐与本 JD 最匹配的 Ready 项目。

#### 匹配规则

1. 取 Ready 项目（Readiness ≥ 70%）
2. 与 Part 4 Evidence Matrix 的能力条目做交集比对
3. 取与 Primary Evidence 同项目且 Readiness 最高的前 3 个

#### 输出

写入 `01_jd_match_report.md` Part 8 新增 Portfolio Selection 表。

| 优先级 | 推荐项目 | Readiness | 匹配理由 | 展示方式 |
|:--:|------|:--:|------|------|
| Top 1 | [项目A] | 91% | 与 JD 核心能力直接对应 | 面试开场深度案例 |
| Top 2 | [项目B] | 86% | 补强 JD 次要能力 | 聊到相关话题时引出 |
| Backup | [项目C] | 71% | 展示交叉能力 | 面试尾声补充 |

---

## Step 9.5: Delivery Finalization（投递定稿 v2.8）

### 目标

将 Step 9 生成的 working 版简历（含推理标注）转化为**可直接投递的定稿包**：净化 → 审核 → 导出 Word/PDF。解决"md 简历含 `<!-- -->` 注释、TC/D 标注不能直接投递"的最后一公里问题。

**v2.8 范围**：仅中文版（`02_resume_cn.md`）。英文版（`03_resume_en.md`）待中文版验证后扩展——管道零改动，仅换输入文件 + 英文模板 + 字体栈。

### 触发（opt-in）

Step 9 简历生成后，用户说"转投递版 / 导出投递 / 我要投了"时进入。不自动执行。

### 产物结构（新增 deliverables/ 子目录）

```
resume-outputs/{date}-{company}-{role}/
├── 02_resume_cn.md                    # working 版（保留推理标注，供追踪迭代）
└── deliverables/
    ├── 02_resume_cn_final.md          # 净化后 md（供用户审核）
    ├── 02_resume_cn_final.docx        # 定稿 Word
    ├── 02_resume_cn_final.pdf         # 定稿 PDF
    ├── cover_letter_final.docx/.pdf   # 可选附件（求职信，Pack A/B）
    └── portfolio_final.pdf            # 可选附件（作品集，Pack A）
```

**working 与 final 物理隔离**：追踪用 working 版，投递用 deliverables/。**skill 只读 .md 文件，永不读取 .docx/.pdf 二进制**（格式转换不经过 LLM，token 成本 ≈ 0）。

### 流程（5 步）

| 步骤 | 操作 | 执行者 |
|------|------|--------|
| 1. 净化 | L1 剥离 `<!-- -->` 注释块；L2 剥离 D0-D3 标注行、TC 编号、版本号注释；收集 `[待补充]` 单独列出 | LLM |
| 2. 审核 | 用户按 Delivery Checklist 逐项核对 final.md | 用户 |
| 3. 修改 | 用户改 final.md；此后 final.md 为**定稿事实源**（单一事实源：小改直接改 final.md 再导出，大幅迭代回 working 版重走） | 用户 |
| 4. 导出 | 运行 `scripts/export_resume.py` 生成 docx + pdf | 脚本（无 LLM） |
| 5. 目检定稿 | 用户打开 docx/pdf 确认分页/字体/无乱码 | 用户 |

### 净化规则（Strip Rules）

| 层 | 规则 | 校验 |
|----|------|------|
| L1 结构剥离 | 删除所有 `<!-- -->` 注释块 | grep 无 `<!--` |
| L2 语义剥离 | 删 D0-D3 标注、TC 编号、版本注释；`[待补充]` → 提示用户先补或删除 | grep 无 `TC\d+`、无 `D[0-3]`、无 `[待补充]` |

**铁律：净化不改内容，只剥离标注**（不编造、不美化，与 Evidence Driven 一致）。PII 反转：工作版用 `[XX]` 脱敏，投递版由用户在审核时填入真实值。

### final.md 结构约定（v2.8.1 渲染依赖）

final.md 顶部必须有 header 区块（`>` 引用行，供姓名/意向/2×2 信息渲染）：

```markdown
# [姓名]

> 求职意向：[目标岗位] ｜ [期望城市]
> 电话：[电话] ｜ 邮箱：[邮箱]
> 城市：[城市] ｜ 年限：[工作年限]

## 职业定位
...
```

- 第 1 行 `# ` = 姓名；3 行 `> ` = 意向/信息（`｜` 分隔两栏，标签用 `：` 分隔）
- 其余 `## ` 节自动进入"节"列表；`### ` 行 = 条目 meta（蓝色加粗）；`- ` bullet 归入当前条目（有 meta 时）或当前节段落
- `**加粗**` 在 docx/pdf 渲染为加粗、HTML 渲染为 `<b>`

### Delivery Checklist（投递前核对清单）

- [ ] PII 真实值已填（[XX] → 真实公司/姓名/电话/邮箱）
- [ ] 无内部推理字段（注释 / TC / D 标注 / 版本号）
- [ ] 数字与 Career DNA 一致（量化结果未漂移）
- [ ] 职业定位仍来自 07（未漂移）
- [ ] 长度 1-2 页
- [ ] 格式：日期格式统一、无乱码

### 导出引擎（scripts/export_resume.py · v2.8.1 HTML 模板驱动）

**架构（Template-as-Spec）**：HTML 模板是「设计源」——用户改模板 CSS/结构 = 改设计，渲染脚本零改动。渲染管线：

```
final.md（净化定稿）
  → build_data() 结构化（姓名/意向/2×2信息/节/条目）
  → mini_template 渲染 resume_template.html（v1 抽象模板）→ final.html（v2 完整版，可预览）
  → HTML → PDF（Platypus，样式从模板 CSS 变量提取）
  → HTML → DOCX（最简转换，效果可接受部分损失）
```

```bash
python scripts/export_resume.py \
  --input  deliverables/02_resume_cn_final.md \
  --format all \
  --photo  证件照.jpg \
  [--template assets/templates/resume-outputs/resume_template.html] \
  [--theme blue]          # 可选：覆盖模板 CSS 变量（Track 联动）
```

- **产物**：`deliverables/02_resume_cn_final.html`（v2 完整版：样式+内容）+ `.pdf`（主，保真）+ `.docx`（辅，最简）
- **模板分层**：v1 = `resume_template.html`（占位符 + CSS 变量，用户编辑设计）；v2 = 渲染后的完整版（预览/核对）
- **占位符语法**（`scripts/mini_template.py`，零依赖，支持嵌套 each）：`{{姓名}}` `{{意向}}` `{{#each 信息}}` `{{#each 节}}`（含 `{{标题}}` `{{段落}}` `{{条目}}` `{{meta}}` `{{行}}`）
- **样式控制**：模板 `:root` CSS 变量（--accent/--block-bg/--font/--title-size/--line-spacing/页边距/**--body-indent/--bullet-indent/--heading-space-before/--heading-space-after/--entry-space** 等）——用户改这些 = 改设计；`--theme` 可覆盖配色（Track 联动）
- **样式修改走模板（v2.8.1 样式变量桥）**：所有布局数值（缩进/间距）均由模板 :root 变量驱动，**改模板即可，勿改 py**。例如：缩进改大 → `--body-indent: 56px`；行距 → `--line-spacing: 1.8`。改完跑 `--format all` 三端生效
- **背景系统（v2.8.2）**：页面整体背景 + Header 背景均可用模板变量配置，PDF 由 onPage canvas 绘制、HTML 端 CSS/SVG 同步。页面背景：`--page-bg-type: none|color|image` + `--page-bg-value`（色值或图片路径）+ `--page-bg-opacity`（水印）；Header 背景：`--header-bg-type: color|image|shape` + `--header-bg-value`；形状组合：`--header-shape: rounded|square|wave|slant`（主形状）+ `,block|dots|stripe`（装饰层，逗号分隔 ≤3）；形状参数：`--shape-wave-amplitude/segments/line`、`--shape-slant-angle`、`--deco-block/dots/stripe-*`。背景图资产放 `assets/backgrounds/`
- **结构类约定**（引擎支持，勿改名）：`.header` `.header-left` `.photo` `.name` `.intent` `.contact` `.section` `.section-title` `.entry` `.entry-meta` `ul` `li` `p`（`.shape-layer` 为背景装饰层，引擎自动跳过）
- **docx 最简转换取舍**：保留标题/节/段落/bullet/加粗/颜色/照片；损失圆角背景块/同行横线/形状背景等精细样式（PDF 主保真，docx 可损；背景系统仅 PDF/HTML 生效）
- **二期规划（暂缓）**：`parse_docx_template.py`（用户任意 docx 模板 → HTML v1 自动解析）。当前 v1 模板已定型 + 变量桥覆盖多数样式调整，二期按需再做（换新模板 / 分发后新用户上手时），推荐半自动版（提取 docx 样式规格 → 生成 v1 骨架 + 占位符，用户微调）而非全自动语义识别

### 附件（按 Fit 分层，同走净化）

| Fit | 附件 |
|-----|------|
| Strong（Pack A） | 求职信（07_boss_greeting → cover_letter_final）+ 作品集（XX_portfolio → portfolio_final） |
| Moderate（Pack B） | 求职信（08_boss_greeting → cover_letter_final） |
| Stretch/Weak（Pack C/D） | 可选 |

---

## Step X: Boss Greeting Generation（Boss 打招呼语生成 v1.6.1）

### 目标

将 v1.5.6 最终收敛结果压缩为一条可诱导 HR 回复的首条消息。不重新计算分数。

### 输入字段（仅读取 v1.5.6 收敛值）

| 输入 | 来源 |
|------|------|
| Match Score | `01_jd_match_report.md` 3.1 Match Summary |
| Decision Score | `01_jd_match_report.md` Part 7 Decision Score |
| Greeting Objective + Primary Hook + Safe Evidence + Curiosity Bait | `01_jd_match_report.md` **8.7 Boss Greeting Input Pack** |
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

`resume-outputs/{YYYYMMDD}-{company}-{role}/07_boss_greeting.md`（**Pack A**，A 无 06_gap → greeting 顺位 07）
`resume-outputs/{YYYYMMDD}-{company}-{role}/08_boss_greeting.md`（**Pack B**，B 有 06_gap + 07_upgrade → greeting 顺位 08）

> 编号映射规则见 `references/pack_templates/README.md`。版式骨架见 `references/pack_templates/08_boss_greeting_template.md`。禁止按文件内容逆推编号（upgrade/gap/greeting 的编号由 Pack 结构决定）。

---

## Step 10: Knowledge Update（知识更新）

> **Phase 归属（v2.17.0）**：**10.A / 10.B / 10.C → P1** —— 市场情报与「投不投」无关，**看过就该沉淀**（且新赛道发现依赖观察计数，挡在门后就永不积累）；
> **10.D → P2** —— 那是「**打算投**」的登记，不是「分析过」的登记（与本节既有纪律同源：Mode D 不写 `Applied`）。

### A. 更新 knowledge/role_snapshots/{role_name}.md（v1.4.1 增强 · **P1**）

> **Track 字段契约（v2.14.0）**：`Track（职业赛道）` 为**受控取值** —— 只允许填 `10_career_tracks/` 下的赛道文件名（**不含 `.md`**，如 `rd_pm`）或 `none`；**所有解释一律写 `Track Note（赛道说明）`**（子域限定 / 为何 none / 交叉参考）。**禁止散文、双语括注、斜杠并列**（此前 13 个实例写成 13 条不同的散文，导致人/脚本都归不了组）—— 由 P2 `role-snapshot-schema` 校验。首次建档与后续更新同样适用。

1. 更新 **Common Hiring Intent**：基于本次 Hiring Intent Analysis 合并更新（典型招聘意图）
2. 更新 **Talent Persona**：基于本次 Talent Persona Inference 合并更新（典型画像特征）
3. 更新 **Typical Evidence**：基于本次 Evidence Expectation（含 Ownership/Scope/Impact）合并更新
4. 更新 **Career Background Distribution**：本 Role 常见职业背景分布
5. 更新 **Skill Weight Baseline**（v1.4.1 新增）：基于多次 Skill Weight Analysis 累积各能力的平均权重
6. 更新 **Hiring Intent Trends / Talent Persona Trends / Evidence Trends**（≥3 次观察后）
7. **回写索引 README**（v2.14.0 新增；**v2.17.0 加 `Observed Companies` 列**）：在 `knowledge/role_snapshots/README.md` 的「索引」表登记 / 更新本 Role 一行 ——
   `Role | Track（受控取值） | Observed JD Count | Observed Companies（已观察公司数） | 文件 | 段完整性`，
   并同步「按赛道归组」「缺段待刷新」「新赛道候选」三节。
   - **`Observed Companies` 列 = 本 Role 快照 `Observed Companies` 字段解析出的「不同公司数」**（解析规则见 §Step 10 C 第 7 条），
     **不是 `Observed JD Count`** —— 二者在「同一公司同批次多份 JD」时会显著背离（实测某岗 4 份 JD / 1 家公司）。
     该列是「新赛道发现」的唯一输入，**必须每次回写**。
   - **README 不存在时按本节表头初始化**（表头即结构契约；`knowledge/` 不属 Career DNA SSOT，无需四件套登记），
     并补齐「按赛道归组 / 缺段待刷新 / 新赛道候选 / 别名冲突 / 已处置」各节骨架。
   - 首次建档同样必须登记。**新字段 / 新文件不加回写钩子 = 第一天即脏**（v2.12.0 `01_application_index` 缺 Pack 列
     且 Mode D 从不回写 → 实测 8 个投递包仅登记 2 行的教训）。

### B. 更新 knowledge/skill_snapshots/{domain_name}.md（v1.4.1 增强 · **P1**）

每个 Skill 更新：

1. 更新 **Aliases**（v1.4.1 新增）：如 JD 中出现该 Skill 的新表述，追加到 Aliases 列表（去重）
2. 更新 **Typical Evidence**：含 Ownership/Scope/Impact 三维度的典型证据形式
3. 更新 **Business Meaning**：该 Skill 在业务中的价值解释
4. 更新 **Related Hiring Intent**：该 Skill 关联哪类招聘意图
5. 更新 **Typical Results**：该 Skill 的典型成果量化方式
6. 更新 **Typical Ownership**：基于多次 Evidence Expectation 的 Expected Ownership 均值

### C. 更新 career-dna/10_career_tracks/{track}.md（v1.4.2 增强 · **P1**）

1. 重新计算 **Track Confidence Breakdown**：Evidence Strength / Role Snapshot Validation / Market Demand 三分量
2. 更新 **Validation Status**：基于 JD 频率和覆盖比例判定 Validated / Emerging / Uncertain
3. 更新 **Market Validation**：本次 JD 是否验证了该 Track 的市场需求
4. 更新 **Matched Hiring Intent**：哪些 Hiring Intent 被本次 JD 覆盖
5. 更新 **Evidence Strength**：基于 Evidence Expectation 评估证据强度（Strong / Moderate / Weak）
6. 更新 **Market Demand Signals / Recent JD Coverage / Market Signal**
7. **新赛道发现（New Track Discovery v2.17.0）** —— 本步的**常驻分支**：`Track: none` 的快照**无 track 可更新**，
   发现链路此前正是在此处断掉（「新赛道」只能靠人读 README 时才被想到）。**每次观察后必须执行**：

   - **候选池** = 所有 `Track（职业赛道）` 取值为 `none` 的 Role Snapshot（用户侧 `knowledge/role_snapshots/`，
     索引见其 README 的「按赛道归组 · `none` 组」与「新赛道候选」表）。
   - **判据** = **同一快照内「已观察的不同公司数」≥ 3**。**计量单位是公司数，不是 JD 数** ——
     同一公司在同一批次放出 N 份同类 JD 只算 **1** 个市场信号
     （实测某岗 4 份 JD 全部来自同一公司同一批次；若按 JD 数计该岗早已「达标」，而它实际只有 1 家雇主）。
   - **计法** = 解析该快照的 `Observed Companies` 字段（受控格式见下）—— **剥离 `（）` 括注后**按 ` · ` / `+` / `、` 切分；
     `unknown`（JD 未标注公司）**不计入**；**括注内提及的关联方不计入**（母公司 / 客户不算独立观察）。
   - **动作**：
     - **未达标** → 在 README「新赛道候选」表更新本 Role 的已观察公司数与「距阈值」列（`3 - N`）；
     - **达标** → 在 README「新赛道候选」表把该行状态改为 `⚠️ 建议评估`，并**在会话中主动提示用户**：
       「`{role}` 已跨 3 家公司观察，是否评估新建赛道？」——**并给出观察依据**（哪几家、各多少份 JD）。
   - **边界（硬）**：**建不建新赛道由人拍板**。本步**只登记候选与提示**，**禁止**自动创建 / 修改
     赛道文件（新建赛道属 career-dna 写入，须走 Mode A/B 契约；赛道置信度是用户侧判断，不是脚本结论）。
   - **`none` 不是「废弃」**：它是**未命中已登记赛道**，本身就是发现信号（实测 5/12 快照为 `none`）。
   - **`Observed Companies` 受控格式**：字段值 = **公司名**（多家用 ` · ` 或 `+` 分隔），
     每家的说明写在紧跟其后的 `（）` 括注内（证码 / 城市 / 隶属 / 规模）；**括注内容不计入公司计数**；
     JD 未标注公司 → 写受控值 `unknown`（**不计入**），推断理由写括注。
     **禁止**把说明写成 ` · ` 分隔的平铺串（会被解析成另一家公司 → 误触发新赛道发现）。
     由 P2 `role-snapshot-schema` 第 ④ 项校验。

### D. 回写投递索引（v2.12.0 新增 · **P2**）

在 `application-tracker/01_application_index.md` 登记 / 更新本次投递一行 ——

1. 填写 Company / Industry / Role / City / Salary / Source / **Pack**（相对路径 `../resume-outputs/{YYYYMMDD}-{company}-{role}/`）
2. Status = `Planned`，Last Update = 当日
3. 已存在同 Company + Role 行 → **原地更新**，不重复添加
4. `Status` 由 **Mode E** 在真实投递后流转为 `Applied` 及以后；**Mode D 不写 `Applied`**
   （否则「已备包」与「已投递」混淆，并虚高 Mode C Step 6 的市场验证率统计）

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
