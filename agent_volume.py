from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeManager:
    def __init__(self):
        print("INFO: 正在使用标准枚举器初始化音频...")
        try:
            # 1. 这种方式返回的是原始的 IMMDeviceEnumerator 封装
            enumerator = AudioUtilities.GetDeviceEnumerator()
            
            # 2. 直接获取默认设备，这会返回原始的 IMMDevice
            device = enumerator.GetDefaultAudioEndpoint(0, 0)
            
            # 3. 激活音频终端接口
            interface = device.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("INFO: 音频接口初始化成功 (标准方案)")
            
        except Exception as e:
            print(f"ERROR: 初始化失败: {e}")
            print("尝试最后的兜底方案 (GetSpeakers)...")
            try:
                # 最后的最后：尝试 pycaw 的简易接口
                speakers = AudioUtilities.GetSpeakers()
                # 针对不同版本的封装处理
                raw_device = speakers._device if hasattr(speakers, '_device') else speakers
                interface = raw_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                print("INFO: 兜底方案初始化成功")
            except Exception as e2:
                print(f"CRITICAL: 方案全部失败: {e2}")
                raise

    def set_volume(self, level):
        """设置音量 (0-100)"""
        try:
            val = max(0.0, min(1.0, float(level) / 100.0))
            self.volume.SetMasterVolumeLevelScalar(val, None)
            print(f"DEBUG: 成功设置音量为: {int(val*100)}%")
        except Exception as e:
            print(f"ERROR: 调节音量失败: {e}")

    def get_volume(self):
        """获取当前音量"""
        try:
            current_level = self.volume.GetMasterVolumeLevelScalar()
            return int(round(current_level * 100))
        except:
            return 0
