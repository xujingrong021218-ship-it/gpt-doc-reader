"""
主文档读取器 - 支持多种格式
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class Document:
    """文档对象 - 统一的文档接口"""
    
    def __init__(self, content: str, filename: str, doc_type: str, raw_data: Optional[Any] = None):
        self.content = content
        self.filename = filename
        self.doc_type = doc_type
        self.raw_data = raw_data
        self.created_at = datetime.now()
        self.metadata = {}
    
    def get_text(self) -> str:
        """获取纯文本内容"""
        return self.content
    
    def get_structure(self) -> Dict[str, Any]:
        """获取文档结构（章节、段落等）"""
        from .processors import StructureAnalyzer
        analyzer = StructureAnalyzer()
        return analyzer.analyze(self.content)
    
    def get_summary(self, length: str = 'medium') -> str:
        """生成摘要
        
        Args:
            length: 'short', 'medium', 'long'
        """
        from .processors import Summarizer
        summarizer = Summarizer()
        return summarizer.summarize(self.content, length)
    
    def get_table_of_contents(self) -> list:
        """生成目录"""
        structure = self.get_structure()
        return structure.get('chapters', [])
    
    def get_highlights(self) -> list:
        """提取重点内容"""
        from .processors import TextExtractor
        extractor = TextExtractor()
        return extractor.extract_highlights(self.content)
    
    def search(self, keyword: str) -> list:
        """搜索关键词"""
        from .processors import TextExtractor
        extractor = TextExtractor()
        return extractor.search(self.content, keyword)
    
    def export(self, format: str) -> str:
        """导出为其他格式
        
        Args:
            format: 'markdown', 'txt', 'html'
        """
        from .processors import TextExtractor
        extractor = TextExtractor()
        
        if format == 'markdown':
            return extractor.to_markdown(self.content, self.get_structure())
        elif format == 'txt':
            return self.content
        elif format == 'html':
            return extractor.to_html(self.content)
        return self.content
    
    def __repr__(self):
        return f"Document(name='{self.filename}', type='{self.doc_type}', size={len(self.content)} chars)"


class DocumentReader:
    """统一的文档读取器"""
    
    def __init__(self):
        from .loaders.pdf_loader import PDFLoader
        from .loaders.word_loader import WordLoader
        from .loaders.image_loader import ImageLoader
        from .loaders.markdown_loader import MarkdownLoader
        from .loaders.text_loader import TextLoader
        
        self.loaders = {
            'pdf': PDFLoader(),
            'docx': WordLoader(),
            'doc': WordLoader(),
            'png': ImageLoader(),
            'jpg': ImageLoader(),
            'jpeg': ImageLoader(),
            'md': MarkdownLoader(),
            'markdown': MarkdownLoader(),
            'txt': TextLoader(),
        }
        self.documents = {}
    
    def load(self, file_path: str) -> Document:
        """加载任何格式的文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            Document 对象
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 获取文件扩展名
        ext = path.suffix.lstrip('.').lower()
        
        if ext not in self.loaders:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        # 使用对应的加载器
        loader = self.loaders[ext]
        content = loader.load(file_path)
        
        doc = Document(
            content=content,
            filename=path.name,
            doc_type=ext,
            raw_data={'file_path': str(path), 'file_size': path.stat().st_size}
        )
        
        self.documents[path.name] = doc
        return doc
    
    def load_from_text(self, text: str, filename: str = "document.txt") -> Document:
        """从纯文本加载"""
        doc = Document(
            content=text,
            filename=filename,
            doc_type='txt'
        )
        self.documents[filename] = doc
        return doc
    
    def get_document(self, filename: str) -> Optional[Document]:
        """获取已加载的文档"""
        return self.documents.get(filename)
    
    def list_documents(self) -> list:
        """列出所有已加载的文档"""
        return list(self.documents.values())
