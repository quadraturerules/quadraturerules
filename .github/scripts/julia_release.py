import json
import sys
from datetime import datetime

import github

access_key, version = sys.argv[-2:]

git = github.Github(access_key)

qr = git.get_repo("quadraturerules/TabulatedQuadratureRules.jl")
branch = qr.get_branch("main")
ref = qr.get_git_ref("heads/main")
base_tree = qr.get_git_tree(branch.commit.sha)

qr.create_git_tag_and_release(
    f"{version}",
    f"{version}",
    f"{version}",
    f"Release version {version[1:]}",
    branch.commit.sha,
    "commit",
)
