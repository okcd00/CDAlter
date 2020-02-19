# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : CDBrain.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : Control and make use of all parts.
# ==========================================================================
# from utils import *
from CDEyes import WindowEye
from CDHands import MouseHand


class CDBrain(object):
    w_eye = WindowEye()
    m_hand = MouseHand()

    def __init__(self):
        pass

    def __repr__(self):
        return None

    def __str__(self):
        return None


if __name__ == '__main__':
    print("pass")
