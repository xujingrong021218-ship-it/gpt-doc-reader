"""
PDF 加载器
"""


class PDFLoader:
    """PDF 文件加载器"""
    
    def load(self, file_path: str) -> str:
        """加载 PDF 文件"""
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("请安装 pdfplumber: pip install pdfplumber")
        
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        
        return "\n\n".join(text)
