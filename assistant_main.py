import sys
import threading
import queue
import time
import os
import asyncio
import socket
import edge_tts
import pygame
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from actions import Actions
import config
from web_ui import DASHBOARD_HTML  # 导入外部 UI 模板

app = Flask(__name__)
CORS(app)
actions_worker = Actions()

# --- 稳定的 TTS 播报器 (Edge-TTS) ---
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
            if text:
                try:
                    temp_file = "temp_voice.mp3"
                    communicate = edge_tts.Communicate(text, config.VOICE_NAME)
                    loop.run_until_complete(communicate.save(temp_file))
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy(): time.sleep(0.1)
                    pygame.mixer.music.unload()
                    if os.path.exists(temp_file): os.remove(temp_file)
                except Exception as e: print(f"Speech Error: {e}")
            self.msg_queue.put(None) if text is None else None # 哨兵处理
            self.msg_queue.task_done()

    def speak(self, text):
        self.msg_queue.put(text)

speaker = Speaker()

@app.route('/')
def index():
    # 获取本地 IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try: s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]
    except: ip = '您的电脑IP'
    finally: s.close()
    
    return render_template_string(DASHBOARD_HTML, 
                                 commands=config.COMMANDS, 
                                 port=config.API_PORT, 
                                 local_ip=ip)

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    text = data.get("text", "")
    if not text: return jsonify({"status": "error"}), 400
    matched = False
    for cmd_id, info in config.COMMANDS.items():
        if any(kw == text for kw in info['post_params']):
            func = getattr(actions_worker, info['action'], None)
            if func:
                func(*info['params'])
                speaker.speak(info['reply'])
                matched = True
            break
    if not matched: print(f"未匹配: {text}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.API_PORT)
