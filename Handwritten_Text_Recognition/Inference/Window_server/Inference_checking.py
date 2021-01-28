from SamplePreprocessor import preprocess
import cv2
import argparse
from Model import Model, DecoderType
from DataLoaderIAM import DataLoaderIAM, Batch

class FilePaths:
    "filenames and paths to data"
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'
    fnInfer = '../data/test12.png'
    fnCorpus = '../data/corpus.txt'

def infer(model, fnImg):
    img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)

    batch = Batch(None, [img])
    (recognized, probability) = model.inferBatch(batch, True)
    print(f'Recognized: "{recognized[0]}"')
    print(f'Probability: {probability[0]}')


decoderType = DecoderType.BestPath
print(open(FilePaths.fnAccuracy).read())
model = Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True)
print(type(FilePaths.fnInfer))
infer(model, FilePaths.fnInfer)
