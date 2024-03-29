# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : KeyMouseHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc1    : Control Keyboard and Mouse with basic libraries (win32)
#   require  : 
#   desc2    : Control Keyboard and Mouse with PyUserInput (PyUserInput>=0.1.11)
#   require  : Linux - Xlib (python-xlib) / Mac - Quartz, AppKit / Windows - pywin32, pyHook
# ==========================================================================
import re
import time
import ctypes
import win32api
import win32con
import win32gui
from pymouse import PyMouse
from pykeyboard import PyKeyboard


class KeyMouseHand_WIN32(object):
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

    @staticmethod
    def sent_key(key=None):
        if key is None:
            key = win32con.KEYEVENTF_KEYUP
        win32api.keybd_event(13, 0, 0, 0)
        win32api.keybd_event(13, 0, key, 0)

    def __repr__(self):
        pass

    def __str__(self):
        pass


class KeyMouseHand_PUI(object):
    mouse = PyMouse()
    keyboard = PyKeyboard()

    def __init__(self):
        self.x_dim, self.y_dim = self.mouse.screen_size()

    def _keys(self, key):
        if key.lower().startswith('ctrl+'):
            return [self.keyboard.control_key, key[5:]]
        if key.lower().startswith('alt+'):
            return [self.keyboard.alt_key, key[4:]]
        if re.match('^f[0-9]{1,2}$', key.lower()):
            return [self.keyboard.function_keys[int(key[1:])]]
        if key.lower().startswith('num'):
            if key[3:].isdigit():
                return [self.keyboard.numpad_keys[int(key[3:])]]
            return [self.keyboard.numpad_keys[key[3:]]]
        return [key]

    def click(self, x, y, key=1):
        self.mouse.click(x, y, key)

    def double_click(self, x, y, key=1):
        self.mouse.click(x, y, key, n=2)

    def type(self, text):
        self.keyboard.type_string(text)

    def press_key(self, key):
        return self.keyboard.press_keys(self._keys(key))

    def release_key(self, key):
        return self.keyboard.release_key(key)

    def tap_key(self, key, times=1, interval=1):
        # press and release
        self.keyboard.tap_key(key, n=times, interval=interval)

    def tap_comb(self, key, times=1, comb='ctrl'):
        comb_dict = {
            'ctrl': self.keyboard.control_key,
            'alt': self.keyboard.alt_key,
            'shift': self.keyboard.shift_key
        }
        comb = comb_dict.get(comb, comb)
        self.press_key(comb)
        self.tap_key(key=key, times=times)
        self.press_key(comb)


# KeyMouseHand = KeyMouseHand_WIN32
KeyMouseHand = KeyMouseHand_PUI


if __name__ == '__main__':
    # Windows System
    mh = KeyMouseHand()
    mh.double_click()
    mh.keyboard.press_keys(['d'])
