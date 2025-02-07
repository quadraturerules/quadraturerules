      {{for Q in rules}}
      INCLUDE "{{Q.snake_case_name}}.f"
      {{end for}}

c Gets a quadrature rule for a single integral
c
c rtype input:
{{for Q in rules}}
{{if Q.itype == single}}
c   {{Q.index}} = {{Q.name}}
{{end if}}
{{end for}}
c
c dtype input:
{{for D in domains}}
c   {{D.index}} = {{D.name}}
{{end for}}
      SUBROUTINE siquad(rtype, dtype, order, pts, wts, npts, ptdim)
      INTEGER rtype
      INTEGER dtype
      INTEGER order
      INTEGER ptdim
      INTEGER npts
      REAL pts
      DIMENSION pts(0:ptdim, 0:npts)
      REAL wts
      DIMENSION wts(0:npts)

      {{for Q in rules}}
      {{if Q.itype == single}}
      IF (rtype == {{Q.index}}) THEN
      CALL {{Q.abbrv_name}}(dtype, order, pts, wts, npts, ptdim)
      END IF
      {{end if}}
      {{end for}}
      END

c Gets a quadrature rule for a double integral
c
c rtype input:
{{for Q in rules}}
{{if Q.itype == double}}
c   {{Q.index}} = {{Q.name}}
{{end if}}
{{end for}}
c
c dtype input:
{{for D in domains}}
c   {{D.index}} = {{D.name}}
{{end for}}
      SUBROUTINE diquad(rt, dt, order, p1, p2, wts, npts, p1d, p2d)
      INTEGER rt
      INTEGER dt
      INTEGER order
      INTEGER p1d
      INTEGER p2d
      INTEGER npts
      REAL p1
      DIMENSION p1(0:p1d, 0:npts)
      REAL p2
      DIMENSION p2(0:p2d, 0:npts)
      REAL wts
      DIMENSION wts(0:npts)

      {{for Q in rules}}
      {{if Q.itype == double}}
      IF (rtype == {{Q.index}}) THEN
      CALL {{Q.abbrv_name}}(dt, order, p1, p2, wts, npts, p1d, p2d)
      END IF
      {{end if}}
      {{end for}}
      END
