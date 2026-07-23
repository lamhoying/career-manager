#!/usr/bin/env python3
"""
completeness_checker.py - Scan Career DNA files and calculate completeness.

Analyzes each career-dna/*.md file for content completeness based on
heuristics (non-empty fields, filled tables, presence of placeholders).

Usage:
    python3 completeness_checker.py [career-dna_directory]

If directory is omitted, looks for ./career-dna/

Output: Prints a completeness report and optionally updates 09_completeness_report.md
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Files to check and their weights in overall score
# v1.3: 10_career_tracks is a directory, not a single file
# v1.5: 11_online_profile is a derived asset, low weight
MODULE_CONFIG = {
    "01_profile.md": {"name": "Profile", "weight": 10},
    "02_timeline.md": {"name": "Timeline", "weight": 14},
    "03_projects.md": {"name": "Projects", "weight": 20},
    "04_skill_graph.md": {"name": "Skill Graph", "weight": 20},
    "05_story_bank.md": {"name": "Story Bank", "weight": 9},
    "06_failure_story.md": {"name": "Failure Story", "weight": 5},
    "07_career_identity.md": {"name": "Career Identity", "weight": 9},
    "08_question_backlog.md": {"name": "Question Backlog", "weight": 5},
    "10_career_tracks": {"name": "Career Tracks", "weight": 5, "is_dir": True},
    "11_online_profile.md": {"name": "Online Profile", "weight": 3},
}

# Placeholders that indicate unfilled content
PLACEHOLDERS = [
    "[待补充]",
    "[待填写]",
    "[项目名称]",
    "[故事标题]",
    "[案例标题]",
    "[方向名称",
    "[公司名]",
    "[竞争力1]",
    "[能力1]",
    "（待填写）",
    "（暂无",
]


def check_file_completeness(filepath: Path) -> tuple:
    """
    Check completeness of a single file or directory.
    Returns (completeness_percentage, details).
    """
    if not filepath.exists():
        return 0, {"reason": "文件/目录不存在"}

    # v1.3: Handle directory (10_career_tracks/)
    if filepath.is_dir():
        track_files = list(filepath.glob("*.md"))
        # Must have README.md and at least 1 track file
        has_readme = (filepath / "README.md").exists()
        track_count = sum(1 for f in track_files if f.name != "README.md")
        if has_readme and track_count >= 1:
            return 100, {"reason": f"OK: README.md + {track_count} track files"}
        elif has_readme:
            return 50, {"reason": "有 README.md 但无 track 文件（需 Mode A 构建）"}
        elif track_count >= 1:
            return 40, {"reason": "有 track 文件但缺少 README.md"}
        else:
            return 10, {"reason": "目录为空，需 Mode A 构建"}
    # End directory handling

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Remove empty lines and comment lines
    content_lines = [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("<!--") and not line.strip().startswith("-->")
    ]

    if not content_lines:
        return 0, {"reason": "文件为空"}

    total_fields = 0
    filled_fields = 0
    placeholder_count = 0

    # Count placeholder occurrences
    for placeholder in PLACEHOLDERS:
        placeholder_count += content.count(placeholder)

    # Count table rows (lines starting with |)
    table_rows = [l for l in content_lines if l.startswith("|") and not l.startswith("|--") and not l.startswith("|-")]
    # Filter out header rows
    data_rows = [r for r in table_rows if not all(c == "-" or c == " " or c == "|" for c in r.replace("|", "").strip()[:3])]

    # Count filled fields (lines with content after : or - or in tables)
    for line in content_lines:
        # Check for field patterns like "- **Field**：" or "| value |"
        if line.startswith("- **") and "**" in line[4:]:
            total_fields += 1
            # Check if there's actual content after the field name
            after_colon = line.split("：", 1)[-1].strip() if "：" in line else line.split(":", 1)[-1].strip()
            if after_colon and after_colon not in PLACEHOLDERS and len(after_colon) > 2:
                filled_fields += 1
        elif line.startswith("|") and not line.startswith("|--"):
            # Table row
            cells = [c.strip() for c in line.split("|")[1:-1]]
            for cell in cells:
                if cell and cell != "---" and not cell.startswith("-"):
                    total_fields += 1
                    if cell not in PLACEHOLDERS and len(cell) > 1:
                        filled_fields += 1

    # Count numbered items (### N. or ## N.)
    numbered_sections = len(re.findall(r"^##+\s+\d+\.", content, re.MULTILINE))

    # Calculate completeness
    if total_fields > 0:
        field_ratio = filled_fields / total_fields
    else:
        # Fallback: use content density
        content_chars = len(content.replace("\n", "").replace(" ", ""))
        field_ratio = min(content_chars / 500, 1.0)  # 500 chars = 100%

    # Penalize for placeholders
    placeholder_penalty = min(placeholder_count * 0.05, 0.3)
    completeness = max(0, (field_ratio - placeholder_penalty) * 100)

    # Bonus for having multiple sections/content
    if numbered_sections >= 2:
        completeness = min(100, completeness + 10)

    # Special handling for question_backlog - having open questions is fine
    if filepath.name == "08_question_backlog.md":
        # Backlog is complete if it exists and has structure
        if "Open" in content and "Answered" in content:
            completeness = 100
        else:
            completeness = 50

    details = {
        "total_fields": total_fields,
        "filled_fields": filled_fields,
        "placeholders": placeholder_count,
        "sections": numbered_sections,
        "reason": "OK" if completeness > 30 else "内容不足",
    }

    return round(completeness), details


def get_grade(score: int) -> str:
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 40:
        return "C"
    else:
        return "D"


def get_status_icon(score: int) -> str:
    if score >= 70:
        return "✅"
    elif score >= 40:
        return "⚠️"
    else:
        return "❌"


def run_check(career_dna_dir: str = "./career-dna"):
    """Run completeness check on career-dna directory."""
    base_path = Path(career_dna_dir).resolve()

    if not base_path.exists():
        print(f"❌ 目录不存在: {base_path}")
        print("   请先运行 init_career_dna.py 初始化 Career DNA。")
        return None

    results = {}
    total_weight = 0
    weighted_sum = 0

    print("=" * 60)
    print("  Career DNA 完整度报告")
    print(f"  目录: {base_path}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    print(f"{'模块':<25} {'完整度':>8} {'权重':>6} {'状态':>6}")
    print("-" * 50)

    for filename, config in MODULE_CONFIG.items():
        is_dir = config.get("is_dir", False)
        filepath = base_path / filename
        if is_dir:
            score, details = check_file_completeness(filepath)
        else:
            score, details = check_file_completeness(filepath)
        results[filename] = {"score": score, "details": details, **config}

        weighted_sum += score * config["weight"]
        total_weight += config["weight"]

        icon = get_status_icon(score)
        print(f"  {config['name']:<23} {score:>6}%  {config['weight']:>5}%  {icon:>4}")

    overall_score = round(weighted_sum / total_weight) if total_weight > 0 else 0
    overall_grade = get_grade(overall_score)
    overall_icon = get_status_icon(overall_score)

    print("-" * 50)
    print(f"  {'整体完整度':<23} {overall_score:>6}%  {'100%':>5}%  {overall_icon:>4}")
    print(f"  等级: {overall_grade}")
    print()

    # Identify gaps
    gaps = []
    suggestions = []  # list of (text, priority) tuples
    for filename, result in results.items():
        if result["score"] < 50:
            gaps.append(f"{result['name']} ({result['score']}%)")
            if result["score"] == 0:
                suggestions.append((f" urgently needs to be filled - {result['name']}", "High"))
            else:
                suggestions.append((f" needs more content - {result['name']}", "Medium"))

    if gaps:
        print("📋 信息缺口:")
        for gap in gaps:
            print(f"   • {gap}")
        print()

    if suggestions:
        print("💡 建议补充项:")
        for i, (s, priority) in enumerate(suggestions, 1):
            print(f"   {i}. {s.strip()} (优先级: {priority})")
        print()

    # Generate report content
    report_content = generate_report(overall_score, overall_grade, results, gaps, suggestions)

    # Update 09_completeness_report.md
    report_path = base_path / "09_completeness_report.md"
    if report_path.exists() or True:
        report_path.write_text(report_content, encoding="utf-8")
        print(f"✅ 完整度报告已更新: {report_path}")

    return {"overall": overall_score, "grade": overall_grade, "modules": results}


def generate_report(overall_score, overall_grade, results, gaps, suggestions):
    """Generate markdown report content."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# 完整度报告 (Completeness Report)",
        "",
        "## 整体完整度",
        f"- **评分**：{overall_score}%",
        f"- **等级**：{overall_grade}",
        "",
        "## 各模块完整度",
        "",
        "| 模块 | 完整度 | 状态 |",
        "|------|--------|------|",
    ]

    for filename, result in results.items():
        icon = get_status_icon(result["score"])
        lines.append(f"| {result['name']} | {result['score']}% | {icon} |")

    lines.extend([
        "",
        "## 信息缺口",
    ])
    if gaps:
        for i, gap in enumerate(gaps, 1):
            lines.append(f"{i}. {gap}")
    else:
        lines.append("（暂无显著缺口）")

    lines.extend([
        "",
        "## 建议补充项",
    ])
    if suggestions:
        for i, (s, priority) in enumerate(suggestions, 1):
            lines.append(f"{i}. {s.strip()} (优先级: {priority})")
    else:
        lines.append("（暂无）")

    lines.extend([
        "",
        f"## 生成时间",
        f"{now}",
        "",
    ])

    return "\n".join(lines)


def main():
    career_dna_dir = sys.argv[1] if len(sys.argv) > 1 else "./career-dna"
    run_check(career_dna_dir)


if __name__ == "__main__":
    main()
