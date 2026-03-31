import os
import subprocess


def kill_port(port):
    try:
        # 查找占用端口的 PID
        output = subprocess.check_output(
            f"netstat -ano | findstr :{port}", shell=True
        ).decode()
        for line in output.strip().split("\n"):
            pid = line.strip().split()[-1]
            print(f"正在清理端口 {port} 的进程 PID: {pid}")
            os.system(f"taskkill /F /PID {pid}")
    except:
        print(f"端口 {port} 看起来是干净的，没有被占用。")


kill_port(5000)
