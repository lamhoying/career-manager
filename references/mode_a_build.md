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

## Workflow（10 步工作流）

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

### Step 8: 构建职业身份（Career Identity）

填写 `career-dna/07_career_identity.md`：
- 基于 Step 3-7 的信息综合提炼
- 回答三个核心问题：我是谁、我的职业标签是什么、我的核心竞争力是什么
- 提炼差异化优势
- 记录职业价值观

### Step 9: 发现职业方向并生成 Career Track 文件（Career Track Discovery）

**目标**：识别 2-4 个潜在职业方向，并为每个方向生成完整的 `career-dna/10_career_tracks/{track}.md` 文件，而不是只写一句话。

#### 9.1 识别潜在 Track

基于 Step 5（Skill Graph）的 Domain 分布 + Step 8（Career Identity）的职业标签：

- 从 Skill Graph 中提取用户能力最强的 Domain（Confidence 均值最高的 2-4 个）
- 从 Career Identity 的职业标签匹配对应的 Track
- 结合行业常识补充可能的转型方向

输出候选 Track 列表（如 Project Manager / QA Manager / Implementation Consultant）。

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

**示例输出**：

```
career-dna/10_career_tracks/qa_manager.md

Track: QA Manager
Confidence: 85
Positioning: "5年QA经验，从手工测试到自动化测试体系搭建..."
Career Narrative: "从测试工程师起步，经历..."
Evidence: Test Automation (C90) | QA Process (C85) | ...
Core Strengths: 1. 测试自动化体系建设...
Known Gaps: CI/CD Integration（完全缺失, High）| ...
Target Roles: QA Manager, Test Lead, Quality Assurance Manager
```

**缺失信息处理**：如果某字段因信息不足无法填写（如没有失败案例支撑 Career Narrative），标注 `[待补充]` 并记入 Question Backlog。不阻塞 Track 文件生成。

#### 9.4 更新 README.md

更新 `career-dna/10_career_tracks/README.md` 的总览表，填入所有 Track 的摘要行：

```markdown
| Track | Confidence | Target Roles | Last Updated |
|-------|------------|-------------|--------------|
| QA Manager | 85 | QA Manager, Test Lead | 2026-07 |
| Project Manager | 72 | 研发PM, PMO | 2026-07 |
| Implementation Consultant | 60 | 实施顾问, 交付经理 | 2026-07 |
```

#### 9.5 关联 Question Backlog

将每个 Track 的 Known Gaps 中无法自动填补的项转化为 Backlog 问题。每个问题必须关联到对应 Track：

```markdown
### Q[N]: QA Manager 方向缺少 CI/CD 集成的实践证据，你是否有相关经验？

- **关联 Track**：QA Manager
- **关联 Gap**：CI/CD Integration
- **关联 Skill**：CI/CD Pipeline
- **潜在影响**：High（Evidence Count 0→1，Confidence 预计 +15）
```

### Step 10: 生成完整度报告和待补充问题库

执行 `scripts/completeness_checker.py` 计算完整度：

```bash
python3 scripts/completeness_checker.py [career-dna目录路径]
```

根据脚本输出填写：
- `career-dna/09_completeness_report.md`：完整度评分、各模块完整度、信息缺口、建议补充项
- `career-dna/08_question_backlog.md`：所有在上述步骤中积累的待确认问题（含 Step 9 产生的 Track/Gap 关联问题）

### Step 11: 生成 Online Career Profile（在线职业档案 v1.5）

**目标**：自动推导 `career-dna/11_online_profile.md`，不直接填写新内容。

**数据来源**（全部来自已完成填写的 DNA 文件）：

| 区块 | 数据来源 |
|------|----------|
| Part 1: Personal Branding | `07_career_identity.md` → Branding Keywords / Headline |
| Part 2: Career Summary | `01_profile.md` + `02_timeline.md` + `07_career_identity.md` → Career Summary |
| Part 3: Core Competencies | `04_skill_graph.md` → Confidence ≥ 60 的能力 |
| Part 4: Highlight Projects | `03_projects.md` + `10_career_tracks/` Recommended Projects |
| Part 5: Target Tracks | `10_career_tracks/` → 按 Confidence 排序取 Top 3 |

**规则**：
- Online Profile 是派生资产（Derived Asset），不直接填写新内容
- 如果来源文件某字段未填 → Online Profile 对应区块标记 `[待补充：来源 xxx.md 未完成]`
- 不阻塞生成

## Important Rules（重要规则）

1. **不要进行深度盘问**。每步最多追问 1-2 个高价值问题。
2. **缺失信息进入 Backlog**，不阻塞建档。Track 文件生成也不因信息不足暂停。
3. **所有能力必须有证据**。无证据的能力标注为 Aware。
4. **完整度目标 60%-80%**。不需要 100% 完整才能结束 Build Mode。
5. **Track 文件必须生成**。Step 9 必须为每个识别的 Track 生成完整的 `{track}.md` 文件，而不是只写摘要。
6. **Backlog 问题必须关联 Track**。Step 9 产生的 Known Gaps 转化为 Backlog 问题时，必须标注 Track / Gap / Skill / Impact 关联字段。
7. **完成后向用户展示完整度报告和 Track 总览**，并告知 Backlog 中有哪些待补充问题，鼓励用户在 Mode B 中逐步补充。

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
