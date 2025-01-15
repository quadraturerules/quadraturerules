#include <quadraturerules/quadraturerules.h>
#include <cassert>

using namespace quadraturerules;

int main() {
  for (std::size_t order = 1; order <= 5; ++order)
  {
    auto [pts, wts] = single_integral_quadrature(
        QuadratureRule::GaussLegendre, Domain::Interval, order);
    double sum = 0.0;
    for (std::size_t i = 0; i < wts.size(); ++i)
      sum += wts[i];
    assert(abs(sum - 1.0) < 1e-7);
  }
}
