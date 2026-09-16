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
"""

import argparse
import base64
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from mini_template import render as mini_render


# ---------- final.md → 结构化数据 ----------

_ARROW_FALLBACK = {
    "\u2192": "->",   # → U+2192：NotoSansSC 无此字形（PDF 显示豆腐块），渲染出口降级为 ASCII；HTML 端不受影响
}


def _pdf_safe(s: str) -> str:
    """渲染安全化：把 CJK 字体缺失的符号替换为 ASCII（仅 PDF/DOCX 文本出口调用，不落源文件）。"""
    for k, v in _ARROW_FALLBACK.items():
        s = s.replace(k, v)
    return s


def _fmt(s: str) -> str:
    """转义 + **加粗** → <b>。"""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


def parse_md(text: str):
    elements = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            elements.append(("blank", ""))
            continue
        if line.startswith("# "):
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
    return elements


def build_data(md_text: str, photo_path: str = "") -> dict:
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
                cur["段落"].append(_fmt(line))
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
            elif val.tag == "br":
                out.append("<br/>")
            else:
                walk(val)

    walk(node)
    return "".join(out)


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


def html_to_pdf(html_text: str, out_path: Path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                    TableStyle, Image, HRFlowable)
    from reportlab.lib.styles import ParagraphStyle

    bold_font = _reg_cn_fonts()
    css = extract_css_vars(html_text)
    def cv(var, default):
        v = css.get(var, default).strip()
        return v
    accent = HexColor(cv("--accent", "#1564BF"))
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

    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                            topMargin=mt * mm, bottomMargin=mt * mm,
                            leftMargin=ms * mm, rightMargin=ms * mm)
    # reportlab 5.x：页面回调是 build() 参数（onPage 构造函数参数已废弃/被忽略）
    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
    return out_path


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


def _fill_rich(p, parts, font="微软雅黑", size=10.5, color="1A1A1A"):
    """[(text, bold)] → docx runs。"""
    for text, bold in parts:
        _set_font(p.add_run(text), font, size, bold, color)


def html_to_docx(html_text: str, out_path: Path):
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


def make_static_preview(template_text: str, out_path: Path):
    """用内置示例数据渲染出静态预览（无 JS 依赖，供浏览器直接查看版式）。
    模板无需嵌入 PREVIEW_DATA：示例数据内置在此处，v1 模板保持纯占位符（引擎用）。"""
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
    ap.add_argument("--format", choices=["html", "pdf", "docx", "all", "preview"], default="all",
                    help="preview = 用模板内嵌示例数据生成静态预览（改模板后刷新预览用）")
    ap.add_argument("--photo", default=None, help="证件照（可选）")
    ap.add_argument("--theme", default=None, help="配色覆盖（可选，覆盖模板 CSS 变量）")
    args = ap.parse_args()

    in_path = Path(args.input)

    if args.template:
        tpl_path = Path(args.template)
    else:
        here = Path(__file__).resolve().parent
        tpl_path = here.parent / "assets" / "templates" / "resume-outputs" / "resume_template.html"
    if not tpl_path.exists():
        print(f"❌ 模板不存在: {tpl_path}")
        sys.exit(1)

    if args.format == "preview":
        out = make_static_preview(tpl_path.read_text(encoding="utf-8"),
                                  in_path.parent / f"{tpl_path.stem}_static_preview.html")
        if not out:
            sys.exit(1)
        print(f"✅ 静态预览已生成: {out}")
        print("提示：浏览器打开即可查看版式（无 JS 依赖）；修改模板后重跑 --format preview 刷新。")
        return

    if not in_path.exists():
        print(f"❌ 输入文件不存在: {in_path}")
        sys.exit(1)

    md_text = in_path.read_text(encoding="utf-8")
    data = build_data(md_text, args.photo or "")
    tpl_text = tpl_path.read_text(encoding="utf-8")
    # 背景形状层注入（v2.8.4 多形状：--header-shapes 层名列表；空则兼容旧单形状；color/image 为空数组不渲染）
    _bg = extract_css_vars(tpl_text)
    _bgv = lambda k, d="": _bg.get(k, d).strip()
    data["header_shape_layers"] = []
    data["header_decos"] = []
    if _bgv("--header-bg-type", "color") == "shape":
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

    results = []
    if args.format in ("html", "all"):
        out_html = out_dir / f"{stem}.html"
        out_html.write_text(_embed_photo_as_data_uri(html), encoding="utf-8")
        results.append(out_html)
    if args.format in ("pdf", "all"):
        try:
            out_pdf = out_dir / f"{stem}.pdf"
            html_to_pdf(html, out_pdf)
            results.append(out_pdf)
        except ImportError as e:
            print(f"❌ PDF 需要 reportlab：{e}")
    if args.format in ("docx", "all"):
        try:
            out_docx = out_dir / f"{stem}.docx"
            html_to_docx(html, out_docx)
            results.append(out_docx)
        except ImportError as e:
            print(f"❌ DOCX 需要 python-docx：{e}")

    if not results:
        sys.exit(1)
    for r in results:
        print(f"✅ 已生成: {r}")
    print("提示：final.html 为 v2 完整版（样式+内容）可预览；内容定稿以 final.md 为单一事实源。")


if __name__ == "__main__":
    main()
