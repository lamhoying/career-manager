# Transferable Capability Generation（可迁移能力生成规则 v2.3）

## 触发条件

- Mode A Step 9.5：Skill Graph 构建完成后自动触发
- Mode B Step 4.5：Skill Graph 能力条目变更后触发
- Mode D Step 4.5：JD 分析时作为映射源调用

## Capability Identity 推导规则（v2.3.1）

### 原则

Skill Graph 条目是「能力事实」（我会什么），Capability Identity 是「能力本质」（这是什么能力）。

### 去工具化

- 从能力名称中移除：[某工具A] / [某工具B] / [某语言] 等工具/框架名称
- 保留：该能力要解决的核心问题类型

### 去角色化

- 从能力名称中移除：[岗位标签A] / [岗位标签B] / [岗位标签C] 等岗位标签
- 保留：该能力体现的管理/执行/分析层次

### 合并规则

- 多个 Skill Graph 能力指向同一核心问题 → 合并为一个 Capability Identity
- 示例：[能力组件A] + [能力组件B] + [能力组件C] → [Capability Identity 名称]

### 推导步骤

1. 遍历 Skill Graph 中 Confidence ≥ 50 的能力条目
2. 对每个条目：提取核心动词（管理/设计/推动/分析/保障）+ 核心对象
3. 合并指向同一核心问题的条目
4. 生成 Capability Identity（工具无关、岗位无关）

## Source A: Career DNA 自发现（初始化）

```
04_skill_graph
    ↓
聚类能力 → 生成 Capability Identity（工具无关、岗位无关）
    ↓
关联 Evidence（从 Skill Graph 证据列提取）
    ↓
推导 Components（该 Identity 的子能力组成）
    ↓
评估 Transfer Potential（跨岗跨度越小越高）
    ↓
定义 Transfer Boundary（对照 10_career_tracks + knowledge/role_snapshots）
    ↓
定义 Position Constraint（对照 10_career_tracks 的 Positioning + 07_career_identity 的 Career Identity）
    ↓
生成 Expression Intent（突出 = 角色核心需求抽象，避免 = 岗位标签/操作细节）
```

## Source B: JD 反馈增强（持续修正）

```
Mode D JD 分析
    ↓
发现 JD 对某 Track 的能力表述方式
    ↓
更新对应 Position Constraint 的「推荐」和「禁止」措辞方向
    ↓
验证 Transfer Boundary 的「适合」是否覆盖此 JD → 未覆盖则追加
    ↓
表达方向闭环：市场表述 → Position Constraint → Expression Intent → Online Profile
```

## Core Abstraction 推导规则

- 去除原始岗位名称 → 提取底层行为动词
- 优先使用「推动」「协调」「设计」「保障」等通用动词
- 必须可跨 Track 理解：非本行业 HR 也能看懂
- 示例：[某领域 某职能] → "[通用能力描述]"

## Transferable Keywords 输出规则

- 每个 Track 输出 2-3 个关键词
- 关键词来自 `knowledge/role_snapshots/{role}.md` 的 Role Capability Model
- 关键词 + 能力名称 = 完整岗位语言表达

## Forbidden Translation 判定

以下标记为禁止翻译：
- 原始岗位标签（不应直接出现在其他岗位的 Online Profile 中）
- 工具级描述（如 "[某工具操作]" → 应转换为 "[某流程] 体系设计"）
- 一次性项目行动（属于项目经历，不应作为能力翻译输出）

## 与 Skill Graph 的同步规则

- Skill Graph 能力被删除 → 对应 Transferable 标记 Deprecated（不删除）
- Skill Graph Confidence 变化 → 更新 Evidence Strength
- Transferable 中不新增独立能力（新能力必须先在 Skill Graph 登记）

## Online Profile 集成（v2.3.5 Capability-First）

生成管线从 Experience-First 升级为 Capability-First：

```
04b
↓
Capability Ranking（Position Constraint + Transfer Potential 排序）
↓
Personal Positioning（能力身份，禁止岗位标签开头）
↓
Experience Evidence（经历作为 Capability 的证据来源）
↓
Project Showcase（每个案例标注展示 Capability）
```

叙事结构从「我是 XX 岗位后来做了管理」变为「我是 XX 能力型人才，XX 经历是证据」。

TC 表在 Online Profile 中各字段的角色：
- **Capability Identity** → 个人优势中的能力名称
- **Position Constraint** → Capability Ranking 的排序依据
- **Expression Intent** → 个人优势造句方向
- **Components** → Capability Skills 层输出
- **Evidence** → 个人优势和工作经历的证据来源
