"""Provenance: why the learner is told what the learner guide tells them.

The guide presents ROADMAP.md, and ROADMAP.md rests on the evidence in research/.
Modern AI Engineering adds one more link in that chain: its current practices are
recorded, with status and evidence, in the current-practice register that the
4-week scan maintains. These checks fail the build when a learner-facing claim
loses its basis:

- every Modern topic declares, in a hidden ``<!-- practice: ... -->`` marker, the
  register entries it teaches, and the register names the same topic;
- only Current Practice and Established entries are taught; watched entries are not;
- every register entry cites evidence that exists in the report it links to;
- a contemporary source the guide asks the learner to consult is listed in the
  register with the gap it fills;
- the permanent curriculum in ROADMAP.md changes only through an accepted change:
  its protected fingerprint ignores nothing but the current-practice column that the
  4-week scan may update.

Semantic fidelity (whether a sentence says no more than its source) cannot be judged
by a script; it is reviewed by hand and recorded in design/learner-guide.md. The
checks here make that review answerable: every claim has a place to trace to.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
from dataclasses import dataclass, field

from .extract import section_heading, table_cells
from .guide import Guide, labelled_sections
from .markdown import MarkdownDocument, inline_text, meaningful
from .validate import ValidationReport

PRACTICE = re.compile(r"<!--\s*practice:\s*(.*?)\s*-->", re.S)
SOURCE_ID = re.compile(r"\b[A-Z]{1,2}\d{1,2}\b")
NOT_TAUGHT = "—"


@dataclass
class Evidence:
    href: str  # repository-relative path of the linked report
    ids: list[str] = field(default_factory=list)


@dataclass
class Entry:
    id: str
    practice: str
    status: str
    evidence: list[Evidence]
    taught_in: str


@dataclass
class Reference:
    title: str
    url: str
    used_in: str


def _columns(doc: MarkdownDocument, table) -> list[str]:
    return doc.table_rows(table)[0]


def _table(doc: MarkdownDocument, section: str):
    h = section_heading(doc, 2, section)
    return next(b for b in doc.section_blocks(h) if b.type == "table")


def _evidence(doc: MarkdownDocument, cell) -> list[Evidence]:
    found: list[Evidence] = []
    for c in meaningful(cell.children):
        if c.type == "link_open":
            href = (c.attrGet("href") or "").split("#", 1)[0]
            found.append(Evidence(posixpath.normpath(posixpath.join(posixpath.dirname(doc.rel_path), href))))
        elif c.type == "text" and found:
            found[-1].ids += SOURCE_ID.findall(c.content)
    return found


def read_register(doc: MarkdownDocument, cfg: dict) -> tuple[list[Entry], list[Reference]]:
    table = _table(doc, cfg["practices_section"])
    cols = _columns(doc, table)
    col = {name: cols.index(name) for name in ("ID", "Practice", "Status", "Evidence", "Taught in")}
    entries = [Entry(inline_text(r[col["ID"]]).strip(), inline_text(r[col["Practice"]]).strip(),
                     inline_text(r[col["Status"]]).strip(), _evidence(doc, r[col["Evidence"]]),
                     inline_text(r[col["Taught in"]]).strip())
               for r in table_cells(doc, table)]
    table = _table(doc, cfg["references_section"])
    cols = _columns(doc, table)
    col = {name: cols.index(name) for name in ("Reference", "Link", "Used in")}
    refs = [Reference(inline_text(r[col["Reference"]]).strip(), inline_text(r[col["Link"]]).strip(),
                      inline_text(r[col["Used in"]]).strip()) for r in table_cells(doc, table)]
    return entries, refs


def source_ids(doc: MarkdownDocument) -> set[str]:
    """IDs a report assigns to its sources: the first cell of every table row."""
    ids: set[str] = set()
    for b in doc.blocks(0, len(doc.tokens)):
        if b.type == "table":
            ids |= {row[0].strip("* ") for row in doc.table_rows(b) if row}
    return ids


def declared_practices(guide: Guide) -> dict[str, list[str]]:
    """Register IDs each Modern topic declares, by topic title."""
    doc = guide.doc
    out: dict[str, list[str]] = {}
    for topic in guide.stages:
        ids: list[str] = []
        for t in doc.tokens[topic.heading.index:doc.section_end(topic.heading)]:
            if t.type == "html_block":
                for m in PRACTICE.finditer(t.content):
                    ids += [x.strip() for x in m.group(1).split(",") if x.strip()]
        out[topic.title] = ids
    return out


def consulted(doc: MarkdownDocument, blocks) -> list[str]:
    """Links of study items marked **consult:**."""
    urls: list[str] = []
    for b in blocks:
        if b.type != "bullet_list":
            continue
        item: list = []
        for t in doc.tokens[b.start:b.end]:
            if t.type == "list_item_open" and t.level == 1:
                item = []
            elif t.type == "inline":
                item += meaningful(t.children)
            elif t.type == "list_item_close" and t.level == 1:
                verb = any(c.type == "text" and c.content.strip() == "consult:" for c in item)
                link = next((c.attrGet("href") for c in item if c.type == "link_open"), None)
                if verb and link:
                    urls.append(link)
    return urls


def check_provenance(report: ValidationReport, guide: Guide, register: MarkdownDocument,
                     docs: dict[str, MarkdownDocument], cfg: dict) -> None:
    entries, refs = read_register(register, cfg)
    topics = {t.title for t in guide.stages}
    teachable = set(cfg["teachable"])

    problems: list[str] = []
    seen: set[str] = set()
    for e in entries:
        if e.id in seen:
            problems.append(f"{e.id} is listed twice")
        seen.add(e.id)
        if e.status not in cfg["statuses"]:
            problems.append(f"{e.id} has an unknown status '{e.status}'")
        if not e.evidence:
            problems.append(f"{e.id} cites no evidence")
        for ev in e.evidence:
            target = docs.get(ev.href)
            if target is None:
                problems.append(f"{e.id} cites a document outside the repository's sources: {ev.href}")
                continue
            unknown = [i for i in ev.ids if i not in source_ids(target)]
            if unknown:
                problems.append(f"{e.id} cites IDs that {ev.href} does not define: {unknown}")
        if e.taught_in != NOT_TAUGHT and e.taught_in not in topics:
            problems.append(f"{e.id} is taught in '{e.taught_in}', which is not a Modern topic")
        if e.taught_in != NOT_TAUGHT and e.status not in teachable:
            problems.append(f"{e.id} is {e.status} but taught in '{e.taught_in}'")
    report.check(not problems, "every current-practice register entry has a status and resolvable evidence",
                 "; ".join(problems[:6]))

    problems = []
    by_id = {e.id: e for e in entries}
    declared = declared_practices(guide)
    for title, ids in declared.items():
        if not ids:
            problems.append(f"'{title}' declares no register entries")
        for i in ids:
            e = by_id.get(i)
            if e is None:
                problems.append(f"'{title}' declares {i}, which the register does not list")
            elif e.status not in teachable:
                problems.append(f"'{title}' teaches {i}, which is {e.status}")
            elif e.taught_in != title:
                problems.append(f"'{title}' declares {i}, but the register says it is taught in '{e.taught_in}'")
    for e in entries:
        if e.taught_in in declared and e.id not in declared[e.taught_in]:
            problems.append(f"the register says '{e.taught_in}' teaches {e.id}, but the topic does not declare it")
    outside = guide.doc.source[:guide.doc.source.find("\n## " + guide.modern.heading.text)] if guide.modern else ""
    if PRACTICE.search(outside):
        problems.append("a Depth step declares current-practice entries: dynamic material must stay in Modern")
    report.check(not problems, "Modern topics teach only Current Practice or Established register entries",
                 "; ".join(problems[:6]))

    problems = []
    doc = guide.doc
    urls = {r.url: r for r in refs}
    for r in refs:
        if r.used_in not in topics:
            problems.append(f"reference '{r.title}' is used in '{r.used_in}', which is not a Modern topic")
    for topic in guide.stages:
        study = labelled_sections(doc, topic.shell).get(cfg["study_label"], [])
        for url in consulted(doc, study):
            if url not in urls:
                problems.append(f"'{topic.title}' consults {url}, which the register does not list")
            elif urls[url].used_in != topic.title:
                problems.append(f"'{topic.title}' consults {url}, listed for '{urls[url].used_in}'")
        for r in refs:
            if r.used_in == topic.title and r.url not in consulted(doc, study):
                problems.append(f"the register lists '{r.title}' for '{topic.title}', which does not consult it")
    for step in guide.sequence:
        if consulted(doc, step.shell):
            problems.append(f"'{step.heading.text}' consults a current reference: only Modern topics may")
    report.check(not problems, "every contemporary reference the guide consults is in the register with its gap",
                 "; ".join(problems[:6]))


def check_claim_strength(report: ValidationReport, guide: Guide, phrases: list[str]) -> None:
    """Wording that asserts more than the evidence can carry (adoption, consensus, superiority)."""
    text = " ".join(inline_text(t) for t in guide.doc.tokens if t.type == "inline").casefold()
    found = [p for p in phrases if re.search(rf"\b{re.escape(p.casefold())}\b", text)]
    report.check(not found, "the learner guide makes no unsupported claims of adoption or consensus",
                 f"found: {found}")


def protected_fingerprint(source: str, column: str) -> str:
    """SHA-256 of ROADMAP.md with only the current-practice column of §7 blanked.

    The 4-week scan may edit that column (MAINTENANCE.md §4); any other change to
    ROADMAP.md alters this fingerprint and needs an accepted curriculum change.
    """
    lines = source.split("\n")
    out: list[str] = []
    index = None
    for line in lines:
        cells = line.split("|") if line.startswith("|") else None
        if cells and column in [c.strip() for c in cells]:
            index = [c.strip() for c in cells].index(column)
        elif index is not None and not cells:
            index = None
        elif index is not None and cells and not set(line) <= set("|- "):
            cells[index] = " "
            line = "|".join(cells)
        out.append(line)
    return hashlib.sha256("\n".join(out).encode("utf-8")).hexdigest()
