# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : ZoomEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2022-10-25
#   desc     : Zoom in the view around the mouse.
# ==========================================================================

import tkinter
import win32api
import threading  # 导入多线程模块
from PIL import ImageGrab, ImageTk
from pynput import mouse


class ZoomEye(object):
    def __init__(self, debug=False):
        root = tkinter.Tk()
        screenW = root.winfo_screenwidth()
        screenH = root.winfo_screenheight()

        root.geometry("500x300")
        root.wm_attributes('-topmost', 1)  # [1] 置顶
        root.overrideredirect(True)  # 不显示标题栏
        
        self.immg = None
        self.root = root
        self.canvas = None
        self.event = threading.Event()
        self.event.clear()
        # self.mouse_event = PyMouseEvent(capture=True)
        self.mouse_event = mouse.Listener(on_click=True)
        self.mouse_right_is_down = False

    def run(self):
        # [2] 全局化图像对象，避免销毁导致闪烁
        global immg                             
        # [3] 获取鼠标坐标
        x,y = win32api.GetCursorPos()                  
        img = ImageGrab.grab((x-50,y-30,x+50,y+30))
        # 全屏抓取
        immg = ImageTk.PhotoImage(img.resize((500,300)))      
        # [4] 画布从中心点开始绘制
        self.canvas.create_image(250,150,image=immg) 
        # [5] 不断刷新放大镜的位置
        self.root.geometry("500x300+{}+{}".format(x+50,y+30))
        self.root.after(func=self.run, ms=10)

    def draw_zoom(self):                 
        # 获取鼠标坐标
        x, y = win32api.GetCursorPos()                  
        img = ImageGrab.grab((x-50,y-30,x+50,y+30))
        # 全屏抓取
        self.immg = ImageTk.PhotoImage(img.resize((500,300)))      
        # 画布从中心点开始绘制
        self.canvas.create_image(250, 150, image=self.immg) 
        # 不断刷新放大镜的位置
        self.root.geometry("500x300+{}+{}".format(x+50,y+30))
        self.root.after(func=self.run, ms=10)

    def paint(self):
        # 创建白色画布
        self.canvas = tkinter.Canvas(
            self.root, width=500, height=300)     
        # 画布放置至窗体
        self.canvas.pack(
            fill=tkinter.BOTH, expand=tkinter.YES)      

    def run_test_listener(self):
        if self.mouse_right_is_down:
            self.draw_zoom()
        self.mouse_right_is_down = False

    def left_click_down(self):
        print("left click")
        self.mouse_left_is_down = True

    def right_click_down(self):
        print("right click")
        self.mouse_right_is_down = True

    def __call__(self):
        self.root.after(func=self.run, ms=100)
        self.paint()
        # 开始循环
        self.root.mainloop()


if __name__ == "__main__":
    ze = ZoomEye()
    ze()
