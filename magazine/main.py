import pygame
from PIL import Image, ImageDraw

pygame.init()

screen_w = 16*100
screen_h = 9*100

screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

a4_w = 2480 
a4_h = 3508
image_w, image_h = 2480, 3508
image = Image.new("RGB", (a4_w, a4_h), (255, 255, 255))
draw = ImageDraw.Draw(image)

canvas_mul = 0.25
canvas_w = int(2480*canvas_mul) 
canvas_h = int(3508*canvas_mul)

def draw_grid():
    grid_color_monocrome = 200
    grid_color = (grid_color_monocrome, grid_color_monocrome, grid_color_monocrome)
    grid_size = 8
    grid_col_num = (canvas_w // grid_size)
    for i in range(grid_col_num + 1):
        pygame.draw.line(
            screen, 
            grid_color, 
            (canvas_x + (i * grid_size), canvas_y), 
            (canvas_x + (i * grid_size), canvas_y + canvas_h)
    )
    
    grid_row_num = (canvas_h // grid_size)
    for i in range(grid_row_num + 1):
        pygame.draw.line(
            screen, 
            grid_color, 
            (canvas_x, canvas_y + (i * grid_size)), 
            (canvas_x + canvas_w, canvas_y + (i * grid_size))
    )

def draw_ruler():
    grid_col_num = 12
    grid_size = canvas_w / grid_col_num
    for i in range(grid_col_num + 1):
        pygame.draw.line(
            screen, 
            (255, 0, 255), 
            (canvas_x + (i * grid_size), 0), 
            (canvas_x + (i * grid_size), screen_h)
    )
    grid_row_num = 12
    grid_size = canvas_h / grid_row_num
    for i in range(grid_row_num + 1):
        pygame.draw.line(
            screen, 
            (255, 0, 255), 
            (canvas_x, canvas_y + (i * grid_size)), 
            (canvas_x + canvas_w, canvas_y + (i * grid_size))
    )

canvas = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
canvas = pygame.transform.smoothscale(canvas, (canvas_w, canvas_h))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    canvas_x = screen_w//2 - canvas_w//2
    canvas_y = screen_h//2 - canvas_h//2
    screen.blit(canvas, (canvas_x, canvas_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()