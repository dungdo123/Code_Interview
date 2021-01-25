from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle

# load the image
pixels = imread('images/jun2.jpg')
# load the pre-trained model
classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
# perform face detection
bboxes = classifier.detectMultiScale(pixels)
# print bbox for each detected face
for box in bboxes:
    # extract
    x, y, width, height = box
    x2, y2 = x + width, y + height
    rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)
# show the image
imshow('face detection', pixels)
waitKey(0)
destroyAllWindows()