# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : CDBrain.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-02-19
#   desc     : Control and make use of all parts.
#              Only import the packages you need.
# ==========================================================================
# from utils import *
from CDEyes.WindowEye import WindowEye
from CDHands.KMHand import KMHand


class CDBrain(object):
    w_eye = WindowEye()
    m_hand = KMHand()

    def __init__(self):
        pass

    def __repr__(self):
        return None

    def __str__(self):
        return None


if __name__ == '__main__':
    print("pass")
