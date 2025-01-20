# C++ library

The source code of the quadraturerules C++ library can be downloaded from the
[latest release on GitHub](https://github.com/quadraturerules/quadraturerules/releases/latest/).
It can be installed by running:

```bash
wget https://github.com/quadraturerules/quadraturerules/releases/download/{{VERSION}}/cpp_source.tar.gz
mkdir src
tar -xvf cpp_source.tar.gz -C src
mkdir build
cd build
cmake ../src
make
make install
```

Once the library is installed, you can run the tests by running:

```bash
python src/test/run_tests.py
```

Or you can run individual tests:

```bash
cd src/test/{TEST_NAME}
cmake .
make .
./{TEST_NAME}
```

## Usage

The library's function `single_integral_quadrature` can be used to get the points and weights
of quadrature rules for a single integral. For example the following snippet will create an
order 3 Xiao--Gimbutas rule on a triangle:

```cpp
#include <quadraturerules.h>

using quadraturerules

auto [points, weights] = single_integral_quadrature(
    QuadratureRule::XiaoGimbutas,
    Domain::Triangle,
    3,
);
```

Note that the points return by the library are represented using
[barycentric coordinates](/barycentric.md).
