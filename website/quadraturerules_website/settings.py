"""Settings."""

import os as _os
import typing as _typing

import yaml as _yaml
from webtools import settings
from webtools.tools import join as _join

dir_path = _join(_os.path.dirname(_os.path.realpath(__file__)), "..")
root_path = _join(dir_path, "..")
template_path = _join(dir_path, "template")
files_path = _join(dir_path, "files")
pages_path = _join(dir_path, "pages")
rules_path = _join(root_path, "rules")
html_path = _join(dir_path, "_html")

github_token: _typing.Optional[str] = None

processes = 1

with open(_join(root_path, "VERSION")) as f:
    version = f.read().strip()

site_data = {}
for file in _os.listdir(_join(dir_path, "data")):
    if not file.startswith("."):
        with open(_join(dir_path, "data", file)) as f:
            site_data[file] = _yaml.load(f, Loader=_yaml.FullLoader)

settings.owners = ["mscroggs"]
settings.editors = site_data["editors"]
settings.contributors = site_data["contributors"]
settings.url = "https://quadraturerules.org"
settings.website_name = [
    "The online encyclopedia of quadrature rules",
    "the online encyclopedia of quadrature rules",
]
settings.repo = "mscroggs/quadraturerules"

settings.dir_path = dir_path
settings.html_path = html_path
settings.template_path = template_path
settings.github_token = github_token
settings.str_extras = [
    ("{{tick}}", "<span style='color:#008800'>&#10004;</span>"),
    ("{{VERSION}}", version),
]


def set_html_path(path):
    """Set HTML path."""
    global html_path
    html_path = path
    settings.html_path = path


def set_github_token(token):
    """Set GitHub token."""
    global github_token
    github_token = token
    settings.github_token = token
