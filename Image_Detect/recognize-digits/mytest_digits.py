# 识别LCD显示屏上的数字：
# 定位LCD区域，利用足够的对比度使用边缘检测完成
# 提取LCD，寻找具有最大矩形轮廓的数字区域，透视变换
# 提取数字区域，阈值化和形态计算
# 识别数字，根据七段显示器特点将数字ROI分为七个部分，对阈值图像应用像素计数以确定给的片段的开/关
# 

from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import argparse
import cv2

# define a dictionary of digit segment: to identify each digit on the thermostat
DIGIT_LOOKUP = {
    (1,1,1,0,1,1,1): 0,
    (0,0,1,0,0,1,0): 1,
    (1,0,1,1,1,1,0): 2,
    (1,0,1,1,0,1,1): 3,
    (0,1,1,1,0,1,0): 4,
    (1,1,0,1,0,1,1): 5,
    (1,1,0,1,1,1,1): 6,
    (1,0,1,0,0,1,0): 7,
    (1,1,1,1,1,1,1): 8,
    (1,1,1,1,0,1,1): 9}

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', required=True, help='path to the image file')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

image = imutils.resize(image, height=500)       # 调整大小
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转化为灰度
blurred = cv2.GaussianBlur(gray, (5,5), 0)      # 对5x5内核应用高斯模糊，以减少高频噪声
edged = cv2.Canny(blurred, 50, 200, 255)        # 通过Canny边缘检测器计算边缘轮廓

# 提取区域轮廓并按其面积降序排序
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:                      # 对排序的轮廓列表逐次遍历，应用轮廓逼近
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)   # 近似轮廓

    if len(approx) == 4:            # 近似轮廓含有四个顶点：假设已找到LCD区域
        displayCnt = approx
        break

# 获取四个顶点后，通过四点透视变换提取LCD:
warped = four_point_transform(gray, displayCnt.reshape(4,2))
output = four_point_transform(image, displayCnt.reshape(4,2))

# 对图像进行阈值处理，二值化反色
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# 利用形态操作来清理阈值图像，将获得一个较好的分割图像
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


# 应用轮廓过滤，寻找数字轮廓
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []          # 此列表存储数字本身轮廓


for c in cnts:          # 对每个轮廓过滤宽高比（1：2），确保在'数字'可接受范围内
    (x, y, w, h) = cv2.boundingRect(c)
    if w >= 15 and (h >= 30 and h <= 40):
        digitCnts.append(c)

# 注：确定适当的宽度和高度约束需要几轮反复试验，循环遍历每个轮廓，分别绘制它们的边界框，
# 并检查其尺寸，确保可以在数字轮廓属性之间找到共同点。

# 基于(x,y)坐标从左到右对数字轮廓进行排序
digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
digits = []

# loop over each of the digits
for c in digitCnts:
    (x, y, w, h) = cv2.boundingRect(c)      # 计算边界框
    roi = thresh[y:y + h, x:x + w]          # 应用Numpy数组切片来提取单独数字ROI

    (roiH, roiW) = roi.shape            # 根据ROI尺寸计算出每个相近段的近似宽度和高度
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    dHC = int(roiH * 0.05)

    segments = [
        ((0,0), (w, dH)),                       # top
        ((0,0), (dW, h // 2)),                  # top-left
        ((w - dW, 0), (w, h // 2)),             # top-right
        ((0,(h // 2)-dHC), (w, (h // 2)+dHC)),  # center
        ((0, h // 2), (dW, h)),                 # bottom-left
        ((w-dW, h // 2), (dW, h)),              # bottom-right
        ((0, h - dH), (w, h))                   # bottom
    ]
    on = [0] * len(segments)        # 该列表值1表示段'ON', 0表示'OFF'

# 遍历每个线段的(x, y)坐标
    for (i, ((xA, yA),(xB, yB))) in enumerate(segments):
        segROI = roi[yA:yB, xA:xB]          # 提取段ROI，用以非零像素计数，'ON'状态的像素数
        total = cv2.countNonZero(segROI)
        area = (xB -xA) * (yB - yA)

        if total / float(area) > 0.5:       # 若非零像素占该段总面积之比大于50%，即可认为该段是ON
            on[i] = 1

    print(tuple(on))
    
    digit = DIGIT_LOOKUP[tuple(on)]
    digits.append(digit)

    cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 1)
    cv2.putText(output, str(digit), (x-10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,220,120),2)


print(u'{}{}.{} \u00b0C'.format(*digits))
cv2.imshow('Input', image)
cv2.imshow('Output', output)
cv2.waitKey(0)






