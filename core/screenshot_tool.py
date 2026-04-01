import os
import threading
from datetime import datetime
from PIL import Image

# 尝试加载 windows_capture (现代 API, 支持 HDR 捕获)
try:
    import windows_capture
    from windows_capture import Frame, FrameProcessor, CaptureControl, NativeWindowsCapture
    WINDOWS_CAPTURE_AVAILABLE = True
except ImportError:
    WINDOWS_CAPTURE_AVAILABLE = False
    class Frame: pass
    class FrameProcessor: pass
    class CaptureControl: pass
    class NativeWindowsCapture: pass

def take_silent_screenshot(save_dir="temp"):
    """
    安静地截取全屏并保存。优先使用 Windows 现代 API 以解决 HDR 过曝。
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filepath = os.path.join(save_dir, "last_screenshot.png")

    # 1. 尝试使用现代 Windows Graphics Capture (解决 HDR 效果好)
    if WINDOWS_CAPTURE_AVAILABLE:
        try:
            processor = SingleFrameProcessor()
            capture = NativeWindowsCapture(processor)
            capture.start()
            
            if processor.stop_event.wait(timeout=2.0) and processor.frame_img:
                img = processor.frame_img
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # --- 用户要求不再手动降低亮度 ---
                img.save(filepath)
                return filepath
        except Exception as e:
            print(f"WindowsCapture Error: {e}")

    # 2. 备选方案：pyautogui (保底，防止 API 库不工作)
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        # 对于普通的 BitBlt 截图，保持原始亮度不处理
        screenshot.save(filepath)
        return filepath
    except Exception as e:
        print(f"Fallback Screenshot Error: {e}")
        return None

class SingleFrameProcessor(FrameProcessor):
    def __init__(self):
        super().__init__()
        self.frame_img = None
        self.stop_event = threading.Event()

    def on_frame_arrived(self, frame: Frame, capture_control: CaptureControl):
        self.frame_img = frame.to_pil()
        capture_control.stop()
        self.stop_event.set()

    def on_closed(self):
        self.stop_event.set()




