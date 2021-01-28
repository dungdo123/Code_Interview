import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('brain.png', 0)
row, col = img.shape

# add noise to an image
img_cpy = img.copy()
noise = cv2.randn(img_cpy, 150, 30)
gaussian_img = cv2.add(noise, img)

# Erosion: the thickness or size of foreground will be decreased
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)

# Dilation: opposite of erosion
dilation = cv2.dilate(img, kernel, iterations=1)

# opening: another name of erosion followed by dilation
# useful in removing noise
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing: reverse of Opening
# Useful in closing small holes inside the foreground objects
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Morphological Gradient
# the difference between dilation and erosion
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# Top Hat
# difference between input image and Opening of the image
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Black Hat
# the difference between the closing of the input image and input image.
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

plt.subplot(321),plt.imshow(erosion),plt.title('erosion')
plt.xticks([]), plt.yticks([])
plt.subplot(322),plt.imshow(img),plt.title('original')
plt.xticks([]), plt.yticks([])
plt.subplot(323),plt.imshow(dilation),plt.title('dilation')
plt.xticks([]), plt.yticks([])
plt.subplot(324),plt.imshow(closing),plt.title('fill inside')
plt.xticks([]), plt.yticks([])
plt.subplot(325),plt.imshow(gaussian_img),plt.title('noise')
plt.xticks([]), plt.yticks([])
plt.subplot(326),plt.imshow(opening),plt.title('reduced_noise')
plt.xticks([]), plt.yticks([])
plt.show()

