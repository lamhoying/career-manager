#!/usr/bin/env python3
"""
Export Resume Finalization Script (v2.8.1) — HTML 模板驱动架构

流程：
    final.md（净化定稿内容）
        → build_data() 解析为结构化数据（姓名/意向/2×2信息/节/条目）
        → mini_template 渲染 resume_template.html（v1 抽象模板）→ final.html（v2 完整版）
        → HTML → PDF（Platypus，样式从模板 CSS 变量提取）
        → HTML → DOCX（最简转换，效果可接受部分损失）

设计原则（Template-as-Spec）：
    - HTML 模板是「设计源」：用户改模板 CSS/结构 = 改设计，渲染脚本零改动
    - 模板占位符由 scripts/mini_template.py 渲染（{{变量}} / {{#each 列表}}）
    - 渲染引擎支持的结构类（约定）：.header/.photo/.name/.intent/.contact/
      .section/.section-title/.entry/.entry-meta/ul/li/p
    - 颜色/背景/字号/行距从模板 :root CSS 变量提取；--theme 可覆盖（Track 联动）

用法：
    python export_resume.py --input deliverables/02_resume_cn_final.md \
        --template assets/templates/resume-outputs/resume_template.html \
        --format all --photo photo.jpg [--theme blue]
        --format pages          # 只试渲染取页数（不落盘；供 Step 9.6 Portfolio Gate 报数）
"""

import argparse
import base64
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

from mini_template import render as mini_render


# ---------- final.md → 结构化数据 ----------

# 兜底映射 —— **只在「字体确实没有该字形」时才启用**（判定见 _pdf_safe）。
# ⚠️ 这不是主机制，只是最后一层网：
#    主机制 = 字体本身覆盖（scripts/build_cn_font.py 补齐字形 + validate_career_dna.py
#    P2 `pdf-glyph-coverage` 守闸）。因为 reportlab 直绘**无字体回退**，缺字形 = 静默丢字，
#    所以对「连补齐后的字体也没有」的字符，用有字形的近似形式替代，宁可降级也不丢字。
# 历史：v2.23.0 前本表是**无条件**替换（→ 一律变 ->），起因是当时的字体缺这些字形；
#       字体补齐后若仍无条件替换，会出现「明明有真字形却被降级」的假降级 ⇒ v2.23.1 改为覆盖度驱动。
_ARROW_FALLBACK = {
    "\u2192": "->",     # → RIGHTWARDS ARROW
    "\u2190": "<-",     # ← LEFTWARDS ARROW
    "\u2191": "^",      # ↑ UPWARDS ARROW
    "\u2193": "v",      # ↓ DOWNWARDS ARROW
    "\u2194": "<->",    # ↔ LEFT RIGHT ARROW
    "\u21d2": "=>",     # ⇒ RIGHTWARDS DOUBLE ARROW
    "\u21d4": "<=>",    # ⇔ LEFT RIGHT DOUBLE ARROW
    "\u21c4": "<->",    # ⇄ RIGHTWARDS ARROW OVER LEFTWARDS ARROW
    "\u21c5": "^v",     # ⇅ UPWARDS ARROW LEFTWARDS OF DOWNWARDS ARROW
    "\u2713": "\u00b7",  # ✓ CHECK MARK → 中点（有字形）
    "\u2714": "\u00b7",  # ✔ HEAVY CHECK MARK
    "\u2717": "x",      # ✗ BALLOT X
    "\u2718": "x",      # ✘ HEAVY BALLOT X
    "\u2264": "<=",     # ≤
    "\u2265": ">=",     # ≥
    "\u2260": "!=",     # ≠
    "\u2248": "~=",     # ≈
    "\u00b1": "+/-",    # ±
    "\u221a": "sqrt",   # √
    "\u221e": "inf",    # ∞
    "\u2211": "sum",    # ∑
    "\u220f": "prod",   # ∏
    "\u222b": "int",    # ∫
    "\u2208": "in",     # ∈
    "\u2207": "grad",   # ∇
    "\u00d7": "x",      # ×（Latin-1，正常都在字体里；留作极端情况兜底）
    "\u2460": "(1)", "\u2461": "(2)", "\u2462": "(3)", "\u2463": "(4)", "\u2464": "(5)",
    "\u2465": "(6)", "\u2466": "(7)", "\u2467": "(8)", "\u2468": "(9)", "\u2469": "(10)",
    "\u2705": "[OK]",   # ✅
    "\u26a0": "!",      # ⚠
    "\u2139": "(i)",    # ℹ（信息标记）—— 闸门 pdf-glyph-coverage 在案例库查出（v2.23.1）
    "\u274c": "x",      # ❌
}
_FB_KEYS = frozenset(_ARROW_FALLBACK)

# F41（v2.24.0）：惰性字形缺口 —— **按类兜底**（逐键枚举永远滞后于语料）。
#   判据 = 字体无字形 ∧ 显式降级表无项 ∧ 属「符号类」∧ 非真·不可见
#     ⇒ 降级为通用占位（保证 PDF **永不静默丢字**）。
#   ⚠️ **只兜符号类**：字母 / 汉字等非符号类**不擅自替换**（会破坏语义），保持原样并交给
#      P2 `pdf-glyph-coverage` 报警 —— 该闸门**看不见本兜底**（它只读本文件的显式表字面量），
#      故「已兜底」与「仍报警」并存正是设计意图：不丢字 + 让人知道。
_GLYPH_GENERIC_FALLBACK = "\u00b7"                     # 通用降级位（中点，字体有真字形）
_GLYPH_SYMBOL_CATS = frozenset({"So", "Sm", "Sk", "Sc"})
_GLYPH_INVISIBLE_CATS = frozenset({"Cf", "Mn", "Me", "Zl", "Zp", "Zs"})
_GLYPH_CORRUPT_CP = 0xFFFD                              # 数据损坏哨兵 —— 禁兜底（否则掩盖损坏）

# F57（v2.24.0）：==强调== 用的主题色 —— 由 html_to_pdf() 从模板 --accent 注入（不得硬编码色板）。
_CURRENT_ACCENT = "#1564BF"


def _generic_glyph_fallback(ch: str):
    """字体无字形且显式表无项 ⇒ 按类给通用降级；不适用返回 None（= 原样保留）。"""
    if ord(ch) == _GLYPH_CORRUPT_CP:
        return None                                     # 损坏字符：原样交给闸门报 corrupt
    cat = unicodedata.category(ch)
    if cat in _GLYPH_INVISIBLE_CATS:
        return ""                                       # 不可见字符：丢弃无损
    if cat in _GLYPH_SYMBOL_CATS:
        return _GLYPH_GENERIC_FALLBACK
    return None

# 中文字体码位集合缓存：None=未尝试 / False=加载失败（退回整表降级）/ set=已加载
_CN_FONT_CMAP = None
_CN_FONT_CMAP_TRIED = False


def _cn_font_cmap():
    """本 skill 中文字体的实际码位集合（懒加载 + 缓存）。

    返回 set[int]；缺字体文件或缺 fontTools ⇒ 返回 False（调用方退回「整表降级」的保守策略）。
    判据来源是**实测 cmap**，不是硬编码假设 —— 字体补齐后降级自动失效。
    """
    global _CN_FONT_CMAP, _CN_FONT_CMAP_TRIED
    if _CN_FONT_CMAP_TRIED:
        return _CN_FONT_CMAP
    _CN_FONT_CMAP_TRIED = True
    try:
        from fontTools.ttLib import TTFont
        p = (Path(__file__).resolve().parent.parent
             / "assets" / "fonts" / "NotoSansSC-Regular.ttf")
        s = set()
        for tb in TTFont(str(p), lazy=True)["cmap"].tables:
            s |= set(tb.cmap.keys())
        _CN_FONT_CMAP = s
    except Exception:
        _CN_FONT_CMAP = False
    return _CN_FONT_CMAP


def _pdf_safe(s: str) -> str:
    """渲染安全化：**字体没有的**符号才用 ASCII 近似替代（仅 PDF/DOCX 文本出口调用，不落源文件）。

    与 v2.23.0 的行为差异：原先无条件替换（→ 一律变 ->），现在先查字体 cmap ——
    字体有真字形就**原样保留**（→ 仍是 →），只有字体也没有时才降级。
    这样「补字体」与「降级」不会互相抵消（旧写法会让补齐的字形永远用不上）。
    """
    cm = _cn_font_cmap()
    if not cm:                                # 拿不到 cmap ⇒ 保守：整表降级
        for k, v in _ARROW_FALLBACK.items():
            s = s.replace(k, v)
        return s
    if all(ord(ch) in cm for ch in s):
        return s                              # 快路径：全部有真字形
    out = []
    for ch in s:
        if ord(ch) in cm:
            out.append(ch)
            continue
        if ch in _ARROW_FALLBACK:
            out.append(_ARROW_FALLBACK[ch])
            continue
        g = _generic_glyph_fallback(ch)       # F41：按类兜底（符号类 → ·）
        out.append(ch if g is None else g)
    return "".join(out)


def _fmt(s: str) -> str:
    """转义 + **加粗** → <b>；==强调== → <span class="em-accent">（v2.24.0 · F57）。

    ⚠️ **斜体对本项目 CJK 字体无效**（NotoSansSC 无 italic 变体，reportlab 静默忽略 <i>）⇒
       「强调」的唯一可用形态 = **加粗 + 主题色**（实测 reportlab <font color> 与 docx run-level 均支持）。
    """
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"==(.+?)==", r'<span class="em-accent">\1</span>', s)
    return s


def _split_row(row: str):
    """拆分表格行：尊重 \\| 转义，去掉被 | 包裹产生的首尾空单元格。"""
    cells = re.split(r"(?<!\\)\|", row)
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


def _is_sep_row(cells):
    """分隔行判定：形如 |---|:--:|---| ⇒ 各单元格仅由 - : 空格 组成且至少一个 '-'。"""
    return bool(cells) and all(c and set(c) <= set("-: ") and "-" in c for c in cells)


def parse_md(text: str):
    """md → 元素流。原有 5 种 kind 语义不变，新增 3 种 + 注释块跳过：
         ("table", {"head": [...], "rows": [[...]]})   ← 连续 | 行 + 第 2 行是分隔行
         ("code",  {"lang": str, "text": str})         ← ``` 围栏块
         ("hr",    "")                                 ← 独占一行的 ---
         HTML 注释块（<!-- … -->，可跨行）整体跳过，不进入元素流；
         行尾注释（`正文 <!-- 说明 -->`）一并剥离 —— 否则注释文字会混进字段值。
    兼容性：新 kind 对 build_data_resume()（简历）无对应分支 ⇒ 静默忽略；
            注释跳过对既有语料是 no-op（简历定稿 md 实测 0 处注释）。
    """
    elements = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # ---- HTML 注释块（可跨行）：整块跳过 ----
        if line.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1  # 跳过含 --> 的那一行（未闭合时 i 越界，while 自然结束）
            continue
        # ---- 代码围栏 ----
        if line.startswith("```"):
            lang = line[3:].strip()
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # 跳过收尾围栏
            elements.append(("code", {"lang": lang, "text": "\n".join(buf)}))
            continue
        # ---- 表格 ----
        if line.startswith("|"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                buf.append(lines[i].strip())
                i += 1
            rows = [_split_row(r) for r in buf]
            if len(rows) >= 2 and _is_sep_row(rows[1]):
                elements.append(("table", {"head": rows[0], "rows": rows[2:]}))
            else:
                # 非规范表格：逐行退化为正文 —— 不丢内容、不静默吞表
                for r in buf:
                    elements.append(("body", r))
            continue
        # ---- 行尾注释：剥离（否则注释文字混进字段值；如 `**标签**：A ｜ B  <!-- 说明 -->`）----
        if "<!--" in line:
            line = re.sub(r"<!--.*?-->", "", line).strip()
            if not line:
                i += 1
                continue
        # ---- 单行 ----
        if line in ("---", "***", "___"):
            elements.append(("hr", ""))
        elif not line:
            elements.append(("blank", ""))
        elif line.startswith("# "):
            elements.append(("title", line[2:].strip()))
        elif line.startswith("## "):
            elements.append(("heading", line[3:].strip()))
        elif line.startswith("### "):
            elements.append(("meta", line[4:].strip()))
        elif line.startswith("- "):
            elements.append(("bullet", line[2:].strip()))
        elif line.startswith("> "):
            elements.append(("quote", line[2:].strip()))
        else:
            elements.append(("body", line))
        i += 1
    return elements


# 简历 profile 数据构建（原 build_data；v2.23.0 起改名以支持 profile 分派，函数体零改动）
def build_data_resume(md_text: str, photo_path: str = "") -> dict:
    elements = parse_md(md_text)
    data = {"姓名": "", "意向": "", "信息": [], "节": [], "证件照": photo_path or ""}

    # header：title + quotes
    for kind, line in elements:
        if kind == "title":
            data["姓名"] = _fmt(line)
    for kind, line in elements:
        if kind != "quote":
            continue
        if "求职意向" in line:
            data["意向"] = _fmt(line)
        else:
            for seg in re.split(r"[｜|]", line):
                label, _, val = seg.partition("：")
                if label.strip() and val.strip():
                    data["信息"].append({"标签": _fmt(label.strip()), "值": _fmt(val.strip())})

    # sections
    cur = None
    for kind, line in elements:
        if kind == "heading":
            cur = {"标题": _fmt(line), "段落": [], "条目": []}
            data["节"].append(cur)
        elif kind == "meta":
            if cur:
                cur["条目"].append({"meta": _fmt(line), "行": []})
        elif kind == "bullet":
            if cur:
                if cur["条目"]:
                    cur["条目"][-1]["行"].append(_fmt(line))
                else:
                    cur["段落"].append(_fmt(line))
        elif kind == "body":
            if cur:
                if cur["条目"]:
                    # F47 ②（v2.24.0）：**含 meta 的节，正文归入当前条目** —— 否则落入「节段落」，
                    # 而模板先渲段落、再渲条目 ⇒ 正文被**上提到该节全部条目之前**
                    # （公司简介跑到所有公司标题前面 = 典型场景）。不丢内容、不报错，只在渲染后看图才发现。
                    cur["条目"][-1]["行"].append(_fmt(line))
                else:
                    cur["段落"].append(_fmt(line))
    return data


# ---------- 合册 profile：md → 结构化数据 ----------

# 合册模板里「非小节内容」的容器类名（_blocks 递归时跳过，避免重复渲染）
_PORTFOLIO_SKIP_CLS = {"sub-title", "case-title", "facts", "case-quote",
                       "cover-title", "cover-meta",
                       # 刀 B 新增容器：.hero 标题区 / 事实卡 / 目录 / 页脚
                       "hero", "hero-badges", "row", "k", "full",
                       "toc", "toc-title", "toc-row", "footer"}


def _pf_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# F51（v2.24.0）：合册**不支持行内 code** —— 反引号**渲染时剥离、内容原样保留**。
#   契约（09_portfolio_book.md）已明写「三问」；原先反引号被 _pf_escape 原样保留 ⇒ 字面印出。
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


def _pf_inline(s: str) -> str:
    """行内标记：**剥反引号** + **加粗** → <b> + ==强调== → <span class="em-accent">（与 _fmt 同规则）。"""
    s = _INLINE_CODE_RE.sub(r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", _pf_escape(s))
    s = re.sub(r"==(.+?)==", r'<span class="em-accent">\1</span>', s)
    return s


def _pf_block_html(kind, val) -> str:
    """单个元素 → 小节内的 HTML 片段（预渲染：mini_template 无 #if，只能预渲染）。"""
    if kind == "body":
        return f"<p>{_pf_inline(val)}</p>"
    if kind == "table":
        head = "".join(f"<th>{_pf_inline(c)}</th>" for c in val["head"])
        rows = "".join("<tr>" + "".join(f"<td>{_pf_inline(c)}</td>" for c in r) + "</tr>"
                       for r in val["rows"])
        return f'<table class="table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == "code":
        return f'<div class="flow">{_pf_escape(val["text"])}</div>'
    if kind == "hr":
        return ""
    return ""


# ---------- 刀 B 版式工具（合册专用） ----------

_PF_KV_RE = re.compile(r"^\s*(.*?)\s*[:：]\s*(.*)$", re.S)
# 块级标签剥离（事实卡只吃行内内容）—— 消费端防御：md 作者把表格/块写进案例头部也不破 DOM
_PF_BLOCK_TAG_RE = re.compile(
    r"</?(?:p|div|table|thead|tbody|tr|td|th|ul|ol|li|section|h[1-6])(?:\s[^>]*)?>", re.I)
_PF_FACT_LABELS = ("项目", "起止", "角色")


def _pf_kv(seg: str):
    """事实条片段 → (标签, 值)。标签 = 首个冒号之前（剥掉 ** 与 <b> 壳）。

    ⚠️ 仅在「像标签」时才认（≤6 字、无空白、无方括号）——否则 `[XX：项目]` 这类
       值里的冒号会被误判成标签，导致卡片错位。不像标签 ⇒ (None, 原片段)。
    """
    m = _PF_KV_RE.match(seg)
    if not m:
        return None, seg
    key = re.sub(r"</?b>", "", m.group(1)).strip().strip("*").strip()
    if not key or len(key) > 6 or re.search(r"[\s\[\]｜|]", key):
        return None, seg
    return key, m.group(2).strip()


def _pf_split_tags(val: str):
    """标签值 → 列表（支持 ｜ 与 | 分隔）。"""
    return [t.strip() for t in re.split(r"[｜|]", val) if t.strip()]


# F35（v2.24.0 · L2 语义剥离）：封面 `派生自` 字段 —— 印**内部文件路径 + 案例库结构**
#   （`portfolio-outputs/{case}.md @日期`）⇒ 无对外语义，渲染时**整段剥离**。
#   判据 = 「段」的**纯文本**（剥 `**` 与 HTML 标签）以「派生自：」起始。
_PF_DERIVED_FROM_RE = re.compile(r"^(?:\*+)?\s*派生自\s*(?:\*+)?\s*[:：]")


def _pf_plain_text(s: str) -> str:
    """剥 `*` 与 HTML 标签后取纯文本（**仅判定用**，不用于输出）。"""
    return re.sub(r"[*]+", "", re.sub(r"<[^>]+>", "", s or "")).strip()


def _pf_strip_cover_l2(val: str) -> str:
    """F35（v2.24.0 · L2）：剥离封面元信息里的 `派生自` 段。

    处理两种写法：**整行**（`> **派生自**：…`）与**同行分段**（`… ｜ **派生自**：…`）。
    分段式只删**命中段** ⇒ 同行承载的 姓名 / 应聘 **不被连带丢失**（不静默丢内容）。
    返回剥离后的行；整行都是该字段 ⇒ 返回 ""（调用方跳过该行）。
    """
    if not val or "派生自" not in val:
        return val
    segs = re.split(r"\s*[｜|]\s*", val)
    kept = [s for s in segs if not _PF_DERIVED_FROM_RE.match(_pf_plain_text(s))]
    return " ｜ ".join(kept)


def _pf_split_facts(事实条: str):
    """事实条 → (事实卡行, 口径文本)。

    拆分规则（防静默丢内容 · 对齐骨架契约「项目 ｜ 起止 ｜ 角色 ｜ 口径」）：
      · 口径段按标签识别（不按位置）—— 位置决定前 3 段的默认标签
      · 非口径段 < 3 ⇒ **整行降级**为单行卡（原文一字不丢，不硬切）
      · 其余游离片段（刀 A 会把案例头部的 bullet/正文并进事实条）⇒ **中性 full 行**（不丢内容）
      · **F35（v2.24.0 · L2 语义剥离）**：`口径` 段**不进事实卡**；值仍随第二返回值交回调用方
    """
    事实条 = _PF_BLOCK_TAG_RE.sub("", 事实条 or "").strip()
    segs = [s.strip() for s in 事实条.split("｜")]
    pos, kou = [], ""
    for s in segs:
        if not s:
            continue
        k, v = _pf_kv(s)
        if k == "口径":
            kou = v if not kou else (kou + " ｜ " + v)
        else:
            pos.append((k, s, v))
    if len(pos) < 3:
        # F35：降级单行卡改由**非口径段**拼回 ⇒ 口径段（L2）不印，其余一字不丢
        kept = [s for _k, s, _v in pos]
        return ([{"标签": "", "值": " ｜ ".join(kept), "cls": " full"}] if kept else []), kou
    rows = []
    for i, (k, s, v) in enumerate(pos[:3]):
        rows.append({"标签": k or _PF_FACT_LABELS[i],
                     "值": (s if k is None else v), "cls": ""})
    # F35（v2.24.0 · L2）：游离片段（pos[3:]）原**并入「口径」格** ⇒ 现改**中性 full 行**
    #   —— 它们是案例头部并进来的正文 / bullet，属**对外可见事实**，不得跟着 口径 一起被剥掉。
    rest = [s for _k, s, _v in pos[3:]]
    if rest:
        rows.append({"标签": "", "值": " ｜ ".join(rest), "cls": " full"})
    return rows, kou


# ---------- F40：附录区（Appendix） ----------

_PF_APPENDIX_PREFIX = "附录"      # 受控前缀：`## 附录：{名}` ⇒ 归附录桶（规则真源见 references/portfolio_outputs.md §7）


def _pf_is_appendix(val: str) -> bool:
    """标题纯文本是否以受控前缀「附录」起始（F40 · 单一判据源）。"""
    plain = re.sub(r"<[^>]+>", "", val or "").strip()
    return plain.startswith(_PF_APPENDIX_PREFIX)


def _pf_appendix_html(items) -> str:
    """附录区 → HTML（F40）。

    与案例块**同构**（.hero / .facts / .sub），唯一差别 = 外层 `<section class="appendix">`
    ⇒ 由模板 CSS 弱化标题区；**独立桶** ⇒ 不进 `.toc`、不计案例数。
    无附录 ⇒ 返回空串（模板 `{{附录块}}` 处整块不出现）。
    """
    if not items:
        return ""
    out = []
    for c in items:
        buf = ['<section class="appendix">']
        buf.append(f'<div class="hero"><div class="case-title">{c["标题"]}</div>')
        if c["徽章"]:
            buf.append('<div class="hero-badges">')
            buf.extend(f'<span class="badge{b["cls"]}">{b["文本"]}</span>' for b in c["徽章"])
            buf.append("</div>")
        buf.append("</div>")
        if c["事实卡行"]:
            buf.append('<div class="facts">')
            buf.extend(f'<div class="row{r["cls"]}"><span class="k">{r["标签"]}</span>{r["值"]}</div>'
                       for r in c["事实卡行"])
            buf.append("</div>")
        buf.append(c["摘要块"])
        for s in c["小节"]:
            buf.append(f'<div class="sub"><div class="sub-title">{s["标题"]}</div>{s["html"]}</div>')
        buf.append("</section>")
        out.append("".join(buf))
    return "\n".join(out)


def _pf_toc_html(cases) -> str:
    """目录块（刀 B）：案例数 ≥ 2 才渲染；HTML 端**不编造页码**（页码列留格式位）。"""
    if len(cases) < 2:
        return ""
    rows = []
    for c in cases:
        title = re.sub(r"^案例\s*\d+\s*[:：]\s*", "", c["标题"])
        rows.append(f'<div class="toc-row"><span class="tx">{title}</span>'
                    f'<span class="dots"></span><span class="pg">·</span></div>')
    return ('<div class="toc"><div class="toc-title">目录</div>'
            + "".join(rows) + "</div>")


def _pf_footer_html(css, title: str) -> str:
    """页脚块（刀 B）：--footer: none ⇒ 空串（整块不出现）。
    HTML 端只给「格式示意」—— 浏览器无法预知分页，页码的真实值由 PDF/DOCX 侧生成。"""
    mode = ((css or {}).get("--footer", "page-x-of-y") or "").strip()
    if mode == "none":
        return ""
    ph = "第 X 页 / 共 Y 页" if mode == "page-x-of-y" else "第 X 页"
    t = re.sub(r"<[^>]+>", "", title or "")
    return f'<div class="footer"><span>{t}</span><span class="pg">{ph}</span></div>'


# ---------- 刀 D：页眉 / 水印（PDF · DOCX · HTML 三出口同源） ----------
# 文案派生集中在此：三出口各自解析自己的输入（PDF 读 DOM / DOCX 读 DOM / HTML 由 data 供块），
# 但**取字段与拼文案的规则只有这一份** —— 否则三处会各自漂移。

_WM_INTERNAL_MARKERS = re.compile(r"\[内部\]|\[原设计·汇报稿\]")


def _wm_force_draft(text: str) -> bool:
    """披露 fail-safe（刀 D）：残留内部档标记 ⇒ 水印强制 draft。

    判据来源：披露分级 L3 会剥 `[内部]` / `[原设计·汇报稿]`（见 references/portfolio_outputs.md）。
    这两个标记**出现在待渲染文本里** = 「该件含内部档内容」的**可验证信号** ⇒ 按 fail-safe
    拒绝以正式档位（trace）输出。举证责任在「无害」侧（default-open）。
    """
    return bool(_WM_INTERNAL_MARKERS.search(text or ""))


def _pf_cover_field(lines, label: str) -> str:
    """从封面元信息行取「{label}：值」的值（按 ｜ 分段；容忍 **加粗** 与全角冒号）。"""
    for ln in lines or []:
        for seg in re.split(r"[｜|]", ln):
            seg = re.sub(r"\*+", "", seg).strip()
            m = re.match(rf"^{re.escape(label)}\s*[:：]\s*(.*)$", seg)
            if m:
                return m.group(1).strip()
    return ""


def _pf_header_parts(css, lines):
    """页眉文案 (left, right)。left = 姓名（full 档附加「联系」）；right = 「应聘 公司 · 岗位」。

    --header: full 需封面元信息含「联系」行；无该行 ⇒ **静默降级 auto**（只给姓名，不报错）。
    """
    mode = ((css or {}).get("--header", "auto") or "").strip() or "auto"
    name = _pf_cover_field(lines, "姓名")
    if mode == "full":
        contact = _pf_cover_field(lines, "联系")
        left = f"{name} ｜ {contact}" if (name and contact) else name
    else:
        left = name
    comp = _pf_cover_field(lines, "应聘")
    return left, (f"应聘 {comp}" if comp else "")


def _pf_watermark_text(css, lines, mode: str) -> str:
    """水印文案。

    `--watermark-text` 非 auto ⇒ 用其原值；`auto` ⇒ 由封面元信息派生：
        「{姓名} · 应聘 {公司} · 仅供招聘评估使用」—— 每投递对象唯一 ⇒ 泄漏可溯源。
    draft 档恒带 `DRAFT · 待确认` 前缀（显著 ⇒ 解决 Gate 阶段预览件被误投）。
    """
    raw = ((css or {}).get("--watermark-text", "auto") or "").strip()
    raw = raw.strip('"').strip("'").strip()
    if raw and raw.lower() not in ("auto", "none"):
        base = raw
    else:
        name = _pf_cover_field(lines, "姓名")
        comp = _pf_cover_field(lines, "应聘")
        parts = ([name] if name else []) + ([f"应聘 {comp}"] if comp else [])
        base = " · ".join(parts)
        if base:
            base = base + " · 仅供招聘评估使用"
    if mode == "draft":
        return f"DRAFT · 待确认 ｜ {base}" if base else "DRAFT · 待确认"
    return base


def _pf_header_html(css, lines) -> str:
    """页眉块（刀 D）：--header: none ⇒ 空串（整块不出现）。

    同页脚：HTML 端只给一行**观感占位**（浏览器无分页 ⇒ 不编造逐页重复）。
    """
    mode = ((css or {}).get("--header", "auto") or "").strip() or "auto"
    if mode == "none":
        return ""
    left, right = _pf_header_parts(css, lines)
    if not (left or right):
        return ""                       # 封面无身份信息 ⇒ 不产出空页眉
    return (f'<div class="header"><span>{left}</span>'
            f'<span class="to">{right}</span></div>')


def _pf_watermark_html(css, lines) -> str:
    """水印块（刀 D）：--watermark: none ⇒ 空串。文字平铺（非 logo），文案见 _pf_watermark_text。"""
    mode = ((css or {}).get("--watermark", "trace") or "").strip() or "trace"
    if mode == "none":
        return ""
    text = _pf_watermark_text(css, lines, mode)
    if not text:
        return ""                       # 封面缺身份信息 ⇒ 不产出空白水印层
    n = 1 if mode == "draft" else 6     # trace 平铺若干份示意；draft 居中一份大字
    spans = "".join(f"<span>{text}</span>" for _ in range(n))
    cls = " is-draft" if mode == "draft" else ""
    return f'<div class="watermark{cls}">{spans}</div>'


def _facts_row_parts(row):
    """facts 行（.row > span.k + 其余）→ (标签节点 | None, [(kind, 节点|文本)])。
    值节点里**不含**标签 —— 供 PDF 取 markup、DOCX 取 rich parts，两格式同源。"""
    k, items = None, []
    for kind, v in row.content:
        if kind == "c" and "k" in v.cls():
            k = v
        else:
            items.append((kind, v))
    return k, items


def _hex_rgb01_pure(h: str):
    """#RRGGBB / RRGGBB → (r,g,b) 0-1 浮点。不做 var() 解引用（调用方已解引用）。"""
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _mix_rgb01(h1: str, h2: str, t: float):
    """两色线性混合（t=0 → h1，t=1 → h2）→ (r,g,b)。
    PDF 专用：reportlab 的 TableStyle 不认 rgba alpha ⇒ 与白预混，避免「透明底变实心」。"""
    a, b = _hex_rgb01_pure(h1), _hex_rgb01_pure(h2)
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def _mix_hex(h1: str, h2: str, t: float) -> str:
    """同上，返回 "RRGGBB"（DOCX 用）。"""
    r, g, b = _mix_rgb01(h1, h2, t)
    return "".join(f"{int(round(v * 255)):02X}" for v in (r, g, b))


def build_data_portfolio(md_text: str, photo_path: str = "", css: dict = None) -> dict:
    """合册 md → 模板数据（契约见 assets/templates/resume-outputs/09_portfolio_book.md 头部注释）。

    返回：{"标题", "封面": [str], "封面原文": [str], "目录块": str,
           "页眉块": str, "页脚块": str, "水印块": str, "附录块": str,
           "案例": [{"标题","事实条","事实卡行","徽章","标签","摘要块",
                     "小节":[{"标题","html"}]}],
           "附录": [同"案例"结构]（F40 · 独立桶 ⇒ 不进目录 / 不计案例数）,
           "证件照", "header_shape_layers": [], "header_decos": []}
    css = 模板 CSS 变量表（extract_css_vars 结果）⇒ 页眉 / 页脚 / 水印块据此判定开关；
          缺省 None ⇒ 按合册默认（--header: auto / --footer: page-x-of-y / --watermark: trace）。
    """
    elements = parse_md(md_text)
    data = {"标题": "", "封面": [], "封面原文": [], "目录块": "", "页眉块": "",
            "页脚块": "", "水印块": "", "案例": [], "附录": [], "附录块": "",
            "证件照": photo_path or "",
            "header_shape_layers": [], "header_decos": []}
    cur, sub = None, None            # 当前案例 / 当前小节
    bullets = []                     # 连续 bullet 缓冲（合成 <ul>）
    bucket = "案例"                  # F40：当前区段桶 —— "案例" / "附录"（受控前缀判定）

    def flush_sub():
        nonlocal bullets
        if sub is not None:
            if bullets:
                sub["html"] += "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
                bullets = []
            sub["html"] = sub["html"].strip()

    for kind, val in elements:
        if kind == "title":
            data["标题"] = _pf_inline(val)
        elif kind == "heading":
            flush_sub()
            cur = {"标题": _pf_inline(val), "事实条": "", "事实卡行": [], "徽章": [],
                   "标签": [], "摘要块": "", "小节": []}
            sub, bullets = None, []
            # F40：受控前缀「附录」⇒ 归**附录桶**（不进目录 / 不计案例数 / 恒置尾）
            bucket = "附录" if _pf_is_appendix(val) else "案例"
            data[bucket].append(cur)
        elif kind == "quote" and cur is None:
            # F35（v2.24.0 · L2）：封面 `派生自` 段印内部路径 ⇒ **剥离后再决定是否入册**
            _cv = _pf_strip_cover_l2(val)
            if _cv:
                data["封面"].append(_pf_inline(_cv))      # 首个 ## 之前的引用 = 封面元信息
                data["封面原文"].append(_cv)               # 同一行的**纯文本**（页眉 / 水印派生用）
        elif cur is not None:
            if kind == "meta":                            # ### → 小节标题
                flush_sub()
                sub = {"标题": _pf_inline(val), "html": ""}
                bullets = []
                cur["小节"].append(sub)
            elif kind == "quote":                         # 案例内引用 = 摘要
                cur["摘要块"] = f'<div class="case-quote">{_pf_inline(val)}</div>'
            elif kind == "bullet":
                if sub is not None:
                    bullets.append(_pf_inline(val))
                else:
                    # 案例头部的 bullet（尚无 ### 小节）：并入事实条，不静默丢内容
                    cur["事实条"] = ((cur["事实条"] + " ｜ " + _pf_inline(val))
                                     if cur["事实条"] else ("• " + _pf_inline(val)))
            elif (kind == "body" and sub is None
                  and re.match(r"^\s*\*{0,2}标签\*{0,2}\s*[:：]", val)):
                # 可选第 5 段「标签：」（刀 B · 契约兼容扩展）⇒ 为 .badge 供数，不进事实条
                cur["标签"].extend(_pf_split_tags(
                    re.sub(r"^\s*\*{0,2}标签\*{0,2}\s*[:：]\s*", "", val)))
            elif kind in ("body", "table", "code", "hr"):
                if sub is not None:
                    if kind != "hr" and bullets:
                        sub["html"] += "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
                        bullets = []
                    sub["html"] += _pf_block_html(kind, val)
                elif kind != "hr":
                    # 案例头部（首个 ### 之前）：并入事实条 —— 不静默丢内容
                    # ⚠️ 事实条是**行内**片段（会被拆成事实卡各格与徽章文本）⇒ 不得包块级标签：
                    #    刀 A 此处用 _pf_block_html 产出 `<p>…</p>`，刀 A 不可见（Paragraph 忽略
                    #    未知标签），到刀 B 被拆进 <span>/<div class="row"> ⇒ 直接破坏 DOM 嵌套。
                    frag = _pf_inline(val) if kind == "body" else _pf_block_html(kind, val)
                    cur["事实条"] = (cur["事实条"] + " ｜ " + frag) if cur["事实条"] else frag
    flush_sub()
    # ---- 刀 B：案例级派生（事实卡行 / 徽章）+ 目录块 / 页脚块 ----
    # F40：附录与案例**同构派生**（事实卡 / 徽章）；但**目录块只由「案例」生成** ⇒ 附录不进目录
    for c in data["案例"] + data["附录"]:
        rows, _kou = _pf_split_facts(c["事实条"])
        c["事实卡行"] = rows
        # F35（v2.24.0 · L2 语义剥离）：`口径` 徽章**不再输出**（原为「口径：{值}」）。
        #   值仍由 _pf_split_facts 返回（_kou）以备调试 / 核查，**不进任何输出产物**。
        c["徽章"].extend({"文本": t, "cls": " plain"} for t in c["标签"])
    data["目录块"] = _pf_toc_html(data["案例"])
    data["页脚块"] = _pf_footer_html(css, data["标题"])
    # ---- 刀 D：页眉块 / 水印块 ----
    # ⚠️ 披露 fail-safe：待渲染的 md 里残留内部档标记 ⇒ 说明未过 L3 剥离
    #    ⇒ 水印强制 draft（宁可显著，不可把内部档当正式件投出去）。
    if _wm_force_draft(md_text):
        css = dict(css or {})
        css["--watermark"] = "draft"
    data["页眉块"] = _pf_header_html(css, data["封面原文"])
    data["水印块"] = _pf_watermark_html(css, data["封面原文"])
    # ---- F40：附录区（`kind=doc` 附加资料）HTML —— 置尾 · 不进目录 / 不计案例数 ----
    data["附录块"] = _pf_appendix_html(data["附录"])
    return data


# ---------- HTML DOM 解析（轻量） ----------

class Node:
    """轻量 DOM 节点：content 保序存储 [("t", 文本), ("c", 子节点)]，避免文本/子节点顺序错乱。"""
    __slots__ = ("tag", "attrs", "content")
    def __init__(self, tag="", attrs=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.content = []
    def add_text(self, data):
        if self.content and self.content[-1][0] == "t":
            self.content[-1] = ("t", self.content[-1][1] + data)
        else:
            self.content.append(("t", data))
    def add_child(self, node):
        self.content.append(("c", node))
    @property
    def children(self):
        return [c for k, c in self.content if k == "c"]
    @property
    def text(self):
        """纯文本（递归含子节点，不含 <b> 标记）。字符已过 _pdf_safe（→ → ->，防 tofu）。"""
        out = []
        for kind, val in self.content:
            if kind == "t":
                out.append(_pdf_safe(val))
            else:
                out.append(val.text)
        return "".join(out)
    def find_all(self, tag):
        out = []
        for c in self.children:
            if c.tag == tag:
                out.append(c)
            out.extend(c.find_all(tag))
        return out
    def find_first(self, tag):
        for c in self.children:
            if c.tag == tag:
                return c
            r = c.find_first(tag)
            if r:
                return r
        return None
    def cls(self):
        return (self.attrs.get("class") or "").split()


class _Builder(HTMLParser):
    VOID = {"img", "br", "hr"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].add_child(node)
        if tag not in self.VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].add_child(Node(tag, dict(attrs)))
    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()
    def handle_data(self, data):
        if self.stack:
            self.stack[-1].add_text(data)


def parse_dom(html_text: str) -> Node:
    b = _Builder()
    b.feed(html_text)
    return b.root


def rich_text(node: Node):
    """节点富文本（按文档顺序）：[(text, is_bold), ...]。text 已过 _pdf_safe（→ → ->）。"""
    out = []
    def walk(n, bold):
        for kind, val in n.content:
            if kind == "t":
                out.append((_pdf_safe(val), bold))
            else:
                if val.tag == "b":
                    walk(val, True)
                elif val.tag == "span" and "em-accent" in val.cls():
                    walk(val, True)         # F57：DOCX **降级为加粗**（不涉色 —— docx 定性为「可损」）
                elif val.tag == "br":
                    out.append(("\n", bold))
                else:
                    walk(val, bold)
    walk(node, False)
    return [(t, b) for t, b in out if t]


def _node_markup(node: Node) -> str:
    """节点 → reportlab Paragraph markup：保留 <b> 粗体子树；文本转义 XML 特殊字符并过 _pdf_safe（→ → ->）。

    注意：不能用 Node.text —— 它递归成纯文本会把 <b> 标记剥掉，导致 PDF 正文粗体丢失（HTML 端 <b>
    由浏览器渲染正常，PDF 端必须显式重建 markup）。
    """
    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = []

    def walk(n):
        for kind, val in n.content:
            if kind == "t":
                out.append(esc(_pdf_safe(val)))
            elif val.tag == "b":
                out.append("<b>")
                walk(val)
                out.append("</b>")
            elif val.tag == "span" and "em-accent" in val.cls():
                out.append('<b><font color="%s">' % _CURRENT_ACCENT)   # F57：加粗 + 主题色
                walk(val)
                out.append("</font></b>")
            elif val.tag == "br":
                out.append("<br/>")
            else:
                walk(val)

    walk(node)
    return "".join(out)


_PALETTE_MARKER_RE = re.compile(r"\{\{>\s*([\w./-]+)\s*\}\}")
_SHARED_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates" / "_shared"


def _inline_palette(tpl_text: str) -> str:
    """把模板里的共享片段标记（如 {{> palette}}）替换为 _shared/palette.css 全文。

    配色唯一定义源 ⇒ 简历与合册两模板共用，改一处两处生效。
    ⚠️ 必须在 mini_render 与 extract_css_vars 之前调用：变量不内联 ⇒ PDF/DOCX 读不到
       ⇒ 静默回退脚本内 default 色 = 配色漂移。
    无标记 ⇒ 原样返回（向后兼容旧模板）；
    有标记但文件缺失 ⇒ 报错中止（不静默降级 —— 静默降级正是漂移的来源）。
    """
    def repl(m):
        name = m.group(1)
        f = _SHARED_DIR / (name if name.endswith(".css") else f"{name}.css")
        if not f.exists():
            print(f"❌ 模板引用了不存在的共享片段: {m.group(0)}（期望 {f}）")
            sys.exit(1)
        return f.read_text(encoding="utf-8")
    return _PALETTE_MARKER_RE.sub(repl, tpl_text)


def extract_css_vars(html_text: str) -> dict:
    """从 <style> 的 :root 提取 CSS 变量。"""
    vars_ = {}
    for m in re.finditer(r":root\s*\{([^}]*)\}", html_text):
        for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", m.group(1)):
            vars_[k.strip()] = v.strip()
    return vars_


def apply_theme_override(html_text: str, theme: dict) -> str:
    """--theme 覆盖模板 CSS 变量（Track 联动快速换色）。"""
    def repl(m):
        body = m.group(1)
        body = re.sub(r"--accent:\s*[^;]+;", f"--accent: #{theme['accent']};", body)
        body = re.sub(r"--accent-dark:\s*[^;]+;", f"--accent-dark: #{theme['accent_dark']};", body)
        body = re.sub(r"--line:\s*[^;]+;", f"--line: #{theme['line']};", body)
        return ":root{" + body + "}"
    return re.sub(r":root\s*\{([^}]*)\}", repl, html_text)


# ---------- HTML → PDF（Platypus） ----------

def _reg_cn_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    here = Path(__file__).resolve().parent
    reg = here.parent / "assets" / "fonts" / "NotoSansSC-Regular.ttf"
    bold = here.parent / "assets" / "fonts" / "NotoSansSC-Bold.ttf"
    if reg.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("CN", str(reg)))
        pdfmetrics.registerFont(TTFont("CN-Bold", str(bold)))
        registerFontFamily("CN", normal="CN", bold="CN-Bold", italic="CN", boldItalic="CN-Bold")
        return "CN-Bold"
    # fallback 系统宋体
    import os
    songti = "/System/Library/Fonts/Supplemental/Songti.ttc"
    if os.path.exists(songti):
        pdfmetrics.registerFont(TTFont("CN", songti, subfontIndex=6))
        pdfmetrics.registerFont(TTFont("CN-Bold", songti, subfontIndex=1))
        registerFontFamily("CN", normal="CN", bold="CN-Bold", italic="CN", boldItalic="CN-Bold")
        return "CN-Bold"
    return "CN"


def _find_body(root: Node) -> Node:
    """从 DOM 树找 <body>（root → html → body）。"""
    html_node = next((c for c in root.children if c.tag == "html"), root)
    return html_node.find_first("body") or root


def _pf_style(name, parent, size, **kw):
    """合册样式工厂：**凡覆盖 fontSize 必同步 leading**。

    ⚠️ reportlab 的行框高 = leading；leading < fontSize 时字形会溢出到下一行 ⇒ 视觉重叠。
    HTML / DOCX 无此耦合 ⇒ 该缺陷只在 PDF 侧出现（表现为「PDF 与 html/docx 不一致」）。
    """
    from reportlab.lib.styles import ParagraphStyle
    lead = kw.pop("leading", None) or size * 1.3
    return ParagraphStyle(name, parent=parent, fontSize=size, leading=lead, **kw)


def _ratio(raw, dflt: float) -> float:
    """CSS 比例值 → float。

    容忍空串 / 非数字 / 越界 ⇒ 一律回落默认值 —— 一条脏变量不该把整份产出打断。
    """
    try:
        v = float(str(raw).strip())
    except (TypeError, ValueError):
        return dflt
    return v if 0.0 <= v <= 1.0 else dflt


def _portfolio_metrics(cv, cv_px) -> dict:
    """合册版式量 —— **唯一定义源 = portfolio 模板 :root 的 CSS 变量**（PDF 与 DOCX 共用本函数）。

    变量名以合册模板的声明为准，仅在缺失时才回落到简历同名变量
    （否则「模板里声明的变量」= 空声明 ⇒ 改模板不生效，属静默降级）。
    ⚠️ 本函数返回的每个字号，使用处必须经 _pf_style() 注入 leading。
    """
    def _pt(pf_var, rs_var, dflt):
        raw = cv(pf_var, "").strip()
        if not raw:
            raw = cv(rs_var, dflt)
        return float(str(raw).strip().rstrip("pt"))
    body_sz = float(cv("--body-size", "10.5").rstrip("pt"))
    small_raw = cv("--small-size", "").strip()
    # --small-size 是合册专有变量 ⇒ 不做「回落简历同名变量」（简历的 --info-size 语义不同）
    small_sz = float(small_raw.rstrip("pt")) if small_raw else max(body_sz - 1.5, 6.0)
    return {
        "book":       _pt("--book-title-size", "--title-size", "24"),     # 封面主标题
        "case":       _pt("--case-title-size", "--heading-size", "16"),   # 案例标题
        "sub":        _pt("--sub-title-size",  "--heading-size", "12"),   # 小节标题
        "body":       body_sz,                                            # 正文（刀 B：目录项）
        "small":      small_sz,                                           # 辅助小字（刀 B：徽章 / 页脚）
        "case_space": cv_px("--case-space-before", 20),                   # 案例之间
        "cover_gap":  cv_px("--cover-meta-gap", 28),                      # 封面装饰线 → 元信息
        # ---- 刀 D 新增（封面居中 / 间距）----
        "cover_rule_gap":  cv_px("--cover-rule-gap", 18),                 # 封面标题 → 装饰线
        "cover_top_ratio": _ratio(cv("--cover-top-ratio", "0.45"), 0.45),  # 留白分配比（0.5=居中）
    }


def html_to_pdf(html_text: str, out_path: Path, profile: str = "resume", _total: int = 0,
                page_height: float = None):
    """HTML → PDF。

    _total：页脚 --footer: page-x-of-y 需要的**总页数**（首趟为空 ⇒ 先数页数再整函数重跑；
            重跑而非复用 flowables —— reportlab build 会消费 flowable，复用是错的）。
    page_height：**页面高度（pt）**；`None` = A4（默认，向后兼容）。传大值 ⇒ **单张超高页** ——
            PNG 长图（F25）走此路径（内容不分页 ⇒ 无页背景 / 水印接缝；页宽恒为 A4 宽）。
            ⚠️ 只改页高、不改页宽 ⇒ 版式（内容宽 = A4宽 − 左右边距）不变。
    返回：总页数（int）。
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor
    import io as _io
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                    TableStyle, Image, HRFlowable, Preformatted, PageBreak)
    from reportlab.lib.styles import ParagraphStyle

    bold_font = _reg_cn_fonts()
    css = extract_css_vars(html_text)
    def cv(var, default):
        v = css.get(var, default).strip()
        return v
    accent = HexColor(cv("--accent", "#1564BF"))
    global _CURRENT_ACCENT
    _CURRENT_ACCENT = cv("--accent", "#1564BF")   # F57：行内强调色源 = 模板 --accent
    line_c = HexColor(cv("--line", "#D9E2F0"))
    text_c = HexColor(cv("--text", "#1A1A1A"))
    block_bg = HexColor(cv("--block-bg", "#EAF2FA"))
    font_family = cv("--font", "CN")
    title_size = float(cv("--title-size", "20").rstrip("pt"))
    heading_size = float(cv("--heading-size", "14").rstrip("pt"))
    body_size = float(cv("--body-size", "10.5").rstrip("pt"))
    line_spacing = float(cv("--line-spacing", "1.6"))
    mt = float(cv("--page-margin-top", "18").rstrip("mm"))
    ms = float(cv("--page-margin-side", "16").rstrip("mm"))
    page_w_cm = 21.0 - 2 * ms / 10.0  # A4 宽 - 左右页边距（--page-margin-side），替代硬编码 17.8cm

    # ---- 布局变量桥：从模板 :root 的 CSS 变量读取布局数值（px → pt 换算） ----
    # 用户改 resume_template.html 的 :root 变量（--body-indent 等）即改 PDF/DOCX 版式，无需改本脚本
    def cv_px(var: str, default_px: float) -> float:
        """读取 CSS 变量（支持 px/pt/mm），统一换算为 pt。"""
        raw = cv(var, f"{default_px}px").strip()
        if raw.endswith("px"):
            return float(raw[:-2]) * 0.75   # 1px = 0.75pt
        if raw.endswith("pt"):
            return float(raw[:-2])
        if raw.endswith("mm"):
            return float(raw[:-2]) * 2.835  # 1mm ≈ 2.835pt
        return float(raw) * 0.75
    body_indent = cv_px("--body-indent", 28)      # 节内正文右平移
    bullet_indent = cv_px("--bullet-indent", 46)  # bullet 再右平移
    heading_sb = cv_px("--heading-space-before", 14)
    heading_sa = cv_px("--heading-space-after", 8)
    entry_space = cv_px("--entry-space", 8)
    # Header 布局变量
    header_pad_top = cv_px("--header-pad-top", 12)
    header_pad_bottom = cv_px("--header-pad-bottom", 12)
    header_pad_left = cv_px("--header-pad-left", 14)
    header_pad_right = cv_px("--header-pad-right", 10)
    photo_margin_top = cv_px("--photo-margin-top", 0)
    photo_gap = cv_px("--photo-gap", 12)
    name_to_info = cv_px("--name-to-info", 10)
    info_line_gap = cv_px("--info-line-gap", 2)
    intent_size = float(cv("--intent-size", "12").rstrip("pt"))
    info_size = float(cv("--info-size", "10.5").rstrip("pt"))
    photo_w_cm = float(cv("--photo-width", "3.5").rstrip("cm"))
    # header 文字色（v2.8.5）：--header-text-color / --header-tag-color（默认继承 --text / --accent）
    header_text_color = cv("--header-text-color", "#1A1A1A").strip()
    header_tag_color = cv("--header-tag-color", "#1564BF").strip()
    header_tag_hex = header_tag_color
    if header_tag_hex.startswith("var("):
        header_tag_hex = cv(header_tag_hex[4:-1].strip(), "#1564BF").strip()

    import math as _m
    from reportlab.lib.colors import Color as _Color

    def _hex_rgb01(h):
        if h.startswith("var("):  # 解析 CSS 变量引用 var(--x) → 实际色值
            inner = h[4:-1].strip()
            h = cv(inner, "#EAF2FA").strip()
        h = h.strip().lstrip("#")
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    s_name = ParagraphStyle("name", fontName=bold_font, fontSize=title_size, leading=title_size * 1.2,
                            textColor=_Color(*_hex_rgb01(header_text_color)))
    s_intent = ParagraphStyle("intent", fontName="CN", fontSize=intent_size, leading=intent_size * 1.3,
                              textColor=_Color(*_hex_rgb01(header_text_color)))
    s_head = ParagraphStyle("head", fontName=bold_font, fontSize=heading_size, leading=heading_size * 1.3,
                            spaceBefore=heading_sb, spaceAfter=heading_sa, textColor=text_c)
    # 注意：节标题 Paragraph 放入 Table 单元格，spaceBefore/spaceAfter 实测不生效；
    # 间距实际由渲染循环中的 Spacer(1, heading_sb/sa) 控制（[YYYY-MM-DD] 实测确认）
    s_meta = ParagraphStyle("meta", fontName=bold_font, fontSize=body_size, leading=body_size * line_spacing, textColor=accent)
    s_body = ParagraphStyle("body", fontName="CN", fontSize=body_size, leading=body_size * line_spacing, textColor=text_c, wordWrap="CJK")
    s_bullet = ParagraphStyle("bullet", fontName="CN", fontSize=body_size, leading=body_size * line_spacing,
                              leftIndent=18, textColor=text_c, wordWrap="CJK")
    s_item = ParagraphStyle("item", fontName="CN", fontSize=info_size, leading=info_size * line_spacing,
                            textColor=_Color(*_hex_rgb01(header_text_color)))

    # ---- 背景层（v2.8.2：页面背景 + header 形状背景，onPage canvas 绘制） ----
    page_bg_type = cv("--page-bg-type", "none").strip()
    page_bg_value = cv("--page-bg-value", "#FFFFFF").strip()
    page_bg_opacity = float(cv("--page-bg-opacity", "100").strip().rstrip("%")) / 100.0
    header_bg_type = cv("--header-bg-type", "color").strip()
    header_bg_value = cv("--header-bg-value", "#EAF2FA").strip()
    header_shape = [s.strip() for s in cv("--header-shape", "rounded").split(",") if s.strip()]
    header_shapes = [s.strip() for s in cv("--header-shapes", "").split(",") if s.strip()]  # v2.8.4 多形状层名
    hbh_raw = cv("--header-bg-height", "auto").strip()
    header_bg_height = None if hbh_raw.lower() == "auto" else cv_px("--header-bg-height", 105)  # None=auto 跟随照片高度
    header_bg_stroke = cv("--header-bg-stroke", "").strip() or None  # 主形状描边色（空=无描边）
    wave_amp = cv_px("--shape-wave-amplitude", 10)
    wave_seg = max(int(float(cv("--shape-wave-segments", "40"))), 8)
    wave_line = cv("--shape-wave-line", "#D9E2F0").strip() or None
    slant_angle = float(cv("--shape-slant-angle", "45").rstrip("deg"))
    deco_block_alpha = float(cv("--deco-block-alpha", "0.13"))
    deco_dots_alpha = float(cv("--deco-dots-alpha", "0.30"))
    deco_stripe_angle = float(cv("--deco-stripe-angle", "45").rstrip("deg"))
    deco_stripe_alpha = float(cv("--deco-stripe-alpha", "0.22"))
    photo_h_pt = None  # auto 高度时记录照片实际渲染高度

    # ---- 合册版式开关（刀 B）----
    # 简历模板**不声明** --cover-page / --footer ⇒ 默认 same / none ⇒ 简历零变化
    # （这是「机制保证」，不是「我们没动它」：变量未声明 ⇒ 读到的就是关闭态）
    cover_page = cv("--cover-page", "always" if profile == "portfolio" else "same").strip()
    footer_mode = cv("--footer", "page-x-of-y" if profile == "portfolio" else "none").strip()
    _small_raw = cv("--small-size", "").strip()
    small_size_pt = float(_small_raw.rstrip("pt")) if _small_raw else max(body_size - 1.5, 6.0)
    footer_title_pt = ""     # 页脚左侧文案（= 合册主标题；构 story 时回填）

    # ---- 刀 D 版式开关：页眉 / 水印 ----
    # 简历模板**不声明** --header / --watermark ⇒ 默认 none ⇒ 简历零变化
    # （同 --cover-page / --footer：机制保证，不是「我们没动它」）
    header_mode = cv("--header", "auto" if profile == "portfolio" else "none").strip() or "none"
    wm_mode = cv("--watermark", "trace" if profile == "portfolio" else "none").strip() or "none"
    try:
        wm_opacity = float(cv("--watermark-opacity", "0.04").strip() or 0.04)
    except ValueError:
        wm_opacity = 0.04
    # 披露 fail-safe：残留内部档标记 ⇒ trace 升为 draft（关掉水印的件不因此被打开）。
    # ⚠️ **两个判据都要查**（实测：只查 html_text 会漏）：
    #    ① `_wm_force_draft(html_text)` —— 标记**存活到 HTML** 的情形（可见文本）；
    #    ② `watermark is-draft` —— 标记**被 md→HTML 转换剥掉**的情形（如写在 HTML 注释里，
    #       而注释恰是本 skill 作者批注的惯用形式）。此时 `build_data_portfolio` 已据 **md**
    #       把水印块判为 draft ⇒ **HTML 出口已是 draft**；若 PDF 只查 html_text 就仍停在 trace
    #       ⇒ **同一产物两出口给出不同披露等级**（危险方向：内部档被当正式件投出去）。
    #    判据统一为「**HTML 已按 draft 渲染 ⇒ PDF 跟随**」—— 单一判定点 = 水印块生成处。
    if wm_mode == "trace" and (_wm_force_draft(html_text)
                              or "watermark is-draft" in html_text):
        wm_mode = "draft"
    cover_meta_plain: list[str] = []   # 封面元信息纯文本（构 story 时收集）
    header_left_pt = ""                # 页眉左段（构 story 时回填）
    header_right_pt = ""               # 页眉右段
    wm_text_pt = ""                    # 水印文案

    def _draw_one_shape(c, name, x, y, w, h):
        """绘制单个形状层（--shape-{name}-* 参数）。"""
        typ = cv(f"--shape-{name}-type", "trapezoid").strip()
        color = cv(f"--shape-{name}-color", "#1A3A6E").strip()
        h_raw = cv(f"--shape-{name}-height", "auto").strip()
        height = h if h_raw.lower() == "auto" else cv_px(f"--shape-{name}-height", h)
        ox = cv_px(f"--shape-{name}-offset-x", 0)
        oy = cv_px(f"--shape-{name}-offset-y", 0)
        align = cv(f"--shape-{name}-align", "bottom").strip().lower()
        if align == "top":
            oy = h - height  # v2.8.7: top 对齐=层顶边贴区域顶（自动计算，忽略 offset-y）
        sx, sy, sh = x + ox, y + oy, height
        fill = _Color(*_hex_rgb01(color))
        if typ == "trapezoid":
            raw = cv(f"--shape-{name}-insets", "0 0 0 0").strip().split()
            def _iv(i, d=0.0):
                return float(raw[i].rstrip("pxpt").replace("pt", "")) if i < len(raw) else d
            tl, tr, bl, br = _iv(0), _iv(1), _iv(2), _iv(3)
            p = c.beginPath()
            p.moveTo(sx + tl, sy + sh)              # 左上（顶边左缩进 tl）
            p.lineTo(sx + w - tr, sy + sh)          # 右上（顶边右缩进 tr）
            p.lineTo(sx + w - br, sy)               # 右下（底边右缩进 br）
            p.lineTo(sx + bl, sy)                   # 左下（底边左缩进 bl）
            p.close()
            c.setFillColor(fill)
            c.drawPath(p, fill=1, stroke=0)
        elif typ == "slant":
            cut = min(sh * _m.tan(_m.radians(slant_angle)), w * 0.5)
            p = c.beginPath()
            p.moveTo(sx, sy + sh); p.lineTo(sx + w - cut, sy + sh)
            p.lineTo(sx + w, sy + sh - cut); p.lineTo(sx + w, sy + sh)
            p.lineTo(sx, sy); p.close()
            c.setFillColor(fill)
            c.drawPath(p, fill=1, stroke=0)
        elif typ == "square":
            c.setFillColor(fill)
            c.rect(sx, sy, w, sh, fill=1, stroke=0)
        else:  # rounded
            c.setFillColor(fill)
            c.roundRect(sx, sy, w, sh, 8, fill=1, stroke=0)

    def _draw_header_shapes(c, x, y, w, h):
        """在区域 (x,y)-(x+w,y+h) 绘制 header 形状背景。
        v2.8.4：--header-shapes 非空 → 多形状堆叠（每层独立 type/color/参数）；
        为空 → 兼容旧单形状模式（--header-shape 主形状 + 装饰层）。"""
        if header_shapes:
            for name in header_shapes:
                _draw_one_shape(c, name, x, y, w, h)
            return
        # ---- 旧单形状模式（兼容） ----
        main = header_shape[0] if header_shape else "rounded"
        fill = _Color(*_hex_rgb01(header_bg_value))
        path = None
        if main == "wave":
            path = c.beginPath()
            path.moveTo(x, y + h)
            n = wave_seg
            pts = [(x + i * (w / n), y + h + wave_amp * _m.sin(i / n * 2 * _m.pi * 2)) for i in range(n + 1)]
            for px, py in pts:
                path.lineTo(px, py)
            path.lineTo(x, y)
            path.close()
            c.setFillColor(fill)
            c.drawPath(path, fill=1, stroke=0)
        elif main == "slant":
            cut = min(h * _m.tan(_m.radians(slant_angle)), w * 0.5)
            path = c.beginPath()
            path.moveTo(x, y + h); path.lineTo(x + w - cut, y + h)
            path.lineTo(x + w, y + h - cut); path.lineTo(x + w, y + h)
            path.lineTo(x, y); path.close()
            c.setFillColor(fill)
            c.drawPath(path, fill=1, stroke=0)
        elif main == "square":
            c.setFillColor(fill)
            c.rect(x, y, w, h, fill=1, stroke=0)
        else:  # rounded
            c.setFillColor(fill)
            c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        stroke_c = header_bg_stroke or (wave_line if main == "wave" else None)
        if stroke_c:
            c.setStrokeColor(_Color(*_hex_rgb01(stroke_c)))
            c.setLineWidth(0.8)
            if main in ("wave", "slant") and path is not None:
                c.drawPath(path, fill=0, stroke=1)
            elif main == "square":
                c.rect(x, y, w, h, fill=0, stroke=1)
            else:
                c.roundRect(x, y, w, h, 8, fill=0, stroke=1)
        accent_rgb = _hex_rgb01(cv("--accent", "#1564BF"))
        if "block" in header_shape:
            c.setFillColor(_Color(accent_rgb[0], accent_rgb[1], accent_rgb[2], deco_block_alpha))
            c.roundRect(x + w - 92, y + h - 34, 84, 26, 8, fill=1, stroke=0)
        if "dots" in header_shape:
            c.setFillColor(_Color(accent_rgb[0], accent_rgb[1], accent_rgb[2], deco_dots_alpha))
            c.circle(x + 34, y + 10, 4.5, fill=1, stroke=0)
            c.circle(x + 48, y + 10, 3.0, fill=1, stroke=0)
            c.circle(x + 58, y + 10, 3.6, fill=1, stroke=0)
        if "stripe" in header_shape:
            c.saveState()
            c.translate(x + w * 0.55, y + 12)
            c.rotate(-deco_stripe_angle)
            c.setFillColor(_Color(accent_rgb[0], accent_rgb[1], accent_rgb[2], deco_stripe_alpha))
            c.rect(0, 0, 90, 5, fill=1, stroke=0)
            c.restoreState()

    def draw_background(cv_, doc_):
        """页面回调（build onFirstPage/onLaterPages）：页面背景（每页）+ header 背景（第一页顶部区域）。"""
        W_, H_ = doc_.pagesize
        # 页面背景
        if page_bg_type in ("color", "image"):
            if page_bg_type == "image" and Path(page_bg_value).exists():
                cv_.saveState()
                cv_.setFillAlpha(page_bg_opacity)
                try:
                    cv_.drawImage(str(page_bg_value), 0, 0, width=W_, height=H_, preserveAspectRatio=False)
                finally:
                    cv_.restoreState()
            else:
                try:
                    cv_.setFillColor(_Color(*_hex_rgb01(page_bg_value)))
                except Exception:
                    cv_.setFillColor(_Color(1, 1, 1))
                cv_.setFillAlpha(page_bg_opacity)
                cv_.rect(0, 0, W_, H_, fill=1, stroke=0)
        # header 背景（第一页顶部）；高度：auto=照片高度+上下内边距（完整包裹照片），否则用固定值
        if cv_.getPageNumber() == 1:
            if header_bg_height is None:
                hh = photo_h_pt if photo_h_pt else 105
                hh = hh + header_pad_top + photo_margin_top + header_pad_bottom  # 背景完整包裹照片
            else:
                hh = header_bg_height
            hx = ms * mm
            hy = H_ - mt * mm - hh
            hw = W_ - 2 * ms * mm
            if header_bg_type == "image" and Path(header_bg_value).exists():
                cv_.drawImage(str(header_bg_value), hx, hy, width=hw, height=hh, preserveAspectRatio=False)
            elif header_bg_type == "shape":
                _draw_header_shapes(cv_, hx, hy, hw, hh)

    def _draw_footer(cv_, doc_):
        """页脚（刀 B）：--footer 决定格式；封面页（--cover-page: always 的第 1 页）不画。
        页码口径：封面不印 ⇒ 正文自 1 起，Y = 总页数 − 1（--footer: page-x-of-y）。"""
        if footer_mode == "none":
            return
        pn = cv_.getPageNumber()
        off = 1 if cover_page == "always" else 0
        if pn - off < 1:                       # 封面页（或未独立成页时的第 1 页起点）
            return
        W_, H_ = doc_.pagesize
        y = mt * mm - 12
        cv_.saveState()
        cv_.setStrokeColor(line_c)
        cv_.setLineWidth(0.6)
        cv_.line(ms * mm, y + 9, W_ - ms * mm, y + 9)
        cv_.setFont("CN", small_size_pt)
        cv_.setFillColor(text_c)
        if footer_title_pt:
            cv_.drawString(ms * mm, y, footer_title_pt)
        if footer_mode == "page-x-of-y" and _total > 0:
            label = f"第 {pn - off} 页 / 共 {_total - off} 页"
        else:
            label = f"第 {pn - off} 页"
        cv_.setFillColor(accent)
        cv_.drawRightString(W_ - ms * mm, y, label)
        cv_.restoreState()

    def _draw_header(cv_, doc_):
        """页眉（刀 D · --header）：封面页不画（与页脚同规则）。

        文案来源 = 封面元信息（零新字段）；--header: full 需封面含「联系」行，无则降级 auto。
        空间核算：--page-margin-top 18mm ≈ 51pt，页眉占 10pt + 下边线 ⇒ 正文不挤压；
        ⚠️ 若日后把 --page-margin-top 调到 < 14mm 就会撞（模板维护钩子已登记）。
        """
        if header_mode == "none" or not (header_left_pt or header_right_pt):
            return
        pn = cv_.getPageNumber()
        off = 1 if cover_page == "always" else 0
        if pn - off < 1:
            return
        W_, H_ = doc_.pagesize
        y = H_ - mt * mm + 10
        cv_.saveState()
        cv_.setFont("CN", small_size_pt)
        cv_.setFillColor(text_c)
        if header_left_pt:
            cv_.drawString(ms * mm, y, header_left_pt)
        if header_right_pt:
            cv_.setFillColor(accent)
            cv_.drawRightString(W_ - ms * mm, y, header_right_pt)
        cv_.setStrokeColor(line_c)
        cv_.setLineWidth(0.5)
        cv_.line(ms * mm, y - 5, W_ - ms * mm, y - 5)
        cv_.restoreState()

    def _draw_watermark(cv_, doc_):
        """水印（刀 D · --watermark）：文字平铺（trace）/ 居中大字（draft）。

        为什么用文字不用 logo：求职者没有品牌 logo，自造 monogram 会被误认为某公司标识；
        而文字承载「是谁 · 投给谁 · 作何用」⇒ 泄漏可溯源 —— 这才是防盗水印的真实价值。
        为什么平铺：只用水印无法局部裁除（去水印成本高）；单个大对角字易被裁。
        绘制时机：onPage ⇒ 在 flowables **之前**绘制 ⇒ 位于正文之下，不伤可读性。
        """
        if wm_mode == "none" or not wm_text_pt:
            return
        W_, H_ = doc_.pagesize
        if wm_mode == "draft":
            size = small_size_pt * 4.4
            alpha = min(max(wm_opacity * 3.0, 0.10), 0.18)   # 显著但仍不遮字
        else:
            size = small_size_pt * 1.6
            alpha = min(max(wm_opacity, 0.02), 0.10)         # 建议 3%–6%，上限 10%
        cv_.saveState()
        cv_.setFillColor(accent)
        try:
            cv_.setFillAlpha(alpha)
        except Exception:
            pass                                             # 老版 reportlab 无 alpha ⇒ 不中断
        cv_.setFont("CN", size)
        cv_.translate(W_ / 2.0, H_ / 2.0)
        cv_.rotate(-30)
        if wm_mode == "draft":
            cv_.drawCentredString(0, 0, wm_text_pt)
        else:
            gap_x = size * 8.0
            gap_y = size * 3.4
            tw = cv_.stringWidth(wm_text_pt, "CN", size) + gap_x
            R = ((W_ ** 2 + H_ ** 2) ** 0.5) / 2.0 + tw     # 覆盖旋转后的整页所需半径
            row, yy = 0, -R
            while yy < R:                                    # 隔行错位 ⇒ 更像平铺纹样
                xx = -R + (row % 2) * (tw / 2.0)
                while xx < R:
                    cv_.drawString(xx, yy, wm_text_pt)
                    xx += tw
                yy += gap_y
                row += 1
        cv_.restoreState()

    def _on_page(cv_, doc_):
        """页面回调：背景 → 水印 → 页眉 → 页脚（未开启者各自立即返回）。

        顺序即层序：水印最先（最底），页眉 / 页脚最后（保证压在水印之上、始终可读）。
        """
        draw_background(cv_, doc_)
        _draw_watermark(cv_, doc_)
        _draw_header(cv_, doc_)
        _draw_footer(cv_, doc_)

    def p_rich(text):
        return Paragraph(text, s_body)

    root = parse_dom(html_text)
    body = _find_body(root)
    story = []

    # 模板若用 .page 容器包裹，递归到 .page 内；否则直接在 body children 上迭代
    page_node = None
    for c in body.children:
        if c.tag == "div" and "page" in c.cls():
            page_node = c
            break
    container = page_node if page_node else body

    toc_needed = False   # 合册目录（刀 B）：随 DOM 里是否存在 .toc 置位
    if profile == "portfolio":
        # ---- 合册 profile：封面 + 案例块（.table / .flow 走结构渲染，不再退化为文本） ----
        pf = _portfolio_metrics(cv, cv_px)

        # ---- 刀 B 版式常量与派生色 ----
        # 派生色：reportlab 的 TableStyle 不认 rgba alpha ⇒ 与白预混（全部由 --accent 派生，不引入新色）
        _acc_hex = cv("--accent", "#1564BF")
        badge_tint = _mix_rgb01(_acc_hex, "#FFFFFF", 0.90)   # hero 底（accent 10%）
        badge_deep = _mix_rgb01(_acc_hex, "#FFFFFF", 0.82)   # 徽章底（accent 18%）
        badge_edge = _mix_rgb01(_acc_hex, "#FFFFFF", 0.55)   # 徽章边
        hero_bar_w = cv_px("--hero-bar", 4)
        hero_pad_x, hero_pad_y = 14.0, 9.0    # 版式常量（与模板 .hero 同步 —— 见模板维护钩子 3）
        badge_pad_x, badge_pad_y, badge_gap = 5.0, 2.2, 6.0
        avail_badge_w = page_w_cm * cm - hero_bar_w - 2 * hero_pad_x
        avail_flow_h = A4[1] - 2 * mt * mm - 8   # 单块流式高度上限（超一页 ⇒ 预分片）

        def _s(parent, name):
            return next((c for c in parent.children
                         if c.tag == "div" and name in c.cls()), None)

        def _pf_table(tbl, indent=0.0):
            rows = []
            for tr in tbl.find_all("tr"):
                cells = [c for c in tr.children if c.tag in ("td", "th")]
                rows.append([Paragraph(_node_markup(c), s_body) for c in cells])
            rows = [r for r in rows if r]
            if not rows:
                return None
            ncol = max(len(r) for r in rows)
            rows = [r + [Paragraph("", s_body)] * (ncol - len(r)) for r in rows]
            w = max((page_w_cm * cm - indent) / ncol, 1.0 * cm)
            t = Table(rows, colWidths=[w] * ncol, repeatRows=1)   # repeatRows：跨页重复表头
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), block_bg),
                ("GRID", (0, 0), (-1, -1), 0.4, line_c),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            return t

        def _pf_badge(span, plain=False):
            """徽章 → (1×1 圆角 Table, 宽)。真底色：预混色填充（reportlab 无 rgba）。

            F50（v2.24.0）：原用 `Paragraph.wrap()` 的**返回宽**当固有宽 —— 它返回的是
            **实际排版用宽（= 可用宽）**，不是文本固有宽（实测 avail=400 → w=400.00）
            ⇒ `_pack_badges` 的换行判据 `cur_w + w + gap > avail` **恒真** ⇒ 徽章退化「1 枚 / 行」。
            改用 `pdfmetrics.stringWidth()` 取**文本固有宽**（pt，与 colWidths 同尺度）。
            """
            raw = _pdf_safe(span.text)
            txt = _pf_escape(raw)
            st = _pf_style("pf_bg", s_body, pf["small"], textColor=(text_c if plain else accent))
            p = Paragraph(txt, st)
            from reportlab.pdfbase.pdfmetrics import stringWidth as _sw
            w = _sw(raw, st.fontName, st.fontSize)
            style = [("LEFTPADDING", (0, 0), (-1, -1), badge_pad_x),
                     ("RIGHTPADDING", (0, 0), (-1, -1), badge_pad_x),
                     ("TOPPADDING", (0, 0), (-1, -1), badge_pad_y),
                     ("BOTTOMPADDING", (0, 0), (-1, -1), badge_pad_y),
                     ("ROUNDEDCORNERS", [7, 7, 7, 7])]
            if plain:
                style.append(("BOX", (0, 0), (-1, -1), 0.4, line_c))
            else:
                style.append(("BACKGROUND", (0, 0), (-1, -1), _Color(*badge_deep)))
                style.append(("BOX", (0, 0), (-1, -1), 0.4, _Color(*badge_edge)))
            t = Table([[p]], colWidths=[w + 2 * badge_pad_x], style=style)
            return t, w + 2 * badge_pad_x

        def _pack_badges(cells):
            """[(table, w)] → 按可用宽贪心换行 → [Table]（行内 RIGHTPADDING=gap 充当间距）。"""
            rows, cur, cur_w = [], [], 0.0
            for t, w in cells:
                if cur and cur_w + w + badge_gap > avail_badge_w:
                    rows.append(cur)
                    cur, cur_w = [], 0.0
                cur.append(t)
                cur_w += w + (badge_gap if len(cur) > 1 else 0)
            if cur:
                rows.append(cur)
            out = []
            for row in rows:
                out.append(Table([row], colWidths=[c._colWidths[0] for c in row],
                                 style=[("LEFTPADDING", (0, 0), (-1, -1), 0),
                                        ("RIGHTPADDING", (0, 0), (-1, -1), badge_gap),
                                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                                        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            return out

        def _pf_facts(node):
            """元信息卡（刀 B）：2 列 = 4 列网格（标签 accent + 值）· 无框线 + 行下细线。"""
            items = []
            for r in node.children:
                if r.tag == "div" and "row" in r.cls():
                    k, spans = _facts_row_parts(r)
                    parts = []
                    for kind, v in spans:
                        parts.append(_node_markup(v) if kind == "c"
                                     else _pf_escape(_pdf_safe(v)))
                    items.append((_node_markup(k) if k is not None else "",
                                  "".join(parts).strip()))
            if not items:
                return None
            grid = [items[i:i + 2] for i in range(0, len(items), 2)]
            w_tot = page_w_cm * cm
            k_w, v_w = w_tot * 0.13, w_tot * 0.37
            rows = []
            for pair in grid:
                row = []
                for i in range(2):
                    if i < len(pair):
                        kl, vl = pair[i]
                        row.append(Paragraph(kl, _pf_style("pf_fk", s_body, pf["body"],
                                                           textColor=accent)))
                        row.append(Paragraph(vl, _pf_style("pf_fv", s_body, pf["body"])))
                    else:
                        row.extend([Paragraph("", s_body), Paragraph("", s_body)])
                rows.append(row)
            t = Table(rows, colWidths=[k_w, v_w, k_w, v_w])
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                                   ("TOPPADDING", (0, 0), (-1, -1), 3),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                   ("LINEBELOW", (0, 0), (-1, -1), 0.4, line_c)]))
            return t

        def _pf_hero(node, ap=False):
            """案例标题区（刀 B）：左 accent 竖条 + 浅底（2 列表格）· 内含标题 + 徽章行。

            ⚠️ 不复用简历 .header 的形状背景 —— 那是**页面级 onPage 绘制**（页的属性、非块的属性），
               硬复用会把整页形状画进每个案例。视觉同源靠**配色/变量同源**保证。
            标题段样式名固定 "pf_ct" —— 目录回填（afterFlowable）据此识别。
            ⚠️ F40：附录（ap=True）标题改用样式名 **"pf_at"** ⇒ **不进目录**
               （目录只收 "pf_ct"）；字号降为小节级、色转正文色 ⇒ 视觉弱化。
            """
            blob = []
            t = _s(node, "case-title")
            if t is not None:
                blob.append(Paragraph(_node_markup(t),
                                      _pf_style("pf_at" if ap else "pf_ct", s_head,
                                                pf["sub"] if ap else pf["case"],
                                                textColor=text_c if ap else accent)))
            bd = _s(node, "hero-badges")
            if bd is not None:
                cells = [_pf_badge(sp, plain="plain" in sp.cls())
                         for sp in bd.children
                         if sp.tag in ("span", "div") and "badge" in sp.cls()]
                if cells:
                    blob.append(Spacer(1, 4))
                    blob.extend(_pack_badges(cells))
            if not blob:
                return []
            inner_w = page_w_cm * cm - hero_bar_w
            t2 = Table([["", blob]], colWidths=[hero_bar_w, inner_w],
                       style=[("BACKGROUND", (0, 0), (0, 0), accent),
                              ("BACKGROUND", (1, 0), (1, 0), _Color(*badge_tint)),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LEFTPADDING", (0, 0), (0, 0), 0),
                              ("RIGHTPADDING", (0, 0), (0, 0), 0),
                              ("TOPPADDING", (0, 0), (0, 0), 0),
                              ("BOTTOMPADDING", (0, 0), (0, 0), 0),
                              ("LEFTPADDING", (1, 0), (1, 0), hero_pad_x),
                              ("RIGHTPADDING", (1, 0), (1, 0), hero_pad_x),
                              ("TOPPADDING", (1, 0), (1, 0), hero_pad_y),
                              ("BOTTOMPADDING", (1, 0), (1, 0), hero_pad_y)])
            return [t2, Spacer(1, entry_space / 2)]

        def _pf_flow_chunks(text, style, avail_h):
            """单块超页高 ⇒ 按行预分片（reportlab 对高于一页的 Preformatted 抛 LayoutError）。"""
            lines = (text or "").split("\n")
            lh = float(style.leading or 12)
            per = max(1, int((avail_h - 16) // lh))
            if len(lines) <= per:
                return [text]
            return ["\n".join(lines[i:i + per]) for i in range(0, len(lines), per)]

        def _blocks(nodes, indent=0.0):
            """小节内容块 → flowables（p / ul / table / div.flow），顺序保真。"""
            flows = []
            for ch in nodes:
                cls = ch.cls()
                if cls and (_PORTFOLIO_SKIP_CLS & set(cls)):
                    continue
                if ch.tag == "p":
                    st = ParagraphStyle("pf_p", parent=s_body, leftIndent=indent + body_indent)
                    flows.append(Paragraph(_node_markup(ch), st))
                elif ch.tag in ("ul", "ol"):
                    for li in ch.children:
                        if li.tag == "li":
                            st = ParagraphStyle("pf_li", parent=s_bullet,
                                                leftIndent=indent + bullet_indent)
                            flows.append(Paragraph("• " + _node_markup(li), st))
                elif ch.tag == "table":
                    t = _pf_table(ch, indent)
                    if t is not None:
                        flows.append(t)
                        flows.append(Spacer(1, entry_space))
                elif ch.tag == "div" and "flow" in cls:
                    st = ParagraphStyle("pf_flow", parent=s_body, fontName="CN",
                                        fontSize=body_size - 1, leading=(body_size - 1) * 1.4,
                                        leftIndent=indent, backColor=block_bg, borderPadding=6,
                                        borderRadius=4)
                    for chunk in _pf_flow_chunks(ch.text, st, avail_flow_h):
                        flows.append(Preformatted(chunk, st))     # chunk 已过 _pdf_safe
                    flows.append(Spacer(1, entry_space))
                elif ch.tag in ("div", "blockquote", "section"):
                    flows.extend(_blocks(ch.children, indent))
            return flows

        def _pf_case(sec, ap=False):
            flows = [Spacer(1, pf["case_space"])]
            for c in sec.children:
                cls = c.cls()
                if "hero" in cls:
                    flows.extend(_pf_hero(c, ap))
                elif "facts" in cls:
                    t = _pf_facts(c)
                    if t is not None:
                        flows.append(t)
                        flows.append(Spacer(1, entry_space / 2))
                elif "case-quote" in cls:
                    flows.append(Paragraph(_node_markup(c),
                                           ParagraphStyle("pf_cq", parent=s_body, leftIndent=10)))
                elif "sub" in cls:
                    st = _s(c, "sub-title")
                    if st:
                        flows.append(Spacer(1, heading_sb))
                        flows.append(Paragraph(_node_markup(st),
                                               _pf_style("pf_sub", s_head, pf["sub"])))
                        flows.append(Spacer(1, heading_sa))
                    flows.extend(_blocks(c.children))
            return flows

        for child in container.children:
            cls = child.cls()
            if "cover" in cls:
                # 先取文案（页眉 / 水印 / 页脚共用；全部来自封面元信息 ⇒ 零新字段）
                for d in child.children:
                    dcls = d.cls()
                    if "cover-title" in dcls:
                        footer_title_pt = d.text          # 页脚左侧文案 = 合册主标题
                    elif "cover-meta" in dcls:
                        for m in d.children:
                            if m.tag == "div":
                                cover_meta_plain.append(m.text)   # 页眉 / 水印派生源
                if header_mode != "none":
                    header_left_pt, header_right_pt = _pf_header_parts(css, cover_meta_plain)
                if wm_mode != "none":
                    wm_text_pt = _pf_watermark_text(css, cover_meta_plain, wm_mode)

                def _cover_items():
                    """构建封面 flowables（**可重复调用**：测量一次、渲染一次）。

                    ⚠️ 必须重建而非复用：wrap() 会改 flowable 内部状态，
                       测量过的实例不能再拿去 build（沿用本文件既有纪律「重跑而非复用」）。
                    按 DOM 顺序渲染（标题 / 装饰线 / 元信息）—— 顺序即版式，勿重排。
                    """
                    items = []
                    for d in child.children:
                        dcls = d.cls()
                        if "cover-title" in dcls:
                            items.append(Paragraph(
                                _node_markup(d),
                                _pf_style("pf_cov", s_head, pf["book"],
                                          textColor=accent, alignment=1)))
                        elif "cover-rule" in dcls:
                            items.append(HRFlowable(width=96, thickness=3, color=accent,
                                                    hAlign="CENTER",
                                                    spaceBefore=pf["cover_rule_gap"],
                                                    spaceAfter=0))
                        elif "cover-meta" in dcls:
                            items.append(Spacer(1, pf["cover_gap"]))
                            for m in d.children:
                                if m.tag == "div":
                                    items.append(Paragraph(
                                        _node_markup(m),
                                        _pf_style("pf_cm", s_body, info_size,
                                                  alignment=1)))
                    return items

                # ---- 动态上留白（刀 D · F37）----
                # 旧实现固定 Spacer(1, 36) ⇒ 内容全部堆在上半页，下半页空白（owner 反馈）。
                # 现按「可用高 − 内容高」的 --cover-top-ratio 分配上留白（0.5 = 数学居中）。
                # ⚠️ clamp 是必需的：留白算大 ⇒ 封面溢出成 2 页 ⇒ _total 与页脚口径全错。
                # ⚠️ 此处 **拿不到 doc_**（SimpleDocTemplate 在 story 构建之后才创建）
                #    ⇒ 页面尺寸直接取 A4，与 doc_kw 的 pagesize 同源。
                _pw, _ph = A4
                _cov_w = _pw - 2 * ms * mm
                _cov_h = _ph - 2 * mt * mm
                _cov_items = _cover_items()                  # 测量实例
                _cov_need = sum(it.wrap(_cov_w, _cov_h)[1]
                                + getattr(it, "spaceBefore", 0)
                                + getattr(it, "spaceAfter", 0) for it in _cov_items)
                _cov_slack = max(_cov_h - _cov_need, 0.0)
                _cov_pad = max(_cov_slack * pf["cover_top_ratio"], min(24.0, _cov_slack))
                # ⚠️ 走 stderr：stdout 是 --format pages 的**契约输出**（只允许 `N 页`），
                #    往 stdout 打印诊断会直接破坏该契约（实测踩过）。
                print(f"  [封面] 可用高 {_cov_h:.0f}pt / 内容高 {_cov_need:.0f}pt"
                      f" / 上留白 {_cov_pad:.0f}pt（ratio={pf['cover_top_ratio']}）",
                      file=sys.stderr)
                story.append(Spacer(1, _cov_pad))
                story.extend(_cover_items())                 # 重建后渲染
                if cover_page == "always":
                    # 封面独立成页 ⇒ 页脚回调天然干净：第 1 页 = 封面（不画），其后 = 正文（画）
                    story.append(PageBreak())
            elif "toc" in cls:
                # 目录页（案例数 ≥ 2 时「目录块」才非空 ⇒ 才会出现该节点）
                from reportlab.platypus.tableofcontents import TableOfContents
                story.append(Paragraph("目录",
                                       _pf_style("pf_toc_t", s_head, pf["case"],
                                                 textColor=accent)))
                story.append(Spacer(1, heading_sa + 2))
                story.append(TableOfContents(
                    levelStyles=[_pf_style("pf_toc0", s_body, pf["body"])],
                    dotsMinLevel=0))    # dotsMinLevel=0 ⇒ 0 级（案例级）也带点线引导
                toc_needed = True
                story.append(PageBreak())
            elif child.tag == "section" and "case" in cls:
                story.extend(_pf_case(child))
            elif child.tag == "section" and "appendix" in cls:
                # F40：附录区（置尾 · 不计案例数 · 不进目录）
                story.extend(_pf_case(child, ap=True))



    else:
        for child in container.children:
            if child.tag == "div" and "header" in child.cls():
                # 找 .header-left（跳过 shape-layer 等装饰 div）
                left = next((c for c in child.children if c.tag == "div" and "header-left" in c.cls()), None)
                name_node = child.find_first("span") if False else (left.find_first("span") if left else None)
                # 左列：姓名+意向 行 + 2×2 信息
                left_flows = []
                name_text, intent_text = "", ""
                spans = left.find_all("span") if left else []
                for sp in spans:
                    if "name" in sp.cls():
                        name_text = sp.text
                    elif "intent" in sp.cls():
                        intent_text = sp.text
                if name_text or intent_text:
                    html = f'<font size="{int(title_size)}"><b>{name_text}</b></font>&nbsp;&nbsp;&nbsp;&nbsp;<font size="{int(intent_size)}">{intent_text}</font>'
                    left_flows.append(Paragraph(html, s_intent))
                contact = left.find_first("div") if left else None
                rows = []
                if contact:
                    for item in contact.children:
                        if item.tag == "div" and "item" in item.cls():
                            tag, val = "", ""
                            for kind, part in item.content:      # ★ 遍历 content（含 div 直接文本 t 节点）→ 修复值空白
                                if kind == "t":
                                    val += _pdf_safe(part.strip())
                                elif part.tag == "span" and "tag" in part.cls():
                                    tag = part.text
                                else:
                                    val += part.text
                            gap = "&nbsp;" if val else ""   # 标签"电话："与值的分隔（HTML 端用 .tag margin-right 等效）
                            rows.append(Paragraph(f'<font color="{header_tag_hex}"><b>{tag}</b></font>{gap}{val}', s_item))
                if rows:
                    left_flows.append(Spacer(1, name_to_info))  # ★ 姓名行与信息间距（--name-to-info）
                    pair = [rows[i:i + 2] for i in range(0, len(rows), 2)]
                    info_col_w = (page_w_cm - photo_w_cm - header_pad_right * 0.0353
                                  - header_pad_left * 0.0353 - photo_gap * 0.0353) / 2  # 信息列宽（cm）
                    left_flows.append(Table(pair, colWidths=[max(info_col_w, 3.0) * cm] * 2,
                                            style=[("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                   ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                                                   ("TOPPADDING", (0, 0), (-1, -1), info_line_gap / 2),
                                                   ("BOTTOMPADDING", (0, 0), (-1, -1), info_line_gap / 2)]))
                # 照片
                photo_flow = Spacer(1, 1)
                img = child.find_first("img")
                if img:
                    src = img.attrs.get("src", "")
                    if src and Path(src).exists():
                        from reportlab.lib.utils import ImageReader
                        try:
                            ir = ImageReader(src)
                            iw, ih = ir.getSize()
                            pw = photo_w_cm * cm                    # ★ 照片宽（--photo-width）
                            ph = pw * ih / iw
                            photo_h_pt = ph                         # 记录照片高度（--header-bg-height: auto 用）
                            photo_flow = Image(src, width=pw, height=ph)
                        except Exception:
                            pass
                # 照片贴右固定；左列 = 内容宽 - 照片宽 - header右内边距；照片与信息间距由 --photo-gap 承担
                col_left = page_w_cm - photo_w_cm - header_pad_right * 0.0353
                header_style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (0, 0), header_pad_left),
                                ("RIGHTPADDING", (0, 0), (0, 0), 0),
                                ("TOPPADDING", (0, 0), (0, 0), header_pad_top),
                                ("BOTTOMPADDING", (0, 0), (0, 0), header_pad_bottom),
                                ("LEFTPADDING", (1, 0), (1, 0), 0),
                                ("RIGHTPADDING", (1, 0), (1, 0), header_pad_right),
                                ("TOPPADDING", (1, 0), (1, 0), header_pad_top + photo_margin_top),
                                ("BOTTOMPADDING", (1, 0), (1, 0), 0)]
                if header_bg_type == "color":
                    # 纯色：Table 画背景块（含圆角）
                    header_style.insert(0, ("BACKGROUND", (0, 0), (-1, -1), block_bg))
                    header_style.append(("ROUNDEDCORNERS", [8, 8, 8, 8]))
                # shape/image 类型：Table 透明，背景由 onPage canvas 绘制（内容浮在背景上）
                header_tbl = Table([[left_flows, photo_flow]],
                                   colWidths=[col_left * cm, photo_w_cm * cm],
                                   style=header_style)
                story.append(header_tbl)
                story.append(Spacer(1, 6))  # header 与首节之间的固定小间距（节标题上方由 --heading-space-before 控制）

            elif child.tag == "section" and "section" in child.cls():
                title = next((c for c in child.children if c.tag == "div" and "section-title" in c.cls()), None)
                if title:
                    story.append(Spacer(1, heading_sb))  # ★ 节标题上方间距（--heading-space-before；实测 reportlab Table 内 Paragraph spaceBefore 不生效，Spacer 为唯一生效源）
                    head_para = Paragraph(title.text, s_head)
                    head_line = HRFlowable(width="100%", thickness=1.2, color=line_c)
                    story.append(Table([[head_para, head_line]], colWidths=[None, "*"],
                                       style=[("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                              ("LEFTPADDING", (0, 0), (0, 0), 8),
                                              ("RIGHTPADDING", (0, 0), (0, 0), 8),
                                              ("TOPPADDING", (0, 0), (-1, -1), 3),
                                              ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                              ("LEFTPADDING", (1, 0), (1, 0), 8),
                                              ("RIGHTPADDING", (1, 0), (1, 0), 0)]))
                    story.append(Spacer(1, heading_sa))  # ★ 节标题下方间距（--heading-space-after）
                # 节内正文统一右平移 2 字符（28pt）— 节标题保持顶格；粗体经 _node_markup 保留（原 _to_pdf(sub.text)
                # 走 Node.text 纯文本会把 <b> 剥掉 → PDF 正文粗体失效，已废弃）
                first_entry = True
                for sub in child.children:
                    if sub.tag == "p":
                        style_p = ParagraphStyle("p_indent", parent=s_body, leftIndent=body_indent)
                        story.append(Paragraph(_node_markup(sub), style_p))
                    elif sub.tag == "div" and "entry" in sub.cls():
                        if not first_entry:
                            story.append(Spacer(1, entry_space))  # ★ 条目之间间距（--entry-space）
                        first_entry = False
                        meta = next((c for c in sub.children if c.tag == "div" and "entry-meta" in c.cls()), None)
                        if meta:
                            style_meta = ParagraphStyle("meta_indent", parent=s_meta, leftIndent=body_indent)
                            story.append(Paragraph(_node_markup(meta), style_meta))
                        ul = sub.find_first("ul")
                        if ul:
                            for li in ul.children:
                                if li.tag == "li":
                                    style_li = ParagraphStyle("li_indent", parent=s_bullet, leftIndent=bullet_indent)
                                    story.append(Paragraph("• " + _node_markup(li), style_li))

    def _collect_toc_titles(flowable, out):
        """收集 flowable 里的案例标题段（样式名 pf_ct），**含嵌套表格单元格**。

        ⚠️ reportlab 的 afterFlowable 只派发**顶层** flowable：案例标题在 .hero 表格里
           ⇒ 不对表格下钻就一条目录也收不到（目录永远 = 占位符，且 multiBuild 首趟即"满足"）。
           下钻须能处理「列表」这一层：单元格内容往往是裸 flowable 列表。
        """
        if isinstance(flowable, (list, tuple)):
            # ⚠️ 单元格内容常是**裸 flowable 列表**（reportlab 的 _cellvalues 只到"行"这一层）
            #    ⇒ 不在此处分派就永远递归不进表格里的段落（目录会一条都收不到）。
            for sub in flowable:
                if sub is not None:
                    _collect_toc_titles(sub, out)
            return
        if isinstance(flowable, Paragraph):
            if getattr(getattr(flowable, "style", None), "name", "") == "pf_ct":
                out.append(flowable)
            return
        for cell in (getattr(flowable, "_cellvalues", None) or ()):
            _collect_toc_titles(cell, out)

    class _PortfolioDocTemplate(SimpleDocTemplate):
        """合册专用：afterFlowable → 为案例标题段（样式名 pf_ct）发 TOCEntry。
        仅在合册 + 存在目录时启用；简历路径不走 multiBuild（保持单趟 build ⇒ 零变化）。"""

        def afterFlowable(self, flowable):
            found = []
            _collect_toc_titles(flowable, found)
            # 页码口径与页脚一致：封面独立成页时封面不计入 ⇒ 目录页码 = 物理页 − 1
            off = 1 if cover_page == "always" else 0
            for p in found:
                self.notify("TOCEntry", (0, p.getPlainText(), self.page - off))

    doc_kw = dict(pagesize=(A4 if page_height is None else (A4[0], float(page_height))),
                  topMargin=mt * mm, bottomMargin=mt * mm,
                  leftMargin=ms * mm, rightMargin=ms * mm)
    use_toc = bool(profile == "portfolio" and toc_needed)
    if footer_mode == "page-x-of-y" and not _total:
        # 首趟：数总页数（story 会被 build 消费 ⇒ 递归重跑本函数、flowables 重造，而非复用）
        cnt = _PortfolioDocTemplate(_io.BytesIO(), **doc_kw)
        if use_toc:
            cnt.multiBuild(story)      # 与正式渲染同一路径 ⇒ 目录占位高度一致 ⇒ 页数可信
        else:
            cnt.build(story)
        return html_to_pdf(html_text, out_path, profile, _total=cnt.page,
                           page_height=page_height)
    if use_toc:
        doc = _PortfolioDocTemplate(str(out_path), **doc_kw)
        # reportlab 5.x：页面回调是 build() 参数；multiBuild 才能把目录页码回填
        doc.multiBuild(story, onFirstPage=_on_page, onLaterPages=_on_page)
    else:
        doc = SimpleDocTemplate(str(out_path), **doc_kw)
        doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return doc.page


# ---------- HTML → DOCX（最简转换，可接受效果损失） ----------

def _set_font(run, name: str, size: float, bold: bool, color: str = None):
    from docx.shared import Pt, RGBColor
    from docx.oxml.ns import qn
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts")
    if rFonts is None:
        rFonts = rPr.makeelement(qn("w:rFonts"), {})
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), name)


def _add_shading(p, fill_hex: str):
    from docx.oxml.ns import qn
    pPr = p._p.get_or_add_pPr()
    shd = pPr.makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): fill_hex})
    pPr.append(shd)


def _add_run_shading(run, fill_hex: str):
    """run 级底纹（刀 B：.badge 真底色 —— DOCX 无圆角，用底色 + accent 字近似）。"""
    from docx.oxml.ns import qn
    rPr = run._element.get_or_add_rPr()
    rPr.append(rPr.makeelement(qn("w:shd"),
                               {qn("w:val"): "clear", qn("w:color"): "auto",
                                qn("w:fill"): fill_hex}))


def _add_left_border(p, color_hex: str, sz_eighth: int = 18):
    """段落左边框（刀 B：.hero 左竖条）。插在 w:shd 之前（OOXML 顺序：pBdr < shd）。"""
    from docx.oxml.ns import qn
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn("w:pBdr"), {})
    pBdr.append(pPr.makeelement(qn("w:left"), {
        qn("w:val"): "single", qn("w:sz"): str(sz_eighth),
        qn("w:space"): "6", qn("w:color"): color_hex}))
    shd = pPr.find(qn("w:shd"))
    if shd is not None:
        shd.addprevious(pBdr)
    else:
        pPr.append(pBdr)


def _add_field(p, instr: str, placeholder: str = "", font=None, size=None, color=None):
    """插入 Word 域（刀 B：页脚页码 / 目录）。dirty=true ⇒ Word/WPS 打开时自动求值。
    域结果文本取 rPr 的字号字体 ⇒ 必须显式 _set_font，否则页码会与页脚其余文字不同号。"""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    r = p.add_run()
    if font:
        _set_font(r, font, size, False, color)

    def _el(tag, **attrs):
        e = OxmlElement("w:" + tag)
        for k, v in attrs.items():
            e.set(qn("w:" + k), v)
        return e

    r._r.append(_el("fldChar", fldCharType="begin", dirty="true"))
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    r._r.append(it)
    r._r.append(_el("fldChar", fldCharType="separate"))
    if placeholder:
        t = OxmlElement("w:t")
        t.text = placeholder
        r._r.append(t)
    r._r.append(_el("fldChar", fldCharType="end"))
    return r


def _center_section_vertically(sec) -> None:
    """封面节纵向居中（刀 D · F37）：python-docx 原生支持 ⇒ sectPr/vAlign=center。

    ⚠️ 只对「封面独立成节」使用 —— 多页节里居中会把整节内容拉到垂直中间。
    """
    try:
        from docx.enum.section import WD_ALIGN_VERTICAL
        sec.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    except Exception:
        pass      # 老版本 python-docx 无该枚举 ⇒ 静默不居中（不打断导出）


def _docx_header(sec, left: str, right: str, ms: float, small: float, color: str,
                 accent: str):
    """DOCX 页眉（刀 D · F38）：左 = 姓名（full 档附加联系），右 = 应聘 公司 · 岗位。

    Word 逐页自动重复（放进 sec.header 即生效）⇒ 无需像 PDF 那样手工画。
    """
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.shared import Cm
    sec.header.is_linked_to_previous = False
    p = sec.header.paragraphs[0]
    p.paragraph_format.tab_stops.add_tab_stop(Cm(21.0 - 2 * ms / 10.0), WD_TAB_ALIGNMENT.RIGHT)
    _set_font(p.add_run(left or ""), "微软雅黑", small, False, color)
    if right:
        p.add_run("\t")
        _set_font(p.add_run(right), "微软雅黑", small, True, accent)


def _docx_footer(sec, mode: str, title: str, ms: float, small: float, use_section_pages: bool,
                 color: str):
    """DOCX 页脚（刀 B）：左 = 合册标题，右 = 页码（Word 域，打开时自动求值）。
    use_section_pages=True ⇒ SECTIONPAGES（正文节页数，封面已排除）；False ⇒ NUMPAGES。"""
    from docx.shared import Cm
    from docx.enum.text import WD_TAB_ALIGNMENT
    sec.footer.is_linked_to_previous = False
    p = sec.footer.paragraphs[0]
    p.paragraph_format.tab_stops.add_tab_stop(Cm(21.0 - 2 * ms / 10.0), WD_TAB_ALIGNMENT.RIGHT)
    _set_font(p.add_run(title or ""), "微软雅黑", small, False, color)
    p.add_run("\t")
    _set_font(p.add_run("第 "), "微软雅黑", small, False, color)
    _add_field(p, "PAGE", font="微软雅黑", size=small, color=color)
    if mode == "page-x-of-y":
        _set_font(p.add_run(" 页 / 共 "), "微软雅黑", small, False, color)
        _add_field(p, "SECTIONPAGES" if use_section_pages else "NUMPAGES",
                   font="微软雅黑", size=small, color=color)
    _set_font(p.add_run(" 页"), "微软雅黑", small, False, color)


def _docx_body_section(doc, ms: float, mt: float, footer_mode: str, title: str, small: float,
                       color: str, header_mode: str = "none", header_left: str = "",
                       header_right: str = "", accent: str = ""):
    """封面独占一节 ⇒ 正文另起一节：页码自 1 重排（封面不计入），页眉 / 页脚只挂正文节。"""
    from docx.enum.section import WD_SECTION
    from docx.shared import Mm
    from docx.oxml.ns import qn
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.top_margin = Mm(mt)
    sec.bottom_margin = Mm(mt)
    sec.left_margin = Mm(ms)
    sec.right_margin = Mm(ms)
    sec._sectPr.append(sec._sectPr.makeelement(qn("w:pgNumType"), {qn("w:start"): "1"}))
    if footer_mode != "none":
        _docx_footer(sec, footer_mode, title, ms, small, True, color)
    if header_mode != "none" and (header_left or header_right):
        _docx_header(sec, header_left, header_right, ms, small, color, accent)
    return sec


def _fill_rich(p, parts, font="微软雅黑", size=10.5, color="1A1A1A"):
    """[(text, bold)] → docx runs。"""
    for text, bold in parts:
        _set_font(p.add_run(text), font, size, bold, color)


def html_to_docx(html_text: str, out_path: Path, profile: str = "resume"):
    from docx import Document
    from docx.shared import Cm, Pt

    css = extract_css_vars(html_text)
    def cv(var, default):
        # docx 颜色值无需 # 前缀（RGBColor.from_string 期望）
        return css.get(var, default).strip().lstrip("#")
    def cv_px(var, default_px):
        raw = css.get(var, f"{default_px}px").strip()
        if raw.endswith("px"):
            return float(raw[:-2]) * 0.75
        if raw.endswith("pt"):
            return float(raw[:-2])
        if raw.endswith("mm"):
            return float(raw[:-2]) * 2.835
        return float(raw) * 0.75
    accent = cv("--accent", "1564BF")
    text_c = cv("--text", "1A1A1A")
    block_bg = cv("--block-bg", "EAF2FA")
    title_size = float(cv("--title-size", "20").rstrip("pt"))
    heading_size = float(cv("--heading-size", "14").rstrip("pt"))
    body_size = float(cv("--body-size", "10.5").rstrip("pt"))
    intent_size = float(cv("--intent-size", "12").rstrip("pt"))
    header_text_color = cv("--header-text-color", "1A1A1A")
    if header_text_color.startswith("var("):
        header_text_color = cv(header_text_color[4:-1].strip(), "1A1A1A")
    header_tag_hex = cv("--header-tag-color", "1564BF")
    if header_tag_hex.startswith("var("):
        header_tag_hex = cv(header_tag_hex[4:-1].strip(), "1564BF")
    body_indent = cv_px("--body-indent", 28)      # 节内正文右平移
    bullet_indent = cv_px("--bullet-indent", 46)  # bullet 再右平移
    heading_sb = cv_px("--heading-space-before", 14)
    heading_sa = cv_px("--heading-space-after", 8)
    entry_space = cv_px("--entry-space", 8)
    photo_w_cm = float(cv("--photo-width", "3.5").rstrip("cm"))  # 证件照宽（--photo-width）

    doc = Document()
    for section in doc.sections:
        from docx.shared import Mm
        mt = float(cv("--page-margin-top", "18").rstrip("mm"))
        ms = float(cv("--page-margin-side", "16").rstrip("mm"))
        section.top_margin = Mm(mt); section.bottom_margin = Mm(mt)
        section.left_margin = Mm(ms); section.right_margin = Mm(ms)

    root = parse_dom(html_text)
    body = _find_body(root)

    if profile == "portfolio":
        # ---- 合册 profile：封面 + 案例块（表格 / 流程块用可用能力近似，同 docx 一貫取舍） ----
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        pf = _portfolio_metrics(cv, cv_px)          # 与 PDF 侧共用同一处读取（跨格式同源）
        # ---- 刀 B：分页 / 页脚开关 + 派生色（与 PDF 同源：由 --accent 预混，不引入新色）----
        accent_hex = cv("--accent", "1564BF")
        tint_hex = _mix_hex(accent_hex, "FFFFFF", 0.90)      # hero 底（accent 10%）
        deep_hex = _mix_hex(accent_hex, "FFFFFF", 0.82)      # 徽章底（accent 18%）
        cover_page = cv("--cover-page", "always").strip()
        footer_mode = cv("--footer", "page-x-of-y").strip()
        footer_title = ""
        # ---- 刀 D：页眉 / 水印开关 ----
        # ⚠️ --watermark 在 DOCX **未实现**（python-docx 无原生水印，须手写 VML）⇒ 见待办 F39。
        #    这里显式提示一次，避免「以为加了水印」——静默忽略才是最坏的结果。
        header_mode = cv("--header", "auto").strip() or "none"
        wm_mode = cv("--watermark", "trace").strip() or "none"
        header_left = header_right = ""
        cover_meta_plain: list[str] = []

        def _ds(parent, name):
            return next((c for c in parent.children
                         if c.tag == "div" and name in c.cls()), None)

        def _df_table(tbl, indent=0.0):
            grid = []
            for tr in tbl.find_all("tr"):
                cells = [c for c in tr.children if c.tag in ("td", "th")]
                if cells:
                    grid.append(cells)
            if not grid:
                return
            ncol = max(len(g) for g in grid)
            t = doc.add_table(rows=len(grid), cols=ncol)
            try:
                t.style = "Table Grid"
            except KeyError:
                pass
            for ri, cells in enumerate(grid):
                for ci in range(ncol):
                    para = t.cell(ri, ci).paragraphs[0]
                    if ci < len(cells):
                        _fill_rich(para, rich_text(cells[ci]), size=body_size, color=text_c)
                    if ri == 0:
                        _add_shading(para, block_bg)          # 表头底色（复用既有能力）

        def _df_blocks(nodes, indent=0.0):
            for ch in nodes:
                cls = ch.cls()
                if cls and (_PORTFOLIO_SKIP_CLS & set(cls)):
                    continue
                if ch.tag == "p":
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Pt(indent + body_indent)
                    _fill_rich(p, rich_text(ch), size=body_size, color=text_c)
                elif ch.tag in ("ul", "ol"):
                    for li in ch.children:
                        if li.tag == "li":
                            p = doc.add_paragraph()
                            p.paragraph_format.left_indent = Pt(indent + bullet_indent)
                            _set_font(p.add_run("• "), "微软雅黑", body_size, False, text_c)
                            _fill_rich(p, rich_text(li), size=body_size, color=text_c)
                elif ch.tag == "table":
                    _df_table(ch, indent)
                elif ch.tag == "div" and "flow" in cls:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Pt(indent)
                    _add_shading(p, block_bg)
                    _set_font(p.add_run(ch.text), "Consolas", body_size - 1, False, text_c)
                elif ch.tag in ("div", "blockquote", "section"):
                    _df_blocks(ch.children, indent)

        def _df_hero(hero, ap=False):
            """案例标题区（刀 B）：标题挂 Heading 1（**目录域只收集标题样式**，不挂则域为空）·
            徽章行 = 左竖条 + 底色 + run 级底纹。
            ⚠️ F40：附录（ap=True）**不挂 Heading 1** ⇒ **不进 Word 目录域**
               （目录域只收集标题样式）；字号降为小节级、色转正文色 ⇒ 视觉弱化。"""
            t = _ds(hero, "case-title")
            if t is not None:
                p = doc.add_paragraph()
                if not ap:
                    try:
                        p.style = doc.styles["Heading 1"]
                    except KeyError:
                        pass
                p.paragraph_format.space_before = Pt(pf["case_space"])
                p.paragraph_format.space_after = Pt(2)
                _fill_rich(p, rich_text(t), size=pf["sub"] if ap else pf["case"],
                           color=text_c if ap else accent)
            bd = _ds(hero, "hero-badges")
            if bd is not None:
                badges = [sp for sp in bd.children
                          if sp.tag == "span" and "badge" in sp.cls()]
                if badges:
                    p = doc.add_paragraph()
                    _add_shading(p, tint_hex)
                    _add_left_border(p, accent_hex, 18)
                    p.paragraph_format.left_indent = Pt(6)
                    p.paragraph_format.space_after = Pt(4)
                    first = True
                    for sp in badges:
                        if not first:
                            p.add_run("  ")
                        first = False
                        plain = "plain" in sp.cls()
                        run = p.add_run(sp.text)
                        _set_font(run, "微软雅黑", pf["small"], not plain,
                                  text_c if plain else accent)
                        if not plain:
                            _add_run_shading(run, deep_hex)

        def _df_facts(node):
            """元信息卡（刀 B）：2 列 = 4 列**无边框表**（标签 accent 粗体 + 值）· 与 PDF 同构。
            ⚠️ 刻意不做「降级为段落」（与设计稿 v1 的取向相反）：DOCX 同样会被打开、被打印，
               跨格式观感差距过大与「视觉同源」目标冲突。"""
            items = []
            for r in node.children:
                if r.tag == "div" and "row" in r.cls():
                    k, spans = _facts_row_parts(r)
                    val = []
                    for kind, v in spans:
                        if kind == "c":
                            val.extend(rich_text(v))
                        else:
                            t_ = _pdf_safe(v).strip()
                            if t_:
                                val.append((t_, False))
                    items.append((rich_text(k) if k is not None else [], val))
            if not items:
                return
            grid = [items[i:i + 2] for i in range(0, len(items), 2)]
            tbl = doc.add_table(rows=len(grid), cols=4)
            for ri, pair in enumerate(grid):
                for ci2 in range(2):
                    if ci2 >= len(pair):
                        continue
                    cells = tbl.rows[ri].cells
                    kp = cells[ci2 * 2].paragraphs[0]
                    vp = cells[ci2 * 2 + 1].paragraphs[0]
                    for pp in (kp, vp):
                        pp.paragraph_format.space_before = Pt(2)
                        pp.paragraph_format.space_after = Pt(2)
                    if pair[ci2][0]:
                        _fill_rich(kp, pair[ci2][0], size=body_size, color=accent)
                    _fill_rich(vp, pair[ci2][1], size=body_size, color=text_c)

        def _df_case(sec, ap=False):
            for c in sec.children:
                cls = c.cls()
                if "hero" in cls:
                    _df_hero(c, ap)
                elif "facts" in cls:
                    _df_facts(c)
                elif "case-quote" in cls:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Pt(10)
                    _fill_rich(p, rich_text(c), size=body_size, color=text_c)
                elif "sub" in cls:
                    st = _ds(c, "sub-title")
                    if st:
                        p = doc.add_paragraph()
                        p.paragraph_format.space_before = Pt(heading_sb)
                        p.paragraph_format.space_after = Pt(heading_sa)
                        _fill_rich(p, rich_text(st), size=pf["sub"], color=text_c)
                    _df_blocks(c.children)

        for node in body.children:
            cls = node.cls()
            if "cover" in cls:
                if cover_page == "always":
                    # 封面纵向居中（刀 D · F37）：DOCX 走节级 vAlign；封面独立成节时才安全
                    _center_section_vertically(doc.sections[0])
                for d in node.children:
                    dcls = d.cls()
                    if "cover-title" in dcls:
                        footer_title = re.sub(r"<[^>]+>", "", d.text)
                        p = doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        _fill_rich(p, rich_text(d), size=pf["book"], color=accent)
                    elif "cover-meta" in dcls:
                        first_meta = True
                        for m in d.children:
                            if m.tag == "div":
                                cover_meta_plain.append(m.text)
                                p = doc.add_paragraph()
                                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                if first_meta:
                                    # 标题 → 元信息 总间距（刀 D）：DOCX 不渲染装饰线，
                                    # 故取「标题→线 + 线→元信息」两段之和，与 PDF/HTML 观感对齐。
                                    p.paragraph_format.space_before = Pt(
                                        pf["cover_rule_gap"] + pf["cover_gap"])
                                    first_meta = False
                                _fill_rich(p, rich_text(m), size=body_size, color=text_c)
                if header_mode != "none":
                    header_left, header_right = _pf_header_parts(
                        extract_css_vars(html_text), cover_meta_plain)
                if cover_page == "always":
                    # DOCX 无「页级」回调 ⇒ 封面独立成页 = 独立分节（页码自正文节重排）
                    _docx_body_section(doc, ms, mt, footer_mode, footer_title,
                                       pf["small"], text_c, header_mode, header_left,
                                       header_right, accent)
            elif "toc" in cls:
                # 目录（刀 B）：插 Word TOC 域；Word/WPS 打开时自动更新（dirty=true）
                p = doc.add_paragraph()
                _fill_rich(p, [("目录", True)], size=pf["case"], color=accent)
                _add_field(doc.add_paragraph(), 'TOC \\o "1-1" \\h \\z \\u',
                           placeholder="（右键 → 更新域，生成目录页码）",
                           font="微软雅黑", size=pf["small"], color=text_c)
                doc.add_page_break()
            elif node.tag == "section" and "case" in cls:
                _df_case(node)
            elif node.tag == "section" and "appendix" in cls:
                # F40：附录区（置尾 · 不计案例数 · 不进目录域）
                _df_case(node, ap=True)
        if cover_page != "always":
            # 封面未独立成节 ⇒ 页眉 / 页脚落在第 1 节（含封面 ⇒ 页码用 NUMPAGES）
            if footer_mode != "none":
                _docx_footer(doc.sections[0], footer_mode, footer_title, ms, pf["small"],
                             False, text_c)
            if header_mode != "none" and (header_left or header_right):
                _docx_header(doc.sections[0], header_left, header_right, ms, pf["small"],
                             text_c, accent)
        if wm_mode != "none":
            print("ℹ️ DOCX 不生成水印（--watermark 仅对 PDF / HTML 生效；DOCX 需手写 VML，"
                  "见待办 F39）")



    else:
        for node in body.children:
            if node.tag == "div" and "header" in node.cls():
                # 找 .header-left（跳过 shape-layer 等装饰 div）
                left = next((c for c in node.children if c.tag == "div" and "header-left" in c.cls()), None)
                # 姓名 + 意向（同段）
                p = doc.add_paragraph()
                spans = left.find_all("span") if left else []
                for sp in spans:
                    if "name" in sp.cls():
                        _fill_rich(p, rich_text(sp), size=title_size, color=header_text_color)
                    elif "intent" in sp.cls():
                        _set_font(p.add_run("　　"), "微软雅黑", intent_size, False, header_text_color)
                        _fill_rich(p, rich_text(sp), size=intent_size, color=header_text_color)
                # 2×2 信息
                contact = left.find_first("div") if left else None
                if contact:
                    for item in contact.children:
                        if item.tag == "div" and "item" in item.cls():
                            tag_parts, val_parts = [], []
                            for kind, part in item.content:      # ★ 遍历 content（含 div 直接文本 t 节点）→ 修复值空白
                                if kind == "t":
                                    txt = part.strip()
                                    if txt:
                                        val_parts.append((_pdf_safe(txt), False))
                                elif part.tag == "span" and "tag" in part.cls():
                                    tag_parts.extend(rich_text(part))
                                else:
                                    val_parts.extend(rich_text(part))
                            p = doc.add_paragraph()
                            if tag_parts:
                                _fill_rich(p, tag_parts, size=body_size, color=header_tag_hex)
                            if val_parts:
                                p.add_run(" ")  # 标签"电话："与值的分隔（HTML 端用 .tag margin-right 等效）
                                _fill_rich(p, val_parts, size=body_size, color=header_text_color)
                # 照片
                img = node.find_first("img")
                if img:
                    src = img.attrs.get("src", "")
                    if src and Path(src).exists():
                        try:
                            doc.add_picture(src, width=Cm(photo_w_cm))
                        except Exception:
                            pass

            elif node.tag == "section" and "section" in node.cls():
                title = next((c for c in node.children if c.tag == "div" and "section-title" in c.cls()), None)
                if title:
                    p = doc.add_paragraph()
                    p.paragraph_format.space_before = Pt(heading_sb)  # ★ 节标题上方（--heading-space-before）
                    p.paragraph_format.space_after = Pt(heading_sa)   # ★ 节标题下方（--heading-space-after）
                    _fill_rich(p, rich_text(title), size=heading_size, color=text_c)
                first_entry = True
                for sub in node.children:
                    if sub.tag == "p":
                        p = doc.add_paragraph()
                        p.paragraph_format.left_indent = Pt(body_indent)
                        _fill_rich(p, rich_text(sub), size=body_size, color=text_c)
                    elif sub.tag == "div" and "entry" in sub.cls():
                        if not first_entry:
                            sp = doc.add_paragraph()
                            sp.paragraph_format.space_before = Pt(entry_space)  # ★ 条目间距（--entry-space）
                        first_entry = False
                        meta = next((c for c in sub.children if c.tag == "div" and "entry-meta" in c.cls()), None)
                        if meta:
                            p = doc.add_paragraph()
                            p.paragraph_format.left_indent = Pt(body_indent)
                            _fill_rich(p, rich_text(meta), size=body_size, color=accent)
                        ul = sub.find_first("ul")
                        if ul:
                            for li in ul.children:
                                if li.tag == "li":
                                    p = doc.add_paragraph()
                                    p.paragraph_format.left_indent = Pt(bullet_indent)
                                    _set_font(p.add_run("• "), "微软雅黑", body_size, False, text_c)
                                    _fill_rich(p, rich_text(li), size=body_size, color=text_c)

    # 行距统一应用（来自模板 --line-spacing 变量）
    ls = float(css.get("--line-spacing", "1.6").strip())
    for p in doc.paragraphs:
        p.paragraph_format.line_spacing = ls

    doc.save(str(out_path))
    return out_path


# ---------- 入口 ----------

def _embed_photo_as_data_uri(html_text: str) -> str:
    """把 img src 本地路径替换为 data URI（供 HTML 预览直接显示）。"""
    def repl(src):
        if src and Path(src).exists():
            try:
                b64 = base64.b64encode(Path(src).read_bytes()).decode()
                return f"data:image/jpeg;base64,{b64}"
            except Exception:
                return src
        return src
    return re.sub(r'<img src="([^"]+)"', lambda m: f'<img src="{repl(m.group(1))}"', html_text)


_SCRIPT_BLOCK_RE = re.compile(r"<script.*?</script>", re.DOTALL)


def _strip_preview_scripts(template_text: str) -> str:
    """剥离 v1 模板的浏览器预览 script 块（渲染引擎不需要，避免误渲染占位符）。"""
    return _SCRIPT_BLOCK_RE.sub("", template_text)


# 作品集合册示例 md（刀 B-⑦）：**不另造数据集** —— 直接跑真正的 build_data_portfolio，
# 好处是静态预览与真实管线同构（结构一旦漂移，预览立刻暴露），且示例全为占位符（无 PII）。
_PREVIEW_MD_PORTFOLIO = """# 作品集案例合册 · [目标岗位]

> **姓名**：[姓名] ｜ **应聘**：[公司] · [岗位] ｜ **日期**：[YYYY-MM-DD]
> **定位一句**：[一句话 —— 为什么这份合册值得看]
> **派生自**：portfolio-outputs/[case-a].md, [case-b].md @[YYYY-MM-DD]

---

## 案例 1：[案例标题甲]

**[项目名甲]** ｜ **[起止时间]** ｜ **[角色]** ｜ **口径**：[<变体短名>]

**标签**：[跨团队协作] ｜ [AI 赋能] ｜ [0→1]

> [一句话：什么问题、什么动作、什么结果]

### 项目背景

[2-3 句：为什么立项 / 当时环境 / 触发因素]

| 问题 | 影响 |
|------|------|
| [问题点 1] | [影响描述 1] |
| [问题点 2] | [影响描述 2] |

### 关键流程（As-Is → To-Be）

```
[步骤 A]
   ↓
[步骤 B]        ← 瓶颈
   ↓
[目标结果]
```

### 能力体现

- [能力 1]
- [能力 2]

---

## 案例 2：[案例标题乙]

**[项目名乙]** ｜ **[起止时间]** ｜ **[角色]** ｜ **口径**：[<变体短名>]

**标签**：[体系落地] ｜ [自动化]

> [一句话]

### [按 JD 取舍小节]

[正文 / 表格 / 流程块]
"""


def make_static_preview(template_text: str, out_path: Path, profile: str = "resume"):
    """用内置示例数据渲染出静态预览（无 JS 依赖，供浏览器直接查看版式）。
    模板无需嵌入 PREVIEW_DATA：示例数据内置在此处，模板保持纯占位符（引擎用）。
    作品集 profile 走 _PREVIEW_MD_PORTFOLIO + build_data_portfolio ⇒ 与真实管线同构。"""
    if profile == "portfolio":
        data = build_data_portfolio(_PREVIEW_MD_PORTFOLIO, "", {})
        tpl_clean = _strip_preview_scripts(template_text)
        html = mini_render(tpl_clean, data)
        html = re.sub(r"<title>.*?</title>", "<title>合册静态预览（示例内容）</title>", html, count=1)
        out_path.write_text(html, encoding="utf-8")
        return out_path
    data = {
        "姓名": "[姓名]",
        "意向": "求职意向：[目标岗位] ｜ [期望城市]",
        "信息": [
            {"标签": "电话", "值": "[电话]"}, {"标签": "邮箱", "值": "[邮箱]"},
            {"标签": "城市", "值": "[城市]"}, {"标签": "年限", "值": "[工作年限]"},
        ],
        "证件照": "",
        "节": [
            {"标题": "职业定位", "段落": ["[职业定位内容——整段注入]"], "条目": []},
            {"标题": "核心能力", "段落": ["项目管理：xxx｜xxx｜xxx"], "条目": []},
            {"标题": "工作经历", "段落": [], "条目": [
                {"meta": "[起止时间] [公司名] [岗位]", "行": ["[动词] + [做了什么] + [量化结果]"]},
            ]},
            {"标题": "项目经历", "段落": [], "条目": [
                {"meta": "[项目名]", "行": ["[项目一句话背景]"]},
            ]},
            {"标题": "技能与认证", "段落": ["[证书1] ｜ [证书2]"], "条目": []},
            {"标题": "教育背景", "段落": [], "条目": [
                {"meta": "[起止时间] [学校] [专业] · [学历]", "行": []},
            ]},
        ],
    }
    tpl_clean = _strip_preview_scripts(template_text)
    html = mini_render(tpl_clean, data)
    html = re.sub(r"<title>.*?</title>", "<title>模板静态预览（示例内容）</title>", html, count=1)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Export final resume via HTML template (v2.8.1)")
    ap.add_argument("--input", required=True, help="deliverables/02_resume_cn_final.md")
    ap.add_argument("--template", default=None,
                    help="HTML v1 抽象模板（默认 assets/templates/resume-outputs/resume_template.html）")
    ap.add_argument("--format", choices=["html", "pdf", "docx", "all", "preview", "pages",
                                         "png", "png-long"], default="all",
                    help="preview = 用模板内嵌示例数据生成静态预览（改模板后刷新预览用）；"
                         "png = 分页 PNG + 长图 PNG（F25）；png-long = 只出长图")
    ap.add_argument("--profile", choices=["auto", "resume", "portfolio"], default="auto",
                    help="渲染 profile：auto = 读模板头 render-profile 标记，无标记则 resume")
    ap.add_argument("--photo", default=None, help="证件照（可选）")
    ap.add_argument("--theme", default=None, help="配色覆盖（可选，覆盖模板 CSS 变量）")
    ap.add_argument("--png-width", type=int, default=1160,
                    help="PNG 目标宽度 px（默认 1160 = Boss 消息卡片建议宽；1740 = 1.5×）")
    args = ap.parse_args()

    in_path = Path(args.input)

    TEMPLATES = {
        "resume": "resume-outputs/resume_template.html",
        "portfolio": "portfolio-outputs/portfolio_book_template.html",
    }

    def _detect_profile(tpl_file: Path) -> str:
        """模板头自声明（<!-- render-profile: X -->）。无标记 ⇒ resume。"""
        m = re.search(r"<!--\s*render-profile:\s*([\w-]+)\s*-->",
                      tpl_file.read_text(encoding="utf-8"))
        return m.group(1) if m else "resume"

    if args.template:
        tpl_path = Path(args.template)
        profile = args.profile if args.profile != "auto" else _detect_profile(tpl_path)
    else:
        # 不做文件名推断（脆）；auto + 无模板 ⇒ resume（完全向后兼容），
        # 合册须显式给 --template（走自声明）或 --profile portfolio。
        profile = "resume" if args.profile == "auto" else args.profile
        here = Path(__file__).resolve().parent
        tpl_path = here.parent / "assets" / "templates" / TEMPLATES[profile]
    if not tpl_path.exists():
        print(f"❌ 模板不存在: {tpl_path}")
        sys.exit(1)

    if args.format == "preview":
        out = make_static_preview(_inline_palette(tpl_path.read_text(encoding="utf-8")),
                                  in_path.parent / f"{tpl_path.stem}_static_preview.html",
                                  profile)
        if not out:
            sys.exit(1)
        print(f"✅ 静态预览已生成: {out}")
        print("提示：浏览器打开即可查看版式（无 JS 依赖）；修改模板后重跑 --format preview 刷新。")
        return

    if not in_path.exists():
        print(f"❌ 输入文件不存在: {in_path}")
        sys.exit(1)

    md_text = in_path.read_text(encoding="utf-8")
    tpl_text = _inline_palette(tpl_path.read_text(encoding="utf-8"))
    if profile == "portfolio":
        # css 传入 ⇒ 页脚块可读 --footer（以模板声明为准；未声明 ⇒ 合册默认 page-x-of-y）
        data = build_data_portfolio(md_text, args.photo or "", extract_css_vars(tpl_text))
    else:
        data = build_data_resume(md_text, args.photo or "")
    # 背景形状层注入（v2.8.4 多形状：--header-shapes 层名列表；空则兼容旧单形状；color/image 为空数组不渲染）
    _bg = extract_css_vars(tpl_text)
    _bgv = lambda k, d="": _bg.get(k, d).strip()
    data["header_shape_layers"] = []
    data["header_decos"] = []
    if profile == "resume" and _bgv("--header-bg-type", "color") == "shape":
        shapes = [s for s in _bgv("--header-shapes").split(",") if s.strip()]
        W_pt, H_pt = 504, 105  # 内容宽 pt / 背景高 pt（viewBox 单位与 PDF 同构）
        hbh = _bgv("--header-bg-height", "auto")
        if hbh.lower() != "auto":
            try:
                H_pt = float(hbh.rstrip("pt"))
            except ValueError:
                pass

        def _npt(raw, d=0.0):
            try:
                return float(str(raw).replace("px", "").replace("pt", ""))
            except (ValueError, TypeError):
                return d

        if shapes:
            # 多形状堆叠：每层一个完整形状（align: top=顶对齐 oy=0；bottom=底对齐 oy=H_pt-height）
            for nm in shapes:
                typ = _bgv(f"--shape-{nm}-type", "trapezoid")
                color = _bgv(f"--shape-{nm}-color", "#1A3A6E")
                ox = _npt(_bgv(f"--shape-{nm}-offset-x", "0"))
                align = _bgv(f"--shape-{nm}-align", "bottom").strip().lower()
                height = _npt(_bgv(f"--shape-{nm}-height", f"{H_pt}pt"), H_pt)
                oy = 0 if align == "top" else (H_pt - height)  # v2.8.7 align 支持（HTML y 向下）
                ins = [_npt(v) for v in _bgv(f"--shape-{nm}-insets", "0 0 0 0").split()]
                ins += [0] * (4 - len(ins))
                tl, tr, bl, br = ins[:4]
                if typ == "trapezoid":
                    d = (f"M{tl + ox},{oy} L{W_pt - tr + ox},{oy} "
                         f"L{W_pt - br + ox},{height + oy} L{bl + ox},{height + oy} Z")
                elif typ == "slant":
                    cut = min(height, W_pt * 0.3)
                    d = (f"M{ox},{oy} L{W_pt - cut + ox},{oy} L{W_pt + ox},{cut + oy} "
                         f"L{W_pt + ox},{height + oy} L{ox},{height + oy} Z")
                else:  # square / rounded（预览端直角近似）
                    d = f"M{ox},{oy} L{W_pt + ox},{oy} L{W_pt + ox},{height + oy} L{ox},{height + oy} Z"
                data["header_shape_layers"].append({"path": d, "color": color,
                                                     "viewbox": f"0 0 {W_pt} {H_pt}"})
        else:
            # 旧单形状模式（--header-shape）
            main = [s for s in _bgv("--header-shape", "rounded").split(",") if s.strip()]
            m0 = main[0] if main else "rounded"
            color = _bgv("--header-bg-value", "#EAF2FA")
            if m0 == "wave":
                data["header_shape_layers"].append({
                    "path": "M0,0 H680 V78 Q650,62 620,78 T560,78 T500,78 T440,78 T380,78 "
                            "T320,78 T260,78 T200,78 T140,78 T80,78 T20,78 Q0,80 0,80 Z",
                    "color": color, "viewbox": "0 0 680 120"})
            elif m0 == "slant":
                cut = min(H_pt, W_pt * 0.3)
                data["header_shape_layers"].append({
                    "path": f"M0,0 L{W_pt - cut},0 L{W_pt},{cut} L{W_pt},{H_pt} L0,{H_pt} Z",
                    "color": color, "viewbox": f"0 0 {W_pt} {H_pt}"})
            else:
                data["header_shape_layers"].append({
                    "path": f"M0,0 L{W_pt},0 L{W_pt},{H_pt} L0,{H_pt} Z",
                    "color": color, "viewbox": f"0 0 {W_pt} {H_pt}"})
            if "block" in main:
                data["header_decos"].append({"cls": "deco-block", "html": ""})
            if "dots" in main:
                data["header_decos"].append({
                    "cls": "deco-dots",
                    "html": '<span style="width:8px;height:8px"></span>'
                            '<span style="width:5px;height:5px"></span>'
                            '<span style="width:6px;height:6px"></span>'})
            if "stripe" in main:
                data["header_decos"].append({"cls": "deco-stripe", "html": ""})
    # 剥离浏览器预览 script 块（仅用于 v1 模板预览，不进渲染）
    tpl_text = _strip_preview_scripts(tpl_text)
    html = mini_render(tpl_text, data)
    if args.theme:
        from importlib import import_module
        # 复用本文件的 THEMES（内联简单映射，避免循环依赖）
        THEMES = {
            "blue": {"accent": "1564BF", "accent_dark": "003B8E", "line": "D9E2F0", "text": "1A1A1A"},
            "green": {"accent": "2E7D32", "accent_dark": "1B5E20", "line": "C8E6C9", "text": "1A1A1A"},
            "orange": {"accent": "E65100", "accent_dark": "BF360C", "line": "FFE0B2", "text": "1A1A1A"},
            "dark": {"accent": "37474F", "accent_dark": "263238", "line": "CFD8DC", "text": "1A1A1A"},
        }
        if args.theme in THEMES:
            html = apply_theme_override(html, THEMES[args.theme])

    out_dir = in_path.parent
    stem = in_path.stem

    if args.format == "pages":
        # 刀 C ⑩：只试渲染取真实页数，不写任何文件（供 Step 9.6 Phase A / Portfolio Gate 报数）
        import tempfile

        with tempfile.TemporaryDirectory() as _td:
            try:
                pages = html_to_pdf(html, Path(_td) / f"{stem}.pdf", profile)
            except ImportError as e:
                print(f"❌ PDF 需要 reportlab：{e}")
                sys.exit(1)
        if isinstance(pages, int):
            print(f"{pages} 页")
        else:
            print("页数未知（renderer 未返回计数）")
        return

    results = []
    if args.format in ("html", "all"):
        out_html = out_dir / f"{stem}.html"
        out_html.write_text(_embed_photo_as_data_uri(html), encoding="utf-8")
        results.append(out_html)
    if args.format in ("pdf", "all"):
        try:
            out_pdf = out_dir / f"{stem}.pdf"
            pages = html_to_pdf(html, out_pdf, profile)
            results.append(out_pdf)
            if profile == "portfolio" and isinstance(pages, int):
                # 刀 C 已接入：10 页放行在 Step 9.6 Portfolio Gate；脚本只「报数」不「拦」（放行判定在 LLM 层）
                print(f"📄 合册页数：{pages} 页（--cover-page: always 时含封面页）")
        except ImportError as e:
            print(f"❌ PDF 需要 reportlab：{e}")
    if args.format in ("docx", "all"):
        try:
            out_docx = out_dir / f"{stem}.docx"
            html_to_docx(html, out_docx, profile)
            results.append(out_docx)
        except ImportError as e:
            print(f"❌ DOCX 需要 python-docx：{e}")

    if args.format in ("png", "png-long"):
        # F25（v2.24.0）：PNG = **PDF 的再派生**（final.md → HTML → PDF → PNG）——
        # 不截图 HTML（HTML 是浏览器连续流，与 A4 分页 + onPage 背景层**不同源**）。
        # `png` = 分页图 + 长图（两者都出）；`png-long` = 只出长图。
        import tempfile
        want_pages = args.format == "png"
        try:
            import render_png
        except ImportError as e:
            print(f"❌ PNG 需要 render_png 模块：{e}")
            render_png = None
        if render_png is not None:
            png_dir = out_dir / "png"
            with tempfile.TemporaryDirectory() as _td:
                try:
                    base_pdf = Path(_td) / f"{stem}.pdf"
                    n_pages = html_to_pdf(html, base_pdf, profile)   # 分页源 + 长图页高基准
                    if not isinstance(n_pages, int):
                        n_pages = 1
                    if want_pages:
                        results.extend(render_png.pdf_pages_to_png(
                            base_pdf, png_dir, stem, args.png_width))
                    _h = render_png.long_page_height(n_pages)
                    if _h is None:
                        print(f"⚠️ 内容过长（>{render_png.MAX_PAGE_PT:.0f}pt）⇒ 长图降级："
                              f"只出分页图（PDF 单边尺寸上限）")
                    else:
                        long_pdf = Path(_td) / f"{stem}_long.pdf"
                        # 单张超高页：内容不分页 ⇒ 无页背景 / 水印接缝
                        html_to_pdf(html, long_pdf, profile, page_height=_h)
                        results.append(render_png.pdf_long_to_png(
                            long_pdf, png_dir / f"{stem}_long.png", args.png_width))
                except ImportError as e:
                    print(f"❌ PNG 需要 pypdfium2（Apache-2.0）+ Pillow：{e}")

    if not results:
        sys.exit(1)
    for r in results:
        print(f"✅ 已生成: {r}")
    print("提示：final.html 为 v2 完整版（样式+内容）可预览；内容定稿以 final.md 为单一事实源。")


# 向后兼容别名：旧调用方仍可用 build_data（= 简历 profile）
build_data = build_data_resume


if __name__ == "__main__":
    main()
