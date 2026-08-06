# Transferable Capability Mapping（可迁移能力映射 v2.3.3）

<!--
可迁移能力映射层 — Skill Graph → 岗位语言的解释器。
v2.3.3 升级：Expression Rules → Expression Intent（存意图不存句子）+ 新增 Position Constraint。
-->

- **Version**: v2.0
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

**[Track A]**:
定位: [背景而非职业身份 / 核心能力 / 加分项]
禁止（Forbidden）: [不应出现的表达方向]
推荐（Recommended）: [应突出的表达方向]

**[Track B]**:
定位: [背景而非职业身份 / 核心能力 / 加分项]
禁止（Forbidden）: [不应出现的表达方向]
推荐（Recommended）: [应突出的表达方向]

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
