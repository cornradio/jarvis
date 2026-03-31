import os
import sys

def enable_autostart():
    # 1. 获取启动文件夹路径
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    vbs_path = os.path.join(startup_folder, 'JARVIS_AutoStart.vbs')
    
    # 2. 获取当前项目信息
    project_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
    main_script = os.path.join(project_dir, 'assistant_main.py')
    
    # 3. 编写 Vbs 脚本内容
    # 注意：""" 是为了处理路径中包含空格的情况，0 代表隐藏运行
    content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "{project_dir}"
WshShell.Run """{python_exe}"" ""{main_script}""", 0, False
'''
    
    try:
        # VBS 建议使用 UTF-16 或 ANSI/GBK
        with open(vbs_path, 'w', encoding='utf-16') as f:
            f.write(content)
        
        # 4. 删除旧的 .bat 脚本（如果存在）
        bat_old = os.path.join(startup_folder, 'JARVIS_AutoStart.bat')
        if os.path.exists(bat_old): os.remove(bat_old)

        print(f"✅ 成功！JARVIS 已切换为【极致隐藏模式】。")
        print(f"启动脚本已更换为: {vbs_path}")
        print(f"原理: 使用 VBScript 引擎在后台直接拉起 pythonw 进程。")
    except Exception as e:
        print(f"❌ 失败: {e}")

if __name__ == "__main__":
    enable_autostart()
