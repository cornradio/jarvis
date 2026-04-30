# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# --- 【系统配置】 ---
API_PORT = 20026

# --- 【语音反馈配置】 ---
VOICE_ENABLED = True
VOICE_ENGINE = "local"
LOCAL_RATE = 280
EDGE_VOICE = "zh-CN-YunxiNeural"
EDGE_RATE = "+50%"

# --- 【指令注册表】 ---
# label: 网页名 | post_params: 接口参数 | action: 函数名 | params: 参数列表 | reply: 回复 | emoji: 图标emoji | icon: 自定义图标URL
COMMANDS = {
    # 1. 游戏快捷
    "open_ow": {
        "label": "守望先锋",
        "post_params": ["开启守望", "OW"],
        "action": "run_cmd",
        "params": [r'"C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"'],
        "reply": "正在为您开启守望先锋，祝您游戏愉快",
        "emoji": "🎮",
        "icon": None,
    },
    "open_steam": {
        "label": "Steam",
        "post_params": ["蒸汽平台", "steam"],
        "action": "run_cmd",
        "params": [r'"C:\Program Files (x86)\Steam\steam.exe"'],
        "reply": "正在为您开启steam，祝您游戏愉快",
        "emoji": "🎮",
        "icon": None,
    },
    # 2. 安全与防御协议
    "wipe_data": {
        "label": "毁灭证据",
        "post_params": ["销毁", "毁灭"],
        "action": "wipe_evidence",
        "params": ["C:\\Users\\kasus\\Downloads\\证据"],
        "reply": "遵命，所有痕迹已抹除",
        "emoji": "🗑️",
        "icon": None,
    },
    "abort_shutdown": {
        "label": "取消关机",
        "post_params": ["取消关机", "别关机"],
        "action": "run_cmd",
        "params": ["shutdown -a"],
        "reply": "遵命，已中止关机流程",
        "emoji": "⏸️",
        "icon": None,
    },
    # 3. 音量控制阵列
    "vol_0": {
        "label": "静音",
        "post_params": ["静音", "0"],
        "action": "set_vol",
        "params": [0],
        "reply": "已静音",
        "emoji": "🔇",
        "icon": None,
    },
    "vol_50": {
        "label": "音量 50%",
        "post_params": ["音量一半", "50"],
        "action": "set_vol",
        "params": [50],
        "reply": "音量五十",
        "emoji": "🔉",
        "icon": None,
    },
    "vol_100": {
        "label": "音量 MAX",
        "post_params": ["一百", "100"],
        "action": "set_vol",
        "params": [100],
        "reply": "音量拉满",
        "emoji": "🔊",
        "icon": None,
    },
    # 4. 效率与媒体控制
    "play_toggle": {
        "label": "播放/暂停",
        "post_params": ["暂停", "播放"],
        "action": "toggle_play_pause",
        "params": [],
        "reply": "OK",
        "emoji": "▶️",
        "icon": None,
    },
    "close_win": {
        "label": "关闭窗口",
        "post_params": ["关窗口"],
        "action": "close_active_window",
        "params": [],
        "reply": "关了",
        "emoji": "❌",
        "icon": None,
    },
    "empty_bin": {
        "label": "清理回收站",
        "post_params": ["清垃圾"],
        "action": "empty_recycle_bin",
        "params": [],
        "reply": "垃圾已清理",
        "emoji": "🧹",
        "icon": None,
    },
    "calc": {
        "label": "计算器",
        "post_params": ["计算器"],
        "action": "launch_tool",
        "params": ["calc"],
        "reply": "打开计算器",
        "emoji": "🧮",
        "icon": None,
    },
    "Flydigi": {
        "label": "手柄驱动",
        "post_params": ["手柄驱动"],
        "action": "launch_tool",
        "params": ["C:\Program Files\Flydigi Space Station\Flydigi Space Station.exe"],
        "reply": "打开Flydigi手柄驱动",
        "emoji": "🎮",
        "icon": None,
    },
    "start_up": {
        "label": "开机启动",
        "post_params": ["开机启动文件夹"],
        "action": "launch_tool",
        "params": [
            r"C:\Users\kasus\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        ],
        "reply": "打开开机启动文件夹",
        "emoji": "🚀",
        "icon": None,
    },
    "chrome": {
        "label": "Chrome",
        "post_params": ["chrome"],
        "action": "launch_tool",
        "params": ["chrome"],
        "reply": "打开chrome",
        "emoji": "🌐",
        "icon": None,
    },
    "taskmgr": {
        "label": "任务管理",
        "post_params": ["任务管理"],
        "action": "launch_tool",
        "params": ["taskmgr"],
        "reply": "启动管理",
        "emoji": "📊",
        "icon": None,
    },
    # 5. 屏幕环境
    "bright_min": {
        "label": "深夜模式",
        "post_params": ["黑夜"],
        "action": "adjust_brightness",
        "params": [0],
        "reply": "进入黑夜模式",
        "emoji": "🌙",
        "icon": None,
    },
    "bright_max": {
        "label": "白天模式",
        "post_params": ["白天"],
        "action": "adjust_brightness",
        "params": [100],
        "reply": "亮起",
        "emoji": "☀️",
        "icon": None,
    },
    # 6. 快捷链接
    "github": {
        "label": "GitHub",
        "post_params": ["github"],
        "action": "open_url",
        "params": ["https://github.com"],
        "reply": "打开代码库",
        "emoji": "💻",
        "icon": None,
    },
    # 7. 系统终结
    "lock": {
        "label": "锁屏",
        "post_params": ["锁屏"],
        "action": "lock_screen",
        "params": [],
        "reply": "再见",
        "emoji": "🔒",
        "icon": None,
    },
    "screenshot": {
        "label": "屏幕截图",
        "post_params": ["截图"],
        "action": "take_screenshot",
        "params": [],
        "reply": "咔嚓",
        "emoji": "📸",
        "icon": None,
    },
    "clipboard": {
        "label": "剪切板",
        "post_params": ["剪切板"],
        "action": "get_clipboard",
        "params": [],
        "reply": "远程剪切板",
        "emoji": "📋",
        "icon": None,
    },
    "camera": {
        "label": "远程拍照",
        "post_params": ["拍照"],
        "action": "take_photo",
        "params": [],
        "reply": "请微笑",
        "emoji": "📷",
        "icon": None,
    },
    "shutdown": {
        "label": "关机",
        "post_params": ["关机", "自毁"],
        "action": "run_cmd",
        "params": ['shutdown -s -t 60 -c "JARVIS: 系统即将关闭，倒计时60秒"'],
        "reply": "系统即将关闭，倒计时60秒",
        "emoji": "⏻",
        "icon": None,
    },
}
