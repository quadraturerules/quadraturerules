"""Definitions of quadrature rules."""
{{for Q in rules}}
from quadraturerules.rules.{{Q.snake_case_name}} import {{Q.snake_case_name}}
{{end for}}
