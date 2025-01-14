# Making a new release

To make a new release of the quadraturerules library, follow these steps:

1. Open a pull request to increase the version number in [VERSION](VERSION). The version number should have the format `{Q}.{V}`
   where `Q` is the number of rules in the `rules/` folder and `V` is a minor version number which should be updated whenever a rule is updated
   and reset to 0 whenever `Q` is increased.

2. Wait for the CI to pass and merge the PR.

3. Create a [new tag](https://github.com/mscroggs/quadraturerules/releases/new) on GitHub. The title and tag should be `v{VERSION}`.

4. Python and Rust releases should be created automaticaly by the [release](https://github.com/mscroggs/quadraturerules/actions/workflows/release.yml) CI workflow.
