"""Substitution."""

from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from gen.nodes import Node
else:
    Node = typing.Any


class Substitutor(ABC):
    """Substitutor."""

    @abstractmethod
    def substitute(self, code: str, variable: str, bracketed: bool = True) -> str:
        """Substitute."""

    @abstractmethod
    def loop_targets(self, variable: str) -> typing.Dict[str, typing.List[Substitutor]]:
        """Get list of loop targets."""
