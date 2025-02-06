      INCLUDE "quadraturerules.f"

      PROGRAM test
      REAL p,w
      DIMENSION p(0:2, 0:5)
      DIMENSION w(0:5)

      CALL siquad(1, 0, 5, p, w, 5, 2)

      sumto = 0
      DO i = 0, 4
      sumto = sumto + w(i)
      END DO

      IF (abs(1 - sumto) .LT. 0.00000001) THEN
      PRINT *, "Test passed"
      ELSE
      PRINT *, "Test failed"
      END IF
      END
