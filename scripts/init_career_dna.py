#!/usr/bin/env python3
"""
init_career_dna.py - Initialize Career DNA directory structure.

Creates the four-layer skeleton declared in SKILL.md:
    career-dna/            SSOT 文件（清单见 assets/career_dna_manifest.json）
    knowledge/             role_snapshots / skill_snapshots
    resume-outputs/        Mode D 产物
    application-tracker/   Mode E 投递追踪（01_application_index.md 是 Mode E 的前置条件）

Usage:
    python3 init_career_dna.py [target_directory]

If target_directory is omitted, creates in current working directory.

v2.18.0 修复：任何以 '-' 开头的参数都会被拒绝。此前 `sys.argv[1]` 无校验，
误传 flag（如 --help / --dry-run）会被当成目标路径，静默在 CWD 建出一整套 SSOT 目录。
"""

import argparse
import json
import os
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# v2.9.1: Career DNA 文件清单改由 assets/career_dna_manifest.json 唯一定义。
# 本脚本不再持有硬编码清单 —— 此前清单散落在 4 处（本脚本 / completeness_checker.py /
# SKILL.md / career_dna_structure.md）且口径已漂移（10 vs 12）。任何新增文件必须先在
# manifest 登记，否则 validate_career_dna.py 报 P0（orphan）。
# ---------------------------------------------------------------------------

MANIFEST_REL = Path("assets") / "career_dna_manifest.json"


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


def load_manifest() -> dict:
    return json.loads(find_manifest().read_text(encoding="utf-8"))


_MANIFEST = load_manifest()

# Template files to create (filename, description)
# v1.3: 10_career_tracks is now a directory, not a single file (is_dir=true in manifest)
CAREER_DNA_FILES = [
    (entry["filename"], entry["desc"])
    for entry in _MANIFEST["ssot_files"]
    if not entry.get("is_dir")
]

# Also create output directories
# v1.3: removed job-tracks (merged into career-dna/10_career_tracks/)
OUTPUT_DIRS = ["resume-outputs"]

# Knowledge Layer directories (v1.1+)
KNOWLEDGE_DIRS = ["knowledge/role_snapshots", "knowledge/skill_snapshots"]

# Application Tracker Layer（v2.18.0 新增）
# 此前 init 不建此层 → SKILL.md 声明的四层架构与初始化脚本不一致，
# 且 Mode E 的前置条件（application-tracker/01_application_index.md 必须存在）
# 在新用户首次初始化后必然不满足。
TRACKER_DIR = "application-tracker"
TRACKER_FILES = ["01_application_index.md", "02_status_definitions.md"]
TRACKER_SUBDIRS = ["archives"]

# Career Tracks directory (v1.3+)
CAREER_TRACKS_DIR = "career-dna/10_career_tracks"

# Career Tracks README template (v1.3+)
CAREER_TRACKS_README = """# Career Tracks Overview（赛道总览）

<!--
职业赛道总览 — v1.3 目录模式。
列出所有 Career Track 及其 Confidence 摘要。
每个 Track 的详细信息见对应的 {track}.md 文件。
-->

| Track | Confidence | Target Roles | Last Updated |
|-------|------------|-------------|--------------|
| （待 Mode A 构建） | - | - | - |

## 说明

- **Track**: 职业赛道名称
- **Confidence**: 用户在该赛道的整体匹配置信度 (0-100)
- **Target Roles**: 该赛道下可投递的具体岗位
- **Last Updated**: 最近一次更新时间

每个 Track 的详细内容（Positioning / Career Narrative / Evidence / Core Strengths / Known Gaps 等）见对应文件。
"""

# Career DNA 草稿区说明（v2.9.1+）—— 下划线前缀 = 非 SSOT
DRAFT_README = """# _inbox — Career DNA 草稿区（非 SSOT）

这里放**临时产物**：某次提问生成的分析、尚未定稿的策略稿、待整理但还不属于任何
已登记文件的素材。

## 规则

- 下划线前缀 = **非 SSOT**。本目录不参与完整度计分，可随时清理。
- 正式资产**不得**引用本目录内容；要引用必须先转正。
- **转正路径**：走「四件套登记」——① 在 `assets/career_dna_manifest.json` 增加条目
  ② 提供同名模板 ③ 给出权重 ④ 同步 SKILL.md 目录树 / Mode A 产物计数 / Resources。

## 自检

```
python3 scripts/validate_career_dna.py <career-dna目录>
```

未登记文件出现在 career-dna/ 根目录会被判为 P0 orphan。
"""


def get_template_dir():
    """Find the templates directory relative to this script."""
    script_path = Path(__file__).resolve().parent
    template_dir = script_path.parent / "assets" / "templates" / "career-dna"
    if not template_dir.exists():
        # Fallback: try relative to skill root
        template_dir = script_path.parent / "assets" / "templates" / "career-dna"
    return template_dir


def init_career_dna(target_dir: str = "."):
    """Initialize career-dna directory with template files."""
    target_path = Path(target_dir).resolve()
    career_dna_dir = target_path / "career-dna"

    # Check if career-dna already exists
    if career_dna_dir.exists():
        existing_files = list(career_dna_dir.glob("*.md"))
        if existing_files:
            print(f"⚠️  career-dna/ 目录已存在于: {career_dna_dir}")
            print(f"   已有 {len(existing_files)} 个文件。")
            response = input("   是否覆盖？(y/N): ").strip().lower()
            if response != "y":
                print("   已取消。未做任何更改。")
                return False
            shutil.rmtree(career_dna_dir)

    # Create career-dna directory
    career_dna_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 创建目录: {career_dna_dir}")

    # Get template directory
    template_dir = get_template_dir()

    if template_dir.exists():
        # Copy templates from assets
        for filename, desc in CAREER_DNA_FILES:
            src = template_dir / filename
            dst = career_dna_dir / filename
            if src.exists():
                shutil.copy2(src, dst)
                print(f"✅ 创建文件: {filename} ({desc})")
            else:
                # Create empty file with header if template not found
                dst.write_text(f"# {desc}\n\n（待填写）\n", encoding="utf-8")
                print(f"✅ 创建文件: {filename} ({desc}) [空模板]")
    else:
        # Templates not found, create minimal files
        for filename, desc in CAREER_DNA_FILES:
            dst = career_dna_dir / filename
            dst.write_text(f"# {desc}\n\n（待填写）\n", encoding="utf-8")
            print(f"✅ 创建文件: {filename} ({desc}) [空模板]")

    # Create output directories
    for dir_name in OUTPUT_DIRS:
        output_dir = target_path / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to preserve empty directory
        gitkeep = output_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
        print(f"✅ 创建目录: {dir_name}/")

    # Create Knowledge Layer directories (v1.1+)
    for dir_name in KNOWLEDGE_DIRS:
        knowledge_dir = target_path / dir_name
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = knowledge_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
        print(f"✅ 创建目录: {dir_name}/")

    # Create Career Tracks directory (v1.3+)
    career_tracks_dir = target_path / CAREER_TRACKS_DIR
    career_tracks_dir.mkdir(parents=True, exist_ok=True)
    # Create README.md
    readme_path = career_tracks_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text(CAREER_TRACKS_README, encoding="utf-8")
    print(f"✅ 创建目录: {CAREER_TRACKS_DIR}/ (含 README.md)")

    # Create Application Tracker layer (v2.18.0+)
    tracker_dir = target_path / TRACKER_DIR
    tracker_dir.mkdir(parents=True, exist_ok=True)
    tracker_tpl_dir = template_dir.parent / TRACKER_DIR
    for filename in TRACKER_FILES:
        src = tracker_tpl_dir / filename
        dst = tracker_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ 创建文件: {TRACKER_DIR}/{filename}")
        else:
            dst.write_text(f"# {filename}\n\n（待填写）\n", encoding="utf-8")
            print(f"✅ 创建文件: {TRACKER_DIR}/{filename} [空模板]")
    for sub in TRACKER_SUBDIRS:
        sub_dir = tracker_dir / sub
        sub_dir.mkdir(parents=True, exist_ok=True)
        archive_tpl = tracker_tpl_dir / sub
        if archive_tpl.exists():
            for tpl in sorted(archive_tpl.glob("*.md")):
                shutil.copy2(tpl, sub_dir / tpl.name)
    print(f"✅ 创建目录: {TRACKER_DIR}/ (含 archives/)")

    # Create draft area (v2.9.1+) —— 下划线前缀 = 非 SSOT，不参与完整度计分
    draft_name = _MANIFEST.get("draft_dir", "_inbox")
    draft_dir = career_dna_dir / draft_name
    draft_dir.mkdir(parents=True, exist_ok=True)
    draft_readme = draft_dir / "README.md"
    if not draft_readme.exists():
        draft_readme.write_text(DRAFT_README, encoding="utf-8")
    print(f"✅ 创建目录: career-dna/{draft_name}/ (草稿区)")

    print(f"\n🎉 Career DNA 初始化完成！")
    print(f"   目录: {career_dna_dir}")
    print(f"   文件数: {len(CAREER_DNA_FILES)} + 10_career_tracks/")
    print(f"   知识层: knowledge/role_snapshots/, knowledge/skill_snapshots/")
    print(f"   赛道库: {CAREER_TRACKS_DIR}/")
    print(f"   投递追踪: {TRACKER_DIR}/ (含 archives/)")
    print(f"\n下一步: 开始填写 Career DNA 文件，或上传简历让 AI 帮你解析。")
    return True


def main():
    parser = argparse.ArgumentParser(
        prog="init_career_dna.py",
        description="初始化 Career DNA 四层目录结构（career-dna/ · knowledge/ · resume-outputs/ · application-tracker/）。",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="目标目录（默认为当前工作目录）",
    )
    args = parser.parse_args()

    target = args.target_dir
    # v2.18.0 修复（B1）：argparse 已拦截未知 flag（--dry-run 等会直接报错退出），
    # 此处再拦一次以 '-' 开头的位置参数（如单写 `-`），并拒绝「存在但非目录」的路径。
    if target.startswith("-"):
        parser.error(f"目标目录不得以 '-' 开头（收到 {target!r}）—— 这通常是误传的 flag。")
    existing = Path(target)
    if existing.exists() and not existing.is_dir():
        parser.error(f"目标路径已存在但不是目录: {existing}")

    init_career_dna(target)


if __name__ == "__main__":
    main()
