"""Build validation (AD3): practical checks, not a framework."""

from __future__ import annotations

import posixpath
import re
from collections import Counter
from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .markdown import MarkdownDocument, create_parser, is_literal_placeholder

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
OPTIONAL_CLOSE = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "option"}
REMOTE = re.compile(r"^(?:https?:)?//", re.I)
WORD = re.compile(r"\w+", re.UNICODE)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    passed: list[str] = field(default_factory=list)

    def check(self, ok: bool, label: str, detail: str = "", warn: bool = False) -> None:
        if ok:
            self.passed.append(label)
        elif warn:
            self.warnings.append(f"{label}: {detail}")
        else:
            self.errors.append(f"{label}: {detail}")

    def print(self) -> None:
        print(f"Validation: {len(self.passed)} passed, {len(self.warnings)} warnings, {len(self.errors)} errors")
        for w in self.warnings:
            print(f"  warning  {w}")
        for e in self.errors:
            print(f"  ERROR    {e}")


NON_TEXT = {"script", "style", "title", "head"}


class _TextExtractor(HTMLParser):
    """Collects visible text.

    mode "content" skips subtrees marked as presentation chrome (``data-chrome``);
    mode "chrome" collects only those subtrees; mode "all" collects both.
    """

    def __init__(self, mode: str = "content") -> None:
        super().__init__(convert_charrefs=True)
        self.mode = mode
        self.parts: list[str] = []
        self.stack: list[tuple[str, bool]] = []
        self.skip_depth = 0
        self.hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        chrome = any(name == "data-chrome" for name, _ in attrs)
        if tag in NON_TEXT:
            self.hidden_depth += 1
        if tag in VOID:
            return
        self.stack.append((tag, chrome))
        if chrome:
            self.skip_depth += 1

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        if tag in NON_TEXT:
            self.hidden_depth = max(0, self.hidden_depth - 1)
        if tag in VOID:
            return
        while self.stack:
            open_tag, chrome = self.stack.pop()
            if chrome:
                self.skip_depth -= 1
            if open_tag == tag:
                break

    def handle_data(self, data):
        if self.hidden_depth:
            return
        in_chrome = self.skip_depth > 0
        if self.mode == "all" or (self.mode == "chrome") == in_chrome:
            self.parts.append(data)


def visible_text(html: str, mode: str = "content") -> str:
    parser = _TextExtractor(mode)
    parser.feed(html)
    return " ".join(parser.parts)


def text_words(html: str, mode: str = "content") -> Counter:
    return Counter(WORD.findall(visible_text(html, mode)))


def _reference_parser():
    """A plain Markdown renderer; placeholders such as <date> are shown as text."""
    md = create_parser()

    def html_inline(self, tokens, idx, options, env):
        content = tokens[idx].content
        return escape(content) if is_literal_placeholder(content) else content

    md.add_render_rule("html_inline", html_inline)
    return md


def source_sequence(doc: MarkdownDocument) -> list[str]:
    """Words of a canonical document, in order, as a plain renderer presents them."""
    return WORD.findall(visible_text(_reference_parser().render(doc.source)))


def source_words(doc: MarkdownDocument) -> Counter:
    return Counter(source_sequence(doc))


def wording_preserved(report: ValidationReport, doc: MarkdownDocument, rendered_body: str) -> None:
    """Canonical wording must survive presentation unchanged and in order."""
    reference = source_sequence(doc)
    generated = WORD.findall(visible_text(rendered_body))
    detail = ""
    if reference != generated:
        k = next((i for i, (a, b) in enumerate(zip(reference, generated)) if a != b),
                 min(len(reference), len(generated)))
        detail = (f"first difference at word {k}: source={reference[max(0, k - 4):k + 4]} "
                  f"rendered={generated[max(0, k - 4):k + 4]} (lengths {len(reference)}, {len(generated)})")
    report.check(reference == generated, f"wording preserved in order: {doc.rel_path}", detail)


def guide_wording_preserved(report: ValidationReport, doc: MarkdownDocument, heading, blocks, rendered_body: str,
                            page_rel: str) -> None:
    """A guide page presents its section of the guide word for word, in order.

    The reference is the step's heading and content blocks, cut from the source
    by line and rendered by a plain renderer; Markdown-only navigation is excluded
    on both sides.
    """
    lines = doc.source.splitlines(keepends=True)
    chunks = []
    for start in [heading.index] + [b.start for b in blocks]:
        first, last = doc.tokens[start].map
        chunks.append("".join(lines[first:last]))
    reference = WORD.findall(visible_text(_reference_parser().render("\n\n".join(chunks))))
    generated = WORD.findall(visible_text(rendered_body))
    detail = ""
    if reference != generated:
        k = next((i for i, (a, b) in enumerate(zip(reference, generated)) if a != b),
                 min(len(reference), len(generated)))
        detail = (f"first difference at word {k}: source={reference[max(0, k - 4):k + 4]} "
                  f"rendered={generated[max(0, k - 4):k + 4]} (lengths {len(reference)}, {len(generated)})")
    report.check(reference == generated, f"guide wording preserved in order: {page_rel}", detail)


def ids_absent(report: ValidationReport, page_rel: str, page_html: str, pattern: str) -> None:
    """Internal curriculum identifiers never reach a learner page."""
    found = sorted(set(re.findall(pattern, visible_text(page_html, "all"))))
    report.check(not found, f"no internal curriculum identifiers: {page_rel}", f"found={found}")


FIFTH_LEVEL = re.compile(r"(?<!not a )(?<!not the )\bfifth (?:depth )?(?:stage|level)\b|\b(?:level|stage) 5\b", re.I)
# "Research" as the depth level (capitalized), not "research literacy" or "research contribution".
AFTER_RESEARCH = re.compile(r"\b[Aa]fter (?:you (?:finish|complete) |completing |finishing )?Research\b(?! literacy| contribution)")
RETIRED_MARKERS = ("modern-badge", "modern-tag", "modern-dot")


class _ShapeParser(HTMLParser):
    """Collects the parts of a page that show how the learner's area is structured."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool, bool]] = []  # tag, in area nav, in rail group
        self.groups: list[str] = []
        self.tracks: list[str] = []  # top-level sections of the area nav ("Depth path", …)
        self.group_track: list[int] = []  # index into tracks for each group
        self.links: list[str] = []
        self.link_track: list[int] = []
        self.numbered_track: list[int] = []  # track of each numbered entry
        self.primary: list[str] = []
        self.in_primary = 0
        self.in_track = False
        self.actions: list[str] = []  # links in Home's hero actions
        self.in_actions = 0
        self.area_navs = 0
        self.page_tocs = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        parent = self.stack[-1] if self.stack else ("", False, False)
        in_nav = parent[1] or (tag == "nav" and "area-nav" in cls)
        in_group = tag == "p" and in_nav and "rail-group" in cls
        self.in_track = tag == "p" and in_nav and "rail-track" in cls
        if self.in_track:
            self.tracks.append("")
        if in_group:
            self.groups.append("")
            self.group_track.append(len(self.tracks) - 1)
        if in_nav and tag == "a" and "area-link" in cls:
            self.links.append(a.get("href") or "")
            self.link_track.append(len(self.tracks) - 1)
        if in_nav and tag == "span" and "area-link-num" in cls:
            self.numbered_track.append(len(self.tracks) - 1)
        if tag == "nav" and "area-nav" in cls:
            self.area_navs += 1
        if tag == "nav" and "page-toc" in cls:
            self.page_tocs += 1
        if tag == "p" and "home-actions" in cls:
            self.in_actions += 1
        elif self.in_actions and tag == "a":
            self.actions.append(a.get("href") or "")
        if tag == "nav" and a.get("aria-label") == "Primary":
            self.in_primary += 1
            self.primary.append("")
        elif self.in_primary and tag == "a":
            self.primary.append("")
        self.stack.append((tag, in_nav, in_group or parent[2]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            if self.stack.pop()[0] == tag:
                break
        if tag == "nav" and self.in_primary:
            self.in_primary -= 1
        if tag == "p":
            self.in_track = False
            self.in_actions = 0

    def handle_data(self, data):
        if self.in_track and self.tracks:
            self.tracks[-1] += data
        if self.stack and self.stack[-1][2]:
            self.groups[-1] += data
        if self.in_primary and self.primary:
            self.primary[-1] += data


def parallel_track_presented(report: ValidationReport, page_rel: str, page_html: str, is_home: bool,
                             is_learn: bool, expected_tracks: list[str], expected_groups: list[str], entries: int,
                             modern_page: str, learn_prefix: str) -> None:
    """Modern AI Engineering is a parallel curriculum beside the Depth path: never a fifth depth
    level, never placed after Research, never numbered, and never behind Evidence or About."""
    text = " ".join(visible_text(page_html, "all").split())
    found = FIFTH_LEVEL.findall(text)
    report.check(not found, f"Modern AI Engineering is never a fifth depth level: {page_rel}", f"found={found}")
    late = [m.group(0) for m in AFTER_RESEARCH.finditer(text) if "not" not in text[max(0, m.start() - 24):m.start()]]
    report.check(not late, f"Modern AI Engineering is never placed after Research: {page_rel}", f"found={late}")
    leftover = [c for c in RETIRED_MARKERS if c in page_html]
    report.check(not leftover, f"no per-step Modern AI Engineering badges, tags or dots: {page_rel}",
                 f"found={leftover}")
    shape = _ShapeParser()
    shape.feed(page_html)
    base = posixpath.dirname(page_rel)
    resolve = lambda h: posixpath.normpath(posixpath.join(base, h.partition("#")[0]))  # noqa: E731
    if is_home:
        actions = [resolve(h) for h in shape.actions]
        ok = modern_page in actions and actions and all(a.startswith(learn_prefix) for a in actions)
        report.check(ok, "Home's first actions start learning: the Depth path and Modern AI Engineering, "
                         "with Evidence and About secondary", f"actions={actions}")
    if is_learn:
        tracks = [" ".join(x.split()) for x in shape.tracks]
        groups = [" ".join(g.split()) for g in shape.groups]
        modern = len(tracks) - 1
        problems = []
        if tracks != expected_tracks:
            problems.append(f"tracks={tracks}")
        if groups != expected_groups or any(k != 0 for k in shape.group_track):
            problems.append(f"Depth sections={groups}")
        if len(shape.links) != entries:
            problems.append(f"entries={len(shape.links)} (expected {entries})")
        if modern in shape.numbered_track:
            problems.append("Modern AI Engineering entries are numbered")
        if shape.area_navs != 1 or shape.page_tocs:
            problems.append(f"navigation panels: {shape.area_navs} area, {shape.page_tocs} page contents")
        report.check(not problems, f"Learn shows two parallel tracks and one navigation: {page_rel}",
                     "; ".join(problems))


class _UnitParser(HTMLParser):
    """The unit's own contents and the sections it should match."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.toc: list[str] = []      # hrefs in the unit contents, in order
        self.sections: list[str] = []  # ids of the unit's area and concept headings, in order
        self.toc_at = -1
        self.study_at = -1
        self.navs = 0
        self.in_toc = False
        self.in_unit = False
        self.n = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.n += 1
        if tag == "nav" and "unit-toc" in cls:
            self.in_toc, self.toc_at, self.navs = True, self.n, self.navs + 1
        if self.in_toc and tag == "a":
            self.toc.append((a.get("href") or "").lstrip("#"))
        if tag == "section" and ("unit-area" in cls or "unit-concept" in cls):
            self.in_unit = True
        if tag in ("h2", "h3") and a.get("id") and self.in_unit:
            self.sections.append(a["id"])
            self.in_unit = False
        if tag == "section" and "guide-block--study" in cls and self.study_at < 0:
            self.study_at = self.n

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_toc:
            self.in_toc = False


def unit_contents_match_sections(report: ValidationReport, page_rel: str, page_html: str) -> None:
    """A unit's contents is generated from its sections: same entries, same order, before the reading."""
    p = _UnitParser()
    p.feed(page_html)
    if not p.toc and not p.sections:
        return
    problems = []
    if p.toc != p.sections:
        missing = [s for s in p.sections if s not in p.toc]
        extra = [s for s in p.toc if s not in p.sections]
        problems.append(f"contents and sections differ (missing from contents: {missing[:3]}, "
                        f"with no section: {extra[:3]})")
    if p.navs != 1:
        problems.append(f"{p.navs} unit contents on the page")
    if p.study_at >= 0 and p.toc_at > p.study_at:
        problems.append("the contents comes after the reading")
    report.check(not problems, f"the unit's contents matches its sections: {page_rel}", "; ".join(problems))


def primary_nav_is(report: ValidationReport, page_rel: str, page_html: str, labels: list[str],
                   expected: list[str]) -> None:
    shape = _ShapeParser()
    shape.feed(page_html)
    found = [" ".join(p.split()) for p in shape.primary if p.strip()]
    report.check(labels == expected and found == expected, f"top-level navigation is {' | '.join(expected)}: {page_rel}",
                 f"configured={labels} rendered={found}")


def _hrefs(html: str) -> list[str]:
    return re.findall(r'<a [^>]*href="([^"]+)"', html)


def words_from_sources(report: ValidationReport, page_rel: str, page_html: str, docs: list[MarkdownDocument]) -> None:
    """Every word a page presents as content comes from its canonical sources.

    Interface text must be marked ``data-chrome``; anything else on the page is
    treated as canonical content and must exist in the sources it draws on.
    """
    vocabulary: set[str] = set()
    for doc in docs:
        vocabulary.update(source_words(doc))
    foreign = sorted(set(text_words(page_html)) - vocabulary)
    report.check(not foreign, f"content words come from canonical sources: {page_rel}", f"unsourced={foreign[:12]}")


def stale_phrases_absent(report: ValidationReport, page_rel: str, page_html: str, phrases: list[str],
                         all_text: bool) -> None:
    """Superseded status wording must not reach learners or the interface."""
    text = " ".join(visible_text(page_html, "all" if all_text else "chrome").split()).casefold()
    found = [p for p in phrases if p.casefold() in text]
    scope = "page text" if all_text else "interface text"
    report.check(not found, f"no stale status wording in {scope}: {page_rel}", f"found={found}")


class _StructureCounter(HTMLParser):
    """Counts structural elements outside chrome subtrees."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.counts: Counter = Counter()
        self.ids: set[str] = set()
        self.stack: list[bool] = []
        self.chrome = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        chrome = "data-chrome" in a
        if tag not in VOID:
            self.stack.append(chrome)
            if chrome:
                self.chrome += 1
        if self.chrome:
            return
        cls = (a.get("class") or "").split()
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "table", "ol", "ul", "blockquote", "hr"):
            self.counts[tag] += 1
        elif tag == "figure" and "data-diagram" in a:
            self.counts["diagram"] += 1
        elif tag == "div" and "code-block" in cls:
            self.counts["code"] += 1
        elif tag == "a" and "heading-anchor" not in cls:
            self.counts["link"] += 1
        elif tag == "span" and "link-unavailable" in cls:
            self.counts["link"] += 1

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        if self.stack.pop():
            self.chrome -= 1


def structure_preserved(report: ValidationReport, doc: MarkdownDocument, rendered_body: str) -> None:
    """Headings, tables, lists, quotes, diagrams, code, rules and links survive rendering."""
    expected: Counter = Counter()
    for t in doc.tokens:
        if t.type == "heading_open":
            expected[t.tag] += 1
        elif t.type in ("table_open", "blockquote_open"):
            expected[t.type[:-5]] += 1
        elif t.type == "ordered_list_open":
            expected["ol"] += 1
        elif t.type == "bullet_list_open":
            expected["ul"] += 1
        elif t.type == "hr":
            expected["hr"] += 1
        elif t.type == "fence":
            expected["diagram" if t.info.strip().split()[:1] == ["mermaid"] else "code"] += 1
        elif t.type == "code_block":
            expected["code"] += 1
        elif t.type == "inline":
            expected["link"] += sum(1 for c in t.children or [] if c.type == "link_open")
    counter = _StructureCounter()
    counter.feed(rendered_body)
    diff = {k: (expected[k], counter.counts[k]) for k in set(expected) | set(counter.counts)
            if expected[k] != counter.counts[k]}
    report.check(not diff, f"structure preserved: {doc.rel_path}", f"(source, rendered)={diff}")
    missing = [h.slug for h in doc.headings if h.slug not in counter.ids]
    report.check(not missing, f"heading anchors preserved: {doc.rel_path}", f"missing={missing[:8]}")


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.assets: list[str] = []
        self.counts: Counter = Counter()
        self.html_lang = False
        self.stack: list[str] = []
        self.mismatches: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.counts[tag] += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "html" and a.get("lang"):
            self.html_lang = True
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href"):
            self.assets.append(a["href"])
        if tag == "img" and a.get("src"):
            self.assets.append(a["src"])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack and self.stack[-1] != tag and self.stack[-1] in OPTIONAL_CLOSE:
            self.stack.pop()
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.mismatches.append(tag)


def _parse(path: Path) -> _PageParser:
    parser = _PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def journey_pager_follows(report: ValidationReport, site: Path, order: list[str], landing: str) -> None:
    """The primary pager walks the one journey, unit by unit.

    The learner guide states a single route through the Depth path and its Modern detours.
    This check reads the generated pages and fails the build if the site's own forward and
    backward controls would take a learner anywhere else — skipping a required detour,
    jumping ahead of a topic's prerequisites, or leaving a page with no way onward.
    """
    link = re.compile(r'<a[^>]*class="[^"]*guide-pager-link--(prev|next)[^"]*"[^>]*href="([^"]+)"', re.S)
    problems: list[str] = []
    for k, rel in enumerate(order):
        path = site / rel
        if not path.is_file():
            problems.append(f"{rel}: missing")
            continue
        found = {kind: (path.parent / href).resolve() for kind, href in link.findall(path.read_text("utf-8"))}
        for kind, step in (("prev", -1), ("next", 1)):
            neighbour = order[k + step] if 0 <= k + step < len(order) else landing
            expected = (site / neighbour).resolve()
            actual = found.get(kind)
            if actual is None:
                problems.append(f"{rel}: no {kind} control")
            elif actual != expected:
                problems.append(f"{rel}: {kind} leads to {actual.relative_to(site.resolve()).as_posix()}, "
                                f"not {neighbour}")
    report.check(not problems, "the primary pager follows the canonical learner journey",
                 "; ".join(problems[:6]))


def typography_policy(report: ValidationReport, site: Path, justified: list[str]) -> None:
    """Justification is for long-form prose, and only where the measure is wide enough.

    The earlier policy justified every piece of text on the site, which stretched headings,
    navigation, labels and table cells into uneven gaps and left narrow screens full of
    rivers. These checks hold the replacement: nothing but the declared prose selectors may
    justify text, and that prose must fall back to ragged right on a narrow measure.
    """
    css = "\n".join(f.read_text(encoding="utf-8") for f in site.rglob("*.css") if "vendor" not in f.parts)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules = [(" ".join(sel.split()), body) for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)]
    stray = sorted({sel for sel, body in rules
                    if re.search(r"text-align\s*:\s*justify", body) and sel not in justified})
    report.check(not stray, "only long-form prose is justified", f"also justified: {stray[:4]}")

    narrow = [block for block in re.findall(r"@media[^{]*max-width[^{]*\{(.*?)\n\}", css, re.S)]
    ragged = any(re.search(r"text-align\s*:\s*left", block) and all(s.split(",")[0] in block for s in justified[:1])
                 for block in narrow)
    report.check(ragged, "justified prose falls back to ragged right on a narrow measure",
                 "no max-width rule sets the prose selectors left-aligned")


def validate_site(report: ValidationReport, site: Path, required_pages: list[str],
                  justified_selectors: list[str]) -> None:
    pages = {p.relative_to(site).as_posix(): _parse(p) for p in site.rglob("*.html") if "vendor" not in p.parts}

    for rel in required_pages:
        path = site / rel
        report.check(path.is_file() and path.stat().st_size > 0, f"page generated: {rel}", "missing or empty")

    typography_policy(report, site, justified_selectors)
    for p in site.rglob("*.html"):
        if "vendor" in p.parts:
            continue
        html = p.read_text(encoding="utf-8")
        styling = " ".join(re.findall(r'style="([^"]*)"', html) + re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
        found = re.findall(r"text-align\s*:\s*[\w-]+", styling) + re.findall(r'<[a-z][^>]*\salign="[^"]*"', html)
        report.check(not found, f"alignment is left to the stylesheet: {p.relative_to(site).as_posix()}",
                     f"found={found[:3]}")

    for rel, page in sorted(pages.items()):
        report.check(page.counts["main"] == 1, f"one <main>: {rel}", f"found {page.counts['main']}")
        report.check(page.counts["h1"] == 1, f"one <h1>: {rel}", f"found {page.counts['h1']}")
        report.check(page.html_lang, f"html lang attribute: {rel}", "missing")
        report.check(page.counts["title"] == 1, f"<title>: {rel}", "missing")
        leftover = [t for t in page.stack if t not in OPTIONAL_CLOSE]
        report.check(not page.mismatches and not leftover, f"balanced structure: {rel}",
                     f"unexpected closes={page.mismatches[:5]} unclosed={leftover[:5]}")
        dupes = [i for i, n in Counter(page.ids).items() if n > 1]
        report.check(not dupes, f"unique ids: {rel}", f"duplicates={dupes[:5]}")
        for nav in ("nav",):
            report.check(page.counts[nav] >= 1, f"navigation landmark: {rel}", "no <nav>")

        base = posixpath.dirname(rel)
        broken = []
        for href in page.links:
            parts = urlsplit(href)
            if parts.scheme or href.startswith("//") or href.startswith("mailto:"):
                continue
            target = rel if not parts.path else posixpath.normpath(posixpath.join(base, unquote(parts.path)))
            if target.endswith("/"):
                target += "index.html"
            if target not in pages:
                broken.append(href)
                continue
            if parts.fragment and unquote(parts.fragment) not in pages[target].ids:
                broken.append(href)
        report.check(not broken, f"internal links and anchors resolve: {rel}", f"{len(broken)} broken, e.g. {broken[:5]}")

        missing_assets, remote_assets = [], []
        for src in page.assets:
            if REMOTE.match(src):
                remote_assets.append(src)
                continue
            # Assets carry a ?v= digest so a rebuilt site is never served from a stale cache.
            path = src.split("?", 1)[0]
            if not (site / posixpath.normpath(posixpath.join(base, path))).is_file():
                missing_assets.append(src)
        report.check(not missing_assets, f"local assets exist: {rel}", f"{missing_assets}")
        report.check(not remote_assets, f"no network runtime assets: {rel}", f"{remote_assets}")

    own_assets = [p for p in (site / "assets").rglob("*") if p.suffix in (".css", ".js") and "vendor" not in p.parts]
    for asset in own_assets:
        text = asset.read_text(encoding="utf-8")
        remote = re.search(r"url\(\s*['\"]?(?:https?:)?//|@import\s+['\"]?(?:https?:)?//|fetch\(|import\(", text)
        report.check(remote is None, f"asset works offline: {asset.relative_to(site).as_posix()}",
                     f"found {remote.group(0) if remote else ''}")
    vendor = site / "assets/vendor/mermaid/mermaid.min.js"
    report.check(vendor.is_file(), "vendored Mermaid present", "missing")
    if vendor.is_file():
        report.check("import(" not in vendor.read_text(encoding="utf-8", errors="ignore"),
                     "vendored Mermaid has no dynamic network imports", "found import(")
