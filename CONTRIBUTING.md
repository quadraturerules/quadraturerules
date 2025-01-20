# Contributing to the online encyclopedia of quadrature rules

## Making suggestions

If you want to suggest changes to the online encyclopedia of quadrature rules, please use the
[issue tracker](https://github.com/quadraturerules/quadraturerules/issues)
on GitHub.

## Contributing directly

### Submitting a pull request
If you want to directly submit changes to the online encyclopedia of quadrature rules, you can do this by forking the [GitHub repository](https://github.com/quadraturerules/quadraturerules),
making changes, then submitting a pull request.
If you want to contribute, but are unsure where to start, have a look at the
[issue tracker](https://github.com/quadraturerules/quadraturerules/labels/good%20first%20issue) for issues labelled "good first issue".

### Adding a quadrature rule
Rules in the online encyclopedia of quadrature rules are defined using files in the `rules/` folder.
A yaml file called `Qxxxxxx.qr` (where `xxxxxx` is the next unused index) is used to define a family of rules.
The entries in this yaml file are:

<table class='bordered align-left'>
<thead>
<tr><td>Name</td><td>Required</td><td>Description</td></tr>
</thead>
<tr><td>`name`</td><td>{{tick}}</td><td>The name of the rule (ascii), with `&#8209;&#8209;` used between names of different people (eg `Gauss&#8209;&#8209;Legendre`).</td></tr>
<tr><td>`alt&#8209;names`</td><td></td><td>Alternative names of the rule.</td></tr>
<tr><td>`integral&#8209;type`</td><td></td><td>The type of the integral (default: `single`).</td></tr>
<tr><td>`integrand`</td><td>{{tick}}</td><td>The integrand that the quadrature rule can be used to approximate.</td></tr>
<tr><td>`notes`</td><td></td><td>Notes about the quadrature rule.</td></tr>
<tr><td>`references`</td><td></td><td>References to where the rule is defined.</td></tr>
</table>

Alongside this yaml file, a folder called `Qxxxxxx` is included, which contants a series of yaml files called `*.rule`. Each of these files
contains the points and weights for an instance of the quadrature family on a given domain with a given order. At the top of this file, metadata
in included in yaml format between two lines containing only `&#8209;&#8209;`. These entries in the metadata are used:

<table class='bordered align-left'>
<thead>
<tr><td>Name</td><td>Required</td><td>Description</td></tr>
</thead>
<tr><td>`domain`</td><td>{{tick}}</td><td>The domain of the integral.</td></tr>
<tr><td>`order`</td><td>{{tick}}</td><td>The order (or degree) of the rule.</td></tr>
</table>

After the metadata, the points and weights are given in format `point_0 point_1 ... | weight`
(where (`point_0`, `point_1`, ...) are the [barycentric coordinates](website/pages/barycentric.md) of a quadrature point)
with one line for each pair of points.

### Testing your contribution
When you open a pull request, a series of tests and style checks will run via GitHub Actions.
(You may have to wait for manual approval for these to run.)
These tests and checks must pass before the pull request can be merged.
If the tests and checks fail, you can click on them on the pull request page to see where the failure is happening.

## Code of conduct
We expect all our contributors to follow our [code of conduct](CODE_OF_CONDUCT.md). Any unacceptable
behaviour can be reported to Matthew (quadraturerules@mscroggs.co.uk).
