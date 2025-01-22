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

int single_integral_quadrature_points_size(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == single}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_points_size(domain, order);
  {{end if}}
  {{end for}}
  default:
    return -1;
  }
}

int single_integral_quadrature_weights_size(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_weights_size(domain, order);
  {{end for}}
  default:
    return -1;
  }
}

int double_integral_quadrature_first_points_size(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == double}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_first_points_size(domain, order);
  {{end if}}
  {{end for}}
  default:
    return -1;
  }
}

int double_integral_quadrature_second_points_size(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == double}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_second_points_size(domain, order);
  {{end if}}
  {{end for}}
  default:
    return -1;
  }
}

int double_integral_quadrature_weights_size(
    QuadratureRule rtype,
    Domain domain,
    int order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  case QR_{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}_weights_size(domain, order);
  {{end for}}
  default:
    return -1;
  }
}
