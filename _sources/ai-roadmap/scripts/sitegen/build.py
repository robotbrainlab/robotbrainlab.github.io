"""Build pipeline for the learner site.

Stages: discover canonical sources through the configured routes → parse →
read the learner guide and check it against the curriculum specification →
build area navigation → render the guide (one page per step) and the canonical
documents → compose Home and the area landings → validate → replace ``site/``.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import posixpath
import re
import shutil
import sys
import tempfile
import tomllib
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from . import GENERATOR_VERSION, SITE_VERSION
from .extract import ExtractionError, ReportInfo, labelled_paragraph, report_info, roadmap_architecture, \
    section_heading, table_after, table_cells
from .guide import Guide, GuideStep, check_guide, check_label_integrity, check_learner_structure, \
    check_orchestration, check_reading_plan, check_unit_shape, gate_item_counts, parse_guide, \
    read_specification, return_unit, topic_status
from .markdown import MarkdownDocument, PresentationRenderer, RenderContext, create_parser, inline_text
from .provenance import check_claim_strength, check_provenance, protected_fingerprint, read_register
from .validate import (
    ValidationReport,
    guide_wording_preserved,
    ids_absent,
    parallel_track_presented,
    journey_pager_follows,
    primary_nav_is,
    stale_phrases_absent,
    unit_contents_match_sections,
    structure_preserved,
    validate_site,
    words_from_sources,
    wording_preserved,
)

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent.parent
HOME_PAGE = "index.html"
NOT_FOUND_PAGE = "404.html"
EXCLUDED_DIRS = {".venv", "site", "scripts", "node_modules", "__MACOSX"}


@dataclass
class Page:
    rel: str  # output path relative to site root
    html: str
    sources: list[str] = field(default_factory=list)  # canonical files the page draws on
    learner: bool = False  # part of the learner experience: stricter checks apply


@dataclass
class Source:
    rel: str
    page: str
    area: str
    kind: str
    group: str | None
    doc: MarkdownDocument
    info: ReportInfo


def load_config() -> dict:
    with open(PACKAGE.parent / "site.toml", "rb") as fh:
        return tomllib.load(fh)


def rel_url(from_page: str, to_page: str) -> str:
    base = posixpath.dirname(from_page) or "."
    return posixpath.relpath(to_page, base)


def root_prefix(page_rel: str) -> str:
    return "../" * page_rel.count("/")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


class SiteBuilder:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.md = create_parser()
        self.renderer = PresentationRenderer()
        self.env = Environment(
            loader=FileSystemLoader(PACKAGE / "templates"),
            autoescape=select_autoescape(["html"]),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.report = ValidationReport()
        self.unavailable_links: set[tuple[str, str]] = set()
        self.guide_bodies: list[tuple[GuideStep, str]] = []

    # ----- discovery -------------------------------------------------------------

    def discover(self) -> None:
        self.sources: dict[str, Source] = {}
        pages: dict[str, str] = {}
        for route in self.config["routes"]:
            for path in sorted(REPO.glob(route["source"])):
                rel = path.relative_to(REPO).as_posix()
                if rel in self.sources or not path.is_file():
                    continue
                page = route["page"].format(stem=path.stem)
                if page in pages:
                    raise ExtractionError(f"Two sources route to {page}: {pages[page]} and {rel}")
                pages[page] = rel
                doc = MarkdownDocument(REPO, rel, self.md)
                self.sources[rel] = Source(rel, page, route["area"], route["kind"], route.get("group"), doc,
                                           report_info(doc))
        for key, rel in self.config["sources"].items():
            if rel.endswith(".md") and rel not in self.sources:
                raise ExtractionError(f"Required canonical source missing or unrouted ({key}): {rel}")

        self.unrouted = sorted(
            p.relative_to(REPO).as_posix()
            for p in REPO.rglob("*.md")
            if not (set(p.relative_to(REPO).parts[:-1]) & EXCLUDED_DIRS)
            and not any(part.startswith(".") for part in p.relative_to(REPO).parts)
            and p.relative_to(REPO).as_posix() not in self.sources
        )

        src = self.config["sources"]
        self.site_doc = self.sources[src["site"]].doc
        self.guide_source = self.sources[src["guide"]]
        self.roadmap = self.sources[src["curriculum"]]
        self.maintenance = self.sources[src["maintenance"]]
        state_path = REPO / src["maintenance_state"]
        self.state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}

        self.page_map = {rel: s.page for rel, s in self.sources.items()}
        self.aliases = dict(self.config.get("aliases", {}))
        self.landings = {key: area["landing"] for key, area in self.config["areas"].items()}
        self.landings["reviews"] = "reviews/index.html"
        self.page_kinds = {s.page: s.kind for s in self.sources.values()}
        self.page_kinds[self.landings["evidence"]] = "evidence"
        self.kind_labels = dict(self.config.get("xref", {}))

        self.reports = sorted((s for s in self.sources.values() if s.kind == "evidence"),
                              key=lambda s: (s.info.date or "", s.rel), reverse=True)
        self.registers = [s for s in self.sources.values() if s.kind == "register"]
        self.reviews = sorted((s for s in self.sources.values() if s.kind == "review"),
                              key=lambda s: (s.info.date or "", s.rel), reverse=True)
        self.read_guide()

    def read_guide(self) -> None:
        g = self.config["guide"]
        self.guide: Guide = parse_guide(self.guide_source.doc, g["intro_section"], g["part_prefix"],
                                        g["checkpoint_prefix"], g["modern_section"],
                                        g["unit_labels"]["back_labels"])
        self.step_pages = {s.slug: f"learn/{s.slug}/index.html" for s in self.guide.sequence}
        self.modern_page = f"learn/{self.guide.modern.slug}/index.html"
        self.stage_pages = {s.slug: f"learn/{s.slug}/index.html" for s in self.guide.stages}
        self.unit_pages = dict(self.step_pages) | dict(self.stage_pages)
        # The one journey the learner walks: Depth steps with each Modern topic where it is taken.
        self.journey = [u for _, u in self.guide.units]
        self.journey_at = {u.slug: k for k, u in enumerate(self.journey)}
        for page in [*self.step_pages.values(), self.modern_page, *self.stage_pages.values()]:
            self.page_kinds[page] = "guide"
        # The guide is split across pages; its in-document anchors lead to the page that holds them.
        self.anchor_map = dict(self.step_pages) | dict(self.stage_pages) | {
            self.guide.modern.slug: self.modern_page,
            self.guide.intro.slug: f"{self.landings['learn']}#{self.guide.intro.slug}",
        }

        m = self.roadmap.doc
        cfg = self.config["curriculum"]
        arch = roadmap_architecture(m)
        self.stages = arch.stages
        self.spec = read_specification(m, cfg, arch.stages, arch.track)
        usage = section_heading(m, 2, cfg["usage_section"])
        roles_table = table_after(m, usage, labelled_paragraph(m, usage, cfg["roles_label"]))
        self.presentation = {
            "emphasis_rows": cfg["emphasis_rows"],
            "resource_rows": cfg["resource_rows"],
            "role_column": cfg["role_column"],
            "roles": [inline_text(row[0]).strip() for row in table_cells(m, roles_table)],
        }

    # ----- rendering helpers ------------------------------------------------------------

    def ctx(self, source: Source, page_rel: str, **kw) -> RenderContext:
        return RenderContext(
            source_rel=source.rel,
            page_rel=page_rel,
            page_map=self.page_map,
            aliases=self.aliases,
            page_kinds=self.page_kinds,
            kind_labels=self.kind_labels,
            kind=source.kind,
            presentation=self.presentation,
            anchor_map=self.anchor_map if source is self.guide_source else {},
            split_source=self.guide_source.rel,
            split_anchors=self.anchor_map,
            **kw,
        )

    def blocks_html(self, source: Source, page_rel: str, blocks, guide: bool = False) -> Markup:
        ctx = self.ctx(source, page_rel, guide=guide)
        if page_rel != source.page and source is not self.guide_source:
            # a document's blocks shown on another page: its own anchors lead back to it
            ctx.anchor_map = {h.slug: f"{source.page}#{h.slug}" for h in source.doc.headings}
        html = self.renderer.render_blocks(source.doc, blocks, ctx)
        self.unavailable_links.update((page_rel, h) for h in ctx.unavailable_links)
        return Markup(html)

    def inline(self, source: Source, page_rel: str, children) -> Markup:
        ctx = self.ctx(source, page_rel)
        html = self.renderer.render_inline(children or [], ctx)
        self.unavailable_links.update((page_rel, h) for h in ctx.unavailable_links)
        return Markup(html)

    def heading_html(self, source: Source, page_rel: str, heading) -> Markup:
        return self.inline(source, page_rel, source.doc.tokens[heading.index + 1].children)

    def lead_html(self, page_rel: str, step: GuideStep) -> Markup:
        lead = next((b for b in step.blocks if b.type == "paragraph"), None)
        if lead is None:
            return Markup("")
        return self.inline(self.guide_source, page_rel, self.guide_source.doc.tokens[lead.start + 1].children)

    # ----- navigation ----------------------------------------------------------------------

    def primary_nav(self, page_rel: str, current_area: str | None) -> list[dict]:
        return [
            {"label": self.config["areas"][key]["label"], "href": rel_url(page_rel, self.landings[key]),
             "current": key == current_area}
            for key in self.config["nav"]["primary"]
        ]

    def entry(self, page_rel: str, target: str, title: str, **extra) -> dict:
        return {"title": title, "href": rel_url(page_rel, target), "current": target == page_rel,
                "children": [], "number": "", "date": None, "toc": False, "cls": ""} | extra

    def area_nav(self, page_rel: str, area: str) -> dict:
        label = self.config["areas"][area]["label"]
        groups: list[dict] = []
        if area == "learn":
            groups.append({"label": None, "entries": [
                self.entry(page_rel, self.landings["learn"], "How this guide works"),
            ]})
            groups.append({"track": self.config["guide"]["depth_track_label"], "label": None, "entries": []})
            for part in self.guide.parts:
                groups.append({"label": self.section_name(part.title), "entries": [
                    self.entry(page_rel, self.step_pages[s.slug], s.title, number=s.number,
                               cls="is-checkpoint" if s.kind == "checkpoint" else "")
                    for s in part.steps
                ]})
            groups.append({"track": self.guide.modern.heading.text, "label": None, "entries": [
                self.entry(page_rel, self.modern_page, self.config["guide"]["modern_nav_title"]),
                *(self.entry(page_rel, self.stage_pages[st.slug], st.title) for st in self.guide.stages),
            ]})
        elif area == "evidence":
            groups.append({"label": None, "entries": [self.entry(page_rel, self.landings["evidence"], "All reports")]})
            groups.append({"label": "Current practice", "entries": [
                self.entry(page_rel, s.page, s.doc.title) for s in self.registers]})
            groups.append({"label": "Research reports", "entries": [
                self.entry(page_rel, s.page, s.info.title, date=s.info.date) for s in self.reports
            ]})
        elif area == "about":
            groups.append({"label": None, "entries": [self.entry(page_rel, self.landings["about"], "About overview")]})
            for group_label, members in self.about_groups():
                groups.append({"label": group_label, "entries": [
                    self.entry(page_rel, m["page"], m["title"]) for m in members
                ]})
        return {"key": area, "label": label, "groups": groups}

    def about_groups(self) -> list[tuple[str, list[dict]]]:
        order: list[str] = []
        members: dict[str, list[dict]] = {}
        for route in self.config["routes"]:
            if route["area"] == "about" and route.get("group") and route["group"] not in order:
                order.append(route["group"])
        for s in self.sources.values():
            if s.area == "about" and s.kind != "review":
                members.setdefault(s.group or "", []).append(
                    {"title": s.doc.title, "page": s.page, "kind": s.kind, "path": s.rel})
        for link in self.config.get("about_links", []):
            members.setdefault(link["group"], []).append(
                {"title": link["title"], "page": link["page"], "kind": link["kind"], "path": None})
        return [(g, members[g]) for g in order if g in members]

    @staticmethod
    def toc(doc: MarkdownDocument) -> list[dict]:
        items: list[dict] = []
        for h in doc.headings:
            if h.level == 2:
                items.append({"text": h.text, "slug": h.slug, "children": []})
            elif h.level == 3 and items:
                items[-1]["children"].append({"text": h.text, "slug": h.slug})
        return items

    # ----- page contexts ----------------------------------------------------------------------

    def asset_version(self) -> str:
        """A short digest of the stylesheets and scripts, so a learner's browser never keeps
        yesterday's presentation after the site is rebuilt."""
        if not hasattr(self, "_asset_version"):
            digest = hashlib.sha256()
            for f in sorted((PACKAGE / "assets").rglob("*")):
                if f.is_file() and f.suffix in (".css", ".js") and "vendor" not in f.parts:
                    digest.update(f.read_bytes())
            self._asset_version = digest.hexdigest()[:10]
        return self._asset_version

    def base_context(self, page_rel: str, area: str | None, sources: list[str]) -> dict:
        return {
            "root": root_prefix(page_rel),
            "assets": self.asset_version(),
            "site_title": self.site_doc.title,
            "primary_nav": self.primary_nav(page_rel, area),
            "home_href": rel_url(page_rel, HOME_PAGE),
            "is_home": page_rel == HOME_PAGE,
            "sources": sources,
            "has_mermaid": False,
            "has_toc": False,
            "toc": [],
        }

    def marker(self, kind: str, note: str | None = None) -> str:
        k = self.config["kinds"][kind]
        return self.env.get_template("partials/doc_marker.html").render(
            kind=kind, label=k["label"], note=note if note is not None else k.get("note", ""))

    def curriculum_note(self) -> str:
        labels = self.roadmap.info.labels
        baseline, accepted = labels.get("Baseline"), labels.get("Accepted")
        parts = [f"Baseline {baseline}" if baseline else "", f"Accepted {accepted}" if accepted else ""]
        return " · ".join(p for p in parts if p) or self.config["kinds"]["curriculum"]["note"]

    def shell_page(self, page_rel: str, area: str, kind: str, title: str, body: str, sources: list[str],
                   toc: list[dict], crumbs: list[dict], has_mermaid: bool = False, learner: bool = False) -> Page:
        context = self.base_context(page_rel, area, sources) | {
            "page_title": title,
            "area_nav": self.area_nav(page_rel, area),
            "breadcrumbs": [{"label": "Home", "href": rel_url(page_rel, HOME_PAGE)}, *crumbs],
            "doc_kind": kind,
            "body": Markup(body),
            "toc": toc,
            "has_toc": bool(toc),
            "has_mermaid": has_mermaid,
        }
        return Page(page_rel, self.env.get_template("document.html").render(context), sources, learner)

    # ----- canonical documents ------------------------------------------------------------------

    def document_meta(self, source: Source) -> str:
        info = source.info
        meta = []
        if info.date:
            label = next((k for k in info.labels if "date" in k.casefold()), None)
            meta.append((label or "Date", Markup(f'<time datetime="{escape(info.date)}">{escape(info.date)}</time>')))
        for label in self.config.get("evidence", {}).get("type_labels", []):
            if label in info.labels:
                meta.append((label, info.labels[label]))
                break
        meta.append(("Canonical source", Markup(f"<code>{escape(source.rel)}</code>")))
        return self.env.get_template("partials/doc_meta.html").render(meta=meta)

    def build_document(self, source: Source) -> tuple[Page, str]:
        page_rel = source.page
        is_spec = source is self.roadmap
        ctx = self.ctx(
            source,
            page_rel,
            before_h1=self.marker(source.kind, self.curriculum_note() if is_spec else None),
            after_h1=self.env.get_template("partials/spec_note.html").render(
                guide_href=rel_url(page_rel, self.landings["learn"])) if is_spec else self.document_meta(source),
        )
        body = self.renderer.render_document(source.doc, ctx)
        self.unavailable_links.update((page_rel, h) for h in ctx.unavailable_links)
        area_label = self.config["areas"][source.area]["label"]
        crumbs = [{"label": area_label, "href": rel_url(page_rel, self.landings[source.area])}]
        page = self.shell_page(page_rel, source.area, source.kind, source.doc.title, body, [source.rel],
                               self.toc(source.doc), crumbs, has_mermaid=ctx.has_mermaid)
        return page, body

    # ----- the learner guide -----------------------------------------------------------------------

    @staticmethod
    def section_name(part_title: str) -> str:
        """"Part 1 — Fundamentals" → "Fundamentals": the learner section a part forms."""
        return part_title.split("—", 1)[-1].strip()

    def opens_text(self, topic: GuideStep) -> str:
        """When a Modern topic opens, as the guide states it: after its last required step, and
        its best time where that is later."""
        required, best = self.guide.opening(topic)
        seq = self.guide.sequence
        if not required:
            return "From the start"
        text = f"After step {seq[max(required)].number}"
        if best is not None and best > max(required):
            text += f" · best at step {seq[best].number}"
        return text

    def stage_models(self, page_rel: str) -> list[dict]:
        return [{"title": st.title, "href": rel_url(page_rel, self.stage_pages[st.slug]),
                 "lead": self.lead_html(page_rel, st), "opens": self.opens_text(st)} for st in self.guide.stages]

    def build_modern(self) -> Page:
        """The Modern AI Engineering overview: what it is, how it relates to depth, when topics open."""
        page_rel = self.modern_page
        g = self.guide_source
        m = self.guide.modern
        topics = self.guide.stages
        body = self.env.get_template("guide_modern.html").render(
            slug=m.slug,
            heading=self.heading_html(g, page_rel, m.heading),
            intro=self.blocks_html(g, page_rel, m.intro, guide=True),
            first=self.stage_models(page_rel)[0],
            start_href=rel_url(page_rel, self.step_pages[self.guide.steps[0].slug]),
            start_title=self.guide.steps[0].title,
        )
        self.guide_bodies.append((m, body))
        return self.shell_page(page_rel, "learn", "guide", m.title, body, [g.rel], [],
                               [{"label": "Learn", "href": rel_url(page_rel, self.landings["learn"])}],
                               has_mermaid="data-diagram" in body, learner=True)

    def build_stage(self, index: int) -> Page:
        topics = self.guide.stages
        topic = topics[index]
        page_rel = self.stage_pages[topic.slug]
        g = self.guide_source
        body = self.env.get_template("guide_stage.html").render(
            track=self.guide.modern.heading.text,
            opens=self.opens_text(topic),
            slug=topic.slug,
            heading=self.heading_html(g, page_rel, topic.heading),
            content=self.unit_body(page_rel, topic),
            **self.pager(page_rel, topic),
            overview_href=rel_url(page_rel, self.landings["learn"]),
        )
        self.guide_bodies.append((topic, body))
        return self.shell_page(page_rel, "learn", "guide", topic.title, body, [g.rel], [],
                               [{"label": "Learn", "href": rel_url(page_rel, self.landings["learn"])},
                                {"label": self.guide.modern.heading.text,
                                 "href": rel_url(page_rel, self.modern_page)}],
                               has_mermaid="data-diagram" in body, learner=True)

    def unit_toc(self, step: GuideStep) -> str:
        """The unit's own contents: its concept hierarchy, linking to the sections on this page.

        Generated from the unit's headings, so it cannot drift from them.
        """
        if not step.areas:
            return ""
        title = self.config["guide"]["unit_labels"]["toc_title"]
        out = [f'<nav class="unit-toc" aria-labelledby="unit-toc-title" data-chrome>',
               f'<p class="unit-toc-title" id="unit-toc-title">{escape(title)}</p>',
               '<ol class="unit-toc-list">']
        for area in step.areas:
            out.append(f'<li><a href="#{area.heading.slug}">{escape(area.heading.text)}</a>')
            if area.concepts:
                out.append('<ol class="unit-toc-sublist">')
                out += [f'<li><a href="#{c.heading.slug}">{escape(c.heading.text)}</a></li>'
                        for c in area.concepts]
                out.append('</ol>')
            out.append('</li>')
        out += ['</ol>', '</nav>']
        return "\n".join(out)

    def unit_body(self, page_rel: str, step: GuideStep) -> Markup:
        """A unit's body with its contents placed after the orientation and before the concepts."""
        g = self.guide_source
        if not step.areas:
            return self.blocks_html(g, page_rel, step.blocks, guide=True)
        labels = self.config["guide"]["unit_labels"]
        wanted = [labels["toc_before_label"], labels["modern_toc_before_label"]]
        cut = next((k for k, b in enumerate(step.blocks)
                    if (g.doc.paragraph_label(b) or ("",))[0] in wanted), len(step.front))
        return Markup(self.study_items_html(str(self.blocks_html(g, page_rel, step.blocks[:cut], guide=True))
                                            + self.unit_toc(step)
                                            + str(self.blocks_html(g, page_rel, step.blocks[cut:], guide=True))))

    def study_items_html(self, html: str) -> str:
        """Give each study item the shape of the question a learner is asking.

        The canonical bullet carries four facts in one sentence: the role the resource plays,
        which resource it is, what to read now, and why. Read as prose it has to be decoded;
        set on four lines it can be scanned. Only the presentation changes — every word, link
        and mark stays where the canonical source put it, and an item that does not follow the
        pattern (a planned material, a note about a missing resource) is left alone.
        """
        fields = re.compile(
            r"^(?P<role><strong>[^<]*</strong>)\s*·\s*(?P<title>.*?)\s*—\s*"
            r"(?P<task>.*?)(?P<why><strong>Why:</strong>.*)?$", re.S)

        def shape(m: re.Match) -> str:
            f = fields.match(m[1].strip())
            if f is None:
                return m[0]
            parts = [f'<span class="study-role">{f["role"]}</span>',
                     f'<span class="study-title">{f["title"]}</span>',
                     f'<span class="study-task">{f["task"].strip()}</span>']
            if f["why"]:
                parts.append(f'<span class="study-why">{f["why"].strip()}</span>')
            return "<li>" + "".join(parts) + "</li>"

        def within(block: re.Match) -> str:
            return block[1] + re.sub(r"<li>((?:(?!</li>).)*)</li>", shape, block[2], flags=re.S) + block[3]

        return re.sub(r'(<ul class="guide-list guide-list--study">)(.*?)(</ul>)', within, html, flags=re.S)

    def journey_link(self, page_rel: str, unit: GuideStep | None, back: bool, from_modern: bool) -> dict | None:
        """One end of the primary pager: the unit the learner meets next (or met last).

        The pager walks the single journey, so a required detour cannot be stepped over by
        clicking Next. A detour is still a detour: when the link leads into Modern AI
        Engineering it carries the topic's own status, so a recommended or available topic
        is never mistaken for the next compulsory unit.
        """
        if unit is None:
            return None
        modern = unit in self.guide.stages
        note = None
        if modern:
            status = topic_status(self.guide, unit, self.config["guide"]["topic_labels"])
            note = f"{self.guide.modern.heading.text} · {status.lower()}" if status else \
                self.guide.modern.heading.text
        elif from_modern and not back:
            note = self.config["guide"]["return_note"]
        label = ("← Previous" + (f" · {note}" if note else "")) if back else \
                ("Next →" + (f" {note}" if note else ""))
        return {"href": rel_url(page_rel, self.unit_pages[unit.slug]), "title": unit.title,
                "number": unit.number, "checkpoint": unit.kind == "checkpoint",
                "modern": modern, "label": label}

    def pager(self, page_rel: str, unit: GuideStep) -> dict:
        """The units either side of this one on the journey.

        Where the next unit is a detour the path does not depend on, the pager also offers the
        step the learner would reach by leaving it for later: occupying the Next position should
        not be what makes a recommended topic feel compulsory.
        """
        k = self.journey_at[unit.slug]
        from_modern = unit in self.guide.stages
        nxt = self.journey[k + 1] if k + 1 < len(self.journey) else None
        skip = None
        if nxt in self.guide.stages and topic_status(self.guide, nxt,
                                                     self.config["guide"]["topic_labels"]) != "Required":
            after = next((u for u in self.journey[k + 1:] if u not in self.guide.stages), None)
            skip = self.journey_link(page_rel, after, False, from_modern)
        return {
            "previous": self.journey_link(page_rel, self.journey[k - 1] if k else None, True, from_modern),
            "next": self.journey_link(page_rel, nxt, False, from_modern),
            "skip": skip,
        }

    def build_guide_step(self, index: int) -> Page:
        seq = self.guide.sequence
        step = seq[index]
        page_rel = self.step_pages[step.slug]
        g = self.guide_source
        numbered = self.guide.steps
        body = self.env.get_template("guide_step.html").render(
            part=step.part.title if step.part else "",
            position=(f"Step {step.number} of {len(numbered)}" if step.kind == "step" else "Checkpoint"),
            checkpoint=step.kind == "checkpoint",
            slug=step.slug,
            heading=self.heading_html(g, page_rel, step.heading),
            content=self.unit_body(page_rel, step),
            **self.pager(page_rel, step),
            overview_href=rel_url(page_rel, self.landings["learn"]),
        )
        self.guide_bodies.append((step, body))
        return self.shell_page(page_rel, "learn", "guide", step.title, body, [g.rel], [],
                               [{"label": "Learn", "href": rel_url(page_rel, self.landings["learn"])},
                                *([{"label": step.part.title, "href": None}] if step.part else [])],
                               has_mermaid="data-diagram" in body, learner=True)

    def build_guide_overview(self) -> Page:
        page_rel = self.landings["learn"]
        g = self.guide_source
        first = self.guide.steps[0]
        parts = []
        for part in self.guide.parts:
            parts.append({
                "title": part.title,
                "slug": part.slug,
                "intro": self.blocks_html(g, page_rel, part.intro),
                "steps": self.journey_entries(page_rel, part),
            })
        body = self.env.get_template("guide_overview.html").render(
            title=g.doc.title,
            preamble=self.blocks_html(g, page_rel, self.guide.preamble),
            start_href=rel_url(page_rel, self.step_pages[first.slug]),
            start_title=first.title,
            intro_slug=self.guide.intro.slug,
            intro_title=self.heading_html(g, page_rel, self.guide.intro.heading),
            intro=self.blocks_html(g, page_rel, self.guide.intro.blocks, guide=True),
            parts=parts,
            modern_title=self.guide.modern.heading.text,
            modern_slug=self.guide.modern.slug,
            modern_href=rel_url(page_rel, self.modern_page),
            modern_lead=self.modern_lead(page_rel),
            stages=self.stage_models(page_rel),
            depth_label=self.config["guide"]["depth_track_label"],
        )
        return self.shell_page(page_rel, "learn", "guide", "Learning guide", body, [g.rel], [],
                               [{"label": "Learn", "href": None}], has_mermaid="data-diagram" in body,
                               learner=True)

    def journey_entries(self, page_rel: str, part: "GuidePart") -> list[dict]:
        """A stage's units in the order the learner meets them: its steps, with each Modern
        topic shown where the journey reaches it — the two dimensions, in one sequence."""
        own = {s.slug for s in part.steps}
        labels = self.config["guide"]["topic_labels"]
        entries: list[dict] = []
        for position, unit in self.guide.units:
            modern = unit in self.guide.stages
            if not modern and unit.slug not in own:
                continue
            if modern and self.guide.sequence[int(position)].slug not in own:
                continue  # a topic belongs to the stage of the step it is taken at
            entry = {"title": unit.title, "number": unit.number, "modern": modern, "meta": None,
                     "checkpoint": unit.kind == "checkpoint",
                     "href": rel_url(page_rel, self.unit_pages[unit.slug]),
                     "lead": self.lead_html(page_rel, unit)}
            if modern:
                status = topic_status(self.guide, unit, labels)
                back = return_unit(self.guide, unit, labels)
                entry["meta"] = " · ".join(x for x in [
                    self.guide.modern.heading.text,
                    status.lower() if status else None,
                    f"then back to {back.title}" if back else None] if x)
            entries.append(entry)
        return entries

    def modern_lead(self, page_rel: str) -> Markup:
        """The first paragraph of the Modern AI Engineering section: what it is."""
        lead = self.guide_source.doc.first_plain_paragraph(self.guide.modern.intro)
        return self.blocks_html(self.guide_source, page_rel, [lead]) if lead else Markup("")

    def dimensions_html(self, page_rel: str) -> Markup:
        """The guide's own statement of its two dimensions, from "How to Use This Guide"."""
        label = self.config["guide"]["dimensions_label"]
        blocks = self.guide.intro.blocks
        block = next((b for b in blocks if (self.guide_source.doc.paragraph_label(b) or ("",))[0] == label), None)
        if block is None:
            raise ExtractionError(f"{self.guide_source.rel}: no '{label}' paragraph in the guide's introduction")
        return self.blocks_html(self.guide_source, page_rel, [block])

    # ----- composed pages ------------------------------------------------------------------------

    def build_home(self) -> Page:
        page_rel = HOME_PAGE
        site = self.sources[self.config["sources"]["site"]]
        lead = next((b for b in site.doc.preamble_blocks() if b.type == "paragraph"), None)
        first = self.guide.steps[0]
        parts = [{
            "title": p.title,
            "intro": self.blocks_html(self.guide_source, page_rel, p.intro),
            "steps": [{"title": s.title, "number": s.number, "href": rel_url(page_rel, self.step_pages[s.slug])}
                      for s in p.steps if s.kind == "step"],
        } for p in self.guide.parts]
        context = self.base_context(page_rel, None, [site.rel, self.guide_source.rel]) | {
            "page_title": self.site_doc.title,
            "lead": self.inline(site, page_rel, site.doc.tokens[lead.start + 1].children) if lead else "",
            "start_href": rel_url(page_rel, self.step_pages[first.slug]),
            "start_title": first.title,
            "guide_href": rel_url(page_rel, self.landings["learn"]),
            "parts": parts,
            "depth": [self.section_name(p.title) for p in self.guide.parts],
            "depth_label": self.config["guide"]["depth_track_label"],
            "dimensions": self.dimensions_html(page_rel),
            "modern_title": self.guide.modern.heading.text,
            "modern_href": rel_url(page_rel, self.modern_page),
            "modern_lead": self.modern_lead(page_rel),
            "topics": self.stage_models(page_rel),
            "evidence_href": rel_url(page_rel, self.landings["evidence"]),
            "spec_href": rel_url(page_rel, self.roadmap.page),
            "about_href": rel_url(page_rel, self.landings["about"]),
            "report_count": len(self.reports),
        }
        return Page(page_rel, self.env.get_template("home.html").render(context),
                    [site.rel, self.guide_source.rel], learner=True)

    def build_evidence_landing(self) -> Page:
        page_rel = self.landings["evidence"]
        type_labels = self.config.get("evidence", {}).get("type_labels", [])
        reports = []
        for s in self.reports:
            label = next((lab for lab in type_labels if lab in s.info.labels), None)
            reports.append({"title": s.info.title, "href": rel_url(page_rel, s.page), "date": s.info.date,
                            "type_label": label, "type": s.info.labels.get(label) if label else None,
                            "path": s.rel})
        registers = [{"title": s.doc.title, "href": rel_url(page_rel, s.page), "path": s.rel,
                      "lead": self.blocks_html(s, page_rel, [s.doc.first_plain_paragraph(s.doc.preamble_blocks())])}
                     for s in self.registers]
        scans = [{"title": s.info.title, "href": rel_url(page_rel, s.page), "date": s.info.date, "path": s.rel}
                 for s in self.reviews]
        body = self.env.get_template("evidence_landing.html").render(
            marker=Markup(self.marker("evidence")), reports=reports, registers=registers, scans=scans,
            guide_href=rel_url(page_rel, self.landings["learn"]),
            spec_href=rel_url(page_rel, self.roadmap.page))
        return self.shell_page(page_rel, "evidence", "evidence", "Evidence", body,
                               [s.rel for s in [*self.reports, *self.registers]], [],
                               [{"label": "Evidence", "href": None}])

    def build_reviews_landing(self) -> Page:
        page_rel = self.landings["reviews"]
        mt = self.maintenance
        m = mt.doc
        labels = self.config["maintenance_state"]
        cycles = []
        for key, due_key, last_key in (
            ("scan_section", "next_modern_ai_scan_due", "last_modern_ai_scan"),
            ("review_section", "next_curriculum_review_due", "last_curriculum_review"),
        ):
            heading = section_heading(m, 2, labels[key])
            purpose = next((h for h in m.subheadings(heading, 3) if h.text.startswith("Purpose")), None)
            para = next((b for b in m.section_blocks(purpose) if b.type == "paragraph"), None) if purpose else None
            cycles.append({
                "title": heading.text,
                "href": rel_url(page_rel, mt.page) + "#" + heading.slug,
                "purpose": self.inline(mt, page_rel, m.tokens[para.start + 1].children) if para else "",
                "state": [{"label": labels[due_key], "value": self.state.get(due_key)},
                          {"label": labels[last_key], "value": self.state.get(last_key)}],
            })
        command_heading = section_heading(m, 2, labels["command_section"])
        command_block = next((b for b in m.section_blocks(command_heading) if b.type == "blockquote"), None)
        body = self.env.get_template("reviews_landing.html").render(
            marker=Markup(self.marker("review")),
            command_title=command_heading.text,
            command_href=rel_url(page_rel, mt.page) + "#" + command_heading.slug,
            command_html=self.blocks_html(mt, page_rel, [command_block]) if command_block else "",
            cycles=cycles,
            baseline=self.state.get("baseline"),
            baseline_date=self.state.get("baseline_date"),
            state_path=self.config["sources"]["maintenance_state"],
            reviews=[{"title": s.info.title, "href": rel_url(page_rel, s.page), "date": s.info.date}
                     for s in self.reviews],
            maintenance_title=m.title,
            maintenance_href=rel_url(page_rel, mt.page),
        )
        toc = [{"text": "Maintenance command", "slug": "maintenance-command", "children": []},
               {"text": "Review cycles", "slug": "review-cycles", "children": []},
               {"text": "Review reports", "slug": "review-reports", "children": []}]
        return self.shell_page(page_rel, "about", "review", "Maintenance and reviews", body,
                               [mt.rel, *(s.rel for s in self.reviews)], toc,
                               [{"label": "About", "href": rel_url(page_rel, self.landings["about"])}])

    def build_about_landing(self) -> Page:
        page_rel = self.landings["about"]
        groups = []
        for label, members in self.about_groups():
            groups.append({
                "label": label,
                "id": slug(label),
                "entries": [{"title": e["title"], "href": rel_url(page_rel, e["page"]), "path": e["path"],
                             "kind": self.config["kinds"][e["kind"]]["label"],
                             "note": self.config["kinds"][e["kind"]].get("note", "")} for e in members],
            })
        body = self.env.get_template("about_landing.html").render(
            groups=groups, guide_href=rel_url(page_rel, self.landings["learn"]), summary=self.about_summary(page_rel))
        toc = [{"text": g["label"], "slug": g["id"], "children": []} for g in groups]
        return self.shell_page(page_rel, "about", "project", "About", body,
                               [s.rel for s in self.sources.values() if s.area == "about"], toc,
                               [{"label": "About", "href": None}])

    def about_summary(self, page_rel: str) -> Markup:
        """A short account of the project, in the canonical files' own words: purpose and the two
        dimensions (README preamble), the Computer Science & Engineering boundary (ROADMAP.md
        preamble), and how the roadmap is kept current (README)."""
        site = self.sources[self.config["sources"]["site"]]
        cfg = self.config["about"]
        preamble = [b for b in site.doc.preamble_blocks() if b.type in ("paragraph", "ordered_list", "bullet_list")]
        boundary = [b for b in self.roadmap.doc.preamble_blocks() if b.type == "paragraph"
                    and cfg["boundary_phrase"] in inline_text(self.roadmap.doc.tokens[b.start + 1])]
        current = section_heading(site.doc, 2, cfg["current_section"])
        keeping = site.doc.first_plain_paragraph(site.doc.section_blocks(current))
        if not boundary or keeping is None:
            raise ExtractionError("About summary: canonical paragraphs not found")
        return Markup(self.blocks_html(site, page_rel, preamble) + self.blocks_html(self.roadmap, page_rel, boundary[:1])
                      + self.blocks_html(site, page_rel, [keeping]))

    def build_not_found(self) -> Page:
        context = self.base_context(NOT_FOUND_PAGE, None, []) | {
            "page_title": "Page not found",
            "links": [{"label": self.config["areas"][k]["label"], "href": self.landings[k]}
                      for k in self.config["nav"]["primary"]],
        }
        return Page(NOT_FOUND_PAGE, self.env.get_template("404.html").render(context), [], learner=True)

    # ----- output ------------------------------------------------------------------------------------

    def write(self, out_dir: Path, pages: list[Page]) -> None:
        for page in pages:
            target = out_dir / page.rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(page.html, encoding="utf-8")
        shutil.copytree(PACKAGE / "assets", out_dir / "assets",
                        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
        state = self.config["sources"]["maintenance_state"]
        manifest = {
            "site": SITE_VERSION,
            "generator": GENERATOR_VERSION,
            "note": "Generated presentation. Canonical Markdown sources take precedence.",
            "pages": sorted(p.rel for p in pages),
            "sources": {
                rel: hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
                for rel in sorted([*self.sources, *([state] if (REPO / state).is_file() else [])])
            },
        }
        (out_dir / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def check_materials(report: ValidationReport, sources: dict, guide_source: str, kind: str = "material") -> None:
    """Materials this curriculum writes itself are reachable, and their code runs.

    A material is only real when a learner meets it: every one must be linked from the guide
    at the point where its capability is needed, or it is a file nobody will ever open. And
    because several of them are exercises the learner is meant to run, their Python must at
    least parse — a broken snippet in a learning material is a defect, not a typo.
    """
    materials = {rel: src for rel, src in sources.items() if src.kind == kind}
    orphans = [rel for rel in materials if f"]({rel})" not in guide_source]
    report.check(not orphans, "every curriculum material is reached from the learner guide",
                 f"never linked: {sorted(orphans)}")

    problems: list[str] = []
    for rel, src in sorted(materials.items()):
        for n, block in enumerate(re.findall(r"```python\n(.*?)```", src.doc.source, re.S), start=1):
            try:
                ast.parse(block)
            except SyntaxError as exc:
                problems.append(f"{rel} block {n}: line {exc.lineno}: {exc.msg}")
    report.check(not problems, "the code in every curriculum material parses", "; ".join(problems[:4]))


def section_labels(guide_config: dict) -> list[str]:
    """Every label the guide uses to open a section, from the shapes the config defines."""
    labels: set[str] = set()
    for group in ("unit_labels", "topic_labels"):
        for key, value in guide_config[group].items():
            if isinstance(value, str) and not key.endswith(("_source_label", "_part", "_title")):
                labels.add(value)
            elif key in ("back_labels", "required", "orientation"):
                labels.update(value)
    return sorted(labels)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the learner site from canonical Markdown.")
    parser.add_argument("--out", default=None, help="Output directory (default: site/ from site.toml)")
    args = parser.parse_args(argv)

    config = load_config()
    out_dir = Path(args.out).resolve() if args.out else REPO / config["output"]["dir"]
    builder = SiteBuilder(config)
    report = builder.report

    try:
        builder.discover()
        check_guide(report, builder.guide, builder.spec, builder.stages)
        check_reading_plan(report, builder.guide, builder.spec, config["curriculum"]["required_complete"])
        check_learner_structure(report, builder.guide, builder.spec, config["validation"]["expected_sequence"],
                                config["guide"]["topic_labels"],
                                gate_item_counts(builder.roadmap.doc, config["curriculum"]["readiness_section"]))
        check_orchestration(report, builder.guide, config["guide"]["topic_labels"])
        check_label_integrity(report, builder.guide, section_labels(config["guide"]))
        check_materials(report, builder.sources, builder.guide_source.doc.source)
        register = builder.sources[config["register"]["source"]]
        check_provenance(report, builder.guide, register.doc, {rel: s.doc for rel, s in builder.sources.items()},
                         config["register"] | {"study_label": config["guide"]["topic_labels"]["study"]})
        check_claim_strength(report, builder.guide, config["validation"]["overclaim_phrases"])
        check_unit_shape(report, builder.guide, builder.spec, config["guide"]["unit_labels"],
                         [r.title for r in read_register(register.doc, config["register"])[1]])
        baseline = builder.roadmap.info.labels.get("Baseline")
        report.check(baseline == config["validation"]["baseline"], "the current baseline is the accepted one",
                     f"ROADMAP.md says Baseline {baseline}")
        protected = protected_fingerprint(builder.roadmap.doc.source, config["validation"]["current_practice_column"])
        report.check(protected == config["validation"]["roadmap_protected_sha256"],
                     "ROADMAP.md is the accepted curriculum: only the §7 current-practice column may change",
                     "ROADMAP.md changed outside the current-practice column: update scripts/site.toml only "
                     "after an accepted curriculum change")
        pages: list[Page] = []
        for source in builder.sources.values():
            if source is builder.guide_source:
                continue
            page, body = builder.build_document(source)
            wording_preserved(report, source.doc, body)
            structure_preserved(report, source.doc, body)
            pages.append(page)
        pages.append(builder.build_guide_overview())
        pages += [builder.build_guide_step(k) for k in range(len(builder.guide.sequence))]
        pages.append(builder.build_modern())
        pages += [builder.build_stage(k) for k in range(len(builder.guide.stages))]
        pages += [
            builder.build_home(),
            builder.build_evidence_landing(),
            builder.build_reviews_landing(),
            builder.build_about_landing(),
            builder.build_not_found(),
        ]
    except ExtractionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for step, body in builder.guide_bodies:
        page = builder.step_pages.get(step.slug) or builder.stage_pages.get(step.slug) or builder.modern_page
        guide_wording_preserved(report, builder.guide.doc, step.heading, getattr(step, "blocks", None) or step.intro,
                                body, page)
    docs = {rel: s.doc for rel, s in builder.sources.items()}
    validation = config["validation"]
    for page in pages:
        words_from_sources(report, page.rel, page.html, [docs[s] for s in page.sources])
        stale_phrases_absent(report, page.rel, page.html, validation["stale_phrases"], all_text=page.learner)
        if page.learner:
            ids_absent(report, page.rel, page.html, validation["internal_ids"])
            unit_contents_match_sections(report, page.rel, page.html)
            parallel_track_presented(report, page.rel, page.html, is_home=page.rel == HOME_PAGE,
                                     is_learn=page.rel.startswith("learn/"),
                                     expected_tracks=config["validation"]["learn_tracks"],
                                     expected_groups=config["validation"]["learn_sections"],
                                     entries=len(builder.guide.sequence) + 2 + len(builder.guide.stages),
                                     modern_page=builder.modern_page,
                                     learn_prefix="learn/")
        primary_nav_is(report, page.rel, page.html, [config["areas"][k]["label"] for k in config["nav"]["primary"]],
                       config["validation"]["top_navigation"])

    with tempfile.TemporaryDirectory(prefix="site-build-") as tmp:
        staging = Path(tmp) / "site"
        staging.mkdir()
        builder.write(staging, pages)
        required = [HOME_PAGE, NOT_FOUND_PAGE, *builder.landings.values(), *(p.rel for p in pages)]
        validate_site(report, staging, required_pages=required,
                      justified_selectors=config["validation"]["justified_selectors"])
        journey_pager_follows(report, staging, [builder.unit_pages[u.slug] for u in builder.journey],
                              builder.landings["learn"])

        print(f"Generated {len(pages)} pages from {len(builder.sources)} canonical documents "
              f"({len(builder.guide.sequence)} learner-guide pages).")
        if builder.unrouted:
            print(f"Markdown files outside the site (no route): {', '.join(builder.unrouted)}")
        if builder.unavailable_links:
            print(f"Links to files that are not part of the generated site (rendered as plain text): "
                  f"{len(builder.unavailable_links)}")
            for page_rel, href in sorted(builder.unavailable_links):
                print(f"  {page_rel}: {href}")
        report.print()
        if report.errors:
            print("Build failed validation; site/ was not replaced.", file=sys.stderr)
            return 1

        if out_dir.exists():
            if out_dir.name != "site" and not args.out:
                raise RuntimeError(f"Refusing to replace unexpected directory {out_dir}")
            for child in out_dir.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        else:
            out_dir.mkdir(parents=True)
        for child in staging.iterdir():
            shutil.move(str(child), out_dir / child.name)

    print(f"Site written to {out_dir}")
    return 0
