# coding: utf-8
# ==========================================================================
#   Copyright (C) since 2025 All rights reserved.
#
#   filename : jump_game.py
#   author   : chendian / okcd00@qq.com
#   date     : 2025/12/25 22:46:10
#   desc     : 
#              
# ==========================================================================

import os, sys, time, json

from pymouse import PyMouse
from pynput import keyboard
import math

mouse = PyMouse()

coordinates = {
    "src_x": 0,
    "src_y": 0,
    "dest_x": 0,
    "dest_y": 0,
}

def on_press(key):
    try:
        if key.char == 'a':
            x, y = mouse.position()
            print(f"{x=}, {y=}")

            coordinates['src_x'] = x
            coordinates['src_y'] = y

        if key.char == 'b':
            x, y = mouse.position()
            print(f"{x=}, {y=}")

            coordinates['dest_x'] = x
            coordinates['dest_y'] = y

            dist = math.sqrt( ( coordinates['dest_x']-coordinates['src_x'])**2 + ( coordinates['dest_y']-coordinates['src_y'])**2 )
            duration = dist * 0.0033
            print(f"[{dist}] {duration=}")

            mouse.press(x, y, 1)
            time.sleep(duration)
            mouse.release(x, y, 1)

    except AttributeError as e:
        print(e)
        pass 

def on_release(key):
    if key == keyboard.Key.esc: 
        return False 
    
if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
