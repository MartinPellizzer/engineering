import os
import json
import pygame

from reportlab.pdfgen import canvas

c = canvas.Canvas('hello.pdf')

c.drawString(100, 700, 'Hello World')

c.save()

# FONT_FAMILY = None
FONT_FAMILY = 'fonts/Inter/static/Inter_18pt-Regular.ttf'
FONT_FAMILY_INTER_MEDIUM = 'fonts/Inter/static/Inter_18pt-Medium.ttf'
FONT_FAMILY_INTER_REGULAR = 'fonts/Inter/static/Inter_18pt-Regular.ttf'
# FONT_FAMILY = 'fonts/Inter/static/Inter_18pt-ExtraLight.ttf'

COLOR_LABEL = (16, 16, 16)
COLOR_ENTRY = (48, 48, 48)
COLOR_BACKGROUND = (255, 255, 255)
COLOR_BORDER_GRAY = (200, 200, 200)
COLOR_BORDER_BLUE = (0, 0, 255)

pygame.init()
WIDTH, HEIGHT = 1280, 720 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aurora")

font_14 = pygame.font.Font(FONT_FAMILY, 14)
font_16 = pygame.font.Font(FONT_FAMILY, 16)
font_18 = pygame.font.Font(FONT_FAMILY, 18)
font = pygame.font.Font(FONT_FAMILY, 36)

font_label = pygame.font.Font(FONT_FAMILY_INTER_MEDIUM, 14)
font_entry = pygame.font.Font(FONT_FAMILY_INTER_REGULAR, 14)

clock = pygame.time.Clock()

node = {
    'val': 1,
    'w': 0,
    'h': 0,
    'children': [
        {
            'val': 5,
            'w': 100,
            'h': 30,
            'children': [
                {
                    'val': 5,
                    'w': 100,
                    'h': 30,
                    'children': []
                },
            ]
        },
        {
            'val': 5,
            'w': 100,
            'h': 30,
            'children': []
        },
    ],
}

root = {
    'type': 'frame',
    'val': '',
    "width": 0,
    "height": 0,
    "children": [
        {
            'type': 'label',
            'val': 'label 1',
            "width": 50, 
            "height": 20, 
            "children": [
                {
                    'type': 'label',
                    'val': 'label 3',
                    "width": 50, 
                    "height": 20, 
                    "children": []
                },
            ]
        },
        {
            'type': 'label',
            'val': 'label 2',
            "width": 30, "height": 40, "children": []
        }
    ]
}

def print_tree(node, indent=0):
    print(" " * indent + f"{node['type']} ({node['x']},{node['y']}) {node['width']}x{node['height']}")
    for child in node["children"]:
        print_tree(child, indent + 4)

def node(node_type, children=None, direction=None, gap=0, val='',
        padding_left=0, padding_right=0, padding_top=0, padding_bottom=0,
        align='start', justify='start', fixed_width=None, fixed_height=None, flex=0,
):
    return {
        "type": node_type,
        "children": children or [],
        "direction": direction,
        "gap": gap,

        'padding_left': padding_left,
        'padding_right': padding_right,
        'padding_top': padding_top,
        'padding_bottom': padding_bottom,

        'align': align,
        'justify': justify,

        'fixed_width': fixed_width,
        'fixed_height': fixed_height,

        'flex': flex,

        "width": 0,
        "height": 0,
        "x": 0,
        "y": 0,

        "val": val,
    }

def intrinsic_size(node):
    if node['type'] == 'button':
        return 80, 30
    if node['type'] == 'label':
        w, h = font_label.size(node['val'])
        return w, h
    if node['type'] == 'entry':
        return 120, 30
    return 0, 0

root = node("frame", 
    [
        node("frame",
            [
                node("label", val='label 1'),
                node("entry", val='')
            ],
            direction='row',
            flex=1
        ),

        node("frame", 
            [
                node("label", val='label 10'),
                node("label", val='label 11'),
                node("label", val='label 12'),
                node("label", val='label 13'),
                node("label", val='label 14'),
            ], 
            direction='row', 
            gap=30,
        ),

        node("frame", 
            [
                node("label", val='label 333'),
                node("label", val='label 4')
            ], 
            direction='column', 
            gap=30,
        ),

    ], 
    direction="column", 
    gap=50,
    padding_left=20,
    padding_right=20,
    padding_top=20,
    padding_bottom=20,
    align='start',
    justify='start',
    fixed_width=800,
    fixed_height=600,
)

root = node("frame", fixed_width=WIDTH, fixed_height=HEIGHT, direction="row", children=
    [
        node('frame', fixed_width=200, fixed_height=HEIGHT, direction="column", children=
            [
                node('frame', fixed_width=200, fixed_height=100, direction="row", children=
                    [
                        node('label', fixed_width=100, fixed_height=100, val='label 1'),
                        node('label', fixed_width=100, fixed_height=100, val='label 2'),
                    ]
                ),
                node('frame', fixed_width=200, fixed_height=100),
                node('frame', fixed_width=200, fixed_height=100),
            ]
        ),
        node('frame', fixed_width=WIDTH-200, fixed_height=HEIGHT),
    ],
)

def compute_container_size(node):

    children = node["children"]
    gap = node['gap']
    count = len(children)

    pad_l = node['padding_left']
    pad_r = node['padding_right']
    pad_t = node['padding_top']
    pad_b = node['padding_bottom']

    if count == 0:
        width = pad_l + pad_r
        height = pad_t + pad_b
        if node['fixed_width'] is not None:
            width = node['fixed_width']
        if node['fixed_height'] is not None:
            height = node['fixed_height']
        node['width'] = width
        node['height'] = height
        return

    if node["direction"] == "row":
        total_width = 0
        max_height = 0
        total_flex = 0

        for child in children:
            total_width += child["width"]
            max_height = max(max_height, child["height"])
            total_flex += child['flex']

        if count > 1:
            total_width += gap * (count - 1)

        width = total_width + pad_l + pad_r
        height = max_height + pad_t + pad_b

        if node['fixed_width'] is not None:
            width = node['fixed_width']
        if node['fixed_height'] is not None:
            height = node['fixed_height']

        free_space = width - pad_l - pad_r - (total_width - (gap * (count - 1)))

        if total_flex > 0 and free_space > 0:
            used_space = 0

            for i, child in enumerate(children):

                if child['flex'] > 0:

                    if i == len(children) - 1:
                        extra = free_space - used_space
                    else:
                        extra = int(free_space * (child['flex'] / total_flex))
                        used_space += extra

                    child['width'] += extra

                    # if child is container, recompute it
                    if child['children']:
                        compute_container_size(child)

        node['width'] = width
        node['height'] = height

    elif node["direction"] == "column":
        max_width = 0
        total_height = 0
        total_flex = 0

        for child in children:
            max_width = max(max_width, child["width"])
            total_height += child["height"]
            total_flex += child['flex']

        if count > 1:
            total_height += gap * (count - 1)

        width = max_width + pad_l + pad_r
        height = total_height + pad_t + pad_b

        if node['fixed_width'] is not None:
            width = node['fixed_width']
        if node['fixed_height'] is not None:
            height = node['fixed_height']

        free_space = height - pad_t - pad_b - (total_height - (gap * (count - 1)))

        if total_flex > 0 and free_space > 0:
            used_space = 0

            for i, child in enumerate(children):

                if child['flex'] > 0:

                    if i == len(children) - 1:
                        extra = free_space - used_space
                    else:
                        extra = int(free_space * (child['flex'] / total_flex))
                        used_space += extra

                    child['height'] += extra

                    if child['children']:
                        compute_container_size(child)

        node['width'] = width
        node['height'] = height


def compute_size(node):
    # case leaf node
    if len(node["children"]) == 0:
        w, h = intrinsic_size(node)
        if node['fixed_width'] is not None:
            w = node['fixed_width']
        if node['fixed_height'] is not None:
            h = node['fixed_height']
        node["width"] = w
        node["height"] = h
        return

    # case container node
    # first compute children
    for child in node["children"]:
        compute_size(child)
    # then compute container size
    compute_container_size(node)

def compute_position(node, x, y):

    # set this node's position
    node["x"] = x
    node["y"] = y


    # if leaf, nothing more to do
    if len(node["children"]) == 0:
        return

    gap = node['gap']

    pad_l = node['padding_left']
    pad_r = node['padding_right']
    pad_t = node['padding_top']
    pad_b = node['padding_bottom']

    align = node['align']
    justify = node['justify']

    children = node['children']
    count = len(children)

    # ROW LAYOUT
    if node["direction"] == "row":

        total_child_width = sum(c['width'] for c in children)
        total_gap = gap * (count - 1) if count > 1 else 0

        free_space = node['width'] - pad_l - pad_r - total_child_width - total_gap

        start_offset = 0

        if justify == 'center':
            start_offset = free_space / 2
        elif justify == 'end':
            start_offset = free_space
        elif justify == 'space-between' and count > 1:
            gap = gap + free_space // (count - 1)

        current_x = x + pad_l + start_offset

        for child in children:

            free_cross = node['height'] - pad_t - pad_b - child['height']

            if align == 'center':
                offset_y = free_cross // 2
            elif align == 'end':
                offset_y = free_cross
            else: 
                offset_y = 0

            child_y = y + pad_t + offset_y

            compute_position(child, current_x, child_y)

            current_x += child["width"] + gap


    # COLUMN LAYOUT
    elif node["direction"] == "column":

        total_child_height = sum(c['height'] for c in children)
        total_gap = gap * (count - 1) if count > 1 else 0

        free_space = node['height'] - pad_t - pad_b - total_child_height - total_gap

        start_offset = 0

        if justify == 'center':
            start_offset = free_space // 2
        elif justify == 'end': 
            start_offset = free_space
        elif justify == 'space-between' and count > 1:
            gap = gap + free_space / (count - 1)

        current_y = y + pad_t + start_offset

        for child in children:

            free_cross = node['width'] - pad_l - pad_r - child['width']

            if align == 'center':
                offset_x = free_cross // 2
            elif align == 'end':
                offset_x = free_cross
            else: 
                offset_x = 0

            child_x = x + pad_l + offset_x

            compute_position(child, child_x, current_y)

            current_y += child["height"] + gap

def layout(node, start_x=0, start_y=0):
    compute_size(node)
    compute_position(node, start_x, start_y)

layout(root, start_x=100, start_y=100)
print_tree(root, indent=0)
# quit()


def draw_recursive(node):
    if node['type'] == 'frame': 
        # pygame.draw.rect(screen, (200, 200, 200,), (node['x'], node['y'], node['width'], node['height']))
        pygame.draw.rect(screen, (0, 0, 0), (node['x'], node['y'], node['width'], node['height']), 1)
    elif node['type'] == 'label': 
        surface = font_label.render(node['val'], True, COLOR_LABEL)
        screen.blit(surface, (node['x'], node['y']))
    elif node['type'] == 'entry':
        '''
        if node['focus'] == True:
            pygame.draw.rect(screen, COLOR_BORDER_BLUE, (node['x'], node['y'], node['w'], node['h']), 1)
        else:
        '''
        pygame.draw.rect(screen, (0, 0, 0), (node['x'], node['y'], node['width'], node['height']), 1)
        # surface = font_entry.render(node['val'], True, COLOR_ENTRY)
        # screen.blit(surface, (node['x'] + (node['height'] // 4), node['y'] + (node['height'] // 4)))

    for child in node['children']:
        draw_recursive(child)

running = True
while running:
    mouse_x,mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(COLOR_BACKGROUND)

    
    layout(root, start_x=0, start_y=0)
    draw_recursive(root)
    # print_tree(root)
    # print(root)
    # quit()

    mouse_pos = font.render(f'{mouse_x} - {mouse_y}', True, (255, 0, 255))
    screen.blit(mouse_pos, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
