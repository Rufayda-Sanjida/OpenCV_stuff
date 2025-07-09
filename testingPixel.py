# import cv2

# # Open the default camera (index 0)
# cap = cv2.VideoCapture(1)

# # Check if the camera opened correctly
# if not cap.isOpened():
#     print("Error: Cannot open camera")
#     exit()

# # Capture a single frame
# ret, frame = cap.read()
# print(frame)

# # Release the camera right after capture
# cap.release()

# # Check if the frame was captured
# if not ret:
#     print("Error: Cannot read frame")
#     exit()


# gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# # Show the frame
# cv2.imshow("Captured Image", gray_frame)

# # Wait until a key is pressed
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# ###################################################################################################################################################
# depth_min = np.min(image_depth)
# depth_max = np.max(image_depth)

# # Normalize depth to range 0-255
# depth_normalized = (255 * (image_depth - depth_min) / (depth_max - depth_min)).astype(np.uint8)
# cv2.imshow("Depth Image", depth_normalized)


# #surface (50, 50) cluster:
# cluster1_center = (50, 50)  # near side

# #breast (50, 50) cluster:
# cluster2_center = (frameDataDetails.width // 2, frameDataDetails.height // 2)  # middle

# cluster_size = 50  # pixels radius for cluster

# # Draw rectangles around cluster centers
# cv2.rectangle(depth_normalized, 
#               (cluster1_center[0] - cluster_size, cluster1_center[1] - cluster_size),
#               (cluster1_center[0] + cluster_size, cluster1_center[1] + cluster_size),
#               color=200, thickness=2)  # light gray rectangle

# cv2.rectangle(depth_normalized,
#               (cluster2_center[0] - cluster_size, cluster2_center[1] - cluster_size),
#               (cluster2_center[0] + cluster_size, cluster2_center[1] + cluster_size),
#               color=200, thickness=2)

# cv2.imshow("Depth Image with Clusters", depth_normalized)


import cv2

# Open the default camera (index 1 or 0 depending on your system)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Cannot read frame")
    exit()

# Convert to grayscale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Get dimensions
height, width = gray_frame.shape
print("Image size:", width, "x", height)

# Define clusters
cluster_size = 50
cluster1_center = (50, 50)
cluster2_center = (width // 2, height // 2)

# Convert grayscale to BGR so we can draw colored rectangles
gray_bgr = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

# Draw rectangles
cv2.rectangle(gray_bgr,
              (cluster1_center[0] - cluster_size, cluster1_center[1] - cluster_size),
              (cluster1_center[0] + cluster_size, cluster1_center[1] + cluster_size),
              color=(255, 200, 100), thickness=3)

cv2.rectangle(gray_bgr,
              (cluster2_center[0] - cluster_size, cluster2_center[1] - cluster_size),
              (cluster2_center[0] + cluster_size, cluster2_center[1] + cluster_size),
              color=(100, 255, 100), thickness=3)

# Show the image
cv2.imshow("Captured Image with Clusters", gray_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
