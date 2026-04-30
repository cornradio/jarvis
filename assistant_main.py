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
import importlib  # 用于热重载
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from actions import Actions
import config
from core.web_ui import DASHBOARD_HTML, OLD_DASHBOARD_HTML, SETTINGS_HTML
import pystray
from PIL import Image, ImageDraw

import webbrowser


# --- 系统托盘系统 (V1.0) ---
def setup_tray():
    def create_image():
        # 生成一个深蓝色带光泽的圆圈作为图标
        width = 64
        height = 64
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse([8, 8, 56, 56], fill=(0, 150, 255))  # 贾维斯蓝
        dc.ellipse([16, 16, 48, 48], outline=(255, 255, 255), width=2)
        return image

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)  # 强制关闭所有关联线程并退出

    def on_open_web(icon, item):
        # 自动获取本机 IP 或直接访问 localhost
        webbrowser.open(f"http://127.0.0.1:{config.API_PORT}")

    def on_open_folder(icon, item):
        # 打开项目根目录
        os.startfile(os.path.dirname(os.path.abspath(__file__)))

    icon = pystray.Icon(
        "JARVIS",
        create_image(),
        menu=pystray.Menu(
            pystray.MenuItem("🖥️ 仪表盘", on_open_web),
            pystray.MenuItem("📁 项目文件夹", on_open_folder),
            pystray.MenuItem("❌ 退出", on_quit),
        ),
    )
    icon.run()


# 启动托盘线程
threading.Thread(target=setup_tray, daemon=True).start()

app = Flask(__name__, static_folder="core/static")
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
                self.msg_queue.task_done()
                continue

            # 说话前音量检查
            try:
                cv = actions_worker.vm.get_volume()
                low = False
                if cv < 15:
                    low = True
                    actions_worker.vm.set_volume(30)
            except:
                pass

            try:
                if config.VOICE_ENGINE == "edge":
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    temp_file = f"voice_{int(time.time())}.mp3"
                    communicate = edge_tts.Communicate(
                        text, config.EDGE_VOICE, rate=config.EDGE_RATE
                    )
                    loop.run_until_complete(communicate.save(temp_file))
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.05)
                    pygame.mixer.music.unload()
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    loop.close()
                else:
                    pythoncom.CoInitialize()
                    le = pyttsx3.init()
                    le.setProperty("rate", config.LOCAL_RATE)
                    vs = le.getProperty("voices")
                    for v in vs:
                        if "zh" in v.id.lower() or "chinese" in v.name.lower():
                            le.setProperty("voice", v.id)
                            break
                    le.say(text)
                    le.runAndWait()
                    del le
                    pythoncom.CoUninitialize()
            except Exception as e:
                print(f"Speech Error: {e}")

            if low:
                try:
                    actions_worker.vm.set_volume(cv)
                except:
                    pass
            self.msg_queue.task_done()

    def speak(self, text):
        self.msg_queue.put(text)


speaker = Speaker()


@app.route("/")
def index():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return render_template_string(
        OLD_DASHBOARD_HTML,
        commands=config.COMMANDS,
        port=config.API_PORT,
        local_ip=ip,
        voice_on=config.VOICE_ENABLED,
        engine_name=config.VOICE_ENGINE,
    )

@app.route("/new")
def new_index():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return render_template_string(
        DASHBOARD_HTML,
        commands=config.COMMANDS,
        port=config.API_PORT,
        local_ip=ip,
        voice_on=config.VOICE_ENABLED,
        engine_name=config.VOICE_ENGINE,
    )

@app.route("/old")
def old_index():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return render_template_string(
        OLD_DASHBOARD_HTML,
        commands=config.COMMANDS,
        port=config.API_PORT,
        local_ip=ip,
        voice_on=config.VOICE_ENABLED,
        engine_name=config.VOICE_ENGINE,
    )


@app.route("/settings")
def settings():
    return render_template_string(SETTINGS_HTML, config=config, commands=config.COMMANDS)


@app.route("/settings/save", methods=["POST"])
def save_settings():
    data = request.json
    try:
        config.API_PORT = data.get("API_PORT", config.API_PORT)
        config.VOICE_ENABLED = data.get("VOICE_ENABLED", config.VOICE_ENABLED)
        config.VOICE_ENGINE = data.get("VOICE_ENGINE", config.VOICE_ENGINE)
        config.LOCAL_RATE = data.get("LOCAL_RATE", config.LOCAL_RATE)
        config.EDGE_VOICE = data.get("EDGE_VOICE", config.EDGE_VOICE)
        config.EDGE_RATE = data.get("EDGE_RATE", config.EDGE_RATE)
        new_commands = data.get("commands", {})
        if new_commands:
            config.COMMANDS = new_commands
        import ast
        config_content = """# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# --- 【系统配置】 ---
API_PORT = {API_PORT}

# --- 【语音反馈配置】 ---
VOICE_ENABLED = {VOICE_ENABLED}
VOICE_ENGINE = "{VOICE_ENGINE}"
LOCAL_RATE = {LOCAL_RATE}
EDGE_VOICE = "{EDGE_VOICE}"
EDGE_RATE = "{EDGE_RATE}"

# --- 【指令注册表】 ---
# label: 网页名 | post_params: 接口参数 | action: 函数名 | params: 参数列表 | reply: 回复 | emoji: 图标emoji | icon: 自定义图标URL
COMMANDS = {COMMANDS}
""".format(
            API_PORT=config.API_PORT,
            VOICE_ENABLED=config.VOICE_ENABLED,
            VOICE_ENGINE=config.VOICE_ENGINE,
            LOCAL_RATE=config.LOCAL_RATE,
            EDGE_VOICE=config.EDGE_VOICE,
            EDGE_RATE=config.EDGE_RATE,
            COMMANDS=ast.literal_eval(repr(config.COMMANDS))
        )
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


# --- 新增：热重载接口 ---
@app.route("/reload", methods=["POST"])
def reload_config():
    global config, actions_worker
    try:
        # 重载配置
        importlib.reload(config)
        # 重载动作模块
        import actions

        importlib.reload(actions)
        from actions import Actions

        actions_worker = Actions()  # 更新实例

        speaker.speak("核心逻辑与配置已成功重载")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"status": "error"}), 400

    # 动态查找指令，如果指令是截图这种需要返回文件的，同步处理
    for cmd_id, info in config.COMMANDS.items():
        if any(kw == text for kw in info.get("post_params", [])):
            if info.get("action") == "take_screenshot":
                speaker.speak(info.get("reply", "截图"))
                img_path = actions_worker.take_screenshot()
                if img_path and os.path.exists(img_path):
                    filename = os.path.basename(img_path)
                    response = send_file(
                        img_path, as_attachment=True, download_name=filename
                    )
                    response.headers["X-File-Name"] = filename
                    return response
                else:
                    return jsonify({"status": "error", "msg": "Screenshot failed"}), 500

            if info.get("action") == "take_photo":
                speaker.speak(info.get("reply", "拍照"))
                photo_path = actions_worker.take_photo()
                if photo_path and os.path.exists(photo_path):
                    filename = os.path.basename(photo_path)
                    response = send_file(
                        photo_path, as_attachment=True, download_name=filename
                    )
                    response.headers["X-File-Name"] = filename
                    return response
                else:
                    return jsonify({"status": "error", "msg": "Camera capture failed"}), 500

            if info.get("action") == "get_clipboard":
                speaker.speak(info.get("reply", "获取内容"))
                res = actions_worker.get_clipboard()
                if res and res.get("path") and os.path.exists(res["path"]):
                    filename = os.path.basename(res["path"])
                    # 关键：手动构造响应并暴露文件名 Header
                    response = send_file(
                        res["path"], as_attachment=True, download_name=filename
                    )
                    response.headers["X-File-Name"] = filename.encode("utf-8").decode(
                        "latin-1"
                    )  # 处理中文名
                    return response
                else:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "msg": "Clipboard is empty or inaccessible",
                            }
                        ),
                        404,
                    )

    # 其余指令：异步执行
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
        if any(kw == text for kw in info["post_params"]):
            # 先说话再执行
            speaker.speak(info["reply"])

            func = getattr(actions_worker, info["action"], None)
            if func:
                try:
                    func(*info["params"])
                except Exception as e:
                    print(f"Action Exec Error: {e}")
            return


if __name__ == "__main__":
    import socket
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0

    if not is_port_available(config.API_PORT):
        print(f"CRITICAL: Port {config.API_PORT} is blocked by Windows or another app!")
    # 端口检查与清理
    app.run(host="0.0.0.0", port=config.API_PORT)