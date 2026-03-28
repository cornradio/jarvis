# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# --- 【系统配置】 ---
API_PORT = 5000 

# --- 【语音反馈配置】 ---
VOICE_ENABLED = True     # 默认开启语音反馈
VOICE_ENGINE  = "local"  # 切换选项: "local" (极速本地) 或 "edge" (真人云端)

# 本地语速 (pyttsx3): 默认 200, 建议 250-300 为快捷语速
LOCAL_RATE = 280

# 云端参数 (edge-tts):
# 语速: "+0%" 到 "+50%" (建议使用 "+50%" 满足您的快捷要求)
EDGE_VOICE = "zh-CN-YunxiNeural"
EDGE_RATE  = "+50%"

# --- 【指令注册表】 ---
COMMANDS = {
    # 特殊：语音控制开关 (由网页端专用触发)
    "toggle_voice": {
        "label": "语音开关",
        "post_params": ["切换语音"],
        "action": "none", # 内部逻辑处理
        "params": [],
        "reply": "语音反馈已更新"
    },
    "toggle_engine": {
        "label": "切换引擎",
        "post_params": ["切换引擎"],
        "action": "none",
        "params": [],
        "reply": "切换成功"
    },
    # 业务指令
    "vol_unmute": {
        "label": "音量恢复",
        "post_params": ["恢复音量", "恢复"],
        "action": "set_vol",
        "params": [30],
        "reply": "恢复"
    },
    "vol_max": {
        "label": "音量 MAX",
        "post_params": ["一百"],
        "action": "set_vol",
        "params": [100],
        "reply": "拉满"
    },
    "play_toggle": {
        "label": "播放/暂停",
        "post_params": ["播放", "暂停"],
        "action": "toggle_play_pause",
        "params": [],
        "reply": "收到"
    },
    "bright_up": {
        "label": "亮度 +",
        "post_params": ["亮一点"],
        "action": "adjust_brightness",
        "params": [True],
        "reply": "调亮"
    },
    "open_bili": {
        "label": "Bilibili",
        "post_params": ["b站"],
        "action": "open_url",
        "params": ["https://www.bilibili.com"],
        "reply": "走着"
    },
    "lock_pc": {
        "label": "锁屏",
        "post_params": ["锁屏"],
        "action": "lock_screen",
        "params": [],
        "reply": "再见"
    },
    "shutdown_pc": {
        "label": "关机",
        "post_params": ["关机"],
        "action": "shutdown",
        "params": [],
        "reply": "准备撤退"
    }
}
