import cv2
import numpy as np

img = cv2.imread('Cat_picasso.jpg', 1)
cv2.imshow('test img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()