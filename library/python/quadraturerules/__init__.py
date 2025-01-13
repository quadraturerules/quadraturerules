"""Quadrature rules."""

from enum import Enum as _Enum

class QuadratureRules(_Enum):
    {{for Q in rules}}
    {{Q.PascalCaseName}} = {{Q.id}}
    {{end for}}
