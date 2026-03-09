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

running = True
while running:
    text_changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                field_text = field_text[:-1]
            elif event.key == pygame.K_TAB:
                # active_index = (active_index + 1) % len(inputs)
                pass
            else:
                field_text += event.unicode

    screen.fill((18, 18, 18))

    title = font.render("Project Management", True, (255, 255, 255))
    screen.blit(title,(50,50))

    # field 1
    txt_surface = font.render(field_text, True, (255, 255, 255))
    screen.blit(txt_surface, (50+5, 100+5))
    pygame.draw.rect(screen, (200, 200, 200), (50, 100, 100, 30), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
