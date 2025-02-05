module TabulatedQuadratureRules

include("domains.jl")
{{for Q in rules}}
include("{{Q.snake_case_name}}.jl")
{{end for}}

@enum QuadratureRule begin
    {{for Q in rules}}
    QR_{{Q.PascalCaseName}} = {{Q.index}}
    {{end for}}
end

"Get a quadrature rule for a single integral."
function single_integral_quadrature(
    rtype::QuadratureRule,
    domain::Domain,
    order::Integer,
)
    {{for Q in rules}}
    {{if Q.itype == single}}
    if rtype == QR_{{Q.PascalCaseName}}
        return {{Q.snake_case_name}}(domain, order)
    end
    {{end if}}
    {{end for}}
    throw("Unsupported rule for single integral: $rtype")
end

"Get a quadrature rule for a double integral."
function double_integral_quadrature(
    rtype::QuadratureRule,
    domain::Domain,
    order::Integer,
)
    {{for Q in rules}}
    {{if Q.itype == double}}
    if rtype == QR_{{Q.PascalCaseName}}
        return {{Q.snake_case_name}}(domain, order)
    end
    {{end if}}
    {{end for}}
    throw("Unsupported rule for single integral: $rtype")
end

export QuadratureRule
export Domain
export single_integral_quadrature

end
