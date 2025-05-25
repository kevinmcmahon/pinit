# ABOUTME: Wrapper for Pinboard API interactions
# ABOUTME: Handles bookmark creation and API communication

import json
from typing import Any

import pinboard


def add_bookmark(
    pb: pinboard.Pinboard,
    url: str,
    title: str,
    description: str | None = "",
    tags: list[str] | None = None,
    shared: bool = True,
    toread: bool = False,
) -> bool:
    """
    Add a bookmark to Pinboard.

    Args:
        pb: Pinboard API client instance
        url: The URL to bookmark
        title: The title of the bookmark
        description: Extended description (optional)
        tags: List of tags (optional)
        shared: Whether the bookmark is public (default: True)
        toread: Whether to mark as "to read" (default: False)

    Returns:
        True if successful, False otherwise
    """
    if tags is None:
        tags = []

    result = pb.posts.add(
        url=url,
        description=title,  # Pinboard calls the title "description"
        extended=description,  # Pinboard calls the description "extended"
        tags=tags,
        shared=shared,
        toread=toread,
    )

    return bool(result)


def add_bookmark_from_json(
    pb: pinboard.Pinboard, bookmark_data: str | dict[str, Any]
) -> bool:
    """
    Add a bookmark to Pinboard from JSON data.

    Args:
        pb: Pinboard API client instance
        bookmark_data: Either a JSON string or a dictionary with bookmark data

    Returns:
        True if successful, False otherwise
    """
    if isinstance(bookmark_data, str):
        data = json.loads(bookmark_data)
    else:
        data = bookmark_data

    return add_bookmark(
        pb=pb,
        url=data["url"],
        title=data["title"],
        description=data.get("description", ""),
        tags=data.get("tags", []),
    )

