# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : bcr_time_counter.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-04-30
#   desc     : time counter for auto-fight tickets in princess connection re:dive.
# ==========================================================================
import sys
import time

sys.path.append('../')
import threading
from CDEyes.WindowEye import WindowEye
from CDHands.PUIHand import PUIHand


class BcrAgent(object):
    last_time = time.time()
    next_time = time.time()
    cur_gap = 9

    def __init__(self):
        self.eye = WindowEye(window_name=u'夜神模拟器', debug=True)
        self.eye.set_foreground()
        print('Init finished. window at', self.eye.coordinate())
        self.hand = PUIHand()

    @staticmethod
    def get_time():
        return int(time.time())

    @staticmethod
    def show_time(t=None):
        if t is None:
            t = time.time() - 1
        return time.asctime(time.localtime(t))

    def report_time(self):
        cur_time = self.get_time()
        self.refresh_next_time()
        print(
            self.show_time(cur_time), '->',
            self.show_time(self.next_time))
        return cur_time

    def press(self, keys=None):
        if keys is None:
            keys = ['u']
        self.hand.keyboard.press_keys(keys)

    def use_ticket(self):
        # record begin time for 'use'
        # actual hit time is 1s after.
        self.eye.set_foreground()
        self.last_time = self.get_time()
        self.press(['u'])  # use
        time.sleep(1)
        self.press(['o'])  # ok
        time.sleep(1)
        self.press(['s'])  # finish, click side
        return self.last_time

    def change_gap(self):
        # 9 -> 11 or 11 -> 9
        sign = 10 - self.cur_gap
        self.cur_gap = 10 + sign

    def refresh_next_time(self):
        self.next_time = self.last_time + self.cur_gap
        while self.next_time < self.get_time() + 2:
            self.next_time += self.cur_gap
            break

    def wrong_refresh(self):
        # receive error command
        self.last_time -= self.cur_gap
        self.change_gap()
        self.last_time += self.cur_gap
        self.refresh_next_time()

    def click_thread(self):
        self.use_ticket()
        while True:
            cur_time = self.get_time()
            if cur_time > self.next_time:
                self.refresh_next_time()
            elif cur_time == self.next_time:
                self.use_ticket()
                self.report_time()
            # do nothing, wait for next second
            time.sleep(1)

    def read_feedback(self):
        while True:
            feedback = input("If no drop, press y and enter.\n")
            if feedback.strip():
                self.wrong_refresh()
                self.report_time()

    def __call__(self, *args, **kwargs):
        t1 = threading.Thread(target=self.click_thread)
        t2 = threading.Thread(target=self.read_feedback)
        t1.start()
        t2.start()


if __name__ == '__main__':
    ba = BcrAgent()
    ba()
    pass
