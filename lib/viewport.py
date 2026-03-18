MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
camera_x = 0
camera_y = 0
camera_zoom = 1.0
panning = False
pan_last_x = 0
pan_last_y = 0

def world_to_screen(x, y):
    sx = (x - camera_x) * camera_zoom
    sy = (y - camera_y) * camera_zoom
    return int(sx), int(sy)

def screen_to_world(x, y):
    wx = (x / camera_zoom) + camera_x
    wy = (y / camera_zoom) + camera_y
    return wx, wy

