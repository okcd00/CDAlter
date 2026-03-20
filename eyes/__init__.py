# -*- coding: utf-8 -*-
"""
eyes - 视觉感知模块

本模块提供屏幕捕获、窗口识别、OCR识别等视觉功能。

模块组成：
- window_eye.py: 窗口识别与控制
- desktop_eye.py: 桌面截图捕获
- read_eye.py: 文件读取工具
- visual_residue.py: 视觉记忆（截图缓存）
- zoom_eye.py: 局部放大镜
- web_spider_eye.py: 网页爬虫
- web_spider_eye_selenium.py: Selenium 爬虫
- excel_eye.py: Excel 文件处理
- gamepad_eye.py: 游戏手柄输入

系统要求：
- Windows 系统
- pywin32 >= 220

使用示例：
    from eyes.window_eye import WindowEye
    from eyes.desktop_eye import DesktopEye

    # 获取窗口信息
    eye = WindowEye(window_name='记事本')
    print(eye.coordinate())

    # 截图
    desktop = DesktopEye()
    desktop.screenshot()
"""

from __future__ import annotations

__all__ = [
    'WindowEye',
    'DesktopEye',
    'ReadEye',
]

# 延迟导入，避免循环依赖
def __getattr__(name: str):
    if name == 'WindowEye':
        from eyes.window_eye import WindowEye
        return WindowEye
    elif name == 'DesktopEye':
        from eyes.desktop_eye import DesktopEye
        return DesktopEye
    elif name == 'ReadEye':
        from eyes.read_eye import ReadEye
        return ReadEye
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
