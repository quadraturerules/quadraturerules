"""Build library."""

import argparse
import os
import re
import sys
from datetime import datetime

import gen
from webtools.tools import join

start_all = datetime.now()

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(join(path, "..", "website"))
import gen.qr  # noqa: E402
from quadraturerules_website import rules, settings  # noqa: E402

parser = argparse.ArgumentParser(description="Build quadraturerules library")
parser.add_argument('library', metavar='library', nargs=1,
                    default=None, help="Library to build")

args = parser.parse_args()
lib = args.library[0]

assert lib in os.listdir(path) and lib != "gen"

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
    "rules": [gen.qr.RuleFamily(r) for r in all_rules],
    "domains": [gen.qr.Domain(d, i) for i, d in enumerate(domains)],
}


def sub(content, vars={}):
    """Make substitutions in a file."""
    content = content.replace("{{VERSION}}", version)
    content = content.replace("{{LICENSE}}", license)
    content = content.replace("{{README}}", readme)
    content = re.sub(r"{{website/pages/libraries/([^}]+)}}", load_library_file, content)

    file = gen.parse(content)
    return file.substitute(vars=vars, loop_targets=loop_targets)


def sub_and_copy_files(folder):
    """Make substitutions and copy all files recursively in a directory."""
    for file_ in os.listdir(join(source_dir, folder)):
        file = join(folder, file_)
        if file_.startswith("."):
            continue
        if os.path.isdir(join(source_dir, file)):
            os.mkdir(join(target_dir, file))
            sub_and_copy_files(file)
        elif file.endswith(".template"):
            with open(join(source_dir, file)) as f:
                content = f.read()
            _, metadata_, content = content.split("--\n", 2)
            metadata = {}
            for line in metadata_.strip().split("\n"):
                var, value = line.split(":", 1)
                metadata[var.strip()] = value.strip()
            var, loop_over = metadata["template"].split(" ", 1)
            match loop_over:
                case "in rule":
                    for rule in all_rules:
                        start = datetime.now()
                        print(f"{file} [{rule.name()}]", end="", flush=True)
                        vars = {var: gen.qr.RuleFamily(rule)}
                        filename = sub(metadata["filename"], vars).strip()
                        with open(join(target_dir, folder, filename), "w") as f:
                            f.write(sub(content, vars))
                        end = datetime.now()
                        print(f" (completed in {(end - start).total_seconds():.2f}s)")
                case _:
                    raise ValueError(f"Unsupported loop: {loop_over}")
        else:
            start = datetime.now()
            print(file, end="", flush=True)
            with open(join(source_dir, file)) as f:
                content = f.read()
            with open(join(target_dir, file), "w") as f:
                f.write(sub(content))
            end = datetime.now()
            print(f" (completed in {(end - start).total_seconds():.2f}s)")


sub_and_copy_files("")

# Linting
if lib == "python":
    os.system(f"cd {target_dir} && ruff format .")
if lib == "rust":
    os.system(f"cd {target_dir} && cargo fmt")

end_all = datetime.now()
print(f"Total time: {(end_all - start_all).total_seconds():.2f}s")
