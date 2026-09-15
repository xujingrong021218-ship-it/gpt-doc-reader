"""
图片/OCR 加载器
"""


class ImageLoader:
    """图片文件加载器（OCR）"""
    
    def load(self, file_path: str) -> str:
        """通过 OCR 加载图片中的文字"""
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            raise ImportError("请安装: pip install pytesseract pillow")
        
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        return text if text.strip() else f"[无法从 {file_path} 识别文字]"
