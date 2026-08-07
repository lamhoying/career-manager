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

派生资产不需要用户手动维护。如果目标文件尚未创建，则自动初始化。

### Step 5: 向用户反馈

向用户展示：
1. 本次更新了哪些文件
2. 当前完整度评分（对比上次如有提升，标注提升幅度）
3. Backlog 中仍待回答的问题（按优先级排序，最多展示 5 个）
4. Portfolio 候选池更新情况（Ready 项目数 / Need Evidence 项目数）
5. 建议的下一步行动

## Important Rules（重要规则）

1. **增量更新**，不重建整个 Career DNA。只修改受影响的文件。
2. **保持证据驱动**。新补充的能力必须有对应的项目证据。
3. **Backlog 问题被回答后必须标记为 Answered**，不能遗漏。
4. **每次更新后重新计算完整度**，让用户看到成长进度。
5. **不追问**。用户补充什么就更新什么，不主动盘问。
