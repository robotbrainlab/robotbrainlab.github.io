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
4. Points step 1's primary Python resource at this site's own Python roadmap
   (data-intelligence/books/python-roadmap.html), which opens in a new tab.
5. Adds a dated note to the seven pages that record earlier research, design or review work,
   saying the tutorial they name has since been replaced. Their own text is left as written.
   These are the only changes made to the generated pages; the roadmap's own files are untouched.
6. Replaces data-intelligence/guide/ with the result.
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
OVERRIDE_VERSION = 10

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


# This site hosts its own Python roadmap (data-intelligence/books/python-roadmap.html), written
# for this curriculum: it sequences The Python Tutorial together with uv, ruff, mypy and pytest,
# and splits the language into Fundamentals, Advanced and Mastery. Where the roadmap source names
# the tutorial as a resource to read, the built page names this roadmap and the stage to read
# instead, and the link opens in a new tab. Prose that merely mentions the tutorial is content and
# is left exactly as written. The roadmap source itself is never modified.
LINK_OLD = (
    '<a href="https://docs.python.org/3/tutorial/" class="external" rel="noopener noreferrer">'
    '<em>The Python Tutorial</em><span class="visually-hidden" data-chrome> (external link)</span></a>'
)
LINK_NEW = (
    '<a href="../../../books/python-roadmap.html" class="external" target="_blank" rel="noopener">'
    '<em>Python Roadmap</em><span class="visually-hidden" data-chrome> (opens in a new tab)</span></a>'
)
# page -> list of (exact text in the generated page, its replacement).
PYTHON_SWAPS = {
    "learn/1-python-sql-and-data-analysis/index.html": [
        (LINK_OLD + '</span><span class="study-task"><strong>read:</strong> the complete tutorial.</span>',
         LINK_NEW + '</span><span class="study-task"><strong>read:</strong> the Fundamentals stage; '
                    'Advanced and Mastery as you need them.</span>'),
        ("<em>The Python Tutorial</em>, complete.</p>",
         "<em>Python Roadmap</em>, Fundamentals.</p>"),
        ("<em>The Python Tutorial</em>, errors and exceptions.</p>",
         "<em>Python Roadmap</em>, Fundamentals \u2014 errors and exceptions.</p>"),
        ("<em>The Python Tutorial</em>, virtual environments.</p>",
         "<em>Python Roadmap</em>, Fundamentals \u2014 environments and tooling.</p>"),
        ("<td><em>The Python Tutorial</em>, complete</td>",
         "<td><em>Python Roadmap</em>, Fundamentals</td>"),
    ],
    "learn/6-evaluation-and-testing/index.html": [
        (LINK_OLD + '</span><span class="study-task"><strong>revisit:</strong> chapter 6, \u00a710.11 and '
                    'chapter 12, read as part of the complete tutorial in '
                    '<a href="../1-python-sql-and-data-analysis/index.html">step 1</a>.</span>',
         LINK_NEW + '</span><span class="study-task"><strong>revisit:</strong> modules, testing and '
                    'environments in Fundamentals, read in '
                    '<a href="../1-python-sql-and-data-analysis/index.html">step 1</a>.</span>'),
        ("<em>The Python Tutorial</em> ch 6, revisited from step 1.</p>",
         "<em>Python Roadmap</em>, Fundamentals \u2014 modules and packages, revisited from step 1.</p>"),
        ("<em>The Python Tutorial</em> \u00a710.11 (quality control);",
         "<em>Python Roadmap</em>, Fundamentals \u2014 writing it properly;"),
        ("<em>The Python Tutorial</em> ch 12; <em>Designing Machine Learning Systems</em> ch 6.</p>",
         "<em>Python Roadmap</em>, Fundamentals \u2014 environments and tooling; "
         "<em>Designing Machine Learning Systems</em> ch 6.</p>"),
        ("<td><em>The Python Tutorial</em> ch 6, \u00a710.11, ch 12, revisited from step 1</td>",
         "<td><em>Python Roadmap</em>, Fundamentals, revisited from step 1</td>"),
    ],
    # The curriculum map: the assigned-resource row, the resource table (with its link) and the
    # reading plan all name a resource to read now, so they name this site's roadmap.
    "about/curriculum/index.html": [
        ("<td><em>The Python Tutorial</em> \u2014 <span class=\"role role--primary\">Primary</span>: "
         "the language tour",
         "<td><em>Python Roadmap</em> \u2014 <span class=\"role role--primary\">Primary</span>: "
         "the language, in stages"),
        ("<td>" + LINK_OLD + "</td>", "<td>" + LINK_NEW + "</td>"),
        ("<td><em>The Python Tutorial</em></td>\n<td>Complete</td>\n<td>E1</td>\n"
         "<td>A short, coherent tour of the language</td>",
         "<td><em>Python Roadmap</em></td>\n<td>Fundamentals</td>\n<td>E1</td>\n"
         "<td>A staged path through the language, with projects and exit criteria</td>"),
    ],
    # A learner material whose prerequisites point at step 6, which now names the roadmap.
    "learn/materials/ml-testing-checklist/index.html": [
        ("(<em>The Python Tutorial</em>, revisited in step 6)",
         "(<em>Python Roadmap</em>, revisited in step 6)"),
    ],
}


# Pages that record research, design or review work done on a stated date. Their own sentences
# describe that work and stay exactly as written: renaming the resource in them would claim the
# work examined something that did not exist yet. Instead each carries a dated note saying what
# has changed since. The note sits after the document's meta block, so the page reads: what kind
# of document this is, its title, when it was written, what has changed since.
NOTE_PAGES = (
    "research/2026-09-18-resource-coverage-audit/index.html",
    "research/2026-09-18-targeted-resource-research/index.html",
    "about/design/learner-guide/index.html",
    "about/design/curriculum-proposal/index.html",
    "about/history/roadmap-baseline-1/index.html",
    "about/history/roadmap-baseline-v0/index.html",
    "reviews/2026-09-20-learner-experience-review/index.html",
)
NOTE_DATE = "7 October 2026"
NOTE_ANCHOR = "</dl>"


def python_note(up: str) -> str:
    return (
        f'</dl><p class="ti-update"><strong>Update \u2014 {NOTE_DATE}:</strong> '
        "<em>The Python Tutorial</em> named on this page has been replaced across the guide by "
        f'this site\u2019s own <a href="{up}data-intelligence/books/python-roadmap.html" '
        'target="_blank" '
        'rel="noopener"><strong>Python Roadmap</strong></a>, researched and added on this date. '
        "It covers the language in full: Fundamentals, Advanced and Mastery.</p>"
    )


def add_python_note(html: str, page: str, up: str) -> str:
    """Date-stamp what changed on a page that records earlier work, leaving its own text alone."""
    if page not in NOTE_PAGES:
        return html
    found = html.count(NOTE_ANCHOR)
    if found != 1:
        sys.exit(f"Expected one {NOTE_ANCHOR} to put the note after, found {found}: {page}")
    return html.replace(NOTE_ANCHOR, python_note(up))


def swap_python_resource(html: str, page: str) -> str:
    """Name this site's own Python roadmap where the source names the language's tutorial."""
    for old, new in PYTHON_SWAPS.get(page, ()):
        found = html.count(old)
        if found != 1:
            sys.exit(f"Expected one {old[:48]!r}, found {found}, not patching: {page}")
        html = html.replace(old, new)
    return html


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
        html = swap_python_resource(html, rel)
        html = add_python_note(html, rel, up)
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
