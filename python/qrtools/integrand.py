"""Integrands."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
import math


class Integrand(ABC):
    """An integrand."""

    @abstractmethod
    def as_latex(self) -> str:
        """Convert to LaTeX."""

    @abstractmethod
    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        """Evaluate for a set of inputs."""

    @abstractmethod
    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""

    @abstractmethod
    def _eq(self, other: Self) -> bool:
        """Check if self and other are equal."""

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self._eq(other)

    # Bracketness level
    #
    # Higher values will be bracketed more often. If 0,
    # this item will never be bracketed in LaTeX
    bracketness = 0



class Integer(Integrand):
    """An integer."""

    def __init__(self, i: int):
        self.i = i

    def as_latex(self) -> str:
        return str(self.i)

    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        return self.i

    def _eq(self, other: Self) -> bool:
        return self.i == other.i

    def set_domain(self, domain: str) -> Integrand:
        return self


class Variable(Integrand):
    """A variable."""

    def __init__(self, symbol: str):
        self.symbol = symbol

    def as_latex(self) -> str:
        return self.symbol

    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        return inputs[self.symbol]

    def _eq(self, other: Self) -> bool:
        return self.symbol == other.symbol

    def set_domain(self, domain: str) -> Integrand:
        if self.symbol.startswith("p["):
            assert self.symbol.endswith("]")
            n = int(self.symbol[2:-1])
            match domain:
                case "interval":
                    return parse_integrand(["x", "-x"][n])
                case "triangle":
                    return parse_integrand(["x", "y", "-x-y"][n])
                case _:
                    raise ValueError(f"Unsupported domain: {domain}")
        return self


class Function(Integrand):
    """A function with one or more inputs."""
    def __init__(self, name: str, *inputs: list[Integrand]):
        self.name = name
        self.inputs = inputs

    def as_latex(self) -> str:
        return "f(x)"

    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        return inputs[self.name](*[i.eval(**inputs) for i in self.inputs])

    def _eq(self, other: Self) -> bool:
        return self.name == other.name and len(self.inputs) == len(other.inputs) and all(
            [i == j for i, j in zip(self.inputs, other.inputs)]
        )

    def set_domain(self, domain: str) -> Integrand:
        return Function(self.name, *[i.set_domain(domain) for i in self.inputs])


class BinaryOperator(Integrand):
    """A binary operator."""

    def __init__(
        self,
        a: Integrand,
        b: Integrand,
        latex_template: str,
        fun: Callable,
        a_bracketness: int | None = None,
        b_bracketness: int | None = None,
    ):
        self.a = a
        self.b = b
        self.latex_template = latex_template
        self.f = fun
        self.a_bracketness = self.bracketness if a_bracketness is None else a_bracketness
        self.b_bracketness = self.bracketness if b_bracketness is None else b_bracketness

    def as_latex(self) -> str:
        a = self.a.as_latex()
        b = self.b.as_latex()
        if self.a.bracketness > self.a_bracketness:
            a = f"({a})"
        if self.b.bracketness > self.b_bracketness:
            b = f"({b})"
        return self.latex_template.replace("<a>", a).replace("<b>", b)

    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        return self.f(self.a.eval(**inputs), self.b.eval(**inputs))

    def _eq(self, other: Self) -> bool:
        return self.a == other.a and self.b == other.b

    def set_domain(self, domain: str) -> Integrand:
        return self.__class__(self.a.set_domain(domain), self.b.set_domain(domain))

    character = None


class CommutativeBinaryOperator(BinaryOperator):
    """A commitative binary operator."""

    def _eq(self, other: Self) -> bool:
        return (
            self.a == other.a and self.b == other.b
        ) or (
            self.a == other.b and self.b == other.a
        )


class Subtract(BinaryOperator):
    """Subtraction."""
    def __init__(self, a: Integrand, b: Integrand):
        super().__init__(a, b, "<a>-<b>", lambda x, y: x - y)

    bracketness = 50
    character = "-"


class Add(CommutativeBinaryOperator):
    """Addition."""
    def __init__(self, a: Integrand, b: Integrand):
        super().__init__(a, b, "<a>+<b>", lambda x, y: x + y)

    def set_domain(self, domain: str) -> Integrand:
        a = self.a.set_domain(domain)
        b = self.b.set_domain(domain)
        if isinstance(b, Negate):
            return Subtract(a, b.a)
        return Add(a, b)

    bracketness = 40
    character = "+"


class Divide(BinaryOperator):
    """Division."""
    def __init__(self, a: Integrand, b: Integrand):
        super().__init__(a, b, "\\frac{<a>}{<b>}", lambda x, y: x / y)

    bracketness = 30
    character = "/"


class Multiply(CommutativeBinaryOperator):
    """Muliplication."""
    def __init__(self, a: Integrand, b: Integrand):
        super().__init__(a, b, "<a><b>", lambda x, y: x * y)

    bracketness = 20
    character = "*"


class Raise(BinaryOperator):
    """Raise to a power."""
    def __init__(self, a: Integrand, b: Integrand):
        super().__init__(a, b, "<a>^{<b>}", lambda x, y: x ** y, b_bracketness=1000)

    bracketness = 10
    character = "^"


class UnaryOperator(Integrand):
    """A unary operator."""
    def __init__(
        self,
        a: Integrand,
        latex_template: str,
        fun: Callable,
        a_bracketness: int | None = None,
    ):
        self.a = a
        self.f = fun
        self.latex_template = latex_template
        self.a_bracketness = self.bracketness if a_bracketness is None else a_bracketness

    def as_latex(self) -> str:
        a = self.a.as_latex()
        if self.a.bracketness > self.a_bracketness:
            a = f"({a})"
        return self.latex_template.replace("<a>", a)

    def eval(self, **inputs: dict[str, float | Callable]) -> float:
        return self.f(self.a.eval(**inputs))

    def _eq(self, other: Self) -> bool:
        return self.a == other.a

    def set_domain(self, domain: str) -> Integrand:
        return self.__class__(self.a.set_domain(domain))

    bracketness = 0
    character = None

class Negate(UnaryOperator):
    """A function with one or more inputs."""

    def __init__(self, a: Integrand):
        super().__init__(a, "-<a>", lambda x: -x)

    character = "-"


class Sqrt(UnaryOperator):
    """Square root."""

    def __init__(self, a: Integrand):
        super().__init__(a, "\\sqrt{<a>}", lambda x: math.sqrt(x))

    character = "sqrt"

binary_operators = [
    op for op in globals().values()
    if isinstance(op, type) and issubclass(op, BinaryOperator) and op != BinaryOperator
]
binary_operators.sort(key=lambda c: -c.bracketness)

unary_operators = {
    op.character: op for op in globals().values()
    if isinstance(op, type) and issubclass(op, UnaryOperator) and op != UnaryOperator and len(op.character) == 1
}

functions = {
    op.character: op for op in globals().values()
    if isinstance(op, type) and issubclass(op, UnaryOperator) and op != UnaryOperator and len(op.character) > 1
}


def parse_integrand(function: str) -> Integrand:
    function = function.replace(" ", "")

    for op in binary_operators:
        for i, c in enumerate(function):
            if c == op.character:
                pre = function[:i]
                post = function[i + 1:]
                if len(pre) > 0 and len(post) > 0 and pre.count("(") == pre.count(")"):
                    return op(parse_integrand(pre), parse_integrand(post))
    if function[0] in unary_operators:
        return unary_operators[function[0]](parse_integrand(function[1:]))

    if function[0] == "(" and function[-1] == ")":
        for i, _ in enumerate(function[1:-1]):
            if function[1:1+i].count(")") > function[1:1+i].count("("):
                raise ValueError(f"Invalid integrand: {function}")
        return parse_integrand(function[1:-1])

    if "(" in function and function.endswith(")"):
        name, inputs = function.split("(", 1)
        inputs = inputs[:-1]
        for i, _ in enumerate(inputs):
            if inputs[:i].count(")") > inputs[:i].count("("):
                raise ValueError(f"Invalid integrand: {function}")
        if name in functions:
            return functions[name](*[parse_integrand(i) for i in inputs.split(",")])
        return Function(name, *[parse_integrand(i) for i in inputs.split(",")])

    try:
        return Integer(int(function))
    except ValueError:
        pass

    return Variable(function)
