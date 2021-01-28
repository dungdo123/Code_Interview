# import the necessary packages
import cv2
import numpy as np
# Image processing
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(flags)

# Object tracking using color spaces changing
image = cv2.imread('blue.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow('frame',image)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

cv2.waitKey(0)