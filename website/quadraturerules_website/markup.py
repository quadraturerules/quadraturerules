"""Markup."""

from webtools.markup import markup as _markup


def markup(content: str) -> str:
    """Markup content.

    Args:
        content: Content

    Returns:
        Content with markup replaced by HTML
    """
    return _markup(content, [], [("{{tick}}", "<span style='color:#008800'>&#10004;</span>")])
