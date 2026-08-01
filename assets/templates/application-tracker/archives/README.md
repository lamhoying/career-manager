# Case Archives（投递案例档案 v2.0）

按需建档。在 `01_application_index.md` 中任意投递记录满足以下条件之一时创建。

## 建档条件

1. **进入 HR 面**（Status ≥ 4: HR Interview）
2. **收到明确拒绝反馈**（Rejected 且有 HR/业务原因）
3. **用户手动标记为值得研究**（高意向公司 / 关键岗位）

> 投递 100 个，Index 记录 100 行，Case 文件可能只有 15 个。这是设计意图。

## 文件命名

`{Company}_{Role}.md`（用下划线替代空格）

## Case 文件模板

```markdown
# {Company} — {Role}

## Timeline
- YYYY-MM-DD Applied
- YYYY-MM-DD Viewed
- YYYY-MM-DD HR Interview
- YYYY-MM-DD Rejected

## Feedback
[HR / 面试官的原文反馈。记录原文，不做系统推理加工]

## Personal Notes
[个人面试感受、过程中的观察]

## Lessons Learned
[对该方向的反思。如：需要强化身份叙事、准备某类案例、调整薪资策略等]
```

## Case 文件由谁创建

- Mode E3 (Add Feedback): Status 变更时自动检查并创建/更新
- Mode E4 (Dashboard): 统计时列出待建档高意向投递
