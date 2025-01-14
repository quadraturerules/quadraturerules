"""Integral domains."""

from enum import Enum


class Domain(Enum):
    """A domain of an integral."""

    {{for D in domains}}
    {{D.PascalCaseName}} = {{D.index}}
    {{end for}}
