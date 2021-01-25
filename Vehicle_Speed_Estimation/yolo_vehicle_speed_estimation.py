
# type this command in the terminal to run:
# python yolo_vehicle_speed_estimation.py -i pathtoinputvideo -o pathtooutput -y pretrainedmodel

# import necessary library
from support.centroidtracker import CentroidTracker
from support.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import math
import os

# construct the argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
ap.add_argument("-s", "--skip-frames", type=int, default=10,
	help="# of skip frames between detections")

args = vars(ap.parse_args())

# speed estimation
def estimateSpeed(location1, location2, ppm, fs):
	d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
	d_meters = d_pixels/ppm
	speed = d_meters*fs*3.6
	return speed

# load the COCO class labels
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# init a list of color for different objects
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector and output layer names
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream
if not args.get("input", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

else:
	print("[INFO] opening video file...")
	vs = cv2.VideoCapture(args["input"])
fs = vs.get(cv2.CAP_PROP_FPS)

writer = None
(W, H) = (None, None)

# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

# init centroid tracker
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []
trackableOjects = {}

totalFrames = 0
fps = FPS().start()

while True:
    # read the next frame from the file
    (grabbed, frame) = vs.read()

    # if the frame was not grabbed, then we have reached the end of the stream
    if not grabbed:
        break

    # resize the frame to have maximum width of 500 pixels
    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # init a writer to write video to disk
    if args["output"] is not None and writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 30, (W, H), True)

    # init the status for detecting or tracking
    status = "Waiting"
    rects = []

    # Check to see if we should run a more detection method to aid our tracker
    if totalFrames % args["skip_frames"] == 0:
        # set the status and init our new set of object trackers
        status = "Detecting"
        trackers = []

        # convert the frame to a blob and pass the blob through the network and obtain the detections
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        # init ourlists of detected bboxes, confidences, class IDs
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the classID and confidence of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak detections
                if confidence > args["confidence"]:
                    # scale the bboxes back relative to the size of the image
                    # YOLO return the center (x, y) and width, height
                    box = detection[0:4]*np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center to derive the bottom and left corner of the bboxes
                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))

                    # update bboxes, confidences, classIDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppresion to suppress weak
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # init rect for tracking
                startX = boxes[i][0]
                startY = boxes[i][1]
                endX = boxes[i][0] + boxes[i][2]
                endY = boxes[i][1] + boxes[i][3]

                # construct a dlib rectangle object and start dlib correlation tracker
                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(startX, startY, endX, endY)
                tracker.start_track(rgb, rect)

                # add the tracker to our list and we can use it during skip frames
                trackers.append(tracker)

    # otherwise, we should use object trackers to estimate speed and obtain a higher frame processing
    else:
        # loop over the trackers
        for tracker in trackers:

            # set the status
            status = "Tracking"

            # update the tracker and grab the updated position
            tracker.update(rgb)
            pos = tracker.get_position()

            # unpack the position object
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())


            # calculate pixel per meter (ppm) based on width and heigh
            # ppm = math.sqrt(math.pow(endX - startX, 2) + math.pow(endY - startY, 2)) / math.sqrt(5)
            # ppm based on width of car
            ppm = math.sqrt(math.pow(endX-startX, 2))

            # tracking rect
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # add the bbox coordinates to the rectangles list
            rects.append((startX, startY, endX, endY))

    # use the centroid tracker to associate the object 1 and object 2
    objects = ct.update(rects)
    # loop over the tracked objects
    speed = 0
    for (objectID, centroid) in objects.items():
        # init speed array
        # speed = 0
        # check to see if a tracktable object exists for the current objectID
        to = trackableOjects.get(objectID, None)

        # if there is no tracktable object, create one
        if to is None:
            to = TrackableObject(objectID, centroid)
        # otherwise, use it for speed estimation
        else:
            to.centroids.append(centroid)
            location1 = to.centroids[-2]
            location2 = to.centroids[-1]
            speed = estimateSpeed(location1, location2, ppm, fs)
        trackableOjects[objectID] = to


        cv2.putText(frame, "{:.1f} km/h".format(speed), (centroid[0], centroid[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)


    if writer is not None:
        writer.write(frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    totalFrames += 1
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if writer is not None:
	writer.release()

if not args.get("input", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()


