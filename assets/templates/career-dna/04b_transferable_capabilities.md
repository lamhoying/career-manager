# Transferable Capability Mapping（可迁移能力映射）

> Aligns to: v2.21.0
<!--
可迁移能力映射层 — Skill Graph → 岗位语言的解释器。
v2.3.3 升级：Expression Rules → Expression Intent（存意图不存句子）+ 新增 Position Constraint。

【唯一定义源 · v2.19.0】本文件是 **TC 编号 / TC 名称 / Capability Identity（能力本质）** 的唯一定义源。
  名称的唯一入口是 `### TCxxx: <名>`；他处（`07` Layer 4 的 Tier 表、`03` 的 TC 映射、各 pack 模板）
  **只允许引用 TC 编号，禁止复制名称** —— 复制过的名称会漂移（v2.19.0 收敛前的实测：同一 TC 出现 4 种写法）。

【双向关系分工 · v2.19.0】本文件的 `#### Evidence（证据来源）` 与 `03_projects.md` 的 `TC 映射`
  是同一条「项目 ↔ TC」关系的两侧：`03` = **项目事实侧**，本文件 = **能力侧**。
  按生命周期分别随各自文件刷新，故**不合并**；但任一侧新增/删除关系，另一侧必须同步（validate 的 P0 `duplicate-content` 只查长段落逐字重复，**查不出这种单边漂移**，须靠本条纪律）。
-->

- **Last Updated**: [YYYY-MM-DD]
- **Source**: 04_skill_graph.md / knowledge/role_snapshots/ / 05_story_bank.md

---

## Capability Translation Rules（能力转换规则）

```
Skill Graph（能力事实）
    ↓
Capability Identity（本质能力，去工具/去岗位）
    ↓
Transfer Boundary（适合哪些角色，不代表什么）
    ↓
Position Constraint（在每个岗位如何定位）★ v2.3.3
    ↓
Expression Intent（输出意图，生成器自行造句）
```

---

## Capability Map（能力映射表）

### TC001: [能力本质名称]

#### Capability Identity（能力本质）

[1-2 句 — 在什么环境下，通过什么方式，达成什么效果]

#### Evidence（证据来源）

- [证据项1]
- [证据项2]

#### Components（组件能力）

- [组件能力1]
- [组件能力2]
- [组件能力3]

#### Transfer Potential（迁移潜力）

[High / Medium / Low]

#### Transfer Boundary（迁移边界）

适合（Suitable for）：
- [角色/方向1]
- [角色/方向2]

不代表（Not equivalent to）：
- [不应被视为的能力1]
- [不应被视为的能力2]

#### Position Constraint（岗位定位约束 v2.3.3）
<!-- 在目标岗位中应该如何定位这个能力。回答：这是核心能力还是背景经历？ -->
<!-- 赛道条目数必须与 `10_career_tracks/` 实有赛道一致：有 N 个赛道文件就写 N 条（每赛道一条），禁止写死 2 条。 -->
<!-- 结构：每个 TC 只有一个 Position Constraint 段，赛道用**段内条目**区分。下面为多行式；亦可写成单行式：**赛道名**：定位: … / 禁止: … / 推荐: …（两种写法闸门均认可）。 -->

**[Track A]**:
定位: [背景而非职业身份 / 核心能力 / 加分项]
禁止（Forbidden）: [不应出现的表达方向]
推荐（Recommended）: [应突出的表达方向]

**[Track B]**:
定位: [背景而非职业身份 / 核心能力 / 加分项]
禁止（Forbidden）: [不应出现的表达方向]
推荐（Recommended）: [应突出的表达方向]

**…（按 `10_career_tracks/` 实有赛道逐条补齐，共 N 条）**

#### Expression Intent（表达意图 v2.3.3 升级）
<!-- 意图描述，不存完整句子。生成器根据意图自行造句。 -->

突出（Emphasize）:
- [意图1 — 如 展示主导权 / ownership]
- [意图2 — 如 展示协作机制 / coordination]
- [意图3 — 如 展示交付责任 / delivery]

避免（Avoid）:
- [应避免1 — 如 操作细节而非管理 / operational detail]
- [应避免2 — 如 原始岗位标签 / original role label]

---

### TC002: [下一个能力]

[同上结构]
