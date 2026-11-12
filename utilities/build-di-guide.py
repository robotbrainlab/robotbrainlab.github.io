#!/usr/bin/env python3
"""Build the Data & Intelligence guide from the AI Engineer Roadmap source.

Usage (from the repository root):

    python3 utilities/build-di-guide.py

1. Runs the roadmap's own generator (with its validation) into a temp directory.
   The roadmap source in data-and-intelligence/research/ is only read, never modified.
2. Adds a home button to each page's top bar, holding the site home page and the three
   disciplines, adds the site icon and the site theme override (assets/theme/guide-override.css),
   and justifies the running text on the guide's home page.
3. Names the guide after the site's discipline ("Data & Intelligence") in its chrome, names the
   home page's two actions for where they go, and marks the bold-text sub-headings so they can
   be set ragged right.
4. Points step 1's primary Python resource at this site's own Python roadmap
   (data-and-intelligence/books/python-roadmap.html), which opens in a new tab.
5. Adds a dated note to the seven pages that record earlier research, design or review work,
   saying the tutorial they name has since been replaced. Their own text is left as written.
   These are the only changes made to the generated pages; the roadmap's own files are untouched.
6. Adds an "The On-Ramp" button to the guide's home page, left of its primary action, linking to
   data-and-intelligence/on-ramp.html.
7. Writes a comment at the top of every page saying the page is generated and that a hand
   edit to it is erased by the next build.
8. Replaces the guide's three-state theme button with the site's own two-state switch, and
   joins the two theme memories. The site stores the chosen theme as "ti-theme", the guide as
   "air-theme", so before this each side ignored the other and the theme changed when you
   crossed between them. Every page gets a small script that mirrors one into the other.
9. Replaces data-intelligence/guide/ with the result.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data-and-intelligence" / "research"   # [2026-11-11] was research/ai-roadmap
GUIDE = REPO / "data-and-intelligence" / "guide"
PYTHON = SOURCE / ".venv" / "bin" / "python"
# Site theme override for the guide (assets/theme/guide-override.css). Bump when that file changes.
OVERRIDE_VERSION = 18

# The site and the guide each remember the chosen theme under their own name: the site as
# "ti-theme" (assets/theme/site.js), the guide as "air-theme" (its own generated script). Neither
# read the other, so the theme changed as you crossed between them. This mirrors each into the
# other. It runs in the head, before first paint, so an arriving choice is applied without a
# flash. The site half of the bridge is in assets/theme/site.js.
THEME_BRIDGE = """<script>
(function () {
  var root = document.documentElement, SITE = "ti-theme", GUIDE = "air-theme";
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  /* Arrived from a site page that chose a theme this guide has not been told about. The guide
     stores the choice under its own name, so write it there too and the guide's own script
     agrees with the switch from the first paint. */
  var guide = get(GUIDE), site = get(SITE);
  if (guide !== "light" && guide !== "dark" && (site === "light" || site === "dark")) {
    set(GUIDE, site);
    root.setAttribute("data-theme", site);
  }
  /* The switch itself: two states, the same as every other page on the site. */
  function current() {
    var now = root.getAttribute("data-theme");
    if (now === "dark" || now === "light") return now;
    return (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }
  function menu() {
    var wrap = document.querySelector(".ti-home-menu");
    if (!wrap) return;
    var open = wrap.querySelector(".ti-home-btn"), list = wrap.querySelector(".ti-home-list");
    function shut() { list.hidden = true; open.setAttribute("aria-expanded", "false"); }
    open.addEventListener("click", function (ev) {
      ev.stopPropagation();
      if (list.hidden) { list.hidden = false; open.setAttribute("aria-expanded", "true"); }
      else shut();
    });
    document.addEventListener("click", function (ev) { if (!wrap.contains(ev.target)) shut(); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") shut(); });
  }
  function start() {
    menu();
    var btn = document.getElementById("tiThemeSwitch");
    if (!btn) return;
    function sync() { btn.setAttribute("aria-checked", current() === "dark" ? "true" : "false"); }
    sync();
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      set(SITE, next);
      set(GUIDE, next);
      sync();
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
</script>
"""


# The site carries one theme control on every page: a two-state switch. The guide's generator
# writes a three-state button instead (System / Light / Dark) with the state spelled out beside
# it, which is a different control in a different shape. The site's own switch is put in its
# place here, markup and behaviour, so both sides of the boundary carry the same thing. The
# roadmap's own button is replaced, not hidden; its script then finds no [data-theme-toggle] and
# leaves the theme alone, which is what we want, because the switch below drives it.
THEME_BUTTON = (
    '<button class="tool-button theme-toggle" type="button" data-theme-toggle '
    'aria-label="Theme: System. Activate to change.">\n'
    '        <span class="theme-glyph" aria-hidden="true"></span>'
    '<span class="tool-label theme-label">System</span>\n'
    '      </button>'
)
THEME_SWITCH = """<button class="switch" id="tiThemeSwitch" type="button" role="switch"
              aria-checked="false" aria-label="Dark mode" title="Toggle dark mode">
        <span class="knob">
          <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="4.2" fill="currentColor"/>
            <path d="M12 2v2.5M12 19.5V22M4.2 4.2 6 6M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8 6 18M18 6l1.8-1.8"/>
          </svg>
          <svg class="moon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20.5 14.6A8.5 8.5 0 0 1 9.4 3.5a8.5 8.5 0 1 0 11.1 11.1Z"/>
          </svg>
        </span>
      </button>"""


def swap_theme_control(html: str, page: str) -> str:
    """Put the site's switch where the guide's three-state button was."""
    found = html.count(THEME_BUTTON)
    if found != 1:
        sys.exit(f"Expected one theme button, found {found}, not patching: {page}")
    return html.replace(THEME_BUTTON, THEME_SWITCH)

ANCHOR = '<div class="topbar-tools">'
# Everything the bar needs is in assets/theme/guide-override.css; nothing is left to say here.
STYLE = "</head>"
# The guide's home page only: one button into the on-ramp, beside the roadmap's own two. The full
# table lives at data-and-intelligence/on-ramp.html in the site theme. A bare "button" is the
# roadmap's own neutral outline style, so this needs no CSS of its own and stays secondary to the
# primary action it sits left of.
ON_RAMP_ANCHOR = (
    '<p class="home-actions" data-chrome>\n'
    '      <a class="button button--primary"'
)
ON_RAMP = (
    '<p class="home-actions" data-chrome>\n'
    '      <a class="button" href="../on-ramp.html">The On-Ramp <span aria-hidden="true">&rarr;</span></a>\n'
    '      <a class="button button--primary"'
)


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


# This site hosts its own Python roadmap (data-and-intelligence/books/python-roadmap.html), written
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
        f'this site\u2019s own <a href="{up}data-and-intelligence/books/python-roadmap.html" '
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
# assets/theme/guide-override.css: justifying a six-word line only stretches it into gaps. CSS alone
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


def add_on_ramp(html: str, page: str) -> str:
    """The guide's home page only: the on-ramp button, left of the roadmap's primary action."""
    if html.count(ON_RAMP_ANCHOR) != 1:
        sys.exit(f"Expected one on-ramp anchor, found {html.count(ON_RAMP_ANCHOR)}, not patching: {page}")
    return html.replace(ON_RAMP_ANCHOR, ON_RAMP)


# Not one of the 75 pages said it was generated, so a hand edit to any of them looked like
# ordinary work and was erased, silently, by the next build (main() deletes the whole folder and
# writes it again). This goes at the top of every page, where anyone who opens the file sees it
# first. It changes nothing a reader sees.
MARKER = (
    "<!-- Made by utilities/build-di-guide.py from data-and-intelligence/research/.\n"
    "     Hand edits to this file are erased by the next build. Edit the source instead. -->\n"
)


def add_marker(html: str, page: str) -> str:
    """Say, in the file itself, that the file is generated."""
    # The generator writes it lower case; accept either, and stop if it is neither, rather than
    # putting the comment somewhere a browser would show it.
    if not html.lstrip()[:15].lower().startswith("<!doctype html>"):
        sys.exit(f"Page does not start with a doctype, not patching: {page}")
    return MARKER + html

def home_link(rel_to_root: str) -> str:
    """The site's four destinations, behind one home button.

    This was a single back arrow reading "Towards Intelligence". Every site page instead carries
    the three disciplines as plain links, so the guide was the odd one out; but the guide's bar
    already holds its own sections (Learn, Evidence, About) and cannot hold three more and still
    fit a phone. One home button with a menu holds all four and takes the width of an icon.

    Each row goes to that discipline's own page, not to a section of the home page. The site's own
    nav sends Mathematics to index.html#mathematics, and in a menu that reads as a broken link:
    two of the four rows land on the same page and only the scroll position differs.
    """
    up = rel_to_root
    return (
        '<div class="topbar-tools"><div class="ti-home-menu">'
        '<button class="ti-home-btn" type="button" aria-expanded="false" aria-haspopup="true" '
        'title="Towards Intelligence" aria-label="Towards Intelligence">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M3 10.2 12 3l9 7.2"/><path d="M5.4 9v11h13.2V9"/></svg>'
        '</button>'
        '<ul class="ti-home-list" hidden>'
        f'<li><a class="ti-root" href="{up}index.html">Home page</a></li>'
        f'<li><a href="{up}mathematics/index.html">Mathematics</a></li>'
        f'<li><a href="{up}cse/index.html">CS &amp; Engineering</a></li>'
        f'<li><a class="ti-current" href="{up}data-and-intelligence/guide/index.html">Data &amp; Intelligence</a></li>'
        '</ul></div>'
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
        icon = f'<link rel="icon" type="image/svg+xml" href="{up}assets/favicon/favicon.svg"/>\n'
        theme = f'<link rel="stylesheet" href="{up}assets/theme/guide-override.css?v={OVERRIDE_VERSION}"/>\n'
        rel = page.relative_to(out).as_posix()
        html = html.replace(ANCHOR, home_link(up)).replace("</head>", icon + theme + THEME_BRIDGE + STYLE)
        if rel == HOME_PAGE:
            html = html.replace("</head>", HOME_STYLE)
        html = add_marker(html, rel)
        html = swap_theme_control(html, rel)
        html = mark_subheads(rename(html, rel, rel == HOME_PAGE))
        # After rename(), deliberately: the section carries a button--primary of its own, and
        # rename() asserts the home page has exactly one. Injecting first makes that check fail.
        if rel == HOME_PAGE:
            html = add_on_ramp(html, rel)
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
