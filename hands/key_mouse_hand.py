# -*- coding: utf-8 -*-
"""
key_mouse_hand - 键盘鼠标控制

功能：
- 鼠标移动、点击、拖拽
- 键盘按键、组合键
- 文字输入

提供两种实现：
- KeyMouseHand_WIN32: 使用 win32api (底层)
- KeyMouseHand_PUI: 使用 PyUserInput (跨平台)

依赖：
- pywin32 (win32api, win32con, win32gui)
- pymouse, pykeyboard, pynput

使用示例：
    from hands.key_mouse_hand import KeyMouseHand

    hand = KeyMouseHand()

    # 鼠标操作
    hand.click(100, 200)
    hand.double_click(100, 200)
    hand.move_to(300, 400)

    # 键盘操作
    hand.tap_key('a')
    hand.type('Hello World')
    hand.tap_comb('C', 'ctrl')  # Ctrl+C
"""

from __future__ import annotations

import re
import time
import ctypes
from typing import Optional, List, Tuple, Union

import win32api
import win32con
import win32gui

# 可选依赖，按需导入
try:
    from pymouse import PyMouse
    from pykeyboard import PyKeyboard
    HAS_PYUSERINPUT = True
except ImportError:
    HAS_PYUSERINPUT = False

try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


class KeyMouseHand_WIN32:
    """
    Windows 原生键盘鼠标控制

    使用 win32api 实现，适用于 Windows 系统。

    使用示例：
        hand = KeyMouseHand_WIN32()
        hand.click(100, 200)
    """

    def __init__(self):
        self.current_position = win32api.GetCursorPos()

    def move_to(self, x: int, y: int) -> None:
        """
        移动鼠标到指定位置

        Args:
            x: X 坐标
            y: Y 坐标
        """
        self.current_position = (x, y)
        win32api.SetCursorPos([x, y])

    def move(self, dx: int, dy: int) -> None:
        """
        相对移动鼠标

        Args:
            dx: X 方向偏移
            dy: Y 方向偏移
        """
        x, y = self.current_position
        self.move_to(x + dx, y + dy)

    def _click_win32con(self, x: int, y: int, key: str = 'left') -> None:
        """使用 win32con 点击"""
        if 'left' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP,
                x, y, 0, 0
            )
        if 'right' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_RIGHTDOWN | win32con.MOUSEEVENTF_RIGHTUP,
                x, y, 0, 0
            )
        if 'middle' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_MIDDLEDOWN | win32con.MOUSEEVENTF_MIDDLEUP,
                x, y, 0, 0
            )
        self.current_position = (x, y)

    def _click_win32gui(self, x: int, y: int) -> None:
        """使用 win32gui 点击"""
        pos = (x, y)
        handle = win32gui.WindowFromPoint(pos)
        client_pos = win32gui.ScreenToClient(handle, pos)
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])

        win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
        self.current_position = (x, y)

    def _click_ctypes(self, x: int, y: int) -> None:
        """使用 ctypes 点击"""
        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
        self.current_position = (x, y)

    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        key: str = 'left',
        method: str = 'ctypes'
    ) -> None:
        """
        鼠标点击

        Args:
            x: X 坐标，None 则使用当前位置
            y: Y 坐标，None 则使用当前位置
            key: 按键 ('left', 'right', 'middle')
            method: 实现方法 ('ctypes', 'win32con', 'win32gui')
        """
        if x is None and y is None:
            x, y = win32api.GetCursorPos()

        if method == 'win32con':
            self._click_win32con(x, y, key)
        elif method == 'win32gui':
            self._click_win32gui(x, y)
        elif method == 'ctypes':
            self._click_ctypes(x, y)

    def double_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        wait: float = 0.1
    ) -> None:
        """
        双击

        Args:
            x: X 坐标
            y: Y 坐标
            wait: 两次点击间隔（秒）
        """
        if x is None and y is None:
            x, y = win32api.GetCursorPos()

        self.click(x, y)
        time.sleep(wait)
        self.click(x, y)

    def right_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None
    ) -> None:
        """右键点击"""
        self.click(x, y, key='right')

    def middle_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None
    ) -> None:
        """中键点击"""
        self.click(x, y, key='middle')

    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        鼠标滚轮

        Args:
            amount: 滚动量，正数向上，负数向下
            x: X 坐标
            y: Y 坐标
        """
        if x is not None and y is not None:
            self.move_to(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, amount * 120, 0)

    @staticmethod
    def press_key(key: int, keyup: int = win32con.KEYEVENTF_KEYUP) -> None:
        """
        按键

        Args:
            key: 虚拟键码
            keyup: KEYEVENTF_KEYUP 标志
        """
        win32api.keybd_event(key, 0, 0, 0)
        win32api.keybd_event(key, 0, keyup, 0)

    @staticmethod
    def tap_key(key: int, times: int = 1, interval: float = 0.1) -> None:
        """
        按键（按下并释放）

        Args:
            key: 虚拟键码
            times: 按键次数
            interval: 按键间隔
        """
        for _ in range(times):
            win32api.keybd_event(key, 0, 0, 0)
            time.sleep(interval)
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def __repr__(self) -> str:
        return f"KeyMouseHand_WIN32(position={self.current_position})"


class KeyMouseHand_PUI:
    """
    跨平台键盘鼠标控制

    使用 PyUserInput 实现，支持 Windows/macOS/Linux。

    使用示例：
        hand = KeyMouseHand_PUI()
        hand.click(100, 200)
        hand.type('Hello')
    """

    def __init__(self):
        if not HAS_PYUSERINPUT:
            raise ImportError("PyUserInput not installed. Run: pip install PyUserInput")

        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.x_dim, self.y_dim = self.mouse.screen_size()
        self.current_position = self.mouse.position()

    def _keys(self, key: str) -> List:
        """解析按键字符串"""
        if key.lower().startswith('ctrl+'):
            return [self.keyboard.control_key, key[5:]]
        if key.lower().startswith('alt+'):
            return [self.keyboard.alt_key, key[4:]]
        if key.lower().startswith('shift+'):
            return [self.keyboard.shift_key, key[6:]]

        # F键
        if re.match(r'^f[0-9]{1,2}$', key.lower()):
            return [self.keyboard.function_keys[int(key[1:])]]

        # 数字小键盘
        if key.lower().startswith('num'):
            if key[3:].isdigit():
                return [self.keyboard.numpad_keys[int(key[3:])]]
            return [self.keyboard.numpad_keys[key[3:]]]

        return [key]

    def move_to(self, x: int, y: int) -> None:
        """移动鼠标"""
        self.mouse.move(x, y)
        self.current_position = (x, y)

    def press_mouse(self, x: int, y: int, duration: float = 1.0, button: int = 1) -> None:
        """
        按住鼠标

        Args:
            x: X 坐标
            y: Y 坐标
            duration: 持续时间
            button: 按键 (1=左, 2=右, 3=中)
        """
        self.mouse.press(x, y, button)
        time.sleep(duration)
        self.mouse.release(x, y, button)

    def click(self, x: int, y: int, button: int = 1) -> None:
        """
        鼠标点击

        Args:
            x: X 坐标
            y: Y 坐标
            button: 按键 (1=左, 2=右, 3=中)
        """
        self.mouse.click(x, y, button)
        self.current_position = (x, y)

    def double_click(self, x: int, y: int, button: int = 1) -> None:
        """双击"""
        self.mouse.click(x, y, button, n=2)

    def right_click(self, x: int, y: int) -> None:
        """右键点击"""
        self.click(x, y, button=2)

    def type(self, text: str) -> None:
        """
        输入文字

        Args:
            text: 要输入的文字
        """
        self.keyboard.type_string(text)

    def press_key(self, key: str) -> None:
        """按下按键"""
        return self.keyboard.press_keys(self._keys(key))

    def release_key(self, key: str) -> None:
        """释放按键"""
        return self.keyboard.release_key(self._keys(key)[0])

    def tap_key(self, key: str, times: int = 1, interval: float = 0.1) -> None:
        """
        按键（按下并释放）

        Args:
            key: 按键名称或键码
            times: 按键次数
            interval: 按键间隔
        """
        self.keyboard.tap_key(key, n=times, interval=interval)

    def tap_comb(self, key: str, times: int = 1, comb: str = 'ctrl') -> None:
        """
        组合键

        Args:
            key: 主键
            times: 按键次数
            comb: 组合键 ('ctrl', 'alt', 'shift')
        """
        comb_dict = {
            'ctrl': self.keyboard.control_key,
            'alt': self.keyboard.alt_key,
            'shift': self.keyboard.shift_key
        }
        comb_key = comb_dict.get(comb, comb)

        self.keyboard.press_key(comb_key)
        self.tap_key(key=key, times=times)
        self.keyboard.release_key(comb_key)

    def __repr__(self) -> str:
        return f"KeyMouseHand_PUI(position={self.current_position})"


# 默认使用 PyUserInput 版本（跨平台）
KeyMouseHand = KeyMouseHand_PUI if HAS_PYUSERINPUT else KeyMouseHand_WIN32


__all__ = ['KeyMouseHand', 'KeyMouseHand_WIN32', 'KeyMouseHand_PUI']


if __name__ == '__main__':
    # 测试
    print(f"Using: {KeyMouseHand.__name__}")

    hand = KeyMouseHand()
    print(f"Current position: {hand.current_position}")

    # 测试移动（取消注释运行）
    # hand.move_to(500, 500)
    # hand.click(500, 500)
