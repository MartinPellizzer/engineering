import math

def calc_circle_area(r):
    res = 3.14 * r
    return res

def calc_scientific_notation(number, decimals=3):
    if number == 0: return "0 × 10^0"
    exponent = int(math.floor(math.log10(abs(number))))
    mantissa = number / (10 ** exponent)
    mantissa_str = f"{mantissa:.{decimals}f}"
    return f"{mantissa_str} × 10^{exponent}"


