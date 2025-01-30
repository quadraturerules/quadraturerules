# Quadrature rules

[The online encylopedia of quadrature rules](https://quadraturerules.org) is a reference website that lists a number of quadrature rules.

Quadrature rules are sets of points and weights that are used to approximate integrals. If $\{p_0,\dots,p_{n-1}\}\subset\mathbb{R}^d$ and $\{w_0,\dots,w_{n-1}\}\subset\mathbb{R}$
are the points and weights (repectively) of the quadrature rule for a single integral, then:

$$\int f(x)\,\mathrm{d}x \approx \sum_{i=0}^{n-1}f(p_i)w_i$$

## Website

Before building the online encylopedia of quadrature rules, you must first install qrtools
from the [python](python) directory:
```bash
cd python
python3 -m pip install .
```

The online encylopedia of quadrature rules website can then be built by running:

```bash
cd website
python3 build.py
```
## Libraries

All of the quadrature rules included in the online encylopedia of quadrature rules are included in the quadraturerules library, which is available in the following languages:

| Language                                     | Badges |
| -------------------------------------------- | ------ |
| [Python](website/pages/libraries/python.md)  | [![Test and build Python library](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-python.yml/badge.svg)](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-python.yml) [![PyPI](https://img.shields.io/pypi/v/quadraturerules?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/quadraturerules/) |
| [Rust](website/pages/libraries/rust.md)      | [![Test and build Rust library](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-rust.yml/badge.svg)](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-rust.yml) [![crates.io](https://img.shields.io/crates/v/quadraturerules?color=blue&logo=Rust&logoColor=white)](https://crates.io/crates/quadraturerules/) [![docs.rs](https://img.shields.io/docsrs/quadraturerules?logo=Docs.rs&logoColor=white)](https://docs.rs/quadraturerules/) |
| [C++](website/pages/libraries/cpp.md)        | [![Test and build C++ library](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-cpp.yml/badge.svg)](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-cpp.yml) |
| [C](website/pages/libraries/c.md)            | [![Test and build C library](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-c.yml/badge.svg)](https://github.com/quadraturerules/quadraturerules/actions/workflows/library-c.yml) |

Before building any of the libraries, you must first install qrtools
from the [python](python) directory:
```bash
cd python
python3 -m pip install .
```

You can then build the libraries using the [build.py](library/build.py) script in the library directory.
For example, to build the python library, you can run:

```bash
cd library
python build.py python
```

and to build the rust library, you can run:

```bash
cd library
python build.py rust
```
