<!-- ============================================================
 模板：01 JD Match Report（JD 匹配报告）
 适用：Pack A/B/C/D → 一律落盘为 01_jd_match_report.md
 归纳自：[某真实投递包A]（8-Part 完整版）+ [某真实投递包B] / [某真实投递包C] 交叉验证
 生成时机：Mode D Step 1-7 + Step 8.0-8.7 逐步填充后汇总
 数据来源：JD 原文 / Step 1-4 拆解 / Career DNA 各文件 / Role Snapshot / Track 文件
 结构基线：v1.5.4 8-Part（Part 1-8）→ **v2.18.0 起 9-Part（Part 1-9）**，8.0-8.7 为推荐策略子节；附录 A/B（v2.15.0 新增，与 Part 编号正交）
 附录规则：见 references/mode_d_job_application.md Step 2.9（生成规则）+ 本文件附录区内嵌注释（形态约束）
============================================================ -->

# JD Match Report: {{公司名}} — {{岗位名}}

<!-- 头部注释：生成版本日期 / Track / 双 JD 观察编号（如适用） -->
<!-- 例：<!-- v2.6.4 · [YYYY-MM-DD] · Track: 游戏技术 PM × PMO → 美术管线子域 · Observed=2 --> -->

---

## Part 1: JD Original（JD 原文存档）

<!-- 规则：逐字保存 JD（含薪资/学历/经验/认证/加分项），供后续 Part 引用追溯。缺字段标 [JD 未提供]。 -->

{{JD 原文全文，或结构化摘要：薪资 / 学历 / 经验 / 岗位职责 N 条 / 任职要求 N 条 / 加分项 / 公司线索}}

---

## Part 2: Role Analysis（角色分析）

- **Role（岗位）**: {{标准化 Role 名称 + 一句话岗位本质判定（如 "PMO 型流程建设岗 / 制作线嵌岗"）}}
- **Company（公司）**: {{公司名 + 规模/业务线索}}
- **Date（日期）**: {{YYYY-MM-DD}}
- **Track（赛道）**: {{关联 Track 文件路径/名称 · 子域定位}}

### 2.1 Core Responsibilities（核心职能）

{{职责 1-N 逐条编号摘录，随后附职责重排}}

- **Ownership（责任级别）**: {{Lead / Partial Lead / Support + 依据（用词如"协助/跟进"→Partial Lead）}}
- **Scope（范围）**: {{单项目 / 多项目 / 平台型 + 依据}}
- **Reporting Structure Hint（汇报暗示）**: {{向谁汇报 / 横向服务对象}}

### 2.2 Hiring Intent（招聘意图）

- **Explicit（显性）**: {{JD 明文要求列表}}
- **Implicit（隐性）**: {{从上下文 + Role Snapshot Trend + 行业常识推理}}
- **Business Context（业务背景）**: {{公司阶段（扩张/替补/新业务）推理}}
  <!-- 本行只写**结论**；本次**论证**（查到了什么 / 由此推出什么）→ 本报告**附录 B**。
       调研方法（查什么 / 从哪查 / 怎么把情报变成反问）见 13_interview_narrative_strategy.md Part 10（反向尽调）。
       不要在此重复通用方法；附录 B 也不重述本行结论（单向指针：Part 2.2 = claim → 附录 B = evidence）。 -->
- **Pain Point（痛点推断）**: {{从 JD 高频强调或特殊要求推断团队缺什么}}
- **Hiring Reason**: {{新设岗位 / 替补离职 / 业务扩张 / 项目需求}}

### 2.3 Skill Weight Analysis（能力权重分析）

| 能力 | 权重 | 来源 | 说明 |
|------|:--:|------|------|
| {{能力A}} | {{30%}} | {{职责2+3}} | {{Critical — 岗位本体 / High / Medium}} |
| {{能力B}} | {{25%}} | {{职责}} | {{权重依据}} |

<!-- 规则：权重三维度 = JD 措辞优先级（必须>优先>熟悉；首段>中段>尾段）+ Role Snapshot Skill Frequency（≥80%→3pt 等）+ Critical Evidence 对应 +1pt。 -->
<!-- 多 JD 同品类分析时：附"共同权重印证"引用块。 -->

> {{多 JD 共同信号（如适用）}}

### 2.4 Ideal Candidate（理想候选人画像）

> {{一句话人才画像（自然语言，非关键词列表）}}

- **Career Background（职业背景）**: {{典型行业/岗位/年限}}
- **Typical Experience（典型经历）**: {{典型项目与角色}}
- **Preferred Traits（偏好特质）**: {{特质列表}}

---

## Part 3: DNA Match Analysis（DNA 匹配分析）

### 3.1 Match Summary（匹配概要）

| 维度 | 值 |
|------|-----|
| **Overall Match Score（综合匹配度）** | **{{NN}}%** |
| **Match Confidence（匹配置信度）** | **{{NN}}%** |
| **Application Strategy（求职策略）** | **{{Strong/Moderate/Stretch/Weak}} Fit（{{档位中文}}）** |
| **Package（生成包）** | **Pack {{A/B/C/D}}** |

### 3.2 Match Score Breakdown（匹配得分分解）

| 评分维度 | 权重 | 得分 | 加权 | 说明 |
|----------|------|------|------|------|
| Hard Requirement Match | 40% | {{N}} | {{N}} | {{逐项扣分来源摘要}} |
| Experience Match | 30% | {{N}} | {{N}} | {{行业/场景/角色重叠度}} |
| Capability Match | 20% | {{N}} | {{N}} | {{D0-D4 分布摘要}} |
| Industry Match | 10% | {{N}} | {{N}} | {{Role Snapshot Industries 比对}} |
| **Overall** | **100%** | — | **{{N}}** | {{取整与实质下调理由}} |

#### Hard Requirement Detail（硬性要求明细）

| JD 要求 | 用户状态 | Score | 扣分来源 |
|---------|----------|-------|----------|
| {{要求A（学历/年限/证书/语言等逐项）}} | {{用户状态}} | {{0-100}} | {{扣分理由（头衔不匹配-20~30 / 年限按比例 / 证书缺-10~20 / 完全缺失=0）}} |

### 3.3 Match Confidence Breakdown（匹配置信度分解）

| 置信度因素 | 权重 | 原始分 | 扣分 | 最终分 | 说明 |
|-----------|------|--------|------|--------|------|
| Evidence Count | 30% | {{N}} | {{0}} | {{N}} | {{可用证据/总能力}} |
| Evidence Quality | 30% | {{N}} | {{0}} | {{N}} | {{High/Medium/Low 分布}} |
| Direct Relevance | 25% | {{N}} | {{0}} | {{N}} | {{D0+D1 占比}} |
| Evidence Stability | 15% | {{N}} | {{0}} | {{N}} | {{核心能力跨项目频次}} |
| **Match Confidence** | **100%** | — | — | **{{N}}** | |

### 3.4 Track Validation（赛道验证）

| 验证链路 | 得分 | 说明 |
|----------|------|------|
| Career DNA → {{Track 名}} | {{N}} | {{Track Confidence}} |
| {{Track 名}} → {{岗位}} JD | {{N}} | {{Track Core Skills 覆盖比例}} |
| **Triangulated Validation** | **{{Strong/Moderate/Weak}}** | {{两段均≥70→Strong 等}} |

---

## Part 4: Evidence Distance（证据距离）

### 4.1 Evidence Expectation（证据期望）

<!-- 规则：v1.5.2 起此节为内部推理依据，不强制写入报告。若写：Critical Evidence 列表 + 期望 Ownership/Scope/Impact。 -->

### 4.2 Evidence Matrix（证据分析矩阵）

| JD 能力 | DNA 证据 | Distance | Strength | 说明 |
|---------|----------|:--:|:--:|------|
| {{JD 能力（按权重降序）}} | {{03/05 中的证据 + 量化摘录}} | **D{{0-4}}** | {{1-5}} | {{D0 同职责 / D1 职能等同 / D2 可迁移 / D3 附推理依据 / D4 无证据}} |

<!-- 规则：D3 必须附 1-2 句推理依据否则强制降 D4；D4 = 无证据/推测性，禁建立 Distance。 -->

### 4.3 Evidence Coverage（覆盖率）

{{D0 数量×100 + D1×85 + D2×65 + D3×40 + D4×0 = 总分 / 子证据数 = NN%}}（附算式）

---

## Part 5: Role Authenticity（角色真实性）

| JD Role | 用户最高相关头衔 | 等级 | Score | 判定依据 |
|---------|-------------|:--:|-------|----------|
| {{JD Role}} | {{07/02 中最高相关头衔}} | **Level {{A/B/C/D}}** | {{N}} | {{同岗位 A / 同域不同岗 B / 跨域可迁移 C / 跨赛道 D + Track Confidence ±10 微调}} |

### Hire Probability Adjustment（录用概率修正）

- **Hire Probability（录用概率）**: ≈ {{Match × Authenticity/100}}%
- **修正依据**: {{Authenticity Level + D0/D1 占比调整说明}}

---

## Part 6: Recruiter Risk Funnel（招聘漏斗风险）

| 阶段 | 风险 | 判定依据 |
|------|:--:|----------|
| ATS | {{High/Med/Low}} | {{Hard Requirement Coverage <70%→High}} |
| HR | {{High/Med/Low}} | {{Authenticity C/D→High, B→Medium}} |
| Hiring Manager | {{High/Med/Low}} | {{D2+D3 占比 >40%→High}} |
| Offer Committee | {{High/Med/Low}} | {{P0 Gap ≥2→High}} |

### Stage-Specific Countermeasures（阶段对策）

| 阶段 | 对策 |
|------|------|
| {{ATS}} | {{措辞/关键词策略}} |
| {{HR}} | {{首条消息/话术策略}} |
| {{Hiring Manager}} | {{叙事/证据策略}} |
| {{Offer Committee}} | {{Gap 补强/对冲}} |

> **分工（不得与下游重复写）**：
> - 本 Part = **风险视角** —— 我会因为什么被刷、怎么对冲。
> - 阶段「打法」（谁面我 / 考什么 / 必带材料 / 禁忌 / 收尾动作）见 `13_interview_narrative_strategy.md` Part 7。
> - 本轮实际轮次与用人见 `resume-outputs/{JD}/04_interview_pack.md` §7。

---

## Part 7: Decision Score（决策评分）

<!-- 规则唯一定义源：mode_d_job_application.md §Step 5.8。本处只锁版式，不重复规则。 -->

### 7.1 Formula & Factors（公式与因子）

**Decision Score = 0.7 × Match + 0.3 × HireProbability = Match × (0.7 + 0.3 × Role Authenticity / 100)**

| 因子 | 类型 | 权重 | 判定来源 | 本岗取值 |
|------|:--:|:--:|------|:--:|
| **Match Score（匹配度）** | Core | 70% | → Part 3.2 Overall Match | {{NN}} |
| **Role Authenticity（角色真实性）** | Multiplier | 30% | → Part 5 | {{NN}}%（Level {{A/B/C/D}}） |
| **Hire Probability（录用概率）** | 派生量 | — | = Match × Auth / 100 | {{NN}} |

> **v2.16.0 起废除 Additive 因子**（原 Location 10% / Language 10% / Industry 5%）。
> 废除原因：Language / Industry 与 Match **双计**（`Hard Requirement` 已含语言、`Industry Match` 已含行业）；
> Location / Language **零方差**（常数项使实际门槛由 60 降至 40）。三者信息各有归属 → 见 §7.3，**不折回总分**。

### 7.2 Calculation Breakdown（计算拆解 —— 必须展示）

| 项 | 计算方式 | 值 |
|---|---|:--:|
| Match 基础分 | Part 3.2 | {{NN}} |
| Role Authenticity | Part 5 | {{NN}}%（Level {{X}}） |
| 折扣系数 | 0.7 + 0.3 × Auth / 100 | ×{{0.NNN}} |
| **Decision Score** | Match × 折扣系数 | **{{N}}** |

**档位判定**：{{≥80 强烈建议投 / 60-79 建议投 / <60 谨慎}}

### 7.3 Situational Factors（情境因子 —— 展示项，不参与判定）

<!-- 硬约束：Label 非 Score。不得折回总分、不得参与档位判定、不设分值位。仅作同分 tie-breaker 与投递成本提示。 -->

| 因子 | 状态 | 说明 |
|------|------|------|
| **Location（地点）** | {{同城 ✓ / 异地}} | {{异地：需考虑搬迁 / 通勤成本}} |
| **Language（语言）** | {{JD 要求 + 已达标 / 涉外增量优势 / 不相关}} | {{要求部分已在 Part 3.2 `Hard Requirement` 计分}} |
| **Industry（行业）** | {{同行 / 相邻 / 无关}} | {{已在 Part 3.2 `Industry Match` 计分}} |

---

## Part 8: Recommended Strategy（推荐策略）

### 8.0 Usable Evidence Summary（可用证据汇总）

| 优先级 | 证据 | Distance | Strength | 来源 |
|------|------|:--:|:--:|------|
| **Top 1** | {{证据名 + 量化}} | D{{N}} | {{N}} | {{项目/公司}} |
| **Top 2** | {{证据名 + 量化}} | D{{N}} | {{N}} | {{来源}} |
| **Top 3** | {{证据名 + 量化}} | D{{N}} | {{N}} | {{来源}} |
| **Secondary** | {{辅证据}} | D{{N}} | {{N}} | {{来源}} |

### 8.1 Greeting Recommendation Summary（打招呼策略摘要）

- **Recommended Type**: Type {{A/B/C/D}} — {{版本名}}
- **Alternative Type**: Type {{A/B/C/D}} — {{版本名}}
- **Suggested Tone**: {{一句话语气描述}}

<!-- 规则：Type 选择见 mode_d Step 8.8 条件表（Decision + HR Risk + Primary Distance）。 -->

### 8.2 Gap Priority Matrix（缺口优先级矩阵）

| 缺口 | Impact | Cost | Priority | 建议行动 |
|------|:---:|:---:|:---:|------|
| {{缺口A}} | {{High/Med/Low}} | {{High/Med/Low}} | **P{{0/1/2}}** | {{行动（指向 06/07 文件）}} |

### 8.3 Narrative Mapping（叙事映射）

**我的核心叙事**（07 Layer 3）：{{核心叙事原文}}

**JD 适配角度**：{{JD 需要什么角度}}

**叙事主线**：{{07 核心叙事 + JD 适配的一句话/小段完整叙事}}

<!-- 规则：由 Step 8.12 Narrative Alignment 输出。 -->

### 8.4 Key Projects & Stories（推荐项目与故事）

| # | 项目/故事 | 匹配理由 | TC |
|---|----------|----------|:--:|
| 1 | {{项目/故事名}} | {{匹配的 JD 能力 + D 距离 + 用途（开场主证据等）}} | {{TC00X}} |

<!-- 规则：Tier A Stories 按 Narrative Strength 总分排序（非 TC 优先级）。 -->

### 8.5 Application Advice（投递建议）

- **Hire Probability（录用概率）**: ≈ {{NN}}%
- **是否建议投递**: {{✅/⚠️/❌}} {{建议 + 一句话理由}}
- **策略建议**: {{求职意向写法 / 主打身份 / 不主动提的短板}}
- **重点关注**: {{面试最大试探点 → 指向 05_answer_cards Q 编号}}

### 8.6 Portfolio Selection（作品集推荐）

| 优先级 | 推荐项目 | Readiness | 匹配理由 | 展示方式 |
|:--:|------|:--:|------|------|
| Top 1 | {{项目名}} | {{NN}}% | {{与核心能力直接对应}} | {{面试开场深度案例}} |

<!-- 规则：从 12_portfolio_candidates.md 取 Ready（≥70%）项目，与 Part 4 能力交集，取前 3。 -->

### 8.7 Boss Greeting Input Pack（打招呼素材包）

- **Greeting Objective**: Type {{A/B/C/D}} — {{名称}}
- **Primary Hook**: {{Top1 证据压缩成 1 句}}
- **Supporting Evidence**: {{Top2/Secondary 压缩成 1 句}}
- **Safe Evidence**: {{Type C 用安全区证据}}
- **Curiosity Bait**: {{Type D 用 D2/D3 高 Strength 证据制造意外感}}
- **Avoid**: {{明确不出现的内容}}
- **Recommended Platform Priority**: {{Boss 直聘 > 猎聘 > 邮件}}

---

## Part 9: Outreach Package（外联沟通包）

<!--
桥梁层：Part 4 分析证据 → Part 9 路由证据 → 07_boss_greeting 消费证据（Greeting 不再自己选证据）。
规则定义源 = references/mode_d_job_application.md 的 Step 8.5（Evidence Routing）/ Step 8.6（Platform Strategy）；
本 Part 是**版式唯一定义源**（v2.18.0 起，原 01 遗留副本的 v1.6.2 完整版已收敛至此）。
-->

### 9.1 Evidence Routing（证据路由）

- **候选池**: Part 4.2 Evidence Matrix 中 **Strength ≥ 4** 的全部证据
- **Primary（主证据）**: {{Rule 1+2 最高分证据，通常 D0/D1 —— Greeting 核心卖点 + 简历主叙事}}
- **Secondary（辅证据）**: {{Rule 1+2 次高分证据，D1/D2 —— 补强匹配度，猎聘 / 邮件用}}
- **Curiosity（好奇心证据）**: {{Rule 3 注入，D2/D3 且 Strength≥4 —— Boss Type D / LinkedIn 开场用}}

| 优先级 | 规则 | 逻辑 |
|:--:|------|------|
| **Rule 1** | Distance Priority（距离优先） | D0/D1 永远排最前，D2 次之，D3 仅作备选 |
| **Rule 2** | Role Relevance（角色相关度） | 与 JD Role 直接相关 → 升一级；仅间接相关 → 降一级 |
| **Rule 3** | Novelty Injection（新奇注入） | 若 Top2 证据过于同质化，允许插入 1 个 D2/D3 好奇心证据 —— 仅作为第三证据 |

<!-- 规则：Primary / Secondary 必须与 JD Role 直接相关；Curiosity 允许跨域，但仅在 Type D 中使用。 -->

### 9.2 Platform Variants（平台变体）

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

> LinkedIn 连接消息不附简历、不开口就问「有没有机会」。目标是建立联系，不是推销。

> **下游消费**：`07_boss_greeting.md`（Pack A）/ `08_boss_greeting.md`（Pack B）取本 Part 的 Primary / Secondary / Curiosity，
> 版式见 `references/pack_templates/08_boss_greeting_template.md`。

---

## 附录 A: JD 专业名词解释（Terms Glossary）

<!-- 准入判据（三级）—— 判据是「**是否产生决策信息**」，不是「是不是专业词」：
     · A 级 门槛判定型：该术语构成 JD **硬性要求 / 加分项** → **必写**，且必须有「用户现状」列（✓ / ⚠️ / ✗）
     · B 级 陌生领域扫盲型：用户对该 **track / 行业无背景**、术语构成理解障碍 → **仅该 track 首次出现时写一次**
     · C 级 纯释义型：该词**已出现在 Career DNA 的能力描述中**（04_skill_graph / 04b）→ **禁写**
       （用 Career DNA 当「已知词表」，不新建术语库 —— 判据是「查表」，不是「凭感觉」）
     形态约束：① 列宽 ≤3 列 ② 总条数 ≤20（不含笔误对照）③ 分组名按实际内容生成，禁留空组
              ④ 笔误对照独立成节（它是 Part 1 逐字存档的配套，不属术语解释）
     同 track 复用：同 track 已有历史报告时，只写「复用指针 + 本批新增术语」，不重抄通用词。 -->

<!-- 复用指针（同 track 有历史报告时才写；无历史报告则删除本行）：
> 通用术语（{测试流程 / 常用工具 / SQL}）已在 `resume-outputs/{先前日期}-{公司}-{岗位}/01_jd_match_report.md` 附录 A 解释，
> 本附录仅记录本批新增术语。 -->

### A.1 {分组名 —— 按实际内容生成}

| 术语 | 含义（≤30 字） | 用户现状 / JD 位置 |
|------|------|------|
| {{术语}} | {{一句话}} | {{✓ 有 / ⚠️ 可迁移（有 {X}）/ ✗ 缺 / JD 硬性写入职责}} |

<!-- 规则：A 级术语必须有第三列 —— 直接供 Part 3.2 硬性缺口明细；B 级术语可省此列。 -->

### A.2 原文笔误对照（仅在有笔误时出现）

| JD 原文 | 实际应为 | 位置 |
|------|------|------|
| {{笔误原文}} | {{正确写法}} | {{职责 N / 要求 N}} |

---

## 附录 B: 公司背景尽调（Company Diligence）

<!-- 定位（四处边界，禁止互相复制）：
     · `13` §10.1 尽调三维度 = 查什么 / 从哪查（**通用清单**，不随 JD 变）
     · `01 Part 2.2` Business Context = **结论一行**（claim）→ 指向本附录（evidence）；**反向禁止**（本附录不重述结论）
     · `01 Part 7` Decision Score = **投递建议**（Strong/Moderate/Stretch/Weak Fit → Pack）—— **纯能力导向**，公司维度缺席
     · **本附录** = 本次查到了什么 + 由此推出什么（**论证**），为 Part 7 补上公司侧输入
     ⚠️ 本附录**不产出第二个「投 / 不投」结论** —— 否则与 Part 7 重复，且可能给出相反结论
        （Part 7 说 Strong Fit、本附录说这公司要黄）。结论归 Part 7，本附录只给依据。

     深度分级（**条数只决定深度，不决定做不做**）：
     · **Tier 1（每次必有 · 下限）**：B.1 四项决策摘要 ≈15 行 —— **所有 JD 报告，含 Pack C/D**
     · **Tier 2（值得深挖）**：Tier 1 + B.2 五层调查 + B.3 组织信号 + B.4 四算子 + B.5 口径冲突留痕（≈60 行）
     · **Tier 3（同公司复投）**：Tier 2 + 时点对比（上次 vs 本次变化）
     升级条件（→ Tier 2）：同公司 / 同批次 ≥2 份 JD ｜ JD 与业务阶段有**需解释的关联**（转型 / 跨界 / 新业务线）
                        ｜ 非知名企业需外查 ｜ 用户明确要求；（→ Tier 3）同公司 ≥2 次投递 -->

### B.1 决策摘要（Tier 1 —— 每次必填，四项缺一不可）

| # | 项 | 结论 |
|:--:|---|---|
| 1 | **公司往哪走** | {{战略方向 + 阶段状态（三时态锚点**简版**：说了什么 / 到哪一步 / 何时收钱；**锚点缺一 → 写「阶段未定」**）}} |
| 2 | **岗位在哪一层** | {{基本盘（现金流来源）/ 增长（引擎）/ 故事（未来）→ 岗位是「供养者」还是「被供养者」}} |
| 3 | **JD 组织信号** | {{发布者角色 + 至少一处信号：频率异常 / 时态异常 / 文本复制 / 内部矛盾}} |
| 4 | **对 Part 7 的影响** | {{加强 / 削弱 / 无关 —— 一句话，**不改分数、不改 Pack**}} |

> 兜底：公司信息查不到时**允许写「未获取」**，但**必须显式写出**，不得静默省略。
> ⚠️ 第 3 项（JD 自身信号）**永不适用兜底** —— 零成本可得，缺席即失职。

### B.2 查到了什么（Tier 2 —— 5 层调查）

| 层 | 字段（只写 ★） | 内容（必带信源与日期 / 报告期） |
|:--:|---|---|
| ① 身份层 | ★主体全称 / ★上市代码与板块 / ★成立与上市时间 | {{…}} |
| ② 规模层 | ★员工规模 / ★资质（高新 · 专利 · 软著 · 认证） | {{…}} |
| ③ 财务层 | ★最近一期营收与净利 / ★增速 / ★业务结构占比 / ★地域结构 | {{…}} |
| ④ 市场层 | 主要客户 / 自有品牌 / 二级市场区间涨跌 | {{…}} |
| ⑤ 组织信号层 | —— **见 B.3**（直接由 JD 读出，**最高价值层**） | — |

<!-- 防冗长：①② 层只写 ★ 字段；实控人姓名 / 注册资本 / 成立详细日期等对决策零增益的字段**不写**。
     第⑤层是唯一「免费且独家」的信源 —— 前四层靠外部检索（有成本、有时效），第⑤层直接读 JD。 -->

### B.3 组织信号（Tier 2 · ★ 最高价值层 —— 全部来自 JD 本身）

> 前提认知：**JD 是组织的自白书。** 措辞的**异常**（频率 / 时态 / 发布者 / 内部矛盾）都是信号。

| 信号类型 | 读法 | 本次观察 |
|---|---|---|
| **频率异常** | 反复出现 → 组织级指令，非团队偏好 | {{…}} |
| **时态异常** | 未完成时态（探索 / 寻找 / 引导）→ 方法空白 / 招标式职责 | {{…}} |
| **文本复制** | 逐字相同 → 已跑通的定义被复制（**扩编 vs 补位**） | {{…}} |
| **发布者** | 谁发的 → 编制归属（HR / 总监 / 创始人） | {{…}} |
| **内部矛盾** | 要求与待遇错配 → 岗位定义未跟上组织变化 | {{…}} |

### B.4 由此推出什么（Tier 2 · 4 个推理算子）

| 算子 | 产出 |
|---|---|
| **① 三时态锚点法** | {{战略层说了什么 / 执行层做到哪 / 变现层何时收钱 → 阶段判定；**三锚点须有日期或状态，缺一则判定不成立**}} |
| **② 三层结构** | {{基本盘 / 孵化层 / 输出层 → 目标岗位坐落在哪一层，决定稳定性判断}} |
| **③ JD 信号交叉印证** | {{由 B.3 推出的组织意图}} |
| **④ 否定性证据** | {{「他们没要求什么」→ 窗口判断。⚠️ **必须同时写反面**：窗口存在 ≠ 岗位合适}} |

### B.5 口径冲突留痕（仅在有冲突时出现）

| 事项 | 口径 1 | 口径 2 | 处置 |
|---|---|---|---|
| {{指标}} | {{值 + 信源 + 日期}} | {{值 + 信源 + 日期}} | **并列留痕，不择一采信** |

<!-- 推理纪律（红线，五条）—— 违反任一条即不得写入报告：
     1. **每条判定必须挂锚点** —— 结论后必须能追到一条具体事实，禁裸结论
     2. **口径冲突并列留痕，不择一采信**
     3. **查不到写「未获取」** —— 不编造、不用行业常识填充
     4. **只用公开信息 + JD 交叉印证** —— 不臆测内部人事与财务
     5. **数据标时点** —— 财务 / 股价 / 员工数必带日期或报告期 -->

---

<!-- 收尾检查：
[ ] Part 1-9 齐全（Pack C/D 可精简 Part 5-7 为摘要，见 mode_d）
[ ] 所有 %/Score 有算式或依据
[ ] D3 均有推理依据
[ ] 与 04/05/06/07/08 交叉引用一致（Q 编号 / Gap 编号 / Type 选择）
[ ] 附录 A（若有）≤20 条，且无 C 级纯释义词（判据：该词是否已在 04_skill_graph / 04b 的能力描述中）
[ ] 附录 B 的 Tier 1 四项齐（公司方向 / 岗位层级 / JD 组织信号 / 对 Part 7 的影响）；「未获取」已显式写出（第 3 项不得走兜底）
[ ] 附录 B 每条判定均挂锚点；口径冲突已并列留痕；数据已标时点
[ ] 附录 B 未产出第二个「投 / 不投」结论（决策结论归 Part 7） -->
