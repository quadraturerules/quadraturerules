import pytest
import numpy as np
from quadraturerules import Domain, QuadratureRule, single_integral_quadrature


@pytest.mark.parametrize("order", range(1, 10))
def test_integral_of_polynomial(order):
    # f = x ** (2 * order - 1)
    # integral(f, x) = x ** (2 * order) / (2 * order)
    # integral(f, x=0..1) = 0.5 / order
    pts, wts = single_integral_quadrature(
        QuadratureRule.GaussLobattoLegendre, Domain.Interval, order
    )
    integral = sum(w * p[1] ** (2 * order - 1) for p, w in zip(pts, wts))
    assert np.isclose(integral, 0.5 / order)
