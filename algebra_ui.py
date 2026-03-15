import pygame

import sympy
from sympy import symbols
from sympy.solvers import solve

from lay import layout, node

x = symbols('x')

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ALGEBRA UI")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'

theme_0000 = {
    'background_color': (255, 255, 255),
    'label_font': pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 14),
    'label_color': (20, 20, 20),
}

theme_0001 = {
    'background_color': (20, 20, 20),
    'label_font': pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 14),
    'label_color': (255, 255, 255),
}

theme_cur = theme_0000

entry_1 = node(
    kind='entry', val='x**2 - 2', w_min=200, h_min=30, background_color=theme_cur['background_color'], children=[]
)
label_1 = node(
    kind='label', val='res', w_min=200, h_min=30, background_color=theme_cur['background_color'], children=[]
)

root = node(
    direction='col', w_min=600, h_min=HEIGHT, 
    padding_left=10, padding_right=10, padding_top=10, padding_bottom=10, gap=10,
    background_color=theme_cur['background_color'], 
    children=
    [
        node(
            direction='row', gap=10,
            background_color=theme_cur['background_color'], 
            children=
            [
                entry_1,
                label_1,
            ]
        ),
    ]
)

def draw(node):
    if node['kind'] == 'frame':
        pygame.draw.rect(screen, node['background_color'], (node['x'], node['y'], node['w'], node['h']))
    if node['kind'] == 'label': 
        pygame.draw.rect(screen, node['background_color'], (node['x'], node['y'], node['w'], node['h']))
        surface = theme_cur['label_font'].render(node['val'], True, theme_cur['label_color'])
        screen.blit(surface, (node['x'], node['y']))
    if node['kind'] == 'entry':
        pygame.draw.rect(screen, (0, 0, 0), (node['x'], node['y'], node['w'], node['h']), 1)
        surface = theme_cur['label_font'].render(node['val'], True, theme_cur['label_color'])
        screen.blit(surface, (node['x'] + (node['h'] // 4), node['y'] + (node['h'] // 4)))

    for child in node['children']:
        draw(child)




running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                entry_1['val'] = entry_1['val'][:-1]
            elif event.key == pygame.K_RETURN:
                label_1['val'] = str(solve(entry_1['val'], x)[0])
            else:
                entry_1['val'] += event.unicode

    screen.fill(theme_cur['background_color'])


    layout(root)
    draw(root)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

