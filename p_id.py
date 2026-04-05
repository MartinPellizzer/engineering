# TODO: create empty node (valid only as anchor point to draw arrows, hide when snapshotting)
# TODO: auto increment ids (text in circles) of nodes of same type

import pygame
import math

from lib import viewport

WINDOW_W, WINDOW_H = 1280, 720 

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("P_ID")

COLOR_BLUE = (0, 0, 255)
COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (10, 10, 10)

FONT_FAMILY_IBM_PLEX_MONO_REGULAR = 'fonts/IBM_Plex_Mono/IBMPlexMono-Regular.ttf'
FONT_FAMILY_IBM_PLEX_MONO_BOLD = 'fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'
font_family_text = FONT_FAMILY_IBM_PLEX_MONO_BOLD

font_size_base = 14
font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
font_debug = pygame.font.Font(font_family_text, 24 )

thing_stroke = 3
base_unit = 8

state = {
    'running': True,
    'inputs_context': '',
    'dragging': False,
    'drag_index': None,
    'drag_start_world': None,
    'drag_initial_positions': []
}

viewport_frame = {
    'x': 0,
    'y': 0,
    'w': WINDOW_W,
    'h': WINDOW_H,
}

'''
def screenshot_create_old():
    x1, y1, x2, y2 = None, None, None, None
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            thing_x, thing_y, thing_w, thing_h = thing_bbox_get(thing)
            if x1 == None: x1 = thing_x
            if y1 == None: y1 = thing_y
            if x2 == None: x2 = thing_x + thing_w
            if y2 == None: y2 = thing_y + thing_h
            if x1 > thing_x: x1 = thing_x
            if y1 > thing_y: y1 = thing_y
            if x2 < thing_x + thing_w: x2 = thing_x + thing_w
            if y2 < thing_y + thing_h: y2 = thing_y + thing_h
    x = x1
    y = y1
    w = x2 - x1
    h = y2 - y1
    rect = pygame.Rect(x, y, w, h)
    snapshot = screen.subsurface(rect).copy()
    pygame.image.save(snapshot, 'exports/diagram.png')
'''

def screenshot_create():
    rect = pygame.Rect(0, 0, WINDOW_W, WINDOW_H)
    snapshot = screen.subsurface(rect).copy()
    pygame.image.save(snapshot, 'exports/diagram.png')

def thing_create(
    _id, kind, subkind, text='', x=0, y=0, w=0, h=0, focus=False, node_start_id=None, node_end_id=None, edge_direction=0,
    w_min=0, h_min=0, text_lines=[], center_x=0, center_y=0, 
    socket_radius=None, socket_input_x=None, socket_input_y=None, socket_output_x=None, socket_output_y=None,
    sockets=[],
    points=None,
):
    thing = {
        'id': _id,
        'kind': kind,
        'subkind': subkind,
        'text': text,
        'text_lines': text_lines,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'w_min': w_min,
        'h_min': h_min,
        'center_x': center_x,
        'center_y': center_y,
        'focus': focus,
        'node_start_id': node_start_id,
        'node_end_id': node_end_id,
        'edge_direction': edge_direction,
        'socket_radius': socket_radius,
        'socket_input_x': socket_input_x,
        'socket_input_y': socket_input_y,
        'socket_output_x': socket_output_x,
        'socket_output_y': socket_output_y,
        'sockets': sockets,
        'points': points,
    }
    return thing

canvas = {
    'x': 0, 
    'y': 0, 
    'things': []
}

mouse = {
    'screen_x': 0,
    'screen_y': 0,
    'world_x': 0,
    'world_y': 0,
}

def node_create_solenoid_valve(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None:
        snap_x, snap_y = viewport.snap_to_grid(world_x, world_y)
    # pos by mouse coords
    else:
        snap_x, snap_y = viewport.snap_to_grid(mouse['world_x'], mouse['world_y'])
    _id = str(len(canvas['things'])+1)
    line_length = 32
    thing_w_world = line_length
    thing_h_world = int(line_length * 2.5)
    socket_radius = 4
    socket_input_x = 0 - socket_radius * 2
    socket_input_y = int(thing_h_world * 0.80) - (socket_radius//2)
    socket_input_x, socket_input_y = viewport.snap_to_grid_closest(socket_input_x, socket_input_y)
    socket_output_x = int(thing_w_world) + socket_radius * 2
    socket_output_y = int(thing_h_world * 0.80) - (socket_radius//2)
    socket_output_x, socket_output_y = viewport.snap_to_grid_closest(socket_output_x, socket_output_y)
    sockets = []
    sockets.append({'x': socket_input_x, 'y': socket_input_y})
    sockets.append({'x': socket_output_x, 'y': socket_output_y})
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'solenoid_valve', 
            text = '', 
            text_lines = [f'SV', f'01'], 
            x = snap_x, 
            y = snap_y,
            w = thing_w_world,
            h = thing_h_world,
            socket_radius = socket_radius,
            socket_input_x = socket_input_x,
            socket_input_y = socket_input_y,
            socket_output_x = int(thing_w_world) + socket_radius,
            socket_output_y = int(thing_h_world * 0.75) - (socket_radius//2),
            sockets = sockets,
        )
    )

def node_create_ozone_generator(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None: snap_x, snap_y = viewport.snap_to_grid_closest(world_x, world_y)
    # pos by mouse coords
    else: world_x, world_y = viewport.snap_to_grid_closest(mouse['world_x'], mouse['world_y'])
    ###
    _id = str(len(canvas['things'])+1)
    world_w = base_unit * 10
    world_h = base_unit * 16
    socket_radius = 4
    socket_0000_x, socket_0000_y = viewport.snap_to_grid_closest(-socket_radius * 10, world_h - (base_unit * 4))
    socket_0001_x, socket_0001_y = viewport.snap_to_grid_closest(world_w + socket_radius * 9, world_h - (base_unit * 4))
    sockets = []
    sockets.append({'x': socket_0000_x, 'y': socket_0000_y})
    sockets.append({'x': socket_0001_x, 'y': socket_0001_y})
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'ozone_generator', 
            text = '', 
            text_lines = [f'O3', f'01'], 
            x = world_x, 
            y = world_y,
            w = world_w,
            h = world_h,
            socket_radius = socket_radius,
            sockets = sockets,
        )
    )

def node_create_tank(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None: snap_x, snap_y = viewport.snap_to_grid_closest(world_x, world_y)
    # pos by mouse coords
    else: world_x, world_y = viewport.snap_to_grid_closest(mouse['world_x'], mouse['world_y'])
    ###
    _id = str(len(canvas['things'])+1)
    world_w = base_unit * 10
    world_h = base_unit * 16
    socket_radius = 4
    socket_0000_x, socket_0000_y = viewport.snap_to_grid_closest(
        (base_unit * 2),
        - (base_unit * 2),
    )
    sockets = []
    sockets.append({'x': socket_0000_x, 'y': socket_0000_y})
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'tank', 
            text = '', 
            text_lines = [f'TN', f'01'], 
            x = world_x, 
            y = world_y,
            w = world_w,
            h = world_h,
            socket_radius = socket_radius,
            sockets = sockets,
        )
    )

def node_create_valve_manual(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None: snap_x, snap_y = viewport.snap_to_grid_closest(world_x, world_y)
    # pos by mouse coords
    else: world_x, world_y = viewport.snap_to_grid_closest(mouse['world_x'], mouse['world_y'])
    ###
    _id = str(len(canvas['things'])+1)
    world_w = base_unit * 4
    world_h = base_unit * 6
    socket_radius = 4
    socket_0000_x, socket_0000_y = viewport.snap_to_grid_closest(-(base_unit), (base_unit * 4),)
    socket_0001_x, socket_0001_y = viewport.snap_to_grid_closest(world_w+(base_unit), (base_unit * 4),)
    sockets = []
    sockets.append({'x': socket_0000_x, 'y': socket_0000_y})
    sockets.append({'x': socket_0001_x, 'y': socket_0001_y})
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'valve_manual', 
            text = '', 
            text_lines = [f'MV', f'01'], 
            x = world_x, 
            y = world_y,
            w = world_w,
            h = world_h,
            socket_radius = socket_radius,
            sockets = sockets,
        )
    )

# ;jump
def node_create_plc(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None: snap_x, snap_y = viewport.snap_to_grid_closest(world_x, world_y)
    # pos by mouse coords
    else: world_x, world_y = viewport.snap_to_grid_closest(mouse['world_x'], mouse['world_y'])
    ###
    _id = str(len(canvas['things'])+1)
    world_w = base_unit * 8
    world_h = base_unit * 8
    socket_radius = 4
    socket_0000_x, socket_0000_y = viewport.snap_to_grid_closest((base_unit*4), (world_h + base_unit * 1),)
    sockets = []
    sockets.append({'x': socket_0000_x, 'y': socket_0000_y})
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'plc', 
            text = '', 
            text_lines = [f'PLC', f'01'], 
            x = world_x, 
            y = world_y,
            w = world_w,
            h = world_h,
            socket_radius = socket_radius,
            sockets = sockets,
        )
    )

def node_create(world_x=None, world_y=None):
    node_create_solenoid_valve(world_x, world_y)

def edge_create():
    _id = str(len(canvas['things'])+1)
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'edge', 
            subkind = '', 
        )
    )

def edge_create_advanced(points):
    _id = str(len(canvas['things'])+1)
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'edge', 
            subkind = '', 
            points = points, 
        )
    )

########################################

def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)

    dash_count = int(distance / dash_length)

    for i in range(0, dash_count, 2):
        start = (
            x1 + (dx / dash_count) * i,
            y1 + (dy / dash_count) * i
        )
        end = (
            x1 + (dx / dash_count) * (i + 1),
            y1 + (dy / dash_count) * (i + 1)
        )
        pygame.draw.line(surface, color, start, end, width)

def draw_grid():
    if viewport.state['visual_helpers'] == True:
        if viewport.state['grid_show'] == True:
            step = viewport.GRID_SIZE * viewport.state['camera_zoom']
            # Offset grid based on camera position
            offset_x = (-viewport.state['camera_x'] * viewport.state['camera_zoom']) % step
            offset_y = (-viewport.state['camera_y'] * viewport.state['camera_zoom']) % step
            # Vertical lines
            x = offset_x
            while x < WINDOW_W:
                pygame.draw.line(screen, (200, 200, 200), (int(x), 0), (int(x), WINDOW_H), 1)
                x += step
            # Horizontal lines
            y = offset_y
            while y < WINDOW_H:
                pygame.draw.line(screen, (200, 200, 200), (0, int(y)), (WINDOW_W, int(y)), 1)
                y += step

# node_create(world_x=100, world_y=100)
# node_create(world_x=200, world_y=200)

# edge_create()
# canvas['things'][2]['node_start_id'] = canvas['things'][0]['id']
# canvas['things'][2]['node_end_id'] = canvas['things'][1]['id']

# node_create_ozone_generator(world_x=400, world_y=200)
# node_create_tank(world_x=400, world_y=400)
# node_create_valve_manual(world_x=200, world_y=400)
# node_create_plc(world_x=600, world_y=100)

def node_by_id(_id):
    for thing in canvas['things']:
        if thing['id'] == _id:
            return thing
    return None

edge_tmp = {
    'points': [],
}

def draw_arrow(world_x1, world_y1, world_x2, world_y2):
        arrow_size = 8
        if world_x1 < world_x2:
            world_p1 = (world_x2 + arrow_size, world_y2)
            world_p2 = (world_x2, world_y2 + arrow_size)
            world_p3 = (world_x2, world_y2 - arrow_size)
        elif world_x1 > world_x2:
            world_p1 = (world_x2 - arrow_size, world_y2)
            world_p2 = (world_x2, world_y2 - arrow_size)
            world_p3 = (world_x2, world_y2 + arrow_size)
        else:
            if world_y1 < world_y2:
                world_p1 = (world_x2, world_y2 + arrow_size)
                world_p2 = (world_x2 - arrow_size, world_y2)
                world_p3 = (world_x2 + arrow_size, world_y2)
            else:
                world_p1 = (world_x2, world_y2 - arrow_size)
                world_p2 = (world_x2 + arrow_size, world_y2)
                world_p3 = (world_x2 - arrow_size, world_y2)
        screen_x1, screen_y1 = viewport.world_to_screen(world_p1[0], world_p1[1])
        screen_x2, screen_y2 = viewport.world_to_screen(world_p2[0], world_p2[1])
        screen_x3, screen_y3 = viewport.world_to_screen(world_p3[0], world_p3[1])
        screen_p1 = (screen_x1, screen_y1)
        screen_p2 = (screen_x2, screen_y2)
        screen_p3 = (screen_x3, screen_y3)
        screen_points = [screen_p1, screen_p2, screen_p3]
        pygame.draw.polygon(screen, COLOR_FOREGROUND, screen_points)

def draw_edges():
    for thing in canvas['things']:
        if thing['kind'] == 'edge':
            for point_i in range(len(thing['points'])-1):
                world_x1 = thing['points'][point_i]['x']
                world_y1 = thing['points'][point_i]['y']
                world_x2 = thing['points'][point_i+1]['x']
                world_y2 = thing['points'][point_i+1]['y']
                x1, y1 = viewport.world_to_screen(world_x1, world_y1)
                x2, y2 = viewport.world_to_screen(world_x2, world_y2)
                if thing['focus'] == False:
                    pygame.draw.line(screen, COLOR_FOREGROUND, 
                        (x1, y1), 
                        (x2, y2), 
                        int(thing_stroke * viewport.state['camera_zoom']),
                    )
                else:
                    pygame.draw.line(screen, COLOR_BLUE, 
                        (x1, y1), 
                        (x2, y2), 
                        int(thing_stroke * viewport.state['camera_zoom']),
                    )
            draw_arrow(world_x1, world_y1, world_x2, world_y2)

    global edge_tmp
    # if edge_tmp['points'] != []:
    if edge_creating == True:
        for point_i in range(len(edge_tmp['points'])-1):
            x1, y1 = viewport.world_to_screen(edge_tmp['points'][point_i]['x'], edge_tmp['points'][point_i]['y'])
            x2, y2 = viewport.world_to_screen(edge_tmp['points'][point_i+1]['x'], edge_tmp['points'][point_i+1]['y'])
            pygame.draw.line(screen, COLOR_FOREGROUND, 
                (x1, y1), 
                (x2, y2), 
                int(thing_stroke * viewport.state['camera_zoom']),
            )
        points_n = len(edge_tmp['points'])-1
        world_x1 = edge_tmp['points'][points_n]['x']
        world_y1 = edge_tmp['points'][points_n]['y']
        world_x2 = mouse['world_x']
        world_y2 = mouse['world_y']
        ###
        if abs(world_x2 - world_x1) > abs(world_y2 - world_y1): world_y2 = world_y1
        else: world_x2 = world_x1
        ###
        world_x2, world_y2 = viewport.snap_to_grid_closest(world_x2, world_y2)
        screen_x1, screen_y1 = viewport.world_to_screen(world_x1, world_y1)
        screen_x2, screen_y2 = viewport.world_to_screen(world_x2, world_y2)
        # x1, y1 = viewport.world_to_screen(world_x1, world_y1)
        # x2, y2 = mouse['screen_x'], mouse['screen_y']
        pygame.draw.line(screen, COLOR_FOREGROUND, 
            (screen_x1, screen_y1), 
            (screen_x2, screen_y2), 
            int(thing_stroke * viewport.state['camera_zoom']),
        )
        draw_arrow(world_x1, world_y1, world_x2, world_y2)

def draw_sockets(thing):
    if viewport.state['visual_helpers'] == True:
        thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
        thing_w = int(thing['w'] * viewport.state['camera_zoom'])
        thing_h = int(thing['h'] * viewport.state['camera_zoom'])
        for socket in thing['sockets']:
            socket_input_x = thing_x + (socket['x'] * viewport.state['camera_zoom'])
            socket_input_y = thing_y + (socket['y'] * viewport.state['camera_zoom'])
            pygame.draw.circle(screen, (255, 0, 0), 
                (socket_input_x, socket_input_y), 
                4*viewport.state['camera_zoom']
            )

def draw_nodes_valve(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(4 * viewport.state['camera_zoom'])
    ###
    p_1_x = thing_x
    p_1_y = thing_y
    p_2_x = thing_x + line_length
    p_2_y = thing_y
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x + line_length // 2
    p_1_y = thing_y
    p_2_x = thing_x + line_length // 2
    p_2_y = thing_y + line_length
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + line_length // 2
    p_2_x = thing_x
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + line_length // 2
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 1.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 0.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x + line_length
    p_1_y = thing_y + int(line_length * 0.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    lines = thing['text_lines']            
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = thing_x + int(line_length - line_w) // 2
        line_y = thing_y + int(line_length * 1.5) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ###
    socket_input_x = thing_x + (thing['sockets'][0]['x'] * viewport.state['camera_zoom'])
    socket_input_y = thing_y + (thing['sockets'][0]['y'] * viewport.state['camera_zoom'])
    pygame.draw.circle(screen, (255, 0, 0), 
        (socket_input_x, socket_input_y), 
        4*viewport.state['camera_zoom']
    )
    ###
    draw_sockets(thing)

def draw_node_solenoid_valve(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(thing_stroke * viewport.state['camera_zoom'])
    ### square top
    p_1_x = thing_x
    p_1_y = thing_y
    p_2_x = thing_x + line_length
    p_2_y = thing_y
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### square bottom
    p_1_x = thing_x
    p_1_y = thing_y + line_length
    p_2_x = thing_x + line_length
    p_2_y = thing_y + line_length
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### square left
    p_1_x = thing_x
    p_1_y = thing_y
    p_2_x = thing_x
    p_2_y = thing_y + line_length
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### square right
    p_1_x = thing_x + line_length
    p_1_y = thing_y
    p_2_x = thing_x + line_length
    p_2_y = thing_y + line_length
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### center line
    p_1_x = thing_x + int(line_length * 0.5)
    p_1_y = thing_y + int(line_length * 1)
    p_2_x = thing_x + int(line_length * 0.5)
    p_2_y = thing_y + int(line_length * 2)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### left
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 1.5)
    p_2_x = thing_x
    p_2_y = thing_y + int(line_length * 2.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 1.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 2.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 2.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x + line_length
    p_1_y = thing_y + int(line_length * 1.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 2.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### line bottom
    '''
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 2.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 2.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    '''
    ### text square
    surface = font_text.render('S', True, COLOR_FOREGROUND)
    line_w, line_h = surface.get_size()
    line_x = thing_x + int(line_length//2 - line_w//2)
    line_y = thing_y + int(line_length//2 - line_h//2)
    screen.blit(surface, (line_x, line_y))
    ### tag circle
    radius = int(24*viewport.state['camera_zoom'])
    circle_x = thing_x + int(line_length) + radius
    circle_y = thing_y + int(line_length * 2.5) + radius
    pygame.draw.circle(screen, (0, 0, 0), 
        (circle_x, circle_y), 
        radius,
        int(thing_stroke*viewport.state['camera_zoom']),
    )
    ### tag text
    lines = thing['text_lines']
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = circle_x - line_w//2
        line_y = circle_y - (line_h*(len(lines)-1)) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ### sockets
    draw_sockets(thing)

def draw_node_valve_manual(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(thing_stroke * viewport.state['camera_zoom'])
    ### square bottom
    p_1_x = thing_x
    p_1_y = thing_y
    p_2_x = thing_x + line_length
    p_2_y = thing_y
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### center line
    p_1_x = thing_x + int(line_length * 0.5)
    p_1_y = thing_y
    p_2_x = thing_x + int(line_length * 0.5)
    p_2_y = thing_y + int(line_length * 1)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### left
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 0.5)
    p_2_x = thing_x
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 0.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x
    p_1_y = thing_y + int(line_length * 1.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 0.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ###
    p_1_x = thing_x + line_length
    p_1_y = thing_y + int(line_length * 0.5)
    p_2_x = thing_x + line_length
    p_2_y = thing_y + int(line_length * 1.5)
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### tag circle
    radius = int(24*viewport.state['camera_zoom'])
    circle_x = thing_x + int(line_length) + radius
    circle_y = thing_y + int(line_length * 1.5) + radius
    pygame.draw.circle(screen, (0, 0, 0), 
        (circle_x, circle_y), 
        radius,
        int(thing_stroke*viewport.state['camera_zoom']),
    )
    ### tag text
    lines = thing['text_lines']
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = circle_x - line_w//2
        line_y = circle_y - (line_h*(len(lines)-1)) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ### sockets
    draw_sockets(thing)

def draw_node_ozone_generator(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    # line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(thing_stroke * viewport.state['camera_zoom'])
    unit = base_unit * viewport.state['camera_zoom']
    stroke_width_scaled = int(thing_stroke * viewport.state['camera_zoom'])
    ### square
    rect = pygame.Rect(
        thing_x,
        thing_y,
        thing_w,
        thing_h,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### square small 1
    rect = pygame.Rect(
        thing_x - (unit * 4), 
        thing_y + thing_h - (unit * 6), 
        unit * 4, 
        unit * 4,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### square small 2
    rect = pygame.Rect(
        thing_x + thing_w, 
        thing_y + thing_h - (unit * 6), 
        unit * 4, 
        unit * 4,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### text square
    surface = font_text.render('O3 GEN', True, COLOR_FOREGROUND)
    line_w, line_h = surface.get_size()
    line_x = thing_x + int(thing_w//2 - line_w//2)
    line_y = thing_y + int(thing_h//2 - line_h//2)
    screen.blit(surface, (line_x, line_y))
    ### tag circle
    radius = int(24*viewport.state['camera_zoom'])
    circle_x = thing_x + int(thing_w) + radius
    circle_y = thing_y + int(thing_h) + radius
    pygame.draw.circle(screen, (0, 0, 0), 
        (circle_x, circle_y), 
        radius,
        int(thing_stroke*viewport.state['camera_zoom']),
    )
    ### tag text
    lines = thing['text_lines']
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = circle_x - line_w//2
        line_y = circle_y - (line_h*(len(lines)-1)) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ### sockets
    draw_sockets(thing)

def draw_node_tank(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    # line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(thing_stroke * viewport.state['camera_zoom'])
    unit = base_unit * viewport.state['camera_zoom']
    stroke_width_scaled = int(thing_stroke * viewport.state['camera_zoom'])
    ### square
    rect = pygame.Rect(
        thing_x,
        thing_y,
        thing_w,
        thing_h,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### square small 1
    rect = pygame.Rect(
        thing_x + thing_w//2 - (unit * 2), 
        thing_y - (unit * 4), 
        unit * 4, 
        unit * 4,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### text square
    surface = font_text.render('TANK', True, COLOR_FOREGROUND)
    line_w, line_h = surface.get_size()
    line_x = thing_x + int(thing_w//2 - line_w//2)
    line_y = thing_y + int(thing_h//2 - line_h//2)
    screen.blit(surface, (line_x, line_y))
    ### tag circle
    radius = int(24*viewport.state['camera_zoom'])
    circle_x = thing_x + int(thing_w) + radius
    circle_y = thing_y + int(thing_h) + radius
    pygame.draw.circle(screen, (0, 0, 0), 
        (circle_x, circle_y), 
        radius,
        int(thing_stroke*viewport.state['camera_zoom']),
    )
    ### tag text
    lines = thing['text_lines']
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = circle_x - line_w//2
        line_y = circle_y - (line_h*(len(lines)-1)) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ### sockets
    draw_sockets(thing)

# ;jump
def draw_node_plc(thing):
    thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
    thing_w = int(thing['w'] * viewport.state['camera_zoom'])
    thing_h = int(thing['h'] * viewport.state['camera_zoom'])
    ###
    # line_length = int(thing['w'] * viewport.state['camera_zoom'])
    line_width = int(thing_stroke * viewport.state['camera_zoom'])
    unit = base_unit * viewport.state['camera_zoom']
    stroke_width_scaled = int(thing_stroke * viewport.state['camera_zoom'])
    ### square
    rect = pygame.Rect(
        thing_x,
        thing_y,
        thing_w,
        thing_h,
    )
    inflated_rect = rect.inflate(stroke_width_scaled, stroke_width_scaled)
    pygame.draw.rect(screen, COLOR_FOREGROUND, inflated_rect, line_width)
    ### line 1
    p_1_x = thing_x 
    p_1_y = thing_y + thing_h//2
    p_2_x = thing_x + thing_w//2
    p_2_y = thing_y
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### line 2
    p_1_x = thing_x + thing_w//2
    p_1_y = thing_y
    p_2_x = thing_x + thing_w
    p_2_y = thing_y + thing_h//2
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### line 3
    p_1_x = thing_x + thing_w
    p_1_y = thing_y + thing_h//2
    p_2_x = thing_x + thing_w//2
    p_2_y = thing_y + thing_h
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### line 4
    p_1_x = thing_x + thing_w//2
    p_1_y = thing_y + thing_h
    p_2_x = thing_x
    p_2_y = thing_y + thing_h//2
    pygame.draw.line(screen, COLOR_FOREGROUND, (p_1_x, p_1_y), (p_2_x, p_2_y), line_width)
    ### text square
    surface = font_text.render('PLC', True, COLOR_FOREGROUND)
    line_w, line_h = surface.get_size()
    line_x = thing_x + int(thing_w//2 - line_w//2)
    line_y = thing_y + int(thing_h//2 - line_h//2)
    screen.blit(surface, (line_x, line_y))
    ### tag circle
    radius = int(24*viewport.state['camera_zoom'])
    circle_x = thing_x + int(thing_w) + radius
    circle_y = thing_y + int(thing_h) + radius
    pygame.draw.circle(screen, (0, 0, 0), 
        (circle_x, circle_y), 
        radius,
        int(thing_stroke*viewport.state['camera_zoom']),
    )
    ### tag text
    lines = thing['text_lines']
    for line_i, line in enumerate(lines):
        surface = font_text.render(line, True, COLOR_FOREGROUND)
        line_w, line_h = surface.get_size()
        line_x = circle_x - line_w//2
        line_y = circle_y - (line_h*(len(lines)-1)) + (line_h * line_i)
        screen.blit(surface, (line_x, line_y))
    ### focus
    if thing['focus'] == True:
        pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)
    ### sockets
    draw_sockets(thing)

def draw_nodes():
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            if thing['subkind'] == 'solenoid_valve':
                draw_node_solenoid_valve(thing)
            elif thing['subkind'] == 'ozone_generator':
                draw_node_ozone_generator(thing)
            elif thing['subkind'] == 'tank':
                draw_node_tank(thing)
            elif thing['subkind'] == 'valve_manual':
                draw_node_valve_manual(thing)
            elif thing['subkind'] == 'plc':
                draw_node_plc(thing)

def draw_debug():
    if viewport.state['visual_helpers'] == True:
        if viewport.state['debug_show'] == True:
            y_cur = 0
            surface = font_debug.render(f'''{mouse['screen_x']}:{mouse['screen_y']}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            world_x, world_y = int(mouse['world_x']), int(mouse['world_y'])
            surface = font_debug.render(f'''{world_x}:{world_y}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            world_x, world_y = viewport.snap_to_grid(world_x, world_y)
            surface = font_debug.render(f'''{world_x}:{world_y}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            surface = font_debug.render(f'''{viewport.state['camera_zoom']}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30

def draw_viewport():
    screen.set_clip((viewport_frame['x'], viewport_frame['y'], viewport_frame['w'], viewport_frame['h']))
    draw_grid()
    draw_edges()
    draw_nodes()
    draw_debug()
    screen.set_clip(None)

def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_viewport()
    pygame.display.flip()

def node_drag_end():
    state['dragging'] = False
    state['drag_index'] = None

def node_drag_run():
    if state['dragging']:
        dx = mouse['world_x'] - state['drag_start_world'][0]
        dy = mouse['world_y'] - state['drag_start_world'][1]
        new_x = state['drag_start_world'][0] + dx
        new_y = state['drag_start_world'][1] + dy
        new_x, new_y = viewport.snap_to_grid(new_x, new_y)
        thing = canvas['things'][state['drag_index']]
        thing["x"] = new_x
        thing["y"] = new_y

def socket_screen_coords_center_get(thing, socket):
    thing_screen_x, thing_screen_y = viewport.world_to_screen(thing['x'], thing['y'])
    socket_screen_x = thing_screen_x + int(socket['x'] * viewport.state['camera_zoom'])
    socket_screen_y = thing_screen_y + int(socket['y'] * viewport.state['camera_zoom'])
    return socket_screen_x, socket_screen_y

def socket_screen_bbox_get(thing, socket):
    socket_screen_x, socket_screen_y = socket_screen_coords_center_get(thing, socket)
    socket_screen_radius = int(thing['socket_radius'] * viewport.state['camera_zoom'])
    socket_screen_x1 = socket_screen_x - socket_screen_radius
    socket_screen_y1 = socket_screen_y - socket_screen_radius
    socket_screen_x2 = socket_screen_x + socket_screen_radius
    socket_screen_y2 = socket_screen_y + socket_screen_radius
    return socket_screen_x1, socket_screen_y1, socket_screen_x2, socket_screen_y2

edge_creating = False

def mouse_left_button_socket():
    for thing_i, thing in enumerate(canvas['things']):
        if thing['kind'] == 'node':
            for socket in thing['sockets']:
                socket_screen_x1, socket_screen_y1, socket_screen_x2, socket_screen_y2 = socket_screen_bbox_get(thing, socket)
                if (
                    mouse['screen_x'] > socket_screen_x1 and mouse['screen_x'] < socket_screen_x2 and 
                    mouse['screen_y'] > socket_screen_y1 and mouse['screen_y'] < socket_screen_y2
                ):
                    socket_screen_center_x, socket_screen_center_y = socket_screen_coords_center_get(thing, socket)
                    socket_world_center_x, socket_world_center_y = viewport.screen_to_world(socket_screen_center_x, socket_screen_center_y)
                    # start edge (update -> if not started)
                    global edge_creating
                    global edge_tmp
                    if edge_creating == False:
                        edge_creating = True
                        # world_x2, world_y2 = viewport.snap_to_grid(socket_world_center_x, socket_world_center_y)
                        world_x2, world_y2 = viewport.snap_to_grid_closest(socket_world_center_x, socket_world_center_y)
                        edge_tmp['points'].append({'x': world_x2, 'y': world_y2})
                    else:
                        edge_creating = False
                        world_x2, world_y2 = viewport.snap_to_grid_closest(socket_world_center_x, socket_world_center_y)
                        edge_tmp['points'].append({'x': world_x2, 'y': world_y2})
                        edge_create_advanced(edge_tmp['points'])
                        edge_tmp['points'] = []
                    # end edge (update -> if started)
                    # TODO
                    # return confirmation clicked socket
                    return True
                    break
    return False

def mouse_left_button_canvas():
    global edge_creating
    global edge_tmp
    if edge_creating == True:
        points_n = len(edge_tmp['points'])-1
        world_x1 = edge_tmp['points'][points_n]['x']
        world_y1 = edge_tmp['points'][points_n]['y']
        world_x2 = mouse['world_x']
        world_y2 = mouse['world_y']
        ###
        # screen_x1, screen_y1 = viewport.world_to_screen(, edge_tmp['points'][points_n]['y'])
        # screen_x2, screen_y2 = mouse['screen_x'], mouse['screen_y']
        # if abs(screen_x2 - screen_x1) > abs(screen_y2 - screen_y1): screen_y2 = screen_y1
        # else: screen_x2 = screen_x1
        # world_x2, world_y2 = viewport.screen_to_world(screen_x2, screen_y2)
        # world_x2, world_y2 = viewport.snap_to_grid(world_x2, world_y2)
        if abs(world_x2 - world_x1) > abs(world_y2 - world_y1): world_y2 = world_y1
        else: world_x2 = world_x1
        # world_x2, world_y2 = viewport.snap_to_grid(world_x2, world_y2)
        world_x2, world_y2 = viewport.snap_to_grid_closest(world_x2, world_y2)
        edge_tmp['points'].append({'x': world_x2, 'y': world_y2})
        print(f'{world_x2}:{world_y2}')
    return True

def mouse_left_button_node():
    for thing_i, thing in enumerate(canvas['things']):
        if thing['kind'] == 'node':
            thing_screen_x, thing_screen_y = viewport.world_to_screen(thing['x'], thing['y'])
            thing_screen_w = thing['w'] * viewport.state['camera_zoom']
            thing_screen_h = thing['h'] * viewport.state['camera_zoom']
            if (
                mouse['screen_x'] > thing_screen_x and mouse['screen_x'] < thing_screen_x + thing_screen_w and 
                mouse['screen_y'] > thing_screen_y and mouse['screen_y'] < thing_screen_y + thing_screen_h
            ):
                thing['focus'] = True
                state['dragging'] = True
                state['drag_index'] = thing_i
                state['drag_start_world'] = (thing_screen_x, thing_screen_y)
                return True
                break
    return False

def mouse_left_button_edge():
    if edge_creating == False:
        for thing_i, thing in enumerate(canvas['things']):
            if thing['kind'] == 'edge':
                for point_i in range(len(thing['points'])-1):
                    x1, y1 = viewport.world_to_screen(thing['points'][point_i]['x'], thing['points'][point_i]['y'])
                    x2, y2 = viewport.world_to_screen(thing['points'][point_i+1]['x'], thing['points'][point_i+1]['y'])
                    ###
                    if x1 < x2 or y1 < y2:
                        x1_dir = x1 - int(4 * viewport.state['camera_zoom'])
                        y1_dir = y1 - int(4 * viewport.state['camera_zoom'])
                        x2_dir = x2 + int(4 * viewport.state['camera_zoom'])
                        y2_dir = y2 + int(4 * viewport.state['camera_zoom'])
                    else:
                        x1_dir = x2 - int(4 * viewport.state['camera_zoom'])
                        y1_dir = y2 - int(4 * viewport.state['camera_zoom'])
                        x2_dir = x1 + int(4 * viewport.state['camera_zoom'])
                        y2_dir = y1 + int(4 * viewport.state['camera_zoom'])
                    '''
                    else:
                        if y1 < y2:
                            x1_dir = x1 - int(4 * viewport.state['camera_zoom'])
                            y1_dir = y1 - int(4 * viewport.state['camera_zoom'])
                            x2_dir = x2 + int(4 * viewport.state['camera_zoom'])
                            y2_dir = y2 + int(4 * viewport.state['camera_zoom'])
                    '''
                    if (
                        mouse['screen_x'] > x1_dir and mouse['screen_x'] < x2_dir and 
                        mouse['screen_y'] > y1_dir and mouse['screen_y'] < y2_dir
                    ):
                        thing['focus'] = True

                        return True
                        break
    return False

def inputs_mouse_left_button():
    for thing_i, thing in enumerate(canvas['things']):
        thing['focus'] = False
    if mouse_left_button_socket(): return
    if mouse_left_button_node(): return
    if mouse_left_button_edge(): return
    if mouse_left_button_canvas(): return

def main_inputs():
    global font_text
    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = viewport.screen_to_world(mouse['screen_x'], mouse['screen_y'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['running'] = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    for thing_i, thing in enumerate(canvas['things']):
                        if thing['focus'] == True:
                            del canvas['things'][thing_i]
                elif event.key == pygame.K_o:
                    node_create_ozone_generator(world_x=mouse['world_x'], world_y=mouse['world_y'])
                elif event.key == pygame.K_t:
                    node_create_tank(world_x=mouse['world_x'], world_y=mouse['world_y'])
                elif event.key == pygame.K_s:
                    node_create_solenoid_valve(world_x=mouse['world_x'], world_y=mouse['world_y'])
                elif event.key == pygame.K_m:
                    node_create_valve_manual(world_x=mouse['world_x'], world_y=mouse['world_y'])
                elif event.key == pygame.K_p:
                    node_create_plc(world_x=mouse['world_x'], world_y=mouse['world_y'])
                elif event.key == pygame.K_d:
                    if viewport.state['visual_helpers'] == True: viewport.state['visual_helpers'] = False
                    else: viewport.state['visual_helpers'] = True
                elif event.key == pygame.K_e: 
                    screenshot_create()
                elif event.unicode == "{":
                    print("Left curly bracket")
                    viewport.zoom_from_center('down', 1, 'add', 'int', WINDOW_W//2, WINDOW_H//2)
                    font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
                elif event.unicode == "}":
                    print("Right curly bracket")
                    viewport.zoom_from_center('up', 1, 'add', 'int', WINDOW_W//2, WINDOW_H//2)
                    font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                inputs_mouse_left_button()
            elif event.button == 2:
                viewport.pan_start(mouse['screen_x'], mouse['screen_y'])
            elif event.button == 3:
                node_create()
            elif event.button == 4:
                viewport.zoom_run(direction='up', mouse_screen_x=mouse['screen_x'], mouse_screen_y=mouse['screen_y'])
                font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
            elif event.button == 5:
                viewport.zoom_run(direction='down', mouse_screen_x=mouse['screen_x'], mouse_screen_y=mouse['screen_y'])
                font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
        elif event.type == pygame.MOUSEMOTION:
            node_drag_run()
            viewport.pan_run(mouse['screen_x'], mouse['screen_y'])
        elif event.type == pygame.MOUSEBUTTONUP:
            node_drag_end()
            if event.button == 2:
                viewport.pan_end()

def main():
    while state['running']:

        main_inputs()
        main_draw()

        clock.tick(60)

    pygame.quit()

main()
