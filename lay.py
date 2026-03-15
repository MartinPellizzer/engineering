
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



def print_tree(node, indent=0):
    print(" " * indent + f"{node['id']} ({node['x']},{node['y']}) {node['w']}x{node['h']}")
    for child in node["children"]:
        print_tree(child, indent + 4)

# layout_calc_size(root)
# layout_calc_pos(root)
# print_tree(root, indent=0)
# quit()

