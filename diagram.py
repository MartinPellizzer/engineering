# drag new line with ghosting instead of 2 clicks

import json

import pygame

from lib import viewport

COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (10, 10, 10)
COLOR_ELEMENT_FOCUS = (128, 128, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLOW")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.state['camera_zoom']))

diagram_index = 0

def thing_create(
    _id, kind, name='', x=0, y=0, w=0, h=0, focus=False, node_start=None, node_end=None, edge_direction=0,
    w_min=0, h_min=0,
):
    thing = {
        'id': _id,
        'kind': kind,
        'name': name,
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

dragging = False
drag_index = None
drag_start_world = None
drag_initial_positions = []

def thing_coordinates_get(thing):
    x, y = viewport.world_to_screen(thing["x"], thing["y"])
    w_text, h_text = font_name.size(thing['name'])
    w_min, h_min = thing['w_min'] * viewport.state['camera_zoom'], thing['h_min'] * viewport.state['camera_zoom']
    print(w_text, w_min)
    if w_text > w_min: 
        w = w_text
    else: 
        w = w_min
    if h_text > h_min: 
        h = h_text
    else: 
        h = h_min
    return x, y, w, h

def save(slot):
    with open(f"diagrams/{slot}.json", "w") as file:
        json.dump(canvas, file, indent=4)

def load(slot):
    global diagram_index
    global canvas
    try:
        with open(f"diagrams/{slot}.json", "r") as file:
            canvas = json.load(file)
    except:
        save(slot)
    diagram_index = slot

def draw_line_angled(thing_1, thing_2, edge_direction):
    c1 = thing_1
    c2 = thing_2
    c1x, c1y, c1w, c1h = thing_coordinates_get(c1)
    c2x, c2y, c2w, c2h = thing_coordinates_get(c2)
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
    c1x, c1y, c1w, c1h = thing_coordinates_get(c1)
    c2x, c2y, c2w, c2h = thing_coordinates_get(c2)
    x1, y1 = c1x + c1w//2, c1y + c1h//2
    x2, y2 = c2x + c2w//2, c2y + c2h//2
    # line
    pygame.draw.line(screen, COLOR_FOREGROUND, 
        (x1, y1), 
        (x2, y2), 
        1
    )

def create_edge():
    found = False
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = thing_coordinates_get(thing)
        thing['focus'] = False
        if (
            mouse_screen_x > x and mouse_screen_x < x + w and 
            mouse_screen_y > y and mouse_screen_y < y + h
        ):
            found = True
            # first click
            if edge_tmp['node_start'] == None:
                edge_tmp['node_start'] = thing['id']
                viewport.state['edge_tmp_drawing'] = True
            # second click
            else:
                edge_tmp['node_end'] = thing['id']
                if (
                    edge_tmp['node_start'] != None and edge_tmp['node_end'] != None and
                    edge_tmp['node_start'] != edge_tmp['node_end']
                ):
                    # check if edge already exist betwee the 2 nodes
                    edge_found = False
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
    if not found:
        edge_tmp['node_start'] = None
        edge_tmp['node_end'] = None
        viewport.state['edge_tmp_drawing'] = False

def node_drag_start():
    global dragging
    global drag_index
    global drag_start_world
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = thing_coordinates_get(thing)
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

def draw_debug():
    if viewport.state['debug_show']:
        surface = font_name.render(str(diagram_index), True, COLOR_ELEMENT_FOCUS)
        screen.blit(surface, (0, 0))
        surface = font_name.render(str(viewport.state['camera_zoom']), True, (255, 0, 255))
        screen.blit(surface, (0, 30))
        surface = font_name.render(str(viewport.state['edge_direction_cur']), True, (255, 0, 255))
        screen.blit(surface, (0, 60))
        surface = font_name.render(f'{mouse_screen_x}:{mouse_screen_y}', True, (255, 0, 255))
        screen.blit(surface, (0, 90))

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
            # draw_line_straight(node_start, node_end)
            draw_line_angled(node_start, node_end, thing['edge_direction'])
    # EDGE TMP
    if viewport.state['edge_tmp_drawing']:
        # find start node
        thing_start = None
        for _thing in canvas['things']:
            if edge_tmp['node_start'] == _thing['id']:
                thing_start = _thing
        # calc points 
        c1x, c1y, c1w, c1h = thing_coordinates_get(thing_start)
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
    # NODES
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            x, y, w, h = thing_coordinates_get(thing)
            name = thing['name']
            # frame
            if thing['focus'] == False:
                pygame.draw.rect(screen, COLOR_BACKGROUND, (x, y, w, h))
                pygame.draw.rect(screen, COLOR_FOREGROUND, (x, y, w, h), 1)
            else:
                pygame.draw.rect(screen, COLOR_BACKGROUND, (x, y, w, h))
                pygame.draw.rect(screen, COLOR_ELEMENT_FOCUS, (x, y, w, h), 1)
            # name
            if thing['focus'] == False:
                surface = font_name.render(name, True, COLOR_FOREGROUND)
                text_w, text_h = surface.get_size()
                screen.blit(surface, (x + w//2 - text_w//2, y + h - int(text_h * 1.4)))
            else:
                surface = font_name.render(name, True, COLOR_ELEMENT_FOCUS)
                text_w, text_h = surface.get_size()
                screen.blit(surface, (x + w//2 - text_w//2, y + h - int(text_h * 1.4)))

def node_create():
    snap_x, snap_y = viewport.snap_to_grid(mouse_world_x, mouse_world_y)
    canvas['things'].append(
        thing_create(
            str(len(canvas['things'])+1), 
            kind = 'node', 
            name = 'enter text', 
            x = snap_x, 
            y = snap_y,
            w_min = 256,
            h_min = 64,
        )
    )


def main_draw():
    screen.fill(COLOR_BACKGROUND)
    draw_grid()
    draw_edges()
    draw_nodes()
    draw_debug()
    pygame.display.flip()

def node_delete():
    thing = viewport.thing_focused_get(canvas)
    if thing != None:
        if thing in canvas['things']:
            canvas['things'].remove(thing)
    for edge in canvas['things']:
        if edge['node_start'] == thing['id'] or edge['node_end'] == thing['id']:
            canvas['things'].remove(edge)
    edge_tmp['node_start'] = None
    edge_tmp['node_end'] = None

def screenshot_create():
    x1, y1, x2, y2 = None, None, None, None
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            if x1 == None: x1 = thing['x']
            if y1 == None: y1 = thing['y']
            if x2 == None: x2 = thing['x'] + thing['w']
            if y2 == None: y2 = thing['y'] + thing['h']
            if x1 > thing['x']: x1 = thing['x']
            if y1 > thing['y']: y1 = thing['y']
            if x2 < thing['x'] + thing['w']: x2 = thing['x'] + thing['w']
            if y2 < thing['y'] + thing['h']: y2 = thing['y'] + thing['h']
    x = x1
    y = y1
    w = x2 - x1
    h = y2 - y1
    rect = pygame.Rect(x, y, w, h)
    snapshot = screen.subsurface(rect).copy()
    pygame.image.save(snapshot, 'screenshot.png')

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

            # typing
            elif event.key == pygame.K_BACKSPACE:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['name'] = thing['name'][:-1]
            else:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['name'] += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if event.button == 1:
                    create_edge() 
            else:
                if event.button == 1:
                    if viewport.state['edge_tmp_drawing']:
                        create_edge() 
                    else:
                        node_drag_start()

                elif event.button == 2:
                    viewport.pan_start(mouse_screen_x, mouse_screen_y)

                elif event.button == 3:
                    node_create()

                # ZOOM ON MOUSE POS
                elif event.button == 4:
                    viewport.zoom_run(direction='up', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.state['camera_zoom']))
                elif event.button == 5:
                    viewport.zoom_run(direction='down', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.state['camera_zoom']))

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

