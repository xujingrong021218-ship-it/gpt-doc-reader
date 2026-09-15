"""
Document storage and management.
"""

import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .reader import Document


class DocumentStorage:
    """Manages document storage and retrieval."""
    
    def __init__(self, storage_path: str = "./documents"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_document(self, document: Document, output_format: str = "txt") -> str:
        """
        Save a document to storage.
        
        Args:
            document: Document to save
            output_format: File format extension
            
        Returns:
            Path to saved file
        """
        filename = document.filename or "document"
        if not filename.endswith(f".{output_format}"):
            filename = f"{filename}.{output_format}"
        
        file_path = self.storage_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(document.content)
        
        return str(file_path)
    
    def load_document(self, filename: str) -> Optional[Document]:
        """Load a document from storage."""
        file_path = self.storage_path / filename
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Document(content=content, filename=filename)
    
    def list_documents(self) -> List[dict]:
        """List all documents in storage."""
        documents = []
        
        for file_path in self.storage_path.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                documents.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        
        return sorted(documents, key=lambda x: x["modified"], reverse=True)
    
    def delete_document(self, filename: str) -> bool:
        """Delete a document from storage."""
        file_path = self.storage_path / filename
        
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
        
        return False
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics."""
        total_size = 0
        file_count = 0
        
        for file_path in self.storage_path.glob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "storage_path": str(self.storage_path),
            "file_count": file_count,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }