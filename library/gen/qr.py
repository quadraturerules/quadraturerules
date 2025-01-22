"""Quadrature rule specifics."""

import re
import typing

from gen.substitute import Substitutor
from quadraturerules_website import rules


def replace(
    content: str,
    subs: typing.List[typing.Tuple[str, typing.Callable]],
    bracketed: bool = True,
) -> str:
    """Make multiple replacements."""
    if bracketed:
        for a, b in subs:
            if f"{{{{{a}}}}}" in content:
                content = content.replace(f"{{{{{a}}}}}", b())
    else:
        for a, b in subs:
            if a in content:
                content = content.replace(a, b())
    return content


class IndexedFloat(Substitutor):
    """Substitutor for a floating point number in an array."""

    def __init__(self, value, index):
        """Initialise."""
        self.value = value
        self.index = index

    def substitute(self, code: str, variable: str, bracketed: bool = True) -> str:
        """Substitute."""
        return replace(
            code,
            [
                (f"{variable}", lambda: f"{self.value}"),
                (f"{variable}.index", lambda: f"{self.index}"),
            ],
            bracketed,
        )

    def loop_targets(
        self,
        variable: str,
    ) -> typing.Dict[str, typing.Generator[Substitutor, None, None]]:
        """Get list of loop targets."""
        return {}


class RuleFamily(Substitutor):
    """Substitutor for a rule family."""

    def __init__(self, family):
        """Initialise."""
        self.family = family

    def substitute(self, code: str, variable: str, bracketed: bool = True) -> str:
        """Substitute."""
        return replace(
            code,
            [
                (f"{variable}.code", lambda: f"{self.family.code}"),
                (f"{variable}.index", lambda: f"{self.family.index}"),
                (f"{variable}.itype", lambda: self.family.itype),
                (f"{variable}.name", lambda: self.family.name()),
                (f"{variable}.PascalCaseName", lambda: self.family.name("PascalCase")),
                (f"{variable}.camelCaseName", lambda: self.family.name("camelCase")),
                (f"{variable}.snake_case_name", lambda: self.family.name("snake_case")),
            ],
            bracketed,
        )

    def loop_targets(
        self,
        variable: str,
    ) -> typing.Dict[str, typing.Generator[Substitutor, None, None]]:
        """Get list of loop targets."""
        return {f"{variable}.rules": (Rule(r) for r in self.family.rules)}


class Rule(Substitutor):
    """Substitutor for a rule."""

    def __init__(self, rule):
        """Initialise."""
        self.rule = rule

    def substitute(self, code: str, variable: str, bracketed: bool = True) -> str:
        """Substitute."""
        subs = [
            (f"{variable}.order", lambda: f"{self.rule.order}"),
            (f"{variable}.domain", lambda: self.rule.domain),
            (f"{variable}.len_weights", lambda: f"{len(self.rule.weights)}"),
            (f"{variable}.weights_as_list", lambda: self.rule.weights_as_list()),
            (
                f"{variable}.weights_as_curly_list",
                lambda: self.rule.weights_as_list("{", "}"),
            ),
        ]
        if isinstance(self.rule, rules.QRuleSingle):
            subs += [
                (
                    f"{variable}.len_flat_points",
                    lambda: f"{len(self.rule.points) * len(self.rule.points[0])}",
                ),
                (f"{variable}.points_as_list", lambda: self.rule.points_as_list()),
                (
                    f"{variable}.points_as_flat_list",
                    lambda: self.rule.points_as_flat_list(),
                ),
                (
                    f"{variable}.points_as_curly_list",
                    lambda: self.rule.points_as_list("{", "}"),
                ),
                (
                    f"{variable}.points_as_flat_curly_list",
                    lambda: self.rule.points_as_flat_list("{", "}"),
                ),
            ]
        elif isinstance(self.rule, rules.QRuleDouble):
            subs += [
                (
                    f"{variable}.len_flat_first_points",
                    lambda: f"{len(self.rule.first_points) * len(self.rule.first_points[0])}",
                ),
                (
                    f"{variable}.len_flat_second_points",
                    lambda: f"{len(self.rule.second_points) * len(self.rule.second_points[0])}",
                ),
                (
                    f"{variable}.first_points_as_list",
                    lambda: self.rule.first_points_as_list(),
                ),
                (
                    f"{variable}.first_points_as_flat_list",
                    lambda: self.rule.first_points_as_flat_list(),
                ),
                (
                    f"{variable}.first_points_as_curly_list",
                    lambda: self.rule.first_points_as_list("{", "}"),
                ),
                (
                    f"{variable}.first_points_as_flat_curly_list",
                    lambda: self.rule.first_points_as_flat_list("{", "}"),
                ),
                (
                    f"{variable}.second_points_as_list",
                    lambda: self.rule.second_points_as_list(),
                ),
                (
                    f"{variable}.second_points_as_flat_list",
                    lambda: self.rule.second_points_as_flat_list(),
                ),
                (
                    f"{variable}.second_points_as_curly_list",
                    lambda: self.rule.second_points_as_list("{", "}"),
                ),
                (
                    f"{variable}.second_points_as_flat_curly_list",
                    lambda: self.rule.second_points_as_flat_list("{", "}"),
                ),
            ]
        return replace(code, subs, bracketed)

    def loop_targets(
        self,
        variable: str,
    ) -> typing.Dict[str, typing.Generator[Substitutor, None, None]]:
        """Get list of loop targets."""
        out: typing.Dict[str, typing.Generator[Substitutor, None, None]] = {
            f"{variable}.weights": (
                IndexedFloat(w, i) for i, w in enumerate(self.rule.weights)
            )
        }
        if isinstance(self.rule, rules.QRuleSingle):
            out[f"{variable}.flat_points"] = (
                IndexedFloat(c, i * len(self.rule.points[0]) + j)
                for i, p in enumerate(self.rule.points)
                for j, c in enumerate(p)
            )
        if isinstance(self.rule, rules.QRuleDouble):
            out[f"{variable}.flat_first_points"] = (
                IndexedFloat(c, i * len(self.rule.first_points[0]) + j)
                for i, p in enumerate(self.rule.first_points)
                for j, c in enumerate(p)
            )
            out[f"{variable}.flat_second_points"] = (
                IndexedFloat(c, i * len(self.rule.second_points[0]) + j)
                for i, p in enumerate(self.rule.second_points)
                for j, c in enumerate(p)
            )
        return out


class Domain(Substitutor):
    """Substitutor for a domain."""

    def __init__(self, domain, index):
        """Initialise."""
        self.domain = domain
        self.index = index

    def substitute(self, code: str, variable: str, bracketed: bool = True) -> str:
        """Substitute."""
        parts = re.split(r"--|\s|-", self.domain)
        return replace(
            code,
            [
                (f"{variable}.index", lambda: f"{self.index}"),
                (
                    f"{variable}.PascalCaseName",
                    lambda: "".join(i[0].upper() + i[1:].lower() for i in parts),
                ),
                (
                    f"{variable}.camelCaseName",
                    lambda: parts[0].lower()
                    + "".join(i[0].upper() + i[1:].lower() for i in parts[1:]),
                ),
                (
                    f"{variable}.snake_case_name",
                    lambda: "_".join(i.lower() for i in parts),
                ),
                (f"{variable}.name", lambda: self.domain),
            ],
            bracketed,
        )

    def loop_targets(
        self, variable: str
    ) -> typing.Dict[str, typing.Generator[Substitutor, None, None]]:
        """Get list of loop targets."""
        return {}
