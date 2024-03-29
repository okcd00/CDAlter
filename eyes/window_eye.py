# -*- coding: utf8 -*-
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
import win32con


class WindowEye(object):
    def __init__(self, window_name=None, handle=None, debug=False):
        self.debug = debug
        self.window_handle = handle
        if (handle is None) and (window_name is not None):
            self.window_handle = win32gui.FindWindow(
                None, window_name)
        if self.window_handle is not None:
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
        # SW_HIDE：隐藏窗口并激活其他窗口。nCmdShow=0。
        # SW_MAXIMIZE：最大化指定的窗口。nCmdShow=3。
        # SW_MINIMIZE：最小化指定的窗口并且激活在Z序中的下一个顶层窗口。nCmdShow=6。
        # SW_RESTORE：激活并显示窗口。如果窗口最小化或最大化，则系统将窗口恢复到原来的尺寸和位置。
            在恢复最小化窗口时，应用程序应该指定这个标志。nCmdShow=9。
        # SW_SHOW：在窗口原来的位置以原来的尺寸激活和显示窗口。nCmdShow=5。
        # SW_SHOWDEFAULT：依据在STARTUPINFO结构中指定的SW_FLAG标志设定显示状态，
            STARTUPINFO 结构是由启动应用程序的程序传递给CreateProcess函数的。nCmdShow=10。
        # SW_SHOWMAXIMIZED：激活窗口并将其最大化。nCmdShow=3。
        # SW_SHOWMINIMIZED：激活窗口并将其最小化。nCmdShow=2。
        # SW_SHOWMINNOACTIVE：窗口最小化，激活窗口仍然维持激活状态。nCmdShow=7。
        # SW_SHOWNA：以窗口原来的状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=8。
        # SW_SHOWNOACTIVATE：以窗口最近一次的大小和状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=4。
        # SW_SHOWNORMAL：激活并显示一个窗口。如果窗口被最小化或最大化，系统将其恢复到原来的尺寸和大小。
            应用程序在第一次显示窗口的时候应该指定此标志。nCmdShow=1。
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
    # we = WindowEye(window_name=u'最终幻想XIV', debug=False)
    we = WindowEye(window_name=u'*new 1 - Notepad++', debug=True)
    print(we.coordinate())
    we.set_foreground()