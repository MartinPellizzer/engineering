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

################################################################################
# UNITS AND CONVERSIONS
################################################################################

def g_to_tg(val):
    res = val / 1000 / 1000 / 1000 / 1000
    return res

def g_to_gg(val):
    res = val / 1000 / 1000 / 1000
    return res

def g_to_Mg(val):
    res = val / 1000 / 1000
    return res

def g_to_kg(val):
    res = val / 1000
    return res

def g_to_mg(val):
    res = val * 1000
    return res

# CANONICAL
def in_to_cm(val):
    res = val * 2.54
    return res

def m_to_ft(val):
    res = val * 100 / 2.54 / 12
    return res

# TEMPERATURE
# ---

def celsius_to_kelvin(val):
    res = val + 273
    return res

def kelvin_to_celsius(val):
    res = val - 273
    return res

def density(m, V):
    # letter ro (look like a "p") is the ufficial symbol for density
    res = m / V
    return res

def mass(d, V):
    res = d * V
    return res

################################################################################
# CHEMISTY
################################################################################

def atomic_weight(mass_num_1, perc_1, mass_num_2, perc_2):
    res = ((mass_num_1 * perc_1) + (mass_num_2 * perc_2)) / 100
    return res

