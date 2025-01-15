"""Settings."""

import os as _os
from webtools import settings

dir_path = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "..")
root_path = _os.path.join(dir_path, "..")
template_path = _os.path.join(dir_path, "template")
files_path = _os.path.join(dir_path, "files")
pages_path = _os.path.join(dir_path, "pages")
rules_path = _os.path.join(root_path, "rules")
html_path = _os.path.join(dir_path, "_html")

github_token = None

processes = 1

settings.dir_path = dir_path
settings.html_path = html_path
settings.template_path = template_path
settings.github_token = github_token


def set_html_path(path):
    """Set HTML path."""
    global html_path
    html_path = path
    settings.html_path = path
