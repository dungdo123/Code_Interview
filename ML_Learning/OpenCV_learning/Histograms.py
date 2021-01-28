# What is histogram?
# histogram as a graph or plot, which gives you an overall idea about the intensity distribution of an image
# It is a plot with pixel values (ranging from 0 to 255, not always) in X-axis and corresponding number of pixels in the image on Y-axis
# terminologies: BINS, DIMS, RANGE

# Find histogram: openCV (faster), Numpy

# plotting histograms: matplotlib (directly find and plot histogram), opencv

# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('dave.jpg')
# print(img.shape)
# plotting using matplotlib
# plt.hist(img.ravel(),256,[0,256])
# # plt.show()

# plotting using opencv, creating a mask for finding histogram of an interest region

#1. creating a mask
# mask = np.zeros(img.shape[:2], np.uint8)
# mask[100:300, 100:400] = 255
# masked_img = cv2.bitwise_and(img, img, mask=mask)
#
# # 2.Calculate histogram with mask and without mask
# hist_full = cv2.calcHist([img],[0],None,[256],[0,256])
# hist_mask = cv2.calcHist([img],[0],mask,[256],[0,256])
#
# plt.subplot(221), plt.imshow(img, 'gray')
# plt.subplot(222), plt.imshow(mask,'gray')
# plt.subplot(223), plt.imshow(masked_img, 'gray')
# plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
# plt.xlim([0,256])
#
# plt.show()

# 2D Histogram in OpenCV
# convert BGR image to HSV
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('gate.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0,180,0,256])

plt.subplot(121), plt.imshow(img)
plt.subplot(122), plt.plot(hist)
plt.show()


