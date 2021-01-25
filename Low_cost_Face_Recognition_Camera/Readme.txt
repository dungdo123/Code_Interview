
+ Description:
  This project aims to develop a low-cost camera system that combined face recognition with infrared thermography. The system could be applied for access management, temperature checking. Thanks to the low-price of the AMG8833 thermal sensor, the overall system is just around 100$ (the thermal camera is usually expensive, around 300$(Flir one) just for the camera). To achieve this objective, the source codes are built to solve 3 sub-problems:
  
  1. Face Detection
   + Because of the limitations of Raspberry Pi, the haar_cascade was used for face region detection.
   + Some other face detector are also investigate including: mtcnn, SSD.
  2. Face Recognition
   + 
  3. Temperature monitoring
   + The AMG8833 grideyes was used as thermal sensor.
   + The raw data read from sensor was converted to 8x8 thermal image.
   + The highest value in the temperature array was chose as temperature of object
   
+ Tool:
+ Results:

The temperature checking and face detection:
https://youtu.be/bTRF4Jby9hc

Thermal camera display:
https://youtu.be/MBCObK8PoXc

Face Recognition:
