"""Build library."""

import argparse
import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.join(path, ".."), "website"))
from webbuilder.rules import load_rule  # noqa: E402
from webbuilder import settings  # noqa: E402

parser = argparse.ArgumentParser(description="Build quadraturerules library")
parser.add_argument('library', metavar='library', nargs=1,
                    default=None, help="Library to build")

args = parser.parse_args()
lib = args.library[0]

assert lib in os.listdir(path)

source_dir = os.path.join(path, lib)
assert os.path.isdir(source_dir)
target_dir = os.path.join(path, f"{lib}.build")
if os.path.isdir(target_dir):
    os.system(f"rm -r {target_dir}")

os.mkdir(target_dir)

with open(os.path.join(os.path.join(path, ".."), "VERSION")) as f:
    version = f.read()

rules = []
for file in os.listdir(settings.rules_path):
    if file.endswith(".qr"):
        rules.append(load_rule(file[:-3]))


def replace(content, variable, rule):
    content = content.replace(f"{{{{{variable}.code}}}}", f"{rule.code}")
    content = content.replace(f"{{{{{variable}.index}}}}", f"{rule.index}")
    content = content.replace(f"{{{{{variable}.PascalCaseName}}}}", rule.name("PascalCase"))
    content = content.replace(f"{{{{{variable}.camelCaseName}}}}", rule.name("camelCase"))
    content = content.replace(f"{{{{{variable}.snake_case_name}}}}", rule.name("snake_case"))
    return content


def sub(content):
    content = content.replace("{{VERSION}}", version)
    while "{{end for}}" in content:
        temp, after = content.split("{{end for}}", 1)
        temp2 = temp.split("{{for ")
        before = "{{for ".join(temp2[:-1])
        var, inside = temp2[-1].split(" ", 1)
        content = before.strip() + "\n"
        if inside.startswith("in rules}}\n"):
            inside = inside[11:]
            for rule in rules:
                content += replace(inside, var, rule)
        else:
            raise ValueError("Unsupported loop")
        content += after
    return content


def sub_and_copy_files(folder):
    for file_ in os.listdir(os.path.join(source_dir, folder)):
        file = os.path.join(folder, file_)
        if os.path.isdir(os.path.join(source_dir, file)):
            os.mkdir(os.path.join(target_dir, file))
            sub_and_copy_files(file)
        elif file.endswith(".template"):
            print(file)
        else:
            with open(os.path.join(source_dir, file)) as f:
                content = f.read()
            with open(os.path.join(target_dir, file), "w") as f:
                f.write(sub(content))


sub_and_copy_files("")
