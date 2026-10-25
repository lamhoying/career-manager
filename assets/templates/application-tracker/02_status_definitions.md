# Status Definitions（状态定义）

> Aligns to: v2.24.0
<!--
统一状态定义。所有 Mode E 操作共用。

流转规则：
- 仅允许正向流转（Analyzed → Planned → Applied → Viewed → Contacted → ...）
- **`Analyzed` 不是「已投」也不是「已备料」** —— 它只表示「分析过，未决定」
- Rejected 和 Withdrawn 为终态，不可再变更
- 用户手动触发状态更新，不自动推测
-->

## Stage -1: Analyzed（已分析 · 未决定）
已完成 JD 分析、留有 `01_jd_match_report.md`，但**尚未决定是否投递**、也**未生成材料**（对应 `resume-outputs/{JD}/` 仅 1 个文件）。
与 `Stage 0` 的区别：**`Planned` = 已备料（有 Pack）**；**`Analyzed` = 只看过（无 Pack）**。
决定不投则**停留在本档**（终态之一，不产生 `Rejected`）。

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
业务部门 / Hiring Manager 面试。

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
Analyzed → Planned → Applied → Viewed → Contacted → HR Interview → Hiring Manager → Final Interview → Offer
 ↘ 任意阶段 → Rejected
 ↘ 任意阶段 → Withdrawn

Analyzed 只在「决定要投」时 → Planned（此时才生成 Pack）；决定不投则停留在 Analyzed。
```

## 建档规则

满足以下条件之一时，在 `archives/` 创建 `{Company}_{Role}.md`：

1. Status ≥ 4: HR Interview（进入面试阶段）
2. Status = Rejected 且有明确反馈原因
3. 用户手动标记为"值得研究"
