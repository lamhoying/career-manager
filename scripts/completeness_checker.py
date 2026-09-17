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

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# v2.9.1: 模块清单与权重改由 assets/career_dna_manifest.json 唯一定义。
# 此前同一份清单在本脚本 / init_career_dna.py / SKILL.md / career_dna_structure.md
# 各写一份，且口径已漂移（"10 个文件" vs "12 个文件"）。manifest 是唯一事实源，
# 未登记的 career-dna/ 根目录文件由 validate_career_dna.py 报 P0。
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


def build_module_config() -> dict:
    """从 manifest 派生 MODULE_CONFIG（只取 weight > 0 的 SSOT 条目）。"""
    manifest = json.loads(find_manifest().read_text(encoding="utf-8"))
    config = {}
    for entry in manifest["ssot_files"]:
        if entry.get("weight", 0) <= 0:
            continue  # 09_completeness_report.md 等 generated 产物不计分
        item = {"name": entry["name"], "weight": entry["weight"]}
        if entry.get("is_dir"):
            item["is_dir"] = True
        config[entry["filename"]] = item
    return config


MODULE_CONFIG = build_module_config()

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
    # v2.21.0：07 各层占位符形态（原词表不含 ⇒ 未填写的 07 被计入「已填」，报 100%）
    "[待声明]",
    "[一句话市场身份",
    "[定位方向",
    "[新兴定位",
    "[原始岗位",
    "[原始职能",
    "[起点经历]",
    "[能力维度",
    "[状态 A]",
    "[核心动作",
    "[为什么是核心]",
    "[为什么是支撑]",
    "[为什么是差异化]",
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

    # Special handling for 07_career_identity - Layer 2 未声明检测（v2.21.0 · F18）
    # 仅靠 PLACEHOLDERS 扣分不足（penalty 上限 0.3）。Layer 2 是身份锚点，
    # 其空值会让 Mode D / Online Profile 的硬身份锚点无兜底降级 ⇒ 单独设上限。
    layer2_reason = None
    if filepath.name == "07_career_identity.md":
        layer2_missing = ("[待声明]" in content) or (
            "[一句话市场身份" in content and "[定位方向" in content
        )
        if layer2_missing:
            completeness = min(completeness, 60)
            layer2_reason = "Layer 2（Career Positioning）未声明 —— 须走 Mode A Step 8 采集协议"

    details = {
        "total_fields": total_fields,
        "filled_fields": filled_fields,
        "placeholders": placeholder_count,
        "sections": numbered_sections,
        "reason": "OK" if completeness > 30 else "内容不足",
    }
    if layer2_reason:
        details["reason"] = layer2_reason

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
    print(f"  {'整体完整度':<23} {overall_score:>6}%  {total_weight:>5}%  {overall_icon:>4}")
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
    parser = argparse.ArgumentParser(
        prog="completeness_checker.py",
        description="扫描 Career DNA 文件并输出完整度报告。",
    )
    parser.add_argument(
        "career_dna_dir",
        nargs="?",
        default="./career-dna",
        help="career-dna 目录路径（默认为 ./career-dna）",
    )
    args = parser.parse_args()

    target = args.career_dna_dir
    # v2.18.0 修复（B2）：此前 `--help` 会被当成目录路径，输出「目录不存在」而不是帮助。
    if target.startswith("-"):
        parser.error(f"目录参数不得以 '-' 开头（收到 {target!r}）。")

    run_check(target)


if __name__ == "__main__":
    main()
