# Coutours; simply as a curve joining all the continous points having same color or intensity
# useful for shape analysis and object detection and recognition


import cv2
import matplotlib.pyplot as plt

im = cv2.imread('dave.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,127,255,0)
image, contour = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

plt.subplot(221),plt.imshow(image),plt.title('image')
plt.xticks([]), plt.yticks([])
plt.show()
