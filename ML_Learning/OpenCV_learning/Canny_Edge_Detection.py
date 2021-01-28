# Concept of Canny edge detection
# 1.Noise Reduction
# 2.Finding intensity gradient of the image
# 3.Non-maximum Suppression
#  the results you get is a binary image with "thin edges"
# 4. Hysteresis Thresholding
#  decides which are all edges are really edges and which are not
#  we have to select minVal and max Val ( threshold)
# CED in OpenCv
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('dave.jpg', 0)
edges = cv2.Canny(img, 50, 100)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()