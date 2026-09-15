"""
主包初始化
"""

from .reader import DocumentReader, Document
from .tts import TextToSpeech, SleepAudioBuilder

__version__ = "1.0.0"
__author__ = "xujingrong021218"

__all__ = [
    "DocumentReader",
    "Document",
    "TextToSpeech",
    "SleepAudioBuilder",
]
