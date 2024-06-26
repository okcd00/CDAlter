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
from eyes.window_eye import WindowEye
from hands.pui_hand import PUIHand


class BcrAgent(object):
    cur_gap = 9

    def __init__(self):
        self.eye = WindowEye(window_name=u'ҹ��ģ����', debug=True)
        self.eye.set_foreground()
        print('Init finished. window at', self.eye.coordinate())
        self.hand = PUIHand()
        self.thread1 = threading.Thread(target=self.click_thread)
        self.thread2 = threading.Thread(target=self.read_feedback)
        self.last_time = self.get_time()
        self.next_time = self.get_time()

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
            self.show_time(self.last_time), '<-',
            self.show_time(cur_time), '->',
            self.show_time(self.next_time))
        return cur_time

    def press(self, keys=None):
        if keys is None:
            keys = ['u']
        self.eye.set_foreground()
        self.hand.keyboard.press_keys(keys)

    def use_ticket(self):
        # record begin time for 'use'
        # actual hit time is 1s after.
        self.last_time = self.get_time()
        self.press(['u'])  # use
        time.sleep(1)
        self.press(['o'])  # ok
        time.sleep(3)
        self.press(['s'])  # finish, click ok
        return self.last_time

    def change_gap(self):
        # 9 -> 11 or 11 -> 9
        self.cur_gap = 20 - self.cur_gap

    def refresh_next_time(self):
        self.next_time = self.last_time + self.cur_gap
        while self.next_time < self.get_time() + 2:
            self.next_time += self.cur_gap

    def wrong_refresh(self):
        # receive error command
        self.last_time -= self.cur_gap
        self.change_gap()
        self.refresh_next_time()

    def click_thread(self):
        self.use_ticket()
        self.report_time()
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
            inp = feedback.strip()
            if inp:  # in case of faulty touch
                if feedback.startswith('end'):
                    return  # in case of dead-loop
                self.wrong_refresh()
                print("Gap switched.")
                self.report_time()

    def restart(self):
        self.thread1.start()
        self.thread2.start()
        self.__call__()

    def __call__(self, *args, **kwargs):
        self.thread1.start()
        self.thread2.start()


if __name__ == '__main__':
    ba = BcrAgent()
    ba()
    pass
