"""
Document format converters.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .reader import Document


class Converter(ABC):
    """Base class for document converters."""
    
    @abstractmethod
    def convert(self, document: Document) -> str:
        """Convert document to target format."""
        pass


class MarkdownConverter(Converter):
    """Convert documents to Markdown format."""
    
    def convert(self, document: Document) -> str:
        """
        Convert document to Markdown.
        
        Args:
            document: Document to convert
            
        Returns:
            Markdown formatted string
        """
        content = document.content
        
        # Ensure proper markdown formatting
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Add markdown syntax for headers if not already present
            if line.startswith('##') or line.startswith('###'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)


class PlainTextConverter(Converter):
    """Convert documents to plain text format."""
    
    def convert(self, document: Document) -> str:
        """Convert document to plain text."""
        return document.content


class JSONConverter(Converter):
    """Convert documents to JSON format."""
    
    def convert(self, document: Document) -> str:
        """Convert document to JSON."""
        import json
        
        data = {
            "filename": document.filename,
            "content": document.content,
            "metadata": document.metadata,
            "created_at": document.created_at.isoformat()
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)


class PDFConverter(Converter):
    """Convert documents to PDF format."""
    
    def __init__(self, title: Optional[str] = None):
        self.title = title
    
    def convert(self, document: Document) -> str:
        """
        Convert document to PDF format.
        Note: Returns instruction for PDF creation.
        Actual PDF generation requires additional libraries.
        
        Args:
            document: Document to convert
            
        Returns:
            Instruction string
        """
        instruction = f"""
To convert to PDF, use one of these libraries:
- reportlab: pip install reportlab
- weasyprint: pip install weasyprint
- pypdf: pip install pypdf

Example with reportlab:
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 750, "{document.filename}")
# Add your content here
c.save()
"""
        return instruction.strip()


class ConverterFactory:
    """Factory for creating converters."""
    
    _converters = {
        'markdown': MarkdownConverter,
        'md': MarkdownConverter,
        'text': PlainTextConverter,
        'txt': PlainTextConverter,
        'json': JSONConverter,
        'pdf': PDFConverter,
    }
    
    @classmethod
    def get_converter(cls, format_name: str) -> Converter:
        """
        Get a converter for the specified format.
        
        Args:
            format_name: The format to convert to
            
        Returns:
            Converter instance
            
        Raises:
            ValueError: If format is not supported
        """
        format_name = format_name.lower().strip()
        
        if format_name not in cls._converters:
            supported = ', '.join(cls._converters.keys())
            raise ValueError(f"Unsupported format: {format_name}. Supported: {supported}")
        
        converter_class = cls._converters[format_name]
        return converter_class()
    
    @classmethod
    def register_converter(cls, format_name: str, converter_class: type):
        """Register a new converter."""
        cls._converters[format_name.lower()] = converter_class