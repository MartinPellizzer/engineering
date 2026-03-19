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

component = component_create('0', 'hydrogen', 0, 0)
components['components'].append(component)

def component_coordinates_get(component):
    x, y = viewport.world_to_screen(component["x"], component["y"])
    w, h = component['w'] * viewport.camera_zoom, component['h'] * viewport.camera_zoom
    return x, y, w, h

dragging = False
drag_index = None
drag_offset_x = 0
drag_offset_y = 0
drag_start_world = None
drag_initial_positions = []

running = True
while running:
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    world_x, world_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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
            if viewport.panning:
                dx = mouse_screen_x - viewport.pan_last_x
                dy = mouse_screen_y - viewport.pan_last_y
                viewport.camera_x -= dx / viewport.camera_zoom
                viewport.camera_y -= dy / viewport.camera_zoom
                viewport.pan_last_x = mouse_screen_x
                viewport.pan_last_y = mouse_screen_y

    screen.fill(COLOR_BACKGROUND)

    for component in components['components']:
        x, y, w, h = component_coordinates_get(component)

        name = component['name']
        # frame
        if component['focus'] == False:
            pygame.draw.rect(screen, COLOR_FOREGROUND, (x, y, w, h), 1)
        else:
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

