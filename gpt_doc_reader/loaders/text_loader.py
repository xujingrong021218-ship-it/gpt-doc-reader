"""
纯文本加载器
"""


class TextLoader:
    """纯文本文件加载器"""
    
    def load(self, file_path: str) -> str:
        """加载纯文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
