# --- 亮度调节功能 ---
import screen_brightness_control as sbc

def run(up=True):
    try:
        val = 100 if up is True else (0 if up is False else up)
        sbc.set_brightness(val)
        return True
    except:
        return False
