"""
Utility functions for GPT Doc Reader.
"""

import re
from typing import List, Dict
from datetime import datetime


def extract_metadata(content: str) -> Dict[str, str]:
    """
    Extract metadata from document content (e.g., title, author, date).
    
    Args:
        content: Document content
        
    Returns:
        Dictionary with extracted metadata
    """
    metadata = {}
    
    # Extract title (first line starting with #)
    title_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    # Extract date patterns
    date_pattern = r'\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}'
    date_matches = re.findall(date_pattern, content)
    if date_matches:
        metadata['dates_found'] = date_matches
    
    return metadata


def split_into_paragraphs(content: str) -> List[str]:
    """Split document content into paragraphs."""
    paragraphs = content.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


def count_words(content: str) -> int:
    """Count words in document content."""
    return len(content.split())


def count_sentences(content: str) -> int:
    """Count sentences in document content."""
    sentences = re.split(r'[.!?]+', content)
    return len([s for s in sentences if s.strip()])


def get_statistics(content: str) -> Dict[str, int]:
    """Get various statistics about document content."""
    return {
        'characters': len(content),
        'words': count_words(content),
        'sentences': count_sentences(content),
        'lines': len(content.split('\n')),
        'paragraphs': len(split_into_paragraphs(content)),
    }


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Replace invalid characters with underscores
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        name = name[:250]
        sanitized = f"{name}.{ext}" if ext else name
    
    return sanitized


def highlight_keywords(content: str, keywords: List[str]) -> str:
    """
    Highlight keywords in content.
    
    Args:
        content: Document content
        keywords: List of keywords to highlight
        
    Returns:
        Content with highlighted keywords
    """
    highlighted = content
    
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted = pattern.sub(f"**{keyword}**", highlighted)
    
    return highlighted


def generate_timestamp() -> str:
    """Generate current timestamp."""
    return datetime.now().isoformat()