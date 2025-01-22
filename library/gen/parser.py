"""Code parsing."""

import typing

from gen.nodes import Node, If, For, Line, ListOfNodes


def parse(code: str) -> ListOfNodes:
    print("--------")
    print(code)
    print("--------")
    if "{{end for}}" in code:
        temp, after = code.split("{{end for}}", 1)
        if after.startswith("\n"):
            after = after[1:]
        while temp.endswith(" "):
            temp = temp[:-1]
        temp2 = temp.split("{{for ")
        before = "{{for ".join(temp2[:-1])
        var, inside = temp2[-1].split(" ", 1)
        while before.endswith(" "):
            before = before[:-1]
        if "}}" not in inside:
            from IPython import embed; embed()
        loop_over, inside = inside.split("}}", 1)
        if inside.startswith("\n"):
            inside = inside[1:]
        assert loop_over[:3] == "in "
        loop_over = loop_over[3:]
        return parse(before) + [For(var, loop_over, parse(inside))] + parse(after)

    if "{{end if}}" in code:
        temp, after = code.split("{{end if}}", 1)
        if after.startswith("\n"):
            after = after[1:]
        while temp.endswith(" "):
            temp = temp[:-1]
        temp2 = temp.split("{{if ")
        before = "{{if ".join(temp2[:-1])
        while before.endswith(" "):
            before = before[:-1]
        condition, inside = temp2[-1].split("}}", 1)
        if inside.startswith("\n"):
            inside = inside[1:]
        return parse(before) + [If(condition, parse(inside))] + parse(after)

    return ListOfNodes([Line(line) for line in code.split("\n")])

