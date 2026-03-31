import json
import math

import pygame

from lib import viewport


project_folderpath = 'projects/pyramid'

COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (10, 10, 10)
COLOR_ELEMENT_FOCUS = (128, 128, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
WINDOW_W, WINDOW_H = WIDTH, HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLOW")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
FONT_FAMILY_IBM_PLEX_MONO = 'fonts/IBM_Plex_Mono/IBMPlexMono-Regular.ttf'

font_family_text = FONT_FAMILY_IBM_PLEX_MONO

font_size_base = 8
font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
font_debug = pygame.font.Font(font_family_text, 24 )
font_toolbar = pygame.font.Font(font_family_text, 18 )

diagram_index = 0

toolbar_frame = {
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

edge_tmp = thing_create('-1', kind='edge')

################################################################################
# UTILS
################################################################################
def save(slot):
    with open(f"{project_folderpath}/diagrams/{slot}.json", "w") as file:
        json.dump(canvas, file, indent=4)

def load(slot):
    global diagram_index
    global canvas
    try:
        with open(f"{project_folderpath}/diagrams/{slot}.json", "r") as file:
            canvas = json.load(file)
    except:
        save(slot)
    diagram_index = slot

def screenshot_create():
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

################################################################################
# CREATE / DELETE
################################################################################
def edge_create__first_click(thing):
    edge_tmp['node_start'] = thing['id']
    viewport.state['edge_tmp_drawing'] = True

def edge_create__second_click(thing):
    edge_tmp['node_end'] = thing['id']
    if (
        edge_tmp['node_start'] != None and edge_tmp['node_end'] != None and
        edge_tmp['node_start'] != edge_tmp['node_end']
    ):
        # check if edge already exist betwee the 2 nodes
        edge_found = False
        '''
        for edge in canvas['things']:
            if (
                (
                    edge['node_start'] == edge_tmp['node_start'] and 
                    edge['node_end'] == edge_tmp['node_end']
                ) or
                (
                    edge['node_start'] == edge_tmp['node_end'] and 
                    edge['node_end'] == edge_tmp['node_start']
                )
            ):
                edge_found = True
                break
        '''
        if not edge_found:
            # create edge
            canvas['things'].append(
                thing_create(
                    str(len(canvas['things'])+1), kind='edge', 
                    node_start=edge_tmp['node_start'], 
                    node_end=edge_tmp['node_end'],
                    edge_direction=viewport.state['edge_direction_cur'],
                )
            )
        edge_tmp['node_start'] = None
        edge_tmp['node_end'] = None
        viewport.state['edge_tmp_drawing'] = False

def edge_create__reset():
    edge_tmp['node_start'] = None
    edge_tmp['node_end'] = None
    viewport.state['edge_tmp_drawing'] = False

def edge_create():
    clicked_on_node = False
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = thing_bbox_get(thing)
        thing['focus'] = False
        if (
            mouse_screen_x > x and mouse_screen_x < x + w and 
            mouse_screen_y > y and mouse_screen_y < y + h
        ):
            clicked_on_node = True
            if edge_tmp['node_start'] == None: edge_create__first_click(thing)
            else: edge_create__second_click(thing)
            break
    if not clicked_on_node:
        edge_create__reset()

def node_create():
    snap_x, snap_y = viewport.snap_to_grid(mouse_world_x, mouse_world_y)
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

def node_delete():
    thing = viewport.thing_focused_get(canvas)
    if thing != None:
        if thing in canvas['things']:
            canvas['things'].remove(thing)
    for edge in canvas['things']:
        if edge['node_start'] == thing['id'] or edge['node_end'] == thing['id']:
            canvas['things'].remove(edge)
    ###
    edge_create__reset()

################################################################################
# NAVIGATION
################################################################################
dragging = False
drag_index = None
drag_start_world = None
drag_initial_positions = []

text_cursor = {
    'line_i': 0,
    'char_i': 0,
}

def thing_bbox_get_old(thing):
    x, y = viewport.world_to_screen(thing["x"], thing["y"])
    lines_w_max, lines_h_tot = 0, 0
    ### lines w max
    lines = thing['text_lines']
    for line in lines:
        line_w, _ = font_text.size(line)
        if lines_w_max < line_w: lines_w_max = line_w
    ### lines h tot
    _, line_h = font_text.size('A')
    lines_h_tot = (len(lines)) * line_h
    ### pick bigger
    thing_w_min, thing_h_min = thing['w_min'], thing['h_min']
    if lines_w_max > thing_w_min: w = lines_w_max
    else: w = thing_w_min
    if lines_h_tot > thing_h_min: h = lines_h_tot
    else: h = thing_h_min
    ### snap size to grid
    w = math.ceil(w / viewport.GRID_SIZE) * viewport.GRID_SIZE
    h = math.ceil(h / viewport.GRID_SIZE) * viewport.GRID_SIZE
    ### scale by zoom
    w = w * viewport.state['camera_zoom']
    h = h * viewport.state['camera_zoom']
    return x, y, w, h

def thing_bbox_get(thing):
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

def node_drag_start():
    global dragging
    global drag_index
    global drag_start_world
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = thing_bbox_get(thing)
        thing['focus'] = False
        if (
            mouse_screen_x > x and mouse_screen_x < x + w and 
            mouse_screen_y > y and mouse_screen_y < y + h
        ):
            thing['focus'] = True
            dragging = True
            drag_index = thing_i
            drag_start_world = (x, y)
            # drag_start_world = mouse_world_x, mouse_world_y

def node_drag_run():
    if dragging:
        dx = mouse_world_x - drag_start_world[0]
        dy = mouse_world_y - drag_start_world[1]
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

################################################################################
# DRAW
################################################################################
def draw_line_angled(thing_1, thing_2, edge_direction):
    c1 = thing_1
    c2 = thing_2
    c1x, c1y, c1w, c1h = thing_bbox_get(c1)
    c2x, c2y, c2w, c2h = thing_bbox_get(c2)
    arrow_size = 16
    if edge_direction == 0:
        x1, y1 = c1x + c1w//2, c1y + c1h//2
        x2, y2 = c2x + c2w//2, c1y + c1h//2
        x3, y3 = c2x + c2w//2, c2y + c2h//2
        if y1 < y3:
            arrow_point_1 = (x3 - (arrow_size // 2), y3 - (c2h // 2) - (arrow_size))
            arrow_point_2 = (x3 + (arrow_size // 2), y3 - (c2h // 2) - (arrow_size))
            arrow_point_3 = (x3, y3 - (c2h // 2))
        else:
            arrow_point_1 = (x3 - (arrow_size // 2), y3 + (c2h // 2) + (arrow_size))
            arrow_point_2 = (x3 + (arrow_size // 2), y3 + (c2h // 2) + (arrow_size))
            arrow_point_3 = (x3, y3 + (c2h // 2))
    else:
        x1, y1 = c1x + c1w//2, c1y + c1h//2
        x2, y2 = c1x + c1w//2, c2y + c2h//2
        x3, y3 = c2x + c2w//2, c2y + c2h//2
        if x1 < x3:
            arrow_point_1 = (x3 - (c2w // 2) - (arrow_size), y3 + (arrow_size // 2))
            arrow_point_2 = (x3 - (c2w // 2) - (arrow_size), y3 - (arrow_size // 2))
            arrow_point_3 = (x3 - (c2w // 2), y3)
        else:
            arrow_point_1 = (x3 + (c2w // 2) + (arrow_size), y3 + (arrow_size // 2))
            arrow_point_2 = (x3 + (c2w // 2) + (arrow_size), y3 - (arrow_size // 2))
            arrow_point_3 = (x3 + (c2w // 2), y3)
    # line
    pygame.draw.line(screen, COLOR_FOREGROUND, 
        (x1, y1), 
        (x2, y2), 
        1
    )
    pygame.draw.line(screen, COLOR_FOREGROUND, 
        (x2, y2), 
        (x3, y3), 
        1
    )
    pygame.draw.polygon(
        screen, 
        COLOR_FOREGROUND,
        [
            arrow_point_1,
            arrow_point_2,
            arrow_point_3,
        ]
    )

def draw_line_straight(thing_1, thing_2):
    c1 = thing_1
    c2 = thing_2
    c1x, c1y, c1w, c1h = thing_bbox_get(c1)
    c2x, c2y, c2w, c2h = thing_bbox_get(c2)
    x1, y1 = c1x + c1w//2, c1y + c1h//2
    x2, y2 = c2x + c2w//2, c2y + c2h//2
    # line
    pygame.draw.line(screen, COLOR_FOREGROUND, 
        (x1, y1), 
        (x2, y2), 
        1
    )

def draw_grid():
    if viewport.state['grid_show']:
        step = viewport.GRID_SIZE * viewport.state['camera_zoom']
        # Offset grid based on camera position
        offset_x = (-viewport.state['camera_x'] * viewport.state['camera_zoom']) % step
        offset_y = (-viewport.state['camera_y'] * viewport.state['camera_zoom']) % step
        # Vertical lines
        x = offset_x
        while x < WIDTH:
            pygame.draw.line(screen, (200, 200, 200), (int(x), 0), (int(x), HEIGHT), 1)
            x += step
        # Horizontal lines
        y = offset_y
        while y < HEIGHT:
            pygame.draw.line(screen, (200, 200, 200), (0, int(y)), (WIDTH, int(y)), 1)
            y += step

def draw_edges():
    # EDGES
    for thing in canvas['things']:
        if thing['kind'] == 'edge':
            node_start = None
            node_end = None
            for _thing in canvas['things']:
                if thing['node_start'] == _thing['id']:
                    node_start = _thing
                if thing['node_end'] == _thing['id']:
                    node_end = _thing
            ###
            if viewport.state['edge_style'] == 0:
                draw_line_straight(node_start, node_end)
            else:
                draw_line_angled(node_start, node_end, thing['edge_direction'])
    # EDGE TMP
    if viewport.state['edge_tmp_drawing']:
        # find start node
        thing_start = None
        for _thing in canvas['things']:
            if edge_tmp['node_start'] == _thing['id']:
                thing_start = _thing
        # calc points 
        if viewport.state['edge_style'] == 0:
            c1x, c1y, c1w, c1h = thing_bbox_get(thing_start)
            c2x, c2y = viewport.snap_to_grid(mouse_world_x, mouse_world_y)
            c2w, c2h = 0, 0
            x1, y1 = c1x + c1w//2, c1y + c1h//2
            x2, y2 = c2x + c2w//2, c2y + c2h//2
            # draw lines
            pygame.draw.line(screen, COLOR_FOREGROUND, (x1, y1), (x2, y2), 1)
        else:
            c1x, c1y, c1w, c1h = thing_bbox_get(thing_start)
            c2x, c2y = viewport.snap_to_grid(mouse_world_x, mouse_world_y)
            c2w, c2h = 0, 0
            if viewport.state['edge_direction_cur'] == 0:
                x1, y1 = c1x + c1w//2, c1y + c1h//2
                x2, y2 = c2x + c2w//2, c1y + c1h//2
                x3, y3 = c2x + c2w//2, c2y + c2h//2
            else:
                x1, y1 = c1x + c1w//2, c1y + c1h//2
                x2, y2 = c1x + c1w//2, c2y + c2h//2
                x3, y3 = c2x + c2w//2, c2y + c2h//2
            # draw lines
            pygame.draw.line(screen, COLOR_FOREGROUND, (x1, y1), (x2, y2), 1)
            pygame.draw.line(screen, COLOR_FOREGROUND, (x2, y2), (x3, y3), 1)

def draw_nodes():
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            thing_x, thing_y, thing_w, thing_h = thing_bbox_get(thing)
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
                if thing['focus'] == True:
                    if line_i == text_cursor['line_i']:
                        char_w, char_h = font_text.size('X')
                        cursor_x = line_x + (char_w * text_cursor['char_i'])
                        cursor_y = line_y
                        pygame.draw.rect(screen, COLOR_FOREGROUND, (cursor_x, cursor_y, char_w, char_h), 1)

def draw_debug():
    if viewport.state['debug_show']:
        surface = font_debug.render(str(diagram_index), True, COLOR_ELEMENT_FOCUS)
        screen.blit(surface, (0, 0))
        surface = font_debug.render(str(viewport.state['camera_zoom']), True, (255, 0, 255))
        screen.blit(surface, (0, 30))
        surface = font_debug.render(str(viewport.state['edge_direction_cur']), True, (255, 0, 255))
        screen.blit(surface, (0, 60))
        surface = font_debug.render(f'{mouse_screen_x}:{mouse_screen_y}', True, (255, 0, 255))
        screen.blit(surface, (0, 90))
        y_cur = 90
        y_cur += 30
        ### font
        surface = font_debug.render(f'''font: {font_size_base:.2f} * {viewport.state['camera_zoom']:.2f} = {font_size_base * viewport.state['camera_zoom']:.2f}''', True, (255, 0, 255))
        screen.blit(surface, (0, y_cur))
        y_cur += 30
        ### rect
        if len(canvas['things']):
            thing = canvas['things'][0]
            rect_res = thing['w_min'] * viewport.state['camera_zoom']
            surface = font_debug.render(f'''rect: {thing['w_min']:.2f} * {viewport.state['camera_zoom']:.2f} = {rect_res:.2f}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            thing_x, thing_y, thing_w, thing_h = thing_bbox_get(thing)
            surface = font_debug.render(f'''thin: {thing_w:.2f}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            line_w, _ = font_text.size(thing['text_lines'][0])
            surface = font_debug.render(f'''line: {line_w:.2f}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
            line_w, _ = font_text.size(thing['text_lines'][0])
            if thing_w != 0:
                surface = font_debug.render(f'''perc: {(rect_res / thing_w) * 100:.2f}''', True, (255, 0, 255))
            else:
                surface = font_debug.render(f'''perc: {0 * 100:.2f}''', True, (255, 0, 255))
            screen.blit(surface, (0, y_cur))
            y_cur += 30
        ###
        cursor_line_i = text_cursor['line_i']
        surface = font_debug.render(f'''clin: {cursor_line_i:.2f}''', True, (255, 0, 255))
        screen.blit(surface, (0, y_cur))
        y_cur += 30
        ###
        cursor_char_i = text_cursor['char_i']
        surface = font_debug.render(f'''ccha: {cursor_char_i:.2f}''', True, (255, 0, 255))
        screen.blit(surface, (0, y_cur))
        y_cur += 30

tools = {
    'focus_i': '-1',
    'items': [
        {
            'id': '-1',
            'kind': 'tool',
            'name': 'arrow',
            'label': 'arr',
        },
        {
            'id': '-1',
            'kind': 'tool',
            'name': 'node',
            'label': 'nod',
        },
    ]
}

def draw_toolbar():
    x = toolbar_frame['x']
    y = toolbar_frame['y']
    w = toolbar_frame['w']
    h = toolbar_frame['h']
    pygame.draw.rect(screen, (200, 200, 200), (x, y, w, h))

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

def draw_viewport():
    x = viewport_frame['x']
    y = viewport_frame['y']
    w = viewport_frame['w']
    h = viewport_frame['h']
    clip_rect = (x, y, w, h)
    screen.set_clip(clip_rect)
    draw_grid()
    draw_edges()
    draw_nodes()
    screen.set_clip(None)

def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_toolbar()
    draw_viewport()
    draw_debug()
    pygame.display.flip()

################################################################################
# MAIN
################################################################################
running = True
while running:
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    mouse_world_x, mouse_world_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # while creating line
            if viewport.state['edge_tmp_drawing']:
                if 0: pass
                elif event.key == pygame.K_SPACE:
                    if viewport.state['edge_direction_cur'] == 0: viewport.state['edge_direction_cur'] = 1
                    else: viewport.state['edge_direction_cur'] = 0

            # while holding ctrl
            elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                if 0: pass
                elif event.key == pygame.K_s: save(diagram_index)
                elif event.key == pygame.K_0: load(0)
                elif event.key == pygame.K_1: load(1)
                elif event.key == pygame.K_2: load(2)
                elif event.key == pygame.K_3: load(3)
                elif event.key == pygame.K_4: load(4)
                elif event.key == pygame.K_5: load(5)
                elif event.key == pygame.K_6: load(6)
                elif event.key == pygame.K_7: load(7)
                elif event.key == pygame.K_8: load(8)
                elif event.key == pygame.K_9: load(9)
                elif event.key == pygame.K_x: node_delete()
                elif event.key == pygame.K_e: screenshot_create()
                elif event.key == pygame.K_g:
                    if viewport.state['grid_show']: viewport.state['grid_show'] = False
                    else: viewport.state['grid_show'] = True
                elif event.key == pygame.K_d:
                    if viewport.state['debug_show']: viewport.state['debug_show'] = False
                    else: viewport.state['debug_show'] = True

            elif event.unicode == "{":
                print("Left curly bracket")
                viewport.zoom_from_center('down', 1, 'add', 'int', WIDTH//2, HEIGHT//2)
                font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
            elif event.unicode == "}":
                print("Right curly bracket")
                viewport.zoom_from_center('up', 1, 'add', 'int', WIDTH//2, HEIGHT//2)
                font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))

            # typing
            elif event.key == pygame.K_BACKSPACE:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['text_lines'][0] = thing['text_lines'][0][:-1]

            elif event.key == pygame.K_RETURN:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['text_lines'].append('')

            elif event.key == pygame.K_UP:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        text_cursor['line_i'] -= 1
            elif event.key == pygame.K_DOWN:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        text_cursor['line_i'] += 1
            elif event.key == pygame.K_LEFT:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        text_cursor['char_i'] -= 1
            elif event.key == pygame.K_RIGHT:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        text_cursor['char_i'] += 1

            else:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['text_lines'][0] += event.unicode

        focus_context = ''
        if (
            mouse_screen_x > toolbar_frame['x'] and
            mouse_screen_y > toolbar_frame['y'] and
            mouse_screen_x < toolbar_frame['x'] + toolbar_frame['w'] and
            mouse_screen_y < toolbar_frame['y'] + toolbar_frame['h']
        ):
            focus_context = 'toolbar'
        else:
            focus_context = 'viewport'

        if focus_context == 'toolbar':
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = toolbar_frame['x']
                y = toolbar_frame['y']
                w = toolbar_frame['w']
                h = toolbar_frame['h']
                found = False
                for tool_i, tool in enumerate(tools['items']):
                    tool_w = 50
                    tool_h = 50
                    tool_x = x + (tool_w * tool_i)
                    tool_y = y
                    if (
                        mouse_screen_x > tool_x and
                        mouse_screen_y > tool_y and
                        mouse_screen_x < tool_x + tool_w and
                        mouse_screen_y < tool_y + tool_h
                    ):
                        tools['focus_i'] = tool_i
                        if tool['name'] == 'arrow':
                            if viewport.state['edge_style'] == 0: viewport.state['edge_style'] = 1
                            else: viewport.state['edge_style'] = 0
                        found = True
                        break
                if not found:
                    tools['focus_i'] = -1
            if event.type == pygame.MOUSEBUTTONUP:
                tools['focus_i'] = -1
            if event.type == pygame.MOUSEMOTION:
                pass
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.button == 1:
                        edge_create() 
                else:
                    if event.button == 1:
                        if viewport.state['edge_tmp_drawing']:
                            edge_create() 
                        else:
                            node_drag_start()

                    elif event.button == 2:
                        viewport.pan_start(mouse_screen_x, mouse_screen_y)

                    elif event.button == 3:
                        node_create()

                    # ZOOM ON MOUSE POS
                    elif event.button == 4:
                        viewport.zoom_run(direction='up', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                        font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))
                    elif event.button == 5:
                        viewport.zoom_run(direction='down', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                        font_text = pygame.font.Font(font_family_text, int(font_size_base * viewport.state['camera_zoom']))

            if event.type == pygame.MOUSEBUTTONUP:
                node_drag_end()
                if event.button == 2:
                    viewport.pan_end()

            if event.type == pygame.MOUSEMOTION:
                node_drag_run()
                viewport.pan_run(mouse_screen_x, mouse_screen_y)

    main_draw()

    clock.tick(60)

pygame.quit()

