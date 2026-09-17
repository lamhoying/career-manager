#!/usr/bin/env python3
"""
validate_career_dna.py - Career DNA 写入闸门（Write Gate）

对照 assets/career_dna_manifest.json（Career DNA 文件清单唯一定义源）
校验 career-dna/ 目录，检出污染 SSOT 的行为：

  P0  orphan              根目录出现未登记文件 —— 典型污染，如某次提问随手生成的策略稿
  P0  duplicate-content   跨文件出现长段落逐字重复 —— 双份维护漂移源
  P1  missing             manifest 声明但文件缺失
  P1  unregistered-dir    根目录出现未登记子目录
  P1  derived-part-drift  分区文件（regeneration.mode=partial）的派生区/手写区标题缺失
                          —— 典型事故：自动刷新把「手写区」整段吃掉，肉眼发现不了
  P1  undeclared-part     分区文件里出现 manifest 未声明的 Part
                          —— 与 derived-part-drift 构成双向护栏：一个防「丢」，一个防「偷偷加」
  P2  no-timestamp        派生资产（kind=derived）缺少生成时间戳
  P2  unresolved-anchor   文中的「NN_xxx.md」引用指向一个不存在也没登记的文件 —— 悬空证据指针
  P2  ghost-file-ref      文中的「路径形态 .md 引用」（无 NN_ 数字前缀 / 变量化路径）指向不存在的文件
                          —— 与 unresolved-anchor 互补：后者只认 NN_ 前缀家族，
                             本规则覆盖 `{track}_strategy.md` 这类「变量化路径」幽灵引用
  P2  stale-rule-ref      引用了真源（online_profile_generation.md）已不存在的规则编号
                          —— 典型事故：真源在 v2.7 重编号（R04+R08→R03 等），下游仍写旧号，
                             生成器找不到该规则 → 规则没有进入执行链，退化为模型默认行为
  P2  track-constraint-coverage
                          04b 中每个 TC 的 Position Constraint 段内「赛道条目数」
                          与 `10_career_tracks/` 实有赛道数不一致
                          —— 把模板里的「目录驱动」规则升级为可执行闸门
  P2  role-snapshot-schema knowledge/role_snapshots/ 的结构契约被破坏：
                          ① 段完整性（实例须含模板 8 段）
                          ② Track 取值真实性（受控取值须指向真实存在的赛道文件，或 none）
                          ③ 别名冲突（同一别名出现在 >1 个快照）
                          ④ Observed Companies 受控格式（公司名可解析 —— 「新赛道发现」判据的唯一输入）
                          —— knowledge/ 是唯一「无闸门、无索引、无生命周期」的增长型资产，
                             此前 Track 写成散文 → 人/脚本都归不了组
  P2  identity-layer-schema `07_career_identity.md` 的层契约被破坏：
                          ① 层完整性（5 层标题须齐）
                          ② Layer 2 非空（模板占位 / `[待声明]` ⇒ 未完成声明）
                          ③ Layer 2 的 Track 标注取值 ∈ 赛道文件名 ∪ {none}
                          ④ Layer 5 的收录标注取值 ∈ 本文 Layer 2 条目名 ∪ {none}
                          ⑤ Layer 4 引用的 TC 编号必须存在于 04b
                          —— 07 此前**无任何闸门覆盖**（本脚本 13 项校验均不碰它），
                             而它是全系统唯一「自由声明 + 无来源约束」的字段；
                             Layer 2 空值会让 Mode D / Online Profile 的硬身份锚点无兜底降级
  P2  write-target-drift  「写入 01 报告 Part N」类落点声明指向 canonical 不存在的章节
                          —— 01 报告的 Part 骨架会随版本演进（如 Part 4.5 已合并进 Part 4），
                             但下游「写入 X Part N」的声明不会自动跟着改 → 落点悬空：
                             生成时写进不存在的节，或静默丢字段（A3 类 bug 的机械化捕获）
                          —— 只覆盖**显式写了 01 目标文档 + 写入类动词**的声明；「依据 01 Part N」
                             这类**读取引用**不在本规则内（它是 read-ref，不是落点）

本脚本 **只报告、绝不修改任何文件**。裁决与处置由调用方（AI/用户）执行：
  - orphan / unregistered-dir → 移入 career-dna/_inbox/（草稿区）或走 manifest 登记
  - duplicate-content        → 指定 SSOT 归属方，另一方改为指针
  - derived-part-drift       → 从模板重建缺失分区（手写区有内容时须先抢救）
  - undeclared-part          → 补登记到 manifest 的 regeneration.*_parts，或删掉该 Part
  - ghost-file-ref           → 改正引用路径，或按登记流程真实创建该文件
  - stale-rule-ref           → 把引用改为真源现行编号（真源 = online_profile_generation.md 的 `### Rule Rxx`）
  - track-constraint-coverage → 按 `10_career_tracks/` 实有赛道，逐条补齐缺失的赛道条目
  - role-snapshot-schema     → 补段（或按模板重建）；Track 改为受控取值（解释移入 Track Note）；
                               别名冲突须人工判定归属，不得两边都留；
                               Observed Companies 只放公司名，说明移入 `（）` 括注（未标注公司写 unknown）
  - identity-layer-schema    → 补层（或按模板重建）；Layer 2 未声明须走 Mode A Step 8 采集协议
                               （**不得代填** —— 违 R01）；Track / 收录标注改受控取值；
                               Layer 4 的 TC 编号回 04b 核对
  - write-target-drift       → 把落点改为 canonical 01 报告的现行章节
                               （真源 = references/pack_templates/01_jd_match_report_template.md 的标题骨架）

退出码：存在 P0/P1 → 1；仅有 P2 或无问题 → 0。

Usage:
    python3 validate_career_dna.py [career-dna_directory]
    python3 validate_career_dna.py            # 默认 ./career-dna
"""

import json
import re
import sys
from pathlib import Path

MANIFEST_REL = Path("assets") / "career_dna_manifest.json"

# 视为"长段落"的最小字符数（归一化后）——低于此长度的重复多属通用措辞，不报
DUPLICATE_MIN_CHARS = 80

TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
TIMESTAMP_KEYS = (
    "Last Generated",
    "Last Updated",
    "生成时间",
    "最近生成",
    "Source Files Version",
    "源文件版本",
)

# 分区文件的 Part 标题（## Part 3: xxx / ## Part 3 xxx）
PART_HEADING_RE = re.compile(r"^#{2,3}\s*Part\s+(\d+)\b", re.MULTILINE)

# 文内引用到的 career-dna 风格文件名（NN_xxx.md / NNx_xxx.md）
ANCHOR_RE = re.compile(r"(?<![\w/.-])(\d{2}[a-z]?_[A-Za-z0-9_]+\.md)")

# 单次投递产物（resume-outputs/{JD}/ 下）的固定文件名 —— 被 04/05/01 等正文正常引用，
# 不属于 career-dna 悬空锚点，检出时跳过。
JD_OUTPUT_NAMES = frozenset(
    {
        "01_jd_match_report.md",
        "02_ats_resume.md",
        "02_resume_cn.md",
        "03_boss_resume.md",
        "03_resume_en.md",
        "04_gap_analysis.md",
        "04_interview_pack.md",
        "05_answer_cards.md",
        "06_upgrade_plan.md",
        "07_boss_greeting.md",
    }
)

# ---- P2 ghost-file-ref 相关 ----
# 反引号内的「路径形态 .md 引用」。ANCHOR_RE 只认 NN_ 数字前缀家族，变量化路径
# （如 `{track}_strategy.md`）天然逃逸；本规则覆盖这一类幽灵引用。
GHOST_REF_RE = re.compile(r"`([^`\n]*\.md)`")

# 这些前缀指向 career-dna/ 之外的资产（skill 自带目录、单次投递产物），不参与本规则
GHOST_SKIP_PREFIXES = (
    "resume-outputs/",
    "assets/",
    "knowledge/",
    "references/",
    "scripts/",
    "application-tracker/",
    "http",
)

# 显式白名单：模板名 / 命名模式 / 位于其他目录的固定文件名。
# 与 JD_OUTPUT_NAMES 同级声明 —— 白名单只允许在这里扩，不要在判断逻辑里写特例。
GHOST_REF_WHITELIST = frozenset(
    {
        "README.md",
        "SKILL.md",
        "01_application_index.md",
        "02_status_definitions.md",
        "XX_case.md",
        "XX_portfolio.md",
        "XX_interview_pack.md",
        "XX_answer_cards.md",
        "XX_upgrade_plan.md",
        "XX_gap_analysis.md",
        "XX_transition_resume_cn.md",
        "XX_transition_resume_en.md",
        "XX_transition_feasibility.md",
        "{Company}_{Role}.md",
        "{role_name}.md",
        "{domain_name}.md",
        "{track}.md",
    }
)


# ---- P2 stale-rule-ref 相关 ----
# 规则编号真源 = online_profile_generation.md 的 `### Rule Rxx` 标题集合。
# 引用形态如 R01 / R07 / R01-R07（区间两端各命中一次，均须有效）。
RULE_DEF_RE = re.compile(r"^#{2,4}\s*Rule\s+(R\d+)", re.MULTILINE)
RULE_REF_RE = re.compile(r"(?<![A-Za-z0-9])R(?:0[1-9]|1[0-9])(?![0-9])")


# ---- P2 track-constraint-coverage 相关 ----
# 04b 的「Position Constraint」段：每个 TC 一段，段内按赛道逐条列「定位 / 禁止 / 推荐」。
# 判据：段内赛道条目数 == career-dna/10_career_tracks/ 下 .md 文件数（不含 README）。
POSITION_SECTION_RE = re.compile(r"^#{3,5}\s*Position Constraint\b", re.MULTILINE)
ANY_HEADING_RE = re.compile(r"^#{1,5}\s+\S")
BOLD_LABEL_RE = re.compile(r"^\s*\*\*(?P<label>[^*]+?)\*\*\s*(?P<rest>.*)$")
FIELD_LABEL_RE = re.compile(r"^\s*[:：]?\s*(定位|Position)\s*[:：]")
FIELD_ONLY_RE = re.compile(r"^\s*[:：]?\s*$")


# ---- P2 role-snapshot-schema 相关 ----
# knowledge/role_snapshots/ 是市场情报层（非 Career DNA SSOT），此前无任何闸门覆盖。
# 段清单 = assets/templates/knowledge/role_snapshot.md 的 H2 集合（模板为真源）。
ROLE_SNAPSHOT_SEGMENTS = (
    "Role Capability Model",
    "Hiring Intelligence",
    "JD 观察记录",
    "能力频率统计",
    "公司分布",
    "Persona Statistics",
    "Common Capability Transitions",
    "Trend Intelligence",
)

# 迁移白名单：建于模板升级之前（2026-07-20 ~ 09-02）的旧实例，段标题未齐属已知历史缺口。
# 采用「先上闸门、后补数据」——若先把数据补齐再上闸门，缺口将永远不被记录。
# 随下次 JD 观察自然补齐后，从此名单移除（白名单只允许收缩）。
ROLE_SNAPSHOT_MIGRATION_WHITELIST = frozenset(
    {
        "art_project_manager.md",
        "crm_implementation_consultant.md",
        "it_business_partner.md",
        "presales_technical_pm.md",
        "scrum_master.md",
        "studio_game_pm.md",
    }
)

RS_TRACK_RE = re.compile(r"^- \*\*Track（职业赛道）\*\*:\s*(.+?)\s*$", re.MULTILINE)
RS_ALIAS_RE = re.compile(r"^- \*\*Aliases（别名）\*\*:\s*(.+?)\s*$", re.MULTILINE)
RS_COMPANIES_RE = re.compile(r"^- \*\*Observed Companies（已观察公司）\*\*:\s*(.+?)\s*$", re.MULTILINE)

# ④ Observed Companies 受控格式（v2.17.0）
# 为什么需要：该字段解析出的「不同公司数」是「新赛道发现」判据的**唯一输入**
# （mode_d §Step 10 C 第 7 条）。一旦写成自由文本，计数会**静默失真** ——
# 最危险的不是报错，而是把说明平铺成 ` · ` 串后**凭空多出一家公司**，从而误触发新赛道发现。
# 可判定范围（诚实的边界）：本项只覆盖「把说明平铺进公司名」的可判定形态
# （token 内含 `：，/；,` 等散文标点，或长度超出公司名常理）；
# `名A · 名B` 与 `公司名 · 业务线名` 在格式上不可区分，只能靠规则文本约束，不在闸门判定内。
RS_COMPANY_SPLIT_RE = re.compile(r"[·+、]")
RS_COMPANY_PAREN_RE = re.compile(r"（[^）]*）|\([^)]*\)")
COMPANY_TOKEN_MAX_LEN = 20
COMPANY_TOKEN_BAD_CHARS = ("：", "，", "/", "；", ",")


# ---- P2 write-target-drift 相关 ----
# 「写入 01 报告 Part N」类**落点声明**的可判定子集（语义检查 L1：固定句式的机械化）。
# 唯一定义源 = references/pack_templates/01_jd_match_report_template.md 的标题骨架；
# `## Part N` 为顶层节，`### N.M` 为子节。
# 边界（诚实的范围）：只在**同一行**内做「目标文档 + 邻接 Part」的邻接匹配，且要求写入类动词。
# 之所以要「邻接」而非「同行」：一行里可能同时出现**别的文档**的 Part
# （如 `Part 10（反向尽调）… 落 `01` Part 2.2`），同行即判定会把 `Part 10` 误判成 01 的节。
REPORT01_TEMPLATE_REL = Path("references") / "pack_templates" / "01_jd_match_report_template.md"
WRITE_VERB_RE = re.compile(r"写入|写到|落到|落\s|输出到|归入|记入|写进")
REPORT01_TARGET_RE = re.compile(
    r"(?<![\dA-Za-z])01(?:_jd_match_report(?:\.md)?)?(?![\d])|JD\s*Match\s*Report"
)
PART_REF_RE = re.compile(r"Part\s+(\d+)(?:\.(\d+))?")
# 01 目标与 Part 之间允许的「间隔」：仅标记符/空白，且有长度上限
PART_REF_GAP_RE = re.compile(r"^[\s`*:：>_\-—（）()【】\[\]]*$")
PART_REF_GAP_MAX = 14
# ---- P2 identity-layer-schema 相关 ----
# 07_career_identity.md 此前无任何闸门覆盖（13 项校验均不检查它）。
# 本项覆盖可机械化的五类：层完整性 / Layer 2 非空 / Track 取值 / 收录标注引用 / TC 编号存在性。
IDENTITY_LAYERS = (
    "Layer 1: Professional Identity",
    "Layer 2: Career Positioning",
    "Layer 3: Career Narrative",
    "Layer 4: Capability Priority",
    "Layer 5: Non-Positioning Statement",
)
ID_TRACK_RE = re.compile(r"（Track:\s*(.+?)\s*）")
ID_LISTED_RE = re.compile(r"（收录于 Layer 2:\s*(.+?)\s*）")
ID_TC_RE = re.compile(r"(?<![A-Za-z0-9])TC(\d{3})(?![0-9])")
# 未填写的模板占位（`[赛道文件名 | none]` 等）不报「取值非法」——由 Layer 2 非空检查统一报。
ID_PLACEHOLDER_PREFIX = ("[", "{", "<")


def _extract_layer2_names(body: str) -> set:
    """Layer 2 条目名 = `## Layer 2` 段落内，每条定位在 `—` / `（` 之前的英文主名。

    边界（诚实的范围）：只取 Layer 2 段内、非注释 / 非表格 / 非加粗小标题的行；
    模板占位（以 `[` 开头）不计入。
    """
    names = set()
    in_l2 = False
    in_comment = False
    for raw in body.split("\n"):
        s = raw.strip()
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            if "-->" not in s:
                in_comment = True
            continue
        if s.startswith("## "):
            in_l2 = s.startswith("## Layer 2")
            continue
        if not in_l2 or not s:
            continue
        if s.startswith(("-->", "**", ">", "|", "- [")):
            continue
        if s.startswith("- "):
            s = s[2:]
        name = re.split(r"\s*[—（(]", s)[0].strip().strip("`*")
        if name and not name.startswith("[") and len(name) < 60:
            names.add(name)
    return names


PART_TOP_RE = re.compile(r"^##\s*Part\s+(\d+)\b", re.MULTILINE)
PART_SUB_RE = re.compile(r"^###\s*(\d+)\.(\d+)\b", re.MULTILINE)


def _is_rule_provenance(line: str) -> bool:
    """溯源注记（「（v2.7 合并 R02+R03）」「原 R04 + R08」）记录的是历史编号，跳过。"""
    return "合并" in line or re.search(r"原\s*R", line) is not None


def _ghost_ref_exists(ref: str, base: Path, declared) -> bool:
    """判断一条路径形态引用是否「有真实落点」。

    `{...}` 变量段**不用通配匹配** —— 通配会把 `{track}_strategy.md` 误认成
    「`13_interview_narrative_strategy.md` 存在」（后者确实以 `_strategy.md` 结尾），
    从而把幽灵引用洗白。改为：变量化引用必须带目录（如 `10_career_tracks/{track}.md`），
    且该目录在 career-dna/ 下真实存在；不带目录的变量化引用一律视为可疑。
    """
    if ref in GHOST_REF_WHITELIST or ref in JD_OUTPUT_NAMES or ref in declared:
        return True
    if any(ref.startswith(p) for p in GHOST_SKIP_PREFIXES) or "://" in ref:
        return True
    rel = ref[2:] if ref.startswith("./") else ref
    if rel.startswith("career-dna/"):
        rel = rel[len("career-dna/") :]
    if "{" in rel:
        parent = rel.rsplit("/", 1)[0] if "/" in rel else ""
        return bool(parent) and (base / parent).is_dir()
    return (base / rel).exists()


def _count_track_entries(section_lines) -> int:
    """统计一个 Position Constraint 段内的「赛道条目」数。

    兼容两种实际并存的书写格式：
      - 多行式：`**[Track A]**:` 独占一行，随后若干行 `定位: / 禁止: / 推荐:`
      - 单行式：`**游戏技术 PM**：定位: … / 禁止: … / 推荐: …`
    只计赛道条目标签行，不计段标题、注释行与字段行。
    """
    count = 0
    for idx, line in enumerate(section_lines):
        if line.lstrip().startswith("<!--"):
            continue
        m = BOLD_LABEL_RE.match(line)
        if not m:
            continue
        label = m.group("label").strip()
        if label.startswith("[") and label.endswith("]"):
            label = label[1:-1].strip()
        if not label or FIELD_LABEL_RE.match(label):
            continue
        rest = m.group("rest")
        if FIELD_LABEL_RE.match(rest):      # 单行式：标签后直接跟「定位:」
            count += 1
            continue
        if FIELD_ONLY_RE.match(rest):       # 多行式：标签独占行 → 向后 3 行内须有「定位」
            ahead = section_lines[idx + 1 : idx + 4]
            if any(FIELD_LABEL_RE.match(x) for x in ahead):
                count += 1
    return count


def _report01_part_refs(line: str):
    """抽出「01 目标 + 邻接 Part N」的落点引用（返回 re.Match 列表）。

    邻接规则见 PART_REF_GAP_RE / PART_REF_GAP_MAX 的常量注释：
    同一 01 目标之后**紧跟**（间隔只含标记符）的第一个 `Part N` 才算该目标的落点。
    """
    out = []
    for target in REPORT01_TARGET_RE.finditer(line):
        start = target.end()
        for m in PART_REF_RE.finditer(line, start):
            gap = line[start : m.start()]
            if len(gap) <= PART_REF_GAP_MAX and PART_REF_GAP_RE.match(gap):
                out.append(m)
            break
    return out


def find_manifest() -> Path:
    """定位 career_dna_manifest.json（Career DNA 文件清单唯一定义源）。"""
    script_dir = Path(__file__).resolve().parent
    candidates = (script_dir.parent / MANIFEST_REL, script_dir / MANIFEST_REL)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    tried = "\n".join(f"           {c}" for c in candidates)
    raise SystemExit(
        "❌ 找不到 career_dna_manifest.json（Career DNA 文件清单唯一定义源）。\n"
        f"   已尝试:\n{tried}\n"
        "   请确认本脚本位于 skill 的 scripts/ 目录内，且 assets/ 未被删除。"
    )


def normalize_line(line: str) -> str:
    """归一化一行，用于跨文件重复检测（去掉引用符/列表符/强调符与所有空白）。"""
    s = line.strip()
    s = re.sub(r"^[>\-*+\d\.\)\s]+", "", s)
    s = s.replace("*", "").replace("`", "").replace("_", "")
    s = re.sub(r"\s+", "", s)
    return s


def collect_long_lines(path: Path):
    """收集单个文件中的长段落行：(归一化文本, 原始行号, 原文预览)。"""
    out = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return out
    for lineno, raw in enumerate(text.split("\n"), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("|"):  # 跳过空行与表格行
            continue
        if stripped.startswith("<!--") or stripped.startswith("-->"):
            continue
        norm = normalize_line(stripped)
        if len(norm) >= DUPLICATE_MIN_CHARS:
            out.append((norm, lineno, stripped[:70]))
    return out


def validate(career_dna_dir: str = "./career-dna"):
    base = Path(career_dna_dir).resolve()
    findings = []  # (level, code, name, message)

    if not base.exists():
        print(f"❌ 目录不存在: {base}")
        print("   请先运行 init_career_dna.py 初始化 Career DNA。")
        return None

    manifest = json.loads(find_manifest().read_text(encoding="utf-8"))
    entries = manifest["ssot_files"]
    declared = {e["filename"]: e for e in entries}
    draft_markers = tuple(manifest.get("draft_markers", ["_"]))
    ignored = set(manifest.get("ignored_names", []))

    print("=" * 66)
    print("  Career DNA 写入校验（Validate Write Gate）")
    print(f"  目录: {base}")
    print(f"  定义源: {find_manifest()}")
    print("=" * 66)

    # ---- P0/P1: 根目录条目对照 manifest ----
    present = {}
    for child in sorted(base.iterdir(), key=lambda p: p.name):
        name = child.name
        if name in ignored or name.startswith("."):
            continue
        if name.startswith(draft_markers):
            continue  # 草稿区：非 SSOT，允许存在
        present[name] = child
        if name not in declared:
            level = "P0"
            code = "unregistered-dir" if child.is_dir() else "orphan"
            findings.append(
                (level, code, name, f"{'目录' if child.is_dir() else '文件'}未在 manifest 登记")
            )

    for name, entry in declared.items():
        if name not in present:
            findings.append(("P1", "missing", name, "manifest 已声明但实际缺失"))

    # ---- P0: 跨文件长段落重复（双份维护漂移） ----
    occurrences = {}
    for name, child in present.items():
        if child.is_dir() or child.suffix != ".md":
            continue
        for norm, lineno, preview in collect_long_lines(child):
            occurrences.setdefault(norm, []).append((name, lineno, preview))

    for norm, hits in occurrences.items():
        files = {h[0] for h in hits}
        if len(files) > 1:
            detail = " / ".join(f"{n}:L{ln}" for n, ln, _ in hits)
            findings.append(
                (
                    "P0",
                    "duplicate-content",
                    norm[:40],
                    f"同一长段落出现在 {len(files)} 个文件 → {detail}",
                )
            )

    # ---- P2: 派生资产时间戳 ----
    for name, entry in declared.items():
        if entry.get("kind") != "derived":
            continue
        child = present.get(name)
        if child is None or child.is_dir():
            continue
        try:
            head = child.read_text(encoding="utf-8")[:2000]
        except Exception:
            continue
        if not (TIMESTAMP_RE.search(head) or any(k in head for k in TIMESTAMP_KEYS)):
            findings.append(
                ("P2", "no-timestamp", name, "派生资产缺少生成时间戳 / 源文件版本标注")
            )

    # ---- P1: 分区文件（derived + authored）标题完整性 ----
    # 针对"自动刷新把用户手写区分区整段吃掉"这一类事故 —— 肉眼是发现不了的。
    for name, entry in declared.items():
        regen = entry.get("regeneration") or {}
        if regen.get("mode") != "partial":
            continue
        child = present.get(name)
        if child is None or child.is_dir():
            continue
        declared_parts = list(regen.get("derived_parts", [])) + list(
            regen.get("authored_parts", [])
        )
        if not declared_parts:
            continue
        try:
            body = child.read_text(encoding="utf-8")
        except Exception:
            continue
        found = {int(m) for m in PART_HEADING_RE.findall(body)}
        missing = []
        for label in declared_parts:
            m = re.search(r"(\d+)", str(label))
            if m and int(m.group(1)) not in found:
                missing.append(str(label))
        if missing:
            findings.append(
                (
                    "P1",
                    "derived-part-drift",
                    name,
                    f"分区标题缺失: {' / '.join(missing)}"
                    f"（实见 Part {sorted(found)}）—— 手写区可能被自动刷新覆盖",
                )
            )

    # ---- P1: 反向护栏 —— 文中多出 manifest 未声明的 Part ----
    # derived-part-drift 是单向的（manifest → 文件，查「声明的 Part 有没有丢」）。
    # 这里补反向：文件里出现未声明的 Part —— 「新增 Part 忘记登记」对原闸门完全不可见。
    for name, entry in declared.items():
        regen = entry.get("regeneration") or {}
        if regen.get("mode") != "partial":
            continue
        child = present.get(name)
        if child is None or child.is_dir():
            continue
        declared_nums = set()
        for label in list(regen.get("derived_parts", [])) + list(
            regen.get("authored_parts", [])
        ):
            m = re.search(r"(\d+)", str(label))
            if m:
                declared_nums.add(int(m.group(1)))
        if not declared_nums:
            continue
        try:
            body = child.read_text(encoding="utf-8")
        except Exception:
            continue
        found = {int(m) for m in PART_HEADING_RE.findall(body)}
        undeclared = sorted(found - declared_nums)
        if undeclared:
            findings.append(
                (
                    "P1",
                    "undeclared-part",
                    name,
                    f"出现未声明的 Part: {undeclared}"
                    f"（manifest 已声明 Part {sorted(declared_nums)}）"
                    f" —— 新增 Part 必须同步登记 manifest",
                )
            )

    # ---- P2: 悬空锚点（引用了既不存在也没登记的文件） ----
    for name, child in present.items():
        if child.is_dir() or child.suffix != ".md":
            continue
        try:
            body = child.read_text(encoding="utf-8")
        except Exception:
            continue
        seen = set()
        for ref in ANCHOR_RE.findall(body):
            if ref in seen or ref == name:
                continue
            seen.add(ref)
            if ref in JD_OUTPUT_NAMES or ref in declared or (base / ref).exists():
                continue
            findings.append(
                ("P2", "unresolved-anchor", name, f"引用了不存在的文件 → {ref}")
            )

    # ---- P2: 幽灵文件引用（非 NN_ 前缀 / 变量化路径的 .md 引用） ----
    # 与 unresolved-anchor 互补：后者只认 NN_xxx.md；本规则覆盖 `{track}_strategy.md`
    # 这类「变量化路径」。扫描范围 = career-dna/ 根目录文件 + skill 自带的 assets/templates/
    # （模板是 career-dna 文件的种子，其指针必须是真实的）。两类引用都按 career-dna 根解析。
    ghost_targets = list(present.items())
    templates_root = Path(__file__).resolve().parent.parent / "assets" / "templates"
    if templates_root.is_dir():
        for tpl in sorted(templates_root.rglob("*.md")):
            ghost_targets.append((tpl.name, tpl))

    for name, path in ghost_targets:
        if path.is_dir():
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except Exception:
            continue
        seen = set()
        for ref in GHOST_REF_RE.findall(body):
            ref = ref.strip()
            if not ref or ref in seen:
                continue
            seen.add(ref)
            if _ghost_ref_exists(ref, base, declared):
                continue
            findings.append(
                ("P2", "ghost-file-ref", name, f"引用了不存在的文件 → {ref}")
            )

    # ---- P2: 残留规则编号引用（下游引用了真源已废弃的编号） ----
    # 真源 = references/online_profile_generation.md；扫描 references/ + assets/templates/。
    # 因果链：真源重编号 → 下游仍写旧号 → 生成器找不到 → 规则未进入执行链。
    rule_src = (
        Path(__file__).resolve().parent.parent
        / "references"
        / "online_profile_generation.md"
    )
    if rule_src.is_file():
        valid_rules = set(RULE_DEF_RE.findall(rule_src.read_text(encoding="utf-8")))
        rule_targets = []
        refs_root = Path(__file__).resolve().parent.parent / "references"
        if refs_root.is_dir():
            rule_targets += sorted(refs_root.rglob("*.md"))
        if templates_root.is_dir():
            rule_targets += sorted(templates_root.rglob("*.md"))
        for path in rule_targets:
            try:
                body = path.read_text(encoding="utf-8")
            except Exception:
                continue
            seen_rules = set()
            for lineno, line in enumerate(body.split("\n"), 1):
                if _is_rule_provenance(line):
                    continue
                for ref in RULE_REF_RE.findall(line):
                    if ref in valid_rules or ref in seen_rules:
                        continue
                    seen_rules.add(ref)
                    findings.append(
                        (
                            "P2",
                            "stale-rule-ref",
                            path.name,
                            f"第 {lineno} 行引用了真源不存在的规则编号 → {ref}",
                        )
                    )

    # ---- P2: 01 报告落点漂移（「写入 01 Part N」指向 canonical 不存在的章节） ----
    # 真源 = pack_templates 的 01 报告模板标题骨架。缺失即报错，不回落（与 manifest 同规）。
    tpl01 = Path(__file__).resolve().parent.parent / REPORT01_TEMPLATE_REL
    if not tpl01.is_file():
        findings.append(
            (
                "P2",
                "write-target-drift",
                str(REPORT01_TEMPLATE_REL),
                "找不到 canonical 01 报告模板（唯一定义源缺失）→ 无法校验落点，不回落",
            )
        )
    else:
        skeleton = tpl01.read_text(encoding="utf-8")
        top_parts = {int(n) for n in PART_TOP_RE.findall(skeleton)}
        sub_parts = {f"{a}.{b}" for a, b in PART_SUB_RE.findall(skeleton)}
        drift_targets = []
        drift_root = Path(__file__).resolve().parent.parent / "references"
        if drift_root.is_dir():
            drift_targets += sorted(drift_root.rglob("*.md"))
        if templates_root.is_dir():
            drift_targets += sorted(templates_root.rglob("*.md"))
        for path in drift_targets:
            try:
                body = path.read_text(encoding="utf-8")
            except Exception:
                continue
            seen_drift = set()
            for lineno, line in enumerate(body.split("\n"), 1):
                if not WRITE_VERB_RE.search(line):
                    continue
                for m in _report01_part_refs(line):
                    major, minor = m.group(1), m.group(2)
                    key = f"{major}.{minor}" if minor else None
                    ok = key in sub_parts if key else int(major) in top_parts
                    if ok:
                        continue
                    token = f"Part {major}" + (f".{minor}" if minor else "")
                    if token in seen_drift:
                        continue
                    seen_drift.add(token)
                    findings.append(
                        (
                            "P2",
                            "write-target-drift",
                            path.name,
                            f"第 {lineno} 行落点「{token}」在 01 报告骨架中不存在"
                            f"（canonical 顶层 Part {sorted(top_parts)}）"
                            " —— 落点漂移，须改指现行章节",
                        )
                    )

    # ---- P2: 04b 赛道覆盖（每 TC 段内赛道条目数 = 实有赛道数） ----
    # 与模板中已写入的「目录驱动」规则同源 —— 把模板注释升级为可执行闸门。
    # 只扫 career-dna/ 根目录文件（模板本身是占位骨架，不参与判定）。
    tracks_dir = base / "10_career_tracks"
    if tracks_dir.is_dir():
        track_files = [
            p
            for p in tracks_dir.glob("*.md")
            if p.is_file() and p.stem.lower() != "readme"
        ]
        track_count = len(track_files)
        if track_count:
            for name, child in present.items():
                if child.is_dir() or child.suffix != ".md":
                    continue
                try:
                    body = child.read_text(encoding="utf-8")
                except Exception:
                    continue
                if "Position Constraint" not in body:
                    continue
                lines = body.split("\n")
                heads = [
                    i for i, l in enumerate(lines) if POSITION_SECTION_RE.match(l)
                ]
                bad = []
                for h in heads:
                    end = len(lines)
                    for j in range(h + 1, len(lines)):
                        if ANY_HEADING_RE.match(lines[j]):
                            end = j
                            break
                    got = _count_track_entries(lines[h + 1 : end])
                    if got != track_count:
                        bad.append(f"L{h + 1}: {got}")
                if bad:
                    findings.append(
                        (
                            "P2",
                            "track-constraint-coverage",
                            name,
                            f"{len(bad)} 个 TC 段的赛道条目数 ≠ 实有赛道 {track_count}"
                            f"（{'; '.join(bad)}）—— 按 `10_career_tracks/` 目录驱动补齐",
                        )
                    )

    # ---- P2: Role Snapshot 结构契约（段完整性 / Track 取值 / 别名冲突） ----
    # 扫 knowledge/role_snapshots/（base 的同级目录）。README 是索引，不是快照，跳过。
    rs_dir = base.parent / "knowledge" / "role_snapshots"
    if rs_dir.is_dir():
        tracks_root = base / "10_career_tracks"
        track_names = set()
        if tracks_root.is_dir():
            track_names = {
                q.stem
                for q in tracks_root.glob("*.md")
                if q.is_file() and q.stem.lower() != "readme"
            }

        alias_owner = {}
        for path in sorted(rs_dir.glob("*.md")):
            if path.stem.lower() == "readme":
                continue
            try:
                body = path.read_text(encoding="utf-8")
            except Exception:
                continue
            problems = []

            # ① 段完整性 —— 旧实例走迁移白名单（已知缺口，不逐日刷屏）
            if path.name not in ROLE_SNAPSHOT_MIGRATION_WHITELIST:
                heads = "\n".join(
                    ln for ln in body.split("\n") if ln.startswith("## ")
                )
                missing = [s for s in ROLE_SNAPSHOT_SEGMENTS if s not in heads]
                if missing:
                    problems.append(f"缺段 {' / '.join(missing)}")

            # ② Track 取值真实性 —— 受控取值：赛道文件名 或 none（解释写 Track Note）
            m_track = RS_TRACK_RE.search(body)
            if not m_track:
                problems.append("缺 Track 字段")
            else:
                val = m_track.group(1).strip().strip("`*").strip()
                if val.lower() != "none" and track_names and val not in track_names:
                    problems.append(
                        f"Track 取值 `{val}` 非法 —— 只允许 "
                        f"{'/'.join(sorted(track_names))} 或 none，解释请写 Track Note"
                    )

            # ④ Observed Companies 受控格式 —— 「新赛道发现」判据的唯一输入
            m_comp = RS_COMPANIES_RE.search(body)
            if not m_comp:
                problems.append("缺 Observed Companies 字段")
            else:
                stripped = RS_COMPANY_PAREN_RE.sub(" ", m_comp.group(1))
                tokens = [
                    t.strip()
                    for t in RS_COMPANY_SPLIT_RE.split(stripped)
                    if t.strip()
                ]
                if not tokens:
                    problems.append("Observed Companies 无可解析公司名（剥离括注后为空）")
                else:
                    bad = [
                        t
                        for t in tokens
                        if len(t) > COMPANY_TOKEN_MAX_LEN
                        or any(c in t for c in COMPANY_TOKEN_BAD_CHARS)
                    ]
                    if bad:
                        problems.append(
                            "Observed Companies 受控格式违规 —— 说明须写 `（）` 括注，"
                            f"不得平铺进公司名（可疑片段: {' | '.join(bad[:3])}）"
                        )

            # ③ 别名冲突 —— 整词比对（子串比对会把「[角色]（[方向] 方向）」
            #    误判为与「[角色]」冲突 → 假阳性）
            m_alias = RS_ALIAS_RE.search(body)
            if m_alias:
                for alias in m_alias.group(1).replace("，", ",").split(","):
                    alias = alias.strip().strip("`* ")
                    if alias:
                        alias_owner.setdefault(alias, set()).add(path.name)

            if problems:
                findings.append(
                    ("P2", "role-snapshot-schema", path.name, "；".join(problems))
                )

        conflicts = []
        for alias, owners in sorted(alias_owner.items()):
            if len(owners) > 1:
                conflicts.append(f"`{alias}`（{' / '.join(sorted(owners))}）")
        if conflicts:
            # 聚合为一条 —— 逐别名报会在近似岗位同时建档时一次产 N 条同码 finding，
            # 噪音大且让 P2 计数虚高（本闸门的既有设计原则：只报「有哪类问题」，不逐条刷屏）。
            findings.append(
                (
                    "P2",
                    "role-snapshot-schema",
                    "aliases",
                    f"{len(conflicts)} 个别名跨快照冲突 → {'；'.join(conflicts)}"
                    " —— 须人工判定归属，不得两边都留",
                )
            )

    # ---- P2: 07 Career Identity 层契约（层完整性 / Layer 2 非空 / 字段取值 / TC 编号） ----
    identity_path = base / "07_career_identity.md"
    if identity_path.is_file():
        try:
            body = identity_path.read_text(encoding="utf-8")
        except Exception:
            body = ""
        problems = []

        # ① 层完整性
        heads = "\n".join(ln for ln in body.split("\n") if ln.startswith("## "))
        missing = [s for s in IDENTITY_LAYERS if s not in heads]
        if missing:
            problems.append(f"缺层 {' / '.join(missing)}")

        # ② Layer 2 非空（未声明 / 待声明）
        if "[待声明]" in body:
            problems.append("Layer 2 含 `[待声明]` —— 未完成声明（见 08_question_backlog）")
        elif "[一句话市场身份" in body or "[定位方向" in body:
            problems.append("Layer 2 仍为模板占位符 —— 未采集（须走 Mode A Step 8 采集协议）")

        # ③（F15）Layer 2 的 Track 取值 ∈ 赛道文件名 ∪ {none}
        tracks_root = base / "10_career_tracks"
        id_track_names = set()
        if tracks_root.is_dir():
            id_track_names = {
                q.stem
                for q in tracks_root.glob("*.md")
                if q.is_file() and q.stem.lower() != "readme"
            }
        for val in ID_TRACK_RE.findall(body):
            v = val.strip()
            if v.startswith(ID_PLACEHOLDER_PREFIX):
                continue
            if v.lower() != "none" and v not in id_track_names:
                problems.append(
                    f"Track 取值 `{v}` 非法 —— 只允许 "
                    f"{'/'.join(sorted(id_track_names)) or '(无赛道文件)'} 或 none"
                )

        # ④（F14）Layer 5 的收录标注 ∈ Layer 2 条目名 ∪ {none}
        l2_names = _extract_layer2_names(body)
        for val in ID_LISTED_RE.findall(body):
            v = val.strip()
            if v.startswith(ID_PLACEHOLDER_PREFIX):
                continue
            if v.lower() != "none" and v not in l2_names:
                problems.append(
                    f"收录标注 `{v}` 悬空 —— 必须是本文 Layer 2 的条目名或 none"
                )

        # ⑤（F10）Layer 4 的 TC 编号必须存在于 04b
        cb = base / "04b_transferable_capabilities.md"
        if cb.is_file():
            try:
                have = {
                    f"TC{m}" for m in ID_TC_RE.findall(cb.read_text(encoding="utf-8"))
                }
            except Exception:
                have = set()
            for m in sorted(set(ID_TC_RE.findall(body))):
                if f"TC{m}" not in have:
                    problems.append(f"Layer 4 引用 `TC{m}` 在 04b 中不存在")

        if problems:
            findings.append(
                ("P2", "identity-layer-schema", identity_path.name, "；".join(problems[:4]))
            )

    # ---- 输出 ----
    order = {"P0": 0, "P1": 1, "P2": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1], f[2]))
    counts = {"P0": 0, "P1": 0, "P2": 0}
    for level, code, name, msg in findings:
        counts[level] += 1

    print()
    if not findings:
        print("✅ 校验通过：career-dna/ 与 manifest 完全一致，无污染。")
    else:
        current = None
        for level, code, name, msg in findings:
            if level != current:
                print(f"── {level} ──")
                current = level
            print(f"  [{code}] {name}")
            print(f"        {msg}")
        print()

    print("-" * 66)
    print(f"  P0 (污染，须处置): {counts['P0']}    P1 (不一致): {counts['P1']}    P2 (建议): {counts['P2']}")
    print(f"  已登记 {len(declared)} 项 / 根目录实见 {len(present)} 项")
    print("-" * 66)

    return findings


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "./career-dna"
    findings = validate(target)
    if findings is None:
        sys.exit(2)
    blocking = [f for f in findings if f[0] in ("P0", "P1")]
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
