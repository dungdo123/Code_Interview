# 8 bit embedded classifier run on coral usb
Learn to train a CNN model, run it on Google colab and Coral Accelerator

Introduction

In this project, I built a basic CNN model to classify images of cats and dogs, then compress the trained model using quantization aware training and run it on Coral Accelerator. Base on this basic steps, you can build your own model and try it on an Edge AI device.

Main requirements:
 - Tensorflow 1.15 (support quantization)
 - Edgetpu_Compiler (only install on Linux)
 - USB Coral Accelerator
 
Methods:

 - Compress trained model by quantization aware training
     + set up quantization in training perior( build the model and insert into the graph fake nodes(min/max) for further quantization
     + Call it back after training, quantizing the weights of the model with learned min/max for each layer
     + fix the input, output, choose types of the weights and activations for the tflite (8 bits)
 - After having .tflite file with quantization, use edgetpu_compiler then you will have a freeze model which can run on Coral devices
 
 Results:
 
   All basic steps work well but the accuracy is not high. So it will be optimized. For higher accuracy, you should use Transfer learning technique, which is showed clearly in Coral documents. I will practice that technique and update to this respo when I have time
     
References:
https://github.com/lusinlu/tensorflow_lite_guide
https://coral.ai/docs/accelerator/get-started/
