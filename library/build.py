"""Build library."""

import argparse
import os
import re
import sys
from datetime import datetime

import generate
from webtools.tools import join
from qrtools import generate_qr, rules, settings


start_all = datetime.now()
path = os.path.dirname(os.path.realpath(__file__))
settings.set_root_path(join(path, ".."))

parser = argparse.ArgumentParser(description="Build quadraturerules library")
parser.add_argument('library', metavar='library', nargs=1,
                    default=None, help="Library to build")

args = parser.parse_args()
lib = args.library[0]

assert lib in os.listdir(path)

source_dir = join(path, lib)
assert os.path.isdir(source_dir)
target_dir = join(path, f"{lib}.build")
if os.path.isdir(target_dir):
    os.system(f"rm -r {target_dir}")

os.mkdir(target_dir)

with open(join(path, "..", "VERSION")) as f:
    version = f.read().strip()
with open(join(path, "..", "LICENSE")) as f:
    license = "\n".join(f.read().split("\n")[2:])
with open(join(path, "..", "README.md")) as f:
    readme = f.read()
readme = re.sub(
    r"\(website/pages/([^\)]+)\.md\)",
    r"(https://quadraturerules.org/\1.html)",
    readme)

all_rules = []
for file in os.listdir(settings.rules_path):
    if file.endswith(".qr"):
        all_rules.append(rules.load_rule(file[:-3]))
all_rules.sort(key=lambda r: r.name())

domains = list(set(i.domain for r in all_rules for i in r.rules))
domains.sort(key=lambda d: (rules.dim(d), rules.sort_name(d)))


def load_library_file(m):
    """Load the content of a files in website/pages/libraries/."""
    with open(join(path, "..", "website", "pages", "libraries", f"{m[1]}.md")) as f:
        return "#" + f.read()


loop_targets = {
    "rules": [generate_qr.RuleFamily(r) for r in all_rules],
    "domains": [generate_qr.Domain(d, i) for i, d in enumerate(domains)],
}


def extra_subs(content):
    """Make substitutions in a file."""
    content = content.replace("{{VERSION}}", version)
    content = content.replace("{{LICENSE}}", license)
    content = content.replace("{{README}}", readme)
    content = re.sub(r"{{website/pages/libraries/([^}]+)}}", load_library_file, content)
    return content


generate.folder.generate(
    source_dir,
    target_dir,
    loop_targets=loop_targets,
    extra_subs=extra_subs,
    print_timing=True,
)

# Linting
if lib == "python":
    os.system(f"cd {target_dir} && ruff format .")
if lib == "rust":
    os.system(f"cd {target_dir} && cargo fmt")

end_all = datetime.now()
print(f"Total time: {(end_all - start_all).total_seconds():.2f}s")
