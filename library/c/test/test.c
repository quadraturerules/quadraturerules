#include <assert.h>
#include <math.h>
#include "../quadraturerules.h"

int main()
{
    int npts = quadrature_npoints(QR_GaussLegendre, QR_Interval, 3);
    int ptdim = barycentric_dim(QR_Interval);

    double pts[npts * ptdim];
    double wts[npts];

    single_integral_quadrature(QR_GaussLegendre, QR_Interval, 3, pts, wts);

    double sum = 0.0;
    for (int i=0; i<npts; ++i)
      sum += wts[i];

    assert(fabs(1.0 - sum) < 1e-8);

    return 0;
}
