# -*- coding: utf-8 -*-
"""
utils - 工具函数模块

本模块提供全局工具函数和基础配置。

模块组成：
- atc.py: 数字转中文工具 (Arabic To Chinese)
- pinyin_utils.py: 拼音转换工具

使用示例：
    from utils import PROJECT_PATH
    from utils.atc import num2chinese
    from utils.pinyin_utils import PinyinUtils

    # 数字转中文
    chinese = num2chinese(12345)  # "一万二千三百四十五"

    # 拼音转换
    pu = PinyinUtils()
    pinyin = pu.to_pinyin("你好")  # ['ni', 'hao']
"""

from __future__ import annotations

import os
from pathlib import Path

# 项目根目录路径
PROJECT_PATH = Path(__file__).parent.parent.resolve()

# 为了兼容旧代码，同时提供字符串形式
PROJECT_PATH_STR = str(PROJECT_PATH)

__all__ = [
    'PROJECT_PATH',
    'PROJECT_PATH_STR',
]

if __name__ == '__main__':
    print(f"PROJECT_PATH: {PROJECT_PATH}")
