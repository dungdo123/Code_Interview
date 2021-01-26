This code is for Mask-RCNN part in my paper "A Deep Learning Approach for Food Quality Classification Based on RF Energy Harvesting and Mask-RCNN"

+ Description
The objective of this project is to develop a Mask-RCNN detector for Food statements. Mask R-CNN is adopted to solve instance segmentation problems. The proposed architecture is shown below:

//img1

To overcome the limitations of small dataset, I applied two methods:
 - Data Augmentation using synthesis images
 The number of training images can be increased by combining fourth ground and difference backgrounds. The example is described below:
 
 <img src="https://github.com/dungdo123/Code_Interview/blob/main/Conference_Paper_%231/Data%20augmentation/dataset/input/backgrounds/1.jpg" width="100" height="100"/> <img src="https://github.com/dungdo123/Code_Interview/blob/main/Conference_Paper_%231/Data%20augmentation/dataset/input/backgrounds/10.jpg" width="100" height="100"/>
 background
 
 - Transfer learning




+ Tools:
