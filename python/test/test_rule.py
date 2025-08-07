import re
import os

import numpy as np
import pytest
import sympy
import yaml
from webtools.tools import join

x = [
    sympy.Symbol("x"),
    sympy.Symbol("y"),
    sympy.Symbol("z"),
]


folder = join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "..",
    "rules",
)
rules = []
for file in os.listdir(folder):
    if not file.startswith(".") and file.endswith(".qr"):
        assert os.path.isfile(os.path.join(folder, file))
        family = file[:-3]
        for rule in os.listdir(join(folder, family)):
            if not rule.startswith("."):
                rules.append((family, rule))


@pytest.mark.parametrize(("family", "rule"), rules)
def test_cell_has_unit_volume(family, rule):
    with open(join(folder, f"{family}.qr")) as f:
        info = yaml.load(f, yaml.FullLoader)
    if info["integrand"] != "f(x)":
        pytest.xfail()

    with open(join(folder, family, rule)) as f:
        volume = sum(float(p.split(" | ")[1]) for p in f.read().split("--")[2].strip().split("\n"))
    assert np.isclose(volume, 1.0)


@pytest.mark.parametrize(("family", "rule"), rules)
def test_barycentric_coordinates(family, rule):
    with open(join(folder, f"{family}.qr")) as f:
        info = yaml.load(f, yaml.FullLoader)
    if info["integrand"] != "f(x)":
        pytest.xfail()

    with open(join(folder, family, rule)) as f:
        for line in f.read().split("--\n")[2].strip().split("\n"):
            p = [float(i) for i in line.split(" | ")[0].split(" ")]
            assert np.isclose(sum(p), 1.0)


@pytest.mark.parametrize(("family", "rule"), rules)
def test_no_standard_form(family, rule):
    with open(join(folder, family, rule)) as f:
        for p in f.read().split("--")[2].strip().split("\n"):
            assert "e" not in p


def sympy_parse(f):
    f = re.sub(r"([0-9])n", r"\1*n", f)
    return sympy.S(f)


def functions(e, degree, domain):
    match e["type"]:
        case "polynomial":
            d = int(sympy_parse(e["degree"]).subs(sympy.Symbol("n"), degree))
            if domain in ["interval"]:
                return [x[0] ** d]
            elif domain in ["triangle", "quadrilateral"]:
                return [x[0] ** (d - i) * x[1] ** i for i in range(d + 1)]
            elif domain in ["tetrahedron", "hexahedron"]:
                return [
                    x[0] ** (d - i - j) * x[1] ** i * x[2] ** j
                    for i in range(d + 1)
                    for j in range(d + 1 - i)
                ]
            else:
                raise ValueError(f"Unsupported domain: {domain}")
        case _:
            raise ValueError(f"Unsupported function type: {e['type']}")


def integral(f, domain):
    match domain:
        case "interval":
            return float(f.integrate((x[0], 0, 1)))
        case "triangle":
            return float(f.integrate((x[0], 0, 1 - x[1]), (x[1], 0, 1)))
        case "quadrilateral":
            return float(f.integrate((x[0], 0, 1), (x[1], 0, 1)))
        case "tetrahedron":
            return float(f.integrate((x[0], 0, 1 - x[1] - x[2]), (x[1], 0, 1 - x[2]), (x[2], 0, 1)))
        case "hexahedron":
            return float(f.integrate((x[0], 0, 1), (x[1], 0, 1), (x[2], 0, 1)))
        case _:
            raise ValueError(f"Unsupported domain: {domain}")


def subs(f, values):
    out = 1 * f
    for i, j in zip(x, values):
        out = out.subs(i, j)
    return float(out)


@pytest.mark.parametrize(("family", "rule"), rules)
def test_exact(family, rule):
    with open(join(folder, f"{family}.qr")) as f:
        family_info = yaml.load(f, yaml.FullLoader)
    if "exact" not in family_info:
        pytest.skip()

    with open(join(folder, family, rule)) as f:
        _, yaml_data, rule = f.read().split("--\n")
    info = yaml.load(yaml_data, yaml.FullLoader)
    pts = []
    wts = []
    for line in rule.strip().split("\n"):
        p, w = line.split(" | ")
        pts.append([float(i) for i in p.split(" ")])
        wts.append(float(w))

    match info["domain"]:
        case "interval":
            mapped_pts = [i[1:] for i in pts]
            volume = 1
        case "triangle":
            mapped_pts = [i[1:] for i in pts]
            volume = 0.5
        case "quadrilateral":
            mapped_pts = [[i[1], i[2]] for i in pts]
            volume = 1
        case "tetrahedron":
            mapped_pts = [i[1:] for i in pts]
            volume = 1 / 6
        case "hexahedron":
            mapped_pts = [[i[1], i[2], i[4]] for i in pts]
            volume = 1
        case _:
            raise ValueError(f"Unsupported domain: {info['domain']}")

    for e in family_info["exact"]:
        for f in functions(e, int(info["order"]), info["domain"]):
            assert np.isclose(
                integral(f, info["domain"]),
                volume * sum(w * subs(f, p) for p, w in zip(mapped_pts, wts)),
            )
