# 🛡️ 贾维斯 (JARVIS) - 网络 API 指挥官

[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/Version-v7.6_Elite-cyan.svg)](#)

> **核心定义**: 这是一个以 **API 驱动** 为灵魂的 Windows 远程控制器。它不仅是一个网页，更是你电脑的“云端外壳”。

---

## 📱 终极玩法：iOS 快捷指令 + Siri 联动 (重点)

本系统的核心价值在于 **“零接触操纵”**。你可以通过 iOS 的“快捷指令” App，通过 `获取 URL 内容 (POST)` 的方式，实现 **“嘿 Siri，销毁证据”** 或 **“嘿 Siri，静音模式”**。

### 如何配置 Siri 控制？
1. **新建快捷指令**: 打开 iOS “快捷指令” -> 创建新指令。
2. **添加操作**: 搜索“获取 URL 内容”。
3. **设置参数**:
   - **URL**: `http://[你的局域网IP]:5000/command`
   - **方法**: `POST`
   - **请求正文 (JSON)**: `{"text": "你的指令参数"}` (例如：`{"text": "锁屏"}`)
4. **命名指令**: 比如叫“锁定电脑”。
5. **语音控制**: 对着 iPhone 喊：**“嘿 Siri，锁定电脑”**，你的 PC 就会瞬间响应并回复真人语音。

---

## 🎨 系统仪表盘 (网页版)

> **注**: 网页仪表盘（`http://localhost:5000`）主要用于 **功能测试**、**查看指令文本** 以及 **动态配置重载**。

### 控制面板特性:
- **可视化测试**: 一键点击，实测 `config.py` 中的动作是否生效。
- **动态状态**: 实时切换 **“极速本地/云端真人”** 语音引擎。
- **🔄 热重载**: 修改 `config.py` 后点击顶部的“重载配置”，无需物理重启程序。

---

## ✨ 核心特性

- **🚀 异步多线程**: 指令执行与语音播报完全解耦，按钮响应快如闪电。
- **🎙️ 二代真人语音**: 基于微软 Edge-TTS (Yunxi/Xiaoxiao)，提供电影级的原声回馈。
- **💀 防御协议**: 永久抹除指定文件夹，秒级清除垃圾，Alt+F4 强制关闭窗口。
- **⚙️ 全开放架构**: 只要懂一点 Python，就能在 `actions.py` 里添加任何系统级操作。

---

## 🛠️ 快速部署

1. **环境准备**: Python 3.10+
2. **安装核心库**:
```powershell
pip install flask flask-cors pyttsx3 pygame edge-tts screen-brightness-control pyautogui pywin32
```
3. **点火启动**:
```powershell
python assistant_main.py
```

---

## ⚙️ 进阶配置指南

针对 **Power User** (专业用户) 的结构：
- **`config.py`**: 指令注册表。定义 `label` (网页名)、`post_params` (API 触发词)、`action` (执行函数) 及语音回复。
- **`actions.py`**: 技能逻辑。在这里用 Python 编写具体的电脑行为（文件操作、进程管理、键盘模拟等）。
- **`web_ui.py`**: 视觉模板。不影响逻辑的前提下，随意修改网页 UI 风格。

---

*Jarvis v7.6 - Designed for absolute control.*
