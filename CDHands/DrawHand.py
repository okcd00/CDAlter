# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : DrawHand.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-05-10
#   desc     : Draw a picture with turtle.
# ==========================================================================
import turtle


class DrawHand(object):
    def __init__(self):
        turtle.setup(650, 350, 200, 200)

    @staticmethod
    def draw():
        turtle.penup()
        turtle.fd(-250)
        turtle.pendown()
        turtle.pensize(25)
        turtle.pencolor("purple")
        turtle.seth(-40)
        for i in range(4):
            turtle.circle(40, 80)
            turtle.circle(-40, 80)
        turtle.circle(40, 80 / 2)
        turtle.fd(40)
        turtle.circle(16, 180)
        turtle.fd(40 * 2 / 3)
        turtle.done()

    def __call__(self, *args, **kwargs):
        self.draw()


if __name__ == '__main__':
    dh = DrawHand()
    dh()


