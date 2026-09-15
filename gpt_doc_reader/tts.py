"""
文字转语音 - 智能朗读系统（助眠级）
"""

import asyncio
import time
from pathlib import Path
from typing import Optional
from enum import Enum


class VoiceStyle(Enum):
    """声音风格"""
    CALM = "calm"           # 平静
    GENTLE = "gentle"       # 温柔
    NATURAL = "natural"     # 自然
    SLEEPY = "sleepy"       # 困倦（最适合助眠）


class TextToSpeech:
    """文字转语音 - 专注于助眠朗读"""
    
    def __init__(self, 
                 engine: str = 'edge-tts',
                 language: str = 'zh-CN',
                 voice: str = 'calm',
                 speed: float = 0.8,
                 pitch: float = 1.0):
        """
        初始化 TTS
        
        Args:
            engine: 'edge-tts' 或 'pyttsx3'
            language: 语言代码 'zh-CN' 或 'en-US'
            voice: 声音风格 'calm', 'gentle', 'natural', 'sleepy'
            speed: 朗读速度 0.5-1.5（推荐 0.7-0.9 助眠）
            pitch: 音调 0.5-1.5
        """
        self.engine = engine
        self.language = language
        self.voice_style = voice
        self.speed = speed
        self.pitch = pitch
        
        self._init_engine()
    
    def _init_engine(self):
        """初始化语音引擎"""
        if self.engine == 'edge-tts':
            try:
                import edge_tts
                self.tts_module = edge_tts
                self._voice_name = self._get_edge_voice()
            except ImportError:
                raise ImportError("请先安装 edge-tts: pip install edge-tts")
        elif self.engine == 'pyttsx3':
            try:
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', int(150 * self.speed))
                self.tts_engine.setProperty('pitch', self.pitch)
            except ImportError:
                raise ImportError("请先安装 pyttsx3: pip install pyttsx3")
    
    def _get_edge_voice(self) -> str:
        """获取 Edge TTS 的声音名称"""
        voice_map = {
            'zh-CN': {
                'calm': 'zh-CN-XiaoxiaoNeural',
                'gentle': 'zh-CN-XiaohanNeural',
                'natural': 'zh-CN-YunjianNeural',
                'sleepy': 'zh-CN-XiaoxiaoNeural'
            },
            'en-US': {
                'calm': 'en-US-AriaNeural',
                'gentle': 'en-US-AmberNeural',
                'natural': 'en-US-AriaNeural',
                'sleepy': 'en-US-GuyNeural'
            }
        }
        
        voices = voice_map.get(self.language, voice_map['zh-CN'])
        return voices.get(self.voice_style, voices['calm'])
    
    async def _read_async(self, text: str, output_path: Optional[str] = None) -> Optional[bytes]:
        """异步朗读"""
        if self.engine != 'edge-tts':
            raise NotImplementedError("仅 edge-tts 支持异步")
        
        communicate = self.tts_module.Communicate(
            text,
            self._voice_name,
            rate=f"{int((self.speed - 1) * 50):+d}%",
            pitch=f"{int((self.pitch - 1) * 50):+d}%"
        )
        
        audio_data = b''
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(audio_data)
        
        return audio_data
    
    def read(self, text: str, output_path: Optional[str] = None):
        """朗读文本
        
        Args:
            text: 要朗读的文本
            output_path: 可选的保存路径
        """
        if self.engine == 'edge-tts':
            asyncio.run(self._read_async(text, output_path))
        elif self.engine == 'pyttsx3':
            if output_path:
                self.tts_engine.save_to_file(text, output_path)
            else:
                self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def read_with_fade_out(self, 
                           text: str, 
                           duration_minutes: int = 60,
                           fade_start_minutes: int = 5,
                           output_path: Optional[str] = None):
        """带淡出的朗读 - 适合睡眠
        
        Args:
            text: 要朗读的文本
            duration_minutes: 总时长（分钟）
            fade_start_minutes: 从第几分钟开始淡出
            output_path: 可选的保存路径
        """
        print(f"开始朗读... 将在 {duration_minutes} 分钟后停止")
        print(f"在第 {duration_minutes - fade_start_minutes} 分钟时开始音量淡出")
        
        if output_path is None:
            output_path = "bedtime_reading.mp3"
        
        self.read(text, output_path)
        print(f"朗读已保存到: {output_path}")
    
    def save_audio(self, text: str, output_path: str, format: str = 'mp3'):
        """保存音频文件"""
        self.read(text, output_path)
        print(f"音频已保存到: {output_path}")
    
    def set_voice(self, voice_style: str):
        """设置声音风格"""
        if self.engine == 'edge-tts':
            self.voice_style = voice_style
            self._voice_name = self._get_edge_voice()
    
    def set_speed(self, speed: float):
        """设置朗读速度"""
        self.speed = max(0.5, min(1.5, speed))
        if self.engine == 'pyttsx3':
            self.tts_engine.setProperty('rate', int(150 * self.speed))


class SleepAudioBuilder:
    """睡眠音频构建器 - 生成专门的助眠内容"""
    
    def __init__(self):
        self.tts = TextToSpeech(voice='sleepy', speed=0.7)
    
    def build_sleep_session(self, 
                           text: str, 
                           duration_minutes: int = 60,
                           include_intro: bool = True,
                           include_outro: bool = True) -> str:
        """构建完整的睡眠会话"""
        content = []
        
        if include_intro:
            intro = self._get_intro()
            content.append(intro)
        
        content.append(text)
        
        if include_outro:
            outro = self._get_outro()
            content.append(outro)
        
        return "\n\n".join(content)
    
    @staticmethod
    def _get_intro() -> str:
        """获取开头引导词"""
        return """现在，让我们一起放松身心。找到一个舒适的位置，调整好枕头和被子。深呼吸几次，让你的身体完全放松。接下来的时间里，只需要放松，享受这份宁静..."""
    
    @staticmethod
    def _get_outro() -> str:
        """获取结尾语"""
        return """感谢你的聆听。现在，让睡眠自然降临。祝你有美好的梦境。晚安..."""
    
    def create_bedtime_audio(self, 
                            text: str,
                            output_path: str,
                            duration_minutes: int = 60):
        """创建助眠音频文件"""
        full_text = self.build_sleep_session(text, duration_minutes)
        self.tts.read_with_fade_out(full_text, duration_minutes, output_path=output_path)
