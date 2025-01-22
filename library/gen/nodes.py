"""Nodes."""

import typing
from abc import ABC, abstractmethod

from gen.substitute import Substitutor


class Node(ABC):
    """Base class."""

    @abstractmethod
    def substitute(
        self,
        vars: typing.Dict[str, Substitutor] = {},
        loop_targets: typing.Dict[str, typing.List[Substitutor]] = {},
    ) -> str:
        """Subtitute variables into node."""


class ListOfNodes(Node):
    """A list of nodes."""

    def __init__(self, nodes: typing.List[Node]):
        """Initialise."""
        self.nodes = nodes

    def __add__(self, other):
        """Add."""
        if isinstance(other, ListOfNodes):
            return ListOfNodes(self.nodes + other.nodes)
        return ListOfNodes(self.nodes + other)

    def substitute(
        self,
        vars: typing.Dict[str, Substitutor] = {},
        loop_targets: typing.Dict[str, typing.List[Substitutor]] = {},
    ) -> str:
        """Subtitute variables into node."""
        return "".join(i.substitute(vars, loop_targets) for i in self.nodes)


class If(Node):
    """An if conditional."""

    def __init__(self, condition: str, inside: ListOfNodes):
        """Initialise."""
        self.condition = condition
        self.inside = inside

    def substitute(
        self,
        vars: typing.Dict[str, Substitutor] = {},
        loop_targets: typing.Dict[str, typing.List[Substitutor]] = {},
    ) -> str:
        """Subtitute variables into node."""
        condition = self.condition
        for v, s in vars.items():
            condition = s.substitute(condition, v, False)
        if "==" in condition:
            a, b = condition.split("==")
            if a.strip() == b.strip():
                return self.inside.substitute(vars, loop_targets)
            else:
                return ""
        if "!=" in condition:
            a, b = condition.split("!=")
            if a.strip() != b.strip():
                return self.inside.substitute(vars, loop_targets)
            else:
                return ""
        raise ValueError(f"Invalid condition: {condition}")


class For(Node):
    """A for loop."""

    def __init__(self, variable: str, loop_over: str, inside: ListOfNodes):
        """Initialise."""
        self.variable = variable
        self.loop_over = loop_over
        self.inside = inside

    def substitute(
        self,
        vars: typing.Dict[str, Substitutor] = {},
        loop_targets: typing.Dict[str, typing.List[Substitutor]] = {},
    ) -> str:
        """Subtitute variables into node."""
        if self.loop_over in loop_targets:
            return "".join(
                self.inside.substitute(
                    {**vars, self.variable: i},
                    loop_targets,
                )
                for i in loop_targets[self.loop_over]
            )
        for v, s in vars.items():
            lt = s.loop_targets(v)
            if self.loop_over in lt:
                return "".join(
                    self.inside.substitute(
                        {**vars, self.variable: i},
                        loop_targets,
                    )
                    for i in lt[self.loop_over]
                )
        raise ValueError(f"Invalid loop target: {self.loop_over}")


class Line(Node):
    """A line of code."""

    def __init__(self, line: str):
        """Initialise."""
        self.line = line

    def substitute(
        self,
        vars: typing.Dict[str, Substitutor] = {},
        loop_targets: typing.Dict[str, typing.List[Substitutor]] = {},
    ) -> str:
        """Subtitute variables into node."""
        line = self.line
        for v, s in vars.items():
            line = s.substitute(line, v)
        return line + "\n"
