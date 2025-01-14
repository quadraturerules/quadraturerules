//! Definitions of quadrature rules.
{{for Q in rules}}
mod {{Q.snake_case_name}};

{{end for}}
{{for Q in rules}}
pub use {{Q.snake_case_name}}::{{Q.snake_case_name}};
{{end for}}
