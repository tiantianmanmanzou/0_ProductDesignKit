#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX to Markdown Converter
将DOCX文档转换为Markdown格式，保留表格和标题层级关系
"""

import os
import argparse
from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


class DocxToMarkdownConverter:
    """DOCX转Markdown转换器"""
    
    def __init__(self, docx_path: str):
        """
        初始化转换器
        
        Args:
            docx_path: DOCX文件路径
        """
        self.docx_path = docx_path
        self.doc = Document(docx_path)
        self.markdown_lines = []
        
    def get_paragraph_style_level(self, paragraph: Paragraph) -> tuple:
        """
        获取段落的样式级别
        
        Args:
            paragraph: 段落对象
            
        Returns:
            (is_heading, level): 是否为标题，标题级别(1-6)
        """
        style_name = paragraph.style.name.lower()
        
        # 检查是否为标题样式
        if 'heading' in style_name:
            # 提取级别数字
            if 'heading 1' in style_name or style_name == 'heading1':
                return (True, 1)
            elif 'heading 2' in style_name or style_name == 'heading2':
                return (True, 2)
            elif 'heading 3' in style_name or style_name == 'heading3':
                return (True, 3)
            elif 'heading 4' in style_name or style_name == 'heading4':
                return (True, 4)
            elif 'heading 5' in style_name or style_name == 'heading5':
                return (True, 5)
            elif 'heading 6' in style_name or style_name == 'heading6':
                return (True, 6)
        
        # 检查中文标题样式
        if '标题' in style_name:
            if '标题 1' in style_name or style_name == '标题1':
                return (True, 1)
            elif '标题 2' in style_name or style_name == '标题2':
                return (True, 2)
            elif '标题 3' in style_name or style_name == '标题3':
                return (True, 3)
            elif '标题 4' in style_name or style_name == '标题4':
                return (True, 4)
            elif '标题 5' in style_name or style_name == '标题5':
                return (True, 5)
            elif '标题 6' in style_name or style_name == '标题6':
                return (True, 6)
        
        # 基于格式判断标题级别（字体大小和加粗）
        if paragraph.runs:
            first_run = paragraph.runs[0]
            is_bold = first_run.font.bold
            font_size = first_run.font.size
            
            # 如果段落加粗且字体较大，判断为标题
            if is_bold and font_size:
                # 字体大小单位是 twips (1/20 point)
                # 转换为磅值进行判断
                size_pt = font_size.pt if hasattr(font_size, 'pt') else font_size / 12700
                
                # 根据字体大小判断标题级别
                if size_pt >= 18:  # 一级标题
                    return (True, 1)
                elif size_pt >= 16:  # 二级标题
                    return (True, 2)
                elif size_pt >= 14:  # 三级标题
                    return (True, 3)
                elif size_pt >= 12:  # 四级标题
                    return (True, 4)
                elif size_pt >= 10:  # 五级标题
                    return (True, 5)
                elif size_pt >= 8:  # 六级标题
                    return (True, 6)
        
        return (False, 0)
    
    def convert_paragraph(self, paragraph: Paragraph) -> str:
        """
        转换段落为Markdown格式
        
        Args:
            paragraph: 段落对象
            
        Returns:
            Markdown格式的文本
        """
        text = paragraph.text.strip()
        if not text:
            return ""
        
        is_heading, level = self.get_paragraph_style_level(paragraph)
        
        if is_heading:
            # 标题格式
            return f"{'#' * level} {text}\n"
        else:
            # 普通正文
            return f"{text}\n"
    
    def convert_table(self, table: Table) -> str:
        """
        转换表格为Markdown格式
        
        Args:
            table: 表格对象
            
        Returns:
            Markdown格式的表格
        """
        if not table.rows:
            return ""
        
        markdown_table = []
        
        # 处理表格的每一行
        for row_idx, row in enumerate(table.rows):
            row_cells = []
            for cell in row.cells:
                # 获取单元格文本，处理多行内容
                cell_text = cell.text.strip().replace('\n', '<br>')
                row_cells.append(cell_text)
            
            # 添加表格行
            markdown_table.append("| " + " | ".join(row_cells) + " |")
            
            # 在第一行后添加分隔符
            if row_idx == 0:
                separator = "| " + " | ".join(["---"] * len(row_cells)) + " |"
                markdown_table.append(separator)
        
        return "\n".join(markdown_table) + "\n"
    
    def convert(self) -> str:
        """
        执行转换
        
        Returns:
            Markdown格式的文本
        """
        self.markdown_lines = []
        
        # 遍历文档中的所有元素
        for element in self.doc.element.body:
            if isinstance(element, CT_P):
                # 段落元素
                paragraph = Paragraph(element, self.doc)
                md_text = self.convert_paragraph(paragraph)
                if md_text:
                    self.markdown_lines.append(md_text)
            
            elif isinstance(element, CT_Tbl):
                # 表格元素
                table = Table(element, self.doc)
                md_table = self.convert_table(table)
                if md_table:
                    self.markdown_lines.append(md_table)
                    self.markdown_lines.append("")  # 表格后添加空行
        
        return "\n".join(self.markdown_lines)
    
    def save_to_file(self, output_path: str):
        """
        保存转换结果到文件
        
        Args:
            output_path: 输出文件路径
        """
        markdown_content = self.convert()
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ 转换完成！")
        print(f"📄 输入文件: {self.docx_path}")
        print(f"📝 输出文件: {output_path}")
        print(f"📊 文档统计:")
        print(f"   - 段落数: {len(self.doc.paragraphs)}")
        print(f"   - 表格数: {len(self.doc.tables)}")


def main():
    """主函数"""
    default_input_file = "/Users/zhangxy/GenAI/DocPilot/docs/yunnan01/低空标准化共享服务产品及能力开发项目COSMIC送审word-需求规格说明书(0916-汇总）.docx"

    parser = argparse.ArgumentParser(
        description="将DOCX文档转换为Markdown格式，保留表格和标题层级关系"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=default_input_file,
        help="输入 DOCX 文件路径（默认使用脚本内置示例文件）",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        default=None,
        help="输出 Markdown 文件路径（默认与输入文件同目录同名，扩展名为 .md）",
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or (os.path.splitext(input_file)[0] + ".md")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误: 文件不存在 - {input_file}")
        return
    
    try:
        # 创建转换器并执行转换
        converter = DocxToMarkdownConverter(input_file)
        converter.save_to_file(output_file)
        
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
