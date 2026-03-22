'''

DISTANCE
1ft = 12in
3ft = 1yd
1in = 2.54cm
1km = 1000m
im = 100cm
1mi = 1.609km
1mi = 528oft

MASS/WEIGT
1kg = 1000g
1kg = 2.2lbs
1lb = 16oz
1tom = 2000lbs
1metric ton = 1000kg
1metric ton = 2204lbs

VOLUME/CAPACITY
1l = 1000ml
1ml = 1cm^3
1m^3 = 1000l
1gal = 3.785l
1gal = 4qts
1qt = 2pints

TIME
1hr = 60min
1min = 60s
1day = 24hrs
365days = 1year
30days = 1month
1century = 100yrs
1millenium = 1000yrs
1leap yr = 366days
1year(avg) = 365.25days

METRIC SYSTEM
T = 10^12
G = 10^9
M = 10^6
K = 10^3
h = 10^2
da = 10^1
d = 10^-1
c = 10^-2
m = 10^-3
u = 10^-6
n = 10^-9
p = 10^-12

DENSITY
d = m/v
ex. 50g / 8.5ml = 5.88 g/ml

INTENSIVE / EXTENSIVE PROPERTIES
INTENSIVE
- boiling point
- melting point
- specific heat capacity
- density (m/v)
- condictivity
- temperature
- (chemical properties)
- (some physical properties)
EXTENSIVE
- moles
- mass
- weight 
- length
- area
- volume
- heat capacity
- internal energy
- dh/ds/dg

TYPES OF MATTER
matter
    - pure substances
        - elements (02, He, N2)
        - compounds (H2O, NaCl, C2H5OH, CO2)
    - mixtures
        - homogeneous (NaCl + H20)
        - heterogeneous (Oil + Water)

SOLIDS / LIQUIDS / GASES

PHYSICAL / CHEMICAL PROPERTIES
PHYSICAL
boiling point
melting point
ductility
malleability
color
viscosity
density
mass, weight
CHEMICAL
flammability
corrosive
combustible
explosive
color channging
pH
taste


'''

########################################
# DISTANCE
########################################

import math

def num_to_scientific_notation(number, decimals=3):
    if number == 0: return "0 × 10^0"
    exponent = int(math.floor(math.log10(abs(number))))
    mantissa = number / (10 ** exponent)
    mantissa_str = f"{mantissa:.{decimals}f}"
    return f"{mantissa_str} × 10^{exponent}"

def ft_to_in(val):
    res = val * 12
    return res
    
def ft_to_yd(val):
    res = val * (1/3)
    return res
    
def in_to_cm(val):
    res = val * 2.54
    return res
    
def km_to_m(val):
    res = val * 1000
    return res
    
def m_to_cm(val):
    res = val * 100
    return res
    
def mi_to_km(val):
    res = val * 1.609
    return res
    
def mi_to_ft(val):
    res = val * 5280
    return res
    
def kilo_to_base(val):
    res = val * 1000
    return res

def base_to_kilo(val):
    res = val / 1000
    return res

print('ft_to_in: 1 ft =', ft_to_in(1), 'in')
print('ft_to_yd: 3 ft =', ft_to_yd(3), 'yd')
print('in_to_cm: 1 in =', in_to_cm(1), 'cm')
print('km_to_m: 1 km =', km_to_m(1), 'm')
print('m_to_cm: 1 m =', m_to_cm(1), 'cm')
print('mi_to_km: 1 mi =', mi_to_km(1), 'km')
print('mi_to_ft: 1 mi =', mi_to_ft(1), 'ft')
print('ft_to_in: 1 ft =', ft_to_in(4), 'in')

print('kilo_to_base: 1 k =', kilo_to_base(1), 'base')
print('base_to_kilo: 1 base =', base_to_kilo(1), 'kilo')
print(f'num_to_scientific_notation: {base_to_kilo(1)} =', num_to_scientific_notation(base_to_kilo(1)))
print(f'num_to_scientific_notation: 9300000000 =', num_to_scientific_notation(9300000000))
print(f'num_to_scientific_notation: 0.00076 =', num_to_scientific_notation(0.00076))
