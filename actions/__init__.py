import sys
import os
import importlib
import logging
from core.agent_volume import VolumeManager

# 设置基础日志，方便调试
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ActionsLoader")

class Actions:
    _instance = None

    def __new__(cls):
        # 简单的单例模式，避免重复加资源 (比如 VolumeManager)
        if cls._instance is None:
            cls._instance = super(Actions, cls).__new__(cls)
            cls._instance.vm = VolumeManager()
            cls._instance.loaded_actions = set() # 记录已加载的动作名
        return cls._instance

    def __init__(self):
        # 每次实例化（包括重载时）都会触发加载动作文件
        self.load_actions()

    def load_actions(self):
        """
        动态扫描 actions 目录下的所有 .py 文件
        并将每个文件中的 run 函数映射为本类的方法
        """
        actions_dir = os.path.dirname(__file__)
        files = [f for f in os.listdir(actions_dir) if f.endswith(".py") and f != "__init__.py"]
        
        # 清除之前加载但现在已经删除的动作
        current_action_names = {f[:-3] for f in files}
        for old_action in list(self.loaded_actions):
            if old_action not in current_action_names:
                if hasattr(self, old_action):
                    delattr(self, old_action)
                self.loaded_actions.remove(old_action)

        logger.info(f"Scanning actions in {actions_dir}...")
        for filename in files:
            module_name = filename[:-3]
            full_module_name = f"actions.{module_name}"
            
            try:
                # 使用 importlib 导入/重载模块
                if full_module_name in sys.modules:
                    module = importlib.reload(sys.modules[full_module_name])
                else:
                    module = importlib.import_module(full_module_name)
                
                # 如果模块有名为 run 的导出函数
                if hasattr(module, 'run'):
                    # 注入 VolumeManager (如果模块需要)
                    if hasattr(module, 'set_vm'):
                        module.set_vm(self.vm)
                    elif hasattr(module, 'vm'):
                        module.vm = self.vm
                        
                    # 将 run 方法绑定到 Actions 实例上
                    setattr(self, module_name, module.run)
                    self.loaded_actions.add(module_name)
                    logger.info(f"Loaded action: {module_name}")
                else:
                    logger.warning(f"Module {module_name} has no 'run' function")
            except Exception as e:
                logger.error(f"Failed to load action {module_name}: {e}")

    def reload(self):
        """手动触发重载动作文件"""
        self.load_actions()
