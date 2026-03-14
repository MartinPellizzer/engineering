import pygame

COLOR_BACKGROUND = (10, 10, 10)
BORDER_COLOR = (100, 100, 100)
COLOR_LABEL = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAY")

FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
font_label = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 14)

def node(_id=0, kind='frame', val='',
        direction='row', 
        w_min=0, h_min=0,
        x=0, y=0, w=0, h=0, 
        padding_left=0, padding_right=0, padding_top=0, padding_bottom=0,
        gap=0, background_color=(0, 0, 0),
        children=[], 
):
    return {
        'id': _id,
        'kind': kind,
        'val': val,
        'direction': direction,
        'start_x': x,
        'start_y': y,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'w_min': w_min,
        'h_min': h_min,
        'padding_left': padding_left,
        'padding_right': padding_right,
        'padding_top': padding_top,
        'padding_bottom': padding_bottom,
        'gap': gap,
        'background_color': background_color,
        'children': children,
    }

'''
sidebar_w = 200
root = node(_id=0, direction='row', children=
    [
        node(_id=0, direction='row', w_min=sidebar_w, h_min=HEIGHT, background_color=(20, 20, 20,), children=
            [
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(60, 60, 60,), children=[]),
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(80, 80, 80,), children=[]),
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(100, 100, 100,), children=[]),
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(120, 120, 120,), children=[]),
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(140, 140, 140,), children=[]),
                node(_id=0, direction='row', w_min=40, h_min=20, background_color=(160, 160, 160,), children=[]),
            ]
        ), 
        node(_id=0, direction='row', w_min=WIDTH-sidebar_w, h_min=HEIGHT, background_color=(40, 40, 40,), children=[]), 
    ]
)
'''

'''
root = node(_id=0, direction='col', background_color=(100, 100, 100), children=
    [
        node(_id=0, direction='row', w_min=200, h_min=100, background_color=(20, 20, 20), children=[]),
        node(_id=0, direction='row', w_min=100, h_min=200, background_color=(40, 40, 40), children=[]), 
    ]
)
'''

sidebar_w = 200
topbar_h = 50
root = node(direction='col', background_color=(255, 0, 255), children=
    [
        # topbar
        node(direction='row', w_min=WIDTH, h_min=topbar_h, background_color=(20, 20, 20), children=
            [
            ]
        ),
        
        # center frame
        node(direction='row', w_min=WIDTH, h_min=HEIGHT-topbar_h, background_color=(40, 40, 40), children=
            [
                    
                # sidebar
                node(direction='col', w_min=sidebar_w, h_min=HEIGHT-topbar_h, 
                    padding_left=10, padding_right=10, padding_top=10, padding_bottom=10, gap=10,
                    background_color=(60, 60, 60), children=
                    [
                        
                        # sidebar item 1
                        node(direction='row', h=topbar_h, gap=10,
                            background_color=(80, 80, 80), children=
                            [
                                node(kind='label', val='label 1', w_min=100, h_min=30, background_color=(100, 100, 100), children=[]),
                                node(kind='label', val='label 2', w_min=100, h_min=30, background_color=(120, 120, 120), children=[]),
                            ]
                        ),
                        # sidebar item 2
                        node(direction='row', h=topbar_h, gap=10,
                            background_color=(80, 80, 80), children=
                            [
                                node(kind='label', val='label 3', w_min=100, h_min=30, background_color=(100, 100, 100), children=[]),
                                node(kind='label', val='label 4', w_min=100, h_min=30, background_color=(120, 120, 120), children=[]),
                            ]
                        ),
                    ]
                ),

                # main frame
                node(direction='col', w_min=WIDTH-sidebar_w, h_min=HEIGHT-topbar_h, background_color=(140, 140, 140), children=
                    [
                    ]
                ),
            ]
        ),
        
        # center frame

        # node(direction='row', w=WIDTH, h=HEIGHT-(topbar_h*3), background_color=(60, 60, 60), children=[]),
    ]
)

'''
'''

def layout_calc_size(node):

    # recursion (do this first to traverse tree in "backwards" order)
    for child in node['children']:
        layout_calc_size(child)

    # >> row direction
    # calc dynamic width of node (only if 0 case)
    if node['direction'] == 'row':
        node_w = 0
        node_h = 0
        for child in node['children']:
            node_w += child['w']
            node_h = max(node_h, child['h'])
            node['w'] = node_w
            node['h'] = node_h
        node['w'] += node['padding_left'] + node['padding_right'] + (node['gap'] * (len(node['children']) - 1))
        node['h'] += node['padding_top'] + node['padding_bottom']

    # >> col direction
    # calc dynamic height of node (only if 0 case)
    if node['direction'] == 'col':
        node_w = 0
        node_h = 0
        for child in node['children']:
            node_w = max(node_w, child['w'])
            node_h += child['h']
            node['w'] = node_w
            node['h'] = node_h
        node['w'] += node['padding_left'] + node['padding_right']
        node['h'] += node['padding_top'] + node['padding_bottom'] + (node['gap'] * (len(node['children']) - 1))

    # override calculated sized if base size specified
    if node['w_min'] != 0:
        node['w'] = max(node['w_min'], node['w'])
    if node['h_min'] != 0:
        node['h'] = max(node['h_min'], node['h'])

def layout_calc_pos(node):

    # >> row direction
    # calc dynamic pos of children (based on current node)
    if node['direction'] == 'row':
        offset_x = node['padding_left']
        offset_y = node['padding_top']
        for child in node['children']:
            child['x'] = node['x'] + offset_x
            child['y'] = node['y'] + offset_y
            offset_x += child['w'] + node['gap']

    # >> col direction
    # calc dynamic pos of children (based on current node)
    if node['direction'] == 'col':
        offset_x = node['padding_left']
        offset_y = node['padding_top']
        for child in node['children']:
            child['x'] = node['x'] + offset_x
            child['y'] = node['y'] + offset_y
            offset_y += child['h'] + node['gap']

    # recursion (do this last to traverse tree id "forward" order)
    for child in node['children']:
        layout_calc_pos(child)



def layout(root):
    # print('-:', node['id'], node['x'], node['y'], node['w'], node['h'])
    layout_calc_size(root)
    layout_calc_pos(root)

def draw(node):
    if node['kind'] == 'frame':
        pygame.draw.rect(screen, node['background_color'], (node['x'], node['y'], node['w'], node['h']))
    if node['kind'] == 'label': 
        pygame.draw.rect(screen, node['background_color'], (node['x'], node['y'], node['w'], node['h']))
        surface = font_label.render(node['val'], True, COLOR_LABEL)
        screen.blit(surface, (node['x'], node['y']))

    for child in node['children']:
        draw(child)



def print_tree(node, indent=0):
    print(" " * indent + f"{node['id']} ({node['x']},{node['y']}) {node['w']}x{node['h']}")
    for child in node["children"]:
        print_tree(child, indent + 4)

# layout_calc_size(root)
# layout_calc_pos(root)
# print_tree(root, indent=0)
# quit()


layout(root)

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR_BACKGROUND)


    layout(root)
    draw(root)
        
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

