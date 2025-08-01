//! Quadrature rules
#![cfg_attr(feature = "strict", deny(warnings), deny(unused_crate_dependencies))]
#![warn(missing_docs)]

mod rules;

/// A domain of an integral.
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[derive(Debug, PartialEq, Eq, Clone, Copy, Hash)]
#[repr(u8)]
pub enum Domain {
    {{for D in domains}}
    /// {{D.name}}
    {{D.PascalCaseName}} = {{D.index}},
    {{end for}}
}

/// A quadrature rule family.
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[derive(Debug, PartialEq, Eq, Clone, Copy, Hash)]
#[repr(u8)]
pub enum QuadratureRule {
    {{for Q in rules}}
    /// {{Q.name}}
    {{Q.PascalCaseName}} = {{Q.index}},
    {{end for}}
}

/// Get a quadrature rule for a single integral.
pub fn single_integral_quadrature(
    rtype: QuadratureRule,
    domain: Domain,
    order: usize,
) -> Result<(Vec<f64>, Vec<f64>), &'static str> {
    match rtype {
        {{for Q in rules}}
        {{if Q.itype == single}}
        QuadratureRule::{{Q.PascalCaseName}} => rules::{{Q.snake_case_name}}(domain, order),
        {{end if}}
        {{end for}}
        _ => Err(format!("Unsupported rule for single integral: {rtype}")),
    }
}

/// Get a quadrature rule for a double integral.
pub fn double_integral_quadrature(
    rtype: QuadratureRule,
    domain: Domain,
    order: usize,
) -> Result<(Vec<f64>, Vec<f64>, Vec<f64>), &'static str> {
    match rtype {
        {{for Q in rules}}
        {{if Q.itype == double}}
        QuadratureRule::{{Q.PascalCaseName}} => rules::{{Q.snake_case_name}}(domain, order),
        {{end if}}
        {{end for}}
        _ => Err(format!("Unsupported rule for single integral: {rtype}")),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use approx::*;

    #[test]
    fn test_sum_weights_1() {
        let weights = single_integral_quadrature(QuadratureRule::GaussLegendre, Domain::Interval, 1).unwrap().1;
        assert_relative_eq!(weights.iter().sum::<f64>(), 1.0);
    }

    #[test]
    fn test_sum_weights_2() {
        let weights = single_integral_quadrature(QuadratureRule::GaussLegendre, Domain::Interval, 2).unwrap().1;
        assert_relative_eq!(weights.iter().sum::<f64>(), 1.0);
    }

    #[test]
    fn test_sum_weights_3() {
        let weights = single_integral_quadrature(QuadratureRule::GaussLegendre, Domain::Interval, 3).unwrap().1;
        assert_relative_eq!(weights.iter().sum::<f64>(), 1.0);
    }
}
