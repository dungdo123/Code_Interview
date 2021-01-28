import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('dave.jpg')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

newmask1 = cv2.imread('newmask.png',0)
newmask = cv2.resize(newmask1,(480,640))
mask[newmask == 0] = 0
mask[newmask == 255] = 1

# rect = (50,100,480,640)
# cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask, bgdModel, fgdModel = cv2.grabCut(img,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

plt.imshow(img),plt.colorbar(),plt.show()