"""Integrands."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

try:
    from typing import Self  # type: ignore
except ImportError:
    from typing_extensions import Self
import math


class Integrand(ABC):
    """An integrand."""

    @abstractmethod
    def as_latex(self) -> str:
        """Convert to LaTeX."""

    @abstractmethod
    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""

    @abstractmethod
    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""

    @abstractmethod
    def _eq(self, other: Self) -> bool:
        """Check if self and other are equal."""

    def __eq__(self, other) -> bool:
        """Check for equality."""
        return type(self) is type(other) and self._eq(other)

    # Bracketness level
    #
    # Higher values will be bracketed more often. If 0,
    # this item will never be bracketed in LaTeX
    bracketness = 0


class Integer(Integrand):
    """An integer."""

    def __init__(self, i: int):
        """Initialise."""
        self.i = i

    def as_latex(self) -> str:
        """Convert to LaTeX."""
        return str(self.i)

    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""
        return self.i

    def _eq(self, other: Self) -> bool:
        return self.i == other.i

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
        return self


class Variable(Integrand):
    """A variable."""

    def __init__(self, symbol: str):
        """Initialise."""
        self.symbol = symbol

    def as_latex(self) -> str:
        """Convert to LaTeX."""
        return self.symbol

    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""
        value = inputs[self.symbol]
        assert isinstance(value, float)
        return value

    def _eq(self, other: Self) -> bool:
        return self.symbol == other.symbol

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
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

    def __init__(self, name: str, *inputs: Integrand):
        """Initialise."""
        self.name = name
        self.inputs = inputs

    def as_latex(self) -> str:
        """Convert to LaTeX."""
        return "f(x)"

    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""
        f = inputs[self.name]
        assert not isinstance(f, float)
        return f(*[i.eval(**inputs) for i in self.inputs])

    def _eq(self, other: Self) -> bool:
        return (
            self.name == other.name
            and len(self.inputs) == len(other.inputs)
            and all([i == j for i, j in zip(self.inputs, other.inputs)])
        )

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
        return Function(self.name, *[i.set_domain(domain) for i in self.inputs])


class BinaryOperator(Integrand):
    """A binary operator."""

    def __init__(
        self,
        a: Integrand,
        b: Integrand,
    ):
        """Initialise."""
        self.a = a
        self.b = b
        if self.a_bracketness is None:
            self.a_bracketness = self.bracketness
        if self.b_bracketness is None:
            self.b_bracketness = self.bracketness

    def as_latex(self) -> str:
        """Convert to LaTeX."""
        a = self.a.as_latex()
        b = self.b.as_latex()
        assert self.a_bracketness is not None
        if self.a.bracketness > self.a_bracketness:
            a = f"({a})"
        assert self.b_bracketness is not None
        if self.b.bracketness > self.b_bracketness:
            b = f"({b})"
        assert self.latex_template is not None
        return self.latex_template.replace("<a>", a).replace("<b>", b)

    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""
        assert self.fun is not None
        return self.fun(self.a.eval(**inputs), self.b.eval(**inputs))

    def _eq(self, other: Self) -> bool:
        return self.a == other.a and self.b == other.b

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
        return self.__class__(self.a.set_domain(domain), self.b.set_domain(domain))

    @abstractmethod
    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        pass

    character: str | None = None
    latex_template: str | None = None
    a_bracketness: int | None = None
    b_bracketness: int | None = None


class CommutativeBinaryOperator(BinaryOperator):
    """A commitative binary operator."""

    def _eq(self, other: Self) -> bool:
        return (self.a == other.a and self.b == other.b) or (
            self.a == other.b and self.b == other.a
        )


class Subtract(BinaryOperator):
    """Subtraction."""

    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        return x - y

    bracketness = 50
    character = "-"
    latex_template = "<a>-<b>"


class Add(CommutativeBinaryOperator):
    """Addition."""

    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        return x + y

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
        a = self.a.set_domain(domain)
        b = self.b.set_domain(domain)
        if isinstance(b, Negate):
            return Subtract(a, b.a)
        return Add(a, b)

    bracketness = 40
    character = "+"
    latex_template = "<a>+<b>"


class Divide(BinaryOperator):
    """Division."""

    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        return x / y

    bracketness = 30
    character = "/"
    latex_template = "\\frac{<a>}{<b>}"


class Multiply(CommutativeBinaryOperator):
    """Muliplication."""

    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        return x * y

    bracketness = 20
    character = "*"
    latex_template = "<a><b>"


class Raise(BinaryOperator):
    """Raise to a power."""

    def fun(self, x: float, y: float) -> float:
        """Evaluate this operator."""
        return x**y

    bracketness = 10
    character = "^"
    latex_template = "<a>^{<b>}"
    b_bracketness = 1000


class UnaryOperator(Integrand):
    """A unary operator."""

    def __init__(
        self,
        a: Integrand,
        a_bracketness: int | None = None,
    ):
        """Initialise."""
        self.a = a
        if self.a_bracketness is None:
            self.a_bracketness = self.bracketness

    def as_latex(self) -> str:
        """Convert to LaTeX."""
        a = self.a.as_latex()
        assert self.a_bracketness is not None
        if self.a.bracketness > self.a_bracketness:
            a = f"({a})"
        assert self.latex_template is not None
        return self.latex_template.replace("<a>", a)

    def eval(self, **inputs: float | Callable) -> float:
        """Evaluate for a set of inputs."""
        return self.fun(self.a.eval(**inputs))

    def _eq(self, other: Self) -> bool:
        return self.a == other.a

    def set_domain(self, domain: str) -> Integrand:
        """Set the domain for the integrand."""
        return self.__class__(self.a.set_domain(domain))

    @abstractmethod
    def fun(self, x: float) -> float:
        """Evaluate this operator."""
        pass

    bracketness = 0
    character: str | None = None
    latex_template: str | None = None
    a_bracketness: int | None = None


class Negate(UnaryOperator):
    """A function with one or more inputs."""

    def fun(self, x: float) -> float:
        """Evaluate this operator."""
        return -x

    character = "-"
    latex_template = "-<a>"


class Sqrt(UnaryOperator):
    """Square root."""

    def fun(self, x: float) -> float:
        """Evaluate this operator."""
        return math.sqrt(x)

    character = "sqrt"
    latex_template = "\\sqrt{<a>}"


binary_operators = [
    op
    for op in globals().values()
    if isinstance(op, type) and issubclass(op, BinaryOperator) and op != BinaryOperator
]
binary_operators.sort(key=lambda c: -c.bracketness)

unary_operators = {
    op.character: op
    for op in globals().values()
    if isinstance(op, type)
    and issubclass(op, UnaryOperator)
    and op != UnaryOperator
    and op.character is not None
    and len(op.character) == 1
}

unary_functions = {
    op.character: op
    for op in globals().values()
    if isinstance(op, type)
    and issubclass(op, UnaryOperator)
    and op != UnaryOperator
    and op.character is not None
    and len(op.character) > 1
}


def parse_integrand(function: str) -> Integrand:
    """Parse a string as an integrand."""
    function = function.replace(" ", "")

    for op in binary_operators:
        for i, c in enumerate(function):
            if c == op.character:
                pre = function[:i]
                post = function[i + 1 :]
                if len(pre) > 0 and len(post) > 0 and pre.count("(") == pre.count(")"):
                    return op(parse_integrand(pre), parse_integrand(post))
    if function[0] in unary_operators:
        return unary_operators[function[0]](parse_integrand(function[1:]))

    if function[0] == "(" and function[-1] == ")":
        for i, _ in enumerate(function[1:-1]):
            if function[1 : 1 + i].count(")") > function[1 : 1 + i].count("("):
                raise ValueError(f"Invalid integrand: {function}")
        return parse_integrand(function[1:-1])

    if "(" in function and function.endswith(")"):
        name, inputs = function.split("(", 1)
        inputs = inputs[:-1]
        for i, _ in enumerate(inputs):
            if inputs[:i].count(")") > inputs[:i].count("("):
                raise ValueError(f"Invalid integrand: {function}")
        if name in unary_functions:
            args = [parse_integrand(i) for i in inputs.split(",")]
            assert len(args) == 1
            return unary_functions[name](args[0])
        return Function(name, *[parse_integrand(i) for i in inputs.split(",")])

    try:
        return Integer(int(function))
    except ValueError:
        pass

    return Variable(function)
