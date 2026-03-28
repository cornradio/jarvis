# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# 【配置说明】:
# label:       网页按钮显示的名称
# post_params: 发送 POST 请求时 text 字段对应的值 (手机/脚本调用时使用)
# action:      对应的执行函数。你可以在 [actions.py] 中增加或修改这些函数
# params:      给 Python 函数传递的参数
# reply:       执行成功后贾维斯的语音回复内容

COMMANDS = {
    "vol_unmute": {
        "label": "音量恢复",
        "post_params": ["恢复音量", "恢复"],
        "action": "set_vol",
        "params": [30],
        "reply": "音量已恢复"
    },
    "vol_max": {
        "label": "音量 MAX",
        "post_params": ["满音量", "一百"],
        "action": "set_vol",
        "params": [100],
        "reply": "音量已拉满"
    },
    "play_toggle": {
        "label": "播放/暂停",
        "post_params": ["播放", "暂停"],
        "action": "toggle_play_pause",
        "params": [],
        "reply": "指令已下达"
    },
    "bright_up": {
        "label": "亮度 +",
        "post_params": ["亮一点", "加亮度"],
        "action": "adjust_brightness",
        "params": [True],
        "reply": "屏幕已调亮"
    },
    "open_bili": {
        "label": "Bilibili",
        "post_params": ["b站", "看视频"],
        "action": "open_url",
        "params": ["https://www.bilibili.com"],
        "reply": "正前往哔哩哔哩"
    },
    "open_github": {
        "label": "GitHub",
        "post_params": ["github"],
        "action": "open_url",
        "params": ["https://github.com"],
        "reply": "正在打开 GitHub"
    },
    "lock_pc": {
        "label": "锁定电脑",
        "post_params": ["锁屏"],
        "action": "lock_screen",
        "params": [],
        "reply": "长官再见"
    },
    "shutdown_pc": {
        "label": "自毁模式",
        "post_params": ["关机"],
        "action": "shutdown",
        "params": [],
        "reply": "关机程序已启动"
    }
}

# 语音播报属性
VOICE_VOLUME = 1.0
VOICE_RATE = 205
