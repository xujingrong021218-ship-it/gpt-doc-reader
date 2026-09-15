"""
Main document reader module for GPT-generated documents.
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class Document:
    """Represents a document with metadata."""
    
    def __init__(self, content: str, filename: str = "", metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.filename = filename
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.processed = False
    
    def __repr__(self):
        return f"Document(filename='{self.filename}', size={len(self.content)} chars)"


class DocumentReader:
    """Reader for ChatGPT-generated documents."""
    
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding
        self.documents: Dict[str, Document] = {}
    
    def load_document(self, file_path: str) -> Document:
        """
        Load a document from file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Document object
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        with open(path, 'r', encoding=self.encoding) as f:
            content = f.read()
        
        doc = Document(
            content=content,
            filename=path.name,
            metadata={"file_path": str(path), "file_size": path.stat().st_size}
        )
        
        self.documents[path.name] = doc
        return doc
    
    def load_from_text(self, text: str, filename: str = "document.txt") -> Document:
        """
        Load a document from text content.
        
        Args:
            text: Document content as text
            filename: Name to assign to the document
            
        Returns:
            Document object
        """
        doc = Document(content=text, filename=filename)
        self.documents[filename] = doc
        return doc
    
    def load_from_url(self, url: str) -> Optional[Document]:
        """
        Load a document from a URL (requires requests library).
        
        Args:
            url: URL to fetch document from
            
        Returns:
            Document object or None if failed
        """
        try:
            import requests
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            filename = url.split('/')[-1] or "document.txt"
            doc = Document(
                content=response.text,
                filename=filename,
                metadata={"source_url": url, "status_code": response.status_code}
            )
            self.documents[filename] = doc
            return doc
        except Exception as e:
            print(f"Error loading from URL: {e}")
            return None
    
    def get_document(self, filename: str) -> Optional[Document]:
        """Get a loaded document by filename."""
        return self.documents.get(filename)
    
    def list_documents(self) -> list:
        """List all loaded documents."""
        return list(self.documents.values())
    
    def read_document(self, document: Document) -> str:
        """
        Read and return the full document content.
        
        Args:
            document: The document to read
            
        Returns:
            Full document content as string
        """
        return document.content
    
    def read_lines(self, document: Document) -> List[str]:
        """
        Read document as lines.
        
        Args:
            document: The document to read
            
        Returns:
            List of lines
        """
        return document.content.split('\n')
    
    def read_paragraphs(self, document: Document) -> List[str]:
        """
        Read document as paragraphs (separated by blank lines).
        
        Args:
            document: The document to read
            
        Returns:
            List of paragraphs
        """
        paragraphs = document.content.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def read_section(self, document: Document, section_name: str) -> Optional[str]:
        """
        Read a specific section from document.
        
        Args:
            document: The document to read from
            section_name: Name of section to read
            
        Returns:
            Section content or None if not found
        """
        sections = self.extract_sections(document)
        return sections.get(section_name.lower())
    
    def extract_sections(self, document: Document) -> Dict[str, str]:
        """
        Extract sections from a document based on headers.
        
        Args:
            document: The document to extract sections from
            
        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {}
        current_section = "introduction"
        current_content = []
        
        for line in document.content.split('\n'):
            if line.startswith('#'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                    current_content = []
                current_section = line.replace('#', '').strip().lower()
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def search(self, document: Document, keyword: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search for keyword in document.
        
        Args:
            document: The document to search
            keyword: Keyword to search for
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matches with line number and context
        """
        results = []
        lines = document.content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if case_sensitive:
                if keyword in line:
                    results.append({
                        'line_number': line_num,
                        'line': line,
                        'position': line.find(keyword)
                    })
            else:
                if keyword.lower() in line.lower():
                    results.append({
                        'line_number': line_num,
                        'line': line,
                        'position': line.lower().find(keyword.lower())
                    })
        
        return results
    
    def get_summary(self, document: Document, max_lines: int = 5) -> str:
        """
        Get a summary of the document (first N lines).
        
        Args:
            document: The document to summarize
            max_lines: Maximum number of lines to return
            
        Returns:
            Summary text
        """
        lines = document.content.split('\n')
        summary_lines = [line for line in lines[:max_lines] if line.strip()]
        return '\n'.join(summary_lines)
    
    def get_statistics(self, document: Document) -> Dict[str, Any]:
        """
        Get statistics about the document.
        
        Args:
            document: The document to analyze
            
        Returns:
            Dictionary with various statistics
        """
        lines = document.content.split('\n')
        words = document.content.split()
        sentences = re.split(r'[.!?]+', document.content)
        
        return {
            'total_characters': len(document.content),
            'total_words': len(words),
            'total_lines': len(lines),
            'total_sentences': len([s for s in sentences if s.strip()]),
            'total_paragraphs': len(self.read_paragraphs(document)),
            'average_words_per_line': round(len(words) / len(lines), 2) if lines else 0,
            'average_line_length': round(len(document.content) / len(lines), 2) if lines else 0,
        }
    
    def extract_keywords(self, document: Document, top_n: int = 10) -> List[tuple]:
        """
        Extract top keywords from document.
        
        Args:
            document: The document to analyze
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, frequency) tuples
        """
        # Simple keyword extraction - filter common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'is', 'was', 'are', 'be', 'have', 'has', 'had', 'do',
                     'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                     'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                     'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why',
                     'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
                     'some', 'such', 'no', 'nor', 'not', 'only', 'same', 'so', 'than',
                     'too', 'very', 'just', 'as', 'if', 'then'}
        
        words = re.findall(r'\b\w+\b', document.content.lower())
        word_freq = {}
        
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:top_n]
    
    def clean_content(self, document: Document) -> str:
        """
        Clean and normalize document content.
        
        Args:
            document: The document to clean
            
        Returns:
            Cleaned content
        """
        lines = document.content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove extra whitespace
            line = line.rstrip()
            cleaned_lines.append(line)
        
        # Remove multiple consecutive blank lines
        result = []
        prev_blank = False
        for line in cleaned_lines:
            is_blank = not line.strip()
            if not (is_blank and prev_blank):
                result.append(line)
            prev_blank = is_blank
        
        return '\n'.join(result)
    
    def get_table_of_contents(self, document: Document) -> List[Dict[str, Any]]:
        """
        Generate table of contents from headers.
        
        Args:
            document: The document to analyze
            
        Returns:
            List of headers with their levels and positions
        """
        toc = []
        lines = document.content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.replace('#', '').strip()
                toc.append({
                    'level': level,
                    'title': title,
                    'line': line_num
                })
        
        return toc