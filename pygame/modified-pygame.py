
'''

#getting the center pixel distance!!

'''


import aditofpython as tof
import numpy as np
import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os

##################################################################################################################################################################
from collections import deque
############################################################################################################

mode = 3

def help():
    print(f"{sys.argv[0]} usage:")
    print(f"USB: {sys.argv[0]} <mode number>")
    print(f"Network connection: {sys.argv[0]} <mode number> <ip>")
    print()
    print("For example:")
    print(f"python {sys.argv[0]} 0 10.43.0.1")
    exit(1)

if len(sys.argv) < 2 or len(sys.argv) > 3 or sys.argv[1] == "--help" or sys.argv[1] == "-h" :
    help()
    exit(-1)

jet_colormap = plt.get_cmap('jet')

system = tof.System()

print("SDK version: ", tof.getApiVersion(), " | branch: ", tof.getBranchVersion(), " | commit: ", tof.getCommitVersion())

cameras = []
ip = ""
if len(sys.argv) == 3:
    mode = sys.argv[1]
    ip = sys.argv[2]
    print (f"Looking for camera on network @ {ip}.")
    ip = "ip:" + ip
elif len(sys.argv) == 2:
    mode = sys.argv[1]
    print (f"Looking for camera on UVC.")
else :
    print("Too many arguments provided!")
    exit(-2)

status = system.getCameraList(cameras, ip)
print("system.getCameraList()", status)

camera1 = cameras[0]

status = camera1.initialize()
print("camera1.initialize()", status)

modes = []
status = camera1.getAvailableModes(modes)
print("camera1.getAvailableModes()", status)
print(modes)

if int(mode) not in modes:
    print(f"Error: Unknown mode - {mode}")
    help()
    exit(-3)

camDetails = tof.CameraDetails()
status = camera1.getDetails(camDetails)
print("camera1.getDetails()", status)
print("camera1 details:", "id:", camDetails.cameraId, "connection:", camDetails.connection)

status = camera1.setMode(int(mode))
print("camera1.setMode()", status)

status = camera1.start()
print("camera1.start()", status)

sensor = camera1.getSensor()
modeDetails = tof.DepthSensorModeDetails()
status = sensor.getModeDetails(int(mode),modeDetails)
    
def normalize(image_scalar, width, height):
    image_scalar_norm = image_scalar / image_scalar.max()

    # Apply the colormap to the scalar image to obtain an RGB image
    image_rgb = jet_colormap(image_scalar_norm)
        
    surface = (image_rgb[:, :, :3] * 255).astype(np.uint8)
    return surface

def animate():
    # frame = tof.Frame()
    # status = camera1.requestFrame(frame)
    # frameDataDetails = tof.FrameDataDetails()
    # status = frame.getDataDetails("depth", frameDataDetails)
    # image = np.array(frame.getData("depth"), copy=False)
    # image = np.rot90(image)

################################################################################
    avg_image = get_averaged_frame()
    # Example: print center pixel depth from averaged image
    center_depth = avg_image[avg_image.shape[0] // 2, avg_image.shape[1] // 2]
    print(f"Averaged center depth: {center_depth:.2f} mm")
    return pygame.surfarray.make_surface(normalize(avg_image, avg_image.shape[1], avg_image.shape[0]))
############################################################################################################

    #return pygame.surfarray.make_surface(normalize(image, frameDataDetails.width, frameDataDetails.height))
    
def main():
    pygame.init()
    window_size = (modeDetails.baseResolutionWidth, modeDetails.baseResolutionHeight)
    screen = pygame.display.set_mode(window_size)

    # display the animation
    done = False
    i = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.blit(animate(), (0, 0))
        pygame.display.flip()

    # quit Pygame
    pygame.quit()

    status = camera1.stop()
    
main()




#######################################################################################################################################
# Holds last N depth frames
frame_buffer = deque(maxlen=100)
def get_averaged_frame():

    frame = tof.Frame()
    camera1.requestFrame(frame)
    image = np.array(frame.getData("depth"), copy=False)
    image = np.rot90(image)

    # Add current frame to buffer
    frame_buffer.append(image)

    # Stack and average the buffered frames
    if len(frame_buffer) > 1:
        avg_image = np.mean(frame_buffer, axis=0)
    else:
        avg_image = image.astype(np.float32)

    return avg_image
#######################################################################################################################################



