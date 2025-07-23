###################################################################################################################################################
    
# Ensure output folder exists
output_folder = os.path.join(os.getcwd(), "images")
os.makedirs(output_folder, exist_ok=True)

# Normalize the depth image to 0-255 for visualization
depth_min = np.min(image_ab)
depth_max = np.max(image_ab)
depth_normalized = (255 * (image_ab - depth_min) / (depth_max - depth_min)).astype(np.uint8)

# Save normalized depth image
cv.imwrite(os.path.join(output_folder, f'depth_norm_{num}.png'), depth_normalized)

# Save raw depth image as 16-bit PNG (will be clamped if out of range)
cv.imwrite(os.path.join(output_folder, f'depth_raw_{num}.png'), image_ab)

# Save raw data as .npy for full precision
np.save(os.path.join(output_folder, f'depth_raw_{num}.npy'), image_ab)

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
#cv.imshow("Depth Image with Clusters", depth_with_annotations)
cv.imwrite(os.path.join(output_folder, f'depth_annotated_{num}.png'), depth_with_annotations)
    

###################################################################################################################################################
    
#getting the actual data (where image_depth = is the image)

height, width = image_depth.shape
top_left_region = image_depth[0:100, 0:100] 


# Compute the starting row and column for the center region
start_row = (height - 100) // 2
start_col = (width - 100) // 2

middle = image_depth[start_row:start_row+100, start_col:start_col+100]

# Mean of the top-left 100x100 region
top_left_mean = np.mean(top_left_region)

# Mean of the center 100x100 region
middle_mean = np.mean(middle)

print("Backgeound distance: " + top_left_mean)
print("object distance: " + middle_mean)

total_distance = top_left_mean - middle_mean


## what does this look visually??
''''''


'''


image_depth =  2D array of real-world distances (in mm)
100x100 =  get the distance of each indivually then find the average in 2 areas (background (right hand corner of pic) + object (middle of pic)) 

image_depth.shape  # e.g. (480, 640)


top_left_region = image_depth[0:100, 0:100]
This gives you:

Rows: from 0 to 99 (first 100 rows)

Columns: from 0 to 99 (first 100 columns)

So you get a 100×100 block of depth values starting at the top-left corner of the image.

'''