# 使用OpenCV-Python实现图片文字区域的识别与分割

import cv2
import argparse
import imutils
import os
import glob
from os import path
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to load image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
# 转化为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 形态计算处理，得到可以查找矩形的图片
sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
# 阈值处理，二值化
ret, binary = cv2.threshold(sobel, 0, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# 设置膨胀和腐蚀操作的核函数
elem1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
elem2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
# 膨胀一次，使得轮廓更加突出
dilation = cv2.dilate(binary, elem2, iterations=1)
# 腐蚀一次，去掉噪声细节，如表格竖线等
erosion = cv2.erode(dilation, elem1, iterations=1)
# 连续膨胀3次，使轮廓更明显
dilation2 = cv2.dilate(erosion, elem2, iterations=3)

# 查找和筛选文字区域
region = []
# 查找得到多个轮廓区域，存储在列表contours中
dilation3, contours, hierarchy = cv2.findContours(dilation2,cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)

# 创建输出目录
out_dir = 'Result'
if path.exists(out_dir):
    for f in glob.glob(out_dir+'/*'):
        os.remove(f)
else:
    os.mkdir(out_dir)

# 遍历所有轮廓，筛选面积较小的
for i in range(len(contours)):
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    if(area < 800):
        continue
    # 将轮廓形状近似到另外一种由更少点组成的轮廓形状
    epsilon = 0.001 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon,True)
    # 找到最小矩形轮廓，及其坐标
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    height = abs(box[0][1]-box[2][1])
    width = abs(box[0][0]-box[2][0])

    if(height > width * 1.3):
        continue
    region.append(box)
    output = image
    for box in region:
        cv2.drawContours(output, [box], 0, (0, 0, 255), 1)
        #print(box)
    #cv2.imshow('Output', output)
    #cv2.waitKey(0)
        
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    height = y2 - y1
    width = x2 - x1
    crop_img:object = output[y1:y1+height, x1:x1+width]
    #im = cv2.imshow('Crop_img', crop_img)
    #cv2.waitKey(0)

    print(out_dir+'/%d'%i+'.jpg')
    cv2.imwrite(out_dir+'/'+str(i)+'.jpg', crop_img)


#cv2.imwrite('out.jpg', output)
#show = cv2.imread('out.jpg')
#cv2.imshow('read-show', show)
#cv2.waitKey(0)

        
#cv2.imshow('Origin', image)
#cv2.imshow('Gray', gray)
#cv2.imshow('sobel', sobel)
#cv2.imshow('dilation', dilation)
#cv2.imshow('erosion', erosion)
#cv2.imshow('dilation2', dilation2)
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('Output', output)
#cv2.waitKey(0)
#cv2.destroyAllWindows()







