# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : PAGHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2022-03-30
#   desc     : Control Keyboard and Mouse
#   require  : Windows - pyautogui
# ==========================================================================
import pyautogui
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


class PAGHand(object):
    # pyautogui is a strong tool library, few to re-implement
    # https://pyautogui.readthedocs.io/en/latest/
    def __init__(self, pic_path_case=None):
        self.screen_width, self.screen_height = pyautogui.size()
        self.current_x, self.current_y = pyautogui.position()
        self.keyboard_keys = pyautogui.KEYBOARD_KEYS
        
        # a dict to record pictures' path
        self.pic_path_case = {}
        if pic_path_case is not None:
            self.pic_path_case = pic_path_case
        
    def move(self, x, y):
        # self.current_x += x
        # self.current_y += y
        pyautogui.move(x, y)

    def move_to(self, x, y, duration=None):
        pyautogui.moveTo(
            x, y, duration=duration,
            tween=pyautogui.easeInOutQuad)
    
    def mouse_down(x=None, y=None, button='left'):
        pyautogui.mouseDown(
            x=x, y=y, button=button)
        
    def mouse_up(x=None, y=None, button='left'):
        pyautogui.mouseUp(
            x=x, y=y, button=button)

    def drag(self, x_offset, y_offset, duration=0.5):
        pyautogui.drag(x_offset, y_offset, duration)

    def drag_to(self, x_offset, y_offset, duration=0.5):
        pyautogui.dragTo(
            x_offset, y_offset, 
            duration=duration)

    def drag_in_sequence(self, offset_list, duration=0.5):
        for x_delta, y_delta in offset_list:
            pyautogui.drag(x_delta, y_delta, duration)

    def scroll(self, amount, x=None, y=None):
        pyautogui.scroll(
            amount_to_scroll=amount, x=x, y=y)

    def click(self, x, y, clicks=1, interval=None, button='left'):
        # button: left, right, middle
        pyautogui.click(
            x, y, clicks=clicks, interval=interval, button=button)
    
    def key_down(key):
        pyautogui.keyDown(key)
        
    def key_up(key):
        pyautogui.mouseUp(key)

    def press(self, key, hold=None):
        # key can be a list or a string
        if hold is not None:
            with pyautogui.hold(hold):
                pyautogui.press(key)
        else:
            pyautogui.press(key)

    def hot_key(self, *args):
        pyautogui.hotkey(*args)

    def write(self, text, interval=0.25):
        pyautogui.write(text, interval=interval)

    def type_write(self, key_list, interval=0.5):
        pyautogui.typewrite(key_list, interval=interval)

    def message_box(self, msg, msg_type='confirm'):
        # msg_type: alert/confirm/prompt
        # OK or Cancel
        return getattr(pyautogui, msg_type)(msg)

    def locate_pic(self, pic_key, pic_path=None, return_type='center'):
        if pic_path is not None:
            if return_type == 'center':
                return pyautogui.locateCenterOnScreen(pic_path)
            else:
                return pyautogui.locateOnScreen(pic_path)
        else:    
            if return_type == 'center':
                return pyautogui.locateCenterOnScreen(self.pic_path[pic_key])
            else:
                return pyautogui.locateOnScreen(self.pic_path[pic_key])

    def locate_pic_all(self, pic_key, pic_path=None):
        if pic_path is not None:
            return pyautogui.locateAllOnScreen(pic_path)
        else:    
            return pyautogui.locateAllOnScreen(self.pic_path[pic_key])

    def click_picture(self, pic_key, pic_path=None):
        if pic_path is not None:
            pyautogui.click(pic_path)
        else:    
            pyautogui.click(self.pic_path[pic_key])

    def screen_shot(dump_path=None):
        if dump_path:
            pyautogui.screenshot(dump_path)
        else:
            pyautogui.screenshot()

    
if __name__ == '__main__':
    pag = PAGHand()
    print(pag.message_box('test', 'confirm'))
