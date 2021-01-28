# 1. Gaussian Pyramids
# 2. Laplacian Pyramids
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# img = cv2.imread('dave.jpg')
# high_reso = cv2.pyrUp(img)
# high_reso2 = cv2.pyrUp(high_reso)
# plt.subplot(221),plt.imshow(high_reso),plt.title('high_resolution')
# plt.xticks([]), plt.yticks([])
# plt.subplot(222),plt.imshow(img),plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(223),plt.imshow(high_reso2),plt.title('high_2')
# plt.xticks([]), plt.yticks([])
# plt.show()

# Image Blending using Pyramids
# import the necessary package
import cv2
import numpy as np

A = cv2.imread('apple.jpg')
B = cv2.imread('orange.jpg')

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    gpA.append(G)

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    gpB.append(G)

# generate Laplacian Pyramid for A
lpA = [gpA[5]]
for i in range(5,0,-1):
    GE = cv2.pyrUp(gpA[i])
    L = cv2.subtract(gpA[i-1],GE)
    lpA.append(L)

# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in range(5, 0, -1):
    GE = cv2.pyrUp(gpB[i])
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)

# Add left and right halves of images
LS = []
for la,lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    ls = np.hstack((la[:,0:cols/2], lb[:,cols/2:]))
    LS.append(ls)

# now reconstruct
ls_ = LS[0]
for i in range(1,6):
    ls_ = cv2.pyrUp(ls_)
    ls_ = cv2.add(ls_, LS[i])

# image with direct connecting each half
real = np.hstack((A[:,:cols/2], B[:,cols/2:]))

Pyramid_blending = cv2.imwrite('Pyramid_blending.jpg', ls_)
raw_blending = cv2.imwrite('Direct_blending.jpg',real)


plt.subplot(221),plt.imshow(A),plt.title('apple')
plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(B),plt.title('orange')
plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(Pyramid_blending),plt.title('Pyramid_blending')
plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(raw_blending),plt.title('Raw_blending')
plt.xticks([]), plt.yticks([])
plt.show()