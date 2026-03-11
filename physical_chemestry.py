'''

LEGEND:
n: amount
p: pressure
T: Temperature


How to Record Each Entry

Title / Date / Context
    Example: “Venturi Injection Efficiency – 2026-03-07 – Water 50 m³/h”

Objective / Problem Statement
    Why this calculation or note exists
    Example: “Determine kLa and required venturi size for target ozone residual.”

Theory / Principle
    Brief explanation of the underlying physics or chemistry
    Include diagrams or sketches

Data / Inputs
    Flow rates, concentration, temperature, pH, etc.

Calculations / Observations
    Step-by-step numeric calculations
    Include units, assumptions, and margin of error

Results / Conclusions
    Example: “Required ozone production: 320 g/h; transfer efficiency ~85%”

Lessons / Notes for Next Time
    What worked, what failed, tips for optimization
    Example: “High humidity reduced efficiency by 10% — add dryer or margin.”

References / Source Links
    Textbooks, manuals, articles, case studies


################################################################################
# PERFECT GAS
################################################################################

----------------------------------------
PRESSURE AND VOLUME
----------------------------------------
pressure (p): the force (F) applied divided by the area (A)
SI unit of pressure is pascal (Pa)
1 Pa = 1 Nm^-2 = 1 kg m^-1 s^-2
standard pressure (p0) defined as p0 = 1 bar = 10^5 Pa ~= 1 atm
pressure measured by a barometer
pressure of a gas in a container, measured by a pressure gauge (see more devices pag. 5)
volume of gas (V): SI unit m^3

----------------------------------------
TEMPERATURE
----------------------------------------
T = thermodynamic temperature
T = 0 (kelvin scale) (K; not gradi K)
until 2019, 273.16 K, now to more precisely known value of  the Boltzmann constant
celsius commonly used for temperatures, denoted 0 (theta) and expressed ind degree Celsius (gradi C)

T/K = 0/gradiC + 273.15

----------------------------------------
AMOUNT
----------------------------------------
n
number of entities of a sample
SI unit: mol
1 mol = 6.02214076x10^23
Avogadro's constant, NA
NA = 6.02214076x10^23 mol^-1
mass = m
molar mass = M

SI unit: molar mas is kg mol^-1 (common g mol^-1)

amount of subtance: n = m/M

----------------------------------------
INTENSIVE and EXTENSIVE PROPERTIES
----------------------------------------

----------------------------------------
EQUATIONS OF STATE
----------------------------------------
p = f(T, V, n)
if perfect gas: p = nRT/V ... (R is a constant depending on the gas)

----------------------------------------
THE EMPIRICAL BASIS OF THE PERFECT GAS
----------------------------------------

Boyle's law:            pV = constant, at constant n,T
Charles's law:           V = constant * T, at constant n,p
                        p = constant * T, at constant n,V
Avogadro's principle:   V = constant * n, at constant p,T

Boyle and Charles are strictly true only when p -> 0
but they are still quite accurate at p = 1 bar (used in chemestry)

pV = constant * nT
>> perfect gas law: pV = nRT

'''

import math

def number_to_scientific(number, decimals=3):
    if number == 0:
        return "0 × 10^0"
    
    # Determine the exponent
    exponent = int(math.floor(math.log10(abs(number))))
    
    # Determine the mantissa
    mantissa = number / (10 ** exponent)
    
    # Format mantissa with comma after the first digit
    mantissa_str = f"{mantissa:.{decimals}f}"  # 3 decimal places, adjust if needed
    
    return f"{mantissa_str} × 10^{exponent}"

def torr_to_pascal(torr_val):
    # res = torr_val * (101325/760)
    res = torr_val * 133.32
    return res

def kelvin_to_celsius(kelvin_val, decimals=-1):
    res = kelvin_val - 273.15
    if decimals != -1:
        res = round(res, decimals)
    return res

def celsius_to_kelvin(val, decimals=-1):
    res = val + 273.15
    if decimals != -1:
        res = round(res, decimals)
    return res

def amount_of_substance(m, M):
    res = m / M
    return res

def calc_number_of_molecules(n):
    res = n * (6.0221 * (10 ** 23))
    return res

print('KELVIN TO CELSIUS:', kelvin_to_celsius(kelvin_val=300))
print('AMOUNT OF SUBSTANCE:', amount_of_substance(m=67, M=23))

print('TORR TO PASCAL:', torr_to_pascal(torr_val=10.4))
print('TORR TO PASCAL:', number_to_scientific(torr_to_pascal(torr_val=10.4), decimals=2))
print('CELSIUS TO KELVIN:', celsius_to_kelvin(val=25.2, decimals=0))
print('AMOUNT OF SUBSTANCE:', number_to_scientific(amount_of_substance(m=0.560 * (10 ** (-3)), M=14.01), decimals=2))
print('NUMBER OF MOLECULES:', number_to_scientific(calc_number_of_molecules(n=3.99 * (10 ** (-5))), decimals=2))

