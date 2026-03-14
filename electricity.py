'''

electron orbits
---
number of electrons per shell: 2N^2
N: number of the orbit (shell)

valence electrons
---
electrons in outer shell
cannot be more than 8
when electron escape an atom -> become free electron
this is called ionization, and positive atoms called positive ion
if atom aquire electron, negative charge and called negative ion

========================================
QUANTITIES
========================================

coulomb (C)
---
electron qe: charge 1.6 * 10^-19 C
1 C = 6.25 * 10^18 (6,250,000,000,000,000,000)

ampere (A)
---
1 ampere = 1 coulomb * second
(I = q/t)

volt (V, or E)
---

ohm (R)
---

watt (W)
---
P = E * I

horse power (hp)
---
1 hp = 746 W

>> check conversions at page 67

ohm's law
---

>> check complete chart formulas
>> check SI table

========================================
MAGNETISM
========================================

english system
---

flux: phi
flux density: magnetic strength (lines per square inch) (B)

flux density = flux lines / area
B = phi / A

total force of magnetic field: magnetomotive force (mmf)
mmf = phi * rel (reluctance)
pull (in pounds) = (B * A) / 72000000

CGS system
---

centimeter-gram-second
1 line = 1 maxwell
1 maxwell / square centimeter = 1 gauss
1 gauss = 6.4516 lines of flux / square inch

in SI system, magnetomotive forced measured in ampere-turns
in CGS, gilberts measure the same

1 gilbert = 1.256 ampere-turns
1 ampere-turn = 0.7905 gilbert

>> check others / and final table

========================================
RESISTORS
========================================

conductors have low resistance
ex. 16 AWG solid copper has 5 ohms per 1000 feet

used for voltage divider

fixed resistors
- composition carbon resistor
- metal film resistor
- carbon film resistor
- metal glaze resistor
- wire-wound resistor

color codes

power ratings

variable resistors

'''

def atom_shell_electron_number_max_get(N):
    res = 2 * (N ** 2)
    return res

def calc_power_va(volt, ampere):
    res = volt * ampere
    return res

def calc_power_ir(ampere, resistance):
    res = (ampere ** 2) * ampere
    return res

def calc_power_vr(volt, resistance):
    res = (volt ** 2) / resistance
    return res

def calc_ohm_e(i, r):
    res = i * r
    return res

def calc_ohm_i(e, r):
    res = e / r
    return res

def calc_ohm_r(e, i):
    res = e / i
    return res

print('SHELL 1 ELECRON NUMBER:', atom_shell_electron_number_max_get(1))
print('SHELL 2 ELECRON NUMBER:', atom_shell_electron_number_max_get(2))
print('SHELL 3 ELECRON NUMBER:', atom_shell_electron_number_max_get(3))
print('SHELL 4 ELECRON NUMBER:', atom_shell_electron_number_max_get(4))
print('SHELL 5 ELECRON NUMBER:', atom_shell_electron_number_max_get(5))

print('POWER VA (W):', calc_power_va(volt=5, ampere=3))
print('POWER IR (W):', calc_power_ir(ampere=5, resistance=3))
print('POWER VR (W):', calc_power_vr(volt=5, resistance=3))
print('OHM E:', calc_ohm_e(i=5, r=5))
print('OHM I:', calc_ohm_i(e=5, r=5))
print('OHM R:', calc_ohm_r(e=5, i=5))
print('POWER VA (W):', calc_power_va(volt=120, ampere=8))

print('OHM I:', calc_ohm_i(e=15, r=30), 'A')
print('POWER VR (W):', calc_power_vr(volt=10, resistance=100), 'W')
