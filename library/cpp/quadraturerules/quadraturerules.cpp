/// Quadrature rules

#include <stdexcept>
#include "quadraturerules.h"
{{for Q in rules}}
#include "{{Q.snake_case_name}}.h"
{{end for}}

using namespace quadraturerules;

std::pair<std::vector<double>, std::vector<double>>
quadraturerules::single_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    std::size_t order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == single}}
  case QuadratureRule::{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}(domain, order);
  {{end if}}
  {{end for}}
  default:
    throw std::runtime_error("Unsupported rule for single integral");
  }
}

std::tuple<std::vector<double>, std::vector<double>, std::vector<double>>
quadraturerules::double_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    std::size_t order
)
{
  switch (rtype)
  {
  {{for Q in rules}}
  {{if Q.itype == double}}
  case QuadratureRule::{{Q.PascalCaseName}}:
    return {{Q.snake_case_name}}(domain, order);
  {{end if}}
  {{end for}}
  default:
    throw std::runtime_error("Unsupported rule for double integral");
  }
}
