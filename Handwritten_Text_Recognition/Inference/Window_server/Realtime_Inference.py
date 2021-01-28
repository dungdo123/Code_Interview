import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
from SamplePreprocessor import preprocess
from Model import Model, DecoderType
from DataLoaderIAM import DataLoaderIAM, Batch

def infer(model, Img):
    img = preprocess(cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY), Model.imgSize)
    batch = Batch(None, [img])
    (recognized, probability) = model.inferBatch(batch, True)
    return recognized, probability

class FilePaths:
    "filenames and paths to data"
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'
    fnInfer = '../data/test12.png'
    fnCorpus = '../data/corpus.txt'

# define parameter for pre-trained model
decoderType = DecoderType.BestPath
print(open(FilePaths.fnAccuracy).read())
model = Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True)
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
           break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        cv_image = np.array(image)

        # Recognition with pre-trained model
        reg, proba = infer(model, cv_image)
        print(f'Recognized: "{reg[0]}"')
        print(f'Probability: {proba[0]}')
        # show the window images
        text = "{}: {:.4f}".format(reg[0], proba[0])
        cv2.putText(cv_image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 2)
        cv2.imshow('Text Recognition', cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()
