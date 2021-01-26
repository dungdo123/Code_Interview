

# Description:

   This project is adopted to help my friend with an assignment in the multi-media class. The objective is to estimate the speed of vehicles in traffic videos. The problem is separated into 3 sub-problem: detection, tracking and speed estimation.
   
   1. Detection:
   
      Some pre-trained model performs best results on object detection including vehicle. I experimented with 3 models: YoloV3, Single Shot Detectors(SSD), and haar cascade. The YoloV3 seems beat the others on accuracy and speed processing.
      
   2. Tracking
   
      Object detection is expensive and slow, we should use object trackers to estimate speed and obtain a higher frame processing. I used dlib library to start a correlation tracker. 
      
   3. Speed Estimation
   
      To my knowledge, there are two state-of-the-art methods to estimate the speed of the vehicle in traffic videos: camera calibration parameters and vehicle speed analysis. The former requires the calibration parameters of the camera which is usually not available for unknown source videos (ex. youtube video), and the latter requires training on a large dataset and some other complicate assumptions. To simplify the problem, I applied the following equation to estimate the speed of cars ( assume that the width of the detected car is 1 meter):
      
               d_pixel x fs x 3.6
               
      speed = -----------------------
      
                      ppm
                    
                    
   Where: d_pixel: distance between two position of detected car.
   
          fs: frame rate
          
          ppm: pixel per meter
          
# Tools:

   - Python
   - OpenCV
   - YoloV3
   - Pycharm
   
# Resutls:

  Check the Vehicles_speed_Estimation in the following link:
  https://youtu.be/n3iB72NIeYU
