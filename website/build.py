"""Build quadraturerules.org."""

import argparse
import os
import re
from datetime import datetime

from webbuilder import settings
from webbuilder.html import make_html_page
from webbuilder.markup import heading, heading_with_self_ref, markup
from webbuilder.rules import load_rule
from webbuilder.tools import html_local, parse_metadata

start_all = datetime.now()

parser = argparse.ArgumentParser(description="Build quadraturerules.org")
parser.add_argument('destination', metavar='destination', nargs="?",
                    default=None, help="Destination of HTML files.")
parser.add_argument('--github-token', metavar="github_token", default=None,
                    help="Provide a GitHub token to get update timestamps.")
parser.add_argument('--processes', metavar="processes", default=None,
                    help="The number of processes to run the building of examples on.")

sitemap = {}


def write_html_page(path: str, title: str, content: str):
    """Write a HTML page.

    Args:
        path: Page path
        title: Page title
        content: Page content
    """
    global sitemap
    assert html_local(path) not in sitemap
    sitemap[html_local(path)] = title
    with open(path, "w") as f:
        f.write(make_html_page(content, title))


def load_md_file(matches):
    """Read the content of a markdown file."""
    with open(os.path.join(settings.root_path, matches[1])) as f:
        return f.read()


args = parser.parse_args()
if args.destination is not None:
    settings.html_path = args.destination

if args.processes is not None:
    settings.processes = int(args.processes)

# Prepare paths
if os.path.isdir(settings.html_path):
    os.system(f"rm -rf {settings.html_path}")
os.mkdir(settings.html_path)

os.system(f"cp -r {settings.files_path}/* {settings.html_path}")

with open(os.path.join(settings.html_path, "CNAME"), "w") as f:
    f.write("quadraturerules.org")

# Make pages
for file in os.listdir(settings.pages_path):
    if file.endswith(".md"):
        start = datetime.now()
        fname = file[:-3]
        print(f"{fname}.html", end="", flush=True)
        with open(os.path.join(settings.pages_path, file)) as f:
            metadata, content = parse_metadata(f.read())

        content = re.sub(r"\{\{(.+\.md)\}\}", load_md_file, content)
        content = content.replace("](website/pages", "](")
        content = markup(content)

        write_html_page(os.path.join(settings.html_path, f"{fname}.html"),
                        metadata["title"], content)
        end = datetime.now()
        print(f" (completed in {(end - start).total_seconds():.2f}s)")


def row(name, content):
    """Make a row of information."""
    if content == "":
        return ""
    else:
        return f"<tr><td>{name}</td><td>{content}</td>"


rules = []

# Make rule pages
for file in os.listdir(settings.rules_path):
    if file.endswith(".qr"):
        start = datetime.now()
        rule = file[:-3]
        print(f"{rule}.html", end="", flush=True)
        q = load_rule(rule)
        rpath = os.path.join(settings.html_path, rule)
        os.mkdir(rpath)

        rules.append((q.code, q.html_name, f"/{rule}"))

        content = heading("h1", f"{q.code}: {q.html_name}")

        content += "<table class='rule'>"
        content += row("Alternative names", q.alt_names("HTML"))
        content += row("Integral", q.integral('LaTeX'))
        content += row("Notes", q.notes("HTML"))
        content += "</table>"

        for i, r in enumerate(q.rules):
            content += heading_with_self_ref("h2", r.title("HTML"))
            content += r.image(os.path.join(rpath, f"{r.title('filename')}.svg"))
            r.save_html_table(os.path.join(rpath, f"{r.title('filename')}.html"))
            content += (
                "<div>"
                f"<a class='toggler' id='show-{i}' "
                f"href=\"javascript:show_points('/{rule}/{r.title('filename')}.html', {i})\">"
                "&darr; show points and weights &darr;</a>"
                f"<a class='toggler' id='hide-{i}' "
                f"href=\"javascript:hide_points({i})\" style='display:none'>"
                "&uarr; hide points and weights &uarr;</a>"
                "</div>"
                f"<div class='point-detail' id='point-detail-{i}'></div>"
            )
        content += (
            "<div id='point-detail-dummy' "
            "style='visibility:hidden;position:absolute;top:0;left:0;z-index:-10'></div>"
        )

        write_html_page(os.path.join(rpath, "index.html"),
                        f"{rule}: {q.html_name}", content)
        end = datetime.now()
        print(f" (completed in {(end - start).total_seconds():.2f}s)")

rules.sort(key=lambda i: i[0])

# List of rules page
content = heading("h1", "List of quadrature rules")
content += "<ul>"
for code, name, url in rules:
    content += f"<li><a href='{url}'>{code}: {name}</a></li>"
content += "</ul>"

write_html_page(os.path.join(settings.html_path, "rules.html"), "List of quadrature rules", content)

# Site map
sitemap[html_local(os.path.join(settings.html_path, "sitemap.html"))] = "List of all pages"


def list_pages(folder: str) -> str:
    """Create list of pages in a folder.

    Args:
        folder: The folder

    Returns:
        List of pages
    """
    items = []
    if folder == "":
        items.append(("A", "<li><a href='/index.html'>Front page</a>"))
    for i, j in sitemap.items():
        if i.startswith(folder):
            file = i[len(folder) + 1:]
            if "/" in file:
                subfolder, subfile = file.split("/", 1)
                if subfile == "index.html":
                    items.append((j.lower(), list_pages(f"{folder}/{subfolder}")))
            elif file != "index.html":
                items.append((j.lower(), f"<li><a href='{i}'>{j}</a></li>"))
    items.sort(key=lambda a: a[0])
    out = ""
    if folder != "":
        title = sitemap[f"{folder}/index.html"]
        out += f"<li><a href='{folder}/index.html'>{title}</a>"
    out += "<ul>" + "\n".join(i[1] for i in items) + "</ul>"
    if folder != "":
        out += "</li>"
    return out


content = heading("h1", "List of all pages") + list_pages("")
with open(os.path.join(settings.html_path, "sitemap.html"), "w") as f:
    f.write(make_html_page(content))

end_all = datetime.now()
print(f"Total time: {(end_all - start_all).total_seconds():.2f}s")
