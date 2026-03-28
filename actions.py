import os
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
            curr = sbc.get_brightness(display=0)[0]
            step = 20 if up else -20
            new_val = max(0, min(100, curr + step))
            sbc.set_brightness(new_val)
            return True
        except:
            return False

    def open_url(self, url):
        webbrowser.open(url)
        return True

    def lock_screen(self):
        ctypes.windll.user32.LockWorkStation()
        return True

    def shutdown(self):
        os.system("shutdown -s -t 60")
        return True
