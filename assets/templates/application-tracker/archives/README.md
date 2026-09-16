# Case Archives（投递案例档案）

> Aligns to: v2.19.0
按需建档。在 `01_application_index.md` 中任意投递记录满足以下条件之一时创建。

## 建档条件

1. **进入 HR 面**（Status ≥ 4: HR Interview）
2. **收到明确拒绝反馈**（Rejected 且有 HR/业务原因）
3. **用户手动标记为值得研究**（高意向公司 / 关键岗位）

> 投递 100 个，Index 记录 100 行，Case 文件可能只有 15 个。这是设计意图。

## 文件命名

`{Company}_{Role}.md`（用下划线替代空格）

## Case 文件模板

模板实体见同目录 **`XX_case.md`**（单一来源，勿在别处复制结构）。

章节构成：

| 章节 | 内容 | 由谁写 |
|------|------|------|
| Timeline | 关键节点日期 | Mode E3 |
| **Interview Log** | 面试流水（轮次 / 面试官 / 形式 / 时长 / 结果） | 用户（每轮后） |
| **Interview Retro** | 逐轮复盘（原题 / 我的回答 / 追问方向 / 卡壳点 / 改法 / 归因） | 用户（每轮后 24h 内） |
| Feedback | 面试官原文反馈（不加工） | Mode E3 |
| Personal Notes | 个人感受与观察 | 用户 |
| Lessons Learned | 对该方向的反思 | 用户 |

> Interview Retro 的归因与沉淀规则见 `career-dna/13_interview_narrative_strategy.md` Part 9。

## Case 文件由谁创建

- Mode E3 (Add Feedback): Status 变更时自动检查并创建/更新
- Mode E4 (Dashboard): 统计时列出待建档高意向投递
