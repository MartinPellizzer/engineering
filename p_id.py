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
    _id, kind, subkind, text='', x=0, y=0, w=0, h=0, focus=False, node_start=None, node_end=None, edge_direction=0,
    w_min=0, h_min=0, text_lines=[],
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
        'focus': focus,
        'node_start': node_start,
        'node_end': node_end,
        'edge_direction': edge_direction,
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

def node_create():
    snap_x, snap_y = viewport.snap_to_grid(mouse['world_x'], mouse['world_y'])
    _id = str(len(canvas['things'])+1)
    line_length = 30
    thing_w_world = line_length
    thing_h_world = int(line_length * 1.5)
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'valve', 
            text = '', 
            text_lines = [f'Gate', f'Valve'], 
            x = snap_x, 
            y = snap_y,
            w = thing_w_world,
            h = thing_h_world,
            w_min = viewport.GRID_SIZE * 4,
            h_min = viewport.GRID_SIZE,
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

def draw_nodes():
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            thing_x, thing_y = viewport.world_to_screen(thing["x"], thing["y"])
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
            ###
            if thing['focus'] == True:
                thing_w = int(thing['w'] * viewport.state['camera_zoom'])
                thing_h = int(thing['h'] * viewport.state['camera_zoom'])
                pygame.draw.rect(screen, (0, 0, 255), (thing_x, thing_y, thing_w, thing_h), 1)

def draw_debug():
    if viewport.state['debug_show']:
        y_cur = 0
        surface = font_debug.render(f'''{mouse['screen_x']}:{mouse['screen_y']}''', True, (255, 0, 255))
        screen.blit(surface, (0, y_cur))
        y_cur += 30

def draw_viewport():
    screen.set_clip((viewport_frame['x'], viewport_frame['y'], viewport_frame['w'], viewport_frame['h']))
    draw_grid()
    draw_nodes()
    draw_debug()
    screen.set_clip(None)

def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_viewport()
    pygame.display.flip()

def node_drag_start():
    for thing_i, thing in enumerate(canvas['things']):
        # x, y, w, h = thing_bbox_get(thing)
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

def main_inputs():
    global font_text
    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = viewport.screen_to_world(mouse['screen_x'], mouse['screen_y'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['running'] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                node_drag_start()
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
