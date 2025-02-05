{{for Q in rules}}
include "{{Q.snake_case_name}}.f90"
{{end for}}

module quadraturerules
  implicit none

  public single_integral_quadrature
  {{for D in domains}}
  public QR_{{D.PascalCaseName}}
  {{end for}}
  {{for R in rules}}
  public QR_{{R.PascalCaseName}}
  {{end for}}
  enum, bind(C)
    {{for D in domains}}
    enumerator :: QR_{{D.PascalCaseName}} = {{D.index}}
    {{end for}}
  end enum
  enum, bind(C)
    {{for R in rules}}
    enumerator :: QR_{{R.PascalCaseName}} = {{R.index}}
    {{end for}}
  end enum

contains

  subroutine single_integral_quadrature(rtype, domain, order, points, weights)
    {{for Q in rules}}
    use {{Q.snake_case_name}}
    {{end for}}
    implicit none
    integer, value :: rtype
    integer, value :: domain
    integer, value :: order
    real, allocatable, intent(out) :: points(:,:)    
    real, allocatable, intent(out) :: weights(:)

    {{for Q in rules}}
    {{for D in domains}}
    {{if Q.itype == single}}
    if (rtype == QR_{{Q.PascalCaseName}} .and. domain == QR_{{D.PascalCaseName}}) then
      call {{Q.abbrv_name}}_{{D.abbrv_name}}(order, points, weights)
    end if
    {{end if}}
    {{end for}}
    {{end for}}
  end subroutine

end module quadraturerules
