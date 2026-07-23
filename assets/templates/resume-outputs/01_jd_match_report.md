# JD Match Report: [公司名] - [岗位名]

<!--
岗位匹配报告 (JD Match Report v1.5.2)
Explainable Match Engine — 每个评分都有依据，每个依据都有来源。

Part 1: JD 原文归档
Part 2: 角色分析（合并 Decomposition + Intent + Persona + Skill Weight）
Part 3: DNA 匹配分析（Score Breakdown + Confidence Breakdown + Track Validation + Evidence Mapping + Strategy）
-->

## Part 1: JD Original（JD 原文存档）

<!-- 完整保存用户提交的 JD 原文，用于未来回溯和验证 -->

```
[用户提交的完整 JD 内容]
```

---

## Part 2: Role Analysis（角色分析 v1.5.2）

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

## Part 3: DNA Match Analysis（DNA 匹配分析 v1.5.2）

### 3.1 Match Summary（匹配概要）

| 维度 | 值 |
|------|-----|
| **Overall Match Score（综合匹配度）** | 70 |
| **Match Confidence（匹配置信度）** | 68 |
| **Application Strategy（求职策略）** | Moderate Fit → Pack B |

> Match Score 回答"你有多匹配"。Match Confidence 回答"我对这个判断有多确定"。

### 3.2 Match Score Breakdown（匹配得分分解）

| 评分维度 | 权重 | 得分 | 加权 | 说明 |
|----------|------|------|------|------|
| **Hard Requirement Match（硬性要求匹配）** | 40% | 72 | 28.8 | 学历/语言/证书/年限逐项判定 |
| **Experience Match（经验匹配）** | 30% | 65 | 19.5 | 行业/场景/角色 重叠度 |
| **Capability Match（能力迁移匹配）** | 20% | 75 | 15.0 | Direct+Adjacent+Missing 加权 |
| **Industry Match（行业匹配）** | 10% | 50 | 5.0 | 同行业/同客户群/同业务场景 |
| **Overall** | **100%** | **68** | **68.3** | |

#### Hard Requirement Detail（硬性要求明细 v1.5.3）

| JD 要求 | 用户状态 | Score | 扣分来源 |
|---------|----------|-------|----------|
| 5年+ Scrum 经验 | 2年实践+QA背景 | 50 | 头衔不匹配(-25) / 年限不足(-25) |
| Jira | 日常使用3年 | 90 | 非管理员角色(-10) |
| 英语流利 | 海外团队协作2年 | 95 | 无证书(-5) |
| [硬性要求4] | [用户状态] | [XX] | [扣分原因] |

> Score = 100 - 各扣分项累加（每项依据差距比例 × 权重）。
> 最终 Hard Requirement Match = 各项 Score 均值。
> 扣分规则：头衔不匹配但经验存在→-20~30 / 年限差距→按比例-10~15/年 / 证书缺失→-10~20 / 完全缺失→Score=0

### 3.3 Match Confidence Breakdown（匹配置信度分解）

| 置信度因素 | 权重 | 得分 | 说明 |
|-----------|------|------|------|
| **Evidence Count（证据数量）** | 30% | [XX] | [N] 项证据支撑 [M] 项能力匹配 |
| **Evidence Quality（证据质量）** | 30% | [XX] | [N] 项 High / [N] 项 Medium / [N] 项 Low |
| **Direct Relevance（直接相关性）** | 25% | [XX] | [N] 项 Direct + [N] 项 Adjacent |
| **Market Validation（市场验证度）** | 15% | [XX] | Observed JD Count: [N] |
| **Match Confidence** | | **68** | |

> Confidence < 70 → 匹配结果仅供参考，需更多证据验证。

### 3.4 Track Validation（赛道验证）

| 验证链路 | 得分 | 说明 |
|----------|------|------|
| Career DNA → [Track Name] | 78 | 用户在该 Track 的 Track Confidence |
| [Track Name] → [Role] JD | 72 | Track Core Skills 与 JD 要求的覆盖比例 |
| **Triangulated Validation（三角验证）** | **Strong / Moderate / Weak** | |

> 三角验证：用户 ↔ Track ↔ JD，比直接 User→JD 匹配更稳定可靠。

### 3.5 Evidence Mapping（证据映射 v1.5.3）

| JD 能力 | Coverage | Direct 证据 | Adjacent 证据 | Missing 证据 | 证据质量 |
|---------|----------|------------|--------------|-------------|----------|
| Scrum 管理 | 80% | 无 | 每日站会主持 / Sprint 回顾 | Burn-down 图表 | Medium |
| 项目管理 | 100% | 版本推进 / 多项目协调 | — | — | High |
| 客户培训 | 0% | — | — | 培训交付经验 | — |

> Coverage = (Direct数×100 + Adjacent数×60) / (Direct数 + Adjacent数 + Missing数)
> 每个 JD 能力可拆分子证据项，覆盖率 = 已覆盖子项 / 总子项
> 证据质量评定：Ownership+Scope+Impact（≥7pt=High, 4-6pt=Medium, ≤3pt=Low）
> Resume Builder 可根据 Missing 列自动判定是否需补充故事/项目

### 3.6 Skill Gaps（能力缺口 v1.5.3）

#### Gap Priority Matrix（缺口优先级矩阵）

| 缺口 | Impact（影响度） | Cost（补齐成本） | Priority（优先级） | 建议行动 |
|------|:---:|:---:|:---:|------|
| CSM 认证 | High | Low | **P0** | 2周考取 CSM |
| Scrum 年限不足 | High | High | **P1** | 6月积累实践 |
| 行业案例 | Medium | High | **P2** | 主动争取项目 |

> Priority = f(Impact, Cost)
> - **P0**: High Impact + Low Cost → 立刻做（ROI 最高，对匹配度提升最大）
> - **P1**: High Impact + High Cost → 计划做（长期投资，需持续积累）
> - **P2**: Low/Medium Impact → 有余力再做

#### 详细缺口

| 缺失能力 | Skill Weight | Impact | Cost | Priority |
|----------|-------------|:------:|:----:|:--------:|
| [能力X] | 25% | High | Low | P0 |
| [能力Y] | 10% | Low | High | P2 |

### 3.7 Recommended Strategy（推荐策略）

#### Narrative Mapping（叙事映射）
[一句话：用什么样的故事主线来包装这次投递]

#### Key Projects（推荐项目）
| # | 项目 | 匹配理由 | 涉及能力 |
|---|------|----------|----------|

#### Key Stories（推荐故事）
| # | 故事 | 适用场景 | 涉及能力 |
|---|------|----------|----------|

#### High Risk Questions（高风险问题）
| 风险问题 | 风险原因 | 严重程度 | 应对策略 |
|----------|----------|----------|----------|

#### Application Advice（投递建议）
- **是否建议投递**: 是 / 谨慎 / 否
- **策略建议**:
- **重点关注**:
