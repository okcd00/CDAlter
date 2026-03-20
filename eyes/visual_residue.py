# -*- coding: utf-8 -*-
"""
visual_residue - 视觉记忆（截图缓存）

功能：
- 将屏幕内容捕获到内存
- 保存为临时 BMP 文件
- 提供时间戳标识

依赖：
- pywin32 (win32gui, win32ui, win32con)

使用示例：
    from eyes.visual_residue import see_and_remember

    # 捕获窗口
    handle = win32gui.FindWindow(None, '记事本')
    tmp_path = see_and_remember(handle)
    # tmp_path 是 BMP 文件路径
"""

from __future__ import annotations

import os
import random
import datetime
from typing import Optional, Tuple

import win32ui
import win32gui
import win32con
from ctypes import windll

from utils import PROJECT_PATH


def time_identifier(add_postfix: bool = True) -> str:
    """
    生成基于时间戳的唯一标识符

    Args:
        add_postfix: 是否添加 .bmp 后缀

    Returns:
        唯一标识符字符串
    """
    time_stamp = '{0:%m%d%H%M%S%f}'.format(datetime.datetime.now())[::-1]
    mask = map(
        lambda x: chr(ord(x[0]) + ord(x[1])),
        zip(time_stamp[::2], time_stamp[1::2])
    )
    t_id = ''.join(mask) + ''.join([str(random.randint(1, 10)) for _ in range(2)])
    return t_id + ('.bmp' if add_postfix else '')


def see_and_remember(
    handle: int,
    position_case: Optional[Tuple[int, int, int, int, int, int]] = None,
    remove_title_bar: bool = True,
    dir_path: Optional[str] = None,
    debug: bool = False
) -> str:
    """
    捕获窗口内容并保存为 BMP 文件

    Args:
        handle: 窗口句柄
        position_case: 位置信息 (left, top, right, bottom, width, height)
        remove_title_bar: 是否移除标题栏
        dir_path: 保存目录，默认为 memory/pictures
        debug: 是否开启调试模式

    Returns:
        BMP 文件路径

    使用示例：
        handle = win32gui.FindWindow(None, '记事本')
        tmp_path = see_and_remember(handle)
    """
    # 获取窗口位置和尺寸
    if position_case:
        left, top, right, bottom, width, height = position_case
    else:
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        width, height = right - left, bottom - top

    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(handle)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 截图至内存设备描述表
    remove_title_bar_flag = int(remove_title_bar)
    mem_dc.BitBlt(
        (0, 0), (width, height),
        img_dc, (0, 0), win32con.SRCCOPY
    )

    # 使用 PrintWindow 获取窗口内容（包括被遮挡的部分）
    result = windll.user32.PrintWindow(
        handle, mem_dc.GetSafeHdc(), remove_title_bar_flag
    )

    if debug:
        print(f'mem_dc.GetSafeHdc: {result}')

    # 确定保存路径
    if dir_path is None:
        dir_path = os.path.join(str(PROJECT_PATH), 'memory', 'pictures')

    os.makedirs(dir_path, exist_ok=True)
    tmp_path = os.path.join(dir_path, time_identifier())

    if debug:
        print(f'Save screenshot to {tmp_path}')

    # 保存位图文件
    screenshot.SaveBitmapFile(mem_dc, tmp_path)

    # 释放资源
    win32gui.DeleteObject(screenshot.GetHandle())
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(handle, desktop_dc)

    return tmp_path


__all__ = ['see_and_remember', 'time_identifier']


if __name__ == '__main__':
    # 测试：列出所有窗口并截图第一个可见窗口
    def enum_callback(hwnd: int, windows: list) -> None:
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))

    windows = []
    win32gui.EnumWindows(enum_callback, windows)

    if windows:
        handle, title = windows[0]
        print(f"Capturing: {title}")
        path = see_and_remember(handle, debug=True)
        print(f"Saved to: {path}")
