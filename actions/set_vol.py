# --- 音量控制功能 ---
vm = None

def set_vm(v):
    global vm
    vm = v

def run(level):
    if vm:
        vm.set_volume(level)
        return True
    return False
