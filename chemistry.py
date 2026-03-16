'''

CHEMISTY - (THEORY)

matter
solid - liquid - gas

~ 118 types of atoms (elements)

solid: definite shape, definite volume
liquid: no definite shape, definite volume
gas: no definite shape, no definite volume

substance
---
element: 1 atom (Na)
compound: multiple elements (NaCl)

some element comes in 2 in nature (N2, O2, F2, Cl2, Br2, I2, H2) - (7 in total) - (diatomic)
but when found in compounds, can be found in 1 

pure substance vs mixture
homogeneous vs heterogeneous
chemical property/change vs physical property/change
intensive property vs extensive property

scientific notation
---
significant figures
accuracy vs precision

units and conversions
---
SI Units

length:         m
mass:           kg (g)
time:           s
temperature:    K
volume:         m3 (L)
energy/work:    J
pressure:       Pa (atm)

density

'''

from lib import calc

print(calc.calc_scientific_notation(472000))
print('g_to_tg:', calc.g_to_tg(75), 'tg')
print('g_to_gg:', calc.g_to_gg(75), 'gg')
print('g_to_Mg:', calc.g_to_Mg(75), 'Mg')
print('g_to_kg:', calc.g_to_kg(75), 'kg')
print('g_to_mg:', calc.g_to_mg(75), 'mg')
print('in_to_cm:', calc.in_to_cm(1), 'cm')
print('m_to_ft:', calc.m_to_ft(17.1), 'ft')
print('celsius_to_kelvin:', calc.celsius_to_kelvin(10), 'K')
print('kelvin_to_celsius:', calc.kelvin_to_celsius(10), 'C')
print('density:', calc.density(12, 8), 'g/cm3')
print('mass:', calc.mass(1.5, 27), 'g')


