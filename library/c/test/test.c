#include <assert.h>
#include <math.h>
#include "../quadraturerules.h"

int main()
{
    int pts_size = single_integral_quadrature_points_size(QR_GaussLegendre, QR_Interval, 3);
    int wts_size = single_integral_quadrature_weights_size(QR_GaussLegendre, QR_Interval, 3);

    double pts[pts_size];
    double wts[wts_size];

    single_integral_quadrature(QR_GaussLegendre, QR_Interval, 3, pts, wts);

    double sum = 0.0;
    for (int i=0; i<pts_size; ++i)
      sum += wts[i];

    assert(fabs(1.0 - sum) < 1e-8);

    return 0;
}
