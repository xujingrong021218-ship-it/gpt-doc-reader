# GPT Doc Reader

一个强大的文档阅读和智能朗读系统，专门用来处理 ChatGPT 生成的各种格式文档。

**核心特性：**
- 📄 支持多格式文档：PDF、Word、Markdown、纯文本、截图
- 🔍 智能内容提取和结构化
- 🎙️ AI 朗读功能（助眠级温柔语音）
- 📝 自动生成笔记和摘要
- 🔎 快速搜索和章节导航
- 💾 本地存储和管理

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/xujingrong021218-ship-it/gpt-doc-reader.git
cd gpt-doc-reader

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```python
from gpt_doc_reader import DocumentReader, TextToSpeech

# 初始化读取器
reader = DocumentReader()

# 加载各种格式的文档
doc_pdf = reader.load('document.pdf')
doc_word = reader.load('document.docx')
doc_img = reader.load('screenshot.png')  # OCR 识别

# 获取提取的文本
text = doc_pdf.get_text()

# 智能朗读（助眠模式）
tts = TextToSpeech(speed=0.8, voice='calm')  # 缓慢平静的声音
tts.read(text)

# 保存为音频文件
tts.save_audio('output.mp3')
```

## 功能详解

### 1. 多格式文档支持

```python
reader = DocumentReader()

# PDF 文档
pdf_doc = reader.load('chatgpt_output.pdf')

# Word 文档
word_doc = reader.load('notes.docx')

# Markdown 文件
md_doc = reader.load('summary.md')

# 截图/图片（自动 OCR）
img_doc = reader.load('screenshot.png')

# 纯文本
txt_doc = reader.load('document.txt')
```

### 2. 智能朗读

```python
from gpt_doc_reader import TextToSpeech

tts = TextToSpeech(
    speed=0.8,           # 朗读速度（0.5-1.5）
    voice='calm',        # 声音风格：calm, gentle, natural, sleepy
    language='zh-CN'     # 语言
)

# 直接朗读
tts.read(text)

# 保存为音频
tts.save_audio('document.mp3', format='mp3')

# 设置睡眠计时器
tts.read_with_fade_out(text, duration_minutes=60)  # 60分钟后逐渐淡出
```

### 3. 内容提取和结构化

```python
# 自动提取结构
structure = doc.get_structure()  # 章节、段落、列表等

# 获取摘要
summary = doc.get_summary(length='short')  # short, medium, long

# 提取要点
highlights = doc.get_highlights()

# 生成目录
toc = doc.get_table_of_contents()
```

## 项目结构

```
gpt-doc-reader/
├── gpt_doc_reader/
│   ├── __init__.py
│   ├── reader.py              # 核心文档读取器
│   ├── tts.py                 # 文字转语音 (TTS)
│   ├── loaders/
│   │   ├── pdf_loader.py      # PDF 加载
│   │   ├── word_loader.py     # Word 加载
│   │   ├── image_loader.py    # 图片/OCR 加载
│   │   ├── markdown_loader.py # Markdown 加载
│   │   └── text_loader.py     # 纯文本加载
│   └── processors/
│       ├── text_extractor.py  # 文本提取
│       ├── structure_analyzer.py  # 结构分析
│       └── summarizer.py      # 摘要生成
├── examples/
│   └── bedtime_reading.py     # 完整示例
├── requirements.txt
├── .env.example
└── README.md
```

## 核心依赖

- **PDF**: pdfplumber, PyPDF2
- **Word**: python-docx
- **OCR**: pytesseract, Pillow
- **TTS**: edge-tts, pyttsx3
- **其他**: numpy, pandas, python-dotenv

## 配置文件

创建 `.env` 文件（基于 `.env.example`）：

```env
# 文档存储路径
DOCS_PATH=./documents
OUTPUT_PATH=./output

# TTS 配置
TTS_ENGINE=edge-tts
TTS_VOICE=zh-CN-XiaoxiaoNeural
TTS_SPEED=0.8
TTS_PITCH=1.0

# 助眠模式配置
SLEEP_MODE_SPEED=0.7
SLEEP_MODE_VOICE=sleepy
SLEEP_DURATION_MINUTES=60

# OCR 配置
OCR_LANGUAGE=chi_sim+eng
```

## 使用场景

### 场景 1：睡前听朗读（助眠）

```python
from gpt_doc_reader import DocumentReader, TextToSpeech, SleepAudioBuilder

# 加载今天的学习笔记
reader = DocumentReader()
doc = reader.load('today_notes.pdf')

# 温柔朗读，60分钟后自动停止
builder = SleepAudioBuilder()
builder.create_bedtime_audio(doc.get_text(), 'bedtime.mp3', duration_minutes=60)
```

### 场景 2：快速阅读 ChatGPT 输出

```python
# 支持所有格式的文档
reader = DocumentReader()

# 无论是 PDF、Word、截图还是 Markdown
doc = reader.load('chatgpt_output.pdf')

# 快速获取摘要
print(doc.get_summary())

# 搜索关键信息
results = doc.search('重要概念')
```

### 场景 3：批量处理和导出

```python
# 加载文档
doc = reader.load('document.docx')

# 转换格式
markdown = doc.export('markdown')

# 生成朗读音频
tts = TextToSpeech(voice='calm', speed=0.8)
tts.save_audio(doc.get_text(), 'output.mp3')
```

## API 文档

### DocumentReader

- `load(path)` - 加载任意格式文档
- `load_from_text(text, filename)` - 从文本加载
- `get_document(filename)` - 获取已加载文档
- `list_documents()` - 列出所有文档

### Document

- `get_text()` - 获取纯文本
- `get_structure()` - 获取文档结构
- `get_summary(length)` - 生成摘要
- `get_highlights()` - 提取要点
- `search(keyword)` - 搜索内容
- `export(format)` - 导出格式

### TextToSpeech

- `read(text)` - 朗读文本
- `read_with_fade_out(text, duration)` - 带淡出的朗读
- `save_audio(text, output_path)` - 保存音频
- `set_voice(style)` - 设置声音
- `set_speed(speed)` - 设置速度

### SleepAudioBuilder

- `build_sleep_session(text, duration)` - 构建睡眠会话
- `create_bedtime_audio(text, output_path)` - 创建助眠音频

## 支持的文件格式

| 格式 | 说明 | 依赖库 |
|------|------|--------|
| .pdf | PDF 文档 | pdfplumber |
| .docx | Word 文档 | python-docx |
| .doc | Word 97-2003 | python-docx |
| .md | Markdown | 内置 |
| .txt | 纯文本 | 内置 |
| .png/.jpg/.jpeg | 图片（OCR）| pytesseract |

## 示例运行

```bash
# 运行完整示例
python examples/bedtime_reading.py
```

## 常见问题

**Q: 如何安装 Tesseract OCR？**

A: 根据你的操作系统：
- Ubuntu: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: 下载安装程序 https://github.com/UB-Mannheim/tesseract/wiki

**Q: TTS 支持哪些语言？**

A: 支持 edge-tts 支持的所有语言，包括中文、英文、日文等。

**Q: 能否离线使用？**

A: 使用 pyttsx3 引擎可以离线使用，但质量不如 edge-tts。

## 许可证

MIT License

---

**更新日期**: 2026-09-15  
**版本**: 1.0.0  
**作者**: xujingrong021218
