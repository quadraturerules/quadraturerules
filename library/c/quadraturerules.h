#ifndef QUADRATURERULES_H

#define QUADRATURERULES_H

/// A domain of an integral.
typedef enum
{
  {{for D in domains}}
  QR_{{D.PascalCaseName}} = {{D.index}},
  {{end for}}
} Domain;

/// A quadrature rule family.
typedef enum
{
  {{for Q in rules}}
  QR_{{Q.PascalCaseName}} = {{Q.index}},
  {{end for}}
} QuadratureRule;

/// Get a quadrature rule for a single integral.
extern int single_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    int order,
    double* points,
    double* weights
);

/// Get a quadrature rule for a single integral.
extern int double_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    int order,
    double* first_points,
    double* second_points,
    double* weights
);

/// Get the number of points for a quadrature rule.
extern int quadrature_npoints(
    QuadratureRule rtype,
    Domain domain,
    int order
);

/// Get the barycentric dimension of a domain
extern int barycentric_dim(
    Domain domain
);

#endif // QUADRATURERULES_H
