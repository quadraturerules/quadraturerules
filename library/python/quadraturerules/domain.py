"""Integral domains."""

from enum import Enum


class Domain(Enum):
    {{for D in domains}}
    {{D.PascalCaseName}} = {{D.index}}
    {{end for}}
