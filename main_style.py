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

def field_create(name, _type, x, y, w, h):
    obj = {
        'name': name,
        'label': name,
        'type': _type,
        'val': '',
        'x': x,
        'y': y,
        'w': w,
        'h': h,
    }
    return obj

fields = []

x_start = 400
y_start = 100
y_cur = 0
FIELD_HEIGHT = 34
for field in fields_0000:
    fields.append(field_create(field, 'entry', x_start, y_start + y_cur, 200, FIELD_HEIGHT))
    y_cur += 34 + 16

def draw_fields():
    surface = font_label.render('Project Settings', True, COLOR_LABEL)
    screen.blit(surface, (x_start, y_start))
    for field_i, field in enumerate(fields):
        if field_i == field_i_cur: border_color = (0, 0, 255)
        else: border_color = COLOR_BORDER_GRAY
        # label
        surface = font_label.render(field['name'], True, COLOR_LABEL)
        screen.blit(surface, (field['x'] - 200, field['y'] + (field['h'] // 4)))
        # field
        pygame.draw.rect(screen, border_color, (field['x'], field['y'], field['w'], field['h']), 1)
        surface = font_entry.render(field['val'], True, COLOR_ENTRY)
        screen.blit(surface, (field['x'] + (field['h'] // 4), field['y'] + (field['h'] // 4)))
    # frame
    pygame.draw.rect(screen, border_color, (x_start - 200 - 50, y_start - 50, 800, 800), 1)

field_i_cur = 0


########################################
########################################
########################################

def layout_components_col_row(parent):
    level_1_y_cur = 0
    for level_1 in parent['children']:
        level_1['x'] = parent['x']
        level_1['y'] = parent['y'] + level_1_y_cur
        level_2_x_cur = 0
        level_2_h_max = 0
        for level_2 in level_1['children']:
            if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
            else: level_2_w = level_2['w']
            if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
            else: level_2_h = level_2['h']
            level_2['x'] = level_1['x'] + level_2_x_cur
            level_2['y'] = level_1['y']
            level_2_x_cur += level_2_w
            if level_2_h_max < level_2_h: level_2_h_max = level_2_h
            ###
            surface = font_label.render(level_2['val'], True, COLOR_LABEL)
            screen.blit(surface, (level_2['x'], level_2['y']))
        level_1_y_cur += level_2_h_max

def layout_components_row_col(parent):
    level_1_x_cur = 0
    for level_1 in parent['children']:
        level_1['x'] = parent['x'] + level_1_x_cur
        level_1['y'] = parent['y']
        level_2_y_cur = 0
        level_2_w_max = 0
        for level_2 in level_1['children']:
            if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
            else: level_2_w = level_2['w']
            if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
            else: level_2_h = level_2['h']
            level_2['x'] = level_1['x']
            level_2['y'] = level_1['y'] + level_2_y_cur
            level_2_y_cur += level_2_h
            if level_2_w_max < level_2_w: level_2_w_max = level_2_w
            ###
            surface = font_label.render(level_2['val'], True, COLOR_LABEL)
            screen.blit(surface, (level_2['x'], level_2['y']))
        level_1_x_cur += level_2_w_max

def layout_ui_backup(root):
    level_1_x_cur = 0
    level_1_y_cur = 0
    row_gap = 0
    for level_1 in root['children']:
        if level_1['direction'] == 'col':
            level_1['x'] = root['x'] + level_1_x_cur
            level_1['y'] = root['y']
            level_2_y_cur = 0
            level_2_w_max = 0
            for level_2 in level_1['children']:
                if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
                else: level_2_w = level_2['w']
                if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
                else: level_2_h = level_2['h']
                level_2['x'] = level_1['x']
                level_2['y'] = level_1['y'] + level_2_y_cur
                level_2_y_cur += level_2_h
                if level_2_w_max < level_2_w: level_2_w_max = level_2_w
            level_1_x_cur += level_2_w_max
        ###
        elif level_1['direction'] == 'row':
            level_1['x'] = root['x']
            level_1['y'] = root['y'] + level_1_y_cur
            level_2_x_cur = 0
            level_2_h_max = 0
            for level_2 in level_1['children']:
                if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
                else: level_2_w = level_2['w']
                if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
                else: level_2_h = level_2['h']
                level_2['x'] = level_1['x'] + level_2_x_cur
                level_2['y'] = level_1['y']
                level_2_x_cur += level_2_w
                if level_2_h_max < level_2_h: level_2_h_max = level_2_h
            level_1_y_cur += level_2_h_max


def component_create(_type, direction='col', val='', x=0, y=0, w=0, h=0, children=[]):
    component = {
        'type': _type,
        'direction': direction,
        'val': val,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': 0,
        'children': children,
    }
    return component

'''
label_0001 = component_create('label', val='LABEL 1', w=100)
entry_0001 = component_create('entry', w=100, h=30)
label_0002 = component_create('label', val='LABEL 2', w=100)
entry_0002 = component_create('entry', w=100, h=30)
frame_0001 = component_create('frame', direction='row', children=[label_0001, entry_0001])
frame_0002 = component_create('frame', direction='row', children=[label_0002, entry_0002])
root = component_create('frame', direction='col', x=300, y=300, children=[frame_0001, frame_0002])
'''

label_w_min = 200
entry_w_min = 300

root_direction = 'col'
level_1_direction = 'row'

root = component_create('frame', direction=root_direction, x=300, y=200, 
    children=[
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Client Name', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Facility Name', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Contact Person', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Email', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Phone', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Location', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Industry', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        ###
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Average Flow Rate', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Maximum Flow Rate', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Unit (m3/h or L/min)', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        ###
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Contaminant Name', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Contaminant Current', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Contaminant Target', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        ###
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Available Power', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Available Space', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Existing Pumps', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Oxygen Supply', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Ventilation', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        ###
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Budget', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Deadline', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Regulatory Constraints', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
        component_create('frame', direction=level_1_direction, 
            children=[
                component_create('label', val='Safety Constraints', w=label_w_min),
                component_create('entry', w=entry_w_min, h=30),
            ]
        ),
    ]
)

scroll_offset = root['y']

def layout_col(root, level_1, level_1_x_cur):
    level_1['x'] = root['x'] + level_1_x_cur
    level_1['y'] = root['y']
    level_2_y_cur = 0
    level_2_w_max = 0
    for level_2 in level_1['children']:
        if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
        else: level_2_w = level_2['w']
        if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
        else: level_2_h = level_2['h']
        level_2['x'] = level_1['x']
        level_2['y'] = level_1['y'] + level_2_y_cur
        level_2_y_cur += level_2_h
        if level_2_w_max < level_2_w: level_2_w_max = level_2_w
    level_1_x_cur += level_2_w_max
    return level_1_x_cur

def layout_row(root, level_1, level_1_y_cur):
    level_1['x'] = root['x']
    level_1['y'] = root['y'] + level_1_y_cur
    level_2_x_cur = 0
    level_2_h_max = 0
    for level_2 in level_1['children']:
        if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
        else: level_2_w = level_2['w']
        if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
        else: level_2_h = level_2['h']
        level_2['x'] = level_1['x'] + level_2_x_cur
        level_2['y'] = level_1['y']
        level_2_x_cur += level_2_w
        if level_2_h_max < level_2_h: level_2_h_max = level_2_h
    level_1_y_cur += level_2_h_max
    return level_1_y_cur

def layout_ui(root):
    level_1_x_cur = 0
    level_1_y_cur = 0
    row_gap = 0
    for level_1 in root['children']:
        if level_1['direction'] == 'col':
            level_1_x_cur = layout_col(root, level_1, level_1_x_cur)
        ###
        elif level_1['direction'] == 'row':
            level_1_y_cur = layout_row(root, level_1, level_1_y_cur)

def draw_ui(root):
    for level_1 in root['children']:
        for level_2 in level_1['children']:
            if level_2['type'] == 'label': 
                surface = font_label.render(level_2['val'], True, COLOR_LABEL)
                screen.blit(surface, (level_2['x'], level_2['y']))
            elif level_2['type'] == 'entry':
                if level_2['focus'] == True:
                    pygame.draw.rect(screen, COLOR_BORDER_BLUE, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                else:
                    pygame.draw.rect(screen, COLOR_BORDER_GRAY, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                surface = font_entry.render(level_2['val'], True, COLOR_ENTRY)
                screen.blit(surface, (level_2['x'] + (level_2['h'] // 4), level_2['y'] + (level_2['h'] // 4)))

def draw_label(level_2):
    surface = font_label.render(level_2['val'], True, COLOR_LABEL)
    screen.blit(surface, (level_2['x'], level_2['y']))

def draw_entry(level_2):
    if level_2['focus'] == True:
        pygame.draw.rect(screen, COLOR_BORDER_BLUE, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
    else:
        pygame.draw.rect(screen, COLOR_BORDER_GRAY, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
    surface = font_entry.render(level_2['val'], True, COLOR_ENTRY)
    screen.blit(surface, (level_2['x'] + (level_2['h'] // 4), level_2['y'] + (level_2['h'] // 4)))

def layout_components_auto_backup(root):
    level_1_x_cur = 0
    level_1_y_cur = 0
    row_gap = 0
    for level_1 in root['children']:
        if level_1['direction'] == 'col':
            level_1['x'] = root['x'] + level_1_x_cur
            level_1['y'] = root['y']
            level_2_y_cur = 0
            level_2_w_max = 0
            for level_2 in level_1['children']:
                if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
                else: level_2_w = level_2['w']
                if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
                else: level_2_h = level_2['h']
                level_2['x'] = level_1['x']
                level_2['y'] = level_1['y'] + level_2_y_cur
                level_2_y_cur += level_2_h
                if level_2_w_max < level_2_w: level_2_w_max = level_2_w
                ###
                if level_2['type'] == 'label': 
                    surface = font_label.render(level_2['val'], True, COLOR_LABEL)
                    screen.blit(surface, (level_2['x'], level_2['y']))
                elif level_2['type'] == 'entry':
                    if level_2['focus'] == True:
                        pygame.draw.rect(screen, COLOR_BORDER_BLUE, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                    else:
                        pygame.draw.rect(screen, COLOR_BORDER_GRAY, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                    surface = font_entry.render(level_2['val'], True, COLOR_ENTRY)
                    screen.blit(surface, (level_2['x'] + (level_2['h'] // 4), level_2['y'] + (level_2['h'] // 4)))
            level_1_x_cur += level_2_w_max

        elif level_1['direction'] == 'row':
            level_1['x'] = root['x']
            level_1['y'] = root['y'] + level_1_y_cur + row_gap
            level_2_x_cur = 0
            level_2_h_max = 0
            row_gap += 16
            for level_2 in level_1['children']:
                if level_2['w'] == 0: level_2_w = font_label.size(level_2['val'])[0]
                else: level_2_w = level_2['w']
                if level_2['h'] == 0: level_2_h = font_label.size(level_2['val'])[1]
                else: level_2_h = level_2['h']
                level_2['x'] = level_1['x'] + level_2_x_cur
                level_2['y'] = level_1['y']
                level_2_x_cur += level_2_w
                if level_2_h_max < level_2_h: level_2_h_max = level_2_h
                ###
                if level_2['type'] == 'label': 
                    surface = font_label.render(level_2['val'], True, COLOR_LABEL)
                    screen.blit(surface, (level_2['x'], level_2['y']))
                elif level_2['type'] == 'entry':
                    if level_2['focus'] == True:
                        pygame.draw.rect(screen, COLOR_BORDER_BLUE, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                    else:
                        pygame.draw.rect(screen, COLOR_BORDER_GRAY, (level_2['x'], level_2['y'], level_2['w'], level_2['h']), 1)
                    surface = font_entry.render(level_2['val'], True, COLOR_ENTRY)
                    screen.blit(surface, (level_2['x'] + (level_2['h'] // 4), level_2['y'] + (level_2['h'] // 4)))
            level_1_y_cur += level_2_h_max

def draw_components(parent):
    pass

def draw_ui_col(root, row_1_h=0):
    child_y_cur = 0
    ###
    parent = root
    for i, child in enumerate(parent['children']):
        child_w, child_h = font_label.size(child['val'])
        child['x'] = parent['x']
        child['y'] = parent['y'] + child_y_cur
        child_y_cur += child_h
        if child['type'] == 'label': 
            ###
            surface = font_label.render(child['val'], True, COLOR_LABEL)
            screen.blit(surface, (child['x'], child['y']))
        elif child['type'] == 'entry':
            ###
            pygame.draw.rect(screen, COLOR_BORDER_GRAY, (child['x'], child['y'], child['w'], child['h']), 1)
            surface = font_entry.render(child['val'], True, COLOR_ENTRY)
            screen.blit(surface, (child['x'] + (child['h'] // 4), child['y'] + (child['h'] // 4)))

def draw_ui_row(root):
    child_x_cur = 0
    ###
    parent = root
    for i, child in enumerate(parent['children']):
        child_w, child_h = font_label.size(child['val'])
        child['x'] = parent['x'] + child_x_cur
        child['y'] = parent['y']
        child_x_cur += child_w
        if child['type'] == 'label': 
            ###
            surface = font_label.render(child['val'], True, COLOR_LABEL)
            screen.blit(surface, (child['x'], child['y']))
        elif child['type'] == 'entry':
            ###
            pygame.draw.rect(screen, COLOR_BORDER_GRAY, (child['x'], child['y'], child['w'], child['h']), 1)
            surface = font_entry.render(child['val'], True, COLOR_ENTRY)
            screen.blit(surface, (child['x'] + (child['h'] // 4), child['y'] + (child['h'] // 4)))
    return child['h']

def calc_layout(parent, direction='row'):
    child_x_cur = 0
    child_y_cur = 0
    ###
    for i, child in enumerate(parent['children']):
        if direction == 'row':
            child['x'] = parent['x'] + child_x_cur
            child['y'] = parent['y']
            child_x_cur += child['w']
            ###
            parent['w'] = child_x_cur
            if parent['h'] < child['h']: parent['h'] = child['h']
        else:
            child['x'] = parent['x']
            child['y'] = parent['y'] + child_y_cur
            child_y_cur += child['h']
            ###
            if parent['w'] < child['w']: parent['w'] = child['w']
            parent['h'] = child_y_cur
    ###
    print(parent)
    return parent
    
def draw_frame(component):
    parent = component
    child_y_cur = 0
    child_w_max = 0
    for i, child in enumerate(parent['children']):
        if child['type'] == '': pass
        elif child['type'] == 'label': 
            parent_y = parent['y'] + scroll_offset
            padding = 16;
            child['w'], child['h'] = font_label.size(child['val'])
            if child_w_max < child['w']: child_w_max = child['w']
            child['x'] = parent['x'] + padding
            child['y'] = parent_y + padding + child_y_cur
            parent['w'] = child_w_max + (padding * 2)
            parent['h'] = child['h'] + (padding * 2) + child_y_cur
            child_y_cur += child['h']
            ###
            surface = font_label.render(child['val'], True, COLOR_LABEL)
            screen.blit(surface, (child['x'], child['y']))
        elif child['type'] == 'entry':
            pass
    pygame.draw.rect(screen, COLOR_BORDER_GRAY, (parent['x'], parent_y, parent['w'], parent['h']), 1)

def draw_components():
    for i, component in enumerate(components):
        if component['type'] == '': pass
        elif component['type'] == 'frame': draw_frame(component)
        # elif component['type'] == 'entry': draw_entry(component)
        # elif component['type'] == 'label': draw_label(component)

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

def compute_size(node):
    if not node['children']:
        return node['width'], node['height']

    widths = []
    heights = []

    for child in node['children']:
        w, h = compute_size(child)
        widths.append(w)
        heights.append(h)

    node['width'] = sum(widths)
    node['height'] = max(heights)

    return node['width'], node['height']

def layout(node, x, y):
    node['x'] = x
    node['y'] = y

    current_x = x

    for child in node['children']:
        layout(child, current_x, y)
        current_x += child['width']

def print_tree(node):
    # print('w', node['width'])
    # print('h', node['height'])
    # print('x', node['x'])
    # print('y', node['y'])
    print(node)
    print()

    for child in node['children']:
        print_tree(child)

def print_tree(node, indent=0):
    print(" " * indent + f"{node['type']} ({node['x']},{node['y']}) {node['width']}x{node['height']}")
    for child in node["children"]:
        print_tree(child, indent + 4)

def node(node_type, children=None, direction=None, val=''):
    return {
        "type": node_type,
        "children": children or [],
        "direction": direction,

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
        return 60, 20
    if node['type'] == 'input':
        return 120, 30
    return 0, 0

root = node("frame", [

    node("frame", [
        node("label", val='label 1'),
        node("label", val='label 2'),
    ], direction='row'),

    node("frame", [
        node("label", val='label 3'),
        node("label", val='label 4')
    ], direction='column')

], direction="column")

def compute_container_size(node):
    children = node["children"]

    if node["direction"] == "row":
        total_width = 0
        max_height = 0

        for child in children:
            total_width += child["width"]
            max_height = max(max_height, child["height"])

        node["width"] = total_width
        node["height"] = max_height


    elif node["direction"] == "column":
        max_width = 0
        total_height = 0

        for child in children:
            max_width = max(max_width, child["width"])
            total_height += child["height"]

        node["width"] = max_width
        node["height"] = total_height

def compute_size(node):

    # CASE 1 — leaf node
    if len(node["children"]) == 0:

        w, h = intrinsic_size(node)
        node["width"] = w
        node["height"] = h
        return


    # CASE 2 — container node

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


    # ROW LAYOUT
    if node["direction"] == "row":

        current_x = x

        for child in node["children"]:

            compute_position(child, current_x, y)

            current_x += child["width"]


    # COLUMN LAYOUT
    elif node["direction"] == "column":

        current_y = y

        for child in node["children"]:

            compute_position(child, x, current_y)

            current_y += child["height"]

compute_size(root)
compute_position(root, 0, 0)

def layout(node, start_x=0, start_y=0):
    compute_size(node)
    compute_position(node, start_x, start_y)

print_tree(root, indent=0)
# print(json.dumps(root, indent=4))
# quit()


def draw_recursive(node):
    if node['type'] == 'label': 
        surface = font_label.render(node['val'], True, COLOR_LABEL)
        screen.blit(surface, (node['x'], node['y']))
    elif node['type'] == 'entry':
        if node['focus'] == True:
            pygame.draw.rect(screen, COLOR_BORDER_BLUE, (node['x'], node['y'], node['w'], node['h']), 1)
        else:
            pygame.draw.rect(screen, COLOR_BORDER_GRAY, (node['x'], node['y'], node['w'], node['h']), 1)
        surface = font_entry.render(node['val'], True, COLOR_ENTRY)
        screen.blit(surface, (node['x'] + (node['h'] // 4), node['y'] + (node['h'] // 4)))

    for child in node['children']:
        draw_recursive(child)

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
                # fields[field_i_cur]['val'] += event.unicode
                for a in root['children']:
                    if 'children' in a:
                        for b in a['children']:
                            if b['focus'] == True:
                                b['val'] += event.unicode
                    ###
                    if b['focus'] == True:
                        b['val'] += event.unicode

        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset += event.y * 30
            root['y'] = scroll_offset
            # clear focus because wrong coords
            for a in root['children']:
                if 'children' in a:
                    for b in a['children']:
                        b['focus'] = False
                ###
                a['focus'] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for a in root['children']:
                if 'children' in a:
                    for b in a['children']:
                        if (mouse_x > b['x'] and 
                            mouse_x < b['x'] + b['w'] and
                            mouse_y > b['y'] and
                            mouse_y < b['y'] + b['h']
                        ):
                            b['focus'] = True
                        else:
                            b['focus'] = False
                ###
                if (mouse_x > a['x'] and 
                    mouse_x < a['x'] + a['w'] and
                    mouse_y > a['y'] and
                    mouse_y < a['y'] + a['h']
                ):
                    a['focus'] = True
                else:
                    a['focus'] = False



    screen.fill(COLOR_BACKGROUND)

    # draw_fields()
    # draw_components()
    # row_1_h = draw_ui_row(row_1)
    # row_2_h = draw_ui_row(row_2)
    # row_3_h = draw_ui_row(row_3)
    # draw_ui_col(col_2, row_1_h)
    # draw_ui(row_1, direction='row')
    # draw_ui(row_1, direction='col')

    # layout_components_col_row(root)
    # layout_components_row_col(root)
    # draw_components(root)
    # layout_ui(root)
    # draw_ui(root)
    
    # compute_size(root)
    # layout(root, 0, 0)
    layout(root, start_x=100, start_y=100)
    draw_recursive(root)
    # print_tree(root)
    # print(root)
    # draw_ui(root)
    # quit()

    mouse_pos = font.render(f'{mouse_x} - {mouse_y}', True, (255, 0, 255))
    screen.blit(mouse_pos, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
