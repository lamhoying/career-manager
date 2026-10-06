#!/usr/bin/env python3
"""中文字体构建 —— 在 NotoSansSC 子集上补齐「符号 / 标点 / 希腊 / 带圈数字」字形。

背景（对应待办 F36）
====================
assets/fonts/NotoSansSC-{Regular,Bold}.ttf 是 **Noto Sans SC 的子集**。
**升级前**仅 **7,946 码位**（只保留常用汉字 + 基本标点，**不含** 箭头 / 数学关系 /
希腊字母 / 带圈数字 / 勾叉）；**v2.23.1 起为 9,313 码位**（已并入安全集内全部可用字形
⇒ 上述符号均已具备**真字形**）。

合册 PDF 由 reportlab **直接绘制**（不是 HTML→PDF），reportlab **无字体回退** ⇒
不在 cmap 的字符 **画不出、不报错、文本层也不留痕** = **静默丢字**。
对照：HTML 走浏览器字体回退、DOCX 走 Word 替换字体 ⇒ 二者一直正常
⇒ 表现为「同一份 md，HTML 好看、PDF 少字」的**出口间不一致**。

做法：**同族同权重重子集**（不混搭其他字体家族 ⇒ 无字形风格错配）
==================================================================
  1) 取完整 Noto Sans SC（变量字体，wght 轴 100–900）。
  2) 实例化到与现有子集**同一权重**。实测标定（勿凭文件名猜 —— 家族名写
     "Noto Sans SC Thin" 是子集工具的残留，其默认实例才是 Thin）：
         现有 Regular ≡ wght 400 ；现有 Bold ≡ wght 700
     判据 = 与变量字体各权重实例做字形外接框面积比对 + 与原件轮廓指纹比对。
  3) 保留集 = 「现有全部码位」∪「安全集 ∩ 完整字体 − 现有」
     ⇒ 用**完整字体重新子集**，而非 merge 追加。
  4) 子集参数与原件对齐：保留全部 layout 表与 name 记录 ⇒ **能力零倒退**；
     并**整体沿用原件的 name 表** ⇒ family/subfamily/version 三处零漂移。

为什么不用 fontTools.merge
==========================
  实测 `Merger().merge()` 在「原件（含 GPOS/GSUB）↔ 补丁子集（已 drop layout）」
  之间报 `TypeError: '>' not supported between NotImplementedType and int`
  （fontTools/merge/base.py::mergeObjects）—— 两字体**表集合不一致**即触发。
  重子集路线无此约束，且实测既有字形轮廓**逐字节等价**（抽样 500 汉字零漂移），
  故弃用 merge。

⚠️ 进程隔离（实测教训）
=======================
  两个目标字体**在同一个进程内**连续构建会 **OOM 被 SIGKILL**（实测：Regular 成功、
  Bold 迭代中途整进程被杀，退出码 137，且**输出全丢** —— 管道缓冲随进程一起消失）。
  ⇒ `--build` 会为每个目标 **fork 一个子进程**（`--build-one`），各自独立内存空间。
  单字体峰值内存约 400 MB、耗时约 30 s（绝大部分在变量字体实例化）。

用法
====
  python3 build_cn_font.py --check                 # 体检：现有覆盖 vs 必检字符
  python3 build_cn_font.py --build --out DIR       # 构建到 DIR（试跑，不动资产）
  python3 build_cn_font.py --verify DIR            # 校验 DIR 内产物
  python3 build_cn_font.py --install DIR           # 备份原件后覆盖 assets/fonts/

⚠️ 源字体（17.7 MB）不进仓库：按 URL 下载到缓存目录并**校验 SHA-256**。
   上游若更新导致 SHA 不符 ⇒ **脚本报错退出**（不静默接受），此时须人工确认新版
   是否仍为 OFL + 是否仍含所需码位 + 是否仍与现有子集同版本，再更新 SRC_SHA256。
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE.parent / "assets" / "fonts"

SRC_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/"
           "NotoSansSC%5Bwght%5D.ttf")
SRC_SHA256 = "a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da"
SRC_NAME = "NotoSansSC[wght].ttf"

# 目标 = 现有两文件 → 对应权重（实测标定，勿凭文件名猜）
TARGETS = [("NotoSansSC-Regular.ttf", 400), ("NotoSansSC-Bold.ttf", 700)]

# 安全集：会被写进中文文档的「符号 / 标点」Unicode 区段
# 判据 = 「可能出现在简历 / 作品集正文里，且报告性文档不该因缺字形而丢字」
SAFETY_RANGES = [
    ("Greek and Coptic", 0x0370, 0x03FF),
    ("General Punctuation", 0x2000, 0x206F),
    ("Super/Subscripts", 0x2070, 0x209F),
    ("Currency Symbols", 0x20A0, 0x20CF),
    ("Letterlike Symbols", 0x2100, 0x214F),
    ("Number Forms", 0x2150, 0x218F),
    ("Arrows", 0x2190, 0x21FF),
    ("Mathematical Operators", 0x2200, 0x22FF),
    ("Misc Technical", 0x2300, 0x23FF),
    ("Control Pictures", 0x2400, 0x243F),
    ("Enclosed Alphanumerics", 0x2460, 0x24FF),
    ("Box Drawing", 0x2500, 0x257F),
    ("Block Elements", 0x2580, 0x259F),
    ("Geometric Shapes", 0x25A0, 0x25FF),
    ("Misc Symbols", 0x2600, 0x26FF),
    ("Dingbats", 0x2700, 0x27BF),
    ("Supplemental Arrows B", 0x2900, 0x297F),
    ("Misc Symbols and Arrows", 0x2B00, 0x2BFF),
    ("CJK Symbols and Punctuation", 0x3000, 0x303F),
    ("Enclosed CJK Letters", 0x3200, 0x32FF),
    ("CJK Compatibility", 0x3300, 0x33FF),
    ("CJK Compat Forms", 0xFE30, 0xFE4F),
    ("Halfwidth/Fullwidth", 0xFF00, 0xFFEF),
]

# 必检字符 —— 与 export_resume.py::_ARROW_FALLBACK 互补：
# 这些必须**有真字形**，不该依赖降级映射。
# ⚠️ 本常量是**唯一真源**：validate_career_dna.py P2 `pdf-glyph-coverage`
#    通过 import 复用，勿在别处复制一份。
CHECKLIST = "→←↑↓↔⇄⇅⇒≤≥≈≠±√∞∑∏∫∈∇ΦΔΣΩαβμ①②③④⑤⑥⑦⑧⑨⑩㊀✓⚠"

# 轮廓漂移抽样：常用汉字（覆盖简体高频字，足以暴露「换了字体版本」这类系统性漂移）
_DRIFT_SAMPLE = (
    "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过"
    "子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体"
    "制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内"
    "数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提"
    "直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计"
    "别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海"
    "口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身"
    "车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石"
    "记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青"
    "省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型"
    "眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞")


# ---------- 基础工具 ----------

def _cmap(t) -> set[int]:
    s: set[int] = set()
    for tb in t["cmap"].tables:
        s |= set(tb.cmap.keys())
    return s


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _safety_cps() -> set[int]:
    s: set[int] = set()
    for _n, a, b in SAFETY_RANGES:
        s |= set(range(a, b + 1))
    return s


def _sig(t, ch: str) -> str | None:
    """字形轮廓指纹（对 draw 指令序列取 md5）。"""
    from fontTools.pens.recordingPen import RecordingPen
    gn = t.getBestCmap().get(ord(ch))
    if not gn:
        return None
    p = RecordingPen()
    t.getGlyphSet()[gn].draw(p)
    return hashlib.md5(repr(p.value).encode()).hexdigest()[:12]


def fetch_source(cache: Path) -> Path:
    """下载并校验源字体（已存在且校验通过则跳过）。"""
    cache.mkdir(parents=True, exist_ok=True)
    dst = cache / SRC_NAME
    if dst.exists() and _sha256(dst) == SRC_SHA256:
        print(f"[缓存] {dst} SHA-256 校验通过")
        return dst
    print(f"[下载] {SRC_URL}")
    tmp = dst.with_suffix(".part")
    with urllib.request.urlopen(SRC_URL, timeout=300) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    got = _sha256(tmp)
    if got != SRC_SHA256:
        tmp.unlink(missing_ok=True)
        sys.exit(f"[FAIL] 源字体 SHA-256 不符\n  期望 {SRC_SHA256}\n  实得 {got}\n"
                 f"  ⇒ 上游可能已更新。请人工确认新版仍为 OFL、仍含所需码位、"
                 f"且仍与现有子集同版本后，再更新 SRC_SHA256。")
    tmp.rename(dst)
    print(f"[OK]  下载并校验通过（{dst.stat().st_size / 1e6:.1f} MB）")
    return dst


# ---------- 子命令 ----------

def cmd_check() -> None:
    from fontTools.ttLib import TTFont
    print("必检字符 =", CHECKLIST)
    for name, _w in TARGETS:
        p = FONT_DIR / name
        if not p.exists():
            sys.exit(f"[FAIL] 缺文件 {p}")
        cur = _cmap(TTFont(p, lazy=True))
        miss = [c for c in CHECKLIST if ord(c) not in cur]
        print(f"\n### {name}")
        print(f"  当前码位 {len(cur)}  体积 {p.stat().st_size / 1e6:.2f} MB")
        print(f"  必检字符缺 {len(miss)}/{len(CHECKLIST)}：{''.join(miss) or '（无）'}")
    print("\n（--check 只读现有文件；缺字形须跑 --build 才会补齐）")


def _build_one(name: str, weight: int, out_dir: Path, cache: Path) -> None:
    """构建**单个**目标字体（每个目标须独立进程 ⇒ 防 OOM）。"""
    from fontTools.subset import Options, Subsetter
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont

    src = fetch_source(cache)
    tgt = FONT_DIR / name
    if not tgt.exists():
        sys.exit(f"[FAIL] 缺目标文件 {tgt}")

    print(f"\n### {name}   ← 实例 wght={weight}")
    t0 = time.time()
    orig = TTFont(str(tgt), lazy=True)
    cur = _cmap(orig)
    orig_tables = sorted(set(orig.keys()) - {"GlyphOrder"})
    print(f"  原件 {len(cur)} 码位 / {orig_tables}")

    t0 = time.time()
    vf = TTFont(str(src))
    instantiateVariableFont(vf, {"wght": weight}, inplace=True, updateFontNames=False)
    print(f"  实例化完成 {time.time() - t0:.1f}s")
    full = _cmap(vf)
    new_cps = sorted((_safety_cps() & full) - cur)
    if not new_cps:
        print("  无缺口，跳过")
        return
    print(f"  可补字形 {len(new_cps)}：{''.join(chr(c) for c in new_cps[:24])} …")

    opt = Options()
    opt.name_IDs = ["*"]          # 保留全部 name 记录
    opt.layout_features = ["*"]   # 保留全部 layout 特性 ⇒ 与原件能力对齐
    opt.notdef_outline = True
    ss = Subsetter(options=opt)
    ss.populate(unicodes=sorted(cur | set(new_cps)))
    t0 = time.time()
    ss.subset(vf)
    print(f"  子集完成 {time.time() - t0:.1f}s")

    # 沿用原件的 name 表 ⇒ family / subfamily / full / version 四处零漂移
    vf["name"] = orig["name"]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / name
    t0 = time.time()
    vf.save(str(out_path))
    print(f"  落盘 {time.time() - t0:.1f}s → {out_path}")
    got = _cmap(TTFont(str(out_path), lazy=True))
    print(f"  结果：{len(cur)} → {len(got)} 码位（+{len(got) - len(cur)}）；"
          f"{tgt.stat().st_size / 1e6:.2f} → {out_path.stat().st_size / 1e6:.2f} MB")


def cmd_build(out_dir: Path, cache: Path, only: str | None) -> None:
    picks = [t for t in TARGETS if only in (None, "", t[0])] if only else TARGETS
    if only and not picks:
        sys.exit(f"[FAIL] --only 不匹配任何目标：{only}（可选 {[t[0] for t in TARGETS]}）")
    print(f"[编排] 目标 {len(picks)} 个，逐个 fork 子进程（防同进程 OOM）")
    for name, weight in picks:
        # 关键：独立进程。同进程连续构建两个字体实测会被 OOM SIGKILL，
        # 且缓冲输出随进程一起丢失（表现为「无任何输出」）。
        cmd = [sys.executable, str(Path(__file__).resolve()), "--build-one",
               name, str(weight), str(out_dir), str(cache)]
        print(f"\n{'=' * 20} {name} {'=' * 20}")
        r = subprocess.run(cmd)
        if r.returncode != 0:
            sys.exit(f"[FAIL] {name} 构建失败，退出码 {r.returncode}")
    print(f"\n[完成] 产物目录：{out_dir}")
    print("⚠️ 覆盖资产前先跑 --verify 校验；本子命令不改资产。")


def cmd_verify(d: Path) -> None:
    from fontTools.ttLib import TTFont
    ok = True
    for name, _w in TARGETS:
        new, old = d / name, FONT_DIR / name
        print(f"\n### {name}")
        if not new.exists():
            print(f"  ✘ 缺产物 {new}")
            ok = False
            continue
        nf, of = TTFont(str(new), lazy=True), TTFont(str(old), lazy=True)
        a, b = _cmap(of), _cmap(nf)

        dropped = a - b
        print(f"  ① 既有码位零丢失：{len(a)} → {len(b)}，丢 {len(dropped)} "
              f"{'✔' if not dropped else '✘ ' + str(sorted(dropped)[:12])}")
        ok &= not dropped

        miss = [c for c in CHECKLIST if ord(c) not in b]
        print(f"  ② 必检字符零缺失：缺 {len(miss)}/{len(CHECKLIST)} "
              f"{'✔' if not miss else '✘ ' + ''.join(miss)}")
        ok &= not miss

        fa, fb = TTFont(str(old)), TTFont(str(new))
        drift = [c for c in _DRIFT_SAMPLE if _sig(fa, c) != _sig(fb, c)]
        print(f"  ③ 既有字形轮廓零漂移：抽样 {len(_DRIFT_SAMPLE)} 汉字，漂移 {len(drift)} "
              f"{'✔' if not drift else '✘ ' + ''.join(drift[:16])}")
        ok &= not drift

        def nm(t, nid):
            return t["name"].getDebugName(nid)
        same = all(nm(of, i) == nm(nf, i) for i in (1, 2, 4, 5))
        print(f"  ④ name 表零漂移（family/subfamily/full/version）：{'✔' if same else '✘'}")
        if not same:
            for i in (1, 2, 4, 5):
                print(f"       id{i}: 旧={nm(of, i)!r} 新={nm(nf, i)!r}")
        ok &= same

        lost = set(o for o in (set(of.keys()) - {"GlyphOrder"}) if o not in set(nf.keys()))
        print(f"  ⑤ layout 表零倒退：缺 {len(lost)} {'✔' if not lost else '✘ ' + str(sorted(lost))}")
        ok &= not lost

    print(f"\n=== verify {'PASS' if ok else 'FAIL'} ===")
    sys.exit(0 if ok else 1)


def cmd_install(d: Path) -> None:
    """备份原件后把产物覆盖进 assets/fonts/，随后自动复核。"""
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # 备份优先落「调用方工作区的 .workbuddy/backups」；无该目录则退回资产同级
    ws = Path.cwd() / ".workbuddy" / "backups"
    bak = (ws if (Path.cwd() / ".workbuddy").is_dir() else FONT_DIR.parent) / \
        f"{stamp}_pre-font-upgrade"
    # 先校验产物，不合格不落地
    print("[前置] 校验产物 ……")
    r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--verify", str(d)])
    if r.returncode != 0:
        sys.exit("[FAIL] 产物未通过校验，已中止安装（资产未被改动）")
    bak.mkdir(parents=True, exist_ok=True)
    for name, _w in TARGETS:
        shutil.copy2(FONT_DIR / name, bak / name)
    print(f"[备份] {bak}")
    for name, _w in TARGETS:
        shutil.copy2(d / name, FONT_DIR / name)
        print(f"[安装] {name}")
    print("[复核] 安装后覆盖检查 ……")
    cmd_check()


def main() -> None:
    ap = argparse.ArgumentParser(description="NotoSansSC 符号字形补齐构建")
    ap.add_argument("--check", action="store_true", help="只体检现有覆盖")
    ap.add_argument("--build", action="store_true", help="构建（逐目标 fork 子进程）")
    ap.add_argument("--build-one", nargs=4, metavar=("NAME", "WEIGHT", "OUT", "CACHE"),
                    help="内部：构建单个目标（由 --build 调用）")
    ap.add_argument("--verify", metavar="DIR", help="校验产物目录")
    ap.add_argument("--install", metavar="DIR", help="校验后备份并覆盖 assets/fonts/")
    ap.add_argument("--out", metavar="DIR", default=None, help="构建输出目录（默认 assets/fonts/）")
    ap.add_argument("--only", metavar="NAME", default=None, help="只处理指定目标文件名")
    ap.add_argument("--cache", metavar="DIR",
                    default=str(Path.home() / ".cache" / "career-manager-fonts"),
                    help="源字体缓存目录")
    a = ap.parse_args()
    if a.build_one:
        _build_one(a.build_one[0], int(a.build_one[1]), Path(a.build_one[2]), Path(a.build_one[3]))
    elif a.verify:
        cmd_verify(Path(a.verify))
    elif a.install:
        cmd_install(Path(a.install))
    elif a.build:
        cmd_build(Path(a.out) if a.out else FONT_DIR, Path(a.cache), a.only)
    elif a.check:
        cmd_check()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
