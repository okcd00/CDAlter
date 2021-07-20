# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : DesktopAvator.py
#   author   : chendian / okcd00@qq.com
#   date     : 2021-07-20
#   desc     : Draw GUI for simple applications
# ==========================================================================

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TablePet(QWidget):
    def __init__(self):
        super(TablePet, self).__init__()
        self.desktop_width = 0
        self.desktop_height = 0
        self.initUi()
        self.tray()

        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(100)
        print("Init Finished.")

    def randomAct(self):
        # 读取图片不同的地址，实现动画效果
        if self.key < 21:
            self.key += 1
        else:
            self.key = 0

        self.pic_url = '../CDMemory/pictures/self_cartoon.png'  #  + str(self.key) + '.png'
        self.pm = QPixmap(self.pic_url)
        if self.is_follow_mouse:
            pass
        else:
            # 实现行进效果
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
        self.w = self.desktop_width // 2
        self.h = self.desktop_height // 2
        self.setGeometry(self.w, self.h, 300, 300)
        # self.setWindowTitle('mypet')
        self.lbl = QLabel(self)
        self.key = 0
        self.pic_url = '../CDMemory/pictures/self_cartoon.png'  # + str(self.key) + '.png'
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

        # 背景透明等效果
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()
        # self.repaint()

    # 系统托盘
    def tray(self):
        tp = QSystemTrayIcon(self)
        tp.setIcon(QIcon('../CDMemory/pictures/self_cartoon.png'))
        ation_quit = QAction('退出', self, triggered=self.quit)
        tpMenu = QMenu(self)
        tpMenu.addAction(ation_quit)
        tp.setContextMenu(tpMenu)
        tp.show()

    # 鼠标事件
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myPet = TablePet()
    sys.exit(app.exec_())
