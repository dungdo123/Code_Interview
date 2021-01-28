
import cv2
import numpy as np

img = cv2.imread('dave.jpg', 0)

# scaling using resize()
# res = cv2.resize(img,None,fx=1, fy=1, interpolation = cv2.INTER_LINEAR)

# Translation
# rows, cols = img.shape
#
# M = np.float32([[1,0,100],[0,1,100]])
# dst = cv2.warpAffine(img, M, (cols, rows))

# Rotation
# rows, cols = img.shape
#
# M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
# dst = cv2.warpAffine(img, M, (cols, rows))

# Affine Transformation
# rows, cols = img.shape
#
# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])
#
# M = cv2.getAffineTransform(pts1,pts2)
#
# dst = cv2.warpAffine(img,M,(cols,rows))

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# plt.show()

# Perspective Transformation : need a 3x3 transformation matrix
rows, cols = img.shape

pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(300,300))

cv2.imshow('image', dst)
cv2.waitKey(0)