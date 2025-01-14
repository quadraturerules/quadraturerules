# Barycentric coordinates
The points that make up the quadrature rules in this encyclopedia are represented using barycentric coordinates.
If \(\vec{v}_0,\dots,\vec{v}_{m-1}\in\mathbb{R}^d\) are the coordinates of the vertices of a polytope and \((p_0,\dots,p_{m-1})\in\mathbb{R}^m\)
is the barycentric coordinates of a quadrature point, then the coordinates of the corresponding quadrature point on the polytope is
given by

$$\sum_{i=0}^{m-1}p_i\vec{v}_i.$$

The quadrature weights in this encyclopedia are normalised for a polytope of volume 1, so an integral can be approximated by

$$\int_I f(x)\,\mathrm{d}x\approx v(I)\sum_{i=0}^{n-1}w_if(\vec{p}_i),$$

where \(\{\vec{p}_0,\dots,\vec{p}_{n-1}\}\subset\mathbb{R}^d\) and \(\{w_0,\dots,w_{n-1}\}\subset\mathbb{R}\)
are the quadrature points and weights, and \(v(I)\) is the volume of the integration domain \(I\).
