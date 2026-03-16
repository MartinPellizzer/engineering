import pygame

COLOR_BACKGROUND = (10, 10, 10)
COLOR_FOREGROUND = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 36)

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR_BACKGROUND)

    pygame.draw.rect(screen, COLOR_FOREGROUND, (100, 100, 100, 100), 1)
    surface = font.render('O', True, COLOR_FOREGROUND)
    screen.blit(surface, (130, 130))

        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

