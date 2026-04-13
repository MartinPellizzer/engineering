import math

import pygame

from lib import viewport

pygame.init()
clock = pygame.time.Clock()

WINDOW_W, WINDOW_H = 1280, 720
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("KNOWLEDGE GRAPH")

COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (0, 0, 0)
COLOR_ELEMENT_FOCUS = (0, 0, 255)

FONT_FAMILY_IBM_PLEX_MONO = 'fonts/IBM_Plex_Mono/IBMPlexMono-Regular.ttf'

font_family_text = FONT_FAMILY_IBM_PLEX_MONO

font_size_base = 8
font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))

game = {
    'running': True,
}

leftbar_frame = {
    'x': 0,
    'y': 0,
    'w': 200,
    'h': WINDOW_H,
}

viewport_frame = {
    'x': 200,
    'y': 0,
    'w': WINDOW_W - 200,
    'h': WINDOW_H,
}

mouse = {
    'screen_x': 0,
    'screen_y': 0,
    'world_x': 0,
    'world_y': 0,
}

dragging = False
drag_index = None
drag_start_world = None

def thing_create(
    _id, kind, text='', x=0, y=0, w=0, h=0, focus=False, node_start=None, node_end=None, edge_direction=0,
    w_min=0, h_min=0, text_lines=[],
):
    thing = {
        'id': _id,
        'kind': kind,
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

def node_create():
    snap_x, snap_y = viewport.snap_to_grid(mouse['world_x'], mouse['world_y'])
    canvas['things'].append(
        thing_create(
            str(len(canvas['things'])+1), 
            kind = 'node', 
            text = '', 
            text_lines = ['???'], 
            x = snap_x, 
            y = snap_y,
            w_min = viewport.GRID_SIZE * 4,
            h_min = viewport.GRID_SIZE,
        )
    )
    print(canvas['things'])

def node_drag_start():
    global dragging
    global drag_index
    global drag_start_world
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = thing_bbox(thing)
        thing['focus'] = False
        if (
            mouse['screen_x'] > x and mouse['screen_x'] < x + w and 
            mouse['screen_y'] > y and mouse['screen_y'] < y + h
        ):
            thing['focus'] = True
            dragging = True
            drag_index = thing_i
            drag_start_world = (x, y)
            # drag_start_world = mouse_world_x, mouse_world_y

def node_drag_run():
    if dragging:
        dx = mouse['world_x'] - drag_start_world[0]
        dy = mouse['world_y'] - drag_start_world[1]
        new_x = drag_start_world[0] + dx
        new_y = drag_start_world[1] + dy
        new_x, new_y = viewport.snap_to_grid(new_x, new_y)
        thing = canvas['things'][drag_index]
        thing["x"] = new_x
        thing["y"] = new_y

def node_drag_end():
    global dragging
    global drag_index
    dragging = False
    drag_index = None

def inputs_mouse(event):
    global font_text

    mouse['screen_x'], mouse['screen_y'] = pygame.mouse.get_pos()
    mouse['world_x'], mouse['world_y'] = viewport.screen_to_world(mouse['screen_x'], mouse['screen_y'])

    if event.type == pygame.MOUSEBUTTONDOWN:
        # LEFT BUTTON
        if event.button == 1: 
            node_drag_start()
        # WHEEL BUTTON
        elif event.button == 2:
            viewport.pan_start(mouse['screen_x'], mouse['screen_y'])
        # RIGHT BUTTON
        elif event.button == 3:
            node_create()
        # WHEEL UP
        elif event.button == 4:
            viewport.zoom_run(direction='up', mouse_screen_x=mouse['screen_x'], mouse_screen_y=mouse['screen_y'])
            font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
        # WHEEL DOWN
        elif event.button == 5:
            viewport.zoom_run(direction='down', mouse_screen_x=mouse['screen_x'], mouse_screen_y=mouse['screen_y'])
            font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
    elif event.type == pygame.MOUSEMOTION:
        node_drag_run()
        viewport.pan_run(mouse['screen_x'], mouse['screen_y'])
    elif event.type == pygame.MOUSEBUTTONUP:
        node_drag_end()
        # WHEEL BUTTON
        if event.button == 2:
            viewport.pan_end()

def main_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game['running'] = False
            
        inputs_mouse(event)


def draw_leftbar():
    pygame.draw.rect(screen, (200, 200, 200), 
        (leftbar_frame['x'], leftbar_frame['y'], leftbar_frame['w'], leftbar_frame['h'])
    )

    '''
    for tool_i, tool in enumerate(tools['items']):
        tool_w = 50
        tool_h = 50
        tool_x = x + (tool_w * tool_i)
        tool_y = y
        if tool_i % 2 == 0:
            color = (100, 100, 100)
        else:
            color = (140, 140, 140)
        if tool_i == tools['focus_i']:
            color = (0, 0, 255)
        pygame.draw.rect(screen, color, (tool_x, tool_y, tool_w, tool_h))
        line = tool['label']
        line_w, line_h = font_toolbar.size(line)
        surface = font_toolbar.render(line, True, (255, 255, 255))
        screen.blit(surface, (tool_x + (tool_w - line_w) // 2, tool_y + (tool_h - line_h) // 2))
    '''

def draw_grid():
    if viewport.state['visual_helpers'] == True:
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

def thing_bbox(thing):
    x, y = viewport.world_to_screen(thing["x"], thing["y"])
    lines = thing['text_lines']
    thing_w, thing_h = 0, 0
    for line in lines:
        line_w, line_h = font_text.size(line)
        if thing_w < line_w: thing_w = line_w
        thing_h += line_h
    ### snap size to grid
    thing_w = math.ceil(thing_w / (viewport.GRID_SIZE * viewport.state['camera_zoom'])) * (viewport.GRID_SIZE * viewport.state['camera_zoom'])
    thing_h = math.ceil(thing_h / (viewport.GRID_SIZE * viewport.state['camera_zoom'])) * (viewport.GRID_SIZE * viewport.state['camera_zoom'])
    ### padding
    padding_left = 8 * viewport.state['camera_zoom']
    padding_right = 8 * viewport.state['camera_zoom']
    thing_w += padding_left
    thing_w += padding_right
    ###
    w = thing_w
    h = thing_h
    return x, y, w, h

def draw_nodes():
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            thing_x, thing_y, thing_w, thing_h = thing_bbox(thing)
            lines = thing['text_lines']
            # frame
            if thing['focus'] == False:
                pygame.draw.rect(screen, COLOR_BACKGROUND, (thing_x, thing_y, thing_w, thing_h))
                pygame.draw.rect(screen, COLOR_FOREGROUND, (thing_x, thing_y, thing_w, thing_h), 1)
            else:
                pygame.draw.rect(screen, COLOR_BACKGROUND, (thing_x, thing_y, thing_w, thing_h))
                pygame.draw.rect(screen, COLOR_ELEMENT_FOCUS, (thing_x, thing_y, thing_w, thing_h), 1)
            # text + cursor
            cursor_x = 0
            cursor_h = 0
            _, line_h = font_text.size('A')
            lines_h_total = (len(lines)) * line_h
            for line_i, line in enumerate(lines):
                surface = font_text.render(line, True, COLOR_FOREGROUND)
                line_w, line_h = surface.get_size()
                line_x = thing_x + (thing_w - line_w) // 2
                line_y = thing_y + ((thing_h - lines_h_total) // 2) + (line_i * line_h)
                screen.blit(surface, (line_x, line_y))
                # cursor
                '''
                if thing['focus'] == True:
                    if line_i == text_cursor['line_i']:
                        char_w, char_h = font_text.size('X')
                        cursor_x = line_x + (char_w * text_cursor['char_i'])
                        cursor_y = line_y
                        pygame.draw.rect(screen, COLOR_FOREGROUND, (cursor_x, cursor_y, char_w, char_h), 1)
                '''

def draw_viewport():
    clip_rect = (viewport_frame['x'], viewport_frame['y'], viewport_frame['w'], viewport_frame['h'])
    screen.set_clip(clip_rect)
    draw_grid()
    # draw_edges()
    draw_nodes()
    screen.set_clip(None)

def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_leftbar()
    draw_viewport()
    pygame.display.flip()


def main():
    while game['running']:

        main_inputs()
        main_draw()

        clock.tick(60)

    pygame.quit()

main()
