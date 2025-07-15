# Define cluster centers
cluster1_center = (50, 50)  # near side
cluster2_center = (frameDataDetails.width // 2, frameDataDetails.height // 2)  # center (implant area)
cluster_size = 50  # pixels radius for rectangle

# Create a copy to draw annotations (don't draw on original)
depth_with_annotations = depth_normalized.copy()

# Draw rectangles around cluster centers
cv.rectangle(depth_with_annotations,
             (cluster1_center[0] - cluster_size, cluster1_center[1] - cluster_size),
             (cluster1_center[0] + cluster_size, cluster1_center[1] + cluster_size),
             color=200, thickness=2)

cv.rectangle(depth_with_annotations,
             (cluster2_center[0] - cluster_size, cluster2_center[1] - cluster_size),
             (cluster2_center[0] + cluster_size, cluster2_center[1] + cluster_size),
             color=200, thickness=2)


## what does this look visually??