# --- 毁灭性删除协议 ---
import os
import shutil

def run(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            return True
        return False
    except Exception as e:
        print(f"Wipe Error: {e}")
        return False
