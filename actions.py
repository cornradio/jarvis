import os
import shutil # 用于递归删除
import ctypes
import pyautogui
import webbrowser
import screen_brightness_control as sbc
from agent_volume import VolumeManager

class Actions:
    def __init__(self):
        self.vm = VolumeManager()

    def set_vol(self, level):
        self.vm.set_volume(level)
        return True

    def toggle_play_pause(self):
        pyautogui.press('playpause')
        return True

    def adjust_brightness(self, up=True):
        try:
            val = 100 if up is True else (0 if up is False else up)
            sbc.set_brightness(val)
            return True
        except: return False

    def open_url(self, url):
        webbrowser.open(url)
        return True

    def launch_tool(self, tool_cmd):
        os.system(f"start {tool_cmd}")
        return True

    def close_active_window(self):
        pyautogui.hotkey('alt', 'f4')
        return True

    def empty_recycle_bin(self):
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1 + 2 + 4)
            return True
        except: return False

    # --- 新增：毁灭性删除协议 ---
    def wipe_evidence(self, folder_path):
        try:
            if os.path.exists(folder_path):
                # 暴力递归删除整个文件夹及其内容
                shutil.rmtree(folder_path)
                # 删完之后重新建个空的，假装没发生过 (可选，如果你需要文件夹保留)
                # os.makedirs(folder_path) 
                return True
            return False
        except Exception as e:
            print(f"Wipe Error: {e}")
            return False

    def lock_screen(self):
        ctypes.windll.user32.LockWorkStation()
        return True

    def shutdown(self):
        os.system("shutdown -s -t 60")
        return True
