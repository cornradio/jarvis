import sys
import threading
import queue
import time
import os
import asyncio
import socket
import edge_tts
import pygame
import pyttsx3
import pythoncom
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from actions import Actions
import config
from web_ui import DASHBOARD_HTML

app = Flask(__name__)
CORS(app)
actions_worker = Actions()

# --- 极速/真人双模 TTS 引擎 ---
class Speaker:
    def __init__(self):
        self.msg_queue = queue.Queue()
        pygame.mixer.init()
        threading.Thread(target=self._speech_worker, daemon=True).start()

    def _speech_worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            text = self.msg_queue.get()
            if not text: 
                self.msg_queue.task_done()
                continue
                
            if not config.VOICE_ENABLED:
                self.msg_queue.task_done()
                continue

            try:
                if config.VOICE_ENGINE == "edge":
                    # --- 真人云端引擎 ---
                    temp_file = "temp_voice.mp3"
                    communicate = edge_tts.Communicate(text, config.EDGE_VOICE, rate=config.EDGE_RATE)
                    loop.run_until_complete(communicate.save(temp_file))
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy(): time.sleep(0.05)
                    pygame.mixer.music.unload()
                    if os.path.exists(temp_file): os.remove(temp_file)
                else:
                    # --- 极速本地引擎 ---
                    pythoncom.CoInitialize()
                    engine = pyttsx3.init()
                    engine.setProperty('rate', config.LOCAL_RATE)
                    # 寻找中文语音
                    voices = engine.getProperty('voices')
                    for v in voices:
                        if "zh" in v.id.lower() or "chinese" in v.name.lower():
                            engine.setProperty('voice', v.id); break
                    engine.say(text)
                    engine.runAndWait()
                    pythoncom.CoUninitialize()
            except Exception as e: print(f"Speaker Error: {e}")
            self.msg_queue.task_done()

    def speak(self, text):
        self.msg_queue.put(text)

speaker = Speaker()

@app.route('/')
def index():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try: s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]
    except: ip = '127.0.0.1'
    finally: s.close()
    
    # 传入当前的语音配置，让 UI 能显示状态
    return render_template_string(DASHBOARD_HTML, 
                                 commands=config.COMMANDS, 
                                 port=config.API_PORT, 
                                 local_ip=ip,
                                 voice_on=config.VOICE_ENABLED,
                                 engine_name=config.VOICE_ENGINE)

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    text = data.get("text", "")
    if not text: return jsonify({"status": "error"}), 400
    
    # --- 内部特殊逻辑：切换设置 ---
    if text == "切换语音":
        config.VOICE_ENABLED = not config.VOICE_ENABLED
        speaker.speak("静音开启" if not config.VOICE_ENABLED else "语音开启")
        return jsonify({"status": "success", "voice_on": config.VOICE_ENABLED})
    
    if text == "切换引擎":
        config.VOICE_ENGINE = "edge" if config.VOICE_ENGINE == "local" else "local"
        speaker.speak(f"已切换到{'云端' if config.VOICE_ENGINE == 'edge' else '本地'}引擎")
        return jsonify({"status": "success", "engine": config.VOICE_ENGINE})

    # --- 常规指令分发 ---
    matched = False
    for cmd_id, info in config.COMMANDS.items():
        if any(kw == text for kw in info['post_params']):
            func = getattr(actions_worker, info['action'], None)
            if func: func(*info['params'])
            speaker.speak(info['reply'])
            matched = True
            break
            
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.API_PORT)
