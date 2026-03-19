import pygame

from lib import viewport

COLOR_BACKGROUND = (255, 255, 255)
COLOR_FOREGROUND = (10, 10, 10)
COLOR_ELEMENT_FOCUS = (128, 128, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 24)

def component_create(
    _id, name, x=0, y=0, w=256, h=64, focus=False,
):
    component = {
        'id': _id,
        'name': name,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
    }
    return component

components = {
    'x': 0, 
    'y': 0, 
    'components': []
}

component_1 = component_create('0', 'hydrogen', 500, 100)
component_2 = component_create('1', 'hydrogen', 800, 400)
component_3 = component_create('2', 'hydrogen', 200, 400)
components['components'].append(component_1)
components['components'].append(component_2)
components['components'].append(component_3)

def edge_create(
    _id, name='', x=0, y=0, w=256, h=64, focus=False, node_start=None, node_end=None,
):
    obj = {
        'id': _id,
        'name': name,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
        'node_start': node_start,
        'node_end': node_end,
    }
    return obj

edges = {
    '_': 0,
    'edges': [],
}

edge_1 = edge_create('0', '', node_start='0', node_end='1')
edge_2 = edge_create('1', '', node_start='0', node_end='2')
edges['edges'].append(edge_1)
edges['edges'].append(edge_2)

edge_tmp = edge_create('-1')

def component_coordinates_get(component):
    x, y = viewport.world_to_screen(component["x"], component["y"])
    w, h = component['w'] * viewport.camera_zoom, component['h'] * viewport.camera_zoom
    return x, y, w, h

dragging = False
drag_index = None
drag_start_world = None
drag_initial_positions = []

GRID_SIZE = 20

def snap_to_grid(x, y):
    x = round(x / GRID_SIZE) * GRID_SIZE
    y = round(y / GRID_SIZE) * GRID_SIZE
    return x, y

running = True
while running:
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    world_x, world_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # create edge
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    found = False
                    for component_i, component in enumerate(components['components']):
                        x, y, w, h = component_coordinates_get(component)
                        component['focus'] = False
                        if (
                            mouse_screen_x > x and mouse_screen_x < x + w and 
                            mouse_screen_y > y and mouse_screen_y < y + h
                        ):
                            found = True
                            # first click
                            if edge_tmp['node_start'] == None:
                                edge_tmp['node_start'] = component['id']
                            # second click
                            else:
                                edge_tmp['node_end'] = component['id']
                                if (
                                    edge_tmp['node_start'] != None and edge_tmp['node_end'] != None and
                                    edge_tmp['node_start'] != edge_tmp['node_end']
                                ):
                                    # check if edge already exist betwee the 2 nodes
                                    edge_found = False
                                    for edge in edges['edges']:
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
                                        edges['edges'].append(
                                            edge_create(
                                                '1', '', 
                                                node_start=edge_tmp['node_start'], 
                                                node_end=edge_tmp['node_end'],
                                            )
                                        )
                                edge_tmp['node_start'] = None
                                edge_tmp['node_end'] = None
                    if not found:
                        edge_tmp['node_start'] = None
                        edge_tmp['node_end'] = None
                # select/drag
                for component_i, component in enumerate(components['components']):
                    x, y, w, h = component_coordinates_get(component)
                    component['focus'] = False
                    if (
                        mouse_screen_x > x and mouse_screen_x < x + w and 
                        mouse_screen_y > y and mouse_screen_y < y + h
                    ):
                        component['focus'] = True
                        dragging = True
                        drag_index = component_i
                        drag_start_world = (x, y)
                        print(drag_start_world)
                        print(drag_index)

            elif event.button == 3:
                components['components'].append(component_create('0', 'hydrogen', x=world_x, y=world_y))
                print(components)

            # ZOOM ON MOUSE POS
            elif event.button == 4 or event.button == 5:
                # world position before zoom
                before_x, before_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

                if event.button == 4:
                    viewport.camera_zoom *= 1.1
                    viewport.camera_zoom = min(viewport.camera_zoom, viewport.MAX_ZOOM)
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.camera_zoom))

                elif event.button == 5:
                    viewport.camera_zoom /= 1.1
                    viewport.camera_zoom = max(viewport.camera_zoom, viewport.MIN_ZOOM)
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(24 * viewport.camera_zoom))

                # world position after zoom
                after_x, after_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

                # adjust camera so point under cursor stays fixed
                viewport.camera_x += before_x - after_x
                viewport.camera_y += before_y - after_y

            elif event.button == 2:
                viewport.panning = True
                viewport.pan_last_x, viewport.pan_last_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            drag_index = None
            print(drag_index)

            if event.button == 2:
                viewport.panning = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                dx = world_x - drag_start_world[0]
                dy = world_y - drag_start_world[1]
                component = components['components'][drag_index]
                new_x = drag_start_world[0] + dx
                new_y = drag_start_world[1] + dy
                new_x, new_y = snap_to_grid(new_x, new_y)
                component["x"] = new_x
                component["y"] = new_y

            if viewport.panning:
                dx = mouse_screen_x - viewport.pan_last_x
                dy = mouse_screen_y - viewport.pan_last_y
                viewport.camera_x -= dx / viewport.camera_zoom
                viewport.camera_y -= dy / viewport.camera_zoom
                viewport.pan_last_x = mouse_screen_x
                viewport.pan_last_y = mouse_screen_y

    screen.fill(COLOR_BACKGROUND)

    for edge in edges['edges']:
        # get start/end components of edge
        component_1 = None
        component_2 = None
        for component in components['components']:
            if edge['node_start'] == component['id']:
                component_1 = component
            if edge['node_end'] == component['id']:
                component_2 = component
        ###
        c1 = component_1
        c2 = component_2
        c1x, c1y, c1w, c1h = component_coordinates_get(c1)
        c2x, c2y, c2w, c2h = component_coordinates_get(c2)
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

    for component in components['components']:
        x, y, w, h = component_coordinates_get(component)
        name = component['name']
        # frame
        if component['focus'] == False:
            pygame.draw.rect(screen, COLOR_BACKGROUND, (x, y, w, h))
            pygame.draw.rect(screen, COLOR_FOREGROUND, (x, y, w, h), 1)
        else:
            pygame.draw.rect(screen, COLOR_BACKGROUND, (x, y, w, h))
            pygame.draw.rect(screen, COLOR_ELEMENT_FOCUS, (x, y, w, h), 1)
        # name
        if component['focus'] == False:
            surface = font_name.render(name, True, COLOR_FOREGROUND)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (x + w//2 - text_w//2, y + h - int(text_h * 1.4)))
        else:
            surface = font_name.render(name, True, COLOR_ELEMENT_FOCUS)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (x + w//2 - text_w//2, y + h - int(text_h * 1.4)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

