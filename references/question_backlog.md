# Question Backlog Rules（待补充问题库规则）

## 定位

Question Backlog 是 Career DNA 的长期资产，跨所有模式共享。它记录所有需要用户在未来补充确认的问题，确保信息缺口不被遗忘。

## 来源

Question Backlog 的问题来自所有模式：

| 来源模式 | 典型问题类型 |
|----------|-------------|
| Mode A: Build | 建档时信息不足、项目细节缺失、能力证据不足 |
| Mode B: Update | 更新时发现的新缺口、需要确认的关联信息 |
| Mode C: Review | 分析时发现的能力证据不足、职业方向需确认 |
| Mode D: Job Application | Targeted Discovery 中用户无法立即回答的问题、JD 匹配中的不确定项 |

## 问题格式（v1.4）

每个问题必须包含以下字段：

```markdown
### Q[N]: [问题内容]

- **产生原因**：为什么会产生这个问题
- **关联能力/文件**：与哪个能力或 Career DNA 文件相关
- **关联 Track**：该问题影响哪个 Career Track（如 Project Manager, QA Manager）
- **关联 Gap**：该问题对应 Track 中的哪个 Known Gap（如 CI/CD Integration）
- **关联 Skill**：该问题直接关联的能力名称（如 Test Automation）
- **关联 Hiring Intent**（v1.4）：该问题关联哪类招聘意图（如 Knowledge Transfer / 项目交付）
- **关联 Evidence**（v1.4）：该问题关联哪类证据（如 培训案例 / 交付文档）
- **潜在影响 (Potential Impact)**：High / Medium / Low（回答后对 Track Confidence 的提升幅度预估）
- **优先级**：High / Medium / Low
- **来源模式**：Build / Update / Review / Job Application
- **来源上下文**：（可选）产生该问题的具体场景
- **状态**：Open / Answered / Archived
```

### 字段说明

| 字段 | 版本 | 用途 | 示例 |
|------|------|------|------|
| Track（关联赛道） | v1.3 | 回答此问题对哪个 Career Track 有帮助 | QA Manager |
| Related Gap（关联缺口） | v1.3 | 对应 Track 中哪个 Known Gap | CI/CD Integration |
| Related Skill（关联能力） | v1.3 | 直接关联的能力名称 | CI/CD Pipeline |
| Potential Impact（潜在影响） | v1.3 | 回答后对 Track Confidence 的提升预估 | High（Evidence Count 0→1，Confidence +15） |
| Related Hiring Intent（关联意图） | v1.4 | 关联哪类招聘意图 | Knowledge Transfer |
| Related Evidence（关联证据） | v1.4 | 关联哪类证据类型 | 培训案例 |

**Impact 估算参考**：
- **High**：当前 Evidence Count = 0，回答后从 0→1，Confidence 大幅跃升
- **Medium**：当前 Evidence Count = 1，回答后升级为 2，Confidence 中等提升
- **Low**：补充性信息，不影响 Confidence 的核心评估

## 优先级定义

- **High**：直接影响 Career DNA 核心完整度或当前 JD 匹配度。应尽快补充。
- **Medium**：影响某些模块的完整度或分析准确性。可在方便时补充。
- **Low**：锦上添花的信息。不影响核心功能。

## 状态流转

```
Open → Answered → (可选) Archived
         ↓
      (如回答无效)
      重新设为 Open
```

### Open → Answered（v1.3 增强闭环）
当用户在 Mode B 或 Mode D 中回答了该问题：
1. 将状态改为 Answered
2. 记录回答内容
3. 记录回答时间
4. 标注回答已回写到哪个 Career DNA 文件
5. 确保 Career DNA 对应文件已更新
6. **如果该问题关联了 Track 和 Gap**：同步更新 `10_career_tracks/{track}.md`：
   - 新证据 → 更新 Evidence 表格 + 增量 Confidence
   - Gap 已填补 → 从 Known Gaps 中移除或降级
   - 更新 Improvement Priorities

### Answered → Archived
以下情况可归档：
- 问题已回答且回写完成，不再需要关注
- 问题已过时（如相关项目/岗位已不再相关）
- 问题重复（已有其他问题覆盖了相同信息）

归档时保留原始问题和回答，不删除，方便未来追溯。

## 管理规则

### 规则 1：不删除问题
问题一旦记录，不删除。只改变状态。保留完整历史。

### 规则 2：去重
新增问题时，检查 Backlog 中是否已有相同或相似问题。如有：
- 相同问题：不重复添加
- 相似问题：合并为一个，保留更完整的描述

### 规则 3：定期回顾
每次进入 Mode B 或 Mode D 时，先读取 Backlog：
- 展示当前 Open 状态的问题（按优先级排序）
- 询问用户是否有想回答的问题
- 如用户回答了问题，立即触发回写流程

### 规则 4：跨模式共享
Backlog 中的问题不局限于产生它的模式。例如：
- Mode A 中产生的关于某项目细节的问题，可能在 Mode D 针对特定 JD 时变得高优先级
- Mode D 中发现的能力缺口，可能在 Mode C 职业分析时需要引用

### 规则 5：限制 Open 问题数量
如 Open 状态问题超过 20 个，提醒用户集中处理一部分，避免 Backlog 变成信息垃圾场。

### 规则 6：关联 Track 优先排序（v1.3 新增）
当多个问题 Open 时，按以下逻辑自动排序展示优先级：
1. **第一优先级**：Potential Impact = High 且 Track Confidence < 60 的问题 → 低 Confidence Track 的高 Impact 问题最优先
2. **第二优先级**：Potential Impact = High 的问题 → 能最大化提升 Track Confidence
3. **第三优先级**：Potential Impact = Medium 的问题
4. **第四优先级**：Potential Impact = Low 的问题

**展示时按 Track 分组**，同一 Track 的问题聚合展示，方便用户一次回答同一方向的问题。

**闭环效果**：
```
Track Known Gap → Backlog Question(Track + Gap + Skill + Impact)
                        ↓
                    用户回答
                        ↓
              Track Confidence ↑  |  Known Gaps ↓
```

### 规则 7：JD 绑定生成（JD Binding v1.4.2）

每个从 JD Match Report 产生的 Backlog 问题，必须绑定触发它的 JD 上下文，实现溯源。

**生成链路**：
```
Evidence Gap（来自 01_jd_match_report.md Part 5.4 Evidence Risks）
    ↓
转化为 Backlog Question
    ↓
自动绑定 Triggered By JD（触发JD） / Role（触发岗位） / Company（触发公司） / Track（触发赛道）
```

**绑定字段**：

| 字段 | 来源 | 示例 |
|------|------|------|
| Triggered By JD（触发JD） | 当前 `resume-outputs/{YYYYMMDD}-{company}-{role}/` 目录名 | 20260720-Tencent-pm |
| Triggered By Role（触发岗位） | JD Match Report Part 2 Role 字段 | Implementation Consultant |
| Triggered By Company（触发公司） | JD Match Report Part 2 Company 字段 | Tencent |
| Triggered By Track（触发赛道） | JD Match Report Part 2 Track 字段 | Consultant |

**作用**：
- **同 Track 聚合**：Backlog 展示时按 Track 分组 → 用户可一次性回答同一方向的问题
- **公司优先级排序**：重复出现的 JD 公司优先展示（高频 JD 的 Gap 更紧急）
- **数据溯源**：未来 v1.5 可追踪「哪份 JD 暴露了最多的能力缺口」
- **职业成长任务池**：将 Backlog 从"随机问题池"转化为"按 JD 需求排序的职业成长任务池"

## 文件位置

Question Backlog 存放在 `career-dna/08_question_backlog.md`。

所有模式在需要时读取此文件。Mode B 和 Mode D 更新此文件后，需向用户展示更新后的 Backlog 摘要。
