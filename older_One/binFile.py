import aditofpython as tof
import argparse
import numpy as np
import cv2 as cv
import open3d as o3d
from enum import Enum
import sys


parser = argparse.ArgumentParser(
    description='Script to run PointCloud')
parser.add_argument('-ip', '--ip', help='Ip address of the ToF device')
parser.add_argument('-f', '--frame', help='Name of an acquired frame to be used')
parser.add_argument('-m', '--mode', help='Camera mode')

args = parser.parse_args()
system = tof.System()

print("SDK version: ", tof.getApiVersion(), " | branch: ", tof.getBranchVersion(), " | commit: ", tof.getCommitVersion())

cameras = []
fileName = args.frame

# Reading binary file 
frame = tof.Frame()
frameHandler = tof.FrameHandler()
status = frameHandler.readNextFrame(frame, fileName)

if not status:
    print('Failed to read frame with status: ', status)

frameDataDetails = tof.FrameDataDetails()
status = frame.getDataDetails("depth", frameDataDetails)
width = frameDataDetails.width
height = frameDataDetails.height

# Get camera details for frame correction
# TO DO: Get the range from camera details when it will be defined
camera_range = 4096
bitCount = 12
max_value_of_AB_pixel = 2 ** bitCount - 1
distance_scale_ab = 255.0 / max_value_of_AB_pixel
distance_scale = 255.0 / camera_range

#how to run bin file:
# python read_frame.py --frame frame_001.bin
 