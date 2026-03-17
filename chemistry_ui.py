import pygame

COLOR_BACKGROUND = (10, 10, 10)
COLOR_FOREGROUND = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_number_start_size = 14
font_symbol_start_size = 24
font_name_start_size = 10
font_symbol = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_symbol_start_size)
font_number = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_number_start_size)
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_name_start_size)

element_hydrogen = {
    'number': '1',
    'symbol': 'H',
    'name': 'hydrogen',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 0,
    'col_i': 0,
}

element_helium = {
    'number': '2',
    'symbol': 'He',
    'name': 'helium',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 0,
    'col_i': 17,
}

element_lithium = {
    'number': '3',
    'symbol': 'Li',
    'name': 'lithium',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 0,
}

element_berylium = {
    'number': '4',
    'symbol': 'Be',
    'name': 'berylium',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 1,
}

element_boron = {
    'number': '5',
    'symbol': 'B',
    'name': 'boron',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 12,
}

element_carbon = {
    'number': '6',
    'symbol': 'C',
    'name': 'carbon',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 13,
}

element_nitrogen = {
    'number': '7',
    'symbol': 'N',
    'name': 'nitrogen',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 14,
}

element_oxygen = {
    'number': '8',
    'symbol': 'O',
    'name': 'oxygen',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 15,
}

element_fluorine = {
    'number': '9',
    'symbol': 'F',
    'name': 'fluorine',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 16,
}

element_neon = {
    'number': '10',
    'symbol': 'Ne',
    'name': 'neon',
    'x': 0,
    'y': 0,
    'w': 64,
    'h': 64,
    'row_i': 1,
    'col_i': 17,
}

periodic_table = {
    'x': 0, 
    'y': 0, 
    'elements': []
}

periodic_table['elements'].append(element_hydrogen)
periodic_table['elements'].append(element_helium)
periodic_table['elements'].append(element_lithium)
periodic_table['elements'].append(element_berylium)
periodic_table['elements'].append(element_boron)
periodic_table['elements'].append(element_carbon)
periodic_table['elements'].append(element_nitrogen)
periodic_table['elements'].append(element_oxygen)
periodic_table['elements'].append(element_fluorine)
periodic_table['elements'].append(element_neon)

def world_to_screen(x, y):
    sx = (x - camera_x) * camera_zoom
    sy = (y - camera_y) * camera_zoom
    return int(sx), int(sy)

def screen_to_world(x, y):
    wx = (x / camera_zoom) + camera_x
    wy = (y / camera_zoom) + camera_y
    return wx, wy

MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
camera_x = 0
camera_y = 0
camera_zoom = 1.0
panning = False
pan_last_x = 0
pan_last_y = 0

running = True
while running:
    mouse_x,mouse_y = pygame.mouse.get_pos()
    world_x, world_y = screen_to_world(mouse_x, mouse_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # ZOOM ON MOUSE POS
            if event.button == 4 or event.button == 5:
                # world position before zoom
                before_x, before_y = screen_to_world(mouse_x, mouse_y)

                if event.button == 4:
                    camera_zoom *= 1.1
                    camera_zoom = min(camera_zoom, MAX_ZOOM)
                    font_symbol = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_symbol_start_size * camera_zoom))
                    font_number = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_number_start_size * camera_zoom))
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_name_start_size * camera_zoom))

                elif event.button == 5:
                    camera_zoom /= 1.1
                    camera_zoom = max(camera_zoom, MIN_ZOOM)
                    font_symbol = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_symbol_start_size * camera_zoom))
                    font_number = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_number_start_size * camera_zoom))
                    font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, int(font_name_start_size * camera_zoom))

                # world position after zoom
                after_x, after_y = screen_to_world(mouse_x, mouse_y)

                # adjust camera so point under cursor stays fixed
                camera_x += before_x - after_x
                camera_y += before_y - after_y

            elif event.button == 2:
                panning = True
                pan_last_x, pan_last_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                panning = False

        if event.type == pygame.MOUSEMOTION:
            if panning:
                dx = mouse_x - pan_last_x
                dy = mouse_y - pan_last_y
                camera_x -= dx / camera_zoom
                camera_y -= dy / camera_zoom
                pan_last_x = mouse_x
                pan_last_y = mouse_y

    screen.fill(COLOR_BACKGROUND)

    tsx, tsy = world_to_screen(periodic_table["x"], periodic_table["y"])
    for element in periodic_table['elements']:
        sw, sh = 64 * camera_zoom, 64 * camera_zoom
        sx = tsx + sw * element['col_i']
        sy = tsy + sh * element['row_i']

        number = element['number']
        symbol = element['symbol']
        name = element['name']
        pygame.draw.rect(screen, COLOR_FOREGROUND, (sx, sy, sw, sh), 1)
        # number
        surface = font_number.render(number, True, COLOR_FOREGROUND)
        screen.blit(surface, (sx + int(4 * camera_zoom), sy + int(4 * camera_zoom)))
        # symbol
        surface = font_symbol.render(symbol, True, COLOR_FOREGROUND)
        text_w, text_h = surface.get_size()
        screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh//2 - text_h//2))
        # name
        surface = font_name.render(name, True, COLOR_FOREGROUND)
        text_w, text_h = surface.get_size()
        screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh - int(text_h * 1.4)))

        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

