# -*- coding: utf-8 -*-
# ==========================================================================
#   Copyright (C) since 2021 All rights reserved.
#
#   filename : typist.py
#   author   : chendian / okcd00@qq.com
#   date     : 2021-07-20
#   desc     : type for a document in notepad
# ==========================================================================
import re
import sys
import time

sys.path.append('./')
sys.path.append('../')
from eyes.window_eye import WindowEye
from hands.pui_hand import PUIHand
from eyes.read_eye import ReadEye
from utils.pinyin_utils import PinyinUtils


SIGN2IS_TABLE = {
    '!': 'shift+1',
    '！': 'shift+1',
    '@': 'shift+2',
    '#': 'shift+3',
    '$': 'shift+4',
    '￥': 'shift+4',
    '%': 'shift+5',
    '^': 'shift+6',
    '……': 'shift+6',
    '&': 'shift+7',
    '*': 'shift+8',
    '(': 'shift+9',
    '（': 'shift+9',
    ')': 'shift+0',
    '）': 'shift+0',
}

SIGN_CHN2ENG = {
    '！': '!',
    '￥': '$',
    '（': '(',
    '）': ')',
    '：': ':',
    '，': ',',
    '。': '.',
    '……': '^',
}


class TypistAgent(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.window_eye = WindowEye(window_name=u'new 1 - Notepad++', debug=True)
        self.window_eye.set_foreground()
        print('Init finished. window at', self.window_eye.coordinate())
        self.typing_hand = PUIHand()
        self.read_eye = ReadEye()
        self.pinyin_memo = PinyinUtils()

    def load_document(self, txt_path):
        self.read_eye.read(txt_path)

    def type_sentence(self, chinese_text, sleep_time=0.25):
        input_sequence = self.pinyin_memo.sentence_pinyin(chinese_text)
        segments = self.pinyin_memo.segmentation(chinese_text)
        seg_indexes = [0]
        for seg in segments:
            seg_length = len(seg)
            # re.match('^[a-z]+$',
            #          ''.join(input_sequence[seg_indexes[-1]:seg_indexes[-1]+seg_length]))
            seg_indexes.append(seg_length + seg_indexes[-1])
        seg_indexes = seg_indexes[1:]
        if self.debug:
            print(segments)
            print(input_sequence)
            print(seg_indexes)
        for idx, inp_c in enumerate(input_sequence):
            inp_c = SIGN_CHN2ENG.get(inp_c, inp_c)
            """
            if inp_c in SIGN2IS_TABLE:
                _comb, _key = SIGN2IS_TABLE[inp_c].split('+')
                if self.debug:
                    print(_comb, '+', _key)
                self.typing_hand.tap_comb(_key, times=1, comb=_comb)
            else:
            """
            if idx in seg_indexes:
                self.typing_hand.type(' ')
            self.typing_hand.type(inp_c)
            time.sleep(sleep_time)


if __name__ == '__main__':
    ta = TypistAgent(debug=True)
    time.sleep(1)
    ta.type_sentence('今天天气好晴朗！123456 bad apple？')
    pass
