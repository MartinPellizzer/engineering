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

atomic structure
---
periodic table

proton   (p) +1 -> +1.602 * 10^-19 C (coulombs)
electron (e) -1 -> -1.602 * 10^-19 C (coulombs)

p/n ~ 1amu

itotopes
atomic number (number of protons in nucleus)
mass number: number of protons + electrons
charge: imbalance of electrons and protons

example: Oxygen
atomic number: 8
mass number: 16 (most common isotope)
charge: 2- (more electrons than protons, total 10 electrons)

a neutral atom is called: atom
a charged atom: ions
positively charged ions: cations
negatively charged ions: anions

atomic weight (different from mass number, even if close)
mass number: get from isotope
atomic weight: get from average of possible isotopes of that atom occuring in nature (weighted average)

periodic table
---
colums: groups
rows: periods

group 1: alkali metals
group 2: alkaline earth metals
group 7 (or 17): halogens
group 8 (or 18): noble gases

naming ionic compounds
---
1. ionic
metal with non metal
m/nm
ex. NaCl

2. molecular
nm/nm

3. acids
- binary
ex. HCl (aq) (if dissolved in water, otherwise molecular class)
- oxyacids
ex. H2SO4

Ionic compounds
- NaCl sodium chloride (Na cation, Cl anion) (metal first, non metal second plus -ide) (Na+1, Cl-1)
- CuCl copper(I) chloride (Cu+1, Cl-1) (cupros chloride)
- CuCl2 copper(II) chloride (Cu+2, Cl-1) (cupric chloride)
exceptions: Ag+1 Cd+2 Zn+2 Al+3 (always the case with these charges)
(- Fe(II) ferrous)
(- Fe(III) ferric)
- NH4Br (NH4 ammonium) (this is an edge case, is polyatomic ions classification, the polyatomic ions must be memorized)
    ammonium bromide
- CuSO4
    copper(II) solfate (II because solfate has -2 charge)
- MgCl2 (since Cl has -1 charge, and Mg has +2 charge, you need 2 Cl to balance 1 Mg)

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
print('atomic weigth:', calc.atomic_weight(35, 75, 37, 25))


