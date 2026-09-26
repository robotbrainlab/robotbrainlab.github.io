#!/usr/bin/env python3
"""Check every internal link on the site: the target file exists, and a #fragment exists on it.

Usage (from the repository root):

    python3 _tools/link-check.py                 # all tracked, published pages (skips _ and . folders)
    python3 _tools/link-check.py cse/index.html  # just these pages

External links (http/https/mailto) are not fetched. Exits 1 on any broken link.
"""

import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parent.parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for key in ("href", "src"):
            if a.get(key) and tag in ("a", "link", "script", "img", "source"):
                self.hrefs.append(a[key])


_cache: dict[Path, Links] = {}


def parse(path: Path) -> Links:
    if path not in _cache:
        p = Links()
        p.feed(path.read_text(encoding="utf-8", errors="replace"))
        _cache[path] = p
    return _cache[path]


def published(path: Path) -> bool:
    return not any(part.startswith(("_", ".")) for part in path.relative_to(REPO).parts)


def main() -> int:
    tracked = subprocess.run(["git", "ls-files", "*.html"], cwd=REPO, capture_output=True, text=True, check=True).stdout.split()
    pages = [REPO / p for p in sys.argv[1:]] or sorted(REPO / p for p in tracked if published(REPO / p))
    broken = 0
    checked = 0
    for page in pages:
        for href in parse(page).hrefs:
            parts = urlsplit(href)
            if parts.scheme or href.startswith(("//", "mailto:", "javascript:", "data:")):
                continue
            checked += 1
            target = page if not parts.path else (page.parent / unquote(parts.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken += 1
                print(f"MISSING  {page.relative_to(REPO)} -> {href}")
                continue
            if parts.fragment and target.suffix == ".html":
                if unquote(parts.fragment) not in parse(target).ids:
                    broken += 1
                    print(f"NO ANCHOR  {page.relative_to(REPO)} -> {href}")
    print(f"{checked} internal links on {len(pages)} pages checked, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
