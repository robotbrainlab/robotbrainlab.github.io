#!/usr/bin/env python3
"""Prove a restyle changed no content: compare a page's text and links with a git revision.

Usage (from the repository root):

    python3 _tools/text-check.py index.html            # working copy vs HEAD
    python3 _tools/text-check.py index.html --rev 683e3ce

Compared, in document order:
  - every text node in <head> <title> and <body> (scripts and styles excluded),
    with runs of ordinary whitespace collapsed; non-breaking spaces are kept exact
  - every href, plus the meta description/og tags and data-label tooltips
Exits 1 and prints the first differences if anything changed.
"""

import argparse
import difflib
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

WS = re.compile(r"[ \t\n\r\f]+")  # not \xa0: a non-breaking space is content
SKIP = {"script", "style"}
META = {"description", "og:title", "og:description"}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.in_title = False
        self.in_body = False
        self.items: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self.skip += 1
        elif tag == "title":
            self.in_title = True
        elif tag == "body":
            self.in_body = True
        elif tag == "meta" and (a.get("name") in META or a.get("property") in META):
            self.items.append(f"[meta {a.get('name') or a.get('property')}] {a.get('content')}")
        if "href" in a and tag == "a":
            self.items.append(f"[href] {a['href']}")
        if "data-label" in a:
            self.items.append(f"[data-label] {a['data-label']}")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip -= 1
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.skip or not (self.in_title or self.in_body):
            return
        text = WS.sub(" ", data).strip(" ")
        if text:
            self.items.append(("[title] " if self.in_title else "") + text)


def extract(html: str) -> list[str]:
    p = Extract()
    p.feed(html)
    return p.items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--rev", default="HEAD")
    args = ap.parse_args()
    old = subprocess.run(["git", "show", f"{args.rev}:{args.page}"], capture_output=True, text=True, check=True).stdout
    new = Path(args.page).read_text(encoding="utf-8")
    a, b = extract(old), extract(new)
    if a == b:
        print(f"OK  {args.page}: {len(a)} text/link items identical to {args.rev}")
        return 0
    print(f"CHANGED  {args.page} vs {args.rev}:")
    for line in list(difflib.unified_diff(a, b, "before", "after", lineterm="", n=1))[:60]:
        print("  " + line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
