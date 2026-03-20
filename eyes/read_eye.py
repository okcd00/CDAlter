# -*- coding: utf-8 -*-
"""
read_eye - 文件读取工具

功能：
- 读取多种格式文件 (txt, json, yaml, pkl)
- 支持目录遍历
- 多进程并行读取

依赖：
- PyYAML

使用示例：
    from eyes.read_eye import ReadEye

    reader = ReadEye()

    # 读取 JSON 文件
    data = reader.read('data.json')

    # 读取目录下的所有文件
    files = reader.read('./data_dir')
"""

from __future__ import annotations

import os
import json
import yaml
import glob
import pickle
import multiprocessing
from pathlib import Path
from copy import deepcopy
from typing import Any, Optional, List, Dict, Callable, Union

from utils import PROJECT_PATH


class ReadEye:
    """
    文件读取工具类

    支持多种文件格式的读取，并提供多进程并行读取能力。

    Attributes:
        project_path: 项目路径
        n_threads: 线程数
    """

    n_threads = 10
    project_path = str(PROJECT_PATH)
    example_data = range(65536)

    def __init__(self, debug: bool = False):
        """
        初始化读取眼睛

        Args:
            debug: 是否开启调试模式
        """
        self.debug = debug
        self.batch_size = 5 * 200
        self.loader_dict = [0] * self.n_threads
        self.data_case = deepcopy(self.example_data)

    def example_data_loader(self, i: int) -> Tuple[int, str]:
        """
        示例数据加载器

        Args:
            i: 线程索引

        Returns:
            (索引, 容器名称)
        """
        self.loader_dict[i] = 1
        return i, f'container_{i}'

    def example_target_func(
        self,
        i: int,
        name: Optional[str] = None
    ) -> List[int]:
        """
        示例目标函数

        Args:
            i: 线程索引
            name: 进程名称

        Returns:
            数据切片
        """
        if name:
            print(f'Run child process {name} ({os.getpid()})')

        left_pivot = i * self.batch_size
        right_pivot = (i + 1) * self.batch_size
        return list(self.data_case[left_pivot:right_pivot])

    def _read_by_postfix(
        self,
        file_path: Union[str, Path],
        postfix: str,
        load_method: str = 'rb',
        inplace: bool = True
    ) -> Any:
        """
        根据后缀读取文件

        Args:
            file_path: 文件路径
            postfix: 文件后缀
            load_method: 读取模式
            inplace: 是否更新内部数据

        Returns:
            文件内容
        """

        def _bs(_f: str) -> Any:
            return open(_f, load_method)

        loading_methods = {
            'dir': lambda d: list(glob.glob(f'{d}/*.*')),
            'json': lambda f: json.load(_bs(f)),
            'pkl': lambda f: pickle.load(_bs(f)),
            'txt': lambda f: [line.strip() for line in open(f, 'r', encoding='utf-8')],
            'yml': lambda f: yaml.load(_bs(f), Loader=yaml.SafeLoader),
            'yaml': lambda f: yaml.load(_bs(f), Loader=yaml.SafeLoader),
        }

        load_func = loading_methods.get(
            postfix,
            loading_methods['txt']
        )

        return_data = load_func(str(file_path))

        if inplace:
            self.data_case = return_data

        return return_data

    def read(self, file_path: Union[str, Path]) -> Any:
        """
        读取文件

        Args:
            file_path: 文件路径

        Returns:
            文件内容

        Note:
            支持的文件格式：
            - .txt: 文本文件，返回行列表
            - .json: JSON 文件，返回字典/列表
            - .yaml/.yml: YAML 文件，返回字典
            - .pkl: Pickle 文件，返回任意对象
            - 目录: 返回文件列表
        """
        file_path = Path(file_path)

        if file_path.is_dir():
            postfix = 'dir'
        elif not file_path.exists():
            print(f'{file_path} is not a file')
            return None
        else:
            postfix = str(file_path.suffix).lower().lstrip('.')

        data = self._read_by_postfix(
            file_path=file_path,
            postfix=postfix
        )
        return data

    def run_multiprocess(
        self,
        target_func: Optional[Callable] = None,
        data_loader: Optional[Callable] = None
    ) -> None:
        """
        运行多进程任务

        Args:
            target_func: 目标函数
            data_loader: 数据加载器
        """
        print(f'Run the main process ({os.getpid()}).')

        if target_func is None:
            target_func = self.example_target_func
        if data_loader is None:
            data_loader = self.example_data_loader

        for i in range(self.n_threads):
            p = multiprocessing.Process(
                target=target_func,
                args=data_loader(i) if data_loader else (i,)
            )
            p.start()

        print('Waiting for all sub-processes done ...')

    def __str__(self) -> str:
        return f"ReadEye(n_threads={self.n_threads})"

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, *args, **kwargs) -> Any:
        return self.read(*args, **kwargs)


__all__ = ['ReadEye']


if __name__ == '__main__':
    reader = ReadEye()
    print(reader)

    # 测试读取当前目录
    # files = reader.read('.')
    # print(f"Files: {files[:5]}")
