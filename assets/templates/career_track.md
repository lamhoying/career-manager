# Career Track（职业赛道）: [Track Name]

<!--
职业赛道 (Career Track) — v1.3 新增 / v1.4 Client Intelligence Upgrade。
属于 Career DNA 个人资产层，回答"为什么用户适合这个方向"。
与 knowledge/role_snapshots/ 的市场画像互补但不重叠。

v1.4 新增: Market Validation / Matched Hiring Intent / Market Demand Signals / Evidence Strength
v1.4.2 新增: Track Confidence Breakdown（三分量分解）/ Market Validation Status / Validation Explanation
v2.12.0 变更: Track Strategy 由独立策略文件改为本文件内的实体段（S1-S4）—— 修复幽灵引用
-->

- **Track**: [赛道名称]
- **Confidence**: [0-100]
- **Last Updated**: [YYYY-MM-DD]

## Track Confidence Breakdown（赛道置信度分解 v1.4.2）

<!-- 让 Track Confidence 可解释：不是"AI觉得85分"，而是"证据85分 + 市场验证90分 + 需求度75分 → 84分" -->

| 分量 | 得分 | 说明 |
|------|------|------|
| **Evidence Strength（证据强度）** | 85 | 该 Domain 下所有 Skill 的 Confidence 均值（来自 Skill Graph） |
| **Role Snapshot Validation（市场验证度）** | 90 | Role Snapshot Core Skills 在 DNA 中的覆盖比例（10/11 = 90%） |
| **Market Demand（市场需求度）** | 75 | 基于 Observed JD Count 分级（≥10=High=90pt, 5-9=Medium=70pt, <5=Low=50pt） |
| **Track Confidence（综合置信度）** | 84 | Evidence × 40% + Role Validation × 35% + Market Demand × 25% |

### 评分解读 (Confidence Explanation)
- **Evidence Strength**: 该域 [N] 项能力，Confidence 均值 [X]，最高 [Max Skill]([score])，最低 [Min Skill]([score])
- **Role Snapshot Validation**: Role Snapshot [M] 项 Core Skills 中 [K] 项有 DNA 证据覆盖 ([K/M] = [X]%)
- **Market Demand**: 已观察 [N] 份 Role Snapshot JD，市场活跃度 [High/Medium/Low]

## Positioning（职业定位）

[一句话职业定位描述]

## Career Narrative（成长主线）

[一段话描述成长轨迹和核心竞争力主线]

## Evidence（支持证据）

| 能力 | 证据来源（项目/经历） | Confidence（置信度） |
|------|----------------------|------------|
| [能力1] | [项目A] | [XX] |
| [能力2] | [项目B] | [XX] |

## Core Strengths（核心优势）

1. **[优势1]**：证据 → [项目/案例]
2. **[优势2]**：证据 → [项目/案例]
3. **[优势3]**：证据 → [项目/案例]

## Recommended Projects（推荐展示项目）

1. **[项目名]** — 推荐理由：
2. **[项目名]** — 推荐理由：

## Recommended Stories（推荐面试故事）

1. **[故事名]** — 适用场景：
2. **[故事名]** — 适用场景：

## Market Intelligence（市场验证 v1.4.2）

- **Validation Status（验证状态）**: Validated（已验证） / Emerging（新兴） / Uncertain（不确定）
- **Matched Hiring Intent（匹配的招聘意图）**: [哪些 Hiring Intent 被最近的 JD 覆盖]
  - [意图1]
  - [意图2]
- **Market Demand Signals（市场需求信号）**: [从 Trend Notes 提取的市场信号]
- **Evidence Strength（证据强度）**: Strong（强） / Moderate（中等） / Weak（弱）
- **Recent JD Coverage（近期JD覆盖率 v1.4.2）**: [最近6个月JD中该Track Role Snapshot Core Skills在DNA中的覆盖率]
- **Market Signal（市场信号强度 v1.4.2）**: Strong（强） / Medium（中） / Low（低）

## Known Gaps（已知差距）

| 差距能力 | 当前状态 | 重要性 | 提升方向 |
|----------|----------|--------|----------|
| [能力X] | 完全缺失 / 等级不足 | High / Medium | [建议] |

## Improvement Priorities（提升优先级）

1. **短期（1-3月）**：[行动] → 目标：[预期效果]
2. **中期（3-6月）**：[行动] → 目标：[预期效果]
3. **长期（6-12月）**：[行动] → 目标：[预期效果]

## Target Roles（目标岗位）

- [岗位1]
- [岗位2]
- [岗位3]

## Online Positioning（在线展示定位 v1.5）

<!-- 用于 11_online_profile.md Part 5 的分级展示 -->
<!-- 所有 Track 文件中 Confidence 最高的 Track 作为 Primary -->
<!-- ⚠️ 与 `07_career_identity` Layer 2 的 Primary / Secondary / Emerging **Positioning** 同名不同义（F16 · v2.21.0）：
     本处层级由 **Confidence 排序**决定；07 处层级由**用户声明**决定。两者无对应关系，读取时不得混用。 -->

- **Primary Track（主赛道）**: [Track Name] — Confidence: [XX]
- **Secondary Track（副赛道）**: [Track Name] — Confidence: [XX]
- **Supporting Track（支持赛道）**: [Track Name] — Confidence: [XX]

> 系统自动按 Confidence 排序。Primary 用于 Boss 标题；Secondary/Supporting 补充展示。

## Track Strategy（赛道策略 v2.12.0）

<!-- Mode C Step 7 生成；v2.12.0 起写在本文件内，废除独立文件（原声明为 {track}_strategy.md） -->

> 与上方 `Recommended Projects` / `Recommended Stories` **分工不重叠**：
> 上方是「可用清单」（哪些项目 / 故事可用），本段是「排序与场景绑定」。
> 本段的项目 / 故事栏**只写条目标题，禁止粘贴正文**；已存在则**原地刷新本段**，不动同文件其他段落。

- **Last Generated**: [YYYY-MM-DD]
- **Source**: 07 / 04b / 本文件上方段落

### S1. Recommended Positioning（本赛道的定位变体）

[一句话 —— 对招聘方说的版本，区别于上方 `## Positioning` 的自我描述版]

### S2. Self-Intro Script（30 秒框架）

[骨架：身份锚点 → 2 个量化锚点 → 与本赛道的关系；正文模板见 13 Part 4 阶段一]

### S3. Project Priority（项目展示顺序）

| 顺序 | 项目（引上方 Recommended Projects） | 对这个赛道强调什么 |
|:--:|------|------|
| 1 | [项目名] | [强调点] |

### S4. Story Mapping（故事绑定）

| 场景 | 选用故事（引上方 Recommended Stories） | 为什么 |
|------|------|------|
| [开场 / 跨部门 / 技术深度 / 失败复盘] | [故事名] | [为什么选它] |

> `Gap Mitigation`（缺口应对）**不在本段建列** —— 见上方 `## Known Gaps` 与 `## Improvement Priorities`，避免双份维护。
