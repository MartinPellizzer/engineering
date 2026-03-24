def element_create(
    number, symbol, name, atomic_mass, col_i, row_i, x=0, y=0, w=64, h=64, focus=False,
    extra=[], bg_color=None, 
):
    element = {
        'number': number,
        'symbol': symbol,
        'name': name,
        'atomic_mass': atomic_mass,
        'group': col_i+1,
        'col_i': col_i,
        'row_i': row_i,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'focus': focus,
        'extra': extra,
        'bg_color': bg_color,
    }
    return element

element_hydrogen =  element_create('1', 'H', 'hydrogen', 1.0078, 0, 0)
element_helium =    element_create('2', 'He', 'helium', 4.0026, 17, 0)
###
element_lithium =   element_create('3', 'Li', 'lithium', 6.9410, 0, 1, extra=['+1 or 1+', 'alkali metal'])
element_berylium =  element_create('4', 'Be', 'berylium', 9.0122, 1, 1, extra=['+2 or 2+', 'alkali earth metal'])
element_boron =     element_create('5', 'B', 'boron', 10.811, 12, 1, bg_color=(128, 128, 128), extra=['+3 or 3+'])
element_carbon =    element_create('6', 'C', 'carbon', 12.011, 13, 1)
element_nitrogen =  element_create('7', 'N', 'nitrogen', 14.007, 14, 1, extra=['-3 or 3-'])
element_oxygen =    element_create('8', 'O', 'oxygen', 15.999, 15, 1, extra=['-2 or 2-'])
element_fluorine =  element_create('9', 'F', 'fluorine', 18.998, 16, 1, extra=['-1 or 1-'])
element_neon =      element_create('10', 'Ne', 'neon', 20.180, 17, 1)
'''
###
element_sodium = element_create('11', 'Na', 'sodium', 0, 2, extra=['+1 or 1+', 'alkali metal'])
element_manganesium = element_create('12', 'Mg', 'manganesium', 1, 2, extra=['+2 or 2+', 'alkali earth metal'])
element_aluminium = element_create('13', 'Al', 'aluminium', 12, 2, extra=['+3 or 3+'])
element_silicon = element_create('14', 'Si', 'silicon', 13, 2, bg_color=(128, 128, 128))
element_phosphorus = element_create('15', 'P', 'phosphorus', 14, 2, extra=['-3 or 3-'])
element_sulfur = element_create('16', 'S', 'sulfur', 15, 2, extra=['-2 or 2-'])
element_chlorine = element_create('17', 'Cl', 'chlorine', 16, 2, extra=['-1 or 1-'])
element_argon = element_create('18', 'Ar', 'argon', 17, 2)
###
element_potassium = element_create('19', 'K', 'potassium', 0, 3, extra=['+1 or 1+', 'alkali metal'])
element_calcium = element_create('20', 'Ca', 'calcium', 1, 3, extra=['+2 or 2+', 'alkali earth metal'])
element_scandium = element_create('21', 'Sc', 'scandium', 2, 3)
element_titanium = element_create('22', 'Ti', 'titanium', 3, 3)
element_vanadium = element_create('23', 'V', 'vanadium', 4, 3)
element_chromium = element_create('24', 'Cr', 'chromium', 5, 3)
element_manganese = element_create('25', 'Mn', 'manganese', 6, 3)
element_iron = element_create('26', 'Fe', 'iron', 7, 3)
element_cobalt = element_create('27', 'Co', 'cobalt', 8, 3)
element_nickel = element_create('28', 'Ni', 'nickel', 9, 3)
element_copper = element_create('29', 'Cu', 'copper', 10, 3)
element_zinc = element_create('30', 'Zn', 'zinc', 11, 3)
element_gallium = element_create('31', 'Ga', 'gallium', 12, 3, extra=['+3 or 3+'])
element_germanium = element_create('32', 'Ge', 'germanium', 13, 3)
element_arsenic = element_create('33', 'As', 'arsenic', 14, 3, bg_color=(128, 128, 128), extra=['-3 or 3-'])
element_selenium = element_create('34', 'Se', 'selenium', 15, 3, extra=['-2 or 2-'])
element_bromine = element_create('35', 'Br', 'bromine', 16, 3, extra=['-1 or 1-'])
element_krypton = element_create('36', 'Kr', 'krypton', 17, 3)
###
element_rubidium = element_create('37', 'Rb', 'rubidium', 0, 4, extra=['+1 or 1+', 'alkali metal'])
element_strontium = element_create('38', 'Sr', 'strontium', 1, 4, extra=['+2 or 2+', 'alkali earth metal'])
element_yttrium = element_create('39', 'Y', 'yttrium', 2, 4)
element_zirconium = element_create('40', 'Zr', 'zirconium', 3, 4)
element_niobium = element_create('41', 'Nb', 'niobium', 4, 4)
element_molybdenum = element_create('42', 'Mo', 'molybdenum', 5, 4)
element_technetium = element_create('43', 'Tc', 'technetium', 6, 4)
element_ruthenium = element_create('44', 'Ru', 'ruthenium', 7, 4)
element_rhodium = element_create('45', 'Rh', 'rhodium', 8, 4)
element_palladium = element_create('46', 'Pd', 'palladium', 9, 4)
element_silver = element_create('47', 'Ag', 'silver', 10, 4)
element_cadmium = element_create('48', 'Cd', 'cadmium', 11, 4)
element_indium = element_create('49', 'In', 'indium', 12, 4, extra=['+3 or 3+'])
element_tin = element_create('50', 'Sn', 'tin', 13, 4)
element_antimony = element_create('51', 'Sb', 'antimony', 14, 4, extra=['-3 or 3-'])
element_tellurium = element_create('52', 'Te', 'tellurium', 15, 4, bg_color=(128, 128, 128), extra=['-2 or 2-'])
element_iodine = element_create('53', 'I', 'iodine', 16, 4, extra=['-1 or 1-'])
element_xenon = element_create('54', 'Xe', 'xenon', 17, 4)
###
element_caesium = element_create('55', 'Ca', 'caesium', 0, 5, extra=['+1 or 1+', 'alkali metal'])
element_barium = element_create('56', 'Ba', 'barium', 1, 5, extra=['+2 or 2+', 'alkali earth metal'])
element_lantharum = element_create('57', 'La', 'lantharum', 2, 5)
element_hafnium = element_create('72', 'Hf', 'hafnium', 3, 5)
element_tantalum = element_create('73', 'Ta', 'tantalum', 4, 5)
element_tungsten = element_create('74', 'W', 'tungsten', 5, 5)
element_rhenium = element_create('75', 'Re', 'rhenium', 6, 5)
element_osmium = element_create('76', 'Os', 'osmium', 7, 5)
element_iridium = element_create('77', 'Ir', 'iridium', 8, 5)
element_platinum = element_create('78', 'Pt', 'platinum', 9, 5)
element_aurum = element_create('79', 'Au', 'aurum', 10, 5)
element_mercury = element_create('80', 'Hg', 'mercury', 11, 5)
element_thallium = element_create('81', 'Tl', 'thallium', 12, 5, extra=['+3 or 3+'])
element_lead = element_create('82', 'Pb', 'lead', 13, 5)
element_bismuth = element_create('83', 'Bi', 'bismuth', 14, 5, extra=['-3 or 3-'])
element_pollonium = element_create('84', 'Po', 'pollonium', 15, 5, extra=['-2 or 2-'])
element_astatine = element_create('85', 'At', 'astatine', 16, 5, bg_color=(128, 128, 128), extra=['-1 or 1-'])
element_radon = element_create('86', 'Rn', 'radon', 17, 5)
###
element_francium = element_create('87', 'Fr', 'francium', 0, 6)
element_radium = element_create('88', 'Ra', 'radium', 1, 6)
element_actinium = element_create('89', 'Ac', 'actinium', 2, 6)
element_rutherfordium = element_create('104', 'Rf', 'rutherfordium', 3, 6)
element_dubnium = element_create('105', 'Db', 'dubnium', 4, 6)
element_seaborgium = element_create('106', 'Sg', 'seaborgium', 5, 6)
element_bohrium = element_create('107', 'Bh', 'bohrium', 6, 6)
element_hassium = element_create('108', 'Hs', 'hassium', 7, 6)
element_meitnerium = element_create('109', 'Mt', 'meitnerium', 8, 6)
element_darmstadium = element_create('110', 'Ds', 'darmstadium', 9, 6)
element_roentgenium = element_create('111', 'Rg', 'roentgenium', 10, 6)
element_copernicium = element_create('112', 'Cn', 'copernicium', 11, 6)
element_nihonium = element_create('113', 'Nh', 'nihonium', 12, 6)
element_flevorium = element_create('114', 'Fl', 'flevorium', 13, 6)
element_moscovium = element_create('115', 'Mc', 'moscovium', 14, 6)
element_livemorium = element_create('116', 'Lv', 'livemorium', 15, 6)
element_tennessine = element_create('117', 'Ts', 'tennessine', 16, 6)
element_oganesson = element_create('118', 'Og', 'oganesson', 17, 6)
###
element_cerium = element_create('58', 'Ce', 'cerium', 3, 8)
element_praseodymium = element_create('59', 'Pr', 'praseodymium', 4, 8)
element_neodymium = element_create('60', 'Nd', 'neodymium', 5, 8)
element_promethium = element_create('61', 'Pm', 'promethium', 6, 8)
element_samarium = element_create('62', 'Sm', 'samarium', 7, 8)
element_europium = element_create('63', 'Eu', 'europium', 8, 8)
element_gadolinium = element_create('64', 'Gd', 'gadolinium', 9, 8)
element_terbium = element_create('65', 'Tb', 'terbium', 10, 8)
element_dysprosium = element_create('66', 'Dy', 'dysprosium', 11, 8)
element_holmium = element_create('67', 'Ho', 'holmium', 12, 8)
element_erbium = element_create('68', 'Er', 'erbium', 13, 8)
element_thulium = element_create('69', 'Tm', 'thulium', 14, 8)
element_ytterbium = element_create('70', 'Yb', 'ytterbium', 15, 8)
element_lutetium = element_create('71', 'Lu', 'lutetium', 16, 8)
'''

elements = []

elements.append(element_hydrogen)
elements.append(element_helium)
elements.append(element_lithium)
elements.append(element_berylium)
elements.append(element_boron)
elements.append(element_carbon)
elements.append(element_nitrogen)
elements.append(element_oxygen)
elements.append(element_fluorine)
elements.append(element_neon)
###
'''
elements.append(element_sodium)
elements.append(element_manganesium)
elements.append(element_aluminium)
elements.append(element_silicon)
elements.append(element_phosphorus)
elements.append(element_sulfur)
elements.append(element_chlorine)
elements.append(element_argon)
###
elements.append(element_potassium)
elements.append(element_calcium)
elements.append(element_scandium)
elements.append(element_titanium)
elements.append(element_vanadium)
elements.append(element_chromium)
elements.append(element_manganese)
elements.append(element_iron)
elements.append(element_cobalt)
elements.append(element_nickel)
elements.append(element_copper)
elements.append(element_zinc)
elements.append(element_gallium)
elements.append(element_germanium)
elements.append(element_arsenic)
elements.append(element_selenium)
elements.append(element_bromine)
elements.append(element_krypton)
###
elements.append(element_rubidium)
elements.append(element_strontium)
elements.append(element_yttrium)
elements.append(element_zirconium)
elements.append(element_niobium)
elements.append(element_molybdenum)
elements.append(element_technetium)
elements.append(element_ruthenium)
elements.append(element_rhodium)
elements.append(element_palladium)
elements.append(element_silver)
elements.append(element_cadmium)
elements.append(element_indium)
elements.append(element_tin)
elements.append(element_antimony)
elements.append(element_tellurium)
elements.append(element_iodine)
elements.append(element_xenon)
###
elements.append(element_caesium)
elements.append(element_barium)
elements.append(element_lantharum)
elements.append(element_hafnium)
elements.append(element_tantalum)
elements.append(element_tungsten)
elements.append(element_rhenium)
elements.append(element_osmium)
elements.append(element_iridium)
elements.append(element_platinum)
elements.append(element_aurum)
elements.append(element_mercury)
elements.append(element_thallium)
elements.append(element_lead)
elements.append(element_bismuth)
elements.append(element_pollonium)
elements.append(element_astatine)
elements.append(element_radon)
###
elements.append(element_francium)
elements.append(element_radium)
elements.append(element_actinium)
elements.append(element_rutherfordium)
elements.append(element_dubnium)
elements.append(element_seaborgium)
elements.append(element_bohrium)
elements.append(element_hassium)
elements.append(element_meitnerium)
elements.append(element_darmstadium)
elements.append(element_roentgenium)
elements.append(element_copernicium)
elements.append(element_nihonium)
elements.append(element_flevorium)
elements.append(element_moscovium)
elements.append(element_livemorium)
elements.append(element_tennessine)
elements.append(element_oganesson)
###
elements.append(element_cerium)
elements.append(element_praseodymium)
elements.append(element_neodymium)
elements.append(element_promethium)
elements.append(element_samarium)
elements.append(element_europium)
elements.append(element_gadolinium)
elements.append(element_terbium)
elements.append(element_dysprosium)
elements.append(element_holmium)
elements.append(element_erbium)
elements.append(element_thulium)
elements.append(element_ytterbium)
elements.append(element_lutetium)
'''

value = {
"R" : 0.082057366,
# Molar gas constant, L⋅atm⋅K−1⋅mol.−1
"c" : 299792458,
# speed of light in vacuum, m/s
"F" : 96485.3321233,
# Faraday’s constant, C/mol.
"k" : 1.380649e-23,
# Boltzmann’s constant, J/K
"h" : 6.62607015e-34, # Planck’s constant, Js
"C" : 1.602176634e-19, # elementary charge, C
"N" : 6.02214076e23,
# Avogadro number, /mol.
"g" : 9.80665,
# acceleration due to gravity, m/s^2
"V" : 22.41396,
# Standard molar volume of ideal gas, L
"e": 9.109383e-31,
# mass of an electron, kg
"p": 1.6726219e-27,
# mass of a proton, kg
"n": 1.6749275e-27,
# mass of a neutron, kg
"ep" : 8.8541878e-12, # vacuum electric permittivity, F/m
"mp" : 1.2566371e-6, # vacuum magnetic permeability, N/A^2
"a" : 5.2917721e-11,
# Bohr radius, m
"A" : 1e-10,
# 1 Angstrom to m
"mu" : 1e-6,
# 1 micron to m
"nm" : 1e-9
# 1 nano meter to m
}
