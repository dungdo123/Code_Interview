import cv2
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN

# define detector
detector = MTCNN()

# init the video stream
print("[INFO] starting video stream ...")
path = "rtsp://admin:admin@192.168.0.51:554"
vs = cv2.VideoCapture(path)
while True:
    ret, frame = vs.read()
    faces = detector.detect_faces(frame)
    print(faces)
    # # plot each face
    # for face in faces:
    #     x1, y1, width, height = face['box']
    #     x2, y2 = x1+width, y1+height
    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
