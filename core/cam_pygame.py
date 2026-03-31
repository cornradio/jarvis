import pygame
import pygame.camera
import os
import time

def take_camera_photo(save_dir="temp"):
    print("[JARVIS] 正在启动摄像头 (PYGAME 驱动模式)...")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    filepath = os.path.join(save_dir, "camera_capture.jpg")

    try:
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        if not cameras:
            print("[JARVIS] 错误: 未检测到摄像头设备！")
            return None
        
        cam = pygame.camera.Camera(cameras[0], (640, 480))
        cam.start()
        
        # 预热并捕捉
        time.sleep(1.0)
        image = cam.get_image()
        pygame.image.save(image, filepath)
        
        cam.stop()
        print(f"[JARVIS] 拍照成功: {filepath}")
        return filepath
    except Exception as e:
        print(f"[JARVIS] 拍照异常: {e}")
        return None
