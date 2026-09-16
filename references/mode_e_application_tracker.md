# Mode E: Application Tracker（投递追踪模式）

> Aligns to: v2.19.0
## Trigger（触发条件）

用户执行以下任一操作：
- 记录新投递
- 更新投递状态
- 记录面试反馈
- 查看投递统计

## Objective（目标）

记录真实市场反馈。**不自动学习、不自动优化、不反向修改 Career DNA。**

```
v1.x: 我应该怎么投？
v2.0: 我投了以后发生了什么？
```

---

## Preconditions（前置条件）

`application-tracker/01_application_index.md` 必须存在。如不存在，从模板初始化。

---

## E1: Add Application（新增投递）

### 输入

用户提供：公司名 / 岗位 / 行业 / 城市 / 薪资范围 / 期望薪资 / 投递平台。

### 操作

1. 在 `01_application_index.md` 追加一行
2. Status = Applied
3. Last Update = 当前日期
4. **Pack**：若对应 `resume-outputs/{YYYYMMDD}-{company}-{role}/` 目录已存在 → 填相对链接
   （`../resume-outputs/{YYYYMMDD}-{company}-{role}/`）；无包则填 `—`
5. Notes 可选填

### 规则

- 公司 + 岗位 若已存在 → 提示"已记录，是否更新状态？"，不重复添加
- 薪资 / 期望薪资 可选填
- **`Pack` 列与 `resume-outputs/` 目录名必须一致**（`{YYYYMMDD}-{company}-{role}`）——
  不一致说明 pack 目录被改名或尚未生成，须先核对再填

---

## E2: Update Status（更新状态）

### 输入

用户提供：公司 + 岗位（定位已有记录）+ 新状态。

### 操作

1. 在 Index 中定位目标行
2. 更新 Status 列
3. 更新 Last Update 列
4. **不动 `Pack` 列** —— pack 目录不会因投递状态变化而改名

### 规则

- 仅允许正向流转。终态（Rejected / Withdrawn）不可再变
- 若进入 Stage 4 (HR Interview)、Offer，或 Stage 8 (Rejected) → 自动触发 E3 建档检查

---

## E3: Add Feedback（记录反馈）

### 触发条件

- Status 变更为 Rejected 且有反馈原因
- Status 达到 HR Interview 及以上
- 用户手动要求建档

### 操作

1. 若 `archives/{Company}_{Role}.md` 不存在 → 从模板 `assets/templates/application-tracker/archives/XX_case.md` 创建
2. 写入 / 更新 Timeline
3. 追加 Feedback / Personal Notes / Lessons Learned
4. **若本次是面试事件** → 在 `Interview Log` 追加一行（日期 / 轮次 / 面试官 / 形式 / 时长 / 结果），
   并提示用户 **24 小时内**补 `Interview Retro`（复盘四问与归因规则见
   `career-dna/13_interview_narrative_strategy.md` Part 9）
5. **若已进入录用阶段（Offer / 背调）** → 在 `Timeline` 追加录用节点，并把本轮 Offer 结构、
   谈判过程与结果、背调进展记入 `Feedback` / `Personal Notes`。
   谈判原则、背调材料清单与口径要求见 `career-dna/13_interview_narrative_strategy.md` Part 11 ——
   **Mode E 只记录本轮实际发生的事，不复制通用原则**

### 规则

- **Feedback 记录原文，不对反馈做系统推理加工**（v2.1 再做分析）
- Personal Notes 为用户主观感受，与 Feedback 分列
- Lessons Learned 为用户自身反思
- **Interview Log / Interview Retro 只记录事实，不做归因结论** —— 归因分类由用户填写，不由 skill 推断
- **反哺路径（v2.10.0）**：复盘中出现的改进需求（如「同一问题被问了 2 次」「同一卡壳点重复出现」），
  由**用户显式发起 Mode B 承接**，才写回 `13_interview_narrative_strategy.md` 手写区 /
  `05_story_bank.md` / `08_question_backlog.md`。
  **Mode E 自身永不写 `career-dna/`** —— 见 Important Rule 5 与 13 Part 9.5。

---

## E4: Dashboard（投递统计）

### 触发

用户要求"查看投递统计 / 投递面板 / Dashboard"。

### 输出

```
## 投递统计（最近 30 天）

| 阶段 | 数量 |
|------|:--:|
| Applied（已投递） | [N] |
| Viewed（已查看） | [N] |
| Contacted（已联系） | [N] |
| HR Interview | [N] |
| Hiring Manager | [N] |
| Offer | [N] |
| Rejected | [N] |

- 投递→查看转化率: [X]%
- 投递→HR面转化率: [X]%
- 投递→Offer转化率: [X]%

## 待关注
（列出状态停滞超过 5 天 / 高意向但未推进的投递）
```

### 规则

- 默认统计最近 30 天。用户可指定时间范围
- 不统计 Stretch/Weak Fit 包（仅记录应用包类型）

---

## Important Rules（重要规则）

1. **仅记录，不学习**。Index 和 Archives 是原始数据存储，不做反向分析。
2. **反馈原文记录**。不加工成系统结论。v2.1+ 再引入 Feedback Intelligence。
3. **Case 按需建档**。不预先生成空白档案。
4. **状态由用户手动更新**。不自动推测（如 Boss"已读"不自动标记 Viewed）。
5. **不对接 Career DNA**。投递结果不自动修正 Match Score / Track Confidence / Role Authenticity。
   复盘产生的反哺需求**由用户显式发起 Mode B 承接**；Mode E 自身永不写 `career-dna/`。
