# -*- coding: utf-8 -*-
"""
desktop_eye - 桌面截图捕获

功能：
- 全屏截图
- 按窗口名称/句柄截图
- 保存截图到文件
- 列举所有窗口

依赖：
- pywin32 (win32gui, win32api, win32con)
- Pillow

使用示例：
    from eyes.desktop_eye import DesktopEye

    # 全屏截图
    desktop = DesktopEye()
    desktop.screenshot()

    # 按窗口名截图
    desktop.capture('记事本')

    # 列出所有窗口
    desktop.show_all_hwnd()
"""

from __future__ import annotations

import os
import time
from typing import Optional, Union, Dict, Tuple

import win32gui
import win32api
import win32con
from PIL import Image

from utils import PROJECT_PATH
from eyes.visual_residue import see_and_remember


class DesktopEye:
    """
    桌面截图捕获类

    提供全屏截图和窗口截图功能。

    Attributes:
        width: 虚拟屏幕宽度
        height: 虚拟屏幕高度
        position: 屏幕位置 (left, top, right, bottom)
    """

    desktop = win32gui.GetDesktopWindow()

    def __init__(self, debug: bool = False):
        """
        初始化桌面眼睛

        Args:
            debug: 是否开启调试模式
        """
        self.debug = debug
        self.project_path = str(PROJECT_PATH)

        # 获取虚拟屏幕尺寸
        self.width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.position = (self.left, self.top, self.right, self.bottom)

    @staticmethod
    def show_all_hwnd() -> Dict[int, str]:
        """
        显示所有可见窗口的句柄和标题

        Returns:
            窗口句柄到标题的映射字典
        """
        hwnd_title: Dict[int, str] = {}

        def get_all_hwnd(hwnd: int, mouse: Any) -> None:
            if (win32gui.IsWindow(hwnd)
                    and win32gui.IsWindowEnabled(hwnd)
                    and win32gui.IsWindowVisible(hwnd)):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(get_all_hwnd, 0)

        for h, t in hwnd_title.items():
            if t:
                print(f"{h}: {t}")

        return hwnd_title

    def save_fig(
        self,
        image: Image.Image,
        save_dir: Optional[str] = None,
        postfix: str = 'jpg',
        quality: int = 75
    ) -> str:
        """
        保存图像到文件

        Args:
            image: PIL Image 对象
            save_dir: 保存目录，默认为 CDMemory/pictures
            postfix: 文件格式 ('jpg' 或 'png')
            quality: 图像质量 (1-100，仅 jpg)

        Returns:
            保存的文件路径
        """
        form_dict = {
            'jpg': 'JPEG',
            'png': 'PNG'
        }

        if save_dir is None:
            save_dir = os.path.join(self.project_path, 'memory', 'pictures')

        os.makedirs(save_dir, exist_ok=True)

        file_path = 'screenshot_{}.{}'.format(
            time.strftime('%y%m%d_%H%M%S', time.localtime()), postfix)
        dump_path = os.path.join(save_dir, file_path)

        form = form_dict.get(postfix.lower(), 'JPEG')
        image.save(fp=dump_path, format=form, quality=quality)

        if self.debug:
            print(f'Saved screenshot to {dump_path}')

        return dump_path

    def load_fig(self, path: str) -> Tuple[Optional[Image.Image], bool]:
        """
        加载图像文件

        Args:
            path: 图像文件路径

        Returns:
            (Image 对象, 是否有效)
        """
        valid_flag = True
        try:
            image = Image.open(path)
            return image, valid_flag
        except Exception as e:
            valid_flag = False
            if self.debug:
                print(f'Failed to load image: {e}')
        return None, valid_flag

    def _get_screenshot(
        self,
        handle: int,
        method: str = 'window'
    ) -> str:
        """
        内部方法：获取截图

        Args:
            handle: 窗口句柄
            method: 'desktop' 或 'window'

        Returns:
            临时 BMP 文件路径
        """
        if method == 'desktop':
            left, top, right, bottom = self.position
            width, height = self.width, self.height
        else:
            left, top, right, bottom = win32gui.GetWindowRect(handle)
            width, height = right - left, bottom - top

        position_case = (left, top, right, bottom, width, height)
        tmp_path = see_and_remember(
            handle, position_case, remove_title_bar=False
        )
        return tmp_path

    def screenshot(
        self,
        save_dir: Optional[str] = None,
        postfix: str = 'jpg',
        quality: int = 75
    ) -> str:
        """
        全屏截图

        Args:
            save_dir: 保存目录
            postfix: 文件格式
            quality: 图像质量

        Returns:
            保存的文件路径
        """
        tmp_path = self._get_screenshot(self.desktop, method='desktop')
        image, valid_flag = self.load_fig(tmp_path)

        if not valid_flag or image is None:
            raise RuntimeError("Failed to capture screenshot")

        save_path = ""
        if postfix.lower() != 'bmp':
            save_path = self.save_fig(
                image=image,
                save_dir=save_dir,
                postfix=postfix,
                quality=quality
            )

        # 清理临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        return save_path

    def capture_by_handle(
        self,
        handle: Union[int, str],
        save_dir: Optional[str] = None,
        postfix: str = 'jpg'
    ) -> str:
        """
        按窗口句柄截图

        Args:
            handle: 窗口句柄或窗口名称
            save_dir: 保存目录
            postfix: 文件格式

        Returns:
            保存的文件路径
        """
        if not isinstance(handle, int):
            return self.capture_by_name(
                window_name=handle, save_dir=save_dir, postfix=postfix
            )

        tmp_path = self._get_screenshot(handle, method='window')
        image, valid_flag = self.load_fig(tmp_path)

        save_path = ""
        if postfix.lower() != 'bmp' and valid_flag and image:
            save_path = self.save_fig(
                image=image, save_dir=save_dir, postfix=postfix
            )

        # 清理临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        return save_path

    def capture_by_name(
        self,
        window_name: str,
        save_dir: Optional[str] = None,
        postfix: str = 'jpg'
    ) -> str:
        """
        按窗口名称截图

        Args:
            window_name: 窗口标题
            save_dir: 保存目录
            postfix: 文件格式

        Returns:
            保存的文件路径
        """
        handle = win32gui.FindWindow(None, window_name)
        return self.capture_by_handle(
            handle=handle, save_dir=save_dir, postfix=postfix
        )

    def capture(
        self,
        name_or_handle: Union[int, str],
        save_dir: Optional[str] = None,
        postfix: str = 'jpg'
    ) -> str:
        """
        按窗口名称或句柄截图（智能识别）

        Args:
            name_or_handle: 窗口名称或句柄
            save_dir: 保存目录
            postfix: 文件格式

        Returns:
            保存的文件路径
        """
        if isinstance(name_or_handle, int):
            return self.capture_by_handle(
                handle=name_or_handle, save_dir=save_dir, postfix=postfix
            )
        return self.capture_by_name(
            window_name=name_or_handle, save_dir=save_dir, postfix=postfix
        )

    def __call__(self, *args, **kwargs):
        return self.capture(*args, **kwargs)


__all__ = ['DesktopEye']


if __name__ == '__main__':
    de = DesktopEye(debug=True)

    # 显示所有窗口
    print("=== 可见窗口列表 ===")
    de.show_all_hwnd()

    # 截取记事本窗口（如果存在）
    # de.capture('记事本')

    # 全屏截图
    # de.screenshot()
