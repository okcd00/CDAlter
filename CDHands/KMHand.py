# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : KMHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : Control Keyboard and Mouse with basic libraries
# ==========================================================================
import time
import ctypes
import win32api
import win32con
import win32gui


class KMHand(object):
    def __init__(self):
        self.current_position = win32api.GetCursorPos()

    def move_to(self, x, y):
        self.current_position = (x, y)
        win32api.SetCursorPos([x, y])

    def _click_win32con(self, x, y, key='left'):
        if 'left' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP |
                win32con.MOUSEEVENTF_LEFTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)
        if 'right' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_RIGHTUP |
                win32con.MOUSEEVENTF_RIGHTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)

    def _click_win32gui(self, x, y):
        pos = (x, y)
        handle = win32gui.WindowFromPoint(pos)
        client_pos = win32gui.ScreenToClient(handle, pos)
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
        self.current_position = (x, y)

    def _click_ctypes(self, x, y):
        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
        self.current_position = (x, y)

    def click(self, x=None, y=None, key='left', method='ctypes'):
        if x is None and y is None:
            x, y = win32api.GetCursorPos()
        if method == 'win32con':
            self._click_win32con(x, y, key)
        elif method == 'win32gui':
            self._click_win32gui(x, y)
        elif method == 'ctypes':
            self._click_ctypes(x, y)

    def double_click(self, x=None, y=None, wait=0.1):
        if x is None and y is None:
            x, y = win32api.GetCursorPos()
        self.click(x, y)
        time.sleep(wait)
        self.click(x, y)

    def sent_key(self):
        win32api.keybd_event(13, 0, 0, 0)
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    mh = KMHand()
    mh.double_click()
