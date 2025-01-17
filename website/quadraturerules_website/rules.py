"""Quadrature rules."""

import math
import os
import re
import typing

import yaml
from quadraturerules_website import settings
from webtools.citations import make_bibtex, markup_citation
from webtools.tools import html_local

PointND = typing.Tuple[float, ...]
Point2D = typing.Tuple[float, float]


def dim(domain: str | None) -> int:
    """Get the dimension of a domain."""
    if domain is None:
        return -1
    if domain == "point":
        return 0
    if domain == "interval":
        return 1
    if domain in ["triangle", "quadrilateral", "circle"]:
        return 2
    if "agon" in domain:
        return 2
    if domain in ["prism", "pyramid", "wedge"]:
        return 3
    if "ahedron" in domain:
        return 3
    return 10


def to_html(content: str) -> str:
    """Convert to HTML."""
    content = content.replace("--", "&ndash;")
    return content


def to_2d(point: PointND, origin: Point2D, axes: typing.List[Point2D]) -> Point2D:
    """Map a point on a domain to a 2D point in an SVG."""
    return (
        origin[0] + sum(a[0] * p for a, p in zip(axes, point)),
        origin[1] + sum(a[1] * p for a, p in zip(axes, point)),
    )


def from_barycentric(point: PointND, domain: typing.List[PointND]) -> PointND:
    """Map from barycentric coordinates to a point on a domain."""
    return tuple(
        sum(p * d[i] for p, d in zip(point, domain))
        for i in range(len(domain[0]))
    )


class QRule:
    """A quadrature rule."""

    def __init__(
        self,
        domain: typing.Optional[str],
        order: typing.Optional[int],
        points: typing.List[typing.List[float]],
        weights: typing.List[float],
        itype: str,
        rule: str,
    ):
        """Create."""
        self.domain = domain
        self.order = order
        self.points = points
        self.weights = weights
        self.itype = itype
        self._rule = rule
        self.family: typing.Optional[QRuleFamily] = None

    def title(self, format: str = "default") -> str:
        """Get title."""
        match format:
            case "default":
                return f"{self.domain} {self.order}"
            case "HTML":
                out = ""
                if self.order is not None:
                    out += f"Order {self.order}"
                if self.domain is not None:
                    if out == "":
                        out += f"{self.domain[0].upper()}{self.domain[1:]}"
                    else:
                        out += " on a"
                        if self.domain[0] in "aeiou":
                            out += "n"
                        out += f" {self.domain}"
                return out
            case "filename":
                out = ""
                if self.domain is not None:
                    out += self.domain.replace(" ", "-")
                if self.order is not None:
                    if out == "":
                        out += "-"
                    out += f"{self.order}"
                return out
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def image(self, filename: str) -> str:
        """Make image of rule."""
        match filename.split(".")[-1]:
            case "svg":
                with open(filename, "w") as f:
                    match self.domain:
                        case "interval":
                            size = (220, 20)
                            domain: typing.List[PointND] = [(0.0,), (1.0,)]
                            domain_lines = [[0, 1]]
                            origin = (10.0, 10.0)
                            axes = [(200.0, 0.0)]
                        case "triangle":
                            size = (220, 194)
                            domain = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
                            domain_lines = [[0, 1, 2, 0]]
                            origin = (10.0, 184.0)
                            axes = [(200.0, 0.0), (100.0, -100*math.sqrt(3))]
                        case "quadrilateral":
                            size = (220, 220)
                            domain = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
                            domain_lines = [[0, 1, 3, 2, 0]]
                            origin = (10.0, 210.0)
                            axes = [(200.0, 0.0), (0.0, -200.0)]
                        case "tetrahedron":
                            size = (205, 209)
                            domain = [
                                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
                            ]
                            domain_lines = [[0, 1, 2, 0], [0, 3, 1], [3, 2]]
                            origin = (10.0, 168.5)
                            axes = [(180.0, 30.0), (185.0, -45.5), (122.0, -158.5)]
                        case "hexahedron":
                            size = (223, 223)
                            domain = [
                                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0),
                                (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (1.0, 1.0, 1.0),
                            ]
                            domain_lines = [[0, 1, 3, 2, 0], [4, 5, 7, 6, 4],
                                            [0, 4], [1, 5], [2, 6], [3, 7]]
                            origin = (10.0, 192.0)
                            axes = [(126.0, 21.0), (77.0, -49.0), (0.0, -133.0)]
                        case "triangular prism":
                            size = (167, 213)
                            domain = [
                                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0),
                                (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0),
                            ]
                            domain_lines = [[0, 1, 2, 0], [3, 4, 5, 3], [0, 3], [1, 4], [2, 5]]
                            origin = (10.0, 182.0)
                            axes = [(126.0, 21.0), (129.5, -32.0), (0.0, -140.0)]
                        case "square-based pyramid":
                            size = (223, 164)
                            domain = [
                                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0),
                                (0.0, 0.0, 1.0),
                            ]
                            domain_lines = [[0, 1, 3, 2, 0], [0, 4, 1], [2, 4, 3]]
                            origin = (10.0, 133.0)
                            axes = [(126.0, 21.0), (77.0, -49.0), (101.5, -123.0)]
                        case _:
                            raise ValueError(f"Unsupported domain: {self.domain}")
                    f.write(f"<svg width='{size[0]}' height='{size[1]}' "
                            "xmlns='http://www.w3.org/2000/svg' "
                            "xmlns:xlink='http://www.w3.org/1999/xlink'>\n")
                    for lines in domain_lines:
                        for a_, b_ in zip(lines[:-1], lines[1:]):
                            a = to_2d(domain[a_], origin, axes)
                            b = to_2d(domain[b_], origin, axes)
                            f.write(f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' "
                                    "stroke='#000000' stroke-width='1.5' "
                                    "stroke-linecap='round' />\n")
                        for p_, w in zip(self.points, self.weights):
                            p = to_2d(from_barycentric(tuple(p_), domain), origin, axes)
                            if w > 0:
                                f.write(f"<circle cx='{p[0]}' cy='{p[1]}' r='{9 * w ** 0.5}' "
                                        "fill='red' />")
                            else:
                                f.write(f"<circle cx='{p[0]}' cy='{p[1]}' r='{9 * (-w) ** 0.5}' "
                                        "fill='blue' />")
                    f.write("</svg>")
            case _:
                raise ValueError(f"Unsupported format: {filename.split('.')[-1]}")
        return f"<img src='{html_local(filename)}'>"

    def save_html_table(self, filename):
        """Save HTML table of points and weights to a file."""
        assert filename.endswith(".html")
        filename_root = filename[:-5]
        filename_root_local = html_local(filename_root)

        assert self._rule.startswith("--\n")
        assert self.family._qr.endswith("\n")
        with open(f"{filename_root}.rule", "w") as f:
            f.write(f"--\n{self.family._qr}{self._rule[3:]}")

        with open(filename, "w") as f:
            f.write("<div class='small-note'>"
                    f"<a href='{filename_root_local}.rule'>&darr; Download as .rule</a></div>")
            if self.itype == "single":
                with open(f"{filename_root}.csv", "w") as f2:
                    f2.write(",".join([f"point[{i}]" for i, _ in enumerate(self.points[0])]))
                    f2.write(",weight\n")
                    for p, w in zip(self.points, self.weights):
                        f2.write(",".join(f"{i}" for i in p) + f",{w}\n")
                f.write("<div class='small-note'>"
                        f"<a href='{filename_root_local}.csv'>&darr; Download as CSV</a></div>")
                with open(f"{filename_root}.json", "w") as f2:
                    f2.write('{"points": [')
                    f2.write(", ".join("[" + ", ".join(
                        f"{i}" for i in p) + "]" for p in self.points))
                    f2.write('], "weights": [')
                    f2.write(", ".join(f"{w}" for w in self.weights))
                    f2.write(']}')
                f.write("<div class='small-note'>"
                        f"<a href='{filename_root_local}.json'>&darr; Download as JSON</a></div>")
            f.write("<br />\n")
            f.write("<table class='points'>\n")
            f.write("<thead>")
            f.write(f"<tr><td colspan='{len(self.points[0])}'>Point</td><td>Weight</td></tr>")
            f.write("</thead>\n")
            for p, w in zip(self.points, self.weights):
                f.write("<tr>")
                for i in p:
                    f.write(f"<td>{i}</td>")
                f.write(f"<td>{w}</td></tr>\n")
            f.write("</table>\n")
            f.write("<div class='small-note'>The points given above are represented using "
                    "<a href='/barycentric.html'>barycentric coordinates</a></div>\n")


class QRuleFamily:
    """A family of quadrature rules."""

    def __init__(
        self,
        code: str,
        name: str,
        alt_names: typing.List[str],
        itype: str,
        integrand: str,
        notes: typing.List[str],
        references: typing.List[typing.Dict[str, typing.Any]],
        rules: typing.List[QRule],
        qr: str,
    ):
        """Create."""
        assert re.match(r"Q[0-9]{6}", code)
        self.code = code
        self.index = int(code[1:])
        self._alt_names = alt_names
        self._name = name
        self.itype = itype
        self.integrand = integrand
        self._notes = notes
        self._references = references
        for r in rules:
            r.family = self
        self.rules = rules
        self._qr = qr

    @property
    def rules_by_domain(self) -> typing.Dict[str, typing.List[QRule]]:
        """Get the rules sorted by domain."""
        rules: typing.Dict[str, typing.List[QRule]] = {}
        for r in self.rules:
            assert r.domain is not None
            if r.domain not in rules:
                rules[r.domain] = []
            rules[r.domain].append(r)
        return rules

    def name(self, format: str = "default") -> str:
        """Get name."""
        parts = re.split(r"--|\s|-", self._name)
        match format:
            case "default":
                return self._name
            case "HTML":
                return to_html(self._name)
            case "PascalCase":
                return "".join([i[0].upper() + i[1:].lower() for i in parts])
            case "camelCase":
                return parts[0].lower() + "".join([i[0].upper() + i[1:].lower() for i in parts[1:]])
            case "snake_case":
                return "_".join([i.lower() for i in parts])
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def alt_names(self, format: str = "default") -> str:
        """Get alternative names."""
        match format:
            case "default":
                return "\n".join(self._alt_names)
            case "HTML":
                return "<br />".join([to_html(i) for i in self._alt_names])
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def integral(self, format: str = "LaTeX"):
        """Get integral."""
        match format:
            case "LaTeX":
                i = "\\(\\displaystyle "
                match self.itype:
                    case "single":
                        i += "\\int"
                    case _:
                        raise ValueError(f"Unsupported integral type: {self.itype}")
                i += f" {self.integrand}"
                match self.itype:
                    case "single":
                        i += "\\,\\mathrm{d}x"
                    case _:
                        raise ValueError(f"Unsupported integral type: {self.itype}")
                i += "\\)"
                return i
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def notes(self, format: str = "HTML"):
        """Get notes."""
        match format:
            case "HTML":
                return to_html("<br />".join(self._notes))
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def references(self, format: str = "HTML"):
        """Get references."""
        match format:
            case "HTML":
                return "<br />".join(
                    f"<div class='citation'>{to_html(markup_citation(r))}</div>"
                    for r in self._references
                )
            case "BibTeX":
                return "\n\n".join(
                    make_bibtex(f"{self.code}-{n + 1}", r)
                    for n, r in enumerate(self._references)
                ) + "\n"
            case _:
                raise ValueError(f"Unsupported format: {format}")

    @property
    def html_name(self) -> str:
        """HTML name."""
        return self.name("HTML")


def load_rule(code: str) -> QRuleFamily:
    """Load a rule from a file and folder."""
    with open(os.path.join(settings.rules_path, f"{code}.qr")) as f:
        qr = f.read()
    data = yaml.safe_load(qr)

    itype = data["integral-type"] if "integral-type" in data else "single"

    rules = []
    pt_dir = os.path.join(settings.rules_path, f"{code}")
    for pt_file in os.listdir(pt_dir):
        if pt_file.endswith(".rule"):
            with open(os.path.join(pt_dir, pt_file)) as f:
                content = f.read()
                if content.startswith("--\n"):
                    _, metadata_, rule_content = content.split("--", 3)
                    metadata = yaml.safe_load(metadata_)
                else:
                    metadata = {}
                points = []
                weights = []
                for line in rule_content.strip().split("\n"):
                    p, w = line.split("|")
                    points.append([float(i) for i in p.strip().split()])
                    weights.append(float(w))

                rules.append(QRule(
                    metadata.get("domain"),
                    metadata.get("order"),
                    points,
                    weights,
                    itype,
                    content,
                ))
    rules.sort(key=lambda r: (dim(r.domain), r.domain, r.order))

    r = QRuleFamily(
        code,
        data["name"],
        data["alt-names"] if "alt-names" in data else [],
        itype,
        data["integrand"],
        data["notes"] if "notes" in data else [],
        data["references"] if "references" in data else [],
        rules,
        qr,
    )
    return r
