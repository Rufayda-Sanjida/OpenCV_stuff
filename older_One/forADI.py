import os
import cv2 as cv
import numpy as np

# Ensure output folder exists
output_folder = os.path.join(os.getcwd(), "images")
os.makedirs(output_folder, exist_ok=True)

# Normalize the depth image to 0-255 for visualization
depth_min = np.min(image_depth)
depth_max = np.max(image_depth)
depth_normalized = (255 * (image_depth - depth_min) / (depth_max - depth_min)).astype(np.uint8)

# Save normalized depth image
cv.imwrite(os.path.join(output_folder, f'depth_norm_{num}.png'), depth_normalized)

# Save raw depth image as 16-bit PNG (will be clamped if out of range)
cv.imwrite(os.path.join(output_folder, f'depth_raw_{num}.png'), image_depth)

# Save raw data as .npy for full precision
np.save(os.path.join(output_folder, f'depth_raw_{num}.npy'), image_depth)

# ----------------------------------------------------------------
# Annotations

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

# Display and save annotated image
cv.imshow("Depth Image with Clusters", depth_with_annotations)
cv.imwrite(os.path.join(output_folder, f'depth_annotated_{num}.png'), depth_with_annotations)
