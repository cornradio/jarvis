# --- 贾维斯核心：全动态 UI 模板库 ---

OLD_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JARVIS CONTROL</title>
    <!-- 引入外部 JS 核心，强制置顶 -->
    <script src="/static/script.js"></script>
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
        .btn-reload { background: #ffab00 !important; color: #000 !important; border-color: #ffab00 !important; font-weight: 800; }
        .btn-new-ui { background: #4caf50 !important; color: #fff !important; border-color: #4caf50 !important; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; max-width: 600px; }
        .card { 
            background: var(--c); border: 1px solid rgba(255,255,255,0.05); border-radius: 15px; 
            padding: 22px 10px; text-align: center; transition: 0.1s;
        }
        .card:active { background: var(--p); color: #000; transform: scale(0.95); }
        .label { font-size: 0.85rem; font-weight: 800; color: var(--p); }
        .hint { font-size: 0.5rem; opacity: 0.15; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>JARVIS CORE</h1>
    <div class="settings-bar">
        <button class="btn-set btn-reload" onclick="doReload()">🔄 强制重启</button>
        <button class="btn-set {% if voice_on %}active{% endif %}" onclick="send('切换语音')">
            {{ '🔊 语音:开' if voice_on else '🔇 语音:关' }}
        </button>
        <button class="btn-set active" onclick="send('切换引擎')">
            {{ '🚀 极速本地' if engine_name == 'local' else '🎙️ 云端真人' }}
        </button>
        <a href="/new" class="btn-set btn-new-ui" style="text-decoration:none;text-align:center;">✨ 新界面</a>
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
</body>
</html>
"""

# --- 新版 a-plan 风格界面 ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="color-scheme" content="dark">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>JARVIS</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🤖</text></svg>">
    <script src="/static/script.js"></script>
    <style>
        :root {
            --primary: #00ecff;
            --bg-dark: #08080a;
            --card-bg: rgba(255,255,255,0.03);
            --card-border: rgba(255,255,255,0.08);
            color-scheme: dark;
        }

        * {
            touch-action: manipulation;
            -webkit-user-select: none;
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            height: 100vh;
            background: radial-gradient(ellipse farthest-corner at center top, #151525 0%, #08080a 70%);
            color: #fff;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            overflow: hidden;
        }

        html {
            background-color: #000 !important;
            color-scheme: dark;
        }

        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            padding: 15px 20px;
            display: flex;
            gap: 10px;
            z-index: 100;
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .top-bar a {
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            transition: all 0.2s;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: rgba(255,255,255,0.7);
        }

        .top-bar a:hover {
            background: var(--primary);
            color: #000;
            border-color: var(--primary);
        }

        .top-bar .voice-toggle {
            margin-left: auto;
        }

        .top-bar .voice-toggle.active {
            background: var(--primary);
            color: #000;
            border-color: var(--primary);
        }

        .app-container {
            position: relative;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 800px;
            height: 75vh;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .app-container::-webkit-scrollbar {
            width: 6px;
        }

        .app-container::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.15);
            border-radius: 3px;
        }

        .icon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 20px;
            padding: 80px 10px 100px;
            justify-items: center;
        }

        .icon {
            width: 90px;
            height: 90px;
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: 8px;
            position: relative;
            overflow: hidden;
        }

        .icon::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(0,236,255,0.1) 0%, transparent 50%);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .icon:hover::before {
            opacity: 1;
        }

        .icon:hover {
            transform: scale(1.1) translateY(-8px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            border-color: var(--primary);
        }

        .icon:active {
            transform: scale(1.05) translateY(-4px);
        }

        .icon-label {
            font-size: 11px;
            color: rgba(255,255,255,0.8);
            text-align: center;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            line-height: 1.2;
            max-width: 85px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .icon-emoji {
            font-size: 28px;
            margin-bottom: 4px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        .dock {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(40, 40, 40, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 26px;
            padding: 12px 20px;
            display: flex;
            gap: 12px;
            z-index: 9999;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }

        .dock a, .dock button {
            font-size: 24px;
            text-decoration: none;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.2);
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            cursor: pointer;
            color: #fff;
        }

        .dock a:hover, .dock button:hover {
            transform: scale(1.3) translateY(-10px);
            background: var(--primary);
            color: #000;
        }

        .dock a:active, .dock button:active {
            transform: scale(1.15) translateY(-5px);
        }

        .toast {
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--primary);
            color: #000;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 500;
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 10000;
            pointer-events: none;
        }

        .toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }

        /* 响应式 */
        @media screen and (max-width: 600px) {
            .app-container {
                width: 95%;
                height: 70vh;
            }

            .icon-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                padding: 70px 5px 120px;
            }

            .icon {
                width: 80px;
                height: 80px;
                border-radius: 20px;
            }

            .icon-emoji {
                font-size: 24px;
            }

            .icon-label {
                font-size: 10px;
            }

            .dock {
                bottom: 15px;
                padding: 10px 15px;
                gap: 8px;
            }

            .dock a, .dock button {
                width: 40px;
                height: 40px;
                font-size: 20px;
            }

            .top-bar {
                padding: 10px 15px;
                flex-wrap: wrap;
            }

            .top-bar a {
                font-size: 12px;
                padding: 6px 12px;
            }
        }

        @media screen and (min-width: 900px) {
            .icon-grid {
                grid-template-columns: repeat(5, 1fr);
            }
        }

        .icon-text {
            background: linear-gradient(135deg, rgba(0,236,255,0.15) 0%, rgba(0,236,255,0.05) 100%);
            border: 1px solid rgba(0,236,255,0.2);
        }

        .group-title {
            grid-column: 1 / -1;
            font-size: 12px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            letter-spacing: 3px;
            padding: 10px 0 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 5px;
            width: 100%;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <a href="/old">📋 旧版界面</a>
        <a href="/settings">⚙️ 配置</a>
        <a href="javascript:void(0)" onclick="doReload()" style="color: #ffab00;">🔄 重载</a>
        <a href="javascript:void(0)" class="voice-toggle {% if voice_on %}active{% endif %}" onclick="send('切换语音')">
            {{ '🔊 开启' if voice_on else '🔇 关闭' }}
        </a>
    </div>

    <div class="app-container">
        <div class="icon-grid">
            {% for cmd_id, item in commands.items() %}
            {% if item.action != 'none' %}
            <div class="icon {% if not item.icon %}icon-text{% endif %}" 
                 onclick="executeAndShow('{{ item.post_params[0] }}', '{{ item.label }}')"
                 {% if item.icon %}style="background-image: url('{{ item.icon }}');"{% endif %}>
                {% if item.icon %}
                <span class="icon-label">{{ item.label }}</span>
                {% else %}
                <span class="icon-emoji">{{ item.emoji }}</span>
                <span class="icon-label">{{ item.label }}</span>
                {% endif %}
            </div>
            {% endif %}
            {% endfor %}
        </div>
    </div>

    <div class="dock">
        <a href="/settings" title="配置">⚙️</a>
        <button onclick="send('锁屏')" title="锁屏">🔒</button>
        <button onclick="send('截图')" title="截图">📸</button>
        <button onclick="send('静音')" title="静音">🔇</button>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        function executeAndShow(cmd, label) {
            send(cmd);
            showToast('执行: ' + label);
        }

        function showToast(msg) {
            var toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(function() {
                toast.classList.remove('show');
            }, 1500);
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                showToast('JARVIS 就绪');
            }
        });
    </script>
</body>
</html>
"""

# --- 设置页面模板 ---
SETTINGS_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="color-scheme" content="dark">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>JARVIS 配置</title>
    <script src="/static/script.js"></script>
    <style>
        :root {
            --primary: #00ecff;
            --bg-dark: #08080a;
            --card-bg: rgba(255,255,255,0.05);
            --card-border: rgba(255,255,255,0.1);
            color-scheme: dark;
        }

        * {
            touch-action: manipulation;
            -webkit-user-select: none;
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: var(--bg-dark);
            color: #fff;
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
            min-height: 100vh;
        }

        .header {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .header a, .header button {
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-size: 14px;
            border: 1px solid var(--card-border);
            background: var(--card-bg);
            color: #fff;
            cursor: pointer;
            transition: all 0.2s;
        }

        .header a:hover, .header button:hover {
            background: var(--primary);
            color: #000;
            border-color: var(--primary);
        }

        .btn-primary {
            background: var(--primary) !important;
            color: #000 !important;
            border-color: var(--primary) !important;
            font-weight: bold;
        }

        .btn-save {
            background: #4caf50 !important;
            border-color: #4caf50 !important;
            color: #fff !important;
        }

        .section {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 14px;
            color: var(--primary);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--card-border);
            letter-spacing: 2px;
        }

        .form-row {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            gap: 15px;
            flex-wrap: wrap;
        }

        .form-label {
            width: 120px;
            font-size: 13px;
            color: rgba(255,255,255,0.6);
        }

        .form-input, .form-select {
            flex: 1;
            min-width: 150px;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid var(--card-border);
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 13px;
        }

        .toggle {
            width: 50px;
            height: 26px;
            background: rgba(255,255,255,0.1);
            border-radius: 13px;
            cursor: pointer;
            transition: 0.2s;
            position: relative;
        }

        .toggle.on {
            background: var(--primary);
        }

        .toggle::after {
            content: '';
            position: absolute;
            top: 3px;
            left: 3px;
            width: 20px;
            height: 20px;
            background: #fff;
            border-radius: 50%;
            transition: 0.2s;
        }

        .toggle.on::after {
            left: 27px;
        }

        .commands-section {
            max-height: 500px;
            overflow-y: auto;
        }

        .cmd-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .cmd-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
        }

        .cmd-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .cmd-title {
            font-weight: bold;
            color: var(--primary);
            font-size: 14px;
        }

        .cmd-delete {
            background: #f44336;
            color: #fff;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }

        .cmd-fields {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .cmd-field {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .cmd-field label {
            font-size: 11px;
            color: rgba(255,255,255,0.4);
        }

        .cmd-field input {
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 12px;
        }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--primary);
            color: #000;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 500;
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 10000;
        }

        .toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }

        .add-cmd {
            background: #4caf50;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            margin-top: 10px;
        }

        @media screen and (max-width: 600px) {
            .form-row {
                flex-direction: column;
                align-items: stretch;
            }

            .form-label {
                width: 100%;
            }

            .cmd-fields {
                grid-template-columns: 1fr;
            }

            .header {
                gap: 10px;
            }

            .header a, .header button {
                flex: 1;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <a href="/">← 返回主页</a>
        <a href="/new">✨ 新界面</a>
        <button onclick="saveSettings()" class="btn-save">💾 保存配置</button>
        <button onclick="addCommand()" class="btn-primary">➕ 添加指令</button>
        <button onclick="testVoice()">🔊 测试语音</button>
    </div>

    <div class="section">
        <div class="section-title">【系统配置】</div>
        <div class="form-row">
            <span class="form-label">API_PORT</span>
            <input type="number" class="form-input" id="API_PORT" value="{{ config.API_PORT }}">
        </div>
        <div class="form-row">
            <span class="form-label">语音反馈</span>
            <div class="toggle {% if config.VOICE_ENABLED %}on{% endif %}" id="VOICE_ENABLED" onclick="this.classList.toggle('on')"></div>
        </div>
        <div class="form-row">
            <span class="form-label">语音引擎</span>
            <select class="form-select" id="VOICE_ENGINE">
                <option value="local" {% if config.VOICE_ENGINE == 'local' %}selected{% endif %}>本地极速</option>
                <option value="edge" {% if config.VOICE_ENGINE == 'edge' %}selected{% endif %}>云端真人</option>
            </select>
        </div>
        <div class="form-row">
            <span class="form-label">LOCAL_RATE</span>
            <input type="number" class="form-input" id="LOCAL_RATE" value="{{ config.LOCAL_RATE }}">
        </div>
        <div class="form-row">
            <span class="form-label">EDGE_VOICE</span>
            <input type="text" class="form-input" id="EDGE_VOICE" value="{{ config.EDGE_VOICE }}">
        </div>
        <div class="form-row">
            <span class="form-label">EDGE_RATE</span>
            <input type="text" class="form-input" id="EDGE_RATE" value="{{ config.EDGE_RATE }}">
        </div>
    </div>

    <div class="section commands-section">
        <div class="section-title">【指令列表】 ({{ commands|length }} 条)</div>
        <div class="cmd-list">
            {% for cmd_id, item in commands.items() %}
            <div class="cmd-card" data-cmd-id="{{ cmd_id }}">
                <div class="cmd-header">
                    <span class="cmd-title">{{ item.label }}</span>
                    <button class="cmd-delete" onclick="deleteCommand('{{ cmd_id }}')">删除</button>
                </div>
                <div class="cmd-fields">
                    <div class="cmd-field">
                        <label>ID</label>
                        <input type="text" value="{{ cmd_id }}" data-field="cmd_id" readonly>
                    </div>
                    <div class="cmd-field">
                        <label>显示名称</label>
                        <input type="text" value="{{ item.label }}" data-field="label">
                    </div>
                    <div class="cmd-field">
                        <label>触发词 (逗号分隔)</label>
                        <input type="text" value="{{ item.post_params|join(',') }}" data-field="post_params">
                    </div>
                    <div class="cmd-field">
                        <label>动作</label>
                        <input type="text" value="{{ item.action }}" data-field="action">
                    </div>
                    <div class="cmd-field">
                        <label>参数 (逗号分隔)</label>
                        <input type="text" value="{{ item.params|join(',') }}" data-field="params">
                    </div>
                    <div class="cmd-field">
                        <label>Emoji</label>
                        <input type="text" value="{{ item.emoji }}" data-field="emoji">
                    </div>
                    <div class="cmd-field" style="grid-column: span 2;">
                        <label>图标 URL (可选)</label>
                        <input type="text" value="{{ item.icon or '' }}" data-field="icon" placeholder="留空使用 Emoji">
                    </div>
                    <div class="cmd-field" style="grid-column: span 2;">
                        <label>回复语</label>
                        <input type="text" value="{{ item.reply }}" data-field="reply">
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <button class="add-cmd" onclick="addCommand()">➕ 添加新指令</button>
    </div>

    <div class="toast" id="toast">保存成功</div>

    <script>
        window.saveSettings = function() {
            var data = {
                API_PORT: parseInt(document.getElementById('API_PORT').value),
                VOICE_ENABLED: document.getElementById('VOICE_ENABLED').classList.contains('on'),
                VOICE_ENGINE: document.getElementById('VOICE_ENGINE').value,
                LOCAL_RATE: parseInt(document.getElementById('LOCAL_RATE').value),
                EDGE_VOICE: document.getElementById('EDGE_VOICE').value,
                EDGE_RATE: document.getElementById('EDGE_RATE').value,
                commands: {}
            };

            document.querySelectorAll('.cmd-card').forEach(function(card) {
                var cmdId = card.querySelector('[data-field="cmd_id"]').value;
                var iconVal = card.querySelector('[data-field="icon"]').value;
                data.commands[cmdId] = {
                    label: card.querySelector('[data-field="label"]').value,
                    post_params: card.querySelector('[data-field="post_params"]').value.split(',').map(function(x) { return x.trim(); }).filter(function(x) { return x; }),
                    action: card.querySelector('[data-field="action"]').value,
                    params: card.querySelector('[data-field="params"]').value.split(',').map(function(x) { return x.trim(); }).filter(function(x) { return x; }),
                    emoji: card.querySelector('[data-field="emoji"]').value || '📌',
                    icon: iconVal || null,
                    reply: card.querySelector('[data-field="reply"]').value
                };
            });

            fetch('/settings/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(function(res) { return res.json(); })
            .then(function(data) {
                var toast = document.getElementById('toast');
                toast.textContent = data.status === 'success' ? '保存成功' : '保存失败: ' + data.msg;
                toast.classList.add('show');
                setTimeout(function() { toast.classList.remove('show'); }, 2000);
            });
        };

        window.deleteCommand = function(cmdId) {
            if (confirm('确定删除指令 ' + cmdId + '?')) {
                var card = document.querySelector('[data-cmd-id="' + cmdId + '"]');
                if (card) card.remove();
            }
        };

        window.addCommand = function() {
            var id = 'cmd_' + Date.now();
            var div = document.createElement('div');
            div.className = 'cmd-card';
            div.setAttribute('data-cmd-id', id);
            div.innerHTML = '<div class="cmd-header"><span class="cmd-title">新指令</span><button class="cmd-delete" onclick="this.closest(\'.cmd-card\').remove()">删除</button></div>' +
                '<div class="cmd-fields">' +
                '<div class="cmd-field"><label>ID</label><input type="text" value="' + id + '" data-field="cmd_id" readonly></div>' +
                '<div class="cmd-field"><label>显示名称</label><input type="text" value="新指令" data-field="label"></div>' +
                '<div class="cmd-field"><label>触发词</label><input type="text" value="" data-field="post_params"></div>' +
                '<div class="cmd-field"><label>动作</label><input type="text" value="run_cmd" data-field="action"></div>' +
                '<div class="cmd-field"><label>参数</label><input type="text" value="" data-field="params"></div>' +
                '<div class="cmd-field"><label>Emoji</label><input type="text" value="📌" data-field="emoji"></div>' +
                '<div class="cmd-field" style="grid-column: span 2;"><label>图标 URL</label><input type="text" value="" data-field="icon" placeholder="留空使用 Emoji"></div>' +
                '<div class="cmd-field" style="grid-column: span 2;"><label>回复语</label><input type="text" value="OK" data-field="reply"></div>' +
                '</div>';
            document.querySelector('.cmd-list').appendChild(div);
            window.scrollTo(0, document.body.scrollHeight);
        };

        window.testVoice = function() {
            fetch('/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: '测试语音'})
            });
        };
    </script>
</body>
</html>
"""
