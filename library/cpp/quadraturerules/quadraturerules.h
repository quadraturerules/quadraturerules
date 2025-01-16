/// Quadrature rules

#pragma once

#include <utility>
#include <vector>

namespace quadraturerules {

/// A domain of an integral.
enum class Domain : int
{
  {{for D in domains}}
  {{D.PascalCaseName}} = {{D.index}},
  {{end for}}
};

/// A quadrature rule family.
enum class QuadratureRule {
  {{for Q in rules}}
  {{Q.PascalCaseName}} = {{Q.index}},
  {{end for}}
};

/// Get a quadrature rule for a single integral.
std::pair<std::vector<double>, std::vector<double>>
single_integral_quadrature(
    QuadratureRule rtype,
    Domain domain,
    std::size_t order
);

} // namespace quadraturerules
