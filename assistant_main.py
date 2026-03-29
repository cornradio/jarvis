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
import importlib # 用于热重载
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from actions import Actions
import config
from web_ui import DASHBOARD_HTML
import pystray
from PIL import Image, ImageDraw

import webbrowser

# --- 系统托盘系统 (V1.0) ---
def setup_tray():
    def create_image():
        # 生成一个深蓝色带光泽的圆圈作为图标
        width = 64; height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse([8, 8, 56, 56], fill=(0, 150, 255)) # 贾维斯蓝
        dc.ellipse([16, 16, 48, 48], outline=(255, 255, 255), width=2)
        return image

    def on_quit(icon, item):
        icon.stop()
        os._exit(0) # 强制关闭所有关联线程并退出

    def on_reload(icon, item):
        # 模拟点击重载
        with app.test_client() as c:
            c.post('/reload')
            
    def on_open_web(icon, item):
        # 自动获取本机 IP 或直接访问 localhost
        webbrowser.open(f"http://127.0.0.1:{config.API_PORT}")

    icon = pystray.Icon("JARVIS", create_image(), menu=pystray.Menu(
        pystray.MenuItem("🖥️ 仪表盘 (Dashboard)", on_open_web),
        pystray.MenuItem("🔄 重载配置", on_reload),
        pystray.MenuItem("❌ 退出 JARVIS", on_quit)
    ))
    icon.run()

# 启动托盘线程
threading.Thread(target=setup_tray, daemon=True).start()

app = Flask(__name__)
CORS(app)
actions_worker = Actions()

# --- TTS 播报器 (V7.2) ---
class Speaker:
    def __init__(self):
        self.msg_queue = queue.Queue()
        pygame.mixer.init()
        threading.Thread(target=self._speech_worker, daemon=True).start()

    def _speech_worker(self):
        while True:
            text = self.msg_queue.get()
            if not text or not config.VOICE_ENABLED:
                self.msg_queue.task_done(); continue
            
            # 说话前音量检查
            try:
                cv = actions_worker.vm.get_volume()
                low = False
                if cv < 15: low = True; actions_worker.vm.set_volume(30)
            except: pass

            try:
                if config.VOICE_ENGINE == "edge":
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    temp_file = f"voice_{int(time.time())}.mp3"
                    communicate = edge_tts.Communicate(text, config.EDGE_VOICE, rate=config.EDGE_RATE)
                    loop.run_until_complete(communicate.save(temp_file))
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy(): time.sleep(0.05)
                    pygame.mixer.music.unload()
                    if os.path.exists(temp_file): os.remove(temp_file)
                    loop.close()
                else:
                    pythoncom.CoInitialize()
                    le = pyttsx3.init()
                    le.setProperty('rate', config.LOCAL_RATE)
                    vs = le.getProperty('voices')
                    for v in vs:
                        if "zh" in v.id.lower() or "chinese" in v.name.lower():
                            le.setProperty('voice', v.id); break
                    le.say(text)
                    le.runAndWait()
                    del le
                    pythoncom.CoUninitialize()
            except Exception as e: print(f"Speech Error: {e}")
            
            if low: 
                try: actions_worker.vm.set_volume(cv)
                except: pass
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
    return render_template_string(DASHBOARD_HTML, commands=config.COMMANDS, 
                                 port=config.API_PORT, local_ip=ip,
                                 voice_on=config.VOICE_ENABLED, engine_name=config.VOICE_ENGINE)

# --- 新增：热重载接口 ---
@app.route('/reload', methods=['POST'])
def reload_config():
    global config, actions_worker
    try:
        # 重载配置
        importlib.reload(config)
        # 重载动作模块
        import actions
        importlib.reload(actions)
        from actions import Actions
        actions_worker = Actions() # 更新实例
        
        speaker.speak("核心逻辑与配置已成功重载")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    text = data.get("text", "")
    if not text: return jsonify({"status": "error"}), 400
    
    # 异步执行动作和语音
    threading.Thread(target=execution_task, args=(text,)).start()
    return jsonify({"status": "success"})

def execution_task(text):
    # 配置切换逻辑
    if text == "切换语音":
        config.VOICE_ENABLED = not config.VOICE_ENABLED
        speaker.speak("语音开启" if config.VOICE_ENABLED else "静音模式")
        return
    if text == "切换引擎":
        config.VOICE_ENGINE = "edge" if config.VOICE_ENGINE == "local" else "local"
        speaker.speak("引擎切换成功")
        return

    # 指令匹配
    for cmd_id, info in config.COMMANDS.items():
        if any(kw == text for kw in info['post_params']):
            # 先说话再执行
            speaker.speak(info['reply'])
            
            func = getattr(actions_worker, info['action'], None)
            if func:
                try: func(*info['params'])
                except Exception as e: print(f"Action Exec Error: {e}")
            return

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.API_PORT)
