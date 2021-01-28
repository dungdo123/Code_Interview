# image blurring: useful for removing noise. It actually removes high frequency content (noise, edge)
# opencv provide mainly 4 methods of blurring techniques

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("dave.jpg", 0)

# Average
blur1 = cv2.blur(img, (5,5))

# Gaussian Filtering: Highly effective in removing Gaussian noise from the image
blur2 = cv2.GaussianBlur(img,(5,5),0)

# Median Filter: removing salt-and-pepper noise, replace by a pixel value that exist in the image
median = cv2.medianBlur(blur2, 5)

# Bilateral Filtering : highly effective at noise while preserving edges
blur3 = cv2.bilateralFilter(img, 9, 75, 75)

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur2),plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()
# cv2.imshow("image", blur)
# cv2.waitKey(0)



