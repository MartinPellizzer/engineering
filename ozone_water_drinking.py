'''

PHYSICAL AND CHEMICAL PROPERTIES

APPLICATIONS IN DRINKING WATER TREATMENT
disinfection
color, taste, odor removal
oxidative reactions is always the mechanism
inorganic and organic compounds
most inorganic reactions are very rapid (not bromate)
organic reactions can be fast or slow, depending on molecules and pH
advance oxidation by hydroxyl radical (HO*)
organic compound oxidized by ozone or HO form shorter-chainded organic molecules, many of which are readily biodegradable and removed in biological filters

inorganic
    - iron
    - manganese
    - hydrogen sulfide
    - bromide

organic
    - pathogens
        - bacteria
        - virus
        - giardia
        - cryptosporidium
    - other
        - solvents, HO
        - pesticides, HO
        - color, HO
        - taste and odor, HO

HO hydroxyl-free radical formation occurs naturally but may be promoted with high pH (>8.0) or with the addition of hydrogen peroxide

- difficult to oxidize organics include many solvents, pesticide, and compounds that cause tastes and odors (2-methylisoborneol [MIB] and geosmin), which are by-products of algal growth and decomposition.
- these organics require OH to oxidize, but most of the time OH produced naturally with ozone are enough
- ozone + hydrogen peroxide = PEROXONE (sometimes called like this)

DISINFECTION

log-inactivation
- 1-log = 90%
- 2-log = 99%
- 3-log = 99.9%

physical removal vs chemical inactivation
removal: sedimentation and filtration
inactivation: even if physically present, is dead, inactive, or incapable of reproduction

fundamental equation: indicates number oif organisms still viable after exposure to any disinfectant

N = N0 * 10^(-kp C^n T^m)
- N: number of organisms that remain viable
- N0: initial number of viable orbanisms
- kp: pathogen inactivation rate constant, Giarda-kg, virus-kv3, or Cryptoporidium-kc, log(N/N0)/CT
- C: residual-in-water, "concentration" of the disinfectant, mg/L
- T: exposure time, min
- n: allows the relative impact of C to be adjusted upward or downward
- m: allows the relative impact of T to be adjusted upward or downward

most of the time, you use n, m = 0
so the equation is Chick's law
used for the USEPA too

N = N0 * 10^(-kpCT)

log(N/N0) = -kp * C * T

to get positive values (ex. 2-log credit) invert log

-----------------------
log(N0/No) = kp * C * T
-----------------------

this equation is the primary one used by plant operator to calculate disinfection credits

- log(N0/N) = log-inactivation credit
- kp: pathogen inactivation rate constant, Giarda-kg, virus-kv3, or Cryptoporidium-kc
- C*T: disinfection "power", or ozone residual (mg/L), times time (min)

AI

log reduction = k * C * T
- k: how easy the microbe is to kill
- C: disinfectant strength
- T: time

-----------------------
k = (log kill) / (C * T)
-----------------------

we rearange the equation to find "k"
basically, based we want to make an experiment and find out "how fast does ozone kill a specific microbe"

temperature changes things:
    - warmer water = faster killing (high k)
    - colder water = slowr killing (low k)

to find k based on temperature, 3 methods:
    - look for already made tables
    - interpolation
        - k = a + b * (T_measured - T_low)
        - start with a base value (a)
        - add a correction based on temperature (b * difference)
    - formula k = c * e^(d * Temp)

special case: Cryptosporidium
    - use CT tables
    - formula k = g * h^(Temp)

---

CT depends on how much log reduction you need (target)
if the plant already do filtration and sedimentation, you need less CT
for example if the target log reduction is 4 log, and filtration already remove 2 log: 
    - you only need 2 log reduction with ozone

'''

import math

def log_kill(kp, C, T):
    res = kp * C * T
    return res

def kp(log_kill, C, T):
    res = log_kill / (C * T )
    return res

def kv(kind, Temp):
    if kind == 'virus': 
        c = 2.174
        d = 0.0701
    elif kind == 'giardia': 
        c = 1.038
        d = 0.0714
    else: return 'invalid data'
    res = c * math.exp(d * Temp)
    return res

def kc(Temp):
    g = 0.0397
    h = 1.09757
    res = g * (h ** Temp)
    return res

def log_kill_target_calc(log_kill_final, log_kill_filtration, log_kill_sedimentation):
    res = log_kill_final - log_kill_filtration - log_kill_sedimentation
    return res

print('log_kill:', log_kill(0.3, 1, 10))
print('kv virus:', kv('virus', 9))
print('kv giarda:', kv('giardia', 9))
print('kv cryptosporidium:', kc(5))
print('kv cryptosporidium:', kc(10))
print('kv cryptosporidium:', kc(15))
print('kv cryptosporidium:', kc(20))
print('log_kill_target_calc:', log_kill_target_calc(4, 2, 0.5), 'log kill')

