# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : ShellHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-20
#   desc     :
# ==========================================================================
import os
import win32api
import win32con


class ShellHand(object):
    def __init__(self, ):
        self.current_status = -1

    def open_with(self, file_path, program_path=None):
        self.current_status = win32api.ShellExecute(
            1,  # handle for father window
            'open',  # action in {"edit", "explore", "open", "find", "print", "NULL"}
            r'{}'.format(program_path),  # file_name
            r'{}'.format(file_path),  # parameters, such as '-perfectworld'
            '',  # default dir
            win32con.SW_SHOWNORMAL  # show command in {}
        )
        return self.current_status

    def open(self, program_path):
        self.current_status = self.open_with(
            file_path='',
            program_path=program_path)
        return self.current_status

    def exec(self, text):
        if not isinstance(text, list):
            if os.path.exists(text):
                file_path = text
                text = [line.strip() for line in open(file_path, 'r')]
            else:
                text = [line.strip() for line in text.split()]
        text = [line.strip() for line in text if not line.startswith('#')]
        for line in text:
            os.system(line)
        return text

    def show_status(self):
        status_dict = {
            0: '内存不足',
            2: '文件名错误',
            3: '路径名错误',
            11: 'EXE文件无效',
            26: '发生共享错误',
            27: '文件名不完全或无效',
            28: '超时',
            29: 'DDE事务失败',
            30: '正在处理其他DDE事务而不能完成该DDE事务',
            31: '没有相关联的应用程序'
        }
        return status_dict.get(self.current_status, '正常')

    def __repr__(self):
        _st = self.show_status()
        return u'<CD ShellHand Instance> with status [{}]'.format(_st)

    def __str__(self):
        pass


if __name__ == '__main__':
    sh = ShellHand()
    sh.open('C:\\ProgramData\\Anaconda3\\python.exe')
    sh.open_with('README.md', 'notepad++.exe')
