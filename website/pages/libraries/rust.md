# Rust library

The quadraturerules Rust library is available on [crates.io](https://crates.io/crates/quadraturerules).
It can be installed by running:

```bash
cargo install quadraturerules
```

To use the latest version of quadraturerules in your crate, add the following to the
`[dependencies]` section of your Cargo.toml file:

```toml
quadraturerules = "{{VERSION}}"
```

## Usage

The library's function `single_integral_quadrature` can be used to get the points and weights
of quadrature rules for a single integral. For example the following snippet will create an
order 3 Xiao--Gimbutas rule on a triangle:

```rust
use quadraturerules::{Domain, QuadratureRule, single_integral_quadrature};

let (points, weights) = single_integral_quadrature(
    QuadratureRule::XiaoGimbutas,
    Domain::Triangle,
    3,
).unwrap();
```

Note that the points returned by the library are represented using
[barycentric coordinates](/barycentric.md).
