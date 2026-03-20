# -*- coding: utf-8 -*-
"""
hands - 操作执行模块

本模块提供键盘鼠标控制、Shell命令执行、GUI操作等功能。

模块组成：
- key_mouse_hand.py: 键盘鼠标控制 (核心)
- shell_hand.py: Shell 命令执行
- gui_hand.py: GUI 自动化 (PyAutoGUI)
- draw_hand.py: 绘图工具 (Turtle)
- packing_hand.py: 程序打包工具
- vk_codes.py: 虚拟键码映射表

使用示例：
    from hands.key_mouse_hand import KeyMouseHand

    # 键盘鼠标操作
    hand = KeyMouseHand()
    hand.click(100, 200)
    hand.type('Hello')
"""

from __future__ import annotations

__all__ = [
    'KeyMouseHand',
    'ShellHand',
    'PAGHand',
    'VK_CODE',
]

def __getattr__(name: str):
    if name == 'KeyMouseHand':
        from hands.key_mouse_hand import KeyMouseHand
        return KeyMouseHand
    elif name == 'ShellHand':
        from hands.shell_hand import ShellHand
        return ShellHand
    elif name == 'PAGHand':
        from hands.gui_hand import PAGHand
        return PAGHand
    elif name == 'VK_CODE':
        from hands.vk_codes import VK_CODE
        return VK_CODE
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
