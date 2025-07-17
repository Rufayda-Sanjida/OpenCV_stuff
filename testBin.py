# This script is used to load and process a depth frame (specifically a .bin file) captured from a Time-of-Flight (ToF) camera using the aditofpython SDK. 
# how to run script for opening bin file:
# python read_frame.py --frame frame_001.bin

import aditofpython as tof
import argparse
import numpy as np
import cv2 as cv
import open3d as o3d
import os

# Initialize ToF system and print SDK version
system = tof.System()
print("SDK version:", tof.getApiVersion(), "| branch:", tof.getBranchVersion(), "| commit:", tof.getCommitVersion())

# Parse arguments
parser = argparse.ArgumentParser(description='Script to run PointCloud')
parser.add_argument('-f', '--frame', help='Name of an acquired frame to be used')
args = parser.parse_args()
fileName = args.frame

# Validate file path
if not os.path.exists(fileName):
    print(f"Error: File '{fileName}' not found.")
    exit(1)

# Load binary frame
frame = tof.Frame()
frameHandler = tof.FrameHandler()
status = frameHandler.readNextFrame(frame, fileName)

if not status:
    print('Failed to read frame with status:', status)
    exit(1)

# Print depth frame details
frameDataDetails = tof.FrameDataDetails()
status = frame.getDataDetails("depth", frameDataDetails)
print("frame.getDataDetails() for 'depth':", status)
print("depth frame details: width:", frameDataDetails.width, "height:", frameDataDetails.height)

# Get and save depth data
depth_map = np.array(frame.getData("depth"), dtype="uint16", copy=False)
np.savetxt("depth_map.csv", depth_map, delimiter=",", fmt="%d")
print("Saved depth map to depth_map.csv")

# Try to get AB data
abDataDetails = tof.FrameDataDetails()
if frame.getDataDetails("ab", abDataDetails) == tof.Status.OK:
    ab_map = np.array(frame.getData("ab"), dtype="uint16", copy=False)
    np.savetxt("ab_map.csv", ab_map, delimiter=",", fmt="%d")
    print("Saved AB map to ab_map.csv")
else:
    print("AB data not available in this frame.")

# Try to get XYZ data
xyzDataDetails = tof.FrameDataDetails()
if frame.getDataDetails("xyz", xyzDataDetails) == tof.Status.OK:
    xyz_map = np.array(frame.getData("xyz"), dtype="int16", copy=False)
    xyz_points = np.resize(xyz_map, (depth_map.shape[0] * depth_map.shape[1], 3))
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(xyz_points.astype(np.float32))
    o3d.io.write_point_cloud("point_cloud.ply", pc)
    print("Saved point cloud to point_cloud.ply")
else:
    print("XYZ data not available in this frame.")
