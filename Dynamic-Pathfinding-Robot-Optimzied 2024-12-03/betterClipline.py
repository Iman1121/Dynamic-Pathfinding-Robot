from math import sqrt

def parallel_points(p1, p2, distance):
    """Calculate parallel line points at a given distance."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = sqrt(dx ** 2 + dy ** 2)
    if length == 0:
        return (p1, p1), (p2, p2)  # Avoid division by zero
    
    # Unit vector perpendicular to the line
    perp_dx, perp_dy = -dy / length, dx / length
    
    # Points for the two parallel lines
    offset1 = (perp_dx * distance, perp_dy * distance)
    offset2 = (-perp_dx * distance, -perp_dy * distance)
    
    p1_offset1 = (p1[0] + offset1[0], p1[1] + offset1[1])
    p2_offset1 = (p2[0] + offset1[0], p2[1] + offset1[1])
    
    p1_offset2 = (p1[0] + offset2[0], p1[1] + offset2[1])
    p2_offset2 = (p2[0] + offset2[0], p2[1] + offset2[1])
    
    return (p1_offset1, p2_offset1), (p1_offset2, p2_offset2)

def clipline_with_parallels(rect, p1, p2, distance=12):
    
    # Calculate parallel lines
    parallel1, parallel2 = parallel_points(p1, p2, distance)
    
    # Clip the lines
    main_clip = rect.clipline(p1, p2)
    parallel1_clip = rect.clipline(parallel1[0], parallel1[1])
    parallel2_clip = rect.clipline(parallel2[0], parallel2[1])
    
    # Return results
    return main_clip, parallel1_clip, parallel2_clip