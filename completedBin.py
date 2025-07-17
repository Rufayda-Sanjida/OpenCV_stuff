# This script is used to load and process a depth frame (specifically a .bin file) captured from a Time-of-Flight (ToF) camera using the aditofpython SDK. 
# how to run script for opening bin file:
# python read_frame.py --frame frame_001.bin

import aditofpython as tof
import argparse
import numpy as np
import cv2 as cv
import open3d as o3d
from enum import Enum
import sys

#Initializes the ToF system and Prints the version of the SDK. FileName from parsed
system = tof.System()
print("SDK version: ", tof.getApiVersion(), " | branch: ", tof.getBranchVersion(), " | commit: ", tof.getCommitVersion())


#parsing arguments here:
parser = argparse.ArgumentParser(description='Script to run PointCloud')
parser.add_argument('-f', '--frame', help='Name of an acquired frame to be used')
args = parser.parse_args()
fileName = args.frame


#Load a Binary Frame
frame = tof.Frame()
frameHandler = tof.FrameHandler()
status = frameHandler.readNextFrame(frame, fileName)


#Check Read Status: it fails then failure is logged in
if not status:
    print('Failed to read frame with status: ', status)


#gets frame metadata 
# frameDataDetails = tof.FrameDataDetails()
# status = frame.getDataDetails("depth", frameDataDetails)
# width = frameDataDetails.width
# height = frameDataDetails.height

frameDataDetails = tof.FrameDataDetails()
status = frame.getDataDetails("depth", frameDataDetails)
print("frame.getDataDetails()", status)
print("depth frame details:", "width:", frameDataDetails.width, "height:", frameDataDetails.height, "type:", frameDataDetails.type)


##################################################################################################################


depth_map = np.array(frame.getData("depth"), dtype="uint16", copy=False)
ab_map = np.array(frame.getData("ab"), dtype="uint16", copy=False)
xyz_map = np.array(frame.getData("xyz"), dtype="int16", copy=False)

# Save depth to CSV
np.savetxt("depth_map.csv", depth_map, delimiter=",", fmt="%d")

# Save point cloud to PLY
xyz_points = np.resize(xyz_map, (depth_map.shape[0] * depth_map.shape[1], 3))
pc = o3d.geometry.PointCloud()
pc.points = o3d.utility.Vector3dVector(xyz_points.astype(np.float32))
o3d.io.write_point_cloud("point_cloud.ply", pc)





# # Get the depth frame
# image_depth = np.array(frame.getData("depth"), copy=False)
# # Get the AB frame
# image_ab = np.array(frame.getData("ab"), copy=False)
# # Get the confidence frame
# image_conf = np.array(frame.getData("conf"), copy=False)

# ## accessing the depth data here:
# print()
# print()
# print("Camera and depth ability is working! Lets see what we got!")
# print()
# print()
# print("Image Depth Data:")
# print(image_depth)
# print()
# print()

#ignore but you can do some frame correcting????
# # Get camera details for frame correction
# # TO DO: Get the range from camera details when it will be defined
# camera_range = 4096
# bitCount = 12
# max_value_of_AB_pixel = 2 ** bitCount - 1
# distance_scale_ab = 255.0 / max_value_of_AB_pixel
# distance_scale = 255.0 / camera_range