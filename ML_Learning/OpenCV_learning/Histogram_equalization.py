# a good image will have pixels from all regions of the image
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('wiki.jpg', 0)

# hist = cv2.calcHist([img],[0],None,[256],[0,256])
#
# cdf = hist.cumsum()
# cdf_normalized = (cdf*hist.max())/(cdf.max())
#
# plt.plot(cdf_normalized, color = 'b')
# # plt.hist(img.flatten(),256,[0,256], color = 'r')
# plt.plot(hist)
# plt.xlim([0,256])
# plt.legend(('cdf','histogram'), loc = 'upper left')
# plt.show()

# hist,bins = np.histogram(img.flatten(),256,[0,256])
#
# cdf = hist.cumsum()
# cdf_normalized = cdf * hist.max()/ cdf.max()
#
# cdf_m = np.ma.masked_equal(cdf, 0)
# cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
# cdf = np.ma.filled(cdf_m,0).astype('uint8')
# img2 = cdf[img]
#
# plt.plot(cdf, color = 'b')
# plt.hist(img2.flatten(),256,[0,256], color = 'r')
# plt.xlim([0,256])
# plt.legend(('cdf','histogram'), loc = 'upper left')
# plt.subplot(221), plt.imshow(img2, 'gray')
# plt.subplot(222), plt.imshow(img, 'gray')
# plt.show()

# Histograms Equalization in OpenCV
equ = cv2.equalizeHist(img)
# # plt.subplot(121), plt.imshow(img, 'gray')
# # plt.subplot(122), plt.imshow(equ, 'gray')
# # plt.show()

# adaptive hsitogram equalization (CLAHE)
clhae = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clhae.apply(img)

cv2.imwrite('clane_2.jpg', cl1)
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(cl1, 'gray')
plt.subplot(223), plt.imshow(equ, 'gray')
plt.show()