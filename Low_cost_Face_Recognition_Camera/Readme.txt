
+ Description:
  This project aims to develop a low-cost camera system that combined face recognition with infrared thermography. The system could be applied for access management, temperature checking. Thanks to the low-price of the AMG8833 thermal sensor, the overall system is just around 100$ (the thermal camera is usually expensive, around 300$(Flir one) just for the camera). To achieve this objective, the source codes are built to solve 3 sub-problems:
  
  1. Face Detection
   + Because of the limitations of Raspberry Pi, the haar_cascade was used for face region detection.
   + Some other face detector are also investigate including: mtcnn, SSD.
  2. Face Recognition
   The Face recognition problem can be described as following:
   
   |--------------------------------------------------------------- |      | -----------------------|     |--------------------|
   |Dataset ---> Face_detector ---> OpenFace model---> 128-d vector |  =>  | SVM classifier training|  => |Run face recognition|
   |----------------------------------------------------------------|      | -----------------------|     |--------------------|
                  Extract_embedding.py                                         train_model.py           recognize.py/recognize_video.py
   
   
  3. Temperature monitoring
   + The AMG8833 grideyes was used as thermal sensor.
   + Raw data read from sensor was converted to 8x8 thermal image and the highest value in the temperature array was chosen as temperature of object
   
+ Tool:
 - Raspberry pi3, AMG88xx
 - Raspbian (linux dis), python 3.
 - OpenCV, pygame, Adafruit_AMG88xx
 - Pretrained model: SSD face detector, OpenFace, 
 
+ Results:

The temperature checking and face detection:
https://youtu.be/bTRF4Jby9hc

Thermal camera display:
https://youtu.be/MBCObK8PoXc

Face Recognition:
https://youtu.be/3OVV7TnWiog

+ References:
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
https://github.com/adafruit/Adafruit_AMG88xx_python
https://makersportal.com/blog/2018/1/25/heat-mapping-with-a-64-pixel-infrared-sensor-and-raspberry-pi
