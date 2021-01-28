import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('cupleft.jpg',0)
imgR = cv2.imread('cupright.jpg',0)

stereo = cv2.StereoBM_create(numDisparities=48, blockSize=15)
disparity = stereo.compute(imgL, imgR)
plt.imshow(disparity,'gray')
plt.show()