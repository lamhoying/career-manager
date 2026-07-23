# Targeted Discovery Rules（定向证据发现规则）

## 定位

Targeted Discovery 不是 Career Advisor（职业顾问）。

职责范围：
- 验证 Career DNA 中已有信息的准确性
- 发现 Career DNA 中遗漏但对当前 JD 高价值的证据
- 升级已有但证据不足的能力
- 利用 Knowledge Layer 的 Role Snapshot 发现隐性能力要求

不负责：
- 职业规划建议（那是 Mode C 的职责）
- 通用能力盘点（那是 Mode A 的职责）
- 长期成长辅导（那是 upgrade_plan 的职责）

## 引用来源（Reference Sources）

Targeted Discovery 交叉引用三个数据源：

| 数据源 | 位置 | 内容 | 用途 |
|--------|------|------|------|
| Career DNA | `career-dna/` | 用户个人经历、能力、项目 | 确认用户已有什么 |
| Skill Graph | `career-dna/04_skill_graph.md` | 用户能力图谱（含 Confidence/Evidence） | 确认能力等级和证据强度 |
| Role Snapshot | `knowledge/role_snapshots/{role_name}.md` | 市场对该 Role 的能力要求快照 | 发现用户可能遗漏的隐性要求 |

## 追问逻辑（Questioning Logic）

核心决策流程：

```
JD 要求某能力
    ↓
Role Snapshot 中是否存在该能力？
    ├─ 否 → 该能力可能是 JD 特定要求，低优先级追问
    └─ 是 → 该能力是该 Role 的常见要求，进入下一步
            ↓
        Career DNA / Skill Graph 中是否有证据？
            ├─ 是 → 跳过，不追问
            └─ 否 → 进入追问 ✅
                    ↓
                检查 Confidence 和 Evidence Count：
                - Confidence < 60 或 Evidence Count = 0 → High 优先级追问
                - Confidence 60-80 或 Evidence Count = 1 → Medium 优先级追问
                - Confidence > 80 且 Evidence Count >= 2 → 跳过
```

**关键改进**：v1.1 起，追问不再只看 JD 措辞，而是结合 Role Snapshot 判断该能力是否为该 Role 的隐性常见要求。即使 JD 未明确写出，但 Role Snapshot 中高频出现的能力，也应纳入追问范围。

## 核心规则

### 规则 1：问题数量限制

每次 Targeted Discovery 最多追问 **3-10 个问题**。

- 匹配度 > 70%：3-5 个问题（只需补充少量证据）
- 匹配度 50%-70%：5-8 个问题（需要发现更多匹配证据）
- 匹配度 < 50%：8-10 个问题（需要深入挖掘潜在匹配点）

**禁止超过 10 个问题。** 超出部分记入 Backlog。

### 规则 2：不重复已确认信息

追问前必须读取 Career DNA 和 Knowledge Layer，确认：
- 哪些信息已确认（Skill Graph 中 Confidence >= 80 且 Evidence Count >= 2）
- 哪些信息已追问过但未回答（在 Backlog 中标记为 Open）
- Role Snapshot 中哪些能力已被 Career DNA 覆盖

只追问未确认且与当前 JD 或 Role Snapshot 高度相关的信息。

### 规则 3：高价值区域优先

按以下优先级寻找证据：

**优先级 1：JD 高权重能力 + Career DNA 未覆盖**
- JD 明确要求且权重高
- Career DNA 中完全没有记录
- 例：JD 要求"预算管理经验"，但 Career DNA 中无任何预算相关内容

**优先级 2：JD 高权重能力 + Career DNA 证据不足（Confidence < 60）**
- JD 明确要求且权重高
- Career DNA 中有提及但缺乏具体项目或量化成果
- Skill Graph 中该能力 Confidence < 60 或 Evidence Count <= 1
- 例：JD 要求"跨部门协作能力"，Career DNA 中有标签但 Confidence 仅 40

**优先级 3：Role Snapshot 高频能力 + Career DNA 未覆盖（隐性要求）**
- JD 未明确写出，但 Role Snapshot 中 Observed JD Count 高且该能力频率高
- Career DNA 中完全没有记录
- 例：项目管理岗位的 Role Snapshot 显示"利益相关方管理"高频出现，即使本 JD 未明确写出，也应追问

**优先级 4：Role Snapshot 高频能力 + Career DNA 证据不足**
- Role Snapshot 中高频出现
- Career DNA 中有记录但证据薄弱
- 例：Role Snapshot 显示"供应商管理"常见，用户 Skill Graph 中有该能力但 Evidence Count = 0

**优先级 5：潜在的高价值未知区域**
- 用户可能有但未提及的经历
- 既不在 JD 中，也不在 Role Snapshot 中，但基于行业常识可能相关
- 例：用户可能有客户培训、危机处理等经验，只是未在简历中体现

### 规则 4：追问方式

追问应自然、非盘问式。推荐话术：

**方式 1：场景触发**
> "我注意到这个岗位比较看重 [某能力]。你在 [某项目] 中有没有涉及这方面的工作？"

**方式 2：扩展提问**
> "你在 [某项目] 中提到了 [某职责]，除了这些，当时有没有也参与了 [相关领域] 的工作？"

**方式 3：假设性提问**
> "这个岗位可能需要处理 [某场景] 的情况，你之前有没有遇到过类似的情境？"

**方式 4：直接确认**
> "你的简历中提到了 [某经历]，能否再详细说说当时你在 [某方面] 的具体角色？"

### 规则 5：回写 Career DNA

Targeted Discovery 的发现必须回写 Career DNA：

| 发现类型 | 回写目标 |
|----------|----------|
| 新项目经历 | `03_projects.md` |
| 新能力 | `04_skill_graph.md` |
| 新面试故事 | `05_story_bank.md` |
| 仍待确认的问题 | `08_question_backlog.md` |
| 能力等级提升 | `04_skill_graph.md`（更新等级和证据） |

**回写规则**：
- 用户确认的信息立即回写
- 用户不确定的信息记入 Backlog，状态为 Open
- 用户否认的信息不回写（避免错误信息污染 Career DNA）

## 输出格式

Targeted Discovery 完成后，输出：

```
## 定向证据发现结果

### 已确认的新证据
1. [发现1] → 已回写到 [文件]
2. [发现2] → 已回写到 [文件]

### 待确认的问题（已加入 Backlog）
1. [问题1] → 优先级：High
2. [问题2] → 优先级：Medium

### 匹配度更新
- 更新前匹配度：XX%
- 更新后匹配度：XX%
- 变化原因：[简述]
```
