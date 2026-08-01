# Status Definitions（状态定义 v2.0）

<!--
统一状态定义。所有 Mode E 操作共用。

流转规则：
- 仅允许正向流转（Applied → Viewed → Contacted → ...）
- Rejected 和 Withdrawn 为终态，不可再变更
- 用户手动触发状态更新，不自动推测
-->

## Stage 0: Planned（待投）
想投但尚未投递。已评估过匹配度但暂未发送简历或打招呼。

## Stage 1: Applied（已投递）
已发送简历或打招呼消息。

## Stage 2: Viewed（已查看）
HR 已查看简历或消息。仅 Boss、猎聘等可感知"已读"的平台适用。官网投递无需此状态。

## Stage 3: Contacted（已联系）
收到 HR 初步联系——消息回复 / 电话 / 添加微信等。

## Stage 4: HR Interview（HR 面试）
HR 面试进行中或已通过。

## Stage 5: Hiring Manager（业务面试）
业务部门 /  Hiring Manager 面试。

## Stage 6: Final Interview（终面）
终面 / Offer Review 阶段。

## Stage 7: Offer（已获 Offer）
收到正式 Offer。

## Stage 8: Rejected（被拒）
公司方明确拒绝或超过两周无回音视为静默拒绝。需记录拒绝原因（如有反馈）。

## Stage 9: Withdrawn（主动放弃）
用户主动放弃该岗位的流程。

## 状态流转图

```
Planned → Applied → Viewed → Contacted → HR Interview → Hiring Manager → Final Interview → Offer
                       ↘ Contacted → Rejected
                       ↘ 任意阶段 → Withdrawn
```

## 建档规则

满足以下条件之一时，在 `archives/` 创建 `{Company}_{Role}.md`：

1. Status ≥ 4: HR Interview（进入面试阶段）
2. Status = Rejected 且有明确反馈原因
3. 用户手动标记为"值得研究"
