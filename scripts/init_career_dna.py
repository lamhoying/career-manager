#!/usr/bin/env python3
"""
init_career_dna.py - Initialize Career DNA directory structure.

Creates the career-dna/ directory with all 10 template files.
Usage:
    python3 init_career_dna.py [target_directory]

If target_directory is omitted, creates in current working directory.
"""

import os
import sys
import shutil
from pathlib import Path

# Template files to create (filename, description)
# v1.3: 10_career_tracks is now a directory, not a single file
CAREER_DNA_FILES = [
    ("01_profile.md", "个人职业档案"),
    ("02_timeline.md", "职业发展轨迹"),
    ("03_projects.md", "项目资产库"),
    ("04_skill_graph.md", "能力图谱"),
    ("05_story_bank.md", "面试故事库"),
    ("06_failure_story.md", "失败案例库"),
    ("07_career_identity.md", "职业身份库"),
    ("08_question_backlog.md", "待补充问题库"),
    ("09_completeness_report.md", "完整度报告"),
    ("11_online_profile.md", "在线职业档案（派生资产 v1.5）"),
]

# Also create output directories
# v1.3: removed job-tracks (merged into career-dna/10_career_tracks/)
OUTPUT_DIRS = ["resume-outputs"]

# Knowledge Layer directories (v1.1+)
KNOWLEDGE_DIRS = ["knowledge/role_snapshots", "knowledge/skill_snapshots"]

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

    print(f"\n🎉 Career DNA 初始化完成！")
    print(f"   目录: {career_dna_dir}")
    print(f"   文件数: {len(CAREER_DNA_FILES)} + 10_career_tracks/")
    print(f"   知识层: knowledge/role_snapshots/, knowledge/skill_snapshots/")
    print(f"   赛道库: {CAREER_TRACKS_DIR}/")
    print(f"\n下一步: 开始填写 Career DNA 文件，或上传简历让 AI 帮你解析。")
    return True


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    init_career_dna(target_dir)


if __name__ == "__main__":
    main()
