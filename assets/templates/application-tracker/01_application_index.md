# Application Tracker（投递追踪表）

> Aligns to: v2.21.0
<!--
v2.0 Application CRM — 只记录真实市场反馈，不自动学习，不自动优化。
快速浏览全部投递状态，类似飞书表格。

字段说明：
- Apply Date: 投递日期 (YYYY-MM-DD)
- Company: 公司名
- Industry: 行业（游戏 / SaaS / 互联网 / 金融 / 制造业 ...）
- Role: 投递岗位
- City: 城市
- Salary: JD 薪资范围
- Expected: 用户期望薪资
- Source: 投递平台（Boss / 猎聘 / 内推 / 官网 / 邮件）
- Status: 当前状态（见 02_status_definitions.md）
- Pack: 该投递的产物目录，相对本文件填 ../resume-outputs/{YYYYMMDD}-{company}-{role}/
        由 Mode D 收尾自动登记；无包（仅分析未生成）填 —
- Last Update: 最近一次状态变更日期（由 Mode E 维护）
- Notes: 备注

Status 语义：Mode D 生成 pack 时登记为 Planned（已备未投）；真实投递后由 Mode E 流转为 Applied 及以后。
-->

| Apply Date | Company | Industry | Role | City | Salary | Expected | Source | Status | Pack | Last Update | Notes |
|------------|---------|----------|------|------|--------|----------|--------|--------|------|-------------|-------|
| [YYYY-MM-DD] | [公司A] | [行业] | [岗位A] | [城市] | [15-30K] | [25K] | Boss | Planned | ../resume-outputs/{YYYYMMDD}-{company}-{role}/ | [YYYY-MM-DD] | — |
| [YYYY-MM-DD] | [公司B] | [行业] | [岗位B] | [城市] | [20-35K] | [28K] | 内推 | Applied | — | [YYYY-MM-DD] | 一面通过 |
| [YYYY-MM-DD] | [公司C] | [行业] | [岗位C] | [城市] | [18-25K] | [20K] | 猎聘 | Rejected | — | [YYYY-MM-DD] | 行业经验不足 |
