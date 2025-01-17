"""Build quadraturerules.org."""

import argparse
import os
import re
from datetime import datetime

from quadraturerules_website import settings
from quadraturerules_website.rules import dim, load_rule
from webtools.html import make_html_page
from webtools.markup import heading, heading_with_self_ref, markup
from webtools.tools import html_local, join, parse_metadata

start_all = datetime.now()

parser = argparse.ArgumentParser(description="Build quadraturerules.org")
parser.add_argument('destination', metavar='destination', nargs="?",
                    default=None, help="Destination of HTML files.")
parser.add_argument('--github-token', metavar="github_token", default=None,
                    help="Provide a GitHub token to get update timestamps.")

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
    with open(join(settings.root_path, matches[1])) as f:
        return f.read()


args = parser.parse_args()
if args.destination is not None:
    settings.set_html_path(args.destination)
if args.github_token is not None:
    settings.set_github_token(args.github_token)

# Prepare paths
if os.path.isdir(settings.html_path):
    os.system(f"rm -rf {settings.html_path}")
os.mkdir(settings.html_path)

os.system(f"cp -r {settings.files_path}/* {settings.html_path}")

with open(join(settings.html_path, "CNAME"), "w") as f:
    f.write("quadraturerules.org")


def row(name, content):
    """Make a row of information."""
    if content == "":
        return ""
    else:
        return f"<tr><td>{name.replace(' ', '&nbsp;')}</td><td>{content}</td>"


rules = []
rules_for_index = []

# Make rule pages
for file in os.listdir(settings.rules_path):
    if file.endswith(".qr"):
        start = datetime.now()
        rule = file[:-3]
        print(f"{rule}.html", end="", flush=True)
        q = load_rule(rule)
        rpath = join(settings.html_path, rule)
        os.mkdir(rpath)

        rules_for_index.append((q.code, q.html_name, f"/{rule}"))
        rules.append(q)

        content = heading("h1", f"{q.code}: {q.html_name}")

        content += "<table class='rule'>"
        content += row("Alternative names", q.alt_names("HTML"))
        content += row("Integral", q.integral('LaTeX'))
        content += row("Notes", q.notes("HTML"))
        bib = q.references("BibTeX")
        if bib != "":
            content += row(
                "References",
                f"{q.references('HTML')}<br /><div class='citation'>"
                f"<a href='/{q.code}/references.bib'>Download references as BibTe&Chi;</a></div>"
            )
            with open(join(settings.html_path, q.code, "references.bib"), "w") as f:
                f.write(bib)
        content += "</table>"

        for domain, rulelist in q.rules_by_domain.items():
            content += heading_with_self_ref("h2", domain[0].upper() + domain[1:])
            domain_content = heading(
                "h1",
                f"{q.html_name} on {'an' if domain[0] in 'aeiou' else 'a'} {domain}")
            domain_content += f"<a class='more' href='/{q.code}'>&larr; Back to {q.html_name}</a>"
            for i, r in enumerate(rulelist):
                r.save_html_table(join(rpath, f"{r.title('filename')}.html"))
                rule_content = ""
                if r.order is not None:
                    rule_content += heading_with_self_ref("h3", f"Order {r.order}")
                rule_content += r.image(join(rpath, f"{r.title('filename')}.svg"))
                rule_content += (
                    "<div>"
                    f"<a class='toggler' id='show-{domain}-{i}' "
                    f"href=\"javascript:show_points('/{rule}/{r.title('filename')}.html',"
                    f"'{domain}-{i}')\">"
                    "&darr; show points and weights &darr;</a>"
                    f"<a class='toggler' id='hide-{domain}-{i}' "
                    f"href=\"javascript:hide_points('{domain}-{i}')\" style='display:none'>"
                    "&uarr; hide points and weights &uarr;</a>"
                    "</div>"
                    f"<div class='point-detail' id='point-detail-{domain}-{i}'></div>"
                )
                if i < 5:
                    content += rule_content
                domain_content += rule_content
            if len(rulelist) > 5:
                content += (
                    f"<a class='more' href='/{q.code}/more-{domain}.html'>"
                    "View higher order rules</a>")
            write_html_page(
                join(rpath, f"more-{domain}.html"),
                f"{rule}: {q.html_name} on {'an' if domain[0] in 'aeiou' else 'a'} {domain}",
                domain_content)
        content += (
            "<div id='point-detail-dummy' "
            "style='visibility:hidden;position:absolute;top:0;left:0;z-index:-10'></div>"
        )

        write_html_page(join(rpath, "index.html"),
                        f"{rule}: {q.html_name}", content)
        end = datetime.now()
        print(f" (completed in {(end - start).total_seconds():.2f}s)")


# Make pages
def make_pages(sub_dir=""):
    """Make pages recursively."""
    for file in os.listdir(join(settings.pages_path, sub_dir)):
        if os.path.isdir(join(settings.pages_path, sub_dir, file)):
            os.mkdir(join(settings.html_path, sub_dir, file))
            make_pages(join(sub_dir, file))
        elif file.endswith(".md"):
            start = datetime.now()
            fname = file[:-3]
            print(f"{sub_dir}/{fname}.html", end="", flush=True)
            with open(join(settings.pages_path, sub_dir, file)) as f:
                metadata, content = parse_metadata(f.read())

            content = re.sub(r"\{\{(.+\.md)\}\}", load_md_file, content)
            content = content.replace("](website/pages/", "](")
            content = markup(content, sub_dir)

            if sub_dir == "" and file == "index.md":
                img = "<div id='sideplots'>"
                for i in settings.site_data["front-page"]["images"]:
                    for q in rules:
                        if q.code == i["rule"]:
                            break
                    else:
                        raise ValueError(f"Invalid rule: {i['rule']}")
                    img += "<div>"
                    for r in q.rules:
                        if r.domain == i['domain'] and r.order == i['order']:
                            img += f"<img src='/{i['rule']}/{r.title('filename')}.svg'>"
                            break
                    else:
                        raise ValueError(f"Invalid domain or order: {i['domain']}, {i['order']}")
                    img += (
                        "<div>"
                        f"An order {i['order']} <a href='/{i['rule']}'>{q.html_name}</a>"
                        f" rule on {'an' if i['domain'][0] in 'aeiou' else 'a'} {i['domain']}."
                        "</div></div>"
                    )
                img += "</div>"
                content = img + content

            write_html_page(join(settings.html_path, sub_dir, f"{fname}.html"),
                            metadata["title"], content)
            end = datetime.now()
            print(f" (completed in {(end - start).total_seconds():.2f}s)")


make_pages()

rules.sort(key=lambda q: q.code)

# List of rules pages
# Alphabetical
rules_for_index.sort(key=lambda i: i[1].lower())
content = heading("h1", "List of quadrature rules (alphabetical)")
content += "<ul>"
for code, name, url in rules_for_index:
    content += f"<li><a href='{url}'>{name} ({code})</a></li>"
content += "</ul>"
write_html_page(
    join(settings.html_path, "rules-alpha.html"),
    "List of quadrature rules (alphabetical)",
    content)

# Rules by index
rules_for_index.sort(key=lambda i: i[0])
content = heading("h1", "List of quadrature rules (by Q-index)")
content += "<ul>"
for code, name, url in rules_for_index:
    content += f"<li><a href='{url}'>{code}: {name}</a></li>"
content += "</ul>"
write_html_page(
    join(settings.html_path, "rules.html"), "List of quadrature rules (by index)", content)

# Lists per domain
domains = list(set(domain for q in rules for domain in q.rules_by_domain))
domains.sort(key=lambda r: (dim(r), r))
content = heading("h1", "List of quadrature rules (by domain)")
for domain in domains:
    content += heading("h2", f"<a href='/rules-{domain}.html'>{domain[0].upper()}{domain[1:]}</a>")
    sub_content = heading(
        "h1", f"List of quadrature rules on {'an' if domain[0] in 'aeiou' else 'a'} {domain}")
    sub_content += "<a class='more' href='/rules-domain.html'>&larr; Back to all domains</a>"
    content += "<ul>"
    sub_content += "<ul>"
    for q in rules:
        if domain in q.rules_by_domain:
            content += f"<li><a href='/{q.code}'>{q.html_name} ({q.code})</a></li>"
            sub_content += f"<li><a href='/{q.code}'>{q.html_name} ({q.code})</a></li>"
    content += "</ul>"
    sub_content += "</ul>"
    write_html_page(
        join(settings.html_path, f"rules-{domain}.html"),
        "List of quadrature rules ({domain})",
        sub_content)
write_html_page(
    join(settings.html_path, "rules-domain.html"), "List of quadrature rules (by domain)", content)

# Lists per integral
integrals = list(set(q.integral() for q in rules))
content = heading("h1", "List of quadrature rules (by integral)")
for n, i in enumerate(integrals):
    content += heading("h2", f"<a href='/rules-integral{n}.html'>{i}</a>")
    sub_content = heading("h1", f"List of quadrature rules for {i}")
    sub_content += "<a class='more' href='/rules-integral.html'>&larr; Back to all integrals</a>"
    content += "<ul>"
    sub_content += "<ul>"
    for q in rules:
        if q.integral() == i:
            content += f"<li><a href='/{q.code}'>{q.html_name} ({q.code})</a></li>"
            sub_content += f"<li><a href='/{q.code}'>{q.html_name} ({q.code})</a></li>"
    content += "</ul>"
    sub_content += "</ul>"
    write_html_page(
        join(settings.html_path, f"rules-integral{n}.html"),
        "List of quadrature rules for {i}",
        sub_content)
write_html_page(
    join(settings.html_path, "rules-integral.html"),
    "List of quadrature rules (by domain)",
    content)

# Site map
sitemap[html_local(join(settings.html_path, "sitemap.html"))] = "List of all pages"


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
with open(join(settings.html_path, "sitemap.html"), "w") as f:
    f.write(make_html_page(content))

end_all = datetime.now()
print(f"Total time: {(end_all - start_all).total_seconds():.2f}s")
