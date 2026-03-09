import pygame

pygame.init()
WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ozone Engineering Assistant")

font = pygame.font.SysFont(None, 36)

project = {
}

field_text = ''

clock = pygame.time.Clock()

field_1 = {
    'val': '',
    'x': 50,
    'y': 100,
    'w': 200,
    'h': 30,
}

field_2 = {
    'val': '',
    'x': 50,
    'y': 200,
    'w': 200,
    'h': 30,
}

fields = []
fields.append(field_1)
fields.append(field_2)

def draw_fields():
    for field_i, field in enumerate(fields):
        if field_i == field_i_cur:
            border_color = (0, 0, 255)
        else:
            border_color = (200, 200, 200)
        pygame.draw.rect(screen, border_color, (field['x'], field['y'], field['w'], field['h']), 2)
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

    title = font.render("Project Management", True, (255, 255, 255))
    screen.blit(title,(50,50))

    draw_fields()

    mouse_pos = font.render(f'{mouse_x} - {mouse_y}', True, (255, 0, 255))
    screen.blit(mouse_pos, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
