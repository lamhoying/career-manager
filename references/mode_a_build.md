# Mode A: Career DNA Build Mode（职业基因库构建模式）

## Trigger（触发条件）

满足任意条件即进入此模式：
- 用户要求建立 Career DNA
- 用户要求梳理经历
- 用户要求盘点能力
- 用户上传简历且不存在 Career DNA
- 用户要求分析职业方向

## Objective（目标）

构建 Career DNA 初版。完整度目标：60%-80%。

**关键规则**：
- 禁止长时间连续追问。最多追问 3 轮，每轮不超过 5 个问题。
- 优先快速完成职业资产建档。
- 缺失信息进入 Question Backlog，不阻塞建档流程。

## Workflow（12 步工作流）

### Step 1: 初始化目录结构

执行 `scripts/init_career_dna.py` 在用户当前工作目录下创建 `career-dna/` 目录（9 个模板文件 + `10_career_tracks/` 目录含 README.md）。

```bash
python3 scripts/init_career_dna.py [目标目录]
```

如不指定目标目录，默认在当前工作目录下创建。

### Step 2: 解析简历（Resume Parsing）

如果用户提供了简历（文件、文本、截图）：
- 提取所有工作经历、项目经历、教育背景、技能列表
- 识别时间线、岗位变迁、晋升路径
- 标记信息不明确或缺失的部分

如果用户未提供简历：
- 询问用户是否愿意提供简历或口述经历
- 以对话方式收集核心信息（公司、岗位、时间、主要项目）

**输出**：内部解析结果，不单独成文件。

### Step 3: 提取职业轨迹（Career Timeline）

填写 `career-dna/02_timeline.md`：
- 整理所有工作经历为时间线表格
- 标注每段经历的起止时间、公司、部门、岗位
- 识别晋升路径和职业转折点
- 分析行业轨迹、职能轨迹、管理轨迹

**追问限制**：如离职原因缺失，不追问，直接留空并记入 Backlog。

### Step 4: 提取项目经历（Project Extraction）

填写 `career-dna/03_projects.md`：
- 从简历/口述中提取每个项目
- 按项目资产库模板填写：基本信息、职责与贡献、成果、可复用证据
- 量化成果优先；无数据时标注 `[待补充]`
- 为每个项目打标签：涉及能力、项目类型

**追问限制**：如项目细节不足，每个项目最多追问 1-2 个高价值问题，其余进入 Backlog。

### Step 5: 构建能力图谱（Skill Graph）

填写 `career-dna/04_skill_graph.md`：
- 从项目经历中提取所有展现的能力
- 按硬技能、软技能/管理能力、领域知识分类
- 为每项能力评定等级（Expert/Proficient/Familiar/Aware）
- 关联证据来源（具体项目）
- 标注应用场景和最近使用时间
- 识别能力缺口

**证据驱动**：每项能力必须有至少一个项目作为证据。无证据的能力标注为 Aware 并记入 Backlog。

### Step 6: 构建故事库（Story Bank）

填写 `career-dna/05_story_bank.md`：
- 从项目经历中提炼面试故事
- 每个故事按 STAR 结构编写
- 标注故事类型（STAR案例/管理案例/冲突案例/项目案例/高光案例）
- 标注适用面试问题
- 标注风险提示（追问可能暴露的弱点）

**目标**：至少 3-5 个故事。不足时不追问，标注 `[待补充]` 并记入 Backlog。

### Step 7: 构建失败案例库（Failure Story Library）

填写 `career-dna/06_failure_story.md`：
- 引导用户回忆 1-2 个失败经历
- 按模板记录：失败经历、教训总结、风险复盘、成长反思
- 标注适用面试问题

**注意**：失败案例需要用户主动提供，不强制追问。如用户无准备，记入 Backlog 等待补充。

### Step 8: 构建职业身份定义（Career Identity v2.5）

填写 `career-dna/07_career_identity.md`，5 层结构：

| 层 | 内容 | 回答 |
|------|------|------|
| Professional Identity | 第一人称身份陈述（起点经历是路径，不是身份） | 我是什么类型的人才 |
| Career Positioning | 主/次/成长市场定位 | 市场怎么认识我 |
| Career Narrative | 核心职业故事 + 价值主张 | 我靠什么创造价值 |
| Capability Priority | 04b 的 Tier A/B/C 权重标注 | 哪些能力写进个人优势 |
| Non-Positioning Statement | 经历来源 ≠ 职业定位（**以每行的「收录于 Layer 2」标注为准**） | 我不是什么 |

**⚠️ Layer 2 采集协议（v2.21.0 · 必须执行）**

Layer 2（Career Positioning）**只能由用户声明，不得从 `02` / `03` / `04` / `04b` 推断或代填**（`R01`）。
建档时**必须显式提问**，一次性问清三件事（问题形态复用 Mode B+ 的三层结构：场景锚定 → 维度提示 → 自由兜底）：

| # | 问什么 | 写入 |
|:--:|---|---|
| 1 | **主定位**：你希望市场怎么认识你？（列 2-3 个候选方向供选择 / 修改） | Layer 2 Primary |
| 2 | **次定位 / 成长方向**：还有哪些方向你希望被同时看到？ | Layer 2 Secondary / Emerging |
| 3 | **赛道映射**（逐条）：该方向对应哪个已有赛道？（列出 `10_career_tracks/` 现有赛道；无对应 → `none`） | Layer 2 的 `Track` 标注 |

**配额与落盘**：建档场景一次性问完（不设轮次上限，因须产出完整 `07`）；**一轮问答结束统一写一次**。
**用户答不上来的条目** → 写 `[待声明]` 并记入 `08_question_backlog.md`（**禁止替用户猜**）。
**收尾必做**：按 Layer 2 定稿同时填写 Layer 5 每条的「收录于 Layer 2」标注 —— 新建档**一律为 `none`**。

### Step 8.5: 生成面试叙事战略手册（Interview Narrative Strategy v2.11.0）

**目标**：以 `07_career_identity`（身份与叙事主线）+ `05_story_bank`（故事编号与 Narrative Strength 评分）+ `02_timeline`（时间线事实）+ `03_projects`（量化证据）+ `04b`（能力措辞）为输入，生成 `career-dna/13_interview_narrative_strategy.md`。

模板：`assets/templates/career-dna/13_interview_narrative_strategy.md`（**12 Parts，分派生区 / 手写区**）。模板尾部另含「**内容填充契约**」—— 定义每一节只允许三种形态（实体内容 / 规则 / 指针），并禁止「空指示」。

**分区规则（v2.11.0 · 必须遵守）**：

| 区 | Part | 生成方式 |
|:--:|------|------|
| **派生区** | Part 1-3 | 由上游文件推导，**自动生成** |
| **手写区** | Part 4-12 | 方法论与战术，**推不出来** —— 首次生成时按模板骨架落地，此后任何刷新都不得覆盖 |

> ⚠️ 手写区被自动刷新吃掉是**肉眼不可见**的事故类型，故 `validate_career_dna.py` 用 P1 `derived-part-drift`
> 检查 12 个 Part 标题是否齐全，并用 P1 `undeclared-part` 检查有没有多出未登记的 Part。收尾必须跑。

| Part | 要做什么 | 硬性约束 |
|------|----------|----------|
| Part 1 核心叙事主线 | 提炼一句话核心叙事 + 三大支柱（各配 TC）+ 底层差异化视角 + 叙事弧线 | 支柱必须映射到 TC；弧线里的"路径"不得写成"身份" |
| Part 2 离职故事话术 | 为每一次变动写话术 + 叙事逻辑，统一落到「阶段完成 → 主动选择 → 能力升级」 | **本 Part 是离职话术的唯一 SSOT**；`02_timeline` 只留时间线事实与指针，禁止两处各写一份 |
| Part 3 赛道转变叙事 | 主转变 / 次转变 / 通用应对结构 | 「禁止自称的标签」必须与 07 Layer 5 **∖ Layer 2 已收录方向** 一致 |
| Part 4 面试三阶段 | 自我介绍结构 + STAR 升维收束 + 四类问题策略 + 反问清单 | 故事编号与评分只能引自 05，**禁止在本文件改分** |
| Part 5 通用战术 | 数字引用卡 / 语言切换 / 状态管理 | 每个数字必须能在 03 或 05 找到出处，禁止估算或夸大 |
| Part 6 口径一致性与追问纵深 | 三层纵深模型 + 核心主张纵深卡 + 口径交叉校验表 + 追问防御 | 规模类数字**必须区分主语**（项目整体 vs 直属团队）；与 core 冲突时一律以 03/05 为准，**只改本手册** |
| Part 7 分轮次与分题型打法 | 分轮次打法总表（谁面 / 考什么 / 必带 / 禁忌 / 收尾）+ 跨轮次叙事一致性 + **7.4 分题型应对**（案例 / 白板 / take-home / 群面 / 压力面 / 技术对等） | **不得与 `01` 报告 Part 6 重复**（那份是风险视角）；7.1 列结构不得改，`04` §7.1 按它对齐 |
| Part 8 面试后跟进 | 时间轴与动作 + 感谢信模板 ×3 + 催进度公式 + 失联处置 + 口头 Offer 应对 | 单轮记录写 `04` §8，**本 Part 只放通用方法** |
| Part 9 复盘回路 | 复盘四问 + 沉淀规则 + 卡壳点归因 + 落点说明 | 记录落点在 `application-tracker/archives/`，**本 Part 只存方法与规则** |
| Part 10 反向尽调 | 尽调三维度（业务产品 / 组织工程 / 风险信号）+ 情报→反问转化公式 + 结论落点 + 红线 | 与 Part 4 阶段三分工：Part 4 = 反问**输出**，本 Part = 尽调**输入**；只用公开信息 |
| Part 11 录用阶段 | Offer 谈判四原则 + 三场景应对与示范句 + 禁忌 + 背调四份材料 + 推荐人不足应对 + 红线 | 与 Part 8.5 衔接（8 管跟进、11 管定案）；收入 / 离职口径必须与 Part 2 / 11.1 一致 |
| Part 12 英文面试准备 | 四件套材料规格 + 语言能力表述方式 + 听不懂/卡壳处置 + 英文版口径要求 | **本 Part 只定义规格与规则**；本轮英文稿写 `04` §10；数字口径不得因换语言放大 |

**生成后**：填写头部 `Last Generated` 与 `Source Files Version`（07/05/02/03/04b），否则报 P2；随后跑 `validate_career_dna.py` 确认无 P1 `derived-part-drift` 与 P1 `undeclared-part`。

**禁止**：把本步骤做成"再写一份简历摘要"——本文件定位是**面试表达层**（逐字可说的话术），不复述经历。单次 JD 的定制策略仍归 `resume-outputs/{JD}/04_interview_pack.md`。

### Step 9: 发现职业方向并生成 Career Track 文件（Career Track Discovery）

**目标**：识别 2-4 个潜在职业方向，并为每个方向生成完整的 `career-dna/10_career_tracks/{track}.md` 文件，而不是只写一句话。

#### 9.1 识别潜在 Track

基于 Step 5（Skill Graph）的 Domain 分布 + Step 8（Career Identity）的职业标签：

- 从 Skill Graph 中提取用户能力最强的 Domain（Confidence 均值最高的 2-4 个）
- 从 Career Identity 的职业标签匹配对应的 Track
- 结合行业常识补充可能的转型方向

输出候选 Track 列表（如 [Track A] / [Track B] / [Track C]）。

#### 9.2 为每个 Track 评估 Confidence（v1.4.2 升级）

Track Confidence 不再是一个静态数值，而是三分量加权计算：

**Track Confidence = Evidence Strength × 40% + Role Snapshot Validation × 35% + Market Demand × 25%**

| 分量 | 计算方式 | 数据来源 |
|------|----------|----------|
| **Evidence Strength（证据强度）** | 该 Domain 下所有 Skill 的 Confidence 均值 | `04_skill_graph.md` |
| **Role Snapshot Validation（市场验证度）** | Role Snapshot Core Skills 在 Skill Graph 中的覆盖比例 | `knowledge/role_snapshots/{role_name}.md` |
| **Market Demand（市场需求度）** | Observed JD Count 分级 | `knowledge/role_snapshots/{role_name}.md` |

**Market Demand 分级**：
- Observed JD Count ≥ 10 → 90pt（High / 市场活跃）
- 5-9 → 70pt（Medium / 市场一般）
- < 5 或无数据 → 50pt（Low / 市场待验证）

**解释输出**：在 Track 文件中写入 Confidence Breakdown，说明三个分量的具体数值和计算依据。

#### 9.3 为每个 Track 生成完整文件

对每个识别的 Track，使用 `assets/templates/career_track.md` 模板生成 `career-dna/10_career_tracks/{track}.md`，填写以下内容：

**必须填写的字段**（从已有 Career DNA 提取，不追问用户）：

| 字段 | 数据来源 |
|------|----------|
| **Track** | 赛道名称（snake_case） |
| **Confidence** | 9.2 计算结果 |
| **Positioning** | 从 Career Identity 提炼与该 Track 相关的定位 |
| **Career Narrative** | 从 Timeline + Identity 提炼该方向的成长主线 |
| **Evidence** | 从 Skill Graph 提取该 Domain 下所有能力的证据表格 |
| **Core Strengths** | Evidence 中 Confidence >= 80 的前 3-5 项 |
| **Recommended Projects** | 从 Projects 提取该 Domain 相关的项目（2-3 个） |
| **Recommended Stories** | 从 Story Bank 匹配该 Track 适用的故事（1-2 个） |
| **Known Gaps** | 从 Skill Graph Gaps 提取该 Domain 相关的缺失能力，标注当前状态和重要性 |
| **Improvement Priorities** | 基于 Known Gaps，按重要性分级为短期/中期/长期提升建议 |
| **Target Roles** | 该赛道下可投递的具体岗位名称 |
| **Track Strategy — S1 Positioning 变体** | 从 07 Career Positioning 改写为「对招聘方说」的版本（区别于本文件 `## Positioning` 的自我描述版） |
| **Track Strategy — S2 Self-Intro 框架** | 身份锚点 + 2 个量化锚点 + 与本赛道的关系（**骨架**，正文模板见 13 Part 4 阶段一） |
| **Track Strategy — S3 Project Priority** | 从上方 `Recommended Projects` 排序（**只写条目标题，禁止粘贴正文**） |
| **Track Strategy — S4 Story Mapping** | 从上方 `Recommended Stories` 绑定场景（开场 / 跨部门 / 技术深度 / 失败复盘） |

> **`## Track Strategy` 段（v2.12.0）**：由 Mode C Step 7 生成，**写在本文件内**（废除独立文件写法）；
> 该段自带 `Last Generated`，**不动文件头 `Last Updated`**（后者 = 赛道置信度重评时间，语义不同）。

**示例输出**：

```
career-dna/10_career_tracks/[track_name].md

Track: [Track名称]
Confidence: [XX]
Positioning: "[N]年[领域]经验，从[原始职能]到[目标能力]..."
Career Narrative: "从[原始岗位]起步，经历..."
Evidence: [能力A] (C[XX]) | [能力B] (C[XX]) | ...
Core Strengths: 1. [核心能力描述]...
Known Gaps: [缺失能力]（完全缺失, High）| ...
Target Roles: [岗位A], [岗位B], [岗位C]
```

**缺失信息处理**：如果某字段因信息不足无法填写（如没有失败案例支撑 Career Narrative），标注 `[待补充]` 并记入 Question Backlog。不阻塞 Track 文件生成。

#### 9.4 更新 README.md

更新 `career-dna/10_career_tracks/README.md` 的总览表，填入所有 Track 的摘要行：

```markdown
| Track | Confidence | Target Roles | Last Updated |
|-------|------------|-------------|--------------|
| [Track A] | [XX] | [岗位A], [岗位B] | [YYYY-MM] |
| [Track B] | [XX] | [岗位C], [岗位D] | [YYYY-MM] |
| [Track C] | [XX] | [岗位E], [岗位F] | [YYYY-MM] |
```

#### 9.5 关联 Question Backlog

将每个 Track 的 Known Gaps 中无法自动填补的项转化为 Backlog 问题。每个问题必须关联到对应 Track：

```markdown
### Q[N]: [Track名称] 方向缺少 [缺失能力] 的实践证据，你是否有相关经验？

- **关联 Track**：[Track名称]
- **关联 Gap**：[缺失能力]
- **关联 Skill**：[对应 Skill Graph 条目]
- **潜在影响**：High（Evidence Count 0→1，Confidence 预计 +15）
```

### Step 9.5: Transferable Capability Discovery（可迁移能力发现 v2.3）

**目标**：从 Skill Graph 自动推导 `career-dna/04b_transferable_capabilities.md`。

**流程**（详见 `references/transferable_capability_generation.md` Source A）：
1. 对 Skill Graph 中 Confidence ≥ 50 的能力，按 Domain 分组
2. 每组推导 Core Abstraction（去岗位标签化）
3. 对照 `10_career_tracks/` 的 Core Skills + `knowledge/role_snapshots/` 的 Role Capability Model
4. 生成每个 Track 的 Transferable Keywords
5. 标注 Forbidden Translation + Evidence Strength
6. 初始 Transfer Confidence = Medium（待 Mode D JD 验证）

**产物**：`career-dna/04b_transferable_capabilities.md`

### Step 10: 生成完整度报告和待补充问题库

执行 `scripts/completeness_checker.py` 计算完整度：

```bash
python3 scripts/completeness_checker.py [career-dna目录路径]
```

根据脚本输出填写：
- `career-dna/09_completeness_report.md`：完整度评分、各模块完整度、信息缺口、建议补充项
- `career-dna/08_question_backlog.md`：所有在上述步骤中积累的待确认问题（含 Step 9 产生的 Track/Gap 关联问题）

### Step 11: 生成 Online Career Profile（在线职业档案 v2.2）

**目标**：自动推导 `career-dna/11_online_profile.md` 为可直接填写 Boss 直聘的在线简历。

**推理链**：Career DNA → Profile Positioning Engine → Universal Strengths → Online Career Profile

**Online Profile Generation Pipeline**：**唯一定义见 `references/online_profile_generation.md` 的 §「Online Profile Generation Pipeline」**（含每步的输入/输出表）。

本手册**不重复该表** —— 步骤索引：Step 0 → 0.3 → 0.5 → 0.7 → 1 → 2 → 3 → 4 → 5 → 6（Identity → Capability → Evidence，不可逆序）。

**规则**（编号对齐 `online_profile_generation.md` v2.7 后的正式编号 R01-R07）：

- R01 → Step 0+1 执行：07 是唯一身份来源。禁止统计岗位频次作为职业身份。
- R02 → Step 5 检查：经历仅作为证据，不得作为身份定义；主语来自 Career Positioning，不得来自原始岗位名。
- R03 → Step 0.5 执行：保留真实岗位 + 增加角色解释层，禁止修改岗位事实，禁止将岗位名改写为更高级头衔；经历角色名与工作内容重构为能力形成视角。
- R04 → Step 0.5+5+6 执行：能力优先于经历；经历必须回答能力形成三问（形成什么能力 / 解决什么问题 / 体现什么价值）；允许高抽象，动词可升级（参与→建立/推动、负责→主导/统筹）。
- R05 → Step 0.5+0.7+6 执行：每个职责段落必须映射 TC；无法映射的内容删除/合并/降级。
- R06 → Step 5+6 检查：Capability 密度 ≥ 70%。「负责…」占比超 30% → 判定失败。
- R07 → 全 Pipeline：固定 Identity→Capability→Evidence 推理链，禁止跳过 Capability Resolution。

## Important Rules（重要规则）

1. **不要进行深度盘问**。每步最多追问 1-2 个高价值问题。
2. **缺失信息进入 Backlog**，不阻塞建档。Track 文件生成也不因信息不足暂停。
3. **所有能力必须有证据**。无证据的能力标注为 Aware。
4. **完整度目标 60%-80%**。不需要 100% 完整才能结束 Build Mode。
5. **Track 文件必须生成**。Step 9 必须为每个识别的 Track 生成完整的 `{track}.md` 文件，而不是只写摘要。
6. **Backlog 问题必须关联 Track**。Step 9 产生的 Known Gaps 转化为 Backlog 问题时，必须标注 Track / Gap / Skill / Impact 关联字段。
7. **完成后向用户展示完整度报告和 Track 总览**，并告知 Backlog 中有哪些待补充问题，鼓励用户在 Mode B 中逐步补充。
8. **写入契约（v2.11.0）**：只允许写入 `assets/career_dna_manifest.json` 中已登记的文件。任何临时分析、草稿、单次提问产物一律写入 `career-dna/_inbox/`（下划线前缀 = 非 SSOT）或 `resume-outputs/`，**不得**落到 `career-dna/` 根目录。收尾时运行 `python3 scripts/validate_career_dna.py <career-dna目录>` 自检——若报 P0 `orphan`，先移出或补登记再结束；若报 P1 `derived-part-drift`（13 号手册的派生区 / 手写区标题缺失），须先从模板重建缺失的 Part 骨架再结束；若报 P1 `undeclared-part`（13 号手册多出未登记的 Part），须补登记 manifest 的 `regeneration.*_parts` 或删除该 Part。

### Step 12: Portfolio Discovery & Output（作品集发现与生成 v2.1）

**目标**：从已完成的 Career DNA 自动发现可生成作品集的项目，验证完整度，输出 Portfolio Case。

#### 12.1 Portfolio Discovery（发现候选）

1. 扫描 `03_projects.md` 全部项目
2. 对每个项目检查 4 项 Discovery Rules（有项目/有角色/有行动/有结果）
3. 满足 3 项以上 → 进入 Portfolio Candidate Pool

#### 12.2 Portfolio Validation（验证）

1. 对每个 Candidate 逐项打 7 维评分（项目背景/角色/问题/方案/行动/成果/能力）
2. Readiness = ✓ 项数 / 7
3. ≥ 70% → Ready / < 70% → Need More Evidence

评分基于 DNA 中**已存在的信息**。缺失即 ✗，不推测补充。
成果维度：仅有定性认可 → △；有具体数字 → ✓。
能力维度：Skill Graph 中有对应条目 → ✓。

#### 12.3 Portfolio Output（生成作品集）

1. 对 Ready 项目逐个按 `XX_portfolio.md` 模板生成
2. 每字段严格从 DNA 提取，不推测补充：

| Portfolio 字段 | 主来源 | 备选来源 | 提取规则 |
|-----------|------|------|------|
| 项目概览 | 03_projects.项目背景 | 03_projects.基本信息 | 取首句 + 项目名 + 时间 |
| 项目背景 | 03_projects.项目背景 | 05_story_bank.Situation | 取全文限 3 句，并提取问题→影响表 |
| 我的角色 | 03_projects.角色/岗位 | — | 取角色 + 汇报关系 + 职责列表 |
| 业务流程分析 | 05_story_bank.Situation + Task | 03_projects.项目背景 | 从 Situation 提取 As-Is / 从 Task 提取痛点，推导 To-Be |
| 项目推进过程 | 05_story_bank.Action | — | 按阶段拆分（调研→设计→实施→优化），每阶段 2-3 行动 |
| 项目成果 | 03_projects.成果 | 05_story_bank.Result | 先取量化再取定性，按层级分类展示 |
| 能力体现 | 04_skill_graph | — | Confidence ≥ 70 且本项目 Evidence 引用的能力，✓ 列表形式 |
| 可迁移价值 | 10_career_tracks | 03_projects.标签 | 取 Track 归属 + 跨行业判断 |

> 不补充 DNA 中不存在的信息。缺字段标注 `[待补充]`。

#### 12.4 Portfolio Gap → Backlog

Need More Evidence 项目向 `08_question_backlog.md` 追加 `[Portfolio]` 标签问题。

#### 产物

- `career-dna/12_portfolio_candidates.md`
- `resume-outputs/XX_portfolio_{项目名}.md`
