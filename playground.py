import pygame

from lib import viewport

COLOR_BACKGROUND = (10, 10, 10)
COLOR_FOREGROUND = (255, 255, 255)
COLOR_ELEMENT_FOCUS = (128, 128, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 24)

def component_create(
    number, name, x=0, y=0, w=256, h=64, focus=False,
):
    element = {
        'number': number,
        'name': name,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
    }
    return element

components = {
    'x': 0, 
    'y': 0, 
    'components': []
}

component = component_create('1', 'hydrogen', 0, 0)
components['components'].append(component)

running = True
while running:
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    world_x, world_y = viewport.screen_to_world(mouse_screen_x, mouse_screen_y)

    # check details on hover
    if 1:
        for element in components['components']:
            tsx, tsy = viewport.world_to_screen(components["x"], components["y"])
            sw, sh = 256 * viewport.camera_zoom, 64 * viewport.camera_zoom
            sx = tsx + sw
            sy = tsy + sh
            element['focus'] = False
            if (
                mouse_screen_x > sx and mouse_screen_x < sx + sw and 
                mouse_screen_y > sy and mouse_screen_y < sy + sh
            ):
                element['focus'] = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for element in components['components']:
                    tsx, tsy = viewport.world_to_screen(components["x"], components["y"])
                    sw, sh = 256 * viewport.camera_zoom, 64 * viewport.camera_zoom
                    sx = tsx + sw
                    sy = tsy + sh
                    element['focus'] = False
                    if (
                        mouse_screen_x > sx and mouse_screen_x < sx + sw and 
                        mouse_screen_y > sy and mouse_screen_y < sy + sh
                    ):
                        element['focus'] = True

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

    tsx, tsy = viewport.world_to_screen(components["x"], components["y"])
    for element in components['components']:
        sw, sh = 256 * viewport.camera_zoom, 64 * viewport.camera_zoom
        sx = tsx + sw
        sy = tsy + sh

        name = element['name']
        # frame
        if element['focus'] == False:
            pygame.draw.rect(screen, COLOR_FOREGROUND, (sx, sy, sw, sh), 1)
        else:
            pygame.draw.rect(screen, COLOR_ELEMENT_FOCUS, (sx, sy, sw, sh), 1)
        # name
        if element['focus'] == False:
            surface = font_name.render(name, True, COLOR_FOREGROUND)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh - int(text_h * 1.4)))
        else:
            surface = font_name.render(name, True, COLOR_ELEMENT_FOCUS)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh - int(text_h * 1.4)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

