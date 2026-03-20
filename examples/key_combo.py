# coding: utf-8
# ==========================================================================
#   Copyright (C) since 2026 All rights reserved.
#
#   filename : key_combo.py
#   author   : chendian / okcd00@qq.com
#   date     : 2026/01/20 04:51:39
#   desc     : 
#              
# ==========================================================================
import time
from pynput import keyboard, mouse

kbd = keyboard.Controller()
mouse_ctl = mouse.Controller()

import win32api
import win32con
import time

def press_f1():
    win32api.keybd_event(win32con.VK_F1, 0, 0, 0)      # 按下
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_F1, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放

def press_esc():
    win32api.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)

def click_mouse(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == 'a':
            print("Detected 'a' - triggering actions...")

            # 1. 模拟 F1
            # kbd.press(keyboard.Key.f1)
            # kbd.release(keyboard.Key.f1)
            press_f1()
            print("F1 pressed")
            time.sleep(0.05)

            # 2. 模拟 ESC
            # kbd.press(keyboard.Key.esc)
            # kbd.release(keyboard.Key.esc)
            press_esc()
            print("ESC pressed")
            time.sleep(0.25)

            # 3. 验证坐标有效性
            screen_width, screen_height = 2560, 1440  # 替换为你的实际分辨率
            x, y = int(2240*1080/1440), int(1161*1080/1440)
            if x >= screen_width or y >= screen_height:
                print(f"⚠️ 坐标 ({x}, {y}) 超出屏幕范围 ({screen_width}x{screen_height})")
                return

            # 4. 移动鼠标并点击
            mouse_ctl.position = (x, y)
            print(f"Mouse moved to ({x}, {y})")
            time.sleep(0.1)  # 确保移动完成
            # mouse_ctl.click(mouse.Button.left, 1)
            click_mouse(x, y)
            print("Mouse clicked")

            print("✅ All actions completed")

    except Exception as e:
        print(f"❌ Error during actions: {e}")

def on_release(key):
    if hasattr(key, 'char') and key.char == 'b':
        print("Exiting listener...")
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listener started. Press 'a' to trigger actions, 'b' to exit.")
    listener.join()