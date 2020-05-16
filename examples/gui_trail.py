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
from CDNerve.BaseFrame import *


if __name__ == '__main__':
    app = wx.App()
    frm = BaseFrame(None, title='CDPlayer\'s Hello-world')
    frm.start()
