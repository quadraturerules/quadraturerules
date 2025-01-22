# Quadrature rules

[The online encylopedia of quadrature rules](https://quadraturerules.org) is a reference website that lists a number of quadrature rules.

Quadrature rules are sets of points and weights that are used to approximate integrals. If $\{p_0,\dots,p_{n-1}\}\subset\mathbb{R}^d$ and $\{w_0,\dots,w_{n-1}\}\subset\mathbb{R}$
are the points and weights (repectively) of the quadrature rule for a single integral, then:

$$\int f(x)\,\mathrm{d}x \approx \sum_{i=0}^{n-1}f(p_i)w_i$$

## Libraries

All of the quadrature rules included in the online encylopedia of quadrature rules are included in the quadraturerules library, which is available in the following languages:

- [Python](website/pages/libraries/python.md)
- [Rust](website/pages/libraries/rust.md)
- [C++](website/pages/libraries/cpp.md)
- [C](website/pages/libraries/c.md)
