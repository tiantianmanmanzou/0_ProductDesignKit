"""将特定结构的Excel转换为分级标题的Markdown文档。"""

from __future__ import annotations

import argparse
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional

import openpyxl


def normalize(cell_value: Optional[object]) -> Optional[str]:
    """把单元格内容转换成去除首尾空格的字符串。"""

    if cell_value is None:
        return None
    text = str(cell_value).strip()
    return text or None


def build_tree(worksheet) -> Dict[str, OrderedDict]:
    """根据Excel中的层级关系构造有序树。"""

    hierarchy: Dict[str, OrderedDict] = OrderedDict()
    current_level_1: Optional[str] = None
    current_level_2: Optional[str] = None

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        level_1 = normalize(row[0]) if len(row) > 0 else None
        level_2 = normalize(row[1]) if len(row) > 1 else None
        level_3 = normalize(row[2]) if len(row) > 2 else None

        if level_1:
            current_level_1 = level_1
            hierarchy.setdefault(current_level_1, OrderedDict())
            current_level_2 = None

        if level_2:
            if not current_level_1:
                raise ValueError("检测到二级栏目，但缺少对应的一级栏目")
            current_level_2 = level_2
            hierarchy.setdefault(current_level_1, OrderedDict())
            hierarchy[current_level_1].setdefault(current_level_2, [])

        if level_3:
            if not current_level_1:
                raise ValueError("检测到三级栏目，但缺少对应的一级栏目")
            target_level_2 = current_level_2 or ""
            hierarchy[current_level_1].setdefault(target_level_2, [])
            if level_3 not in hierarchy[current_level_1][target_level_2]:
                hierarchy[current_level_1][target_level_2].append(level_3)

        # 确保当前的层级至少初始化
        if current_level_1 and current_level_1 not in hierarchy:
            hierarchy[current_level_1] = OrderedDict()
        if current_level_1 and current_level_2:
            hierarchy[current_level_1].setdefault(current_level_2, [])

    return hierarchy


def tree_to_markdown(tree: Dict[str, OrderedDict]) -> List[str]:
    """把层级树转换为Markdown行列表。"""

    lines: List[str] = []
    for level_1, level_2_map in tree.items():
        lines.append(f"# {level_1}")
        lines.append("")
        if not level_2_map:
            continue
        for level_2, level_3_items in level_2_map.items():
            if level_2:
                lines.append(f"## {level_2}")
            if level_3_items:
                for level_3 in level_3_items:
                    lines.append(f"### {level_3}")
            lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="将包含一级/二级/三级列的Excel转换为Markdown标题"
    )
    parser.add_argument("excel_path", type=Path, help="待转换的Excel文件路径")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出Markdown路径（默认与Excel同名）",
    )
    args = parser.parse_args()

    excel_path = args.excel_path.expanduser().resolve()
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel文件不存在: {excel_path}")

    output_path = args.output or excel_path.with_suffix(".md")
    output_path = output_path.expanduser().resolve()

    workbook = openpyxl.load_workbook(excel_path, data_only=True)
    worksheet = workbook.active

    tree = build_tree(worksheet)
    markdown_lines = tree_to_markdown(tree)

    output_path.write_text("\n".join(markdown_lines), encoding="utf-8")
    print(f"已生成Markdown: {output_path}")


if __name__ == "__main__":
    main()
