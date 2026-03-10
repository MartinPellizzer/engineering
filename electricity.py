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
