# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : WindowEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     :
# ==========================================================================
import win32gui
import win32con


class WindowEye(object):
    def __init__(self, window_name=None, handle=None, debug=False):
        self.window_handle = handle
        if (handle is None) and (window_name is not None):
            self.window_handle = win32gui.FindWindow(None, window_name)
            if debug:
                print("{} handle is {}".format(window_name, self.window_handle))
        self.title = win32gui.GetWindowText(self.window_handle)
        self.position = win32gui.GetWindowRect(self.window_handle)
        self.class_name = win32gui.GetClassName(self.window_handle)

    def coordinate(self, position=None):
        keys = ['left', 'top', 'right', 'bottom']
        if position is None:
            position = self.position
        return dict(zip(keys, position))

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
        win32gui.SetForegroundWindow(handle)

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    we = WindowEye(window_name=u'微信', debug=True)
    print(we.coordinate())
