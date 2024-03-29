import tkinter as tk
import threading
from time import sleep

event = threading.Event()

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('演示窗口')
        self.root.geometry("500x200+1100+150")
        self.interface()

    def interface(self):
        """"界面编写位置"""
        self.Button0 = tk.Button(self.root, text="启动", command=self.start)
        self.Button0.grid(row=0, column=0)

        self.Button0 = tk.Button(self.root, text="暂停", command=self.stop)
        self.Button0.grid(row=0, column=1)

        self.Button0 = tk.Button(self.root, text="继续", command=self.conti)
        self.Button0.grid(row=0, column=2)

        self.w1 = tk.Text(self.root, width=70, height=10)
        self.w1.grid(row=1, column=0, columnspan=3)

    def event(self):
        '''按钮事件，一直循环'''
        while True:
            sleep(1)
            event.wait()
            self.w1.insert(1.0, '运行中'+'\n')

    def start(self):
        event.set()
        self.T = threading.Thread(target=self.event)
        self.T.setDaemon(True)
        self.T.start()

    def stop(self):
        event.clear()
        self.w1.insert(1.0, '暂停'+'\n')

    def conti(self):
        event.set()
        self.w1.insert(1.0, '继续'+'\n')

if __name__ == '__main__':
    a = GUI()
    a.root.mainloop()