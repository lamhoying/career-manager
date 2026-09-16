# Mode B: Career DNA Update Mode（职业资产更新模式）

## Trigger（触发条件）

用户执行以下任一操作：
- 补充新经历（新工作、新岗位）
- 补充新项目
- 补充管理经验
- 补充新技能
- 回答 Backlog 中的问题

## Objective（目标）

将用户补充的新信息增量回写到 Career DNA，保持职业资产持续更新。

## Preconditions（前置条件）

`career-dna/` 目录必须已存在。如不存在，提示用户先执行 Mode A。

## Workflow（工作流）

### Step 1: 读取现有 Career DNA

读取以下文件，建立当前状态基线：
- `career-dna/03_projects.md` — 现有项目列表
- `career-dna/04_skill_graph.md` — 现有能力图谱
- `career-dna/05_story_bank.md` — 现有故事库
- `career-dna/07_career_identity.md` — 现有职业身份（5 层结构）
- `career-dna/04b_transferable_capabilities.md` — 现有可迁移能力
- `career-dna/10_career_tracks/` — 现有职业方向
- `career-dna/08_question_backlog.md` — 待回答问题列表

### Step 2: 解析用户补充信息

根据用户输入类型，确定需要更新的文件：

| 用户输入 | 需要更新的文件 |
|----------|----------------|
| 新工作/新岗位 | 02_timeline.md, 03_projects.md, 04_skill_graph.md, 04b_transferable_capabilities.md |
| 新项目 | 03_projects.md, 04_skill_graph.md, 04b_transferable_capabilities.md, 05_story_bank.md |
| 管理经验 | 04_skill_graph.md, 05_story_bank.md, 07_career_identity.md |
| 新技能 | 04_skill_graph.md |
| 回答 Backlog 问题 | 对应文件 + 08_question_backlog.md |

### Step 3: 回写更新

按以下规则回写：

**Projects（项目资产库）**：
- 新项目追加到 `03_projects.md` 末尾
- 按项目资产库模板完整填写
- 量化成果优先，无数据标注 `[待补充]`

**Skill Graph（能力图谱）**：
- 新能力追加到 `04_skill_graph.md` 对应分类
- 已有能力如有新证据，更新等级和证据来源
- 保持能力等级定义一致（Expert/Proficient/Familiar/Aware）

**Story Bank（故事库）**：
- 从新项目中提炼面试故事，追加到 `05_story_bank.md`
- 按 STAR 结构编写
- 标注适用面试问题和风险提示

**Career Identity（职业身份）**：
- 检查新信息是否影响 07 的 5 层结构（Professional Identity / Career Positioning / Career Narrative / Capability Priority / Non-Positioning Statement）
- Layer 4 Capability Priority 如有变化 → 同步更新

**04b Transferable Capabilities**：
- 新项目/经历如形成新的可迁移能力 → 追加 Capability Identity
- 已有 Capability 如有新证据 → 更新 Evidence 字段

**Career Tracks（职业方向）**：
- 如新能力/经历影响了职业方向匹配度，更新 `10_career_tracks/{track}.md`
- 重新评估各方向匹配度

**Question Backlog（待补充问题库）**：
- 如果用户回答了 Backlog 中的问题：将状态从 Open 改为 Answered，记录回答内容和回答时间，标注已回写到哪个文件
- 如果更新过程中发现新的信息缺口：新增问题到 Backlog，状态为 Open

### Step 4: 重新计算完整度

执行 `scripts/completeness_checker.py` 重新计算完整度：

```bash
python3 scripts/completeness_checker.py [career-dna目录路径]
```

更新 `career-dna/09_completeness_report.md`：
- 更新整体完整度评分
- 更新各模块完整度
- 更新信息缺口列表
- 更新建议补充项
- 更新生成时间

### Step 5: 触发 Profile Regeneration（v2.7 新增）

更新完成后，如 `07_career_identity` / `04b_transferable_capabilities` / `03_projects` 任一文件变化 → 触发 `references/online_profile_generation.md` Pipeline 重新生成 `11_online_profile.md`。

### Step 4.5: 刷新派生资产（Derived Asset Refresh v1.5 + v2.1）

如果本次更新涉及以下任一文件，自动刷新对应派生资产：

| DNA 文件变更 | 触发刷新 |
|-------------|------|
| `01_profile` / `02_timeline` / `03_projects` / `04_skill_graph` / `07_career_identity` / `10_career_tracks/` / `12_portfolio_candidates` | `11_online_profile.md`（Online Career Profile v2.2） |
| `04_skill_graph` | `04b_transferable_capabilities.md`（Transferable Capability v2.3） |
| `03_projects` / `05_story_bank` / `04_skill_graph` | `12_portfolio_candidates.md` + Ready 项目的 `XX_portfolio.md` |
| `07_career_identity` / `02_timeline` / `05_story_bank` / `03_projects` / `04b` | `13_interview_narrative_strategy.md` —— **仅派生区 Part 1-3** |

**⚠️ 13 号文件的分区刷新规则（v2.11.0）**：

- 只重生成 **Part 1-3（派生区）**；**Part 4-12（手写区）绝不能被覆盖** —— 那里装的是推不出来的方法论与战术
  （三阶段结构 / 数字卡 / 口径纵深 / 分轮次与分题型打法 / 面试后跟进 / 复盘回路 / 反向尽调 / 录用阶段 / 英文面试）。
- 刷新**前**：确认手写区现有内容（如需要，先暂存）。
- 刷新**后**：运行 `validate_career_dna.py` —— 若报 P1 `derived-part-drift`，说明手写区被吃掉，
  **必须先从模板重建缺失的 Part 骨架，再提示用户补回内容**（不得静默放过）；
  若报 P1 `undeclared-part`，说明有 Part 未登记入 manifest，须补登记或删除。
- 刷新后同步更新头部 `Last Generated` 与 `Source Files Version`（07/05/02/03/04b）。

派生资产不需要用户手动维护。如果目标文件尚未创建，则自动初始化。

### Step 5: 向用户反馈

向用户展示：
1. 本次更新了哪些文件
2. 当前完整度评分（对比上次如有提升，标注提升幅度）
3. Backlog 中仍待回答的问题（按优先级排序，最多展示 5 个）
4. Portfolio 候选池更新情况（Ready 项目数 / Need Evidence 项目数）
5. 建议的下一步行动

## Mode B+: Proactive Interview Sub-flow（主动访谈子流程 v2.7.2）

**定位**：Mode B 内部的可选子流程，**不是新增顶层模式**（Mode Routing 保持 5 模式不变）。解决 Mode B"纯 ingest"的局限——当 Career DNA 中存在"已建档但稀薄"的 entry（缺量化、缺冲突处理、缺 Ownership/Scope 的 STAR），skill 通过**有配额的引导式访谈**将其对话式补全。

### Trigger（触发条件 · 纯 opt-in）

仅以下情况进入 Mode B+，**绝不自动启动**：

- 用户显式要求："帮我深挖 story bank" / "采访我关于 XX 项目" / "把 Backlog 第 N 个问题问完"
- 不响应"补充新信息"类输入（那是 Mode B 本职）

### Workflow（5 步工作流）

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1. Scope Lock | 锁定单一目标 entry | 读取目标 entry 当前内容，定位"稀薄维度"（STAR 缺 Result 量化 / Action 缺冲突处理 / Project 缺职责边界等） |
| 2. 生成访谈问题 | 基于稀薄维度生成 ≤3 个追问 | 每个问题带"目标字段 + 写入位置"标注；禁止开放盘问 |
| 3. 收集回答 | 问题一次性抛出 → 用户答完本轮 | 用户可自由阐述，也可明确跳过某题 |
| 4. 统一回写 | **一轮问答结束写一次** | 把本轮所有回答按 Mode B 回写规则统一落盘对应文件；不逐句写入 |
| 5. 配额检查 + 刷新 | 核对配额 + 触发派生资产刷新 | 达上限则剩余问题转 Backlog；派生资产刷新与完整度重算同 Mode B Step 4 / 4.5 / 5 |

### 问题模板（三层结构 + 自由兜底）

每个问题按以下结构设计，**引导式而非主观式，也非填空题**：

```
① 场景锚定：把用户拉回具体情境
   "你提到 XX 项目延期那次……"
② 维度提示：给出 2-3 个提示关键词（不强迫按序回答）
   "冲突双方是谁 / 你当时的立场 / 最后怎么收场的"
③ 示例锚点：可选，给 1 句话示例降低表达门槛
   "比如：'我坚持先砍范围再谈排期'"
④ 自由兜底：明确告知
   "你也可以用自己的方式讲，我负责整理成话术"
```

### 核心原则

1. **整理话术，不改写事实**：口语 → STAR 结构化 + 能力视角措辞（套用 Reframing 规则），但事实、数字、职责边界一律以用户原话为准。
2. **量化缺失标 `[待补充]`**：不猜测填充（Evidence Driven）。
3. **只挖已存在 entry 的稀薄维度**：不引导编造新经历。
4. **PII 纪律**：全程沿用 v2.5.5 脱敏规则（真实公司/项目/岗位 → 占位符）。

### 配额与护栏（反盘问）

| 护栏 | 取值 |
|------|------|
| 触发 | 仅 opt-in |
| 单 session 目标 | 单一 module / entry |
| 提问配额 | **≤3 问/轮，≤2 轮/session** |
| 落盘粒度 | 一轮问答结束统一写一次（每 session 最多 2 次写盘） |
| 溢出处理 | 配额内未完成 → 剩余问题转 Backlog，结束访谈 |
| 与 Backlog 关系 | 可主动拉取 Backlog Open 问题作为访谈目标（Pull 模式） |

### 与 Mode B 的区别

| 维度 | Mode B | Mode B+ |
|------|--------|---------|
| 提问主动性 | 被动 ingest，不追问 | 主动发起结构化访谈 |
| 触发条件 | 用户给新信息即触发 | 用户显式说"深挖/采访"（opt-in） |
| 目标粒度 | 用户给什么更新什么（广度） | 锁定单一 entry 挖深（深度） |
| 问题来源 | 无（不生成问题） | 从 entry 稀薄维度自动生成 |
| 追问配额 | 0（禁止） | ≤3 问/轮，≤2 轮/session |
| 落盘时机 | 批量回写 | 一轮问答结束写一次 |
| 与 Backlog 关系 | 被动：用户回答才关 | 主动：拉 Backlog 问题来访谈闭合 |

## Important Rules（重要规则）

1. **增量更新**，不重建整个 Career DNA。只修改受影响的文件。
2. **保持证据驱动**。新补充的能力必须有对应的项目证据。
3. **Backlog 问题被回答后必须标记为 Answered**，不能遗漏。
4. **每次更新后重新计算完整度**，让用户看到成长进度。
5. **不追问**。用户补充什么就更新什么，不主动盘问。深挖需求走 Mode B+（opt-in），不进本模式。
6. **写入契约（v2.11.0）**：只写入 `assets/career_dna_manifest.json` 中已登记的文件；用户的补充信息若不属于任何已登记文件，进 `08_question_backlog.md` 或 `career-dna/_inbox/`，**不得**在根目录新建文件。收尾时运行 `python3 scripts/validate_career_dna.py <career-dna目录>`；若刷新了 `13_interview_narrative_strategy.md`，**只允许重生成派生区 Part 1-3**，并同步更新其头部 `Last Generated` 与 `Source Files Version` —— 报 P1 `derived-part-drift` 即说明手写区被吃掉（须先从模板重建骨架、再提示用户补内容）；报 P1 `undeclared-part` 即说明有 Part 未登记入 manifest（须补登记或删除）。两者都不得静默放过。
