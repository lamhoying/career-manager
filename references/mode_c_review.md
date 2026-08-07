# Mode C: Career Review Mode（职业发展分析模式）

## Trigger（触发条件）

用户提出以下问题：
- 我适合什么岗位？
- 我应该转型吗？
- 我的职业发展方向是什么？
- 我的竞争力在哪里？
- 我缺什么能力？

## Preconditions（前置条件）

`career-dna/` 目录必须已存在。如不存在，提示用户先执行 Mode A。

## Workflow（工作流）

### Step 1: 读取 Career DNA

读取以下核心文件：
- `career-dna/07_career_identity.md` — 职业身份（5 层结构）
- `career-dna/04b_transferable_capabilities.md` — 可迁移能力
- `career-dna/10_career_tracks/` — 职业方向
- `career-dna/04_skill_graph.md` — 能力图谱
- `career-dna/02_timeline.md` — 职业轨迹
- `career-dna/03_projects.md` — 项目资产（用于证据引用）

### Step 2: 分析职业身份（Career Identity Analysis）

基于 Career Identity 5 层结构分析：
- **当前定位**：07 Layer 1 Professional Identity + Layer 2 Career Positioning
- **非定位声明**：07 Layer 5 — 哪些经历属于来源而非定位
- **核心能力体系**：基于 04b + 07 Layer 4 Capability Priority（Tier A/B/C）

### Step 3: 分析职业方向（Career Track Analysis）

对 `10_career_tracks/` 中的每个方向进行深度分析：
- **匹配度评估**：重新计算匹配度，考虑最新能力图谱
- **优势分析**：用户在这个方向有哪些优势能力
- **差距分析**：用户缺少哪些关键能力
- **可行性评估**：转型难度、时间成本、市场机会

### Step 4: 能力差距分析（Gap Analysis）

针对用户最感兴趣的方向（或所有方向），进行能力差距分析：

```
目标方向所需能力
    vs
Career DNA 现有能力
    =
    能力差距
```

输出：
- **Critical Gap（关键差距）**：目标方向必需但用户完全缺失的能力
- **Development Gap（发展差距）**：目标方向需要但用户等级不足的能力
- **Transferable Strength（可迁移优势）**：用户已有但目标方向未被充分利用的能力

### Step 5: 生成成长路线图（Learning Roadmap）

基于 Gap Analysis 输出成长路线图：

**短期（1-3个月）**：
- 可立即提升的能力
- 具体行动建议（课程/实践/认证）

**中期（3-6个月）**：
- 需要系统学习的能力
- 建议的学习路径

**长期（6-12个月）**：
- 需要深度积累的能力
- 建议的实践机会

### Step 6: Market Signal Review（市场信号回顾 v2.7）

可选步骤。当 `application-tracker/` 中有投递记录时，结合 07 做方向校准。

**输入**：

| 来源 | 内容 |
|------|------|
| `application-tracker/01_application_index.md` | 投递记录 + 面试结果 |
| `07_career_identity` Layer 2 | Career Positioning |
| `10_career_tracks/` | 各 Track Confidence |

**分析维度**：

| 维度 | 说明 |
|------|------|
| **市场验证率** | 按 Track 统计面试率 → 哪些 Track 市场验证强 |
| **定位偏离检查** | 如果某个 Track 面试率高但 07 未将其列为主/次定位 → 检查是否需要更新 Career Positioning |
| **叙事效果** | 面试反馈中是否有关于「你是什么样的人」的信号 |

**输出**：分析报告（不自动修改 07，仅建议）。

### Step 7: Track Strategy Generation（赛道策略生成 v2.7.1）

基于 Career Identity + Capability Resolution + Track Confidence，为每个 Primary/Secondary Track 生成策略文件。

#### 输入

| 来源 | 内容 |
|------|------|
| `07_career_identity` | Career Positioning + Career Narrative |
| `04b_transferable_capabilities` | Capability Identity + Evidence |
| `10_career_tracks/{track}.md` | Track Confidence + Known Gaps |

#### 输出：每个 Track 生成策略卡片

```yaml
Track Strategy: [Track名称]
  Recommended Positioning: [针对此 Track 的定位变体]
  Top 3 Stories: [按 Narrative Strength 排序]
  Gap Mitigation: [此 Track 的缺口应对策略]
  Self-Intro Script: [30秒自我介绍框架]
  Project Priority: [针对此 Track 的项目展示顺序]
```

#### 规则

- 策略文件存储在 `career-dna/10_career_tracks/{track}_strategy.md`
- Mode D 投递时，先读取对应 Track 的 Strategy，再生成简历
- Mode A/B 更新 DNA 后 → 触发策略重新生成

## Outputs（产物）

直接向用户输出 **Career Review Report（职业发展分析报告）**，包含以下部分：

### 1. 职业身份概览
- 当前定位
- 核心竞争力（附证据）
- 差异化优势

### 2. 推荐职业方向
对每个推荐方向：
- 方向名称
- 匹配度评分
- 匹配理由
- 优势能力
- 关键差距
- 转型建议

### 3. 能力差距分析
- Critical Gap 列表
- Development Gap 列表
- Transferable Strength 列表

### 4. 成长路线图
- 短期/中期/长期提升建议
- 具体行动项

## Important Rules（重要规则）

1. **基于证据分析**。所有结论必须引用 Career DNA 中的具体项目或能力。
2. **不做主观判断**。不评价用户的职业选择好坏，只提供基于数据的分析。
3. **如信息不足以做分析**，将缺口问题记入 Backlog，并告知用户需要补充哪些信息。
4. **报告直接输出给用户**，不需要生成额外文件（除非用户要求保存）。
5. **鼓励用户进入 Mode D**。如用户已有明确目标岗位，引导其提供 JD 进入岗位投递模式。
