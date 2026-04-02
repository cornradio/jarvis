# --- 摄像头拍照功能 ---
from core import cam_pygame as camera_tool

def run():
    # 拍照并返回保存路径
    return camera_tool.take_camera_photo()
