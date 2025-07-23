animation-pygame.py:
- NO Actual numerical depth values are not printed or saved.
- What you get:
    - Live Depth Frames from the ToF camera:
        - It captures the raw depth frame using: frame.getData("depth")
        - This data is a 2D NumPy array, where each pixel value represents the depth (distance) at that point (typically in millimeters).

    - Visualization of Depth: 
        - The raw depth values are normalized and mapped to colors using a Jet colormap.
        - Red/yellow/green/blue represent different distances, letting you visually infer relative depth.


This code can help get read data:
def animate():
    frame = tof.Frame()
    camera1.requestFrame(frame)
    
    image = np.array(frame.getData("depth"), copy=False)
    image = np.rot90(image)

    # Example: print depth at center pixel
    h, w = image.shape
    center_depth = image[h//2, w//2]
    print(f"Center depth: {center_depth} mm")

    return pygame.surfarray.make_surface(normalize(image, w, h))
