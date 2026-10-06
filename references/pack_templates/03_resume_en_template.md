<!-- ============================================================
 模板：03 英文简历（working 版）
 适用：Pack A/B → 落盘 03_resume_en.md（Pack C 用 transition 变体）
 归纳自：[某真实投递包A] / [某真实投递包B] / [某真实投递包C]（结构三版一致：标题英文、中文简历同构）
 生成时机：Mode D Step 9（02 中文定稿后逐节直译 + 语境校准）
 数据来源：02_resume_cn.md（事实与量化逐一对应）+ 03 历史英文简历术语
 内容位职责矩阵：**与 canonical `02` 同源**（v2.23.5 起同批）—— 见 `02_resume_cn_template.md` 头部；
   本模板**只做术语与句式本地化**，不另立规则（禁在此重述矩阵）。
 注意：英文版为中文版的忠实翻译 —— 事实/数字/时间线零漂移；只做术语与句式本地化
============================================================ -->

# {{Name}} — {{Target Role A}} / {{Target Role B}}

<!-- Header comments: reframing rules (E01-E04) + target company/role/date -->

## Professional Summary / Career Positioning

{{EN translation of 职业定位 — same facts, natural EN phrasing}}

<!-- Length (v2.23.5, ADVISORY — non-blocking): ≤ 4 rendered lines (PDF).
     Do NOT restate header fields: City / Target direction live in "Basic Info · Location" + "Target Position" lines.
     Do NOT restate work-history metrics: the summary is a CAPABILITY STATEMENT; figures belong to "Work Experience". -->

## Basic Info

- **Name**: {{Name}}
- **Location**: {{City}}
- **Years of Experience**: {{N}}+ years
- **Languages**: {{Cantonese (native)}} + {{English (certified proficiency, daily cross-border team communication)}} + {{Mandarin}}

## Target Position / Objective

{{JD Role Name EN}} | {{City}} | {{Availability}}
<!-- Rule: objective line = JD role name, NOT 07 positioning -->

## Core Capabilities

{{Capability 1 | Capability 2 | Capability 3 | Capability 4 | Capability 5 | Capability 6}}
<!-- Rule: EN capability names mirror 04b TC names; JD-weighted order; no legacy functional-label as self-tag -->
<!-- Tool annotation (v2.23.5): only when BOTH "JD Explicit emphasis" AND "non-D4 evidence in 04_skill_graph" hold
     may a tool name be parenthesised (e.g. "Performance & Stress Testing (Locust)").
     NEVER annotate a JD-emphasised tool that lacks evidence; the annotation is an INDEX only —
     tools are expanded in "Skills & Certifications · Skills". -->

## Work Experience

### {{Company Full Name}} | {{Actual Job Title}} | {{MMM YYYY – MMM YYYY}}

- {{Company one-liner + project context + reporting line}}
<!-- F47 ② (v2.24.0): the company one-liner MUST be a `- ` bullet — a bare line is hoisted ABOVE every
     company heading in this section (the template renders paragraphs BEFORE entries). -->

- **{{Capability-led subheader [TC00X][D0]}}**: {{description with metrics}}
<!-- One bullet per Capability Interpretation; D0-D1 assertive / D2-D3 transferable tone / D4 omitted -->

### {{Company Full Name}} | {{Actual Job Title}} | {{MMM YYYY – MMM YYYY}}

- {{Cross-industry / career-pivot context if applicable}}

- **{{...}}**: {{...}}

## Key Projects

### {{Project Name}} | {{Project Role}} | {{MMM YYYY – MMM YYYY}}

- **Project Context**: {{three slots (ordered, omittable) — (1) Situation: what it is + stage / scale tier (category / platform / publishing region / delivery form) (2) Constraint: objective hard limits (time zones / compliance review / platform anti-crawling / staffing / parallel windows) (3) Cost: why it is hard / what breaks if missed (JUDGEMENTAL wording, no figures) — subject = the project / environment, NEVER "I"}}
<!-- Three red lines: (1) never restate the `###` heading (name / role / dates) (2) never reuse a metric ALREADY in Work Experience (3) never write "what I did" — the ONLY content slot in this section whose subject is not "I".
     Necessity test: delete the sentence — does "Core Contribution" become unintelligible? If yes keep; if no delete. Length (ADVISORY, non-blocking): <= 3 rendered lines. -->
- **Core Contribution**: {{angle-A clause}}; {{angle-B clause}}
<!-- Single-bullet form: pick the angle(s) first (decision trade-offs / technical difficulty / cross-team blockers), then join clauses with "; ".
     Angle names are NOT printed in the output — their binding force lives in THIS placeholder, so F55 regression protection still holds. -->
- **Outcome**: {{project-unique metrics, or qualitative closure / impact}}  (optional — OMIT if none)
(total **2-3 bullets** = Context 1 + Contribution 1 + Outcome 0-1)
<!-- Rule: pick the 2-3 most TC-relevant projects; capability-led narrative, not a log -->
<!-- Three-label rule (v2.23.5, same source as 02): Context = scope (three slots) / Contribution = decisions (single bullet) / Outcome = impact.
     Iron rule 1 (metrics unique): each metric appears ONCE per resume — never repeat Work Experience figures here (QA-6).
     Iron rule 2 (Outcome gate): Outcome accepts ONLY (1) metrics NOT already in Work Experience, or (2) qualitative closure / impact.
         NEVER relocate Work Experience numbers here. If neither exists, OMIT the label (no filler — "never fabricate" red line).
     Iron rule 3 (layout): ALL items in this section MUST be `- ` bullets — a bare line is bucketed as a paragraph
         and hoisted above every entry in the section (F47 ②). -->

## Education

{{University}} | {{Major}} | {{Bachelor's}} | {{MMM YYYY – MMM YYYY}}（{{honors if any}}）

## Skills & Certifications

- **Skills**: {{JD-weighted skills incl. tools — the ONLY place where tools are expanded; tool names in "Core Capabilities" are indexes only}}
- **Certifications**: {{cert examples; missing cert → "pursuing PMP" phrasing}}
- **Languages**: {{list}}

<!-- ===== QA Layer (EN): same 6 checks as 02 (definition source = mode_d §Step 9.1) — identity drift / capability gap /
     D3 over-packaging / identity regression / capability-tool evidence / cross-section duplication (+ background three-slot) ===== -->
