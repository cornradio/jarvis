# --- 清空回收站 (Windows Only) ---
import ctypes

def run():
    try:
        # SHEmptyRecycleBinW 参数: HWND, RootPath, Flags (1: SHERB_NOCONFIRMATION, 2: SHERB_NOPROGRESSUI, 4: SHERB_NOSOUND)
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1 + 2 + 4)
        return True
    except:
        return False
