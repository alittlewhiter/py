import numpy as np

def area(width, height):
    return width * height

def sigmoid(t):
    a=1.0/(1+np.exp(0-t))
    return a
b=sigmoid(1)
print(b)

