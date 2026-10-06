#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF → PNG 栅格化（F25 · v2.24.0）。

派生关系（唯一合法路径）：
    final.md → HTML → PDF → **PNG**
即 PNG 是 **PDF 的再派生**，不是独立渲染 —— 保证「PNG 与目检定稿的 PDF 像素同源」。
⚠️ **禁止**从 HTML 截图（HTML 是浏览器连续流，与 A4 分页 + onPage 背景层布局**不同源**）。

两种形态：
    - **分页 PNG**（默认主路径）：A4 PDF 逐页栅格化 ⇒ `{stem}_p1.png` / `_p2.png` …
    - **长图 PNG**（备用于「一次给完整印象」）：由「**单张超高页**」PDF 栅格化 ⇒ `{stem}_long.png`
      · 选「单超高页」而非「逐页拼接」：拼接法会在**页背景 / 水印**处产生接缝（onPage 逐页绘制）。
      · 超高页的上限 = `MAX_PAGE_PT`（PDF 单边 ~200in / 14400pt）⇒ 超限由调用方降级分页。
      · 尾部空白按「与底色同色」裁除（`_trim_bottom`）。

依赖（**可选**）：`pypdfium2`（Apache-2.0 / BSD，可随发布型 skill 分发）+ `Pillow`（MIT-CMU）。
缺失时抛 ImportError，由调用方**友善提示、不崩**（同 reportlab / python-docx 处理模式）。
⚠️ 不引入 PyMuPDF（AGPL-3.0）作默认栅格化器；不需要系统级 poppler（pdf2image 的依赖）。

只读 PDF、只写 PNG —— **不修改任何输入文件**；产出的 PNG 为**派生渲染物 · 禁手改**。
"""

from pathlib import Path

# 尺寸常量（pt）
PT_PER_IN = 72.0
A4_W_PT = 595.2755905511812   # 210mm
A4_H_PT = 841.8897637795277   # 297mm
# PDF 单边尺寸业界上限（~200in）；超高页不得超过，否则须降级分页
MAX_PAGE_PT = 14400.0

DEFAULT_WIDTH_PX = 1160       # Boss 官方消息卡片建议宽度（= 580×2 两倍图）
WATERMARK_KEEP = 2            # 裁尾后保留的底部像素（防把最后一行字切掉）


def _require():
    """惰性校验可选依赖（缺失 ⇒ ImportError，调用方负责友善提示）。"""
    try:
        import pypdfium2  # noqa: F401
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "PNG 导出需要 pypdfium2（Apache-2.0）。安装：pip install pypdfium2"
        ) from e
    try:
        import PIL  # noqa: F401
    except ImportError as e:  # pragma: no cover
        raise ImportError("PNG 导出需要 Pillow。安装：pip install Pillow") from e


def _open(pdf_path):
    import pypdfium2 as pdfium
    return pdfium.PdfDocument(str(pdf_path))


def _render(page, width_px: int):
    """按**目标宽度**栅格化单页 ⇒ PIL.Image（宽度导向：平台规范与用户心智单位都是 px）。"""
    w_pt = float(page.get_width())
    if w_pt <= 0:
        raise ValueError("PDF 页宽非法（<=0）")
    scale = float(width_px) / w_pt
    return page.render(scale=scale).to_pil()


def _clean(img):
    """去元数据（EXIF / info）—— 避免软件指纹随图外泄（F25 打磨项 ⑥）。"""
    from PIL import Image
    out = Image.new(img.mode, img.size)
    out.paste(img)
    out.info.clear()
    return out


def _save_png(img, path: Path, optimize: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    _clean(img).save(str(path), "PNG", optimize=optimize)
    return path


def _trim_bottom(img, tol: int = 6):
    """裁除底部与「最底色」同色的空白行（长图尾部留白）。左右上边界不动。"""
    from PIL import Image, ImageChops
    rgb = img.convert("RGB")
    w, h = rgb.size
    if h <= 1:
        return rgb
    bg = rgb.getpixel((0, h - 1))
    diff = ImageChops.difference(rgb, Image.new("RGB", (w, h), bg)).convert("L")
    mask = diff.point(lambda v: 255 if v > tol else 0)
    bbox = mask.getbbox()          # (left, top, right, bottom)
    if not bbox:
        return rgb                 # 整页纯底色 ⇒ 原样返回（不裁成 0 高）
    bottom = min(h, bbox[3] + WATERMARK_KEEP)
    return rgb.crop((0, 0, w, bottom))


def pdf_pages_to_png(pdf_path, out_dir, stem: str, width_px: int = DEFAULT_WIDTH_PX):
    """**分页 PNG**：`pdf_path` 每页 ⇒ `out_dir/{stem}_p{i}.png`。返回落盘路径列表。"""
    _require()
    pdf = _open(pdf_path)
    outs = []
    try:
        n = len(pdf)
        for i in range(n):
            page = pdf[i]
            try:
                img = _render(page, width_px)
            finally:
                page.close()
            outs.append(_save_png(img, Path(out_dir) / f"{stem}_p{i + 1}.png"))
    finally:
        pdf.close()
    return outs


def pdf_long_to_png(pdf_path, out_path, width_px: int = DEFAULT_WIDTH_PX, trim: bool = True):
    """**长图 PNG**：读取「单张超高页」PDF 的第 1 页 ⇒ 一张无缝长图（默认裁尾）。"""
    _require()
    pdf = _open(pdf_path)
    try:
        page = pdf[0]
        try:
            img = _render(page, width_px)
        finally:
            page.close()
    finally:
        pdf.close()
    if trim:
        img = _trim_bottom(img)
    return _save_png(img, Path(out_path))


def long_page_height(page_count: int, top_margin_pt: float = 0.0,
                     bottom_margin_pt: float = 0.0) -> float:
    """长图页高（pt）：足以容纳 N 页 A4 内容 ⇒ 单页不分页。

    `N × A4高 − 底边距`（末页底边距白留由 `_trim_bottom` 收掉）；
    超过 `MAX_PAGE_PT` ⇒ 返回 `None`（调用方降级分页）。
    """
    h = page_count * A4_H_PT - max(0.0, float(bottom_margin_pt))
    if h > MAX_PAGE_PT:
        return None
    return max(h, A4_H_PT)
