# Description

The objective of this project is to build a real-time handwritten/printed text system. The proposed architecture is shown as below:

<img src="https://github.com/dungdo123/Code_Interview/blob/main/Handwritten_Text_Recognition/images/system.PNG" width="600" height="200"/>

To make the system work, we have to solve 2 sub-problems:

1. Model Training

The architecture of HTR DL model can be described as below:

<img src="https://github.com/dungdo123/Code_Interview/blob/main/Handwritten_Text_Recognition/images/model.PNG" width="600" height="300"/>

The model can be trained from scratch or by transfer learning.
The details of model and training process is given in the project [1]

2. Inference system

A client-server system is built to detect the HRT in realtime. The client (Raspberry Pi-Linux OS) streams the images to the window-server through TCP/IP protocol; and the trained DL model will run inference on the server to recognize the given text in the images.

# Demo

The demonstrations can be found below:

demo1: https://youtu.be/1cN30QiZlqc

demo2: https://youtu.be/cn6QpxoF8EI

# Evaluation

The inference hasn't achieved a good results yet, The reasons could be:

- The model was trained on the dataset which just includes the fourth ground ( only text and no backgrounds).
- The low resolution images are given by pi-camera.
- The model is not trained enough.
- etc.

To enhance the performance, some extra-techniques can be applied:

- Detect the text region before inference ( using tesseract).
- Config some parameters of model.
- Continue training.

# References

[1]. https://github.com/githubharald/SimpleHTR

