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
font_number_start_size = 12
font_symbol_start_size = 24
font_name_start_size = 8
font_details = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_details_size)
font_symbol = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_symbol_start_size)
font_number = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_number_start_size)
font_name = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, font_name_start_size)

def element_create(
    number, symbol, name, col_i, row_i, x=0, y=0, w=64, h=64, focus=False,
    extra=[], bg_color=None,
):
    element = {
        'number': number,
        'symbol': symbol,
        'name': name,
        'group': col_i+1,
        'col_i': col_i,
        'row_i': row_i,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
        'extra': extra,
        'bg_color': bg_color,
    }
    return element

element_hydrogen =  element_create('1', 'H', 'hydrogen', 0, 0)
element_helium =    element_create('2', 'He', 'helium', 17, 0)
###
element_lithium =   element_create('3', 'Li', 'lithium', 0, 1, extra=['+1 or 1+', 'alkali metal'])
element_berylium =  element_create('4', 'Be', 'berylium', 1, 1, extra=['+2 or 2+', 'alkali earth metal'])
element_boron =     element_create('5', 'B', 'boron', 12, 1, bg_color=(128, 128, 128), extra=['+3 or 3+'])
element_carbon =    element_create('6', 'C', 'carbon', 13, 1)
element_nitrogen =  element_create('7', 'N', 'nitrogen', 14, 1, extra=['-3 or 3-'])
element_oxygen =    element_create('8', 'O', 'oxygen', 15, 1, extra=['-2 or 2-'])
element_fluorine =  element_create('9', 'F', 'fluorine', 16, 1, extra=['-1 or 1-'])
element_neon =      element_create('10', 'Ne', 'neon', 17, 1)
###
element_sodium = element_create('11', 'Na', 'sodium', 0, 2, extra=['+1 or 1+', 'alkali metal'])
element_manganesium = element_create('12', 'Mg', 'manganesium', 1, 2, extra=['+2 or 2+', 'alkali earth metal'])
element_aluminium = element_create('13', 'Al', 'aluminium', 12, 2, extra=['+3 or 3+'])
element_silicon = element_create('14', 'Si', 'silicon', 13, 2, bg_color=(128, 128, 128))
element_phosphorus = element_create('15', 'P', 'phosphorus', 14, 2, extra=['-3 or 3-'])
element_sulfur = element_create('16', 'S', 'sulfur', 15, 2, extra=['-2 or 2-'])
element_chlorine = element_create('17', 'Cl', 'chlorine', 16, 2, extra=['-1 or 1-'])
element_argon = element_create('18', 'Ar', 'argon', 17, 2)
###
element_potassium = element_create('19', 'K', 'potassium', 0, 3, extra=['+1 or 1+', 'alkali metal'])
element_calcium = element_create('20', 'Ca', 'calcium', 1, 3, extra=['+2 or 2+', 'alkali earth metal'])
element_scandium = element_create('21', 'Sc', 'scandium', 2, 3)
element_titanium = element_create('22', 'Ti', 'titanium', 3, 3)
element_vanadium = element_create('23', 'V', 'vanadium', 4, 3)
element_chromium = element_create('24', 'Cr', 'chromium', 5, 3)
element_manganese = element_create('25', 'Mn', 'manganese', 6, 3)
element_iron = element_create('26', 'Fe', 'iron', 7, 3)
element_cobalt = element_create('27', 'Co', 'cobalt', 8, 3)
element_nickel = element_create('28', 'Ni', 'nickel', 9, 3)
element_copper = element_create('29', 'Cu', 'copper', 10, 3)
element_zinc = element_create('30', 'Zn', 'zinc', 11, 3)
element_gallium = element_create('31', 'Ga', 'gallium', 12, 3, extra=['+3 or 3+'])
element_germanium = element_create('32', 'Ge', 'germanium', 13, 3)
element_arsenic = element_create('33', 'As', 'arsenic', 14, 3, bg_color=(128, 128, 128), extra=['-3 or 3-'])
element_selenium = element_create('34', 'Se', 'selenium', 15, 3, extra=['-2 or 2-'])
element_bromine = element_create('35', 'Br', 'bromine', 16, 3, extra=['-1 or 1-'])
element_krypton = element_create('36', 'Kr', 'krypton', 17, 3)
###
element_rubidium = element_create('37', 'Rb', 'rubidium', 0, 4, extra=['+1 or 1+', 'alkali metal'])
element_strontium = element_create('38', 'Sr', 'strontium', 1, 4, extra=['+2 or 2+', 'alkali earth metal'])
element_yttrium = element_create('39', 'Y', 'yttrium', 2, 4)
element_zirconium = element_create('40', 'Zr', 'zirconium', 3, 4)
element_niobium = element_create('41', 'Nb', 'niobium', 4, 4)
element_molybdenum = element_create('42', 'Mo', 'molybdenum', 5, 4)
element_technetium = element_create('43', 'Tc', 'technetium', 6, 4)
element_ruthenium = element_create('44', 'Ru', 'ruthenium', 7, 4)
element_rhodium = element_create('45', 'Rh', 'rhodium', 8, 4)
element_palladium = element_create('46', 'Pd', 'palladium', 9, 4)
element_silver = element_create('47', 'Ag', 'silver', 10, 4)
element_cadmium = element_create('48', 'Cd', 'cadmium', 11, 4)
element_indium = element_create('49', 'In', 'indium', 12, 4, extra=['+3 or 3+'])
element_tin = element_create('50', 'Sn', 'tin', 13, 4)
element_antimony = element_create('51', 'Sb', 'antimony', 14, 4, extra=['-3 or 3-'])
element_tellurium = element_create('52', 'Te', 'tellurium', 15, 4, bg_color=(128, 128, 128), extra=['-2 or 2-'])
element_iodine = element_create('53', 'I', 'iodine', 16, 4, extra=['-1 or 1-'])
element_xenon = element_create('54', 'Xe', 'xenon', 17, 4)
###
element_caesium = element_create('55', 'Ca', 'caesium', 0, 5, extra=['+1 or 1+', 'alkali metal'])
element_barium = element_create('56', 'Ba', 'barium', 1, 5, extra=['+2 or 2+', 'alkali earth metal'])
element_lantharum = element_create('57', 'La', 'lantharum', 2, 5)
element_hafnium = element_create('72', 'Hf', 'hafnium', 3, 5)
element_tantalum = element_create('73', 'Ta', 'tantalum', 4, 5)
element_tungsten = element_create('74', 'W', 'tungsten', 5, 5)
element_rhenium = element_create('75', 'Re', 'rhenium', 6, 5)
element_osmium = element_create('76', 'Os', 'osmium', 7, 5)
element_iridium = element_create('77', 'Ir', 'iridium', 8, 5)
element_platinum = element_create('78', 'Pt', 'platinum', 9, 5)
element_aurum = element_create('79', 'Au', 'aurum', 10, 5)
element_mercury = element_create('80', 'Hg', 'mercury', 11, 5)
element_thallium = element_create('81', 'Tl', 'thallium', 12, 5, extra=['+3 or 3+'])
element_lead = element_create('82', 'Pb', 'lead', 13, 5)
element_bismuth = element_create('83', 'Bi', 'bismuth', 14, 5, extra=['-3 or 3-'])
element_pollonium = element_create('84', 'Po', 'pollonium', 15, 5, extra=['-2 or 2-'])
element_astatine = element_create('85', 'At', 'astatine', 16, 5, bg_color=(128, 128, 128), extra=['-1 or 1-'])
element_radon = element_create('86', 'Rn', 'radon', 17, 5)
###
element_francium = element_create('87', 'Fr', 'francium', 0, 6)
element_radium = element_create('88', 'Ra', 'radium', 1, 6)
element_actinium = element_create('89', 'Ac', 'actinium', 2, 6)
element_rutherfordium = element_create('104', 'Rf', 'rutherfordium', 3, 6)
element_dubnium = element_create('105', 'Db', 'dubnium', 4, 6)
element_seaborgium = element_create('106', 'Sg', 'seaborgium', 5, 6)
element_bohrium = element_create('107', 'Bh', 'bohrium', 6, 6)
element_hassium = element_create('108', 'Hs', 'hassium', 7, 6)
element_meitnerium = element_create('109', 'Mt', 'meitnerium', 8, 6)
element_darmstadium = element_create('110', 'Ds', 'darmstadium', 9, 6)
element_roentgenium = element_create('111', 'Rg', 'roentgenium', 10, 6)
element_copernicium = element_create('112', 'Cn', 'copernicium', 11, 6)
element_nihonium = element_create('113', 'Nh', 'nihonium', 12, 6)
element_flevorium = element_create('114', 'Fl', 'flevorium', 13, 6)
element_moscovium = element_create('115', 'Mc', 'moscovium', 14, 6)
element_livemorium = element_create('116', 'Lv', 'livemorium', 15, 6)
element_tennessine = element_create('117', 'Ts', 'tennessine', 16, 6)
element_oganesson = element_create('118', 'Og', 'oganesson', 17, 6)
###
element_cerium = element_create('58', 'Ce', 'cerium', 3, 8)
element_praseodymium = element_create('59', 'Pr', 'praseodymium', 4, 8)
element_neodymium = element_create('60', 'Nd', 'neodymium', 5, 8)
element_promethium = element_create('61', 'Pm', 'promethium', 6, 8)
element_samarium = element_create('62', 'Sm', 'samarium', 7, 8)
element_europium = element_create('63', 'Eu', 'europium', 8, 8)
element_gadolinium = element_create('64', 'Gd', 'gadolinium', 9, 8)
element_terbium = element_create('65', 'Tb', 'terbium', 10, 8)
element_dysprosium = element_create('66', 'Dy', 'dysprosium', 11, 8)
element_holmium = element_create('67', 'Ho', 'holmium', 12, 8)
element_erbium = element_create('68', 'Er', 'erbium', 13, 8)
element_thulium = element_create('69', 'Tm', 'thulium', 14, 8)
element_ytterbium = element_create('70', 'Yb', 'ytterbium', 15, 8)
element_lutetium = element_create('71', 'Lu', 'lutetium', 16, 8)

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
###
periodic_table['elements'].append(element_sodium)
periodic_table['elements'].append(element_manganesium)
periodic_table['elements'].append(element_aluminium)
periodic_table['elements'].append(element_silicon)
periodic_table['elements'].append(element_phosphorus)
periodic_table['elements'].append(element_sulfur)
periodic_table['elements'].append(element_chlorine)
periodic_table['elements'].append(element_argon)
###
periodic_table['elements'].append(element_potassium)
periodic_table['elements'].append(element_calcium)
periodic_table['elements'].append(element_scandium)
periodic_table['elements'].append(element_titanium)
periodic_table['elements'].append(element_vanadium)
periodic_table['elements'].append(element_chromium)
periodic_table['elements'].append(element_manganese)
periodic_table['elements'].append(element_iron)
periodic_table['elements'].append(element_cobalt)
periodic_table['elements'].append(element_nickel)
periodic_table['elements'].append(element_copper)
periodic_table['elements'].append(element_zinc)
periodic_table['elements'].append(element_gallium)
periodic_table['elements'].append(element_germanium)
periodic_table['elements'].append(element_arsenic)
periodic_table['elements'].append(element_selenium)
periodic_table['elements'].append(element_bromine)
periodic_table['elements'].append(element_krypton)
###
periodic_table['elements'].append(element_rubidium)
periodic_table['elements'].append(element_strontium)
periodic_table['elements'].append(element_yttrium)
periodic_table['elements'].append(element_zirconium)
periodic_table['elements'].append(element_niobium)
periodic_table['elements'].append(element_molybdenum)
periodic_table['elements'].append(element_technetium)
periodic_table['elements'].append(element_ruthenium)
periodic_table['elements'].append(element_rhodium)
periodic_table['elements'].append(element_palladium)
periodic_table['elements'].append(element_silver)
periodic_table['elements'].append(element_cadmium)
periodic_table['elements'].append(element_indium)
periodic_table['elements'].append(element_tin)
periodic_table['elements'].append(element_antimony)
periodic_table['elements'].append(element_tellurium)
periodic_table['elements'].append(element_iodine)
periodic_table['elements'].append(element_xenon)
###
periodic_table['elements'].append(element_caesium)
periodic_table['elements'].append(element_barium)
periodic_table['elements'].append(element_lantharum)
periodic_table['elements'].append(element_hafnium)
periodic_table['elements'].append(element_tantalum)
periodic_table['elements'].append(element_tungsten)
periodic_table['elements'].append(element_rhenium)
periodic_table['elements'].append(element_osmium)
periodic_table['elements'].append(element_iridium)
periodic_table['elements'].append(element_platinum)
periodic_table['elements'].append(element_aurum)
periodic_table['elements'].append(element_mercury)
periodic_table['elements'].append(element_thallium)
periodic_table['elements'].append(element_lead)
periodic_table['elements'].append(element_bismuth)
periodic_table['elements'].append(element_pollonium)
periodic_table['elements'].append(element_astatine)
periodic_table['elements'].append(element_radon)
###
periodic_table['elements'].append(element_francium)
periodic_table['elements'].append(element_radium)
periodic_table['elements'].append(element_actinium)
periodic_table['elements'].append(element_rutherfordium)
periodic_table['elements'].append(element_dubnium)
periodic_table['elements'].append(element_seaborgium)
periodic_table['elements'].append(element_bohrium)
periodic_table['elements'].append(element_hassium)
periodic_table['elements'].append(element_meitnerium)
periodic_table['elements'].append(element_darmstadium)
periodic_table['elements'].append(element_roentgenium)
periodic_table['elements'].append(element_copernicium)
periodic_table['elements'].append(element_nihonium)
periodic_table['elements'].append(element_flevorium)
periodic_table['elements'].append(element_moscovium)
periodic_table['elements'].append(element_livemorium)
periodic_table['elements'].append(element_tennessine)
periodic_table['elements'].append(element_oganesson)
###
periodic_table['elements'].append(element_cerium)
periodic_table['elements'].append(element_praseodymium)
periodic_table['elements'].append(element_neodymium)
periodic_table['elements'].append(element_promethium)
periodic_table['elements'].append(element_samarium)
periodic_table['elements'].append(element_europium)
periodic_table['elements'].append(element_gadolinium)
periodic_table['elements'].append(element_terbium)
periodic_table['elements'].append(element_dysprosium)
periodic_table['elements'].append(element_holmium)
periodic_table['elements'].append(element_erbium)
periodic_table['elements'].append(element_thulium)
periodic_table['elements'].append(element_ytterbium)
periodic_table['elements'].append(element_lutetium)

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

    # check details on hover
    if 1:
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
            if element['bg_color'] != None:
                pygame.draw.rect(screen, element['bg_color'], (sx, sy, sw, sh))
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
            y_cur = 10
            details = ['number', 'symbol', 'name', 'group']
            for detail in details:
                surface = font_details.render(f'{detail}: {element[detail]}', True, (255, 0, 255))
                screen.blit(surface, (10, y_cur))
                y_cur += 50
            for extra in element['extra']:
                surface = font_details.render(f'{extra}', True, (255, 0, 255))
                screen.blit(surface, (10, y_cur))
                y_cur += 50
        
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

