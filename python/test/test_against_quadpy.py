import numpy as np
import os
import pytest
import yaml
from webtools.tools import join

import quadpy

folder = join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "..",
    "rules",
)

qpy_map = {
    "Q000001": {"interval": quadpy.c1.gauss_legendre},
    "Q000002": {
        "triangle": lambda order: quadpy.t2.schemes["xiao_gimbutas_" + f"00{order}"[-2:]](),
        "tetrahedron": lambda order: quadpy.t3.schemes["xiao_gimbutas_" + f"00{order}"[-2:]](),
    },
    "Q000003": {"interval": quadpy.c1.gauss_lobatto},
    "Q000004": None,
    "Q000005": None,
    "Q000006": {
        "triangle": lambda order: quadpy.t2.schemes[f"hammer_marlowe_stroud_{order}"](),
        "tetrahedron": lambda order: quadpy.t3.schemes[f"hammer_marlowe_stroud_{order}"](),
    },
    "Q000007": None,
}


@pytest.mark.parametrize(
    ("qfolder", "qfile"),
    [
        (qfolder, qfile)
        for qfolder in os.listdir(folder)
        if os.path.isdir(join(folder, qfolder))
        for qfile in os.listdir(join(folder, qfolder))
        if qfile.endswith(".rule") and qpy_map[qfile[:-5]] is not None
    ],
)
def test_against_quadpy(qfolder, qfile):
    qpy_function = qpy_map[qfolder]

    with open(join(folder, qfolder, qfile)) as f:
        _, yaml_data, rule = f.read().split("--\n")
    info = yaml.load(yaml_data, yaml.FullLoader)

    qpy_scheme = qpy_function[info["domain"]](info["order"])

    pts = []
    wts = []
    for line in rule.strip().split("\n"):
        p, w = line.split(" | ")
        pts.append([float(i) for i in p.split(" ")])
        wts.append(float(w))

    match info["domain"]:
        case "interval":
            mapped_pts = [p[0] - p[1] for p in pts]
            volume = 2
        case "triangle":
            mapped_pts = pts
            volume = 1
        case "tetrahedron":
            mapped_pts = pts
            volume = 1
        case _:
            raise NotImplementedError()

    order = []
    for p in mapped_pts:
        for i, q in enumerate(qpy_scheme.points.T):
            if np.allclose(p, q):
                order.append(i)
                break
        else:
            raise ValueError("Points do not match")
    for i, j in enumerate(order):
        assert np.isclose(wts[i] * volume, qpy_scheme.weights[j]), "Weights do not match"
