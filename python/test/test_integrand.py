import pytest
from qrtools.integrand import parse_integrand
import numpy as np


def test_function_1():
    i = parse_integrand("f(x)")
    assert np.isclose(i.eval(x=0.0, f=lambda x: 1 - x), 1.0)


def test_function_2():
    i = parse_integrand("f(x, y)")
    assert np.isclose(i.eval(x=0.3, y=0.2, f=lambda x, y: x + y), 0.5)


def test_function_3():
    i = parse_integrand("f(x,y,z)")
    assert np.isclose(i.eval(x=0.3, y=0.2, z=2.0, f=lambda x, y, z: x + y + z ** 2), 4.5)


def test_chebyshev_1():
    i = parse_integrand("f(x) / sqrt(1-x^2)")
    assert np.isclose(i.eval(x=0.6, f=lambda x: 3 * x), 9 / 4)


def test_chebyshev_2():
    i = parse_integrand("f(x) * sqrt(1-x^2)")
    assert np.isclose(i.eval(x=0.6, f=lambda x: 3 * x), 1.44)


@pytest.mark.parametrize(("integrand", "latex"), [
    ("1", "1"),
    ("x", "x"),
    ("sqrt(x)", "\\sqrt{x}"),
    ("(x + y) + (z + 2)", "x+y+z+2"),
    ("2 * (x - 3)", "2(x-3)"),
    ("2 * ((x - 3))", "2(x-3)"),
    ("(2) * ((x - 3))", "2(x-3)"),
    ("((2) * ((x - 3)))", "2(x-3)"),
    ("2 + (x/3)", "2+\\frac{x}{3}"),
    ("2 + x/3", "2+\\frac{x}{3}"),
    ("2^(x/3)", "2^{\\frac{x}{3}}"),
])
def test_latex(integrand, latex):
    assert parse_integrand(integrand).as_latex() == latex


def test_eq():
    assert parse_integrand("f(x)") == parse_integrand("f(x)")
    assert parse_integrand("2 * x") == parse_integrand("x*2")
    assert parse_integrand("2 + x") == parse_integrand("x + 2")


def test_not_eq():
    assert parse_integrand("f(x)") != parse_integrand("f(x,y)")
    assert parse_integrand("x/2") != parse_integrand("2/x")
    assert parse_integrand("x-2") != parse_integrand("2-x")


@pytest.mark.parametrize(("integrand", "on_interval"), [
    ("p[0]", "x"),
    ("(1 + p[0]) * (1 + p[1])", "(1 + x) * (1 - x)"),
])
def test_set_domain(integrand, on_interval):
    print(parse_integrand(integrand).set_domain("interval").as_latex())
    print(parse_integrand(on_interval).as_latex())
    assert parse_integrand(integrand).set_domain("interval") == parse_integrand(on_interval)
