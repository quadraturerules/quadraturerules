import pytest
import numpy as np
from quadraturerules import Domain, QuadratureRule, single_integral_quadrature


@pytest.mark.parametrize("order", [1, 2, 3])
def test_sum_weights(order):
    assert np.isclose(
        sum(single_integral_quadrature(QuadratureRule.GaussLegendre, Domain.Interval, order)[1]),
        1.0,
    )
