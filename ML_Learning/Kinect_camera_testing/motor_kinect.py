import _thread
import pygame
from _pykinect.pykinect import nui

kinect = nui.Runtime()
kinect.camera.elevation_angle = 15
kinect.close()

