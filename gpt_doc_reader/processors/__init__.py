"""
处理模块 - 文本提取、结构分析、摘要生成
"""

import re
from typing import List, Dict, Any


class TextExtractor:
    """文本提取器"""
    
    @staticmethod
    def extract_highlights(text: str) -> List[str]:
        """提取重点（加粗、标题等）"""
        highlights = []
        
        for line in text.split('\n'):
            if line.startswith('#'):
                highlights.append(line.replace('#', '').strip())
        
        for line in text.split('\n'):
            if line.strip().startswith(('-', '*', '•')):
                highlights.append(line.strip()[1:].strip())
        
        return highlights
    
    @staticmethod
    def search(text: str, keyword: str) -> List[Dict[str, Any]]:
        """搜索关键词"""
        results = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                context = []
                if i > 0:
                    context.append(lines[i-1])
                context.append(line)
                if i < len(lines) - 1:
                    context.append(lines[i+1])
                
                results.append({
                    'line_number': i + 1,
                    'line': line,
                    'context': '\n'.join(context)
                })
        
        return results
    
    @staticmethod
    def to_markdown(text: str, structure: Dict = None) -> str:
        """转换为 Markdown 格式"""
        return text
    
    @staticmethod
    def to_html(text: str) -> str:
        """转换为 HTML 格式"""
        html = "<html><body>"
        for line in text.split('\n'):
            if line.startswith('# '):
                html += f"<h1>{line.replace('#', '').strip()}</h1>"
            elif line.startswith('## '):
                html += f"<h2>{line.replace('#', '').strip()}</h2>"
            elif line.startswith('### '):
                html += f"<h3>{line.replace('#', '').strip()}</h3>"
            elif line.strip():
                html += f"<p>{line}</p>"
        html += "</body></html>"
        return html


class StructureAnalyzer:
    """结构分析器"""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """分析文档结构"""
        chapters = []
        sections = []
        
        for i, line in enumerate(text.split('\n')):
            if line.startswith('# '):
                chapters.append({
                    'title': line.replace('#', '').strip(),
                    'level': 1,
                    'line': i + 1
                })
            elif line.startswith('## '):
                sections.append({
                    'title': line.replace('#', '').strip(),
                    'level': 2,
                    'line': i + 1
                })
        
        return {
            'chapters': chapters,
            'sections': sections,
            'total_lines': len(text.split('\n')),
            'word_count': len(text.split())
        }


class Summarizer:
    """摘要生成器"""
    
    def summarize(self, text: str, length: str = 'medium') -> str:
        """生成摘要"""
        paragraphs = text.split('\n\n')
        
        lengths = {
            'short': max(1, len(paragraphs) // 4),
            'medium': max(2, len(paragraphs) // 2),
            'long': max(3, int(len(paragraphs) * 0.75))
        }
        
        num_paragraphs = lengths.get(length, lengths['medium'])
        summary = '\n\n'.join(paragraphs[:num_paragraphs])
        
        return summary
