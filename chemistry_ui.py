import pygame

COLOR_BACKGROUND = (10, 10, 10)
COLOR_FOREGROUND = (255, 255, 255)
COLOR_ELEMENT_FOCUS = (128, 128, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_details_size = 48
font_number_start_size = 14
font_symbol_start_size = 24
font_name_start_size = 10
font_details = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_details_size)
font_symbol = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_symbol_start_size)
font_number = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_number_start_size)
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_name_start_size)

def element_create(
    number, symbol, name, col_i, row_i, x=0, y=0, w=64, h=64, focus=False,
):
    element = {
        'number': number,
        'symbol': symbol,
        'name': name,
        'col_i': col_i,
        'row_i': row_i,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
    }
    return element

element_hydrogen =  element_create('1', 'H', 'hydrogen', 0, 0)
element_helium =    element_create('2', 'He', 'helium', 17, 0)
element_lithium =   element_create('3', 'Li', 'lithium', 0, 1)
element_berylium =  element_create('4', 'Be', 'berylium', 1, 1)
element_boron =     element_create('5', 'B', 'boron', 12, 1)
element_carbon =    element_create('6', 'C', 'carbon', 13, 1)
element_nitrogen =  element_create('7', 'N', 'nitrogen', 14, 1)
element_oxygen =    element_create('8', 'O', 'oxygen', 15, 1)
element_fluorine =  element_create('9', 'F', 'fluorine', 16, 1)
element_neon =      element_create('10', 'Ne', 'neon', 17, 1)

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
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    world_x, world_y = screen_to_world(mouse_screen_x, mouse_screen_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                for element in periodic_table['elements']:
                    tsx, tsy = world_to_screen(periodic_table["x"], periodic_table["y"])
                    sw, sh = 64 * camera_zoom, 64 * camera_zoom
                    sx = tsx + sw * element['col_i']
                    sy = tsy + sh * element['row_i']
                    element['focus'] = False
                    if (
                        mouse_screen_x > sx and mouse_screen_x < sx + sw and 
                        mouse_screen_y > sy and mouse_screen_y < sy + sh
                    ):
                        element['focus'] = True

            # ZOOM ON MOUSE POS
            elif event.button == 4 or event.button == 5:
                # world position before zoom
                before_x, before_y = screen_to_world(mouse_screen_x, mouse_screen_y)

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
                after_x, after_y = screen_to_world(mouse_screen_x, mouse_screen_y)

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
                dx = mouse_screen_x - pan_last_x
                dy = mouse_screen_y - pan_last_y
                camera_x -= dx / camera_zoom
                camera_y -= dy / camera_zoom
                pan_last_x = mouse_screen_x
                pan_last_y = mouse_screen_y

    screen.fill(COLOR_BACKGROUND)

    tsx, tsy = world_to_screen(periodic_table["x"], periodic_table["y"])
    for element in periodic_table['elements']:
        sw, sh = 64 * camera_zoom, 64 * camera_zoom
        sx = tsx + sw * element['col_i']
        sy = tsy + sh * element['row_i']

        number = element['number']
        symbol = element['symbol']
        name = element['name']
        # frame
        if element['focus'] == False:
            pygame.draw.rect(screen, COLOR_FOREGROUND, (sx, sy, sw, sh), 1)
        else:
            pygame.draw.rect(screen, COLOR_ELEMENT_FOCUS, (sx, sy, sw, sh), 1)
        # number
        if element['focus'] == False:
            surface = font_number.render(number, True, COLOR_FOREGROUND)
            screen.blit(surface, (sx + int(4 * camera_zoom), sy + int(4 * camera_zoom)))
        else:
            surface = font_number.render(number, True, COLOR_ELEMENT_FOCUS)
            screen.blit(surface, (sx + int(4 * camera_zoom), sy + int(4 * camera_zoom)))
        # symbol
        if element['focus'] == False:
            surface = font_symbol.render(symbol, True, COLOR_FOREGROUND)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh//2 - text_h//2))
        else:
            surface = font_symbol.render(symbol, True, COLOR_ELEMENT_FOCUS)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh//2 - text_h//2))
        # name
        if element['focus'] == False:
            surface = font_name.render(name, True, COLOR_FOREGROUND)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh - int(text_h * 1.4)))
        else:
            surface = font_name.render(name, True, COLOR_ELEMENT_FOCUS)
            text_w, text_h = surface.get_size()
            screen.blit(surface, (sx + sw//2 - text_w//2, sy + sh - int(text_h * 1.4)))

        # details
        if element['focus'] == True:
            surface = font_details.render(element['number'], True, (255, 0, 255))
            screen.blit(surface, (10, 10))
            surface = font_details.render(element['symbol'], True, (255, 0, 255))
            screen.blit(surface, (10, 60))
            surface = font_details.render(element['name'], True, (255, 0, 255))
            screen.blit(surface, (10, 110))
        
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

