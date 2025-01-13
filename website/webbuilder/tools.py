"""Tools."""

import typing

import yaml

from webbuilder import settings

if typing.TYPE_CHECKING:
    from numpy import float64
    from numpy.typing import NDArray
    Array = NDArray[float64]
else:
    Array = typing.Any


def parse_metadata(content: str) -> typing.Tuple[typing.Dict[str, typing.Any], str]:
    """Parse metadata.

    Args:
        content: Raw data

    Returns:
        Parsed metadata and content without metadata
    """
    from webbuilder.markup import preprocess

    metadata: typing.Dict[str, typing.Any] = {"title": None}
    if content.startswith("--\n"):
        metadata_in, content = content[3:].split("\n--\n", 1)
        metadata.update(yaml.load(metadata_in, Loader=yaml.FullLoader))
    content = preprocess(content.strip())
    if metadata["title"] is None and content.startswith("# "):
        metadata["title"] = content[2:].split("\n", 1)[0].strip()
    return metadata, content


def html_local(path: str) -> str:
    """Get the local HTML path of a absolute path.

    Args:
        path: The absolute path

    Returns:
        Local HTML path
    """
    assert path.startswith(settings.html_path)
    return path[len(settings.html_path):]
