# -*- coding: utf-8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : gui_trail.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-05-16
#   desc     :
# ==========================================================================
import sys
sys.path.append('../')
import random
from CDNerve.BaseFrame import *


class MyFrame(BaseFrame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

    def init_icon(self):
        icon = wx.Icon('cd_16x16.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(icon)
        return icon

    def init_basic_panel(self):
        # create a panel in the frame
        panel = wx.Panel(self)

        # create a sizer to manage the layout of child widgets
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        horizon_sizer = wx.BoxSizer()

        # put some text with a larger bold font on it
        default_label = "CDPlayer's CrackMe"
        st = self.add_text(text=default_label, parent=panel)
        vertical_sizer.Add(st, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=5)
        self.random_text = self.add_text(text="? ? ? ?", parent=panel, point_size=15)
        vertical_sizer.Add(self.random_text, proportion=2, flag=wx.TOP | wx.CENTER, border=5)

        # add a button
        rd_button = buttons.GenButton(panel, 10, 'Random')  # 基本的通用按钮
        sm_button = buttons.GenButton(panel, 11, 'Submit')  # 基本的通用按钮
        self.Bind(wx.EVT_BUTTON, self.on_rd_click, rd_button)
        self.Bind(wx.EVT_BUTTON, self.on_sm_click, sm_button)
        horizon_sizer.Add(rd_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        horizon_sizer.Add(sm_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        vertical_sizer.Add(horizon_sizer, proportion=1, flag=wx.CENTER)

        panel.SetSizer(vertical_sizer)

    def on_hello(self, event):
        wx.MessageBox("This is a MessageBox, without anything abnormal.")

    def on_rd_click(self, event):
        # number_for_hack
        numbers = random.randint(0, 9999)
        rd_str = ' '.join([d for d in '{:04}'.format(numbers)])
        self.random_text.SetLabel(rd_str)

    def on_sm_click(self, event):
        cur_string = self.random_text.GetLabel()
        cur_number = -1
        if cur_string.isdigit():
            cur_number = int(cur_string.replace(' ', ''))

        if cur_number == 622:  # or True:
            self.random_text.GetFont().PointSize -= 5
            self.random_text.SetLabel('Something abnormal happened.')
            self.file_menu.Remove(self.file_menu.GetMenuItems()[0])
            bonus_item = self.file_menu.Prepend(
                -1, "&旗子",
                "This is the flag for Mission One.")
            self.Bind(wx.EVT_MENU, self.on_bonus, bonus_item)
        else:
            self.random_text.SetLabel('Not This!')

    def on_bonus(self, event):
        """Display an About Dialog"""
        wx.MessageBox(caption="Flag #1 for Mission One",
                      message="{b2tjZDAwLnRlY2gvYXNzZXRzL00xNTUxMG5fVHcwLnBuZw==}",
                      style=wx.OK | wx.ICON_INFORMATION)

    def on_about(self, event):
        """Display an About Dialog"""
        wx.MessageBox(caption="Kari can ask for help any time.",
                      message="You have 3 times of asking for help.\n"
                      "HINT 1: send a heart-warming message to Dian.\n"
                      "HINT 2: send a heart-warming picture to Dian.\n"
                      "HINT 3: send a heart-warming video to Dian.",
                      style=wx.OK|wx.ICON_INFORMATION)


# there can not be `if __name__ == "__main__"` in script for packing.
if __name__ == "__main__":
    frm = MyFrame(None, title='CDPlayer\'s CrackMe.')
    frm.start()
