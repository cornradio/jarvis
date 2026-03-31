import win32clipboard
import os
from PIL import ImageGrab
from datetime import datetime

def get_clipboard_data(save_dir="temp"):
    """
    获取剪切板内容：支持文件、图片、文本。
    返回一个字典：{"type": "...", "path": "..."}
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 优先检查图片（Pillow 接口最简单）
    try:
        img = ImageGrab.grabclipboard()
        if img:
            # 如果是图片列表（文件形式），grabclipboard 会返回列表，这里处理的是真正的位图
            if not isinstance(img, list):
                img_path = os.path.join(save_dir, "clipboard_img.png")
                img.save(img_path)
                return {"type": "image", "path": img_path}
    except Exception as e:
        print(f"Clipboard Image Check Error: {e}")

    # 检查文件和文本
    try:
        win32clipboard.OpenClipboard()
        
        # 1. 检查文件 (CF_HDROP)
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            win32clipboard.CloseClipboard()
            if files and len(files) > 0:
                # 暂时返回第一个文件的路径
                return {"type": "file", "path": files[0]}

        # 2. 检查文本 (CF_UNICODETEXT)
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            text_path = os.path.join(save_dir, "clipboard_text.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)
            return {"type": "text", "path": text_path}

        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f"Clipboard win32 Check Error: {e}")
        try: win32clipboard.CloseClipboard()
        except: pass

    return None
