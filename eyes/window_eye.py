# -*- coding: utf-8 -*-
"""
window_eye - 窗口识别与控制

功能：
- 通过窗口名称或句柄获取窗口信息
- 控制窗口状态（激活、显示、隐藏）
- 获取窗口坐标、大小
- 枚举子窗口和菜单

依赖：
- pywin32 (win32gui, win32con)

使用示例：
    from eyes.window_eye import WindowEye

    # 通过名称获取窗口
    eye = WindowEye(window_name='记事本')
    print(eye.coordinate())  # (left, top, right, bottom)

    # 激活窗口
    eye.set_foreground()

    # 获取子窗口
    children = eye.get_child_windows()
"""

from __future__ import annotations

import time
from typing import Optional, List, Dict, Tuple, Any

import win32gui
import win32con


class WindowEye:
    """
    窗口识别与控制类

    用于获取窗口信息、控制窗口状态。

    Attributes:
        window_handle: 窗口句柄
        title: 窗口标题
        position: 窗口位置 (left, top, right, bottom)
        class_name: 窗口类名

    使用示例：
        eye = WindowEye(window_name='记事本')
        eye.set_foreground()
    """

    def __init__(
        self,
        window_name: Optional[str] = None,
        handle: Optional[int] = None,
        debug: bool = False
    ):
        """
        初始化窗口眼睛

        Args:
            window_name: 窗口标题（模糊匹配）
            handle: 窗口句柄（精确匹配）
            debug: 是否开启调试模式

        Note:
            window_name 和 handle 二选一，优先使用 handle
        """
        self.debug = debug
        self.window_handle: Optional[int] = handle

        if handle is None and window_name is not None:
            self.window_handle = win32gui.FindWindow(None, window_name)

        if self.window_handle is not None:
            self.title = win32gui.GetWindowText(self.window_handle)
            self.position = win32gui.GetWindowRect(self.window_handle)
            self.class_name = win32gui.GetClassName(self.window_handle)
        else:
            self.title = ""
            self.position = (0, 0, 0, 0)
            self.class_name = ""

    def coordinate(
        self,
        position: Optional[Tuple[int, int, int, int]] = None,
        return_type: str = 'dict'
    ) -> Dict[str, int] | Tuple[int, int, int, int]:
        """
        获取窗口坐标

        Args:
            position: 指定位置，默认使用窗口当前位置
            return_type: 返回类型 ('dict' 或 'tuple')

        Returns:
            窗口坐标，格式为 {'left': x, 'top': y, 'right': x2, 'bottom': y2}
            或 (left, top, right, bottom)
        """
        keys = ['left', 'top', 'right', 'bottom']

        if position is None:
            position = self.position

        if return_type == 'tuple':
            return position

        return dict(zip(keys, position))

    def size(
        self,
        position: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, int]:
        """
        获取窗口尺寸

        Args:
            position: 指定位置，默认使用窗口当前位置

        Returns:
            包含 height, width 和坐标信息的字典
        """
        attr = self.coordinate(position)
        size_dict = {
            'height': attr['bottom'] - attr['top'],
            'width': attr['right'] - attr['left']
        }
        size_dict.update(attr)
        return size_dict

    def get_child_windows(self, handle: Optional[int] = None) -> List[int]:
        """
        获取所有子窗口句柄

        Args:
            handle: 父窗口句柄，默认使用当前窗口

        Returns:
            子窗口句柄列表
        """
        if handle is None:
            handle = self.window_handle

        children_windows: List[int] = []

        def enum_callback(hwnd: int, param: List[int]) -> None:
            param.append(hwnd)

        win32gui.EnumChildWindows(handle, enum_callback, children_windows)
        return children_windows

    def get_menu_handle(self, handle: Optional[int] = None) -> int:
        """
        获取菜单句柄

        Args:
            handle: 窗口句柄，默认使用当前窗口

        Returns:
            菜单句柄
        """
        if handle is None:
            handle = self.window_handle
        return win32gui.GetMenu(handle)

    def get_sub_menu_handle(
        self,
        handle: Optional[int] = None,
        index: int = 0
    ) -> int:
        """
        获取子菜单句柄

        Args:
            handle: 菜单句柄，默认使用窗口主菜单
            index: 子菜单索引

        Returns:
            子菜单句柄
        """
        if handle is None:
            handle = self.window_handle
        return win32gui.GetSubMenu(handle, index)

    def set_foreground(self, handle: Optional[int] = None) -> None:
        """
        将窗口设置为前台活动窗口

        Args:
            handle: 窗口句柄，默认使用当前窗口
        """
        if handle is None:
            handle = self.window_handle
        win32gui.SetForegroundWindow(handle)

    def appear(self, handle: Optional[int] = None) -> None:
        """
        显示窗口（如果窗口最小化则恢复）

        Args:
            handle: 窗口句柄，默认使用当前窗口

        Note:
            窗口显示模式说明：
            - SW_HIDE (0): 隐藏窗口
            - SW_MAXIMIZE (3): 最大化
            - SW_MINIMIZE (6): 最小化
            - SW_RESTORE (9): 恢复
            - SW_SHOW (5): 显示
            - SW_SHOWNORMAL (1): 正常显示
        """
        if handle is None:
            handle = self.window_handle

        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
            time.sleep(0.5)

        self.position = self.coordinate(return_type='tuple')

    def minimize(self, handle: Optional[int] = None) -> None:
        """最小化窗口"""
        if handle is None:
            handle = self.window_handle
        win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)

    def maximize(self, handle: Optional[int] = None) -> None:
        """最大化窗口"""
        if handle is None:
            handle = self.window_handle
        win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)

    def hide(self, handle: Optional[int] = None) -> None:
        """隐藏窗口"""
        if handle is None:
            handle = self.window_handle
        win32gui.ShowWindow(handle, win32con.SW_HIDE)

    def close(self, handle: Optional[int] = None) -> None:
        """
        关闭窗口

        Args:
            handle: 窗口句柄，默认使用当前窗口
        """
        if handle is None:
            handle = self.window_handle
        win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

    def is_valid(self) -> bool:
        """检查窗口句柄是否有效"""
        if self.window_handle is None:
            return False
        return win32gui.IsWindow(self.window_handle)

    def is_visible(self) -> bool:
        """检查窗口是否可见"""
        if self.window_handle is None:
            return False
        return win32gui.IsWindowVisible(self.window_handle)

    def is_enabled(self) -> bool:
        """检查窗口是否可用"""
        if self.window_handle is None:
            return False
        return win32gui.IsWindowEnabled(self.window_handle)

    def __repr__(self) -> str:
        return f"WindowEye(handle={self.window_handle}, title='{self.title}')"

    def __str__(self) -> str:
        return f"Window: {self.title} [{self.window_handle}]"


__all__ = ['WindowEye']


if __name__ == '__main__':
    # 测试：列出所有可见窗口
    def enum_windows_callback(hwnd: int, windows: List[Tuple[int, str]]) -> None:
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))

    windows: List[Tuple[int, str]] = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    print("=== 可见窗口列表 ===")
    for hwnd, title in windows[:10]:
        print(f"  {hwnd}: {title}")

    # 测试窗口操作
    if windows:
        test_hwnd, test_title = windows[0]
        eye = WindowEye(handle=test_hwnd)
        print(f"\n窗口信息: {eye}")
        print(f"坐标: {eye.coordinate()}")
        print(f"尺寸: {eye.size()}")
