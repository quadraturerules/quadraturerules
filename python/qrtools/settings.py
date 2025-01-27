"""Settings."""

import os as _os
import typing as _typing

import yaml as _yaml
from webtools import settings
from webtools.tools import join as _join

root_path = ""
website_path = ""
template_path = ""
files_path = ""
pages_path = ""
rules_path = ""
html_path = ""

github_token: _typing.Optional[str] = None

processes = 1

site_data = {}

settings.owners = ["mscroggs"]
settings.editors = site_data["editors"]
settings.contributors = site_data["contributors"]
settings.url = "https://quadraturerules.org"
settings.website_name = [
    "The online encyclopedia of quadrature rules",
    "the online encyclopedia of quadrature rules",
]
settings.repo = "quadraturerules/quadraturerules"

settings.github_token = github_token


def set_root_path(path):
    """Set root path."""
    global root_path
    global website_path
    global template_path
    global files_path
    global pages_path
    global rules_path
    global html_path
    global site_data

    root_path = path
    website_path = _join(root_path, "website")
    template_path = _join(website_path, "template")
    files_path = _join(website_path, "files")
    pages_path = _join(website_path, "pages")
    rules_path = _join(root_path, "rules")

    for file in _os.listdir(_join(website_path, "data")):
        if not file.startswith("."):
            with open(_join(website_path, "data", file)) as f:
                site_data[file] = _yaml.load(f, Loader=_yaml.FullLoader)

    with open(_join(root_path, "VERSION")) as f:
        version = f.read().strip()

    settings.dir_path = website_path
    settings.template_path = template_path
    settings.str_extras = [
        ("{{tick}}", "<span style='color:#008800'>&#10004;</span>"),
        ("{{VERSION}}", version),
    ]

    if html_path == "":
        html_path = _join(dir_path, "_html")
        settings.html_path = html_path


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


if os.path.isfile(_join(_os.path.dirname(_os.path.realpath(__file__)), "..", "..", "README.md")):
    set_root_path(_join(_os.path.dirname(_os.path.realpath(__file__)), "..", ".."))
