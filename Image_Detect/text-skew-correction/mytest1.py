# usage: python mytest1.py -i images\neg_28.png

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to load image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      # 反转图像为反色，深色背景，浅色文字
gray = cv2.bitwise_not(gray)

# 应用阈值操作，对图像进行二值化：浅色变为255，其他'干扰'均为0
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 计算包含文本区域的最小旋转边界框
coords = np.column_stack(np.where(thresh > 0))
# 将前景的所有x,y坐标传递到minAreaRect, 计算包含整个文本的最小旋转矩形
angle = cv2.minAreaRect(coords)[-1]     # 再确定文本倾斜角

if angle < -45:
    angle = -(90+angle)
else:
    angle = -angle

# 应用仿射变换校正倾斜
(h, w) = image.shape[:2]
center = (w//2, h//2)       # 确定图像中心点坐标
M = cv2.getRotationMatrix2D(center, angle, 1.0)     # 获取旋转矩阵
# 对图片image进行实际旋转操作
output = cv2.warpAffine(image, M, (w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# 在图像上绘制'倾斜角度'，验证图像输出是否与旋转角度匹配
cv2.putText(output, 'Angle: {:.2f} degrees'.format(angle), (10,30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

print('[info] angle: {:.3f}'.format(angle))
cv2.imshow('Input:', image)
cv2.imshow('Output:', output)
cv2.waitKey(0)
