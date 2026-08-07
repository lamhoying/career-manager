# Online Profile Generation（Boss 在线简历生成规则 v2.5.6）

<!--
推理链（v2.5.6 — Identity → Capability → Evidence）：
  Step 0:   Identity Resolution — 读取 07 Layer 1,2,5 → 锁定职业身份
  Step 0.3: Capability Resolution — 读取 07 Layer4 + 04b → 锁定核心能力体系
  Step 0.5: Experience Reframing — 经历重构为能力形成视角（R04）
  Step 0.7: Evidence Retrieval — 读取 03 → 以 TC 驱动检索证据（R05）
  Step 1:   Identity Anchor — 读取 07 + Step 0.3 → 身份锚点
  Step 2:   Capability Priority — 07 Layer4 → Tier A/B/C
  Step 3:   TC Selection — 04b → 仅取 Tier A TCs
  Step 4:   Evidence Filtering — 03 → 仅保留 Tier A 案例
  Step 5:   Personal Advantage（R05-R10 强制规则）
  Step 6:   展开工作经历 / 项目经历 / Track Coverage

核心约束：Identity → Capability → Evidence 推理链不可逆序。
Online Profile 是职业营销材料，不是经历摘要。
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

## Profile Generation Rules（强制性生成规则 v2.5.6）

以下规则由生成器强制执行，不可被任何下游步骤覆盖。

### Rule R01 — Professional Identity First

**职业身份唯一来源是 07。以下行为在任何步骤中均为违规：**

- 从 02 的岗位历史中统计出现频次最高的岗位，作为职业身份
- 从 03 的项目角色中推断「这是一个XX的人」
- 在 Profile 生成后，用经历反推身份解释

### Rule R02 — Identity Derivation Prohibition（v2.7 合并 R02+R03）

**职业身份唯一来源是 07。经历仅作为证据。Profile 主语来自 Career Positioning。**

以下行为违规：
- 经历作为身份定义（禁止「[原始岗位 A] 组长」/「[N] 年 [原始岗位] 经验」）
- 主语来自原始岗位（禁止「从执行 [原始岗位] 成长为管理者」）
- 从经历反推身份解释

正确：
- 经历 = 能力证据（「通过 [原始岗位 A] 经历了形成了 [能力]」）
- 主语 = Career Positioning（「[Career Positioning] 人才」）
- Profile 第一句主语 = Identity Resolution.职业身份

### Rule R03 — Role Interpretation（原 R04 + R08 合并 v2.7）

**保留真实岗位名称作为事实。增加角色解释层，不修改事实。**

每个岗位输出：

```yaml
原始岗位: [合同上的岗位名称]
Role Interpretation:
  该岗位主要承担:
    - [能力维度 1]
    - [能力维度 2]
    - [能力维度 3]
```

规则：真实岗位始终保留（事实不可修改）；Role Interpretation 优先使用 Capability Identity 关键词；禁止将岗位名称直接改写为更高级的头衔。

---

### Rule R04 — Capability-First Experience Writing（v2.7 合并 R05+R06）

**Online Profile 优先展示能力，经历以能力形成视角呈现。**

生成层级固定：Capability → Evidence。禁止逆序。
个人优势 = 能力摘要（非经历摘要）。
经历描述必须回答三问：形成了什么能力 / 解决了什么问题 / 体现了什么价值。
允许高抽象（Profile Reframing）。禁止职责升级。动词升级：参与→建立/推动、执行→制定/设计、负责→主导/统筹。
任何以「负责…」「参与…」开头的段落 → 重构为「建立了…」「推动了…」开头。

> ⚠️ ATS Resume 使用独立的 ATS Reframing 机制（mode_d Step 9 + E01-E04）。ATS 推理链到 Evidence 为止，不到 Identity 层。

---

### Rule R05 — Capability Evidence Rule（v2.5.6）

**工作经历中的每个职责段落必须能映射到至少一个 TC。**

无法映射到任何 TC 的内容：
- 删除（低价值流水账）
- 合并（多条操作合并为一个能力描述）
- 降级（从主体内容移至技能标签旁注）

检查方法：
1. 取出每个职责段落
2. 检查是否能在 04b 中找到对应的 Capability Identity
3. 找不到 → 执行删除/合并/降级

---

### Rule R06 — Capability Density（v2.5.6 新增）

**Profile 中能力描述占比必须 ≥ 70%。**

检查项：
- 工作经历中，每条内容必须回答「形成了什么能力」而非「执行了什么任务」
- 如果「负责…」「参与…」「执行…」占比超过 30% → 判定失败，重新生成
- 项目经历中，每条内容必须回答「展示了什么可迁移价值」

---

### Rule R07 — Identity → Capability → Evidence Pipeline（v2.5.6 核心）

**生成 Online Profile 时必须固定执行的推理链，不可逆序：**

```
07 Career Identity
    ↓
职业身份（Identity Resolution）

    ↓
07 Layer4 + 04b
    ↓
核心能力体系（Capability Resolution）

    ↓
03 Projects + 02 Timeline
    ↓
经历证据（Evidence Retrieval）

    ↓
Profile 生成
```

Pipeline 中每个阶段的输出是下一阶段的输入。禁止跳过 Capability Resolution 直接从 Identity 跳到 Evidence。任何尝试从经历反向推导能力的路径 → 阻断。

---

## Online Profile Generation Pipeline（v2.5.6）

生成顺序：**Identity → Capability → Evidence，不可逆序**。

### Step 0: Identity Resolution（身份解析）

执行上文 Identity Resolution。输出 `Identity Resolution` 对象。

**不读 03、04、04b。**

### Step 0.3: Capability Resolution（能力解析 v2.5.6）

基于 Step 0 的 Identity Resolution，从 07 Layer4 + 04b 提取核心能力体系。

#### 输入

| 来源 | 提取内容 |
|------|------|
| Step 0 输出 | Identity Resolution（职业身份） |
| 07 Layer 4 | Capability Priority（Tier A/B/C） |
| 04b | 每个 TC 的 Capability Identity + Evidence |

#### 输出

```yaml
Capability Resolution:
  Core Value Proposition:
    - [Capability Identity 1]
    - [Capability Identity 2]
    - [Capability Identity 3]
  Tier B Support:
    - [Capability Identity 4]
    - [Capability Identity 6]
```

此输出决定：Personal Advantage 写什么 / Experience 保留什么 / Project 排序什么。

### Step 0.5: Experience Reframing（经历重构）

基于 Step 0 + Step 0.3 + TC 映射，对每条工作经历进行重构。

输出 `Reframed Experience` 对象（显示角色 + 能力视角内容 + 形成能力 TC 编号）。

### Step 0.7: Evidence Retrieval（证据检索 v2.5.6）

基于 Step 0.3 的 Capability Resolution，从 03 + 02 检索证据。

- 不按时间倒序列出所有经历
- 按 TC 关联度筛选经历
- 与任何 TC 无关的经历 → 降级为 Timeline 备注或删除

### Step 1: Identity Anchor（身份锚点）

基于 Step 0 + Step 0.3 + Step 0.5 + Step 0.7 + 07 Layer 3。输出身份锚点 + 市场定位 + 价值主张。

### Step 2: Capability Priority（能力排序）

读取 07 Layer 4，获取 Tier A/B/C 分层。对 04b 排序。

### Step 3: TC Selection（TC 选取）

读取 04b，仅取 Tier A 的 TC 条目。不平均/随机/按精彩度选取。

### Step 4: Evidence Filtering（证据筛选）

读取 03，仅保留能证明 Step 3 所选 TCs 的案例。

### Step 5: Personal Advantage Generation（个人优势生成）

基于 Step 0–4 输出，R01-R10 强制规则生成。

### Step 6: Experience & Project Expansion

- 工作经历：Step 0.5 Reframed Experience + Capability Tag + 双层技能标签
- 项目经历：Step 4 筛选后的 Top 3 + Capability Showcase
- Track Coverage：校验

---

## Personal Advantage Generation（个人优势生成规则 v2.5.6）

### 结构（v2.5.6 重构）

```
[职业定位一句话]

擅长：

- [核心能力 A]：[描述]
- [核心能力 B]：[描述]
- [核心能力 C]：[描述]

代表案例：
[关键证据 1]，[关键证据 2]。
```

### 约束

- 长度：≤300 字
- 不是经历摘要，是能力摘要
- 禁止「N年XX经验」开头
- R01-R07 全部规则在此处检查

---

## Work Experience Generation（工作经历生成规则 v2.5.6）

### 结构（v2.5.6 重构）

```
### [公司名]

**岗位**：[原始岗位]
**角色解释**：[该岗位在能力体系中承担的角色]

**能力贡献**：TC001, TC002

**关键成果**：
- [量化结果 1]
- [量化结果 2]
```

### 工作内容规则（R06+R07 约束）

每条内容必须回答三个问题（R04）且映射到至少一个 TC（R05）。无法映射的内容 → 删除。

### 技能标签规则

两层：Capability Skills（TC Components）+ Technical Skills（Skill Graph 工具/技术类）。合计 ≤ 8 个。

---

## Project Experience Generation（项目经历生成规则）

### Capability Showcase 规则

固定 Top 3 案例。每个标注展示 TC。选案确保 Tier A 全部覆盖。

---

## Multi-Track Coverage Rules

| Track | 最低覆盖率 |
|:--:|:--:|
| Primary | ≥ 60% |
| Secondary | ≥ 25% |
| Adjacent | ≥ 15% |
