import os
import sys
import json
import pyaudio
import pyttsx3
import winsound
import time
from vosk import Model, KaldiRecognizer

class VoiceEngine:
    def __init__(self, model_path="model"):
        if not os.path.exists(model_path):
            sys.exit(1)
        
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        
        self.tts = pyttsx3.init()
        # 寻找中文语音包
        for voice in self.tts.getProperty('voices'):
            if "chinese" in voice.name.lower() or "zh" in voice.id.lower() or "huihui" in voice.name.lower():
                self.tts.setProperty('voice', voice.id)
                break
        
        self.tts.setProperty('rate', 170)
        self.tts.setProperty('volume', 1.0)

    def play_ding(self, count=1):
        for _ in range(count):
            winsound.Beep(900, 150)
            if count > 1: time.sleep(0.1)

    def speak(self, text):
        print(f"Assistant: {text}")
        try:
            old_active = self.stream.is_active()
            if old_active: self.stream.stop_stream()
            self.tts.say(text)
            self.tts.runAndWait()
            if old_active: self.stream.start_stream()
        except:
            try: self.stream.start_stream()
            except: pass

    def listen(self, interrupt_callback=None):
        """增强的监听：如果 interrupt_callback 返回 True，则立刻中断监听"""
        while True:
            # 这里的 time.sleep 防止播报时的 CPU 占用
            if not self.stream.is_active():
                time.sleep(0.1)
                continue
                
            # 检查是否有快捷键中断
            if interrupt_callback and interrupt_callback():
                print("DEBUG: 监听到中断信号")
                return "__INTERRUPT__"

            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                continue
                
            if self.recognizer.AcceptWaveform(data):
                res = json.loads(self.recognizer.Result())
                text = res.get('text', '').replace(' ', '')
                if text:
                    return text
            else:
                # 即使没完成一句，也可以检查一下快捷键
                if interrupt_callback and interrupt_callback():
                    return "__INTERRUPT__"
        return ""
