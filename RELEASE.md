# Making a new release

To make a new release of the quadraturerules library, follow these steps:

1. Open a pull request to increase the version number in [VERSION](VERSION). The version number should have the format `{M}.{Q}.{V}`
   where `M` is the major version number, `Q` is the number of rules in the `rules/` folder, and `V` is a minor version number.
   `M` should be updated whenever there are major changes to the library, such as the addition of a new integral type.
   `V` should be updated whenever a rule is updated and reset to 0 whenever `Q` is increased.

2. Wait for the CI to pass and merge the PR.

3. A new tag should automatically be created on GitHub.
   The [release](https://github.com/quadraturerules/quadraturerules/actions/workflows/release.yml) CI workflow should automatically create:

   - A Python release
   - A Rust release
   - An archive of the C++ library source
