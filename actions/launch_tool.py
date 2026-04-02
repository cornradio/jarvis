# --- 启动工具软件 ---
import os

def run(tool_cmd):
    # 注意这里：start "" "路径"
    os.system(f'start "" "{tool_cmd}"')
    return True
