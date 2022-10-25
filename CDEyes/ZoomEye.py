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
from PIL import ImageGrab, ImageTk


class ZoomEye(object):
    def __init__(self, debug=False):
        root = tkinter.Tk()
        screenW = root.winfo_screenwidth()
        screenH = root.winfo_screenheight()
        root.geometry("500x300")
        root.wm_attributes('-topmost', 1)  # [1] 置顶
        
        # 不显示标题栏
        root.overrideredirect(True)
        self.root = root
        self.canvas = None

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
    
    def __call__(self):
        self.root.after(func=self.run, ms=100)
        # 创建白色画布
        self.canvas = tkinter.Canvas(self.root, width=500, height=300)     
        # 画布放置至窗体
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)       
        self.root.mainloop()


if __name__ == "__main__":
    ze = ZoomEye()
    ze()
