import cv2
import numpy as np

# open the image file
img1_color = cv2.imread("cup_thermal.jpg")
img2_color = cv2.imread("cup_visible.jpg")

# Convert to gray scale
img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
height, width = img2.shape

# Create ORB detector
orb_detector = cv2.ORB_create(5000)

# Find key points and descriptor
kp1, d1 = orb_detector.detectAndCompute(img1, None)
kp2, d2 = orb_detector.detectAndCompute(img2, None)

# match 2 features
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

# Match the two sets of descriptors
matches = matcher.match(d1, d2)

# Sort matches on the basis of their Hamming distance
matches.sort(key = lambda x: x.distance)

# Take the top 90% matches forward
matches = matches[:int(len(matches)*90)]
no_of_matches = len(matches)

# Define empty matrices of shape
p1 = np.zeros((no_of_matches, 2))
p2 = np.zeros((no_of_matches, 2))

for i in range(len(matches)):
    p1[i, :] = kp1[matches[i].queryIdx].pt
    p2[i, :] = kp2[matches[i].trainIdx].pt

# find the homography matrix
homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)

# Use the matrix to transform
transformed_img = cv2.warpPerspective(img1_color, homography, (width, height))

# Save the output
cv2.imwrite('output.jpg', transformed_img)

