# --- 系统锁屏 ---
import ctypes

def run():
    ctypes.windll.user32.LockWorkStation()
    return True
