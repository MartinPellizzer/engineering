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

state = {
    'running': True,
    'inputs_context': '',
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
    canvas['things'].append(
        thing_create(
            _id,
            kind = 'node', 
            subkind = 'valve', 
            text = '', 
            text_lines = [f'Gate', f'Valve'], 
            x = snap_x, 
            y = snap_y,
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
            line_length = int(30 * viewport.state['camera_zoom'])
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

def draw_viewport():
    screen.set_clip((viewport_frame['x'], viewport_frame['y'], viewport_frame['w'], viewport_frame['h']))
    draw_grid()
    draw_nodes()
    screen.set_clip(None)

def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_viewport()
    pygame.display.flip()

def main_inputs():
    global font_text
    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = viewport.screen_to_world(mouse['screen_x'], mouse['screen_y'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['running'] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                pass
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
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                viewport.pan_end()
        elif event.type == pygame.MOUSEMOTION:
            viewport.pan_run(mouse['screen_x'], mouse['screen_y'])

def main():
    while state['running']:

        main_inputs()
        main_draw()

        clock.tick(60)

    pygame.quit()

main()
