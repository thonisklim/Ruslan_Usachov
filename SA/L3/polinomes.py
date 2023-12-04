import sympy as sp


def do_offset2_chebish_polinom(x, n):
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = 4 * x - 2
    elif n == 2:
        T = 16*x**2 - 16*x + 3
    else:
        T = 2 * (2 * x - 1) * do_offset2_chebish_polinom(x, n - 1) - do_offset2_chebish_polinom(x, n - 2)
    return T


def do_offset2_chebish_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = 4 * symb - 2
    elif n == 2:
        T = 16*symb**2 - 16*symb + 3
    else:
        T = sp.expand(2 * (2 * symb - 1) * do_offset2_chebish_polinom_univ(var_name, n - 1) - do_offset2_chebish_polinom_univ(var_name, n - 2))
    return T


def do_offset1_chebish_polinom(x, n):
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = 2 * x - 1
    elif n == 2:
        T = 1 - 8*x + 8*x**2
    else:
        T = 2 * (2 * x - 1) * do_offset1_chebish_polinom(x, n - 1) - do_offset1_chebish_polinom(x, n - 2)
    return T


def do_offset1_chebish_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = -1 + 2 * symb
    elif n == 2:
        T = 1 - 8*symb + 8*symb**2
    else:
        T = sp.expand(2 * (-1 + 2 * symb) * do_offset1_chebish_polinom_univ(var_name, n - 1) - do_offset1_chebish_polinom_univ(var_name, n - 2))
    return T


def do_chebish_polinom(x, n):
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = 2 * x
    elif n == 2:
        T = 4*x**2 - 1
    else:
        T = 2 * do_chebish_polinom(x, n - 1) - do_chebish_polinom(x, n - 2)
    return T


def do_chebish_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 0.5
    elif n == 1:
        T = 2 * symb
    elif n == 2:
        T = 4*symb**2 - 1
    else:
        T = sp.expand(2 * do_chebish_polinom_univ(var_name, n - 1) - do_chebish_polinom_univ(var_name, n - 2))
    return T


def do_lezhandr_polinom(x, n):
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = x
    else:
        T = ((2 * n + 1) * x * do_lezhandr_polinom(x, n-1) - n * do_lezhandr_polinom(x, n-2)) * (1 / (n + 1))
    return T


def do_lezhandr_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = symb
    else:
        T = sp.expand(((2 * n + 1) * symb * do_lezhandr_polinom_univ(var_name, n - 1) - n * do_lezhandr_polinom_univ(var_name, n - 2)) * (1 / (n + 1)))
    return T


def do_lagerr_polinom(x, n):
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = -x+1
    else:
        T = (2*n+1-x) * do_lagerr_polinom(x, n-1) - n**2 * do_lagerr_polinom(x, n-2)
    return T


def do_lagerr_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = -symb+1
    else:
        T = sp.expand((2*n+1-symb) * do_lagerr_polinom_univ(var_name, n - 1) - n**2 * do_lagerr_polinom_univ(var_name, n-2))
    return T


def do_ermit_polinom(x, n):
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = 2*x
    else:
        T = 2*x*do_ermit_polinom(x, n-1)-2*n*do_ermit_polinom(x,n-2)
    return T


def do_ermit_polinom_univ(var_name, n):
    symb = sp.symbols(var_name)
    T = 0
    if n == 0:
        T = 1
    elif n == 1:
        T = 2 * symb
    else:
        T = sp.expand(2*symb*do_ermit_polinom_univ(var_name, n - 1) - 2*n*do_ermit_polinom_univ(var_name, n - 2))
    return T
