using TabulatedQuadratureRules
using Test

@testset "TabulatedQuadratureRules.jl" begin
    points, weights = TabulatedQuadratureRules.single_integral_quadrature(
        TabulatedQuadratureRules.QR_GaussLobattoLegendre,
        TabulatedQuadratureRules.Domain_Interval,
        4
    )
    @test isapprox(sum(weights), 1.0)
end
