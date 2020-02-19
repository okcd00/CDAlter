# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : PUIHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : Control Keyboard and Mouse with PyUserInput
#   require  : Linux - Xlib (python-xlib) / Mac - Quartz, AppKit / Windows - pywin32, pyHook
# ==========================================================================
import re
from pymouse import PyMouse
from pykeyboard import PyKeyboard


class PUIHand(object):
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

    def type(self, text):
        self.keyboard.type_string(text)

    def press_key(self, key):
        return self.keyboard.press_keys(self._keys(key))

    def release_key(self, key):
        return self.keyboard.release_key(key)

    def tap_key(self, key, times=1, interval=1):
        # 按住并松开，tap一个键
        self.keyboard.tap_key(key, n=times, interval=interval)

    def tap_comb(self, key, times, comb='ctrl'):
        comb_dict = {
            'ctrl': self.keyboard.control_key,
            'alt': self.keyboard.alt_key,
            'shift': self.keyboard.shift_key
        }
        comb = comb_dict.get(comb, comb)
        self.press_key(comb)
        self.tap_key(key=key, times=times)
        self.press_key(comb)


if __name__ == '__main__':
    # Windows系统
    ph = PUIHand()
    ph.keyboard.press_keys(['d'])
