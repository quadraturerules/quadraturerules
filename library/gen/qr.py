"""Quadrature rule specifics."""

import re
import typing

from gen.substitute import Substitutor
from gen.nodes import Node


def replace(content, subs):
    """Make multiple replacements."""
    for a, b in subs:
        content = content.replace(f"{{{{{a}}}}}", b)
    return content


class RuleFamily(Substitutor):
    """Substitutor for a rule family."""

    def __init__(self, family):
        self.family = family

    def substitute(self, code: str, variable: str) -> str:
        """Substitute."""
        return replace(code, [
            [f"{variable}.code", f"{self.family.code}"],
            [f"{variable}.index", f"{self.family.index}"],
            [f"{variable}.itype", self.family.itype],
            [f"{variable}.name", self.family.name()],
            [f"{variable}.PascalCaseName", self.family.name("PascalCase")],
            [f"{variable}.camelCaseName", self.family.name("camelCase")],
            [f"{variable}.snake_case_name", self.family.name("snake_case")],
        ])

    def loop_targets(self, variable: str) -> typing.Dict[str, typing.List[Substitutor]]:
        """Get list of loop targets."""
        return {f"{variable}.rules": [Rule(r) for r in self.family.rules]}


class Rule(Substitutor):
    """Substitutor for a rule."""

    def __init__(self, rule):
        self.rule = rule

    def substitute(self, code: str, variable: str) -> str:
        """Substitute."""
        subs = [
            [f"{variable}.order", f"{self.rule.order}"],
            [f"{variable}.domain", self.rule.domain],
        ]
        for open, close, name in [
            ("[", "]", "list"),
            ("{", "}", "curly_list"),
        ]:
            if isinstance(rule, rules.QRuleSingle):
                subs += [
                    [f"{variable}.first_points_as_{name}", "<<ERROR>>"],
                    [f"{variable}.first_points_as_flat_{name}", "<<ERROR>>"],
                    [f"{variable}.second_points_as_{name}", "<<ERROR>>"],
                    [f"{variable}.second_points_as_flat_{name}", "<<ERROR>>"],
                    [f"{variable}.points_as_{name}", open + ", ".join(
                        [open + ", ".join([f"{c}" for c in p]) + close for p in self.rule.points]) + close],
                    [f"{variable}.points_as_flat_{name}", open + ", ".join([
                        f"{c}" for p in self.rule.points for c in p]) + close],
                    [f"{variable}.weights_as_{name}", open + ", ".join([
                        f"{w}" for w in self.rule.weights]) + close],
                ]
            elif isinstance(rule, rules.QRuleDouble):
                subs += [
                    [f"{variable}.points_as_{name}", "<<ERROR>>"],
                    [f"{variable}.points_as_flat_{name}", "<<ERROR>>"],
                    [f"{variable}.first_points_as_{name}", open + ", ".join(
                        [open + ", ".join([f"{c}" for c in p]) + close for p in self.rule.first_points]
                    ) + close],
                    [f"{variable}.first_points_as_flat_{name}", open + ", ".join([
                        f"{c}" for p in self.rule.first_points for c in p]) + close],
                    [f"{variable}.second_points_as_{name}", open + ", ".join(
                        [open + ", ".join([f"{c}" for c in p]) + close for p in self.rule.second_points]
                    ) + close],
                    [f"{variable}.second_points_as_flat_{name}", open + ", ".join([
                        f"{c}" for p in self.rule.second_points for c in p]) + close],
                    [f"{variable}.weights_as_{name}", open + ", ".join([
                        f"{w}" for w in self.rule.weights]) + close],
                ]
        return replace(code, subs)

    def loop_targets(self, variable: str) -> typing.Dict[str, typing.List[Substitutor]]:
        """Get list of loop targets."""
        return {}


class Domain(Substitutor):
    """Substitutor for a domain."""

    def __init__(self, domain, index):
        self.domain = domain
        self.index = index

    def substitute(self, code: str, variable: str) -> str:
        """Substitute."""
        parts = re.split(r"--|\s|-", self.domain)
        return replace(code, [
            [f"{variable}.index", f"{self.index}"],
            [f"{variable}.PascalCaseName", "".join(i[0].upper() + i[1:].lower() for i in parts)],
            [f"{variable}.camelCaseName", parts[0].lower() + "".join(
                i[0].upper() + i[1:].lower() for i in parts[1:])],
            [f"{variable}.snake_case_name", "_".join(i.lower() for i in parts)],
            [f"{variable}.name", self.domain],
        ])

    def loop_targets(self, variable: str) -> typing.Dict[str, typing.List[Substitutor]]:
        """Get list of loop targets."""
        return {}
