import sys
import threading
import queue
import pyttsx3
import pythoncom
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from actions import Actions
import config

app = Flask(__name__)
CORS(app)
actions_worker = Actions()

# --- 稳定的 TTS 播报器 ---
class Speaker:
    def __init__(self):
        self.msg_queue = queue.Queue()
        threading.Thread(target=self._speech_worker, daemon=True).start()

    def _speech_worker(self):
        while True:
            text = self.msg_queue.get()
            if text:
                try:
                    pythoncom.CoInitialize()
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if "chinese" in voice.name.lower() or "zh" in voice.id.lower() or "huihui" in voice.name.lower():
                            engine.setProperty('voice', voice.id)
                            break
                    engine.setProperty('rate', config.VOICE_RATE)
                    engine.setProperty('volume', config.VOICE_VOLUME)
                    engine.say(text)
                    engine.runAndWait()
                    del engine
                    pythoncom.CoUninitialize()
                except Exception as e: print(f"Speech Loop Error: {e}")
            self.msg_queue.task_done()

    def speak(self, text):
        self.msg_queue.put(text)

speaker = Speaker()

# --- 动态网页生成逻辑 ---
def get_dashboard():
    cards_html = ""
    for cmd_id, item in config.COMMANDS.items():
        # 这里取 post_params 的第一个作为按钮默认发送的参数
        trigger_val = item['post_params'][0]
        cards_html += f"""
        <div class="card" onclick="send('{trigger_val}')">
            <div class="label">{item['label'].upper()}</div>
            <div class="hint">POST: {trigger_val}</div>
        </div>
        """
    
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JARVIS COMMANDER</title>
    <style>
        :root {{ --p: #00ecff; --bg: #050505; --c: rgba(255,255,255,0.05); }}
        * {{ touch-action: manipulation; -webkit-user-select: none; box-sizing: border-box; }}
        body {{ 
            background: var(--bg); color: #fff; font-family: 'Inter', sans-serif;
            display: flex; flex-direction: column; align-items: center; padding: 20px 10px; margin:0;
        }}
        h1 {{ font-size: 1.2rem; letter-spacing: 5px; margin: 20px 0; color: var(--p); }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; max-width: 600px; }}
        .card {{ 
            background: var(--c); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px 10px; 
            text-align: center; cursor: pointer; transition: 0.1s;
        }}
        .card:active {{ background: var(--p); color: #000; transform: scale(0.95); }}
        .label {{ font-size: 0.85rem; font-weight: 800; }}
        .hint {{ font-size: 0.6rem; opacity: 0.2; margin-top: 5px; }}
        
        # 【加回的 API 提示信息】
        .api-info {{
            margin-top: 30px; padding: 15px; background: #000; border-top: 1px solid #333;
            font-size: 0.7rem; color: #888; width: 100%; max-width: 500px; border-radius: 10px; line-height: 1.6;
        }}
        code {{ color: var(--p); }}
    </style>
</head>
<body>
    <h1>JARVIS CORE</h1>
    <div class="grid">{cards_html}</div>
    
    <div class="api-info">
        <b>📱 手机/远程调用指南:</b><br>
        1. 接口: <code>POST /command</code><br>
        2. 正文 (JSON): <code>{{"text": "指令参数"}}</code><br>
        3. 示例: 发送 <code>{{"text": "锁屏"}}</code> 即可让电脑锁定。
    </div>

    <script>
        function send(t) {{
            fetch('/command', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ text: t }}) }});
        }}
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(get_dashboard())

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    text = data.get("text", "")
    if not text: return jsonify({"status": "error"}), 400
    
    matched = False
    for cmd_id, info in config.COMMANDS.items():
        # 匹配配置中的 post_params
        if any(kw == text for kw in info['post_params']) or any(kw in text for kw in info['post_params']):
            func = getattr(actions_worker, info['action'], None)
            if func:
                func(*info['params'])
                speaker.speak(info['reply'])
                matched = True
            break
            
    if not matched: print(f"未匹配指令: {text}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
