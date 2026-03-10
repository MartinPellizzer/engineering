import pygame

pygame.init()
WIDTH, HEIGHT = 1920, 1280 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ozone Engineering Assistant")

font_16 = pygame.font.SysFont(None, 16)
font_18 = pygame.font.SysFont(None, 18)
font = pygame.font.SysFont(None, 36)

project = {
}

field_text = ''

clock = pygame.time.Clock()

fields_0000 = [
    'Client Name',
    'Facility Name',
    'Contact Person',
    'Email',
    'Phone',
    'Location',
    'Industry',
]

fields_0001 = [
    'Process Description',
    'Fluid Type',
    'Treatment Stage',
]

fields_0002 = [
    'Average Flow Rate',
    'Maximum Flow Rate',
    'Unit (m3/h or L/min)',
]

fields_0003 = [
    'Contaminant Name',
    'Contaminant Current',
    'Contaminant Target',
]

fields_0004 = [
    'Available Power',
    'Available Space',
    'Existing Pumps',
    'Oxygen Supply',
    'Ventilation',
]

fields_0005 = [
    'Budget',
    'Deadline',
    'Regulatory Constraints',
    'Safety Constraints',
]

def field_create(name, x, y, w, h):
    obj = {
        'name': name,
        'val': '',
        'x': x,
        'y': y,
        'w': w,
        'h': h,
    }
    return obj

fields = []

row_size = 80
col_size = 300
x_start = 100
y_start = 100

col_i = 0
for i, field in enumerate(fields_0000):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

col_i = 1
for i, field in enumerate(fields_0001):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

col_i = 2
for i, field in enumerate(fields_0002):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

col_i = 3
for i, field in enumerate(fields_0003):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

col_i = 4
for i, field in enumerate(fields_0004):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

col_i = 5
for i, field in enumerate(fields_0005):
    x = x_start + (col_size * col_i)
    y = y_start + (row_size * i)
    fields.append(field_create(field, x, y, 200, 30))

def draw_fields():
    for field_i, field in enumerate(fields):
        if field_i == field_i_cur: border_color = (0, 0, 255)
        else: border_color = (200, 200, 200)
        # label
        surface = font_18.render(field['name'], True, (255, 255, 255))
        screen.blit(surface, (field['x'], field['y']-18))
        # field
        pygame.draw.rect(screen, border_color, (field['x'], field['y'], field['w'], field['h']), 1)
        surface = font.render(field['val'], True, (255, 255, 255))
        screen.blit(surface, (field['x']+5, field['y']+5))

field_i_cur = 0

running = True
while running:
    mouse_x,mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                fields[field_i_cur]['val'] = fields[field_i_cur]['val'][:-1]
            elif event.key == pygame.K_TAB:
                # active_index = (active_index + 1) % len(inputs)
                pass
            else:
                fields[field_i_cur]['val'] += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, field in enumerate(fields):
                if (mouse_x > field['x'] and 
                    mouse_x < field['x'] + field['w'] and
                    mouse_y > field['y'] and
                    mouse_y < field['y'] + field['h']
                ):
                    field_i_cur = i
                    break


    screen.fill((18, 18, 18))

    draw_fields()

    mouse_pos = font.render(f'{mouse_x} - {mouse_y}', True, (255, 0, 255))
    screen.blit(mouse_pos, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
