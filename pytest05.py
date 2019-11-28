# /usr/bin/env python3
# -*- coding:utf-8 -*-
import math

print('理解呢大 %2d-%02d' %(3,1))
print('chygkkbiu %.2f' %3.1415926535)

def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
print(move(10,12,5,math.pi/6))

def fact(n):
	if n==1:
		return 1
	return n*fact(n-1)
	
print(fact(10))