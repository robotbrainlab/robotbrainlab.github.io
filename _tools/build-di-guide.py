#!/usr/bin/env python3
"""Build the Data & Intelligence guide from the AI Engineer Roadmap source.

Usage (from the repository root):

    python3 _tools/build-di-guide.py

1. Runs the roadmap's own generator (with its validation) into a temp directory.
   The roadmap source in _sources/ai-roadmap/ is only read, never modified.
2. Adds a "Towards Intelligence" link to each page's top bar, pointing back to
   the site home page, adds the site icon and the site theme override (theme/guide-override.css),
   and justifies the running text on the guide's home page.
3. Names the guide after the site's discipline ("Data & Intelligence") in its chrome, names the
   home page's two actions for where they go, and marks the bold-text sub-headings so they can
   be set ragged right.
   These are the only changes made to the generated pages; the roadmap's own files are untouched.
4. Replaces data-intelligence/guide/ with the result.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "_sources" / "ai-roadmap"
GUIDE = REPO / "data-intelligence" / "guide"
PYTHON = SOURCE / ".venv" / "bin" / "python"
# Site theme override for the guide (theme/guide-override.css). Bump when that file changes.
OVERRIDE_VERSION = 9

ANCHOR = '<div class="topbar-tools">'
STYLE = """<style>
  .ti-home { text-decoration: none; }
  @media (max-width: 700px) { .ti-home .tool-label { display: none; } }
</style>
</head>"""
# The guide's home page only: justify its running text. Its lists hold step names and
# titles rather than prose, and its lead is set larger than the body, so both stay ragged.
HOME_PAGE = "index.html"
HOME_STYLE = """<style>
  main.home p:not(.home-actions):not(.ti-subhead):not(.home-lead),
  .site-footer p { text-align: justify; hyphens: auto; }
</style>
</head>"""


# On this site the guide is the Data & Intelligence discipline, so its chrome carries that
# name rather than the roadmap's own: the top bar, the browser tab title and the home page's
# heading. Running text that names the roadmap is content and is left exactly as written.
ROADMAP_NAME = "AI Engineer Roadmap"
GUIDE_NAME = "Data &amp; Intelligence"
BRAND = f'<span class="brand-name">{ROADMAP_NAME}</span>'
HOME_HEADING = f'<h1 class="home-title">{ROADMAP_NAME}</h1>'
# A sub-page's tab title reads "<page> \u00b7 <guide>"; the home page's is the guide's name alone.
TAB_TITLE = re.compile(rf"(<title>(?:.*? \u00b7 )?){re.escape(ROADMAP_NAME)}</title>")
# The generator names the home page's primary action after the first step of the numbered path
# ("Start Fundamentals: ..."). Here it is named for where it goes, like the action beside it.
PRIMARY_ACTION = re.compile(r'(<a class="button button--primary" href="[^"]*">)[^<]*(<span aria-hidden)')
PRIMARY_LABEL = "Explore the roadmap "


# A Markdown sub-heading written as bold text comes through as a paragraph holding nothing but
# that bold run. It is a heading, not running text, so it is marked here and set ragged right in
# theme/guide-override.css: justifying a six-word line only stretches it into gaps. CSS alone
# cannot tell such a paragraph from one that merely opens with a bold lead-in, hence the marker.
SUBHEAD = re.compile(r"<p><strong>((?:(?!</strong>).)*?)</strong></p>", re.S)


def mark_subheads(html: str) -> str:
    return SUBHEAD.sub(r'<p class="ti-subhead"><strong>\g<1></strong></p>', html)


def rename(html: str, page: str, is_home: bool) -> str:
    """Give the guide the site's name for the discipline, in the chrome only."""
    def once(text: str, pattern: re.Pattern, replacement: str, what: str) -> str:
        patched, count = pattern.subn(replacement, text)
        if count != 1:
            sys.exit(f"Expected one {what}, found {count}, not patching: {page}")
        return patched

    if html.count(BRAND) != 1:
        sys.exit(f"Expected one top-bar brand, found {html.count(BRAND)}, not patching: {page}")
    html = html.replace(BRAND, f'<span class="brand-name">{GUIDE_NAME}</span>')
    html = once(html, TAB_TITLE, rf"\g<1>{GUIDE_NAME}</title>", "tab title")
    if is_home:
        if html.count(HOME_HEADING) != 1:
            sys.exit(f"Expected one home heading, not patching: {page}")
        html = html.replace(HOME_HEADING, f'<h1 class="home-title">{GUIDE_NAME}</h1>')
        html = once(html, PRIMARY_ACTION, rf"\g<1>{PRIMARY_LABEL}\g<2>", "primary action")
    return html


def home_link(rel_to_root: str) -> str:
    return (
        f'<div class="topbar-tools"><a class="tool-button ti-home" href="{rel_to_root}index.html" '
        'title="Back to Towards Intelligence" aria-label="Back to Towards Intelligence">'
        '<span aria-hidden="true">&larr;</span><span class="tool-label">Towards Intelligence</span></a>'
    )


def add_home_link(out: Path) -> int:
    patched = 0
    for page in sorted(out.rglob("*.html")):
        # Pages sit in data-intelligence/guide/<rel>; step up to the site root.
        depth = len(page.relative_to(out).parts) - 1 + 2
        html = page.read_text(encoding="utf-8")
        if html.count(ANCHOR) != 1 or html.count("</head>") != 1:
            sys.exit(f"Unexpected page structure, not patching: {page.relative_to(out)}")
        up = "../" * depth
        icon = f'<link rel="icon" type="image/svg+xml" href="{up}favicon/favicon.svg"/>\n'
        theme = f'<link rel="stylesheet" href="{up}theme/guide-override.css?v={OVERRIDE_VERSION}"/>\n'
        rel = page.relative_to(out).as_posix()
        html = html.replace(ANCHOR, home_link(up)).replace("</head>", icon + theme + STYLE)
        if rel == HOME_PAGE:
            html = html.replace("</head>", HOME_STYLE)
        html = mark_subheads(rename(html, rel, rel == HOME_PAGE))
        page.write_text(html, encoding="utf-8")
        patched += 1
    return patched


def main() -> None:
    if not PYTHON.exists():
        sys.exit(f"Missing {PYTHON}. Create it with:\n"
                 f"  cd {SOURCE} && python3.14 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "guide"
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        subprocess.run([str(PYTHON), "scripts/build_site.py", "--out", str(out)], cwd=SOURCE, env=env, check=True)
        print(f"Added the home link to {add_home_link(out)} pages")
        if GUIDE.exists():
            shutil.rmtree(GUIDE)
        shutil.copytree(out, GUIDE)
    print(f"Guide written to {GUIDE.relative_to(REPO)}")


if __name__ == "__main__":
    main()
