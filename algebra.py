'''

THEORY:

---

proportions

2/4 = 5/10
3/6 = x/4

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


if 1:
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

