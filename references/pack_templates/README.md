# Pack Templates（产出包实体模板）

> Aligns to: v2.19.0
> 解决 mode_d 对产物版式的"虚引用"（报告模板无实体文件）与编号漂移（Boss Greeting 在 Pack A/B 下编号不同）。
> 每个模板 = 该产物的**章节骨架 + 固定表格列头 + 字段占位**。内容填充一律由 Mode D 管线 + Career DNA 驱动，模板只锁版式、不锁内容。

## 模板清单与 Pack 覆盖

| 模板 | 产物类型 | Pack A | Pack B | Pack C/D |
|------|---------|:--:|:--:|:--:|
| `01_jd_match_report_template.md` | JD 匹配报告 | ✅ 01 | ✅ 01 | ✅ 01 |
| `02_resume_cn_template.md` | 中文简历（working） | ✅ 02 | ✅ 02 | transition 变体 |
| `03_resume_en_template.md` | 英文简历（working） | ✅ 03 | ✅ 03 | transition 变体 |
| `04_interview_pack_template.md` | 面试准备包 | ✅ 04 | ✅ 04 | ✅ |
| `05_answer_cards_template.md` | 回答卡片库 | ✅ 05 | ✅ 05 | — |
| `06_gap_analysis_template.md` | 能力差距分析 | — | ✅ 06 | ✅ |
| `07_upgrade_plan_template.md` | 竞争力升级计划 | ✅ 06 | ✅ 07 | ✅ |
| `08_boss_greeting_template.md` | Boss 打招呼语 | ✅ 07 | ✅ 08 | 可选 |

> **编号映射铁律**：`06/07/08` 编号随 Pack 结构滑动——Boss Greeting 在 Pack A = `07_boss_greeting.md`，Pack B = `08_boss_greeting.md`（因 B 多一个 06_gap_analysis）。生成时按 Pack 实际编号落盘，**禁止写死 07**。

## 使用方式（供 Mode D 执行时引用）

1. 定位 Pack 类型（Step 7 Application Strategy Decision 输出 Pack A/B/C/D）
2. 按上表加载对应模板文件
3. 模板中 `{{双花括号}}` 为字段占位，由管线各 Step 输出填充
4. `> 规则` 引用块 = 生成约束（数据来源/禁出项），必须遵守
5. 02/03 简历额外执行 Step 9.0 引擎循环 + Step 9.1 QA Layer

## 版式基线

模板骨架归纳自 [某真实投递包A]（最接近 mode_d v2.7.1 的实例）。历史旧版式（[某真实投递包B]/[某真实投递包C] 式：面试身份框架→高频问题→英文面试）已由现行版式取代（含 Narrative Alignment / Tier A Stories / Q 编号答案卡）。
