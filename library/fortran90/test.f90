include "quadraturerules.f90"

program test
  use quadraturerules
  real, allocatable :: points(:,:), weights(:)

  call single_integral_quadrature(QR_GaussLegendre, QR_Interval, 5, points, weights)

  sum = 0
  do i = 0, 4
    sum = sum + weights(i)
  end do

  if (abs(1 - sum) < 1e-8) then
    print *, "Test passed"
  else
    print *, "Test failed"
  end if
end program test
