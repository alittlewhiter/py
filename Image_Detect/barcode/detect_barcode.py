# USAGE
# python detect_barcode.py --image images/barcode_01.jpg

# import the necessary packages
import numpy as np          # numpy进行数字处理
import argparse             # 用于解析命令行参数
import imutils              # 处理库
import cv2                  # 进行opencv绑定

# construct the argument parse and parse the arguments:
# 构造参数解析，并分析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "path to the image file")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
# 导入图片并转化为灰度图
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 计算图片x和y方向的Scharr梯度幅值大小
# compute the Scharr gradient magnitude representation of the images
# in both the x and y direction using OpenCV 2.4
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

# 用Scharr算子的x方向梯度减去y方向梯度：只剩下高水平梯度和低垂直梯度的图像区域
# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# 过滤图片中的噪声：对图片进行'模糊'和'阈值化'操作
# blur and threshold the image
# 使用一个卷积核大小为9x9的均值滤波作用于梯度图片，以平滑图片中的高频噪声
blurred = cv2.blur(gradient, (9, 9))
# 将模糊化的图片进行阈值化：所有像素点灰度值低于255的将设为0(黑)，其余设为255(白)
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

# 缩小条形码垂直方向的间隙：构造一个闭合核，并应用于阈值图片
# construct a closing kernel and apply it to the thresholded image
# 构造一个宽度大于高度的矩形核
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# 执行一系列腐蚀和膨胀操作，移除非条形码区域的斑点
# perform a series of erosions and dilations
closed = cv2.erode(closed, None, iterations = 4)    # 4次腐蚀：清除小的斑点
closed = cv2.dilate(closed, None, iterations = 4)   # 4次膨胀：扩张剩余白色像素

# 寻找阈值化后图片中的条形码轮廓，并根据区域进行排序，仅保留最大区域
# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# 计算最大轮廓的旋转边界框
# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)

# 在检测到的条形码周围绘制边框并显示图片
# draw a bounding box arounded the detected barcode and display the image
cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)


