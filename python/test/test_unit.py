import os

import numpy as np
import pytest
import yaml
from webtools.tools import join

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
