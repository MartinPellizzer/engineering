'''

THEORY:

---

proportions

2/4 = 5/10
3/6 = x/4

functions
---
take an input and do something with it
input x -> output y

y = 2x + 3

ex. if x = 0...
y = 2(0) + 3 = 3

ex. if x = 1...
y = 2(1) + 3 = 5

ex. if x = 2...
y = 2(2) + 3 = 7

f(x) = 2x + 3
ex. if x = 2...
f(2) = 2(2) + 3 = 7

'''

# proportions

if 0:
    # put a zero in for the unknown value
    # n1/d1 = n2/d2
    # 1/2 = x/16
    n1 = 1
    d1 = 2
    n2 = 0
    d2 = 16

    if n2 == 0:
        answer = d2 * n1 / d1
        print('n2 =', answer)

    if d2 == 0:
        answer = n2 * d1 / n1
        print('d2 =', answer)

########################################

# `equations

if 0:
    import sympy
    from sympy import symbols
    from sympy.solvers import solve

    x = symbols('x')

    eq = 2*x**2 - 4

    print('x =', solve(eq, x))

if 0:
    import sympy
    from sympy import symbols
    from sympy.solvers import solve

    x = symbols('x')

    eq = input('entrer equation: 0 = ')

    print('x =', solve(eq, x))

if 0:
    import sympy
    from sympy import symbols
    from sympy.solvers import solve

    x = symbols('x')

    eq = 2*x - 4

    solution = solve(eq, x)

    print('x =', solution[0])

if 0:
    import sympy
    from sympy import symbols
    from sympy.solvers import solve

    x = symbols('x')

    eq = input('enter equation: 0 = ')

    solution = solve(eq, x)
    for s in solution:
        print('x =', s)

if 0:
    from sympy import *

    var('x y')

    first = 2*x + 10

    eq1 = Eq(first, y)

    sol = solve(eq1, x)

    print('x =', sol[0])

if 0:
    import sympy
    from sympy import symbols

    sympy.var('x y')

    eq = 2*x + 10*y + 4
    eq = x**2 - 4
    eq = x**3 - 2*x**2 - 5*x + 6

    print(sympy.factor(eq))


if 0:
    def string_frac(in_string):
        if '/' in in_string:
            nd = in_string.split('/')
            n = float(nd[0])
            d = float(nd[1])
            ans = n/d
            return ans
        else:
            ans = float(in_string)
            return ans

    def one_step_mult():
        import random
        a = random.randint(1, 11)
        b = random.randint(2, 24)
        print(a, 'x =', b)
        ans_in = (input('x = '))
        answer = b/a
        if string_frac(ans_in) == answer:
            print('correct\n')
        else:
            print('try again')
            print('the correct answer is', answer, '\n')

    one_step_mult()

### create functions (video timestamp 00:57:00)

########################################

# `fractions and decimals

if 0:
    print(10**1)
    print(10**2)
    print(10**3)
    print(10**0)

if 0:
    text = input('enter a number: ')
    num = float(text)
    print(num + 4)

if 0:
    digits = input('Enter a decimal number to convert: ')
    exponent = int(len(digits))-1
    n = float(digits)
    numerator = int(n * 10**exponent)
    denominator = 10**exponent
    percent = n * 100
    print('the decimal is', n)
    print('the fraction is', numerator, '/', denominator)
    print('the percent is', percent, '%')

########################################

# `functions

if 0:
    x = 5
    y = 4*x + 3
    print(x, ',', y)
    print('x \t y')
    for x in range(11):
        y = 4*x + 3
        print(x, '\t', y)

if 1:
    def f(x):
        y = 4*x + 3
        return y
    print(5, ',', f(5))
    for x in range(11):
        print(x, '\t', f(x))
