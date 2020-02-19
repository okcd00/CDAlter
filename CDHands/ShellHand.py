# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : ShellHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-20
#   desc     :
# ==========================================================================
import win32api
import win32con

class ShellHand(object):
    def __init__(self, ):
        self.current_status = -1
        self.current_position = (-1, -1)

    def open(self, file_path):
        self.current_status = win32api.ShellExecute(
            1,  # handle for father window
            'open',  # action in {"edit", "explore", "open", "find", "print", "NULL"}
            r'{}'.format(file_path),  # file_name
            '',  # parameters, such as '-perfectworld'
            '',  # default dir
            win32con.SW_SHOWNORMAL  # show command in {}
        )

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
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    sh = ShellHand()
    sh.open('C:\\ProgramData\\Anaconda3\\python.exe')
