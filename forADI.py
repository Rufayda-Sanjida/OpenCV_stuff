import cv2

image_depth = np.array(frame.getData("depth"), copy=False)
# Get the AB frame
image_ab = np.array(frame.getData("ab"), copy=False)
# Get the confidence frame
image_conf = np.array(frame.getData("conf"), copy=False)

###################################################################################################################################################
depth_min = np.min(image_depth)
depth_max = np.max(image_depth)

# Normalize depth to range 0-255
depth_normalized = (255 * (image_depth - depth_min) / (depth_max - depth_min)).astype(np.uint8)
cv2.imshow("Depth Image", depth_normalized)


#surface (50, 50) cluster:
cluster1_center = (50, 50)  # near side

#breast (50, 50) cluster:
cluster2_center = (frameDataDetails.width // 2, frameDataDetails.height // 2)  # middle

cluster_size = 50  # pixels radius for cluster

# Draw rectangles around cluster centers
cv2.rectangle(depth_normalized, 
              (cluster1_center[0] - cluster_size, cluster1_center[1] - cluster_size),
              (cluster1_center[0] + cluster_size, cluster1_center[1] + cluster_size),
              color=200, thickness=2)  # light gray rectangle

cv2.rectangle(depth_normalized,
              (cluster2_center[0] - cluster_size, cluster2_center[1] - cluster_size),
              (cluster2_center[0] + cluster_size, cluster2_center[1] + cluster_size),
              color=200, thickness=2)

cv2.imshow("Depth Image with Clusters", depth_normalized)

