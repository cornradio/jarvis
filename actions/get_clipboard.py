# --- 获取剪切板内容 ---
from core import clipboard_tool

def run():
    # 调用剪切板工具并返回结果字典
    return clipboard_tool.get_clipboard_data()
