# Julia library

The QuadratureRulesDotOrg Julia library is available at [github.com/quadraturerules/QuadratureRulesDotOrg.jl](https://github.com/quadraturerules/QuadratureRulesDotOrg.jl).

## Usage

The library's function `single_integral_quadrature` can be used to get the points and weights
of quadrature rules for a single integral. For example the following snippet will create an
order 3 Xiao--Gimbutas rule on a triangle:

```rust
using QuadratureRulesDotOrg

points, weights = QuadratureRulesDotOrg.single_integral_quadrature(
    QuadratureRulesDotOrg.QR_XiaoGimbutas,
    QuadratureRulesDotOrg.Domain_Triangle,
    3,
)
```

Note that the points returned by the library are represented using
[barycentric coordinates](/barycentric.md).

## Generating the library
The Julia quadraturerules library can be generated from the templates in the online encyclopedia
of quadrature rules GitHub repo. First clone the repo and move into the library directory:

```bash
git clone https://github.com/quadraturerules/quadraturerules.git
cd quadraturerules/library
```

The Julia library can then be generated by running:

```bash
python build.py julia
```

This will create a directory called julia.build containing the Rust source code.
