# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : DesktopEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : it needs package Pillow (olefile>=0.46)
# ==========================================================================
import os
import sys
import time
sys.path.append('./')
sys.path.append('../')

# main packages
import win32gui
import win32api
import win32con
from PIL import Image
from utils import PROJECT_PATH
from CDEyes.visual_residue import see_and_remember


class DesktopEye(object):
    desktop = win32gui.GetDesktopWindow()

    def __init__(self, debug=False):
        self.debug = debug
        self.project_path = PROJECT_PATH

        # desktop size
        self.width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.position = (self.left, self.top, self.right, self.bottom)

    @staticmethod
    def show_all_hwnd():
        hwnd_title = {}

        def get_all_hwnd(hwnd, mouse):
            if (win32gui.IsWindow(hwnd)
                    and win32gui.IsWindowEnabled(hwnd)
                    and win32gui.IsWindowVisible(hwnd)):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(get_all_hwnd, 0)
        for h, t in hwnd_title.items():
            if t:
                print(h, t)

    def save_fig(self, image, save_dir=None, postfix='jpg', quality=75):
        form_dict = {
            'jpg': 'JPEG',
            'png': 'PNG'
        }
        if save_dir is None:
            save_dir = os.path.join(
                self.project_path, 'CDMemory', 'pictures')
        file_path = 'screenshot_{}.{}'.format(
            time.strftime('%y%m%d_%H%M%S', time.localtime()), postfix)
        dump_path = os.path.join(save_dir, file_path)
        form = form_dict.get(postfix.lower(), 'jpg')
        image.save(fp=dump_path, format=form, quality=quality)
        if self.debug:
            print('save screen shot to {}'.format(dump_path))

    def load_fig(self, path):
        valid_flag = True
        try:
            image = Image.open(path)
            return image, valid_flag
        except Exception as e:
            valid_flag = False
            if self.debug:
                print(e)
        return None, valid_flag

    def _get_screenshot(self, handle, method='window'):
        if method == 'desktop':
            left, top, right, bottom = self.position
            width, height = self.width, self.height
        else:  # 'window'
            left, top, right, bottom = win32gui.GetWindowRect(handle)
            width, height = right - left, bottom - top
            # print(left, top, right, bottom)

        position_case = (left, top, right, bottom, width, height)
        tmp_path = see_and_remember(handle, position_case)
        return tmp_path

    def screenshot(self, save_dir=None, postfix='jpg', quality=75):
        # get bitmap object with memory DC
        tmp_path = self._get_screenshot(self.desktop, method='desktop')
        image, valid_flag = self.load_fig(tmp_path)

        # 将截图保存到文件中
        if postfix.lower() != 'bmp':
            self.save_fig(
                image=image, save_dir=save_dir,
                postfix=postfix, quality=quality)
        # Remove bitmap
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    def capture_by_handle(self, handle, save_dir=None, postfix='jpg'):
        if not isinstance(handle, int):
            return self.capture_by_name(
                window_name=handle, save_dir=save_dir, postfix=postfix)
        tmp_path = self._get_screenshot(handle, method='window')
        image, valid_flag = self.load_fig(tmp_path)
        if postfix.lower() != 'bmp':
            self.save_fig(
                image=image, save_dir=save_dir,
                postfix=postfix)
        # Remove bitmap
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    def capture_by_name(self, window_name, save_dir=None, postfix='jpg'):
        handle = win32gui.FindWindow(None, window_name)
        return self.capture_by_handle(
            handle=handle, save_dir=save_dir, postfix=postfix)

    def capture(self, name_or_handle, save_dir=None, postfix='jpg'):
        if isinstance(name_or_handle, int):
            return self.capture_by_handle(
                handle=name_or_handle, save_dir=save_dir, postfix=postfix)
        return self.capture_by_name(
            window_name=name_or_handle, save_dir=save_dir, postfix=postfix)

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    de = DesktopEye(True)
    # de.capture(u'最终幻想XIV')
    de.show_all_hwnd()
    de.capture(u'League of Legends')

