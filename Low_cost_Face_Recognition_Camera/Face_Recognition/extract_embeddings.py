
# import the necessary packages
import argparse
import cv2
import time
import numpy as np
from imutils import paths
import pickle
import os
import imutils

# construct argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True, help= "path to input dataset directory")
ap.add_argument("-e", "--embeddings", required=True, help="path to output serialized db of facial embedding")
ap.add_argument("-d", "--detector", required=True, help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True, help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# load serialized face embedding model from disk
print("[INFO] loading face recognition...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# init list of extracted facial embeddings and corresponding people names
knownEmbeddings = []
knownNames = []

# init the total number of processed faces
total = 0

# loop over the imagespath
for (i, imagePaths) in enumerate(imagePaths):
    # extract the person name from the imagepath
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    name = imagePaths.split(os.path.sep)[-2]

    # load the image, resize to have a width of 600 pixels
    image = cv2.imread(imagePaths)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]

    # construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV face detector
    detector.setInput(imageBlob)
    detections = detector.forward()

    # ensure at least one face was detected
    if len(detections) > 0:
        #assum that each image has only one face
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        # ensure that largest probability is also pass the minimum confidence
        if confidence > args["confidence"]:
            # compute the bbox of faces
            box = detections[0, 0, i, 3:7]*np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI and grab the ROI dimensions
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            # add the name of the person and corresponding face
            # embedding to their respective lists
            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())
            total += 1

# save the facial embedding and names to disk
print("[INFO] serializing {} encodings...".format(total))
data = {"embeddings": knownEmbeddings, "names": knownNames}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()







