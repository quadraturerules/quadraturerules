"""Substitution."""

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from gen.nodes import Node
else:
    Node = typing.Any

class Substitutor(ABC):
    """Substitutor."""

    @abstractmethod
    def substitute(self, code: str, variable: str) -> str:
        """Substitute."""

    @abstractmethod
    def loop_targets(self, variable: str) -> typing.Dict[str, typing.List[Node]]:
        """Get list of loop targets."""
