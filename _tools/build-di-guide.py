#!/usr/bin/env python3
"""Build the Data & Intelligence guide from the AI Engineer Roadmap source.

Usage (from the repository root):

    python3 _tools/build-di-guide.py

1. Runs the roadmap's own generator (with its validation) into a temp directory.
   The roadmap source in _sources/ai-roadmap/ is only read, never modified.
2. Adds a "Towards Intelligence" link to each page's top bar, pointing back to
   the site home page, adds the site icon and the site theme override (theme/guide-override.css),
   and justifies the running text on the guide's home page.
   These are the only changes made to the generated pages; the roadmap's own files are untouched.
3. Replaces data-intelligence/guide/ with the result.
"""

import os
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
OVERRIDE_VERSION = 6

ANCHOR = '<div class="topbar-tools">'
STYLE = """<style>
  .ti-home { text-decoration: none; }
  @media (max-width: 700px) { .ti-home .tool-label { display: none; } }
</style>
</head>"""
# The guide's home page only: justify all running text.
HOME_PAGE = "index.html"
HOME_STYLE = """<style>
  main.home p:not(.home-actions), main.home li, .site-footer p { text-align: justify; hyphens: auto; }
</style>
</head>"""


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
        html = html.replace(ANCHOR, home_link(up)).replace("</head>", icon + theme + STYLE)
        if page.relative_to(out).as_posix() == HOME_PAGE:
            html = html.replace("</head>", HOME_STYLE)
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
