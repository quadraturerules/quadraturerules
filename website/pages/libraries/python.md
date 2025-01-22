# Python library

The quadraturerules Python library is available on [PyPI](https://pypi.org/project/quadraturerules/).
It can be installed by running:

```bash
python -m pip install quadraturerules
```

## Usage

The library's function `single_integral_quadrature` can be used to get the points and weights
of quadrature rules for a single integral. For example the following snippet will create an
order 3 Xiao--Gimbutas rule on a triangle:

```python
from quadraturerules import Domain, QuadratureRule, single_integral_quadrature

points, weights = single_integral_quadrature(
    QuadratureRule.XiaoGimbutas,
    Domain.Triangle,
    3,
)
```

Note that the points returned by the library are represented using
[barycentric coordinates](/barycentric.md).
