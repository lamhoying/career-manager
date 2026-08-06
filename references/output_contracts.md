# Output Contracts（产出合约 v2.1.2）

## 概念

Output Contracts 定义每个求职策略（Pack A/B/C/D）对应的文件产出清单和数据来源。确保不同策略下产出一致、可预期、不遗漏。

## 策略文件映射

### Pack A: Strong Fit（强匹配 — Match ≥ 80）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | JD分析 + Capability Translation |
| 2 | `02_resume_cn.md` | `02_resume_cn.md` | Career DNA + ATS Keywords |
| 3 | `03_resume_en.md` | `03_resume_en.md` | Career DNA (English) |
| 4 | `04_interview_pack.md` | 标准模板 | Expected Stories + High Risk Questions |
| 5 | `05_answer_cards.md` | 标准模板 | Story Bank |
| 6 | `06_upgrade_plan.md` | 标准模板 | Known Gaps + Improvement Priorities |

### Pack B: Moderate Fit（中等匹配 — Match 60-79）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | 同 Pack A |
| 2 | `02_resume_cn.md` | 标准模板 | 同 Pack A |
| 3 | `03_resume_en.md` | 标准模板 | 同 Pack A |
| 4 | `04_interview_pack.md` | 标准模板 | + Gap 相关问题 |
| 5 | `05_answer_cards.md` | 标准模板 | 同 Pack A |
| 6 | `06_gap_analysis.md` | `XX_gap_analysis.md` | Capability Translation Missing + Skill Weight |
| 7 | `07_upgrade_plan.md` | 标准模板 | + Gap Analysis 短期行动 |

### Pack C: Stretch Fit（拉伸匹配 — Match 40-59）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | + 完整 Capability Translation |
| 2 | `02_transition_resume_cn.md` | `XX_transition_resume_cn.md` | Adjacent Match 项目 + 迁移推理 |
| 3 | `03_transition_resume_en.md` | `XX_transition_resume_en.md` | 同上 (English) |
| 4 | `XX_transition_feasibility.md` | `XX_transition_feasibility.md` | Capability Translation 能力迁移分析 |
| 5 | `XX_learning_roadmap.md` | `XX_learning_roadmap.md` | Missing + Skill Weight |
| 6 | `06_interview_pack.md` | 标准模板 | + 转岗高频问题 |

### Pack D: Weak Fit（弱匹配 — Match < 40）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | JD 分析 |
| 2 | `02_gap_analysis.md` | `XX_gap_analysis.md` | Missing + Feasibility |
| 3 | `03_transition_feasibility.md` | `XX_transition_feasibility.md` | Persona + Adjacent + Market |
| 4 | `04_learning_roadmap.md` | `XX_learning_roadmap.md` | Gap + Feasibility → 学习计划 |

> Pack D 不生成简历和面试包。

## 策略升级规则

- Capability Match 中 Adjacent 占比 > 60% 且 Match Score ≥ 40 → **升为 Stretch Fit**
- Missing 中含 Skill Weight > 30% 的 Critical → **降一档**
- 用户明确选择方向 → 不降档

## v1.5.2 / v1.5.3 注意

JD Match Report 模板结构已重构为 3 Parts（Part 1 JD Original / Part 2 Role Analysis / Part 3 DNA Match Analysis）。
Part 3.2 Match Score Breakdown 使用 4 维度（Hard Requirement 40% + Experience 30% + Capability 20% + Industry 10%）。
Part 3.2 Hard Requirement Detail v1.5.3 升级为 Score(0-100)+扣分来源，替代 ✓△✗。
Part 3.5 Evidence Mapping v1.5.3 新增 Coverage% 列 + Direct/Adjacent/Missing 子证据展开。
Part 3.6 Skill Gaps v1.5.3 新增 Gap Priority Matrix（P0/P1/P2）。
本合约中的文件编号不变（01_jd_match_report.md 始终为第一个文件）。

## 07_boss_greeting.md（v1.6.3 更新）

| 属性 | 值 |
|------|-----|
| 所属 | JD 级输出 |
| Pack 覆盖 | Pack A/B/C（Weak Fit 不生成） |
| 输出数量 | 每平台 2 个（Recommended + Alternative） |
| 必须附带 | Why Recommended / Why Alternative / Tone Notes / Do Not Say |
| 禁出 | 全部 Type 版本 / 内部评分术语 / 报告腔文案 |
| 上游依赖 | `01_jd_match_report.md` 3.1 / 8.1 / Part 6 / Part 9.1 |
| 与 11_online_profile.md 关系 | 独立文件 — Online Profile 是长期档案，Greeting 是即时沟通 |
