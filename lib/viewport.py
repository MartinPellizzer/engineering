GRID_SIZE = 64

MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
panning = False
pan_last_x = 0
pan_last_y = 0

state = {
    'panning': False,
    'pan_last_x': 0,
    'pan_last_y': 0,
    'camera_x': 0,
    'camera_y': 0,
    'camera_zoom': 1.0,
    'grid_show': False,
}

def world_to_screen(x, y):
    sx = (x - state['camera_x']) * state['camera_zoom']
    sy = (y - state['camera_y']) * state['camera_zoom']
    return int(sx), int(sy)

def screen_to_world(x, y):
    wx = (x / state['camera_zoom']) + state['camera_x']
    wy = (y / state['camera_zoom']) + state['camera_y']
    return wx, wy

def thing_coordinates_get(thing):
    x, y = world_to_screen(thing["x"], thing["y"])
    w, h = thing['w'] * state['camera_zoom'], thing['h'] * state['camera_zoom']
    return x, y, w, h

def snap_to_grid(x, y):
    x = round(x // GRID_SIZE) * GRID_SIZE
    y = round(y // GRID_SIZE) * GRID_SIZE
    return x, y

def thing_focused_get(things):
    for thing_i, thing in enumerate(things['things']):
        if thing['focus'] == True:
            return thing
    return None

################################################################################
# NAVIGATION
################################################################################

def pan_start(mouse_screen_x, mouse_screen_y):
    state['panning'] = True
    state['pan_last_x'], state['pan_last_y'] = mouse_screen_x, mouse_screen_y

def pan_run(mouse_screen_x, mouse_screen_y):
    if state['panning']:
        dx = mouse_screen_x - state['pan_last_x']
        dy = mouse_screen_y - state['pan_last_y']
        state['camera_x'] -= dx / state['camera_zoom']
        state['camera_y'] -= dy / state['camera_zoom']
        state['pan_last_x'] = mouse_screen_x
        state['pan_last_y'] = mouse_screen_y

def pan_end():
    state['panning'] = False

def zoom_run(direction, mouse_screen_x, mouse_screen_y):
    # world position before zoom
    before_x, before_y = screen_to_world(mouse_screen_x, mouse_screen_y)

    if direction == 'up':
        state['camera_zoom'] *= 1.1
        state['camera_zoom'] = min(state['camera_zoom'], MAX_ZOOM)

    elif direction == 'down':
        state['camera_zoom'] /= 1.1
        state['camera_zoom'] = max(state['camera_zoom'], MIN_ZOOM)

    # world position after zoom
    after_x, after_y = screen_to_world(mouse_screen_x, mouse_screen_y)

    # adjust camera so point under cursor stays fixed
    state['camera_x'] += before_x - after_x
    state['camera_y'] += before_y - after_y

################################################################################
# DRAW
################################################################################

