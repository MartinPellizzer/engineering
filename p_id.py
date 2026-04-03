# TODO: create list of sockets in "thing", not "input" and "output" sockets
# TODO: create edge while clicking on sockets
# TODO: create new components (nodes)

import pygame

from lib import viewport

WINDOW_W, WINDOW_H = 1280, 720 

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("P_ID")

COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (10, 10, 10)

FONT_FAMILY_IBM_PLEX_MONO = 'fonts/IBM_Plex_Mono/IBMPlexMono-Regular.ttf'
font_family_text = FONT_FAMILY_IBM_PLEX_MONO

font_size_base = 16
font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
font_debug = pygame.font.Font(font_family_text, 24 )

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

def thing_create(
    _id, kind, subkind, text='', x=0, y=0, w=0, h=0, focus=False, node_start_id=None, node_end_id=None, edge_direction=0,
    w_min=0, h_min=0, text_lines=[], center_x=0, center_y=0, 
    socket_radius=None, socket_input_x=None, socket_input_y=None, socket_output_x=None, socket_output_y=None,
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

def node_create(world_x=None, world_y=None):
    # pos by parameters
    if world_x != None and world_y != None:
        snap_x, snap_y = viewport.snap_to_grid(world_x, world_y)
    # pos by mouse coords
    else:
        snap_x, snap_y = viewport.snap_to_grid(mouse['world_x'], mouse['world_y'])
    _id = str(len(canvas['things'])+1)
    line_length = 32
    thing_w_world = line_length
    thing_h_world = int(line_length * 1.5)
    socket_radius = 4
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'valve', 
            text = '', 
            text_lines = [f'FV', f'01'], 
            x = snap_x, 
            y = snap_y,
            w = thing_w_world,
            h = thing_h_world,
            w_min = viewport.GRID_SIZE * 4,
            h_min = viewport.GRID_SIZE,
            socket_radius = socket_radius,
            socket_input_x = 0 - socket_radius,
            socket_input_y = int(thing_h_world * 0.75) - (socket_radius//2),
            socket_output_x = int(thing_w_world) + socket_radius,
            socket_output_y = int(thing_h_world * 0.75) - (socket_radius//2),
        )
    )

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

def draw_grid():
    if viewport.state['grid_show']:
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

node_create(world_x=100, world_y=100)
node_create(world_x=200, world_y=200)

# edge_create()
# canvas['things'][2]['node_start_id'] = canvas['things'][0]['id']
# canvas['things'][2]['node_end_id'] = canvas['things'][1]['id']

def node_by_id(_id):
    for thing in canvas['things']:
        if thing['id'] == _id:
            return thing
    return None

edge_tmp = {
    'points': [],
}

def draw_edges():
    '''
    for thing in canvas['things']:
        if thing['kind'] == 'edge':
            node_start = node_by_id(thing['node_start_id'])
            node_end = node_by_id(thing['node_end_id'])
            node_start_x, node_start_y = socket_screen_coords_center_get(node_start, socket='output')
            node_end_x, node_end_y = socket_screen_coords_center_get(node_end, socket='input')
            x1, y1 = node_start_x, node_start_y
            x2, y2 = node_start_x, node_end_y
            x3, y3 = node_end_x, node_end_y
            pygame.draw.line(screen, COLOR_FOREGROUND, 
                (x1, y1), (x2, y2), 
                int(4 * viewport.state['camera_zoom']),
            )
            pygame.draw.line(screen, COLOR_FOREGROUND, 
                (x2 - int(4//2 * viewport.state['camera_zoom']), y2), (x3, y3), 
                int(4 * viewport.state['camera_zoom']),
            )
    '''

    for thing in canvas['things']:
        if thing['kind'] == 'edge':
            print(len(thing['points']))
            for point_i in range(len(thing['points'])-1):
                x1, y1 = viewport.world_to_screen(thing['points'][point_i]['x'], thing['points'][point_i]['y'])
                x2, y2 = viewport.world_to_screen(thing['points'][point_i+1]['x'], thing['points'][point_i+1]['y'])
                pygame.draw.line(screen, COLOR_FOREGROUND, 
                    (x1, y1), 
                    (x2, y2), 
                    int(4 * viewport.state['camera_zoom']),
                )

    global edge_tmp
    '''
    if edge_creating == True:
        x1, y1 = viewport.world_to_screen(edge_tmp['points'][0]['x'], edge_tmp['points'][0]['y'])
        # x1, y1 = edge_tmp['points'][0]['x'], edge_tmp['points'][0]['y']
        x2, y2 = mouse['world_x'], mouse['world_y']
        pygame.draw.line(screen, COLOR_FOREGROUND, 
            (x1, y1), (x2, y2), 
            int(4 * viewport.state['camera_zoom']),
        )
    '''
    # if edge_tmp['points'] != []:
    if edge_creating == True:
        for point_i in range(len(edge_tmp['points'])-1):
            x1, y1 = viewport.world_to_screen(edge_tmp['points'][point_i]['x'], edge_tmp['points'][point_i]['y'])
            x2, y2 = viewport.world_to_screen(edge_tmp['points'][point_i+1]['x'], edge_tmp['points'][point_i+1]['y'])
            pygame.draw.line(screen, COLOR_FOREGROUND, 
                (x1, y1), 
                (x2, y2), 
                int(4 * viewport.state['camera_zoom']),
            )
        points_n = len(edge_tmp['points'])-1
        x1, y1 = viewport.world_to_screen(edge_tmp['points'][points_n]['x'], edge_tmp['points'][points_n]['y'])
        x2, y2 = mouse['screen_x'], mouse['screen_y']
        pygame.draw.line(screen, COLOR_FOREGROUND, 
            (x1, y1), 
            (x2, y2), 
            int(4 * viewport.state['camera_zoom']),
        )

def draw_nodes():
    for thing in canvas['things']:
        if thing['kind'] == 'node':
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
            socket_input_x = thing_x + (thing['socket_input_x'] * viewport.state['camera_zoom'])
            socket_input_y = thing_y + (thing['socket_input_y'] * viewport.state['camera_zoom'])
            pygame.draw.circle(screen, (255, 0, 0), 
                (socket_input_x, socket_input_y), 
                4*viewport.state['camera_zoom']
            )
            ###
            socket_output_x = thing_x + (thing['socket_output_x'] * viewport.state['camera_zoom'])
            socket_output_y = thing_y + (thing['socket_output_y'] * viewport.state['camera_zoom'])
            pygame.draw.circle(screen, (255, 0, 0), 
                (socket_output_x, socket_output_y), 
                4*viewport.state['camera_zoom']
            )

def draw_debug():
    if viewport.state['debug_show']:
        y_cur = 0
        surface = font_debug.render(f'''{mouse['screen_x']}:{mouse['screen_y']}''', True, (255, 0, 255))
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
    if socket == 'input':
        socket_screen_x = thing_screen_x + int(thing['socket_input_x'] * viewport.state['camera_zoom'])
        socket_screen_y = thing_screen_y + int(thing['socket_input_y'] * viewport.state['camera_zoom'])
    elif socket == 'output':
        socket_screen_x = thing_screen_x + int(thing['socket_output_x'] * viewport.state['camera_zoom'])
        socket_screen_y = thing_screen_y + int(thing['socket_output_y'] * viewport.state['camera_zoom'])
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
            socket_screen_x1, socket_screen_y1, socket_screen_x2, socket_screen_y2 = socket_screen_bbox_get(thing, socket='input')
            if (
                mouse['screen_x'] > socket_screen_x1 and mouse['screen_x'] < socket_screen_x2 and 
                mouse['screen_y'] > socket_screen_y1 and mouse['screen_y'] < socket_screen_y2
            ):
                socket_screen_center_x, socket_screen_center_y = socket_screen_coords_center_get(thing, socket='input')
                socket_world_center_x, socket_world_center_y = viewport.screen_to_world(socket_screen_center_x, socket_screen_center_y)
                # start edge (update -> if not started)
                global edge_creating
                global edge_tmp
                if edge_creating == False:
                    edge_creating = True
                    edge_tmp['points'].append({'x': socket_world_center_x, 'y': socket_world_center_y})
                else:
                    edge_creating = False
                    edge_tmp['points'].append({'x': socket_world_center_x, 'y': socket_world_center_y})
                    edge_create_advanced(edge_tmp['points'])
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
        print('mouse_left_button_canvas')
        edge_tmp['points'].append({'x': mouse['world_x'], 'y': mouse['world_y']})
    return True

def mouse_left_button_node():
    for thing_i, thing in enumerate(canvas['things']):
        if thing['kind'] == 'node':
            thing_screen_x, thing_screen_y = viewport.world_to_screen(thing['x'], thing['y'])
            thing_screen_w = thing['w'] * viewport.state['camera_zoom']
            thing_screen_h = thing['h'] * viewport.state['camera_zoom']
            thing['focus'] = False
            if (
                mouse['screen_x'] > thing_screen_x and mouse['screen_x'] < thing_screen_x + thing_screen_w and 
                mouse['screen_y'] > thing_screen_y and mouse['screen_y'] < thing_screen_y + thing_screen_h
            ):
                thing['focus'] = True
                state['dragging'] = True
                state['drag_index'] = thing_i
                state['drag_start_world'] = (thing_screen_x, thing_screen_y)
                # state['drag_start_world'] = mouse_world_x, mouse_world_y
                return True
                break
    return False


def inputs_mouse_left_button():
    if mouse_left_button_socket(): return
    if mouse_left_button_node(): return
    if mouse_left_button_canvas(): return

def main_inputs():
    global font_text
    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = viewport.screen_to_world(mouse['screen_x'], mouse['screen_y'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['running'] = False
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
