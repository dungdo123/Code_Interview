# Reference: https://www.pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/

from __future__ import print_function
import numpy as np
import cv2

# load the image
img1 = cv2.imread("visible.bmp")
img2 = cv2.imread("thermal.bmp")
alpha = 0.3
overlay = img2.copy()
output = img1.copy()
cv2.addWeighted(overlay, alpha, output, 1-alpha, 0, output)
cv2.imshow("Output", output)
cv2.waitKey()
# loop over the alpha transparency values
# for alpha in np.arange(0, 1.1, 0.1)[::-1]:
#     overlay = image.copy()
#     output = image.copy()
#
#     # draw a red rectangle
#     cv2.rectangle(overlay, (420, 205), (595, 385), (0, 0, 255), -1)
#     # apply the overlay
#     cv2.addWeighted(overlay, alpha, output, 1-alpha, 0, output)
#     # Show the output image
#     print("alpha={}, beta={}".format(alpha, 1-alpha))
#     cv2.imshow("Output", output)
#     cv2.waitKey()
