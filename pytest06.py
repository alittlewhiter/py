from turtle import *

def drawStar(x, y):
    pu()
    goto(x, y)
    pd()
    # set heading: 0
    seth(0)
    for i in range(5):
        fd(80)
        rt(144)

for x in range(-500, 750, 250):
    drawStar(x, 0)

done()