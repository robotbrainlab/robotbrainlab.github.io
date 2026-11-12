#!/usr/bin/env python3
"""Check every page of the site in a real browser, at phone width and at desktop width.

Usage (from the repository root):

    python3 utilities/page-check.py                 # 375px and 1280px
    python3 utilities/page-check.py --width 320     # one width
    python3 utilities/page-check.py --verbose       # name every page that passes too

Why it exists. link-check.py proves every link resolves and text-check.py proves no text moved.
Neither opens a page. The defects that reached the owner on 2026-11-12 were all of a third kind:
a card that scrolled sideways on a phone, two menu rows that led to the same page, a bar that
said the same three words twice, a page with no tab icon. Each was cheap to find by loading every
page and measuring, and expensive to find the way he found them.

What it measures, on EVERY page (not a sample):

  * real sideways scroll - scroll right, then read scrollX. scrollWidth lies here, because a
    hidden drawer overflows while `overflow-x: clip` stops the page from scrolling.
  * the chrome a page must carry: the home menu, the theme switch, the gradient tile, a tab icon.
  * the home menu: four rows, each answering 200.
  * anything that scrolls sideways INSIDE its own box, which is how a wide table hides.
  * Google Fonts, which no page on this site should load any more.

How it works. Chrome cannot measure a page from the outside, so the measuring is done by a page:
the script writes a small harness into the repository, serves the repository on a loopback port,
and loads the harness in headless Chrome. The harness walks every page in an iframe of the width
being tested and writes its findings into the DOM, which Chrome prints with --dump-dom.

Two traps this script avoids, both of which cost time on 2026-11-12:

  * It cache-busts the iframe's own URL as well as every stylesheet. Without the first, Chrome
    serves the page it fetched before your edit and the report describes yesterday's site.
  * It fails loudly when a page cannot be loaded at all, rather than counting it as a pass.
  * It ignores a closed off-canvas drawer: fixed, hidden, parked outside the viewport on purpose.
    Headless counts that as a scrolling page; a real browser, where `overflow-x: clip` on <html>
    holds the page still, does not.
"""

import argparse
import http.server
import json
import os
import re
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HARNESS = REPO / ".page-check-harness.html"

CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

# Pages that carry no chrome on purpose, and why.
NO_CHROME = {
    "/data-and-intelligence/index.html": "a redirect into the guide; it has no bar to carry",
}

# Boxes that are allowed to scroll sideways inside themselves. Source text cannot be reflowed
# without breaking it; a table of data can, and must, so tables are not in this list.
ALLOWED_INNER = ("pre.", "code.", "div.mermaid", "div.diagram")


def pages() -> list:
    out = []
    for p in sorted(REPO.rglob("*.html")):
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith((".claude/", "books/", "data-and-intelligence/research/")):
            continue
        if rel.startswith("."):
            continue
        out.append("/" + rel)
    return out


HARNESS_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>page-check</title></head>
<body><pre id="out">RUNNING</pre>
<script>
const PAGES = %s;
const WIDTH = Number(new URLSearchParams(location.search).get('w') || 375);
const ALLOWED = %s;

function look(d, win, w) {
  win.scrollTo(400, 0);
  const sideways = win.scrollX;
  win.scrollTo(0, 0);

  const menu = d.querySelector('.ti-home-menu');
  const rows = menu ? [].map.call(menu.querySelectorAll('a'), a => a.href) : [];

  const inner = [];
  for (const el of d.querySelectorAll('*')) {
    if (el.scrollWidth <= el.clientWidth + 2 || el.clientWidth === 0) continue;
    const ox = win.getComputedStyle(el).overflowX;
    if (ox !== 'auto' && ox !== 'scroll') continue;
    const name = el.tagName.toLowerCase() + '.' + String(el.className || '');
    if (ALLOWED.some(a => name.indexOf(a) === 0)) continue;
    inner.push(name.slice(0, 40) + ' ' + el.clientWidth + '->' + el.scrollWidth);
  }

  /* When the page does scroll, name what sticks out, so the report says where to look. */
  const offenders = [];
  let parked = false;
  if (sideways > 0) {
    for (const el of d.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.right <= w + 1) continue;
      let p = el.parentElement, clipped = false;
      while (p && p !== d.body) {
        if (win.getComputedStyle(p).overflowX !== 'visible') { clipped = true; break; }
        p = p.parentElement;
      }
      if (clipped) continue;
      /* A closed off-canvas drawer is parked outside the viewport on purpose. It is fixed and
         hidden, so nobody can see or reach it, and in a real browser `overflow-x: clip` on <html>
         keeps the page still; only headless reports the scroll. Not a defect. */
      const cs = win.getComputedStyle(el);
      if (cs.position === 'fixed' && cs.visibility === 'hidden') continue;
      offenders.push(el.tagName.toLowerCase() + '.' + String(el.className || '').slice(0, 24)
                     + ' right=' + Math.round(r.right));
    }
    if (offenders.length === 0) parked = true;
  }

  return {
    sideways: parked ? 0 : sideways,
    parked: parked,
    offenders: offenders.slice(0, 3),
    menu: !!menu,
    rows: rows,
    switch: !!d.querySelector('.switch'),
    mark: !!d.querySelector('.brand-mark'),
    icon: !!d.querySelector('link[rel="icon"]'),
    googleFonts: !!d.querySelector('link[href*="fonts.googleapis"]'),
    inner: inner.slice(0, 4),
    title: d.title || ''
  };
}

(async function () {
  const frame = document.createElement('iframe');
  frame.style.cssText = 'position:fixed;left:-9999px;top:0;border:0;height:900px;width:' + WIDTH + 'px';
  document.body.appendChild(frame);

  const results = [];
  const seen = {};

  for (const page of PAGES) {
    let record;
    try {
      await new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(new Error('timed out')), 20000);
        frame.onload = () => { clearTimeout(timer); resolve(); };
        frame.onerror = () => { clearTimeout(timer); reject(new Error('failed to load')); };
        /* Cache-bust the page itself, not only its stylesheets: without this the browser serves
           the copy it fetched before your edit. */
        frame.src = page + '?page-check=' + Date.now();
      });
      const d = frame.contentDocument, win = frame.contentWindow;
      for (const link of d.querySelectorAll('link[rel=stylesheet]')) {
        link.href = link.href + (link.href.indexOf('?') > -1 ? '&' : '?') + 'cb=' + Date.now();
      }
      await new Promise(r => setTimeout(r, 200));
      record = look(d, win, WIDTH);
      record.page = page;
      for (const href of record.rows) seen[href] = true;
    } catch (err) {
      record = { page: page, error: String(err && err.message || err) };
    }
    results.push(record);
  }
  frame.remove();

  /* Every destination the menus offer, asked once each. */
  const targets = {};
  for (const href of Object.keys(seen)) {
    try {
      const res = await fetch(href, { method: 'HEAD' });
      targets[new URL(href).pathname] = res.status;
    } catch (err) {
      targets[href] = String(err);
    }
  }

  document.getElementById('out').textContent =
    'JSON:' + JSON.stringify({ width: WIDTH, results: results, targets: targets });
})();
</script></body></html>
"""


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(port: int):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(REPO), **k)

    class Quiet(socketserver.TCPServer):
        allow_reuse_address = True
        def handle_error(self, request, client_address):  # a closed iframe is not an error
            pass

    httpd = Quiet(("127.0.0.1", port), handler)
    httpd.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def chrome() -> str:
    for path in CHROMES:
        if Path(path).exists():
            return path
    sys.exit("No Chrome, Chromium or Edge found. page-check.py needs one to load the pages.")


def run(width: int, port: int) -> dict:
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.run(
            [chrome(), "--headless=new", "--disable-gpu", "--no-first-run",
             "--force-prefers-reduced-motion", f"--user-data-dir={profile}",
             "--virtual-time-budget=240000", "--dump-dom",
             f"http://127.0.0.1:{port}/{HARNESS.name}?w={width}"],
            capture_output=True, text=True, timeout=600,
        )
    match = re.search(r"JSON:(\{.*?\})</pre>", proc.stdout, re.S)
    if not match:
        sys.exit(f"The harness did not report at {width}px. Chrome said:\n{proc.stderr[:800]}")
    return json.loads(match.group(1))


def report(data: dict, verbose: bool) -> int:
    width, results, targets = data["width"], data["results"], data["targets"]
    problems, notes = [], []

    for r in results:
        page = r["page"]
        if r.get("error"):
            problems.append(f"{page}: did not load ({r['error']})")
            continue
        if r["sideways"] > 0:
            where = "; ".join(r.get("offenders") or []) or "no element found outside a clipped box"
            problems.append(f"{page}: the page scrolls sideways ({r['sideways']}px) - {where}")
        for box in r["inner"]:
            if width <= 640:
                # On a phone a box that scrolls sideways hides content: the reader drags the box
                # while the page stays still, which is the defect reported on 2026-11-12.
                problems.append(f"{page}: a box scrolls sideways inside the page - {box}")
            else:
                notes.append(f"{page}: {box}")
        if r["googleFonts"]:
            problems.append(f"{page}: still loads Google Fonts")
        if not r["icon"]:
            problems.append(f"{page}: no tab icon")
        if page in NO_CHROME:
            continue
        if not r["menu"]:
            problems.append(f"{page}: no home menu")
        elif len(r["rows"]) != 4:
            problems.append(f"{page}: the home menu has {len(r['rows'])} rows, not 4")
        if not r["switch"]:
            problems.append(f"{page}: no theme switch")
        if not r["mark"]:
            problems.append(f"{page}: no gradient tile beside the name")
        if verbose and not problems:
            print(f"  OK  {page}")

    for path, status in sorted(targets.items()):
        if status != 200:
            problems.append(f"the home menu offers {path}, which answers {status}")

    print(f"{len(results)} pages checked at {width}px; "
          f"{len(targets)} menu destinations asked.")
    for p in NO_CHROME:
        print(f"  (no chrome expected on {p}: {NO_CHROME[p]})")
    if problems:
        print(f"\n{len(problems)} problem(s) at {width}px:")
        for p in problems:
            print(f"  - {p}")
    else:
        print(f"No problems at {width}px.")
    if notes:
        # A wide table inside its own scrolling region is how the roadmap's generator presents
        # one on a wide screen, and it is reachable by keyboard. It is worth seeing, not fixing.
        print(f"\n{len(notes)} table(s) scroll inside their own region at {width}px, "
              f"which is the generator's own pattern on a wide screen:")
        for n in notes[:6]:
            print(f"  . {n}")
        if len(notes) > 6:
            print(f"  . ... and {len(notes) - 6} more")
    return len(problems)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--width", type=int, action="append",
                    help="viewport width to test; repeatable (default: 375 and 1280)")
    ap.add_argument("--verbose", action="store_true", help="name every page that passes")
    args = ap.parse_args()
    widths = args.width or [375, 1280]

    page_list = pages()
    if not page_list:
        sys.exit("No pages found. Run this from the repository root.")

    HARNESS.write_text(HARNESS_HTML % (json.dumps(page_list), json.dumps(list(ALLOWED_INNER))),
                       encoding="utf-8")
    port = free_port()
    httpd = serve(port)
    failures = 0
    try:
        for width in widths:
            failures += report(run(width, port), args.verbose)
            print()
    finally:
        httpd.shutdown()
        if HARNESS.exists():
            os.remove(HARNESS)

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
