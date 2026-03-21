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
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 24)

diagram_index = 0

def thing_create(
    _id, kind, name='', x=0, y=0, w=256, h=64, focus=False, node_start=None, node_end=None,
):
    thing = {
        'id': _id,
        'kind': kind,
        'name': name,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
        'node_start': node_start,
        'node_end': node_end,
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

def draw_line_angled(thing_1, thing_2):
    c1 = thing_1
    c2 = thing_2
    c1x, c1y, c1w, c1h = viewport.thing_coordinates_get(c1)
    c2x, c2y, c2w, c2h = viewport.thing_coordinates_get(c2)
    x1, y1 = c1x + c1w//2, c1y + c1h//2
    x2, y2 = c2x + c2w//2, c1y + c1h//2
    x3, y3 = c2x + c2w//2, c2y + c2h//2
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

def draw_line_straight(thing_1, thing_2):
    c1 = thing_1
    c2 = thing_2
    c1x, c1y, c1w, c1h = viewport.thing_coordinates_get(c1)
    c2x, c2y, c2w, c2h = viewport.thing_coordinates_get(c2)
    x1, y1 = c1x + c1w//2, c1y + c1h//2
    x2, y2 = c2x + c2w//2, c2y + c2h//2
    # line
    pygame.draw.line(screen, COLOR_FOREGROUND, 
        (x1, y1), 
        (x2, y2), 
        1
    )

def create_edge():
    if pygame.key.get_mods() & pygame.KMOD_CTRL:
        found = False
        for thing_i, thing in enumerate(canvas['things']):
            x, y, w, h = viewport.thing_coordinates_get(thing)
            thing['focus'] = False
            if (
                mouse_screen_x > x and mouse_screen_x < x + w and 
                mouse_screen_y > y and mouse_screen_y < y + h
            ):
                found = True
                # first click
                if edge_tmp['node_start'] == None:
                    edge_tmp['node_start'] = thing['id']
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
                                )
                            )
                    edge_tmp['node_start'] = None
                    edge_tmp['node_end'] = None
        if not found:
            edge_tmp['node_start'] = None
            edge_tmp['node_end'] = None

def node_drag_start():
    global dragging
    global drag_index
    global drag_start_world
    for thing_i, thing in enumerate(canvas['things']):
        x, y, w, h = viewport.thing_coordinates_get(thing)
        thing['focus'] = False
        if (
            mouse_screen_x > x and mouse_screen_x < x + w and 
            mouse_screen_y > y and mouse_screen_y < y + h
        ):
            thing['focus'] = True
            dragging = True
            drag_index = thing_i
            drag_start_world = (x, y)
            # drag_start_world = world_x, world_y


def node_drag_run():
    if dragging:
        dx = world_x - drag_start_world[0]
        dy = world_y - drag_start_world[1]
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

def main_draw():
    # EDGES
    for thing in canvas['things']:
        if thing['kind'] == 'edge':
            thing_1 = None
            thing_2 = None
            for _thing in canvas['things']:
                if thing['node_start'] == _thing['id']:
                    thing_1 = _thing
                if thing['node_end'] == _thing['id']:
                    thing_2 = _thing
            ###
            draw_line_straight(thing_1, thing_2)

    # NODES
    for thing in canvas['things']:
        if thing['kind'] == 'node':
            x, y, w, h = viewport.thing_coordinates_get(thing)
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

    surface = font_name.render(str(diagram_index), True, COLOR_ELEMENT_FOCUS)
    screen.blit(surface, (0, 0))


running = True
while running:
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    world_x, world_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Typing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                thing = viewport.thing_focused_get(canvas)
                if thing != None:
                    if thing['kind'] == 'node':
                        thing['name'] = thing['name'][:-1]
            else:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.key == pygame.K_e:
                        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
                        snapshot = screen.subsurface(rect).copy()
                        pygame.image.save(snapshot, 'screenshot.png')
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
                    elif event.key == pygame.K_x:
                        thing = viewport.thing_focused_get(canvas)
                        if thing != None:
                            if thing in canvas['things']:
                                canvas['things'].remove(thing)
                        for edge in canvas['things']:
                            if edge['node_start'] == thing['id'] or edge['node_end'] == thing['id']:
                                canvas['things'].remove(edge)
                        edge_tmp['node_start'] = None
                        edge_tmp['node_end'] = None
                else:
                    thing = viewport.thing_focused_get(canvas)
                    if thing != None:
                        if thing['kind'] == 'node':
                            thing['name'] += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                create_edge() 
                node_drag_start()

            elif event.button == 3:
                snap_x, snap_y = viewport.snap_to_grid(world_x, world_y)
                canvas['things'].append(
                    thing_create(
                        str(len(canvas['things'])+1), kind='node', name='hydrogen', 
                        x=snap_x, y=snap_y
                    )
                )

            # ZOOM ON MOUSE POS
            elif event.button == 4:
                viewport.zoom_run(direction='up', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.state['camera_zoom']))
            elif event.button == 5:
                viewport.zoom_run(direction='down', mouse_screen_x=mouse_screen_x, mouse_screen_y=mouse_screen_y)
                font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.state['camera_zoom']))

            elif event.button == 2:
                viewport.pan_start(mouse_screen_x, mouse_screen_y)

        if event.type == pygame.MOUSEBUTTONUP:
            node_drag_end()
            if event.button == 2:
                viewport.pan_end()

        if event.type == pygame.MOUSEMOTION:
            node_drag_run()
            viewport.pan_run(mouse_screen_x, mouse_screen_y)


    ########################################
    # GRID
    ########################################
    step = viewport.GRID_SIZE * viewport.state['camera_zoom']

    # Offset grid based on camera position
    offset_x = (-viewport.state['camera_x'] * viewport.state['camera_zoom']) % step
    offset_y = (-viewport.state['camera_y'] * viewport.state['camera_zoom']) % step

    screen.fill(COLOR_BACKGROUND)

    # Vertical lines
    x = offset_x
    while x < WIDTH:
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (int(x), 0),
            (int(x), HEIGHT),
            1
        )
        x += step

    # Horizontal lines
    y = offset_y
    while y < HEIGHT:
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (0, int(y)),
            (WIDTH, int(y)),
            1
        )
        y += step

    main_draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

