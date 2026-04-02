# --- 屏幕截图工具 ---
from core import screenshot_tool

def run():
    # 此方法调用截图工具并返回文件路径
    return screenshot_tool.take_silent_screenshot()
