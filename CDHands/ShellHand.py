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
            0: '�ڴ治��',
            2: '�ļ�������',
            3: '·��������',
            11: 'EXE�ļ���Ч',
            26: '�����������',
            27: '�ļ�������ȫ����Ч',
            28: '��ʱ',
            29: 'DDE����ʧ��',
            30: '���ڴ�������DDE�����������ɸ�DDE����',
            31: 'û���������Ӧ�ó���'
        }
        return status_dict.get(self.current_status, '����')

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    sh = ShellHand()
    sh.open('C:\\ProgramData\\Anaconda3\\python.exe')
