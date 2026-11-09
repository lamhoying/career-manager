# Output Contracts（产出合约）

> Aligns to: v2.24.0
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
| **去重原则**（v2.30.0）— 同一量化 / 同一事实**不跨节重复**；规则唯一源 = `references/online_profile_generation.md` §3 **`R1–R4`** | **项目经历形态与配额** — Profile 四段·3 槽位 / ATS 三标签·2–3 个（见 §项目经历形态） |

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

## 项目经历形态（v2.30.0 新增 · 防「形态差异」被误判为漂移）

**去重原则共享**（唯一源 = `references/online_profile_generation.md` §3 **`R1–R4`**，`` 升格）；
**段结构 / 配额 / 行级形态不共享** —— 由各渠道的**载体容量**决定，是**刻意设计**。

| 渠道 | 段结构 | 项目数 / 配额 | 行级形态 | 规范落点 |
|---|---|:--:|---|---|
| **Online Profile**（Boss 在线简历） | **四段**：背景与挑战 / 技术实现 / 关键行动 / 成果 | **固定 3 槽位**（不足 3 个不凑数） | 行动 `1.` 编号 · 成果 `-` bullet | `online_profile_generation.md` §Project Experience Generation |
| **ATS Resume**（`02_resume_cn`） | **三标签**：项目背景 / 核心贡献 / 项目成果 | **2–3 个**（按 TC 关联度选） | 三标签**裸行注记**（`.entry-note`） | `pack_templates/02_resume_cn_template.md` §项目经历 |
| **作品集**（`09_portfolio_book`·附件） | 单案例完整叙事（含图表 / 事实卡） | **≤3 案例 / ≤12 页**（每 JD 重选） | 自由 | `mode_d` **Step 9.6** |

**三渠道共同下限（受 `R1–R4` 约束）**

- **R1/R2**：项目侧每条「行动 / 成果」不得与**同渠道**「工作经历」重复 ⇒ 重叠则**改写为项目独有**，不得原样保留。
- **R3**：**同一数字只出现一次** —— 公司级总量留「工作业绩」，项目级切片留「项目成果」。
- **R4**：**单向** —— 只从项目侧删改，**不动工作经历**（工作经历 = 全集，项目经历 = 切面）。

> ⚠️ **不得跨渠道"修正"形态**：ATS 的三标签**不能**改成 Profile 的四段（简历字段无此容量），Profile 的 3 槽位**不能**按 ATS 的 2–3 个压缩。
> ⚠️ **但去重标准必须一致**：任一渠道发现数字 / 事实跨节重复，即违反 `R1–R4`，不论其形态如何。
> **机检（可选·用户侧，未随技能发布）**：`.workbuddy/scripts/_profile_dedup_check.py`（默认检 `11`；`--ats` 扫 `resume-outputs/*/02_resume_cn.md` 与 `deliverables/02_resume_cn_final.md`）。未配置该脚本时可改为人工核对「去标点归一化后逐行相似度 ≥ 0.60」的跨节重复。


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
| 7 | `07_interview_pack.md` | `pack_templates/04_interview_pack_template.md` | + 转岗高频问题 |

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
| **P2 内部** | Step 9.5 / **Step 9.6（作品集合册）** | **P2 内部第 2 个 opt-in**；与 Step 9.5 并列，**非 Phase Gate**（见 `mode_d` §四个「停」） |
| — | 投递索引登记 | **属 P2**（`mode_d` Step 10.D）—— 「打算投」才登记；P1 停住时**不登记**（「分析过」≠「要投」） |

- **P1 停住不是失败**：此时只有 `01` 报告 + 知识回写，**不产生任何 Pack 文件**、不登记投递索引。
- **续跑禁止重跑 Step 1-7**：P2 从已有 `01` 报告取输入（`01` 是自足的）；**仅当**用户显式说「重新分析 / JD 变了」才重跑 P1 并覆盖报告。
- **Portfolio Gate ≠ Phase Gate**：它是 **P2 内部**的 opt-in 停点（决定「合册要不要落盘成 PDF」），不是 P1/P2 之间的决策门。层次 / 性质指针 → `references/mode_d_job_application.md` §四个「停」。

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
| `09_portfolio_book.md` | `assets/templates/resume-outputs/09_portfolio_book.md`（合册骨架 · 输入契约 + Gate 交付物） |
| `09_portfolio_book_final.html` | `assets/templates/portfolio-outputs/portfolio_book_template.html`（合册 HTML 版式） |

**编号映射**：Boss Greeting 在 Pack A = `07_boss_greeting.md`（A 无 gap 文件），Pack B = `08_boss_greeting.md`（B 有 06_gap + 07_upgrade）。upgrade_plan 在 Pack A = `06`、Pack B = `07`。禁止写死 07。

> 本文件历史版本中「JD Match Report 重构为 3 Parts」为 v1.5.2 时代旧说法，v1.5.4 起为 8-Part，**v2.18.0 起为 9-Part**（见上表）。

## 简历版式契约（v2.27.0 新增 · 与「模板实体化」的关系）

`02_resume_cn.md` / `02_resume_cn_final.md` 的**行级写法**与**核心能力工具位**各有唯一定义源，本表只登记**落点**（防第四处定义点）：

| 内容 | 唯一定义源 | 本合约的约束 |
|---|---|---|
| 四条行级写法（二级缩进行 / 悬挂块 / 裸行注记 / 栏目强调） | `assets/templates/resume-outputs/resume_template.html`（约定注释）+ `pack_templates/02_resume_cn_template.md`（版式规则块） | 净化（Step 9.5 L1/L2）**只剥标注、不碰行级形态** |
| 核心能力**工具位** | `mode_d` §Capability Mapping（正文）+ `pack_templates/02` | **至多 2 处**附注、每处**仅 1 个工具**（v2.37.0）；资格 = JD 原文明示（只认 `01` Part 1）**或** `04` 首选证据，且 `04` 须有该工具条目；须留 `<!-- tool-slot -->` 判定痕；工具唯一展开位 = 「技能与认证 · 技能」行 |
| 工具附注闸门 | `mode_d` **QA-5**（`Capability Tool Slot Check`，v2.27.0 改名） | 「核心能力工具数 ≤1 且该工具满足强调 × 证据」 |

> ⚠️ **渲染端契约**：`export_resume.py` 按行首形态注入 `<div class="hang|sub">` 与 `.entry-note` ⇒ **不要在 md 里手调空格**（悬挂缩进由 `_emw` 按**渲染后纯文字宽度**折算——数源串会把 `==技能==` 算成 7 字符而错位）。
> ⚠️ **与 `` 的关系**：v2.24.0 的「裸行必须写成 `- ` bullet」**已被 v2.27.0 修订**（裸行 = 注记行）；旧警告的根因（裸行上提）不再成立。

## 对外披露边界（v2.31.0 新增 · 数据三分类 · ``）

> **规则唯一定义源 = 本节**。适用于**一切会离开本机的材料**：`11_online_profile`（Boss 公开档案）· ATS 简历（`02` / `03` + `deliverables/`）· 作品集（`09`）· 面试材料（`04` / `05`）· Boss 打招呼语（`07` / `08`）。
> **私人真源**（`03_projects` / `04_skill_graph`）与**内部报告**（`01_jd_match_report`）**不在本节约束内**（自用可留全量），但须显式标注「不外发」。

### 1. 三分类（判定问句：**这个数字是谁的？**）

| 类 | 定义 | 判定 | 对外处置 |
|:--:|---|---|---|
| **D-A 成果型** | 由**你 / 项目达成**的结果 | 「这是我做出来的吗？」 | ✅ **保留** —— 这是竞争力 |
| **D-B 规范型** | 由**公司 / 项目定义**的阈值、分档、验收容差、分级门槛 | 「这是别人定的标准吗？」 | 🔒 **抽象** —— 只留「达标 / 超标」，不留数值 |
| **D-C 私有事实** | 真实公司名 / 客户 / 未公开业务数据 | — | 已有 PII 规则管辖（`[XX]` 占位） |

### 2. 典型归属（示例对照，非真实数据）

| D-A（保留） | D-B（抽象） |
|---|---|
| 交付周期 X→Y 天 ｜ 准时交付率 100% ｜ 一次通过率 A–B% ｜ 周期内问题数 ≤ N（**问题客观描述**） ｜ 绩效评级达优（不写具体档位/排名） ｜ 资源 / 成本节约 R% | 内部验收分档阈值 ｜ 资源配比基线 ｜ 质量门禁标准 ｜ 不通过项占比容差 ｜ 各分档验收阈值 |

### 3. 对外表述处置（D-A 保留 / D-B 抽象）

> **分流前置（§1 判定优先）**：先用 §1 问句「这个数字是谁的？」判定 D-A / D-B —— **D-A 走 3.0（保留），D-B 才走 3.1（抽象）**。两类处置互斥，勿跨用。

#### 3.0 D-A 成果型：保留原则（不抽象）

D-A 成就背后**没有公司规范值可抽** —— 数字 / 方向 / 对比本身就是竞争力信号，抽象掉反而丢信号、显心虚。本节**只判定「留 / 剥」，不规定表述形态**（形态由上游引擎推导，落点见本节省略号下方「表述推导落点」）。

**唯一原则**：保留**信息承载部分**（数值 / 方向 / 对比），只剥离**身份泄漏 specifics**（内部型号 / 内部工具名 / 非信号的公司物件）。

**对照测试**（落笔前自问一句）：删掉这个数字 / 表述，成就是否变弱或不可证？
- **是** ⇒ **保留**（它是信号，与领域无关：提升率 / 规模 / 零故障 / 首建机制 / 跨团队覆盖 / 被采纳扩散……都只是这道题的不同答案）；
- **否，仅暴露公司内部物件** ⇒ **剥离**（换成 `[XX]` 或泛称）。

**表述推导落点（本节不重复，只指针）**：成就「怎么写成一句话」由 `pack_templates/02_resume_cn_template.md` 的 **「动作 + 机制 + 量化结果」** + **Capability Interpretation（能力名[JD措辞] → TC + D 标注 → 描述）** 定义，经 `references/mode_d_job_application.md` **Step 9（引擎循环）+ Step 9.1 QA** 落成 bullet。本节仅在其产物上做「留 / 剥」安全过滤。

> ⚠️ **禁把 D-A 硬套 3.1 的 D-B 模板**：纯成果（如「交付周期缩短 R 天」）若被错写成「关键质量指标分档全部达标」，既不真（无分档可抽）也不强（信号被稀释）。

#### 3.1 D-B 规范型：抽象写法（三条模板）

| 原形态 | 抽象后 | 保留了什么 |
|---|---|---|
| 达成内部质量标准（分档值 A/B/C） | 优化后**关键质量指标分档全部达标** | 维度 + 达标结论 |
| 建立 `<阈值串>` 的分档基线 | **按内部三维分档基线**（高 / 中 / 低）严判 | 方法论 + 动作 |
| 通过基线 = 不通过项 ≤X% / 子项 ≤Y% | 内部**验收双门槛**（主项 / 子项占比，阈值属内部规范） | 结构 + 保密声明 |

**三条纪律**

① **不写具体阈值** —— 数值一律换成「达标 / 全项达标 / 双门槛 / 分档」；
② **保留维度名**（如 时间 / 质量 / 成本 / 风险）—— 维度暴露的是**方法论**，不是规范值；
③ **保留改善幅度** —— 「优化前不足 NN（示例）」= 你的**发现**，可留；「目标 MM（示例）」= 公司标准，去掉。

> **为什么这样反而更强**：外部读者不知道你的基线怎么定 ⇒ 具体基线数值是**噪声**；「分档全达标」是**信号**。且主动声明「阈值属内部规范」本身即专业度（保密意识）。

### 4. 机检（可机械核对）

| 特征 | 意图 |
|---|---|
| 阈值关键字 + 数字（如 `基线值` / `阈值` / `上限值`） | 具体阈值 |
| 三档数值串 `\d+\s*/\s*\d+\s*/\s*\d+\s*(单位)` | 分档阈值 |
| 容差 `(≤\|<=)\s*\d+%` | 验收容差 |
| 分级门槛 `>\d+%\s*/\s*>\d+%` | 问题分级 |

脚本（可选·用户侧，未随技能发布）：`.workbuddy/scripts/_disclosure_check.py`（扫 L1–L4，**0 命中**为准）。未配置时可人工核对披露边界。
**已知豁免**：D-A 语境下的 `缺陷率 < 3%`（行业通用表述）· `修复 ≤3 个`（成果计数）—— 机检给出上下文行，人工复核。

### 5. 分层适用范围

| 层 | 文件 | D-B 处置 |
|---|---|---|
| **L1 公开档案** | `career-dna/11_online_profile.md` | **必抽象**（完全公开，风险最高） |
| **L2 投递件** | `02_resume_cn` / `03_resume_en` / `deliverables/02_*` | **必抽象**（会流转 / 存档；投递对象是同行） |
| **L3 附件** | `09_portfolio_book` / `deliverables/09_*` | **必抽象**（留方法论，去阈值） |
| **L4 面试材料** | `04_interview_pack` / `05_answer_cards` | **必抽象**（书面不写；口头由本人现场判断） |
| **L0 私人真源** | `03_projects` / `04_skill_graph` | **保留全量** ＋ 标「不外发」 |
| 内部报告 | `01_jd_match_report` | 保留 ＋ 标「不外发」 |

---

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
| 4 | `deliverables/cover_letter_final.*` | **已移除（v2.24.0）** —— 原写「净化 + 导出」，但全库**无渲染路径**（`pack_templates/` 无 cover 种子 · `export_resume.py --profile` 仅 `auto/resume/portfolio`）⇒ **声明了产物却跑不出来** | 求职信改由**用户自拟**（素材 = `07/08_boss_greeting.md`「邮件版」） | — |
| 5 | `deliverables/09_portfolio_book_final.{md,html,pdf,docx}` | **Step 9.6**（净化 + 渲染） | **案例库（`portfolio-outputs/`）经 Step 9.6 选取** | Pack A·B（有作品集时） |
| 6 | `deliverables/09_portfolio_book_final.md` | Step 9.6 Phase B（净化后 md） | **合册事实源**（脚本只读 `.md`） | Pack A·B |
| 7 | `deliverables/png/{stem}_p{i}.png` / `{stem}_long.png` | `scripts/export_resume.py --format png [--png-width 1160]` | final.md → **PDF**（再派生） | 全部 Pack（opt-in） |

### 规则

- **净化不改内容，只剥离标注**：L1 删 `<!-- -->` 注释；L2 删 D0-D3 / TC 编号 / 版本注释；`[待补充]` 转用户确认
- **PII 反转**：working 版脱敏（[XX]），投递版由用户审核时填真实值
- **单一事实源**：审核后 final.md 为定稿事实源；小改直接改 final.md，大幅迭代回 working 版
- **PNG 为 PDF 的再派生（v2.24.0）**：`final.md → HTML → PDF → PNG` —— **不从 HTML 截图**（HTML 是浏览器连续流，与 A4 分页 + onPage 背景层**不同源**）。分页 `{stem}_p{i}.png`（A4 比例、默认宽 1160）+ 长图 `{stem}_long.png`（**单张超高页**渲染 ⇒ 无接缝）。**派生渲染物 · 禁手改**；**单一事实源仍为 final.md**。**opt-in**（用户说「要发图 / 截图发 Boss」时）⇒ 挂 Step 9.5；⚠️ **与 Step X 打招呼语分开** —— Boss 平台策略「不附简历」约束的是**打招呼语语境**，截图属 **HR 索要后的响应**
- **token 纪律**：skill 只读 .md，永不读 .docx/.pdf 二进制；格式转换由脚本执行，不经过 LLM
- **v2.8 范围**：仅中文（02）；英文版（03）管道复用，待中文验证后扩展
- **模板**：`resume_template.docx` 从用户既有简历提取样式（微软雅黑 / 14pt 加粗标题 / 10.5pt 正文 / #1564BF 蓝色），可替换，脚本零改动
