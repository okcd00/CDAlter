# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : MouseHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     :
# ==========================================================================
import time
import ctypes
import win32api
import win32con


class MouseHand(object):
    def __init__(self, ):
        self.current_position = (-1, -1)

    def move_to(self, x, y):
        self.current_position = (x, y)
        win32api.SetCursorPos([x, y])

    def click_win32con(self, x, y, key='left'):
        if 'left' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)
        if 'right' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)

    def click(self, x, y, key='left', method='win32con'):
        if method == 'win32con':
            self.click_win32con(x, y, key)
        elif method == 'ctypes':
            self.click_ctypes(x, y)

    def double_click(self, wait=0.1):
        self.click()
        time.sleep(wait)
        self.click()

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    mh = MouseHand()
    mh.double_click()
