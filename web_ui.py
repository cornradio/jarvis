# --- 贾维斯核心：全动态 UI 模板库 ---

# 这里只负责美化界面，不涉及后端逻辑
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JARVIS COMMANDER</title>
    <style>
        :root {
            --p: #00ecff; 
            --bg: #09090b;
            --card: rgba(255, 255, 255, 0.04);
            --text: #e2e2e7;
        }
        * { 
            touch-action: manipulation; 
            -webkit-user-select: none; 
            box-sizing: border-box; 
            transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        }
        body { 
            background: var(--bg); color: var(--text); font-family: 'Inter', -apple-system, sans-serif;
            display: flex; flex-direction: column; align-items: center; padding: 30px 15px; margin: 0;
            background-image: radial-gradient(circle at 50% 10%, #1a1a35 0%, #09090b 60%);
            min-height: 100vh;
        }
        h1 { font-size: 1.6rem; font-weight: 200; letter-spacing: 12px; margin: 20px 0 40px 0; color: var(--p); text-shadow: 0 0 30px rgba(0,236,255,0.4); text-transform: uppercase; }
        .grid { 
            display: grid; grid-template-columns: repeat(2, 1fr); 
            gap: 12px; width: 100%; max-width: 600px; 
        }
        .card { 
            background: var(--card); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; 
            padding: 22px 10px; text-align: center; cursor: pointer; backdrop-filter: blur(20px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .card:hover { border-color: var(--p); transform: translateY(-3px); }
        .card:active { background: var(--p); transform: scale(0.95); }
        .card:active .label { color: #000; }
        .label { font-size: 0.85rem; font-weight: 800; color: var(--p); text-shadow: 0 0 10px rgba(0,236,255,0.2); }
        .hint { font-size: 0.55rem; opacity: 0.2; margin-top: 6px; font-weight: 300; letter-spacing: 1px; }
        
        .guide-box {
            margin-top: 50px; width: 100%; max-width: 500px;
            background: rgba(0,0,0,0.5); border-radius: 12px; padding: 25px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .guide-box h3 { color: var(--p); margin-top: 0; font-weight: 400; font-size: 0.9rem; letter-spacing: 2px; }
        .guide-box p { font-size: 0.75rem; color: #888; line-height: 1.8; margin-bottom: 0; }
        code { background: #111; padding: 2px 6px; border-radius: 4px; color: #ffa500; font-family: monospace; border: 1px solid #333; }
    </style>
</head>
<body>
    <h1>JARVIS CORE</h1>
    <div class="grid">
        {% for cmd_id, item in commands.items() %}
        <div class="card" onclick="send('{{ item.post_params[0] }}')">
            <div class="label">{{ item.label }}</div>
            <div class="hint">POST TEXT: {{ item.post_params[0] }}</div>
        </div>
        {% endfor %}
    </div>
    
    <div class="guide-box">
        <h3>📱 远程指令枢纽</h3>
        <p>
            方法: <code>POST</code><br>
            接口: <code>http://{{ local_ip }}:{{ port }}/command</code><br>
            载荷: <code>{"text": "参数内容"}</code>
        </p>
    </div>

    <script>
        function send(t) {
            fetch('/command', { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify({ text: t }) 
            });
        }
    </script>
</body>
</html>
"""
