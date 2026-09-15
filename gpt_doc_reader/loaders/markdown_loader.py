"""
Markdown 加载器
"""


class MarkdownLoader:
    """Markdown 文件加载器"""
    
    def load(self, file_path: str) -> str:
        """加载 Markdown 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
