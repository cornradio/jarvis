# --- 贾维斯 (JARVIS) 核心指令注册表 ---

# --- 【系统配置】 ---
API_PORT = 5000

# --- 【语音反馈配置】 ---
VOICE_ENABLED = True
VOICE_ENGINE = "local"
LOCAL_RATE = 280
EDGE_VOICE = "zh-CN-YunxiNeural"
EDGE_RATE = "+50%"

# --- 【指令注册表】 ---
# label: 网页名 | post_params: 接口参数 | action: 函数名 | params: 参数列表 | reply: 回复
COMMANDS = {
    # 1. 系统底层控制 (网页专用)
    "reload_cfg": {
        "label": "🔄 重载配置",
        "post_params": ["重载"],
        "action": "none",
        "params": [],
        "reply": "配置重载成功",
    },
    "toggle_voice": {
        "label": "音量反馈 ON/OFF",
        "post_params": ["切换语音"],
        "action": "none",
        "params": [],
        "reply": "设置已同步",
    },
    "toggle_engine": {
        "label": "极速/真人切换",
        "post_params": ["切换引擎"],
        "action": "none",
        "params": [],
        "reply": "引擎已切换",
    },
    # 2. 安全与防御协议
    "wipe_data": {
        "label": "毁灭证据",
        "post_params": ["销毁", "毁灭"],
        "action": "wipe_evidence",
        "params": ["C:\\Users\\kasus\\Downloads\\证据"],
        "reply": "遵命，所有痕迹已抹除",
    },
    "abort_shutdown": {
        "label": "取消关机",
        "post_params": ["取消关机", "别关机"],
        "action": "run_cmd",
        "params": ["shutdown -a"],
        "reply": "遵命，已中止关机流程",
    },
    # 3. 音量控制阵列
    "vol_0": {
        "label": "静音",
        "post_params": ["静音", "0"],
        "action": "set_vol",
        "params": [0],
        "reply": "已静音",
    },
    "vol_50": {
        "label": "音量 50%",
        "post_params": ["音量五十", "50"],
        "action": "set_vol",
        "params": [50],
        "reply": "音量五十",
    },
    "vol_100": {
        "label": "音量 MAX",
        "post_params": ["一百", "100"],
        "action": "set_vol",
        "params": [100],
        "reply": "音量拉满",
    },
    # 4. 效率与媒体控制
    "play_toggle": {
        "label": "播放/暂停",
        "post_params": ["暂停", "播放"],
        "action": "toggle_play_pause",
        "params": [],
        "reply": "OK",
    },
    "close_win": {
        "label": "关闭窗口",
        "post_params": ["关窗口"],
        "action": "close_active_window",
        "params": [],
        "reply": "关了",
    },
    "empty_bin": {
        "label": "清理回收站",
        "post_params": ["清垃圾"],
        "action": "empty_recycle_bin",
        "params": [],
        "reply": "垃圾已清理",
    },
    "calc": {
        "label": "计算器",
        "post_params": ["计算器"],
        "action": "launch_tool",
        "params": ["calc"],
        "reply": "打开计算器",
    },
    "chrome": {
        "label": "Chrome",
        "post_params": ["chrome"],
        "action": "launch_tool",
        "params": ["chrome"],
        "reply": "打开chrome",
    },
    "taskmgr_test": {
        "label": "测试-任务管理器",
        "post_params": ["测试任务管理器", "调试"],
        "action": "run_cmd",
        "params": ["taskmgr"],
        "reply": "正在测试通用命令执行：打开任务管理器",
    },
    "taskmgr": {
        "label": "任务管理器",
        "post_params": ["任务管理"],
        "action": "launch_tool",
        "params": ["taskmgr"],
        "reply": "启动管理",
    },
    # 5. 屏幕环境
    "bright_min": {
        "label": "深夜亮度",
        "post_params": ["黑夜"],
        "action": "adjust_brightness",
        "params": [0],
        "reply": "进入黑夜模式",
    },
    "bright_max": {
        "label": "白天亮度",
        "post_params": ["白天"],
        "action": "adjust_brightness",
        "params": [100],
        "reply": "亮起",
    },
    # 6. 快捷链接
    "github": {
        "label": "GITHUB",
        "post_params": ["github"],
        "action": "open_url",
        "params": ["https://github.com"],
        "reply": "打开代码库",
    },
    # 7. 系统终结
    "lock": {
        "label": "锁屏",
        "post_params": ["锁屏"],
        "action": "lock_screen",
        "params": [],
        "reply": "再见",
    },
    "shutdown": {
        "label": "极速关机",
        "post_params": ["关机", "自毁"],
        "action": "run_cmd",
        "params": ['shutdown -s -t 60 -c "JARVIS: 系统即将关闭，倒计时60秒"'],
        "reply": "系统即将关闭，倒计时60秒",
    },
}
