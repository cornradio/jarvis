# --- 贾维斯核心：全动态 UI 模板库 ---

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JARVIS CONTROL</title>
    <style>
        :root { --p: #00ecff; --bg: #08080a; --c: rgba(255,255,255,0.05); }
        * { touch-action: manipulation; -webkit-user-select: none; box-sizing: border-box; }
        body { 
            background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif;
            display: flex; flex-direction: column; align-items: center; padding: 20px 10px; margin: 0;
            background-image: radial-gradient(circle at 50% 5%, #151525 0%, #08080a 70%);
        }
        h1 { font-size: 1.2rem; letter-spacing: 12px; margin: 25px 0; color: var(--p); text-shadow: 0 0 20px rgba(0,236,255,0.4); }
        
        .settings-bar { display: flex; gap: 8px; margin-bottom: 25px; width: 100%; max-width: 600px; flex-wrap: wrap; }
        .btn-set { 
            flex: 1; padding: 12px 5px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.03); color: #fff; font-size: 0.7rem; 
            cursor: pointer; text-transform: uppercase; letter-spacing: 1px; min-width: 100px;
        }
        .btn-set.active { background: var(--p); color: #000; border-color: var(--p); font-weight: bold; }
        
        /* 重载按钮样式 */
        .btn-reload { background: #ffab00 !important; color: #000 !important; border-color: #ffab00 !important; font-weight: 800; }

        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; max-width: 600px; }
        .card { 
            background: var(--c); border: 1px solid rgba(255,255,255,0.05); border-radius: 15px; 
            padding: 22px 10px; text-align: center; transition: 0.1s;
        }
        .card:active { background: var(--p); color: #000; transform: scale(0.95); }
        .label { font-size: 0.85rem; font-weight: 800; color: var(--p); }
        .card:active .label { color: #000; }
        .hint { font-size: 0.5rem; opacity: 0.15; margin-top: 5px; }
        
        .api-info {
            margin-top: 40px; width: 100%; max-width: 500px; padding: 20px;
            background: rgba(0,0,0,0.5); border-top: 1px solid #222; border-radius: 15px;
            font-size: 0.7rem; color: #666; line-height: 1.6;
        }
        code { color: var(--p); font-family: monospace; }
    </style>
</head>
<body>
    <h1>JARVIS CORE</h1>
    
    <div class="settings-bar">
        <!-- 新增重载按钮 -->
        <button class="btn-set btn-reload" onclick="doReload()">🔄 重载配置</button>
        
        <button class="btn-set {% if voice_on %}active{% endif %}" onclick="send('切换语音')">
            {{ '🔊 语音:开' if voice_on else '🔇 语音:关' }}
        </button>
        <button class="btn-set active" onclick="send('切换引擎')">
            {{ '🚀 极速本地' if engine_name == 'local' else '🎙️ 云端真人' }}
        </button>
    </div>

    <div class="grid">
        {% for cmd_id, item in commands.items() %}
        {% if item.action != 'none' %}
        <div class="card" onclick="send('{{ item.post_params[0] }}')">
            <div class="label">{{ item.label }}</div>
            <div class="hint">TEXT: {{ item.post_params[0] }}</div>
        </div>
        {% endif %}
        {% endfor %}
    </div>

    <div class="api-info">
        URL: <code>http://{{ local_ip }}:{{ port }}/command</code><br>
        BODY: <code>{"text": "参数内容"}</code>
    </div>

    <script>
        function send(t) {
            fetch('/command', { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify({ text: t }) 
            }).then(() => {
                if (t.includes('切换')) {
                    setTimeout(() => location.reload(), 300);
                }
            });
        }
        
        function doReload() {
            fetch('/reload', { method: 'POST' }).then(() => {
                setTimeout(() => location.reload(), 300);
            });
        }
    </script>
</body>
</html>
"""
