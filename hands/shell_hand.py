# -*- coding: utf-8 -*-
"""
shell_hand - Shell 命令执行

功能：
- 打开程序/文件
- 执行 Shell 命令
- 执行命令脚本

依赖：
- pywin32 (win32api, win32con)

使用示例：
    from hands.shell_hand import ShellHand

    shell = ShellHand()

    # 打开程序
    shell.open('notepad.exe')

    # 用指定程序打开文件
    shell.open_with('README.md', 'notepad++.exe')

    # 执行命令
    shell.exec('echo Hello World')
"""

from __future__ import annotations

import os
from typing import Optional, List, Union

import win32api
import win32con


class ShellHand:
    """
    Shell 命令执行类

    提供程序打开和命令执行功能。

    Attributes:
        current_status: 最后一次执行的状态码
    """

    # 状态码映射
    STATUS_MESSAGES = {
        0: '内存不足',
        2: '文件未找到',
        3: '路径无效',
        11: 'EXE 文件无效',
        26: '无法共享',
        27: '文件名关联不完整或无效',
        28: '超时',
        29: 'DDE 事务失败',
        30: '正在处理其他 DDE 事务',
        31: '没有关联的应用程序',
        32: '找不到动态链接库',
        33: '应用程序不适合当前环境',
    }

    def __init__(self):
        self.current_status: int = -1

    def open_with(
        self,
        file_path: str,
        program_path: Optional[str] = None
    ) -> int:
        """
        用指定程序打开文件

        Args:
            file_path: 文件路径
            program_path: 程序路径，None 则使用系统默认

        Returns:
            状态码 (>= 32 表示成功)

        使用示例：
            shell.open_with('README.md', 'notepad++.exe')
        """
        self.current_status = win32api.ShellExecute(
            1,                    # 父窗口句柄
            'open',               # 操作类型
            r'{}'.format(program_path or ''),
            r'{}'.format(file_path),
            '',                   # 默认目录
            win32con.SW_SHOWNORMAL
        )
        return self.current_status

    def open(self, program_path: str) -> int:
        """
        打开程序

        Args:
            program_path: 程序路径

        Returns:
            状态码

        使用示例：
            shell.open('notepad.exe')
        """
        self.current_status = self.open_with(
            file_path='',
            program_path=program_path
        )
        return self.current_status

    def exec(self, text: Union[str, List[str]]) -> List[str]:
        """
        执行命令

        Args:
            text: 命令文本，可以是：
                - 文件路径：读取文件中的命令
                - 字符串：按行分割执行
                - 列表：直接执行

        Returns:
            执行的命令列表

        使用示例：
            shell.exec('echo Hello')
            shell.exec(['echo Hello', 'echo World'])
        """
        if not isinstance(text, list):
            if os.path.exists(text):
                with open(text, 'r', encoding='utf-8') as f:
                    text = [line.strip() for line in f]
            else:
                text = [line.strip() for line in text.split('\n')]

        # 过滤注释行
        text = [line for line in text if line and not line.startswith('#')]

        for line in text:
            os.system(line)

        return text

    def show_status(self) -> str:
        """
        显示当前状态信息

        Returns:
            状态信息字符串
        """
        return self.STATUS_MESSAGES.get(
            self.current_status,
            f'未知状态 ({self.current_status})'
        )

    def is_success(self) -> bool:
        """
        检查最后一次操作是否成功

        Returns:
            True 表示成功
        """
        return self.current_status >= 32

    def __repr__(self) -> str:
        status = self.show_status()
        return f'<ShellHand status="{status}">'

    def __str__(self) -> str:
        return self.show_status()


__all__ = ['ShellHand']


if __name__ == '__main__':
    sh = ShellHand()

    # 测试打开记事本
    print("Opening notepad...")
    sh.open('notepad.exe')
    print(f"Status: {sh.show_status()}")
    print(f"Success: {sh.is_success()}")
