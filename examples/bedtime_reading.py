"""
使用示例 - 完整演示
"""

from gpt_doc_reader import DocumentReader, TextToSpeech, SleepAudioBuilder


def example_read_pdf_and_narrate():
    """示例 1：读取 PDF 并朗读"""
    
    print("=" * 60)
    print("示例 1：读取 PDF 并朗读")
    print("=" * 60)
    
    reader = DocumentReader()
    
    example_text = """
    # Python 学习指南
    
    ## 第一章：Python 基础
    Python 是一门高级编程语言，具有简单易学的特点。
    它的语法接近自然语言，使得初学者可以快速上手。
    
    ## 第二章：数据结构
    Python 提供了多种内置数据结构，包括列表、元组、字典等。
    这些数据结构可以帮助我们高效地组织和管理数据。
    """
    
    doc = reader.load_from_text(example_text, "python_guide.txt")
    print(f"已加载: {doc}")
    print(f"内容长度: {len(doc.get_text())} 字符\n")
    
    text = doc.get_text()
    summary = doc.get_summary(length='short')
    print("摘要:")
    print(summary)
    print()


def example_bedtime_narration():
    """示例 2：睡前朗读"""
    
    print("\n" + "=" * 60)
    print("示例 2：睡前朗读（助眠模式）")
    print("=" * 60)
    
    sleep_text = """
    在一个月明星稀的夜晚，有一座古老的图书馆。
    这座图书馆收藏了世界上最珍贵的书籍。
    书架之间的走廊幽深而宁静，只有时钟的滴答声。
    
    一个年轻的学者推开了图书馆的门。
    他的脚步声在空荡荡的大厅里回响。
    窗外的月光洒进来，在地板上投下长长的影子。
    """
    
    builder = SleepAudioBuilder()
    full_text = builder.build_sleep_session(
        sleep_text, 
        duration_minutes=60,
        include_intro=True,
        include_outro=True
    )
    
    print("已准备睡前朗读内容")
    print(f"总字数: {len(full_text)} 字符")


def example_process_multiple_formats():
    """示例 3：处理多种格式"""
    
    print("\n" + "=" * 60)
    print("示例 3：支持的文件格式")
    print("=" * 60)
    
    supported_formats = [
        ('document.pdf', 'PDF 文档'),
        ('notes.docx', 'Word 文档'),
        ('article.md', 'Markdown 文件'),
        ('screenshot.png', '截图（OCR）'),
        ('content.txt', '纯文本'),
    ]
    
    print("支持的文件格式:")
    for filename, description in supported_formats:
        print(f"  • {filename:20} - {description}")


def example_document_operations():
    """示例 4：文档操作"""
    
    print("\n" + "=" * 60)
    print("示例 4：文档操作")
    print("=" * 60)
    
    reader = DocumentReader()
    
    doc_text = """
    # 机器学习基础
    
    ## 什么是机器学习？
    机器学习是人工智能的一个分支。
    
    ## 监督学习
    - 决策树
    - 神经网络
    - 支持向量机
    """
    
    doc = reader.load_from_text(doc_text, "ml_basics.md")
    
    print("文档操作示例:\n")
    
    print("1. 获取纯文本:")
    print(f"   长度: {len(doc.get_text())} 字符\n")
    
    print("2. 获取文档结构:")
    structure = doc.get_structure()
    print(f"   章节数: {len(structure['chapters'])}")
    print(f"   小节数: {len(structure['sections'])}\n")
    
    print("3. 提取要点:")
    highlights = doc.get_highlights()
    for h in highlights[:3]:
        print(f"   • {h}")
    print()


if __name__ == "__main__":
    example_read_pdf_and_narrate()
    example_bedtime_narration()
    example_process_multiple_formats()
    example_document_operations()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)
