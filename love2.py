from time import sleep
import turtle

def go_to(x, y):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()


def big_Circle(size):  #函数用于绘制心的大圆
    turtle.speed(1)
    for i in range(150):
        turtle.forward(size)
        turtle.right(0.3)

def small_Circle(size):  #函数用于绘制心的小圆
    turtle.speed(1)
    for i in range(210):
        turtle.forward(size)
        turtle.right(0.786)

def line(size):
    turtle.speed(1)
    turtle.forward(51*size)

def heart( x, y, size):
    go_to(x, y)
    turtle.left(150)
    turtle.begin_fill()
    line(size)
    big_Circle(size)
    small_Circle(size)
    turtle.left(120)
    small_Circle(size)
    big_Circle(size)
    line(size)
    turtle.end_fill()

def arrow():
    turtle.pensize(10)
    turtle.setheading(0)
    go_to(-400, 0)
    turtle.left(15)
    turtle.forward(150)
    go_to(339, 178)
    turtle.forward(150)

def arrowHead():
    turtle.pensize(1)
    turtle.speed(1)
    turtle.color('red', 'red')
    turtle.begin_fill()
    turtle.left(120)
    turtle.forward(20)
    turtle.right(150)
    turtle.forward(35)
    turtle.right(120)
    turtle.forward(35)
    turtle.right(150)
    turtle.forward(20)
    turtle.end_fill()


def main():
    turtle.pensize(2)
    turtle.color('red', 'pink')
    #getscreen().tracer(30, 0) #取消注释后，快速显示图案
    heart(200, 0, 1)          #画出第一颗心，前面两个参数控制心的位置，函数最后一个参数可控制心的大小
    turtle.setheading(0)             #使画笔的方向朝向x轴正方向
    heart(-80, -100, 1.5)     #画出第二颗心
    arrow()                   #画出穿过两颗心的直线
    arrowHead()               #画出箭的箭头
    go_to(400, -300)
    turtle.write("author：520Python", move=True, align="left", font=("宋体", 30, "normal"))
    turtle.done()

main()