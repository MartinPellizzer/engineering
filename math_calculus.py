'''

CALCULUS

'''

def calc_slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    res = None
    if x1 != x2:
        res = (y2 - y1) / (x2 - x1)
    return res

print("Slope:", calc_slope((1, 1), (2, 2)))
