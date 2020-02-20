# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : DesktopEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     :
# ==========================================================================
import os
import time
import random
import datetime

# main packages
import win32ui
import win32gui
import win32api
import win32con
from PIL import Image
from ctypes import windll


class DesktopEye(object):
    desktop = win32gui.GetDesktopWindow()

    def __init__(self, debug=False):
        # 创建设备描述表
        self.debug = debug
        self.project_path = '..'

        # desktop size
        self.width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.position = (self.left, self.top, self.right, self.bottom)

    def save_fig(self, image, save_dir=None, postfix='jpg', quality=75):
        form_dict = {
            'jpg': 'JPEG',
            'png': 'PNG'
        }
        if save_dir is None:
            save_dir = os.path.join(
                self.project_path, 'data', 'screenshots')
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

    @staticmethod
    def time_identifier(add_postfix=True):
        time_stamp = '{0:%m%d%H%M%S%f}'.format(datetime.datetime.now())[::-1]
        mask = map(lambda x: chr(ord(x[0])+ord(x[1])), zip(time_stamp[::2], time_stamp[1::2]))
        t_id = ''.join(mask) + ''.join([str(random.randint(1, 10)) for _ in range(2)])
        return t_id + ('.bmp' if add_postfix else '')

    def _get_screenshot(self, handle, method='window'):
        if method == 'desktop':
            left, top, right, bottom = self.position
            width, height = self.width, self.height
        else:  # 'window'
            left, top, right, bottom = win32gui.GetWindowRect(handle)
            width, height = right - left, bottom - top

        # 创建设备描述表
        desktop_dc = win32gui.GetWindowDC(handle)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)

        # 创建内存设备描述表
        mem_dc = img_dc.CreateCompatibleDC()

        # 创建位图对象
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)

        # 截图至内存设备描述表
        remove_title_bar = 1  # 0
        mem_dc.BitBlt(
            (0, 0), (width, height),
            img_dc, (left, top), win32con.SRCCOPY)
        result = windll.user32.PrintWindow(handle, mem_dc.GetSafeHdc(), remove_title_bar)
        if self.debug:
            print('mem_dc.GetSafeHdc:', result)

        # 存入bitmap临时文件
        tmp_path = os.path.join(
            self.project_path, 'data', 'tmp', self.time_identifier())
        if self.debug:
            print('save source to {}'.format(tmp_path))
        screenshot.SaveBitmapFile(mem_dc, tmp_path)
        # bmp_str = screenshot.GetBitmapBits(True)

        # 内存释放
        win32gui.DeleteObject(screenshot.GetHandle())
        mem_dc.DeleteDC()
        img_dc.DeleteDC()
        win32gui.ReleaseDC(handle, desktop_dc)
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
            return self.capture(
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

    def capture(self, window_name, save_dir=None, postfix='jpg'):
        handle = win32gui.FindWindow(None, window_name)
        return self.capture_by_handle(
            handle=handle, save_dir=save_dir, postfix=postfix)

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    de = DesktopEye(True)
    de.capture(u'最终幻想XIV')

