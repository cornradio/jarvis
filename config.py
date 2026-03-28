# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# --- 【系统配置】 ---
API_PORT = 5000  # 你可以在这里修改 API 端口

# --- 【语音配置】 ---
# 真人声音设置 (微软 Edge 云端引擎)
# 推荐声音: 
# zh-CN-XiaoxiaoNeural (温柔女声) 
# zh-CN-YunxiNeural (磁性男声)
# zh-CN-XiaoyiNeural (活泼女声)
VOICE_NAME = "zh-CN-YunxiNeural" 

# --- 【指令注册表】 ---
COMMANDS = {
    "vol_unmute": {
        "label": "音量恢复",
        "post_params": ["恢复音量", "恢复"],
        "action": "set_vol",
        "params": [30],
        "reply": "音量已为您恢复到百分之三十"
    },
    "vol_max": {
        "label": "音量 MAX",
        "post_params": ["满音量", "一百"],
        "action": "set_vol",
        "params": [100],
        "reply": "遵命，音量已拉满"
    },
    "play_toggle": {
        "label": "播放/暂停",
        "post_params": ["播放", "暂停"],
        "action": "toggle_play_pause",
        "params": [],
        "reply": "指令已下达，长官"
    },
    "bright_up": {
        "label": "亮度 +",
        "post_params": ["亮一点", "加亮度"],
        "action": "adjust_brightness",
        "params": [True],
        "reply": "屏幕已为您调亮"
    },
    "open_bili": {
        "label": "Bilibili",
        "post_params": ["b站", "看视频"],
        "action": "open_url",
        "params": ["https://www.bilibili.com"],
        "reply": "好的，正前往哔哩哔哩"
    },
    "open_github": {
        "label": "GitHub",
        "post_params": ["github"],
        "action": "open_url",
        "params": ["https://github.com"],
        "reply": "正在为您跳转 GitHub"
    },
    "lock_pc": {
        "label": "锁定电脑",
        "post_params": ["锁屏"],
        "action": "lock_screen",
        "params": [],
        "reply": "好的，长官再见"
    },
    "shutdown_pc": {
        "label": "自毁模式",
        "post_params": ["关机"],
        "action": "shutdown",
        "params": [],
        "reply": "关机程序正在启动，系统将在六十秒后自毁"
    }
}
