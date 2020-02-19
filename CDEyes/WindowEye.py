# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : WindowEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     :
# ==========================================================================
import time
import win32gui
import win32api
import win32con


class WindowEye(object):
    def __init__(self, window_name=None, handle=None, debug=False):
        self.window_handle = handle
        if (handle is None) and (window_name is not None):
            self.window_handle = win32gui.FindWindow(
                None, window_name)
            if debug:
                print("{} handle is {}".format(window_name, self.window_handle))
        self.title = win32gui.GetWindowText(self.window_handle)
        self.position = win32gui.GetWindowRect(self.window_handle)
        self.class_name = win32gui.GetClassName(self.window_handle)

    def coordinate(self, position=None, return_type='dict'):
        keys = ['left', 'top', 'right', 'bottom']
        if position is None:
            position = self.position
        if return_type == 'tuple':
            return position
        return dict(zip(keys, position))

    def size(self, position=None):
        attr = self.coordinate(position)
        size_dict = {
            'height': attr['bottom'] - attr['top'],
            'width': attr['right'] - attr['left']}
        size_dict.update(attr)
        return size_dict

    def get_child_windows(self, handle=None):
        if handle is None:
            handle = self.window_handle
        children_windows = []
        win32gui.EnumChildWindows(
            handle, lambda hwnd, param: param.append(hwnd),
            children_windows)
        return children_windows

    def get_menu_handle(self, handle=None):
        if handle is None:
            handle = self.window_handle
        menu_handle = win32gui.GetMenu(handle)
        return menu_handle

    def get_sub_menu_handle(self, handle=None, index=0):
        if handle is None:
            handle = self.window_handle
        sub_menu_handle = win32gui.GetSubMenu(handle, index)
        return sub_menu_handle

    def set_foreground(self, handle=None):
        if handle is None:
            handle = self.window_handle
        # win32api.keybd_event(13, 0, 0, 0)  # send an enter
        win32gui.SetForegroundWindow(handle)

    def appear(self, handle=None):
        """
        # SW_HIDE�����ش��ڲ������������ڡ�nCmdShow=0��
        # SW_MAXIMIZE�����ָ���Ĵ��ڡ�nCmdShow=3��
        # SW_MINIMIZE����С��ָ���Ĵ��ڲ��Ҽ�����Z���е���һ�����㴰�ڡ�nCmdShow=6��
        # SW_RESTORE�������ʾ���ڡ����������С������󻯣���ϵͳ�����ڻָ���ԭ���ĳߴ��λ�á�
            �ڻָ���С������ʱ��Ӧ�ó���Ӧ��ָ�������־��nCmdShow=9��
        # SW_SHOW���ڴ���ԭ����λ����ԭ���ĳߴ缤�����ʾ���ڡ�nCmdShow=5��
        # SW_SHOWDEFAULT��������STARTUPINFO�ṹ��ָ����SW_FLAG��־�趨��ʾ״̬��
            STARTUPINFO �ṹ��������Ӧ�ó���ĳ��򴫵ݸ�CreateProcess�����ġ�nCmdShow=10��
        # SW_SHOWMAXIMIZED������ڲ�������󻯡�nCmdShow=3��
        # SW_SHOWMINIMIZED������ڲ�������С����nCmdShow=2��
        # SW_SHOWMINNOACTIVE��������С�����������Ȼά�ּ���״̬��nCmdShow=7��
        # SW_SHOWNA���Դ���ԭ����״̬��ʾ���ڡ��������Ȼά�ּ���״̬��nCmdShow=8��
        # SW_SHOWNOACTIVATE���Դ������һ�εĴ�С��״̬��ʾ���ڡ��������Ȼά�ּ���״̬��nCmdShow=4��
        # SW_SHOWNORMAL�������ʾһ�����ڡ�������ڱ���С������󻯣�ϵͳ����ָ���ԭ���ĳߴ�ʹ�С��
            Ӧ�ó����ڵ�һ����ʾ���ڵ�ʱ��Ӧ��ָ���˱�־��nCmdShow=1��
        """
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
            time.sleep(0.5)
        self.position = self.coordinate(return_type='tuple')

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    # we = WindowEye(window_name=u'���ջ���XIV', debug=False)
    we = WindowEye(window_name=u'΢��', debug=True)
    print(we.coordinate())
    we.set_foreground()

