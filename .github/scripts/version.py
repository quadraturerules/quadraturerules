import json
import sys
from datetime import datetime

import github

access_key = sys.argv[-1]

git = github.Github(access_key)

repo = git.get_repo("mscroggs/quadraturerules")
branch = repo.get_branch("main")
ref = repo.get_git_ref("heads/main")
base_tree = repo.get_git_tree(branch.commit.sha)

vfile1 = repo.get_contents("VERSION", branch.commit.sha)
version = vfile1.decoded_content.decode("utf8").strip()

for release in repo.get_releases():
    if release.tag_name == f"v{version}":
        break
else:
    repo.create_git_tag_and_release(
        f"v{version}",
        f"v{version}",
        f"v{version}",
        "",
        branch.commit.sha,
        "commit",
    )
