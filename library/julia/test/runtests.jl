using QuadratureRulesDotOrg
using Test

@testset "QuadratureRulesDotOrg.jl" begin
    points, weights = QuadratureRulesDotOrg.single_integral_quadrature(
        QuadratureRulesDotOrg.QR_GaussLobattoLegendre,
        QuadratureRulesDotOrg.Domain_Interval,
        4
    )
    @test isapprox(sum(weights), 1.0)
end
