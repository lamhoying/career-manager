# Portfolio Candidates（作品集候选池 v2.1）

<!--
从 Career DNA 自动扫描生成。不依赖模型推理，仅基于 DNA 中已存在的信息。
来源：03_projects.md / 05_story_bank.md / 04_skill_graph.md / 10_career_tracks/
-->

## Discovery Rules（发现规则）

一条经历满足以下 4 项中 3 项以上 → 进入 Portfolio Candidate：

| 条件 | 说明 | 来源 |
|:--:|------|------|
| 1 | 有明确项目 | 03_projects |
| 2 | 有明确角色 | 03_projects |
| 3 | 有明确行动 | 05_story_bank |
| 4 | 有明确结果 | 03_projects + 05_story_bank |

---

## Validation Dimensions（验证维度）

每条 Candidate 从 7 个维度评分，每维 ✓/△/✗。评分基于 DNA 中已存在的信息，缺失即 ✗，不推测。

| 维度 | 判定 | 来源 |
|------|:--:|------|
| 项目背景 | 能否用 2-3 句说明为什么做这个项目 | 03_projects |
| 角色定位 | 能否清晰定义自己在该项目中的角色 | 03_projects |
| 核心问题 | 能否描述项目要解决的核心矛盾 | 05_story_bank |
| 解决方案 | 能否说明自己设计的方案逻辑 | 05_story_bank |
| 关键行动 | 能否描述 2-3 个具体操作步骤 | 05_story_bank |
| 项目成果 | 是否有量化结果或定性认可以 | 03_projects + 05_story_bank |
| 能力标签 | 能否映射到 Skill Graph 中的具体能力条目 | 04_skill_graph |

**Readiness = ✓ 项数 / 7**。≥ 70%（5 项以上 ✓）→ Ready，可生成作品集。< 70% → Need More Evidence，进入 Question Backlog [Portfolio]。

---

## Candidates（候选池）

### Ready（≥ 70% — 可生成作品集）

| 项目 | 背景 | 角色 | 问题 | 方案 | 行动 | 成果 | 能力 | Readiness |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| [项目A] | ✓ | ✓ | ✓ | ✓ | △ | ✓ | ✓ | 86% |
| [项目B] | ✓ | ✓ | △ | ✓ | ✓ | ✓ | ✓ | 86% |

### Need More Evidence（< 70%）

| 项目 | 缺失维度 | Readiness | 建议补充 |
|------|------|:--:|------|
| [项目C] | 背景、方案、成果 | 43% | 见 08_question_backlog.md [Portfolio] |

---

## Portfolio Potential Score（作品集潜在价值 v2.1.2）

<!-- v2.1.1 预留字段，v2.1.2 正式启用评分 -->

对每个 Candidate 从 5 个维度评估潜在展示价值（每维 0-20，满分 100）：

| 维度 | 权重 | 定义 | 数据来源 |
|------|:--:|------|------|
| **Complexity（复杂度）** | 20 | 项目涉及的系统/人员/技术复杂度 | 03_projects 项目规模 |
| **Ownership（主导度）** | 20 | 决策权和控制力 | 03_projects 角色/岗位 |
| **Business Impact（业务影响）** | 20 | 对业务指标的影响 | 03_projects 成果 |
| **Transferability（可迁移性）** | 20 | 经验能否复制到其他行业/岗位 | 10_career_tracks |
| **Story Potential（叙事潜力）** | 20 | 能否讲出有张力的故事 | 05_story_bank |

### Potential 分级

| 分数 | 等级 | 处理方式 |
|:--:|------|------|
| 80-100 | **A 级** | 核心案例，强制进入 Portfolio Ready |
| 60-79 | **B 级** | 优秀案例，建议进入 Portfolio Ready |
| 40-59 | **C 级** | 备选案例，用户决定是否展示 |
| < 40 | **D 级** | 不推荐作为 Portfolio |

> A/B 级 + Readiness ≥ 70% → Ready 并生成 Portfolio Case。
> C 级 → 用户手动选择。
> D 级 → 从 Candidates 移除。
