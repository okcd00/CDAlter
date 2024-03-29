# -*- coding: utf-8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : DesktopAvator.py
#   author   : chendian / okcd00@qq.com
#   date     : 2021-07-20
#   desc     : Draw GUI for simple applications
# ==========================================================================

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from utils import PROJECT_PATH
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TablePet(QWidget):
    example_fig = os.path.join(
        PROJECT_PATH, 'CDMemory', 'pictures', 'self_cartoon.png')

    def __init__(self, pic_uri=None, icon_uri=None, random_move=False, click_through=True):
        """
        uri should be relative path (e.g., CDMemory/test.png).
        """
        super(TablePet, self).__init__()
        self.desktop_width = 0
        self.desktop_height = 0
        
        self.icon_uri = self.example_fig
        self.pic_uri = self.example_fig
        if pic_uri and os.path.exists(pic_uri):
            self.pic_uri = os.path.join(PROJECT_PATH, pic_uri)
        if icon_uri and os.path.exists(icon_uri):
            self.icon_uri = os.path.join(PROJECT_PATH, pic_uri)
        self.pm = QPixmap(self.pic_uri) 
        self.figure_size = (self.pm.width(), self.pm.height())  # origin size
        
        self.click_through = click_through
        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        self.initUi()
        self.tray()

        self.timer = QTimer()
        if random_move:
            self.timer.timeout.connect(self.randomAct)
        self.timer.start(100)
        print("Init Finished.")

    def randomAct(self):
        if self.key < 21:
            self.key += 1
        else:
            self.key = 0
            
        self.pm = QPixmap(self.pic_uri)
        if self.is_follow_mouse:
            pass
        else:
            if self.w < self.desktop_width:
                self.w += 2
            else:
                self.w = 0
            self.move(self.w, self.h)
        self.lbl.setPixmap(self.pm)

    def initUi(self):
        screen = QDesktopWidget().screenGeometry()
        self.desktop_width = screen.width()
        self.desktop_height = screen.height()
        _w, _h = self.figure_size
        print(f"Current Desktop Size: {self.desktop_width}x{self.desktop_height}")
        self.w = self.desktop_width // 2 - _w // 2
        self.h = self.desktop_height // 2 - _h // 2
        self.setGeometry(self.w, self.h, _w, _h)
        # self.setWindowTitle('mypet')
        self.lbl = QLabel(self)
        self.key = 0  # for playing animation
        self.pm = QPixmap(self.pic_uri)
        self.lbl.setPixmap(self.pm)

        # flags
        _flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow
        if self.click_through:  # 鼠标穿透
            _flags |= Qt.WindowTransparentForInput
        self.setWindowFlags(_flags)
        self.setAutoFillBackground(False)

        # attributes
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.show()
        # self.repaint()

    def tray(self):
        tp = QSystemTrayIcon(self)
        tp.setIcon(QIcon(self.icon_uri))
        action_quit = QAction('Exit', self, triggered=self.quit)
        tpMenu = QMenu(self)
        tpMenu.addAction(action_quit)
        tp.setContextMenu(tpMenu)
        tp.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.w, self.h = xy.x(), xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def quit(self):
        self.close()
        sys.exit()


def show_sniper_marker():
    app = QApplication(sys.argv)
    sniper_pic_fp = 'memory/pictures/sniper_marker_small_circle.png'
    myPet = TablePet(pic_uri=sniper_pic_fp)
    sys.exit(app.exec_())


def show_desktop_pet():
    app = QApplication(sys.argv)
    myPet = TablePet(random_move=True, click_through=False)
    sys.exit(app.exec_())


if __name__ == '__main__':
    # show_sniper_marker()
    show_desktop_pet()