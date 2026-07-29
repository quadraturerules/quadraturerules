import numpy as np
import pytest

from quadraturerules import Domain, QuadratureRule, single_integral_quadrature


@pytest.mark.parametrize("order", [1, 2, 3])
def test_sum_weights(order):
    assert np.isclose(
        sum(single_integral_quadrature(QuadratureRule.GaussLegendre, Domain.Interval, order)[1]),
        1.0,
    )


@pytest.mark.parametrize("order", range(1, 10))
def test_integral_of_polynomial(order):
    # f = x ** (2 * order - 1)
    # integral(f, x) = x ** (2 * order) / (2 * order)
    # integral(f, x=0..1) = 0.5 / order
    pts, wts = single_integral_quadrature(QuadratureRule.GaussLegendre, Domain.Interval, order)
    integral = sum(w * p[1] ** (2 * order - 1) for p, w in zip(pts, wts))
    assert np.isclose(integral, 0.5 / order)
