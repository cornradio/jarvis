import pyautogui
import os
from datetime import datetime

def take_silent_screenshot(save_dir="temp"):
    """
    安静地截取全屏并保存。
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 使用固定名称或时间戳。为了防止文件过多，可以使用固定名称并在执行后删除。
    # 这里我们返回路径供调用者使用。
    filepath = os.path.join(save_dir, "last_screenshot.png")
    
    try:
        # pyautogui.screenshot() 是静音的
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath
    except Exception as e:
        print(f"Screenshot Error: {e}")
        return None
