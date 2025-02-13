"""Quadrature rules."""

from enum import Enum as _Enum
import typing as _typing
import numpy.typing as _npt
import numpy as _np

from quadraturerules import rules
from quadraturerules.domain import Domain


class QuadratureRule(_Enum):
    """A quadrature rule family."""

    {{for Q in rules}}
    {{Q.PascalCaseName}} = {{Q.index}}
    {{end for}}


def single_integral_quadrature(
    rtype: QuadratureRule,
    domain: Domain,
    order: int,
) -> _typing.Tuple[_npt.NDArray[_np.float64], _npt.NDArray[_np.float64]]:
    """Get a quadrature rule for a single integral."""
    match rtype:
        {{for Q in rules}}
        {{if Q.itype == single}}
        case QuadratureRule.{{Q.PascalCaseName}}:
            return rules.{{Q.snake_case_name}}(domain, order)
        {{end if}}
        {{end for}}
        case _:
            raise ValueError(f"Unsupported rule for single integral: {rtype}")


def double_integral_quadrature(
    rtype: QuadratureRule,
    domain: Domain,
    order: int,
) -> _typing.Tuple[_npt.NDArray[_np.float64], _npt.NDArray[_np.float64], _npt.NDArray[_np.float64]]:
    """Get a quadrature rule for a double integral."""
    match rtype:
        {{for Q in rules}}
        {{if Q.itype == double}}
        case QuadratureRule.{{Q.PascalCaseName}}:
            return rules.{{Q.snake_case_name}}(domain, order)
        {{end if}}
        {{end for}}
        case _:
            raise ValueError(f"Unsupported rule for double integral: {rtype}")
