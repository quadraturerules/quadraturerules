#include "quadraturerules.h"
{{for Q in rules}}
#include "{{Q.snake_case_name}}.c"
{{end for}}

int single_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    int order,
    double* points,
    double* weights
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == single}}
  case QR_{{Q.PascalCaseName}}:
    {{Q.snake_case_name}}(domain, order, points, weights);
    return 0;
  {{end if}}
  {{end for}}
  default:
    return 1;
  }
}

int double_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    int order,
    double* first_points,
    double* second_points,
    double* weights
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == double}}
  case QR_{{Q.PascalCaseName}}:
    {{Q.snake_case_name}}(domain, order, first_points, second_points, weights);
    return 0;
  {{end if}}
  {{end for}}
  default:
    return 1;
  }
}

int quadrature_npoints(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_npoints(domain, order);
  {{end for}}
  default:
    return -1;
  }
}

int barycentric_dim(
    Domain domain
){
  switch (domain)
  {
  {{for D in domains}}
  case QR_{{D.PascalCaseName}}:
    return {{D.nvertices}};
  {{end for}}
  default:
    return -1;
  }
}
