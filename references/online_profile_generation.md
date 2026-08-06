# Online Profile Generation（Boss 在线简历生成规则 v2.5.4）

<!--
推理链（v2.5.4）：
  Step 0: Identity Resolution — 读取 07 Layer 1,2,5 → 锁定职业身份（唯一来源）
  Step 0.5: Experience Reframing — 经历重构为能力形成视角（R04）
  Step 1: Identity Anchor — 读取 07 Layer 1,2,3 → 身份锚点
  Step 2: Capability Priority — 读取 07 Layer 4 → Tier A/B/C
  Step 3: TC Selection — 读取 04b → 仅取 Tier A TCs
  Step 4: Evidence Filtering — 读取 03 → 仅保留 Tier A 案例
  Step 5: Personal Advantage（R01-R04 强制规则）
  Step 6: 展开工作经历 / 项目经历 / Track Coverage

07 是唯一身份来源，04b/03 作为证据池被筛选。经历以能力形成视角呈现。
-->

---

## Identity Resolution（身份解析 v2.5.3）

**生成 Online Profile 之前，必须先完成身份解析。此阶段不读 03、04、04b。**

### 解析步骤

1. 读取 `07_career_identity.md`
2. 提取：
   - Layer 1 Professional Identity → 一句话身份
   - Layer 2 Career Positioning → Primary Positioning
   - Layer 5 Non-Positioning Statement → 禁止表达列表
3. 确定：

```yaml
Identity Resolution:
  职业身份: [07 Layer 2 Primary Positioning]
  禁止表达: [07 Layer 5 全部条目]
  身份锚点来源: 07，非工作经历
```

### 硬约束

- 职业身份唯一来源 = 07。工作经历不能推导职业身份，只能证明职业身份。
- Identity Resolution 一旦完成，后续 Pipeline 不得修改职业身份。
- 后续读取 03/04/04b 时，任何与 Identity Resolution 冲突的身份推断 → 直接丢弃。

---

## Profile Generation Rules（强制性生成规则 v2.5.4）

以下规则由生成器强制执行，不可被任何下游步骤覆盖。

### Rule R01 — Professional Identity First（v2.5.3 强化）

**职业身份唯一来源是 07。以下行为在任何步骤中均为违规：**

- 从 02 的岗位历史中统计出现频次最高的岗位，作为职业身份
- 从 03 的项目角色中推断「这是一个XX的人」
- 在 Profile 生成后，用经历反推身份解释

生成器的第一步永远是读 07，不是读 03 或 04。
如果 07 Professional Identity 声明了「我是 XX型人才」→ 以此为唯一身份来源。

### Rule R02 — Experience is Evidence Only（v2.5.3 新增）

**经历仅允许作为能力证据，不允许作为身份定义。**

错误（经历作为身份）：
- 「[原始岗位 A] 组长」
- 「[N] 年 [原始岗位] 经验」

正确（经历作为证据）：
- 「通过 [原始岗位 A] 经历形成了 [能力描述]」
- 「[N] 年 [行业/领域] 经验」

Profile 的第一句主语必须来自 Identity Resolution 中的「职业身份」字段。
除 Identity Resolution 明确声明外，任何原始岗位名称不得作为主语。

### Rule R03 — Subject from Positioning（v2.5.3 新增）

**Profile 的主语来自 07 Layer 2 Career Positioning，不是来自工作经历。**

错误（主语来自经历）：
- 「从执行 [原始岗位] 成长为管理者」

正确（主语来自 Positioning）：
- 「[Career Positioning] 人才」
- 「通过 [原始岗位]、[行业 A] 和 [行业 B] 等经历形成 [核心能力描述]」

规则：
- Profile 第一句主语 = Identity Resolution.职业身份
- 任何「我是 [原始岗位]」的表达 → 替换为「我是 [职业身份]」
- 除非 07 主动声明该原始岗位即职业定位，否则禁止

### Rule R04 — Experience Reframing（v2.5.4 新增）

**经历必须以「能力形成过程」的视角呈现，而非「原岗位职责复述」。**

#### 角色名重构

| 原始岗位 | 应重构为 |
|------|------|
| [原始岗位] | [该经历在职业身份形成中的角色名，如 "XX [能力方向] 负责人"] |

规则：
- 角色名 = 该经历在职业身份中扮演的角色，不是原始合同抬头
- 重构后的角色名优先使用 TC Capability Identity 关键词
- 原始岗位可在技能标签旁括号注明，但不作为主展示

#### 工作内容重构

| 原始写法模式 | 重构为 |
|------|------|
| 参与 [某技术/工具] [某操作] | 建立 [某能力] 的 [体系/机制/流程] |
| 负责 [某场景] [某操作] | 制定 [某方向] 的 [策略/方案/标准] |
| [某类型] [某操作] | 推动 [某方向] 的 [能力建设/改进/落地] |

**规则**：
- 每一条工作内容必须回答：这段经历形成了什么能力？
- 禁止出现领域操作级词汇（如 [某工具操作]、[某流程环节]），除非作为证据从句
- 句首动词从操作层级升级到能力层级

#### 动词升级映射

```
参与 → 建立 / 推动
执行 → 制定 / 设计
编写 → 推动 / 建设
负责 → 主导 / 统筹
```

---

## Online Profile Generation Pipeline（v2.5.4）

生成顺序：**先锁定身份 → 经历重构为能力视角 → 再排序能力 → 经历作为证据被筛选**。

### Step 0: Identity Resolution（身份解析）

执行上文 Identity Resolution。输出 `Identity Resolution` 对象。

**此步骤在所有 Pipeline 步骤之前，单独执行。不读 03、04、04b。**

### Step 0.5: Experience Reframing（经历重构 v2.5.4）

基于 Step 0 的 Identity Resolution + TC 映射，对每条工作经历进行重构。

#### 输入

| 来源 | 提取内容 |
|------|------|
| Step 0 输出 | Identity Resolution（职业身份 + 禁止表达） |
| `03_projects.md` | 项目 TC 映射 |
| `04b_transferable_capabilities` | TC 的 Capability Identity 名称 |

#### 输出：每条经历输出 Reframed Experience

```yaml
Reframed Experience:
  原始岗位: [raw title]
  显示角色: [capability-based role — 从 TC Identity 推导]
  形成能力: [TC001, TC002, TC006]
  工作内容（能力视角）: [每条从「形成了什么能力」角度写]
  业绩（量化结果）: [保持原有]
```

#### 规则

- 显示角色 = 该经历在职业身份中扮演的角色（优先使用 Capability Identity 关键词）
- 原始岗位不在主展示区出现（可在技能标签旁括号注明）
- 工作内容每一条必须回答「这段经历形成了什么能力」，不得复述原始职责
- 禁止操作级动词作为句首（参照 R04 动词升级映射）

### Step 1: Identity Anchor（身份锚点）

基于 Step 0 的 Identity Resolution + Step 0.5 的 Reframed Experience + `07_career_identity` 的 Layer 3 Career Narrative。

| 子步骤 | 输入 | 输出 |
|------|------|------|
| 1a | Identity Resolution.职业身份 | 一句话身份 |
| 1b | 07 Layer 2 Career Positioning | 市场定位 |
| 1c | 07 Layer 3 Career Narrative | 核心价值主张 |

### Step 2: Capability Priority（能力排序）

读取 07 Layer 4，获取 Tier A/B/C 分层。对 04b 排序。

| 排序 | 来源 | 用途 |
|------|------|------|
| Tier A | 07 Layer 4 | Personal Advantage 正文 |
| Tier B | 07 Layer 4 | 工作经历中体现 |
| Tier C | 07 Layer 4 | 项目经历中展示或面试准备 |

### Step 3: TC Selection（TC 选取）

读取 04b，仅取 Tier A 的 TC 条目。不平均/随机/按精彩度选取。Tier A 优先 → 不足 3 个降级到 Tier B。

### Step 4: Evidence Filtering（证据筛选）

读取 03，仅保留能证明 Step 3 所选 TCs 的案例。TC 关联来自 03 的 TC 映射字段。

### Step 5: Personal Advantage Generation（个人优势生成）

基于 Step 0–4 输出，R01-R04 强制规则生成。

### Step 6: Experience & Project Expansion

- 工作经历：Step 0.5 的 Reframed Experience + Capability Tag + 双层技能标签
- 项目经历：Step 4 筛选后的 Top 3 + Capability Showcase
- Track Coverage：校验

---

## Personal Advantage Generation（个人优势生成规则 v2.5.4）

### 输入

| 来源 | 提取内容 |
|------|------|
| Pipeline Step 0 输出 | Identity Resolution（职业身份 + 禁止表达） |
| Pipeline Step 1 输出 | Identity Anchor（身份 + 市场定位 + 价值主张） |
| Pipeline Step 3 输出 | Tier A TCs（优先） |
| TC Evidence 字段 | 每个 Capability 的对应证据 |

### 结构

```
擅长：

- [Capability Identity 1]：[从 Expression Intent 衍生的简洁能力描述]
- [Capability Identity 2]：[描述]
- [Capability Identity 3]：[描述]

[Step 1 Identity Anchor 的身份一句话]

曾 [Evidence 1]，[Evidence 2]。
```

### 约束

- 长度：≤300 字
- R01：第一句主语是否来自 Step 0 Identity Resolution.职业身份 → 不是则替换
- R02：经历是否作为身份出现 → 是则改为证据从句
- R03：是否出现「我是 [原始岗位]」 → 替换为「我是 [职业身份]」
- R04：经历描述是否从能力形成视角写 → 不是则重构

---

## Work Experience Generation（工作经历生成规则 v2.5.4）

### 输入

| 文件 | 提取内容 |
|------|------|
| Pipeline Step 0.5 输出 | Reframed Experience（显示角色 + 能力视角内容） |
| `02_timeline.md` | 公司/时间线 |
| `05_story_bank.md` | 关键行动描述 |

### 工作内容规则（v2.5.4 重构视角）

结构：2-3 句能力小结 + 有序/无序列表（3-5 条）。

每条必须从「这段经历形成了什么能力」角度书写，不得复述原始职责。
句首动词使用能力层级（参照 R04 动词升级映射）。
禁止出现领域操作级词汇作为主要内容。

### 工作业绩规则

来自 03 的 Evidence 字段，优先量化结果。每段经历 2-3 条。

### Capability Tag 规则

每条经历标注：`关联能力：TC001, TC002`。来源：Step 0.5 Reframed Experience 的「形成能力」字段。

### 技能标签规则

两层：Capability Skills（TC Components）+ Technical Skills（Skill Graph 工具/技术类）。合计 ≤ 8 个。

---

## Project Experience Generation（项目经历生成规则）

### 输入优先级

```
12_portfolio_candidates（Ready）→ 经 Pipeline Step 4 筛选
    ↓
03_projects.md（TC 映射 → 经 Pipeline Step 4 筛选）
```

### Capability Showcase 规则

固定 Top 3 案例，每个标注展示 TC。选案确保 Tier A 全部覆盖。

---

## Multi-Track Coverage Rules

| Track | 最低覆盖率 |
|:--:|:--:|
| Primary | ≥ 60% |
| Secondary | ≥ 25% |
| Adjacent | ≥ 15% |
