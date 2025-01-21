# C++ library

The source code of the quadraturerules C library can be downloaded from the
[latest release on GitHub](https://github.com/quadraturerules/quadraturerules/releases/latest/).
It can be built by running:

```bash
wget https://github.com/quadraturerules/quadraturerules/releases/download/{{VERSION}}/quadraturerules-c-{{VERSION}}.tar.gz
mkdir src
tar -xvf quadraturerules-c-{{VERSION}}.tar.gz -C src
cd src
gcc -c -Wall -Werror -fpic quadraturerules.c
gcc -shared -o libquadraturerules.so quadraturerules.o
```

Once the library is build, you can run the tests by running:

```bash
cd src/test
gcc -L.. -Wall -o test test.c -lquadraturerules
./test
```

## Usage

The library's function `single_integral_quadrature` can be used to write the points and weights
of quadrature rules for a single integral into memory. The functions `quadrature_npoints` and
`barycentric_dim` can be used to compute how large the arrays of doubles for the points and weights
need to be. For example the following snippet will create an order 3 Xiao--Gimbutas rule on a
triangle:

```cpp
#include "quadraturerules.h"

int npts = quadrature_npoints(QR_XiaoGimbutas, QR_Triangle, 3);
int ptdim = barycentric_dim(QR_Triangle);

double pts[npts * ptdim];
double wts[npts];

single_integral_quadrature(QR_XiaoGimbutas, QR_Triangle, 3, pts, wts);
```

Note that the points returned by the library are represented using
[barycentric coordinates](/barycentric.md).
