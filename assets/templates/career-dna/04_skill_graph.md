# 能力图谱 (Skill Graph)

<!--
v1.2 字段说明：Domain / Related Skills
v1.4.2 新增：Evidence Quality（证据质量）/ Evidence Consistency（证据一致性）/ Evidence Recency（证据时效性）
Confidence 从"单一数值"升级为"可解释的三维分解"

Confidence 计算逻辑（v1.4.2 Explainable）:

Confidence = Evidence Count Quality(0-40) + Evidence Quality(0-30) + Recency(0-30)

├── Evidence Count Quality（证据数量质量）:
│   ≥3 项独立证据 = 40pt | 2项 = 25pt | 1项 = 10pt | 0项 = 0pt
├── Evidence Quality（证据质量）:
│   High（项目角色 Lead+ / 有量化数据 / 甲方认可）= 30pt
│   Medium（项目角色 Lead / 有部分量化）= 18pt
│   Low（辅助角色 / 无量化）= 8pt
└── Evidence Recency（证据时效性）:
    ≤6个月 = 30pt | ≤12个月 = 20pt | ≤24个月 = 10pt | >24个月 = 5pt

Evidence Consistency（证据一致性）: 多项目是否持续展现同一能力
- High: 3+ 项目持续展现 → Confidence +5（bonus）
- Medium: 2 项目展现 → 不计入 bonus
- Low: 仅1项目 → Confidence 不加 bonus

Confidence 字段用于：
- Mode D JD Match Report：判断能力证据强度，置信度加权匹配计算
- Mode D Targeted Discovery：决定是否需要追问（Confidence < 60 优先追问）
- Role Snapshot vs Skill Graph 交叉比对：快速定位证据薄弱的能力
- Skill Domain Snapshot 同步：Confidence + Evidence Count 反映个人在该 Domain 的积累深度
- v1.4.2 Score Explainability：回答"为什么这个能力是85分"（Count + Quality + Recency + Consistency）
- v2.3 Transferable Ref（可迁移引用）：指向 04b_transferable_capabilities.md 中的 TC 编号。无 Transferable → 留空（Mode A Step 9.5 自动生成）。一个能力可对应多个 TC。
-->

## 核心能力 (Core Skills)

| Skill（能力） | Domain（域） | Level（等级） | Evidence（证据来源） | Evidence Count（证据数） | Evidence Quality（证据质量） | Evidence Consistency（证据一致性） | Evidence Recency（证据时效） | Confidence（置信度） | Last Verified（最近验证） | Related Skills（关联能力） | Transferable Ref（可迁移引用 v2.3） |
|---------------|-------------|--------------|---------------------|----------------|------------------|---------------------|------------------|------------|---------------|--------------------------|---------------------------|

### 能力等级定义 (Level Definition)
- **Expert（专家）**：能独立主导，能教导他人，有多次成功实践
- **Proficient（熟练）**：能独立完成，有2次以上实践
- **Familiar（熟悉）**：能辅助完成，有1次实践
- **Aware（了解）**：知道概念，无独立实践

### Confidence 计算参考 (Confidence Calculation v1.4.2)

Confidence = Evidence Count Quality + Evidence Quality + Recency + Consistency Bonus

| 分量 | 维度 | 评分标准 | 满分 |
|------|------|----------|------|
| Evidence Count Quality（证据数量质量） | 独立证据项数 | ≥3=40pt, 2=25pt, 1=10pt, 0=0pt | 40 |
| Evidence Quality（证据质量） | 角色 + 量化 + 认可 | High(Lead+/量化/认可)=30pt, Medium(Lead/部分量化)=18pt, Low(辅助/无量化)=8pt | 30 |
| Evidence Recency（证据时效性） | 距今时间 | ≤6月=30pt, ≤12月=20pt, ≤24月=10pt, >24月=5pt | 30 |
| Evidence Consistency（一致性 Bonus） | 多项目持续展现 | 3+项目=+5pt, 2项目=0pt, 1项目=0pt | +5 |

| Confidence | 等级含义 |
|------------|----------|
| 90-100 | 高置信 (High) — 多证据 + 高质量 + 近期 + 一致性强 |
| 70-89 | 中高置信 (Medium-High) — 证据齐全但某维度有短板 |
| 50-69 | 中置信 (Medium) — 证据基础尚可 |
| 30-49 | 低置信 (Low) — 证据薄弱 |
| 0-29 | 待确认 (Unverified) — 无证据，应进入 Backlog |

### Domain 映射参考 (Domain Reference)
| Domain | 示例 Skill |
|--------|-----------|
| Project Management | Stakeholder Management, Risk Management, Resource Planning, Timeline Management |
| Testing | Test Planning, Test Automation, QA Process, Bug Management |
| Business Analysis | Requirements Gathering, Process Mapping, Stakeholder Analysis, Gap Analysis |
| Implementation Consulting | Implementation Planning, Client Training, Go-Live Support, Change Management |

## 能力分类 (Skill Categories)

### 硬技能 (Hard Skills)
| Skill（能力） | Domain（域） | Level（等级） | Evidence（证据） | Evidence Count（证据数） | Confidence（置信度） | Last Verified（最近验证） | Related Skills（关联能力） | Transferable Ref |
|-------|--------|-------|----------|----------------|------------|---------------|----------------|-------------------|

### 软技能 / 管理能力 (Soft Skills / Management)
| Skill（能力） | Domain（域） | Level（等级） | Evidence（证据） | Evidence Count（证据数） | Confidence（置信度） | Last Verified（最近验证） | Related Skills（关联能力） | Transferable Ref |
|-------|--------|-------|----------|----------------|------------|---------------|----------------|-------------------|

### 领域知识 (Domain Knowledge)
| Domain（域） | Depth（深度） | Evidence（证据） | Evidence Count（证据数） | Confidence（置信度） | Last Verified（最近验证） |
|--------|-------|----------|----------------|------------|---------------|

## 能力缺口 (Skill Gaps)
<!-- 列出明显缺失的关键能力 -->

## 交叉引用说明 (Cross-Reference Notes)
<!--
Skill Graph 与 Knowledge Layer 交叉比对：
- Role Snapshot 中有但 Skill Graph 中无 → 能力缺口（Gap）
- Role Snapshot 中有且 Skill Graph 中有但 Confidence < 60 → 证据薄弱，需追问
- Skill Graph 中有但 Role Snapshot 中无 → 可迁移优势（Transferable Strength）

Skill Graph 与 Skill Domain Snapshot 同步：
- Domain Snapshot 中高 Frequency 的 Skill 在 Skill Graph 中 Evidence Count = 0 → 优先建设
- Skill Graph 中高 Confidence 的 Skill 在 Domain Snapshot 中 Frequency = 0 → 潜在差异化优势
-->
