# Output Contracts（产出合约）

> Aligns to: v2.21.0
## 概念

Output Contracts 定义每个求职策略（Pack A/B/C/D）对应的文件产出清单和数据来源。确保不同策略下产出一致、可预期、不遗漏。

**通用底料 vs JD 切片（v2.11.0）**：`career-dna/13_interview_narrative_strategy.md` 承载跨 JD 通用的面试叙事与战术，是**面试表达层的 SSOT**；各 Pack 的 `04/05` 面试产物是它的 **JD 切片**——生成时必须先读 13 的**全 12 个 Part**，再做 JD 适配。禁止绕过 13 从 07/05 重新拼装通用话术。

逐 Part 落点：

| 13 的 Part | 落到哪里 |
|------|------|
| Part 1-5 | `04` §1-§5 / `05` 的通用框架 |
| Part 6 口径纵深卡 | `04` §5 风险题 + `05` 风险卡（数字口径以此为准，禁止本轮加码） |
| Part 7 分轮次与分题型打法 | `04` §7.1（只填本轮实际轮次与用人；7.4 的题型映射到「形式」列） |
| Part 8 面试后跟进 | `04` §8（只记本轮实际动作与回应） |
| Part 9 复盘回路 | `application-tracker/archives/{Company}_{Role}.md`（不入 `04`） |
| Part 10 反向尽调 | `04` §7.2 本轮定制反问 + `01` Part 2.2（通用调研方法不入 `04`） |
| Part 11 录用阶段（谈判 / 背调） | `application-tracker/archives/{Company}_{Role}.md`（**不入 `04`**） |
| Part 12 英文面试准备 | `04` §10（条件必填：JD 要求英语工作语言时） |

## 共享边界表（哪些共享、哪些不共享 — v2.13.0）

各输出模块（Online Profile / ATS Resume / Interview Pack / Cover Letter）**共享同一批源头资产**，但**不共享抽象档位**。禁止把某渠道的具体表达反推或回灌到别的渠道。

| 共享（同一源头，改一处全体受益） | 不共享（各渠道独立决定） |
|---|---|
| **Identity** — `07_career_identity.md`（唯一定义源；L1-L5 分工见 07 头部注释） | **抽象档位** — 各渠道允许的角色/头衔抽象度不同（见下表） |
| **Capability** — `04b_transferable_capabilities.md`（TC + Tier + Position Constraint） | **Reframing 强度** — Profile 可高抽象；ATS 必须可追溯 |
| **Evidence** — `03_projects.md` + `02_timeline.md`（事实与量化结果） | **叙事长度与语气** — 由渠道形态决定 |
| **Narrative** — `13_interview_narrative_strategy.md`（面试表达层 SSOT，通用底料） | **表面化措辞** — 由各渠道的 spec 文件规定 |
| **Pipeline 定义** — `references/online_profile_generation.md` 的 §Online Profile Generation Pipeline | — |

**共享 ≠ 相同字面**：同一身份在四个渠道的**表面化形式**不同，这是**刻意设计**，不是漂移。

## 抽象档位表（Identity 在各渠道的表面化档位 — v2.13.0）

| 渠道 | 允许档位 | 硬约束 | 规范落点 |
|---|:--:|---|---|
| Online Profile（在线简历） | **高抽象** | 允许身份化表达；角色标签须取自 `04b` 的 `Position Constraint.推荐` | `references/online_profile_generation.md` |
| ATS Resume（投递简历） | **中抽象（JD 切片）** | 必须可追溯到 JD 关键词与原始证据；不得出现面试会穿帮的表达 | `references/mode_d_job_application.md` |
| Interview Pack / Answer Cards | **全档（含战术）** | 通用底料取自 13 全 12 Part，再做 JD 适配 | `13_interview_narrative_strategy.md` + `pack_templates/04_*` |
| Cover Letter / Boss Greeting | **低抽象** | 即时沟通语境，不复述简历 | `pack_templates/08_*` |

**反例（禁止）**：① 把 ATS 的「JD 关键词最大化」措辞回灌 Online Profile → 身份漂移；② 把 Profile 的高抽象身份直接抄进 ATS headline → 关键词命中下降 + 面试穿帮。

**统一目标**：**同一根叙事脊柱（07 Layer 3）+ 按渠道规定表面化档位**。既不是「三个模块输出同一字面身份」，也不是「各自重新推导一遍」。

## 策略文件映射

### Pack A: Strong Fit（强匹配 — Match ≥ 80）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | JD分析 + Capability Translation |
| 2 | `02_resume_cn.md` | `02_resume_cn.md` | Resume Identity Lock(07) + Capability Mapping(04b) + JD Skills(Step 3.5) + Evidence(03) + Timeline(02) |
| 3 | `03_resume_en.md` | `03_resume_en.md` | 同上 (English) |
| 4 | `04_interview_pack.md` | 标准模板 | Narrative Alignment(07 Layer 3) + Capability Priority(04b) + Expected Stories + High Risk Questions |
| 5 | `05_answer_cards.md` | 标准模板 | Narrative Alignment(07) + Story Bank(按 TC 筛选) |
| 6 | `06_upgrade_plan.md` | 标准模板 | Known Gaps + Improvement Priorities |

### Pack B: Moderate Fit（中等匹配 — Match 60-79）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | 同 Pack A |
| 2 | `02_resume_cn.md` | 标准模板 | 同 Pack A |
| 3 | `03_resume_en.md` | 标准模板 | 同 Pack A |
| 4 | `04_interview_pack.md` | 标准模板 | **Narrative Strategy(13 通用底料)** + Narrative Alignment(07) + Capability Priority(04b) + Gap 相关问题 |
| 5 | `05_answer_cards.md` | 标准模板 | **Narrative Strategy(13 通用底料)** + Narrative Alignment(07) + Story Bank(按 TC 筛选) |
| 6 | `06_gap_analysis.md` | `XX_gap_analysis.md` | Capability Translation Missing + Skill Weight |
| 7 | `07_upgrade_plan.md` | 标准模板 | + Gap Analysis 短期行动 |

### Pack C: Stretch Fit（拉伸匹配 — Match 40-59）

| # | 文件 | 模板 | 数据来源 |
|---|------|------|----------|
| 1 | `01_jd_match_report.md` | 标准模板 | + 完整 Capability Translation |
| 2 | `02_transition_resume_cn.md` | `XX_transition_resume_cn.md` | Adjacent Match 项目 + 迁移推理 |
| 3 | `03_transition_resume_en.md` | `XX_transition_resume_en.md` | 同上 (English) |
| 4 | `04_transition_feasibility.md` | `XX_transition_feasibility.md` | Capability Translation 能力迁移分析 |
| 5 | `05_gap_analysis.md` | `XX_gap_analysis.md` | Capability Translation Missing + Skill Weight |
| 6 | `06_learning_roadmap.md` | `XX_learning_roadmap.md` | Missing + Skill Weight |
| 7 | `07_interview_pack.md` | `04_interview_pack_template.md` | + 转岗高频问题 |

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

## Phase 归属（v2.17.0 新增 · 两阶段门控）

> **规则唯一定义源** = `references/mode_d_job_application.md` §Phase Routing（分流词表 + fail-safe）与 §Phase Gate（三段式输出 + 续跑规则）。**本表只登记产物归属**，不复述协议。

| Phase | 归属产物 | 说明 |
|---|---|---|
| **P1** Recon | `01_jd_match_report.md`（9 Part + 附录 A/B） | **该阶段唯一产物**。落盘后**必须停于 Phase Gate**；`career-dna/` 与 `knowledge/` 的回写（`mode_d` Step 8 / 10.A-C）同属 P1 |
| **P2** Build | 该 Pack 的全部文件 + `deliverables/` | 由 Gate 放行后生成，清单见上方各 Pack 表 |
| — | 投递索引登记 | **属 P2**（`mode_d` Step 10.D）—— 「打算投」才登记；P1 停住时**不登记**（「分析过」≠「要投」） |

- **P1 停住不是失败**：此时只有 `01` 报告 + 知识回写，**不产生任何 Pack 文件**、不登记投递索引。
- **续跑禁止重跑 Step 1-7**：P2 从已有 `01` 报告取输入（`01` 是自足的）；**仅当**用户显式说「重新分析 / JD 变了」才重跑 P1 并覆盖报告。

## 模板实体化（v2.1.3 更新）

本合约各表"模板"列的「标准模板」即 `references/pack_templates/` 下同名产物模板（01-08 实体版式骨架，含表格列头与字段占位）：

| 产物 | 模板文件 |
|------|----------|
| `01_jd_match_report.md` | `pack_templates/01_jd_match_report_template.md`（**9-Part**：Part 1 JD Original / Part 2 Role Analysis / Part 3 DNA Match / Part 4 Evidence Distance / Part 5 Role Authenticity / Part 6 Recruiter Risk Funnel / Part 7 Decision Score / Part 8 Recommended Strategy / **Part 9 Outreach Package（v2.18.0 收敛进 canonical）**） |
| `02_resume_cn.md` | `pack_templates/02_resume_cn_template.md` |
| `03_resume_en.md` | `pack_templates/03_resume_en_template.md` |
| `04_interview_pack.md` | `pack_templates/04_interview_pack_template.md` |
| `05_answer_cards.md` | `pack_templates/05_answer_cards_template.md` |
| `06_gap_analysis.md` | `pack_templates/06_gap_analysis_template.md` |
| `07_upgrade_plan.md` | `pack_templates/07_upgrade_plan_template.md` |
| `07/08_boss_greeting.md` | `pack_templates/08_boss_greeting_template.md` |

**编号映射**：Boss Greeting 在 Pack A = `07_boss_greeting.md`（A 无 gap 文件），Pack B = `08_boss_greeting.md`（B 有 06_gap + 07_upgrade）。upgrade_plan 在 Pack A = `06`、Pack B = `07`。禁止写死 07。

> 本文件历史版本中「JD Match Report 重构为 3 Parts」为 v1.5.2 时代旧说法，v1.5.4 起为 8-Part，**v2.18.0 起为 9-Part**（见上表）。

## 01 报告评分规则（v2.16.0 收敛）

Decision Score 的**规则与版式各有唯一定义源** —— 本文件不复述定义（防止出现第四处定义点）：

| 内容 | 唯一定义源 |
|---|---|
| **规则** — 公式 / `Factor Types` / Additive 废除原因 / Role Authenticity 折扣语义 / 情境因子边界 | `references/mode_d_job_application.md` **§Step 5.8** |
| **版式** — Part 7 的 7.1 公式与因子 / 7.2 计算拆解 / 7.3 情境因子展示区 | `references/pack_templates/01_jd_match_report_template.md` **Part 7** |

**v2.16.0 变更：Additive 因子废除**（原 `Location` 10% / `Language` 10% / `Industry` 5%）。Decision Score 现仅由两项构成：

```
Decision Score = 0.7 × Match + 0.3 × HireProbability
               = Match × (0.7 + 0.3 × Role Authenticity / 100)
```

废除原因：`Language` / `Industry` 与 `Match` **双计**（`Hard Requirement Match` 40% 已含语言、`Industry Match` 10% 已含行业）；`Location` / `Language` **零方差**（常数项使实际门槛由 60 降至 40）。
三项改为 Part 7 §7.3 `Situational Factors` 的 **Label 展示**（**非 Score**，不参与档位判定，无分值位）。

## 附录 A/B（v2.15.0 新增 · 可选产物）

`01_jd_match_report.md` 的附录 **A（JD 专业名词）/ B（公司背景尽调）** 是**可选产物**，与 `Part 1-9` 骨架**正交**：

| 属性 | 值 |
|------|-----|
| 命名 | `## 附录 A: …` / `## 附录 B: …` —— **不改 Part 编号、不进 Part 骨架** |
| 版式定义源 | `pack_templates/01_jd_match_report_template.md` 附录区（**唯一**） |
| 生成规则 | `mode_d_job_application.md` **Step 2.9** |
| 归属 | 随 `01_jd_match_report.md` 落 `resume-outputs/{JD}/`（**非 Career DNA SSOT**，无需四件套登记） |
| 闸门 | **无** —— 落在 `resume-outputs/`，不纳入 `validate_career_dna.py`；由 `01` 模板「收尾检查」块自检 |
| 附录 A | 三级准入（A 级必写 / B 级 track 首现写一次 / C 级禁写）+ 同 track 复用指针 |
| 附录 B | **每次必做 Tier 1 四项**（含 Pack C/D）；条数只决定深度（Tier 1/2/3）；**不产出第二个「投 / 不投」结论**（决策归 Part 7） |

> 边界：附录 B 为 `Part 2.2` 提供**论证**（claim → evidence 单向指针）；调研**方法**属 `13` §10.1（不随 JD 变）。

## 07/08_boss_greeting.md（v1.6.3 更新 · 编号随 Pack）

| 属性 | 值 |
|------|-----|
| 所属 | JD 级输出（Step X 附加产物，非 Pack 主编号序列） |
| 实际编号 | Pack A = `07_boss_greeting.md` / Pack B = `08_boss_greeting.md` |
| Pack 覆盖 | Pack A/B/C（Weak Fit 不生成） |
| 输出数量 | 每平台 2 个（Recommended + Alternative） |
| 必须附带 | Why Recommended / Why Alternative / Tone Notes / Do Not Say |
| 禁出 | 全部 Type 版本 / 内部评分术语 / 报告腔文案 |
| 上游依赖 | `01_jd_match_report.md` 3.1 / 8.1 / Part 6 / Part 9.1 |
| 与 11_online_profile.md 关系 | 独立文件 — Online Profile 是长期档案，Greeting 是即时沟通 |

## deliverables/ 投递定稿包（v2.8 新增）

### 概念

`deliverables/` 是每次 JD 投递的**最终交付形态**：从 working 版净化、审核、导出的可直接投递文件。与 working 版（含推理标注）物理隔离，追踪与投递互不污染。

### 产物合约

| # | 文件 | 生成方式 | 数据来源 | 适用 |
|---|------|----------|----------|------|
| 1 | `deliverables/02_resume_cn_final.md` | Step 9.5 净化（L1/L2 Strip） | `02_resume_cn.md` | 全部 Pack（A/B/C 有简历） |
| 2 | `deliverables/02_resume_cn_final.docx` | `scripts/export_resume.py --format docx --template resume_template.docx` | final.md | 全部 |
| 3 | `deliverables/02_resume_cn_final.pdf` | `scripts/export_resume.py --format pdf` | final.md | 全部 |
| 4 | `deliverables/cover_letter_final.docx/.pdf` | 净化 + 导出 | `07/08_boss_greeting.md`（编号随 Pack）+ `04_interview_pack.md` | Pack A/B |
| 5 | `deliverables/portfolio_final.pdf` | 净化 + 导出 | `XX_portfolio.md`（Ready 项目） | Pack A |

### 规则

- **净化不改内容，只剥离标注**：L1 删 `<!-- -->` 注释；L2 删 D0-D3 / TC 编号 / 版本注释；`[待补充]` 转用户确认
- **PII 反转**：working 版脱敏（[XX]），投递版由用户审核时填真实值
- **单一事实源**：审核后 final.md 为定稿事实源；小改直接改 final.md，大幅迭代回 working 版
- **token 纪律**：skill 只读 .md，永不读 .docx/.pdf 二进制；格式转换由脚本执行，不经过 LLM
- **v2.8 范围**：仅中文（02）；英文版（03）管道复用，待中文验证后扩展
- **模板**：`resume_template.docx` 从用户既有简历提取样式（微软雅黑 / 14pt 加粗标题 / 10.5pt 正文 / #1564BF 蓝色），可替换，脚本零改动
