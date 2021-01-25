# import the necessary packages
from _pykinect.pykinect import nui
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# init the video stream
print("[INFO] starting video stream ...")
path = "rtsp://admin:admin@192.168.0.51:554"
vs = cv2.VideoCapture(path)

# loop over the frames from the video stream
while True:
    # grab the frame and resize it to have maximum 400 pixel
    ret, frame = vs.read()
    #frame = imutils.resize(frame, width=600, height=600)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    # pass the blob through the network
    net.setInput(blob)
    detections = net.forward()
    # loop over the detection
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < args["confidence"]:
            continue
        box = detections[0, 0, i, 3:7] * np.array([h, w, h, w])
        (starX, startY, endX, endY) = box.astype("int")

        text = "{:.2f}%".format(confidence*100)
        y = startY - 10 if startY > 10 else startY + 10
        cv2.rectangle(frame, (starX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(frame, text, (starX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # press 'q' to break the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindow()
vs.stop()

