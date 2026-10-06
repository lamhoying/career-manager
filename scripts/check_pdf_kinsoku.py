#!/usr/bin/env python3
"""PDF **行首标点**探针（F53 · v2.24.0）—— 出包后的版式检漏器。

**为什么需要它**：`reportlab` 对 CJK **逐字符断行、无禁则 / 避头尾** ⇒ 标点可能落到行首
（「，」「：」等）。**机制级修复经实测不可行**：`U+2060`（word joiner）/ `U+00A0`（nbsp）
**均无法抑制断行** —— 分页法正样本实测（每变体独占一页）：原样在 N=47 触发行首 `，`；
加 `U+2060` 后仍 N=46 触发 ⇒ 只能走「**文本层规避（改词序）+ 本探针检漏**」。

**性质**：**只读检漏 · 不改文件**。按 F53 决议，它是**每份投递件出 PDF 后的一步**（治标手段
必须每包重做，机制不承载）。

判据
----
逐行取**首个非空白字符**，命中禁则标点集即报。**必须排除两类已知假阳性**（v2.24.0 实测）：
  ① **平铺水印**被 PDF 文本层按 block 切开，右半段以 `]` 起头（含「仅供招聘评估使用」）；
  ② **目录引导线**（`. . . .` 点号串，**可带页码尾**，如 `. . . 2`）。
另：`·` **不计**入禁则 —— 本项目正文以 `·` 作分隔符起头是**合法写法**。

依赖：`pymupdf`（本脚本**不进** `validate_career_dna.py` 的闸门链 —— 闸门须在 `python3 -S -E`
下以纯标准库运行；本探针是**独立的出包后检查**）。

用法
----
    python3 check_pdf_kinsoku.py <pdf> [<pdf> ...]
退出码：0 = 全部 0 命中；1 = 有命中（须文本层规避：改写该处词序使标点不落行首）；2 = 参数缺失。
"""
import re
import sys

try:
    import pymupdf
except ImportError:                                  # pragma: no cover
    sys.stderr.write("需要 pymupdf：pip install pymupdf\n")
    sys.exit(2)

# 禁则标点（行首不应出现）—— 不含 `·`（本项目合法行首分隔符，见 docstring）
BANNED_LEAD = "，。、；：？！）】》」』〕〉｝］＞’”‛,.;:!?)]}>"
FP_DOTS = re.compile(r"^[.\s]+\d*$")                 # 目录引导线（可带页码尾）
FP_WATERMARK = re.compile(r"仅[供为]招聘评估使用")     # 平铺水印片段


def scan(path: str):
    """→ [(页码, 行首标点行原文截断)]。"""
    doc = pymupdf.open(path)
    hits = []
    for pno, page in enumerate(doc, 1):
        for block in page.get_text("blocks"):
            for line in block[4].splitlines():
                s = line.strip()
                if not s:
                    continue
                if FP_DOTS.match(s) or FP_WATERMARK.search(s):
                    continue                          # 已知假阳性
                if s[0] in BANNED_LEAD:
                    hits.append((pno, s[:70]))
    return hits


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    total = 0
    for p in argv[1:]:
        hits = scan(p)
        total += len(hits)
        print(f"[{'ok ' if not hits else 'HIT'}] {p} :: 行首标点 {len(hits)} 处")
        for pno, s in hits:
            print(f"        p{pno}: {s}")
    print(f"\n合计 {total} 处")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
