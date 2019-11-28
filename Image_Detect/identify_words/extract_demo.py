# 使用OpenCV-Python实现图片文字区域的识别与分割

import cv2
import argparse
import imutils
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to load image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
# 转化为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
