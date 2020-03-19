# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : ReadEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-03-19
#   desc     : Read contents in some common kinds of files
# ==========================================================================
import os
import json
import yaml
import glob
import pickle
import multiprocessing
from pathlib import Path
from copy import deepcopy
from utils import PROJECT_PATH


class ReadEye(object):
    n_threads = 10
    project_path = PROJECT_PATH
    example_data = range(65536)  # example data

    def __init__(self, debug=False):
        self.debug = debug
        self.batch_size = 5 * 200
        self.loader_dict = [0] * self.n_threads
        self.data_case = deepcopy(self.example_data)

    def example_data_loader(self, i):
        self.loader_dict[i] = 1  # record when it starts
        return i, 'container_{}'.format(i)

    def example_target_func(self, i, name=None):
        print('Run child process %s (%s)' % (name, os.getpid()))
        left_pivot = i * self.batch_size
        right_pivot = (i + 1) * self.batch_size
        return self.data_case[left_pivot: right_pivot]

    def _read_by_postfix(self, file_path, postfix, load_method='rb', inplace=True):

        def _bs(_f):  # basic_stream
            return open(_f, load_method)

        loading_methods = {  # alphabet
            'dir': lambda d: list(glob.glob('{}/*.*'.format(d))),
            'json': lambda f: json.load(_bs(f)),
            'pkl': lambda f: pickle.load(_bs(f)),
            'txt': lambda f: [line.strip() for line in _bs(f)],
            'yml': lambda f: yaml.load(_bs(f)),
        }
        load_func = loading_methods.get(postfix, loading_methods['txt'])
        return_data = load_func(file_path)
        if inplace:
            self.data_case = return_data
        return return_data

    def read(self, file_path):
        if Path.is_dir(file_path):
            postfix = 'dir'  # return a list of files in this dir
        elif not Path.is_file(file_path):
            print('{} is not a file'.format(file_path))
            return None  # Invalid input
        else:  # the most common situation, return contents in file
            postfix = str(file_path).split('.')[-1].lower()
        data = self._read_by_postfix(
            file_path=file_path, postfix=postfix)
        return data

    def run_multiprocess(self, target_func=None, data_loader=None):
        print('Run the main process (%s).' % (os.getpid()))
        if target_func is None:
            target_func = self.example_target_func
        if data_loader is None:
            data_loader = self.example_data_loader
        for i in range(self.n_threads):
            p = multiprocessing.Process(
                target=target_func,
                args=data_loader(i) if data_loader else (i,))
            p.start()
        print('Waiting for all sub-processes done ...')

    def __str__(self):
        return """{}""".format(self.__repr__())

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    re = ReadEye()
    print(re)
