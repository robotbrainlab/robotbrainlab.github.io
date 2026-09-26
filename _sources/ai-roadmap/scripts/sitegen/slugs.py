"""GitHub-compatible heading slugs.

Anchors must be identical to the ones GitHub generates for the canonical
Markdown so that links are interchangeable between Markdown and HTML.
"""

import re

_REMOVE = re.compile(r"[^\w\- ]", re.UNICODE)


def github_slug(text: str) -> str:
    """Lowercase, drop punctuation (keeping hyphens), spaces become hyphens."""
    slug = _REMOVE.sub("", text.strip().lower())
    return slug.replace(" ", "-")


class Slugger:
    """Assigns unique slugs per document, suffixing duplicates like GitHub."""

    def __init__(self) -> None:
        self._seen: dict[str, int] = {}

    def slug(self, text: str) -> str:
        base = github_slug(text)
        if base not in self._seen:
            self._seen[base] = 0
            return base
        self._seen[base] += 1
        candidate = f"{base}-{self._seen[base]}"
        while candidate in self._seen:
            self._seen[base] += 1
            candidate = f"{base}-{self._seen[base]}"
        self._seen[candidate] = 0
        return candidate
