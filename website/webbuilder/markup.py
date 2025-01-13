"""Markup."""

import os
import re
import shlex
import typing
import warnings
from datetime import datetime
from urllib.parse import quote_plus

import symfem
import yaml
from github import Github

from webbuilder import settings

page_references: typing.List[str] = []


def heading(hx: str, content: str, style: typing.Optional[str] = None) -> str:
    """Create heading.

    Args:
        hx: HTML tag
        content: Heading content

    Returns:
        Heading with self reference
    """
    id = quote_plus(content)
    out = f"<{hx}"
    if style is not None:
        out += f" style=\"{style}\""
    out += f">{content}</{hx}>\n"
    return out


def heading_with_self_ref(hx: str, content: str, style: typing.Optional[str] = None) -> str:
    """Create heading with self reference.

    Args:
        hx: HTML tag
        content: Heading content

    Returns:
        Heading with self reference
    """
    id = quote_plus(content)
    out = f"<{hx} id=\"{id}\""
    if style is not None:
        out += f" style=\"{style}\""
    out += f"><a href=\"#{id}\">{content}</a></{hx}>\n"
    return out


def preprocess(content: str) -> str:
    """Preprocess content.

    Args:
        content: Content

    Returns:
        Preprocessed content
    """
    for file in os.listdir(settings.dir_path):
        if file.endswith(".md"):
            if f"{{{{{file}}}}}" in content:
                with open(os.path.join(settings.dir_path, file)) as f:
                    content = content.replace(
                        f"{{{{{file}}}}}",
                        f.read().replace("](https://defelement.org", "]("))
    return content


def markup(content: str) -> str:
    """Markup content.

    Args:
        content: Content

    Returns:
        Content with markup replaced by HTML
    """
    global page_references

    content = preprocess(content)

    out = ""
    popen = False
    ulopen = False
    liopen = False
    code = False
    is_python = False
    is_bash = False

    for line in content.split("\n"):
        if line.startswith("#"):
            if popen:
                out += "</p>\n"
                popen = False
            if ulopen:
                if liopen:
                    out += "</li>"
                    liopen = False
                out += "</ul>\n"
                ulopen = False
            i = 0
            while line.startswith("#"):
                line = line[1:]
                i += 1
            out += heading_with_self_ref(f"h{i}", line.strip())
        elif line.startswith("* "):
            if popen:
                out += "</p>\n"
                popen = False
            if not ulopen:
                out += "<ul>"
                ulopen = True
            if liopen:
                out += "</li>"
                liopen = False
            out += "<li>"
            liopen = True
            out += line[2:].strip()
        elif line == "":
            if popen:
                out += "</p>\n"
                popen = False
            if ulopen:
                if liopen:
                    out += "</li>"
                    liopen = False
                out += "</ul>\n"
                ulopen = False
        elif line == "```":
            code = not code
            is_python = False
            is_bash = False
        elif line == "```python":
            code = not code
            is_python = True
            is_bash = False
        elif line == "```bash":
            code = not code
            is_python = False
            is_bash = True
        else:
            if not ulopen and not popen and not line.startswith("<") and not line.startswith("\\["):
                if code:
                    out += "<p class='pcode'>"
                else:
                    out += "<p>"
                popen = True
            if code:
                if is_python:
                    out += python_highlight(line.replace(" ", "&nbsp;"))
                elif is_bash:
                    out += bash_highlight(line.replace(" ", "&nbsp;"))
                else:
                    out += line.replace(" ", "&nbsp;")
                out += "<br />"
            else:
                out += line
                out += " "

    page_references = []

    out = out.replace("(CODE_OF_CONDUCT.md)", "(code-of-conduct.md)")

    out = insert_links(out)
    out = re.sub(r"{{code-include::([^}]+)}}", code_include, out)
    out = re.sub(r"`([^`]+)`", r"<span style='font-family:monospace'>\1</span>", out)

    out = re.sub(r"\*\*([^\n]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^\n]+)\*", r"<em>\1</em>", out)

    out = out.replace("{{tick}}", "<i class='fa-solid fa-check' style='color:#55ff00'></i>")

    if len(page_references) > 0:
        out += heading_with_self_ref("h2", "References")
        out += "<ul class='citations'>"
        out += "".join([f"<li><a class='refid' id='ref{i+1}'>[{i+1}]</a> {j}</li>"
                        for i, j in enumerate(page_references)])
        out += "</ul>"

    return insert_dates(out)


def insert_links(txt: str) -> str:
    """Insert links.

    Args:
        txt: text

    Returns:
        Text with links
    """
    txt = re.sub(r"\(([^\)]+)\.md\)", r"(/\1.html)", txt)
    txt = re.sub(r"\(([^\)]+)\.md#([^\)]+)\)", r"(/\1.html#\2)", txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", txt)
    return txt


def insert_dates(txt: str) -> str:
    """Insert dates.

    Args:
        txt: Text

    Returns:
        Text with dates inserted
    """
    now = datetime.now()
    txt = txt.replace("{{date:Y}}", now.strftime("%Y"))
    txt = txt.replace("{{date:D-M-Y}}", now.strftime("%d-%B-%Y"))

    return txt


def code_include(matches: typing.Match[str]) -> str:
    """Format code snippet.

    Args:
        matches: Code snippets

    Returns:
        HTML
    """
    out = "<p class='pcode'>"
    with open(os.path.join(settings.dir_path, matches[1])) as f:
        out += "<br />".join(line.replace(" ", "&nbsp;") for line in f)
    out += "</p>"
    return out


def python_highlight(txt: str) -> str:
    """Apply syntax highlighting to Python snippet.

    Args:
        txt: Python snippet

    Returns:
        Snippet with syntax highlighting
    """
    txt = txt.replace(" ", "&nbsp;")
    out = []
    for line in txt.split("\n"):
        comment = ""
        if "#" in line:
            lsp = line.split("#", 1)
            line = lsp[0]
            comment = f"<span style='color:#FF8800'>#{lsp[1]}</span>"

        lsp = line.split("\"")
        line = lsp[0]

        for i, j in enumerate(lsp[1:]):
            if i % 2 == 0:
                line += f"<span style='color:#DD2299'>\"{j}"
            else:
                line += f"\"</span>{j}"

        out.append(line + comment)
    return "<br />".join(out)


def bash_highlight(txt: str) -> str:
    """Apply syntax highlighting to Bash snippet.

    Args:
        txt: Bash snippet

    Returns:
        Snippet with syntax highlighting
    """
    txt = txt.replace(" ", "&nbsp;")
    txt = re.sub("(python3?(?:&nbsp;-m&nbsp;.+?)?&nbsp;)",
                 r"<span style='color:#FF8800'>\1</span>", txt)
    return "<br />".join(txt.split("\n"))
