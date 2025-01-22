"""Code parsing."""

import typing
import re

from gen.nodes import Node, If, For, Line, ListOfNodes


def parse(code: str) -> ListOfNodes:
    pre = ""
    inside = ""
    loop_count = None
    loop_start = None
    for line_n, line in enumerate(code.split("\n")):
        if re.match(r"^\{\{(:?if|for)[^\}]+\}\}$", line.strip()):
            if loop_count is None:
                loop_start = line.strip()
                loop_count = 1
            else:
                loop_count += 1
                inside += line + "\n"
        elif re.match(r"^\{\{end (:?if|for)\}\}$", line.strip()):
            loop_count -= 1
            if loop_count == 0:
                post = "\n".join(code.split("\n")[line_n + 1:])
                if loop_start.startswith("{{for "):
                    var, loop_over = loop_start[6:-2].split(" ", 1)
                    assert loop_over.startswith("in ")
                    loop_over = loop_over[3:]
                    return parse(pre) + [For(var, loop_over, parse(inside))] + parse(post)
                elif loop_start.startswith("{{if "):
                    condition = loop_start[5:-2]
                    return parse(pre) + [If(condition, parse(inside))] + parse(post)
                else:
                    raise ValueError(f"Unexpected loop start: {loop_start}")
            inside += line + "\n"
        elif loop_count is None:
            pre += line + "\n"
        else:
            inside += line + "\n"

    return ListOfNodes([Line(line) for line in code.split("\n")])
