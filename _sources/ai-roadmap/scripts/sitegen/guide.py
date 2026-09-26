"""The learner guide: its structure, and its correspondence with ROADMAP.md.

LEARNING-GUIDE.md presents the accepted curriculum as one path. Each step
declares, in a hidden ``<!-- covers: ... -->`` marker, which parts of the
curriculum it delivers. The checks here fail the build when the guide and
the specification drift apart.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from markdown_it.token import Token

from .extract import ExtractionError, dependency_edges, section_heading, table_cells
from .markdown import Block, Heading, MarkdownDocument, inline_text, meaningful, strip_number
from .validate import ValidationReport

COVERS = re.compile(r"<!--\s*covers:\s*(.*?)\s*-->", re.S)
ROW_ID = re.compile(r"^([A-Z]+\d+)\b")
BLOCK_HEADING = re.compile(r"^([A-Z]+\d+)\.\s+(.+)$")
PHASE = re.compile(r"^Phase\s+(\d+)")
BLOCK_ID = re.compile(r"\b([A-Z]\d+)\b")
QUOTED = re.compile(r'"([^"]+)"')


# ----- guide structure ---------------------------------------------------------------


@dataclass
class UnitConcept:
    """One concept inside an area: what it is, why it is here, where it is studied."""
    heading: Heading
    blocks: list["Block"]


@dataclass
class UnitArea:
    """A major area of a unit's concept hierarchy, with its concepts."""
    heading: Heading
    intro: list["Block"]
    concepts: list[UnitConcept] = field(default_factory=list)


@dataclass
class GuideStep:
    kind: str  # "intro", "step" or "checkpoint"
    heading: Heading
    blocks: list[Block]
    covers: list[str]
    part: "GuidePart | None" = None
    number: str = ""
    front: list[Block] = field(default_factory=list)   # narrative and orientation, before the hierarchy
    areas: list[UnitArea] = field(default_factory=list)  # the unit's concept hierarchy
    back: list[Block] = field(default_factory=list)    # resources, practice, readiness, transition

    @property
    def shell(self) -> list[Block]:
        """Everything outside the concept hierarchy: where the unit's labelled sections live."""
        return self.front + self.back if self.areas else self.blocks

    @property
    def title(self) -> str:
        return strip_number(self.heading.text)

    @property
    def slug(self) -> str:
        return self.heading.slug


@dataclass
class GuidePart:
    heading: Heading
    intro: list[Block]
    steps: list[GuideStep] = field(default_factory=list)

    @property
    def title(self) -> str:
        return self.heading.text

    @property
    def slug(self) -> str:
        return self.heading.slug


@dataclass
class Guide:
    doc: MarkdownDocument
    preamble: list[Block]
    intro: GuideStep
    parts: list[GuidePart]
    modern: GuidePart | None = None  # Modern AI Engineering: a parallel curriculum of topics
    _openings: dict[str, tuple[list[int], int | None]] = field(default_factory=dict)

    @property
    def sequence(self) -> list[GuideStep]:
        """The numbered Depth path in reading order (steps and checkpoints)."""
        return [s for p in self.parts for s in p.steps]

    @property
    def steps(self) -> list[GuideStep]:
        return [s for s in self.sequence if s.kind == "step"]

    @property
    def stages(self) -> list[GuideStep]:
        return self.modern.steps if self.modern else []

    def opening(self, topic: GuideStep) -> tuple[list[int], int | None]:
        """A topic's "Opens when": the Depth steps its first paragraph requires, and the step its
        "best time" paragraph names first (None when it states no separate best time)."""
        if topic.slug in self._openings:  # read once, before rendering rewrites the links
            return self._openings[topic.slug]
        seq = {s.slug: k for k, s in enumerate(self.sequence)}
        paragraphs = [b for b in labelled_sections(self.doc, topic.shell).get(OPENS, []) if b.type == "paragraph"]
        required = [seq[a] for a in section_links(self.doc, paragraphs[:1]) if a in seq]
        best = [seq[a] for a in section_links(self.doc, paragraphs[1:2]) if a in seq]
        self._openings[topic.slug] = (required, best[0] if best else None)
        return self._openings[topic.slug]

    def stage_position(self, topic: GuideStep) -> float:
        """Where a Modern topic sits against the Depth path: just after the step where it is best
        taken, or else just after the last step it requires. Topics meeting at the same step keep
        their order in the guide."""
        required, best = self.opening(topic)
        anchor = best if best is not None else (max(required) if required else -1)
        return anchor + 0.5 + self.stages.index(topic) / 1000

    @property
    def units(self) -> list[tuple[float, GuideStep]]:
        """Depth steps and Modern stages together, ordered by where the learner meets them."""
        depth = [(float(k), s) for k, s in enumerate(self.sequence)]
        return sorted(depth + [(self.stage_position(s), s) for s in self.stages], key=lambda u: u[0])


def is_navigation(doc: MarkdownDocument, block: Block) -> bool:
    """Markdown-only navigation: "In this section" lines and "Back to Contents"."""
    if doc.is_nav_paragraph(block):
        return True
    label = doc.paragraph_label(block)
    return bool(label) and label[0].rstrip(":") == "In this section"


def content_blocks(doc: MarkdownDocument, start: int, end: int) -> list[Block]:
    """Blocks a learner reads: no navigation, rules, comments or wrapper tags."""
    return [
        b for b in doc.blocks(start, end)
        if b.type not in ("hr", "html_block") and not is_navigation(doc, b)
    ]


def split_unit(doc: MarkdownDocument, blocks: list[Block], back_labels: list[str]
               ) -> tuple[list[Block], list[UnitArea], list[Block]]:
    """Split a unit into narrative front matter, its concept hierarchy (H4 areas, H5 concepts)
    and the back matter that follows it (resources, practice, readiness, what comes next)."""
    def level(b: Block) -> int:
        return int(doc.tokens[b.start].tag[1]) if b.type == "heading" else 0

    first = next((k for k, b in enumerate(blocks) if level(b) == 4), None)
    if first is None:
        return blocks, [], []
    end = len(blocks)
    for k in range(first, len(blocks)):
        parsed = doc.paragraph_label(blocks[k])
        if parsed and parsed[0] in back_labels:
            end = k
            break
    areas: list[UnitArea] = []
    for b in blocks[first:end]:
        if level(b) == 4:
            areas.append(UnitArea(doc.heading_at(b.start), []))
        elif level(b) == 5 and areas:
            areas[-1].concepts.append(UnitConcept(doc.heading_at(b.start), []))
        elif areas:
            (areas[-1].concepts[-1].blocks if areas[-1].concepts else areas[-1].intro).append(b)
    return blocks[:first], areas, blocks[end:]


def covers_of(doc: MarkdownDocument, start: int, end: int) -> list[str]:
    ids: list[str] = []
    for t in doc.tokens[start:end]:
        if t.type == "html_block":
            for m in COVERS.finditer(t.content):
                ids += [x.strip() for x in m.group(1).split(",") if x.strip()]
    return ids



def parse_guide(doc: MarkdownDocument, intro_section: str, part_prefix: str, checkpoint_prefix: str,
                modern_section: str | None = None, back_labels: list[str] | None = None) -> Guide:
    h1 = next((h for h in doc.headings if h.level == 1), None)
    if h1 is None:
        raise ExtractionError(f"{doc.rel_path}: no title")
    preamble = [b for b in doc.preamble_blocks() if b.type != "html_block"]

    ih = section_heading(doc, 2, intro_section)
    ie = doc.section_end(ih)
    intro = GuideStep("intro", ih, content_blocks(doc, ih.index + 3, ie), covers_of(doc, ih.index, ie))

    parts: list[GuidePart] = []
    for h in doc.headings:
        if h.level != 2 or not h.text.startswith(part_prefix):
            continue
        subs = doc.subheadings(h, 3)
        first = subs[0].index if subs else doc.section_end(h)
        part = GuidePart(h, content_blocks(doc, h.index + 3, first))
        for s in subs:
            end = doc.section_end(s)
            kind = "checkpoint" if s.text.startswith(checkpoint_prefix) else "step"
            number = s.text.split(".", 1)[0] if kind == "step" else ""
            step = GuideStep(kind, s, content_blocks(doc, s.index + 3, end), covers_of(doc, s.index, end), part,
                             number)
            step.front, step.areas, step.back = split_unit(doc, step.blocks, back_labels or [])
            if not step.covers:
                raise ExtractionError(f"{doc.rel_path}: '{s.text}' declares no <!-- covers: --> marker")
            part.steps.append(step)
        parts.append(part)
    if not parts:
        raise ExtractionError(f"{doc.rel_path}: no sections starting with '{part_prefix}'")
    modern = None
    if modern_section:
        mh = section_heading(doc, 2, modern_section)
        subs = doc.subheadings(mh, 3)
        first = subs[0].index if subs else doc.section_end(mh)
        modern = GuidePart(mh, content_blocks(doc, mh.index + 3, first))
        for sh in subs:
            end = doc.section_end(sh)
            stage = GuideStep("stage", sh, content_blocks(doc, sh.index + 3, end), covers_of(doc, sh.index, end),
                              modern)
            stage.front, stage.areas, stage.back = split_unit(doc, stage.blocks, back_labels or [])
            if not stage.covers:
                raise ExtractionError(f"{doc.rel_path}: stage '{sh.text}' declares no <!-- covers: --> marker")
            modern.steps.append(stage)
    guide = Guide(doc, preamble, intro, parts, modern)
    for topic in guide.stages:
        guide.opening(topic)
    return guide


OPENS = "Opens when"


def labelled_sections(doc: MarkdownDocument, blocks: list[Block]) -> dict[str, list[Block]]:
    """Blocks grouped under the label-only paragraphs ("**Study**", "**Opens when**") that head them."""
    out: dict[str, list[Block]] = {}
    current = ""
    for b in blocks:
        kids = meaningful(doc.tokens[b.start + 1].children) if b.type == "paragraph" else []
        if len(kids) == 3 and kids[0].type == "strong_open" and kids[2].type == "strong_close":
            current = kids[1].content.strip()
            out[current] = []
        elif current:
            out[current].append(b)
    return out


def labelled_links(doc: MarkdownDocument, blocks: list[Block], label: str, first_only: bool = False) -> list[str]:
    """In-guide anchors linked under a label; with first_only, only its first paragraph."""
    section = labelled_sections(doc, blocks).get(label, [])
    if first_only:
        section = section[:1]
    return section_links(doc, section)


def block_text(doc: MarkdownDocument, blocks: list[Block]) -> str:
    return " ".join(inline_text(t) for b in blocks for t in doc.tokens[b.start:b.end] if t.type == "inline")


# ----- what the specification requires ------------------------------------------------


@dataclass
class PlanEntry:
    key: str  # title of the resource
    read: str  # how it is read, as the reading plan states it
    begins: str  # curriculum ID where it enters the path ("" if not stated)

    @property
    def complete(self) -> bool:
        return self.read.startswith("Complete")


@dataclass
class Specification:
    items: dict[str, str]  # curriculum ID -> name (blocks, capabilities, paths, phases)
    stage_of: dict[str, str]  # curriculum ID -> stage
    resources: dict[str, list[str]]  # curriculum ID -> resource keys that must appear with it
    anywhere: list[str]  # resource keys that must appear somewhere in the guide
    named: list[str]  # extension, specialization and frontier names that must appear
    gates: list[str]  # readiness-gate labels
    order: list[tuple[str, str, str]]  # (before, after, reason): before must come no later than after
    optional: list[str] = field(default_factory=list)  # titles ROADMAP lists as not counted as mandatory
    reading_plan: list[PlanEntry] = field(default_factory=list)
    practice_rows: list[tuple[str, list[str]]] = field(default_factory=list)  # §7 row label, resource keys
    phase_count: int = 0
    phases: dict[str, list[str]] = field(default_factory=dict)  # "P1" -> its capability items

    def phase_of(self, item: str) -> str | None:
        return next((p for p, items in self.phases.items() if item in items), None)


def resource_keys(children: list[Token]) -> list[str]:
    """Resources named in an "Assigned resources" cell, one key per resource.

    Segments are separated by " · ". A segment's key is its italic title, else
    its quoted title, else the text before " — " (and before any comma).
    Planned materials, cross-references and "no resource" notes are skipped.
    """
    segments: list[list[Token]] = [[]]
    for c in children:
        if c.type == "text" and " · " in c.content:
            parts = c.content.split(" · ")
            for k, part in enumerate(parts):
                if k:
                    segments.append([])
                t = Token("text", "", 0)
                t.content = part
                segments[-1].append(t)
        else:
            segments[-1].append(c)
    keys: list[str] = []
    for seg in segments:
        holder = Token("inline", "", 0)
        holder.children = seg
        text = inline_text(holder).strip()
        if not text or text.startswith(("Planned", "Cross-reference", "No dedicated")):
            continue
        kids = meaningful(seg)
        em = next((kids[k + 1].content for k, c in enumerate(kids)
                   if c.type == "em_open" and k + 1 < len(kids) and kids[k + 1].type == "text"), None)
        quoted = QUOTED.search(text)
        if em:
            keys.append(em.strip())
        elif quoted:
            keys.append(quoted.group(1).strip())
        else:
            key = text.split(" — ")[0].split(",")[0].replace(" et al.", "").strip()
            if key.startswith("Conditional:"):
                key = key[len("Conditional:"):].strip()
            keys.append(key)
    return keys


def _table_after_label(doc: MarkdownDocument, heading: Heading, label: str) -> Block | None:
    blocks = doc.section_blocks(heading, direct_only=False)
    for k, b in enumerate(blocks):
        parsed = doc.paragraph_label(b)
        if parsed and parsed[0].rstrip(".:").casefold() == label.rstrip(".:").casefold():
            return next((x for x in blocks[k + 1:] if x.type == "table"), None)
    return None


def read_specification(roadmap: MarkdownDocument, cfg: dict, stages: list[str], track: str) -> Specification:
    items: dict[str, str] = {}
    stage_of: dict[str, str] = {}
    resources: dict[str, list[str]] = {}
    order: list[tuple[str, str, str]] = []

    for stage in stages:
        h = section_heading(roadmap, 2, stage)
        for sub in roadmap.subheadings(h, 3):  # blocks with their own section
            m = BLOCK_HEADING.match(sub.text)
            if not m:
                continue
            items[m.group(1)], stage_of[m.group(1)] = m.group(2), stage
            table = next((b for b in roadmap.section_blocks(sub) if b.type == "table"), None)
            for row in table_cells(roadmap, table) if table else []:
                if inline_text(row[0]).strip() == cfg["resource_row"]:
                    resources[m.group(1)] = resource_keys(row[1].children or [])
        for b in roadmap.section_blocks(h):  # capabilities and paths stated in a table
            if b.type == "table":
                for row in table_cells(roadmap, b):
                    m = ROW_ID.match(inline_text(row[0]).strip())
                    if m and m.group(1) not in items:
                        items[m.group(1)] = strip_number(inline_text(row[0]).strip()[len(m.group(1)):].lstrip(". "))
                        stage_of[m.group(1)] = stage
        prereq = next((roadmap.paragraph_label(b) for b in roadmap.section_blocks(h)
                       if (roadmap.paragraph_label(b) or ("",))[0].rstrip(".") == cfg["prerequisites_label"]), None)
        if prereq:  # e.g. "H1: E3, E10, F3. H2: H1, G3 and specialization depth."
            for target, needs in re.findall(r"([A-Z]\d+):\s*([^.]*)", prereq[1]):
                order += [(n, target, f"{n} is a prerequisite of {target}") for n in BLOCK_ID.findall(needs)]

    th = section_heading(roadmap, 2, track)
    phase_table = next((b for b in roadmap.section_blocks(th) if b.type == "table"), None)
    phases: dict[str, list[str]] = {}
    for row in table_cells(roadmap, phase_table):
        m = PHASE.match(inline_text(row[0]).strip())
        if not m:
            continue
        pid = f"P{m.group(1)}"
        opens = BLOCK_ID.findall(inline_text(row[1]))
        phases[pid] = []
        # "What becomes possible": capabilities separated by ";" and sentences; a sentence
        # "X opens after F1" adds its own prerequisite to capability X.
        for sentence in re.split(r"\.\s+", inline_text(row[2]).strip().rstrip(".")):
            later = re.match(r"(.+?)\s+opens after\s+(.+)$", sentence)
            names = [later.group(1)] if later else sentence.split(";")
            for name in (n.strip() for n in names if n.strip()):
                item = f"{pid} {name[0].lower()}{name[1:]}"
                items[item], stage_of[item] = name, track
                phases[pid].append(item)
                needs = opens + (BLOCK_ID.findall(later.group(2)) if later else [])
                order += [(n, item, f"{pid} opens after {n}") for n in needs]
    anywhere: list[str] = []
    practice_rows: list[tuple[str, list[str]]] = []
    practice = _table_after_label(roadmap, th, cfg["track_resources_label"])
    for row in table_cells(roadmap, practice) if practice else []:
        keys = [k for k in resource_keys(row[1].children or []) if "guides" not in k] + \
            QUOTED.findall(inline_text(row[2]))
        anywhere += keys
        practice_rows.append((inline_text(row[0]).strip(), keys))
    phase_count = len(phases)

    for e in dependency_edges(roadmap, section_heading(roadmap, 2, cfg["dependency_section"])):
        if e.hard:
            order.append((e.source, e.target, f"{e.source} is a hard prerequisite of {e.target}"))

    named: list[str] = []
    for section in cfg["named_sections"]:
        h = section_heading(roadmap, 2, section)
        for b in roadmap.section_blocks(h):
            if b.type == "table":
                named += [inline_text(row[1]).strip() for row in table_cells(roadmap, b)]

    gates = [roadmap.paragraph_label(b)[0].rstrip(".")
             for b in roadmap.section_blocks(section_heading(roadmap, 2, cfg["readiness_section"]))
             if roadmap.paragraph_label(b)]
    plan: list[PlanEntry] = []
    rm = section_heading(roadmap, 2, cfg["resource_map_section"])
    plan_table = _table_after_label(roadmap, rm, cfg["reading_plan_label"])
    if plan_table is None:
        raise ExtractionError(f"{roadmap.rel_path}: no '{cfg['reading_plan_label']}' table in '{rm.text}'")
    for row in table_cells(roadmap, plan_table):
        kids = meaningful(row[0].children)
        em = next((kids[k + 1].content for k, c in enumerate(kids)
                   if c.type == "em_open" and k + 1 < len(kids) and kids[k + 1].type == "text"), None)
        begins = inline_text(row[2]).strip()
        phase = PHASE.match(begins)
        begins = f"P{phase.group(1)}" if phase else (begins if BLOCK_ID.fullmatch(begins) else "")
        plan.append(PlanEntry((em or inline_text(row[0])).strip(), inline_text(row[1]).strip(), begins))
    optional: list[str] = []
    extra = _table_after_label(roadmap, rm, cfg["optional_label"])
    for row in table_cells(roadmap, extra) if extra else []:
        kids = meaningful(row[1].children)
        optional += [kids[k + 1].content.strip() for k, c in enumerate(kids)
                     if c.type == "em_open" and k + 1 < len(kids) and kids[k + 1].type == "text"]
    return Specification(items, stage_of, resources, anywhere, named, gates, order, optional, plan, practice_rows,
                         phase_count, phases)


# ----- correspondence checks -------------------------------------------------------------


def check_guide(report: ValidationReport, guide: Guide, spec: Specification, stages: list[str]) -> None:
    doc = guide.doc
    position: dict[str, float] = {}
    units = guide.units
    for label in guide.intro.covers:
        position[label] = -1
    for k, step in units:
        for label in step.covers:
            if label in position:
                report.check(False, f"guide: '{label}' delivered once", f"repeated in '{step.heading.text}'")
            position[label] = k

    missing = [i for i in spec.items if i not in position]
    report.check(not missing, "guide delivers every block, capability, path and phase",
                 f"not delivered: {missing}")
    missing_gates = [g for g in spec.gates if g not in position]
    report.check(not missing_gates, "guide includes every readiness gate", f"missing: {missing_gates}")
    unknown = [x for x in position if x not in spec.items and x not in spec.gates]
    report.check(not unknown, "guide covers only curriculum that exists", f"unknown: {unknown}")

    step_text = {k: block_text(doc, s.blocks) for k, s in units}
    parts = guide.parts + ([guide.modern] if guide.modern else [])
    whole = block_text(doc, guide.preamble + guide.intro.blocks + [b for p in parts for b in p.intro]) + " " + \
        " ".join(step_text.values())
    for phase, items in spec.phases.items():  # a phase begins where its first topic is met
        met = [position[i] for i in items if i in position]
        if met:
            position.setdefault(phase, min(met))
    complete = {e.key: e for e in spec.reading_plan if e.complete}
    absent = [f"{i}: {key}" for i, keys in spec.resources.items() for key in keys
              if i in position and key not in step_text.get(position[i], "")
              and not (key in complete and complete[key].begins in position
                       and position[complete[key].begins] >= position[i])]
    report.check(not absent, "each assigned resource appears in the step that delivers its block",
                 f"missing: {absent[:8]}")
    absent = [key for key in spec.anywhere if key not in whole]
    report.check(not absent, "every parallel-track resource appears in the guide", f"missing: {absent}")
    absent = [n for n in spec.named if n not in whole]
    report.check(not absent, "every extension, specialization and frontier is named", f"missing: {absent[:8]}")

    late = [reason for before, after, reason in spec.order
            if before in position and after in position and position[before] > position[after]]
    report.check(not late, "guide order respects every prerequisite and phase opening", f"violated: {late[:6]}")

    for k in range(1, len(stages)):
        gate = f"Entering {stages[k]}"
        if gate not in position:
            continue
        prev = [position[i] for i, s in spec.stage_of.items() if s == stages[k - 1] and i in position]
        nxt = [position[i] for i, s in spec.stage_of.items() if s == stages[k] and i in position]
        ok = all(p < position[gate] for p in prev) and all(n > position[gate] for n in nxt)
        report.check(ok, f"guide places the '{gate}' checkpoint between {stages[k - 1]} and {stages[k]}",
                     "misplaced", warn=stages[k] == stages[-1])


# ----- reading plan: coherent books are read whole, once, where they begin ----------------------

VERB = re.compile(r"^(read first|read again|read|revisit|consult|do):$")


@dataclass
class StudyItem:
    step: float  # position of the step or stage (see Guide.units)
    text: str
    verb: str
    titles: list[str]
    where: str = ""  # heading of the step or stage


def study_items(guide: Guide) -> list[StudyItem]:
    """Every list item in every step, with its reading verb and italic titles."""
    doc = guide.doc
    items: list[StudyItem] = []
    for k, step in guide.units:
        for block in step.shell:
            if block.type not in ("bullet_list", "ordered_list"):
                continue
            item: list[Token] = []
            for t in doc.tokens[block.start:block.end]:
                if t.type == "list_item_open" and t.level == 1:
                    item = []
                elif t.type == "inline":
                    item.append(t)
                elif t.type == "list_item_close" and t.level == 1:
                    kids = [c for i in item for c in meaningful(i.children)]
                    verb = next((kids[j + 1].content.strip() for j, c in enumerate(kids)
                                 if c.type == "strong_open" and j + 1 < len(kids)
                                 and VERB.match(kids[j + 1].content.strip())), "")
                    # The resource a study item assigns is its first italic title; titles later in the
                    # item are cross-references ("which *Hands-On ML* covers"), not new assignments.
                    titles = [kids[j + 1].content.strip() for j, c in enumerate(kids)
                              if c.type == "em_open" and j + 1 < len(kids) and kids[j + 1].type == "text"][:1]
                    items.append(StudyItem(k, " ".join(inline_text(i) for i in item), verb.rstrip(":"), titles,
                                           step.heading.text))
    return items


def check_reading_plan(report: ValidationReport, guide: Guide, spec: Specification, required: list[str]) -> None:
    plan = {e.key: e for e in spec.reading_plan}
    missing = [k for k in required if k not in plan or not plan[k].complete]
    report.check(not missing, "reading plan keeps the approved books as complete books", f"not complete: {missing}")

    position = {label: k for k, s in guide.units for label in s.covers}
    starts: dict[str, set[float]] = {}  # where a book may begin: a block's step, or any topic of a phase
    for label, k in position.items():
        starts.setdefault(label, set()).add(k)
        phase = spec.phase_of(label)
        if phase:
            starts.setdefault(phase, set()).add(k)
    items = study_items(guide)
    problems: list[str] = []
    for entry in (e for e in spec.reading_plan if e.complete):
        mine = [i for i in items if any(entry.key.startswith(t) and len(t) >= 8 for t in i.titles)]
        intro = [i for i in mine if i.verb == "read"]
        if len(intro) != 1:
            problems.append(f"{entry.key}: introduced {len(intro)} times as new reading (expected once)")
            continue
        start = intro[0].step
        if "complete" not in intro[0].text.casefold():
            problems.append(f"{entry.key}: introduced without being presented as a complete book")
        if entry.begins in starts and start not in starts[entry.begins]:
            problems.append(f"{entry.key}: introduced in '{intro[0].where}', "
                            f"but the reading plan begins it at {entry.begins}")
        for i in mine:
            if i is intro[0]:
                continue
            if i.verb == "consult":
                problems.append(f"{entry.key}: a complete book is only ever read or revisited, not consulted")
            if i.step > start and not (i.verb == "revisit" or (not i.verb and "revisit" in i.text.casefold())):
                problems.append(f"{entry.key}: assigned again as new reading in '{i.where}'")
            if i.step < start and i.verb != "read first":
                problems.append(f"{entry.key}: read before its introduction without 'read first' "
                                f"in '{i.where}'")
            if i.step == start:
                problems.append(f"{entry.key}: fragmented within its introducing step")
    report.check(not problems, "complete books are read once, whole, where they begin, and only revisited later",
                 "; ".join(problems[:6]))


# ----- one Depth path, and Modern AI Engineering as a parallel curriculum of topics -------------------


def section_links(doc: MarkdownDocument, blocks: list[Block]) -> list[str]:
    """Anchors of the guide that a section links to, in order."""
    return [c.attrGet("href")[1:] for b in blocks for t in doc.tokens[b.start:b.end] if t.type == "inline"
            for c in t.children or [] if c.type == "link_open" and (c.attrGet("href") or "").startswith("#")]


def words(text: str) -> int:
    return len(re.findall(r"\w+", text))


def check_learner_structure(report: ValidationReport, guide: Guide, spec: Specification, expected: list[str],
                            topic_labels: dict, gate_items: dict[str, int]) -> None:
    doc = guide.doc
    seq = guide.sequence
    actual = [", ".join(s.covers) for s in seq]
    first = next((i for i, (a, b) in enumerate(zip(actual, expected)) if a != b), min(len(actual), len(expected)))
    report.check(actual == expected, "the Depth path is the accepted sequence of steps and checkpoints",
                 f"differs from the expected sequence at position {first}")
    report.check("<!-- modern:" not in doc.source, "no per-step Modern AI Engineering markers in the guide",
                 "found <!-- modern: --> markers")

    topics = guide.stages
    problems: list[str] = []
    covered = {c for s in topics for c in s.covers}
    phases_covered = sorted({spec.phase_of(c) for c in covered if spec.phase_of(c)})
    if not topics or phases_covered != sorted(spec.phases):
        problems.append(f"topics cover phases {phases_covered}, not {sorted(spec.phases)}")
    for s in topics:
        own = {spec.phase_of(c) for c in s.covers}
        if None in own or len(own) != 1:
            problems.append(f"'{s.title}' must cover capabilities of exactly one §7 phase: {s.covers}")
    numbered = [s.heading.text for s in topics if re.match(r"^\d", s.heading.text)]
    if numbered:
        problems.append(f"topics are numbered like Depth steps: {numbered}")
    depth_titles = {s.title.casefold() for s in seq}
    inside = [s.title for s in topics if s.title.casefold() in depth_titles]
    if inside:
        problems.append(f"topics also appear inside the Depth path: {inside}")
    leaked = [s.heading.text for s in seq if any(spec.phase_of(c) for c in s.covers)]
    if leaked:
        problems.append(f"Depth steps deliver Modern capabilities: {leaked}")
    report.check(not problems, "Modern AI Engineering is a parallel curriculum of topics covering every §7 phase",
                 "; ".join(problems[:6]))

    # Each topic is substantive knowledge, not a pointer back to the Depth path or a project brief.
    problems = []
    index = {s.slug: k for k, s in enumerate(seq)}
    position = {c: k for k, s in enumerate(seq) for c in s.covers}
    for s in topics:
        sections = labelled_sections(doc, s.shell)
        phase = spec.phase_of(s.covers[0]) if s.covers else None
        needed = topic_labels["required"] if phase != "P0" else topic_labels["orientation"]
        missing = [l for l in needed if l not in sections]
        if missing:
            problems.append(f"'{s.title}' lacks {missing}")
            continue
        lead = s.front[0] if s.front else (s.blocks[0] if s.blocks else None)
        if lead is None or lead.type != "paragraph" or doc.paragraph_label(lead):
            problems.append(f"'{s.title}' does not open with why it matters")
        taught = sections[topic_labels["knowledge"]] + [b for a in s.areas
                                                        for b in a.intro + [x for c in a.concepts for x in c.blocks]]
        understand = block_text(doc, taught)
        practise = block_text(doc, sections.get(topic_labels["practice"], []))
        if words(understand) < topic_labels["min_knowledge_words"]:
            problems.append(f"'{s.title}' teaches too little: {words(understand)} words of knowledge")
        if words(understand) < words(practise):
            problems.append(f"'{s.title}' is mostly practice instructions, not knowledge")
        needs_list = [topic_labels["depth"]] + ([] if s.areas else [topic_labels["knowledge"]])
        for label in needs_list:
            if not any(b.type == "bullet_list" for b in sections[label]):
                problems.append(f"'{s.title}': '{label}' has no list")
        lasting = sections[topic_labels["lasting"]]
        if not [a for a in section_links(doc, lasting) if a in index]:
            problems.append(f"'{s.title}' does not name the Depth steps that teach its lasting principle")
        # opening conditions come from ROADMAP.md §7
        required, best = guide.opening(s)
        pos = guide.stage_position(s)
        needs = sorted({b for c in s.covers for b, a, r in spec.order if a == c})
        for n in needs:
            if n in position and position[n] not in required:
                problems.append(f"'{s.title}' does not state that it opens after the step for {n}")
            if n in position and position[n] > pos:
                problems.append(f"'{s.title}' is placed before its prerequisite {n}")
        if best is not None and required and best < max(required):
            problems.append(f"'{s.title}' names a best time before the steps it requires")
        # Entry points from the Depth path: only where the topic opens, or where it is best taken.
        # Resource sections are exempt: naming where a book was begun is provenance, not an invitation.
        resources = {topic_labels["study"], topic_labels["map"]}
        entry = []
        for k, st in enumerate(seq):
            sections = labelled_sections(doc, st.shell)
            cited = {id(b) for label in resources for b in sections.get(label, [])}
            narrative = [b for b in st.blocks if id(b) not in cited]
            if s.slug in section_links(doc, narrative):
                entry.append(k)
        allowed = set(required) | {int(pos)}
        stray = [seq[k].heading.text for k in entry if k not in allowed]
        if stray:
            problems.append(f"Depth steps point to '{s.title}' where it does not open: {stray}")
        if phase != "P0" and int(pos) not in entry:
            problems.append(f"the Depth path does not point to '{s.title}' where it is best taken")
    report.check(not problems, "each Modern topic teaches knowledge, states when it opens, and ties to the Depth path",
                 "; ".join(problems[:6]))

    study = [b for st in topics for b in labelled_sections(doc, st.blocks).get(topic_labels["study"], [])]
    titles = [c.content.strip() for b in study for t in doc.tokens[b.start:b.end] if t.type == "inline"
              for k, c in enumerate(meaningful(t.children)) if c.type == "text"
              and k and meaningful(t.children)[k - 1].type == "em_open"]
    allowed_titles = {e.key for e in spec.reading_plan} | {k for _, keys in spec.practice_rows for k in keys}
    foreign = [t for t in titles if not any(a.startswith(t) or t.startswith(a) for a in allowed_titles)
               and "?" not in t]
    report.check(not foreign, "Modern AI Engineering names only resources Baseline 2 assigns (or consults a register reference)",
                 f"unassigned: {foreign}")

    counts = {}
    for s in seq:
        if s.kind == "checkpoint":
            lists = [b for b in s.blocks if b.type == "bullet_list"]
            counts[s.covers[0]] = sum(1 for t in doc.tokens[lists[0].start:lists[0].end]
                                      if t.type == "list_item_open" and t.level == 1) if lists else 0
    changed = {g: (n, counts.get(g)) for g, n in gate_items.items() if counts.get(g) != n}
    report.check(not changed, "Depth checkpoints present every ROADMAP readiness-gate criterion",
                 f"(roadmap, guide)={changed}")


def cell_links(cell: Token) -> list[str]:
    """Guide anchors a table cell links to."""
    return [c.attrGet("href")[1:] for c in meaningful(cell.children)
            if c.type == "link_open" and (c.attrGet("href") or "").startswith("#")]


def status_word(text: str, statuses: list[str]) -> str | None:
    """The one status a topic declares, or None when it declares none or more than one.

    Matching ignores case, so a second status word in running prose ("available from
    step 11; required by step 16") reads as the ambiguity it is rather than resolving
    silently to whichever word happens to be capitalized.
    """
    found = [w for w in statuses if re.search(rf"\b{w}\b", text, re.I)]
    return found[0] if len(found) == 1 else None


def topic_status(guide: "Guide", topic: GuideStep, labels: dict) -> str | None:
    """A Modern topic's declared status: Required, Recommended or Available."""
    section = labelled_sections(guide.doc, topic.shell).get(labels["status"], [])
    return status_word(block_text(guide.doc, section), labels["statuses"])


def return_unit(guide: "Guide", topic: GuideStep, labels: dict) -> GuideStep | None:
    """The Depth unit a topic sends the learner back to."""
    index = {s.slug: s for s in guide.sequence}
    section = labelled_sections(guide.doc, topic.shell).get(labels["back"], [])
    return next((index[a] for a in section_links(guide.doc, section) if a in index), None)


def check_label_integrity(report: ValidationReport, guide: Guide, labels: list[str]) -> None:
    """A section label belongs at the start of its own paragraph, never inside a sentence.

    An editing pass that splices a label into running text ("attack it,**Practise and
    build**") leaves a paragraph that still parses, still carries every required section,
    and still validates — while the learner reads a broken sentence. One narrow rule
    catches that whole class: in prose, a label may not follow other text on its line.
    Table rows are exempt, because the guide's own table of the unit shape names them.
    """
    found = [(n, line.strip()) for n, line in enumerate(guide.doc.source.split("\n"), 1)
             if not line.lstrip().startswith("|")
             for label in labels if re.search(rf"\S\s*\*\*{re.escape(label)}\*\*", line)]
    report.check(not found, "every section label stands at the start of its own paragraph",
                 "; ".join(f"line {n}: {text[:60]}" for n, text in found[:4]))


def check_orchestration(report: ValidationReport, guide: Guide, labels: dict) -> None:
    """One journey, not two curricula.

    A learner leaving the numbered path for a Modern topic must be told two things the
    topic itself cannot imply: whether the path depends on it, and where the path resumes.
    These checks fail the build when a topic states neither, when a return pointer does not
    lead back to the journey the site's pager walks — the step the topic is taken at, or the
    unit that follows it — or when the section's table of topics and the topics themselves
    disagree about either.
    """
    doc, index = guide.doc, {s.slug: k for k, s in enumerate(guide.sequence)}
    statuses, problems, declared = labels["statuses"], [], {}
    for topic in guide.stages:
        sections = labelled_sections(doc, topic.shell)
        status = status_word(block_text(doc, sections.get(labels["status"], [])), statuses)
        if status is None:
            problems.append(f"'{topic.title}' does not say plainly whether it is required, recommended or available")
        back = [a for a in section_links(doc, sections.get(labels["back"], [])) if a in index]
        anchor = int(guide.stage_position(topic))  # the Depth step the topic is taken at
        if not back:
            problems.append(f"'{topic.title}' does not name the step to return to")
        elif index[back[0]] not in (anchor, anchor + 1):
            problems.append(f"'{topic.title}' returns to '{guide.sequence[index[back[0]]].heading.text}', "
                            f"which is neither '{guide.sequence[anchor].heading.text}', where it is taken, "
                            f"nor the unit that follows it")
        declared[topic.slug] = (status, back[0] if back else None)
    report.check(not problems, "every Modern topic states how to take it and where the numbered path resumes",
                 "; ".join(problems[:6]))

    problems = []
    tables = [b for b in (guide.modern.intro if guide.modern else []) if b.type == "table"]
    if len(tables) != 1:
        problems.append(f"the section lists its topics in {len(tables)} tables, not one")
    else:
        columns = doc.table_rows(tables[0])[0]
        if columns != labels["hub_columns"]:
            problems.append(f"the topic table's columns are {columns}")
        else:
            col = {name: columns.index(name) for name in columns}
            rows = table_cells(doc, tables[0])
            listed = [next(iter(cell_links(r[col["Topic"]])), None) for r in rows]
            if listed != [t.slug for t in guide.stages]:
                problems.append("the topic table is not every topic, in the order the section presents them")
            for slug, row in zip(listed, rows):
                if slug not in declared:
                    continue
                status, back = declared[slug]
                listed_status = status_word(inline_text(row[col["How to take it"]]), statuses)
                if listed_status != status:
                    problems.append(f"the table calls '{slug}' {listed_status}, the topic says {status}")
                target = inline_text(row[col["Return to"]]).casefold()
                expected = guide.sequence[index[back]] if back else None
                if expected is None:
                    continue
                step = expected.kind == "step"
                name = f"step {expected.number}" if step else "checkpoint"
                if not re.search(rf"\bstep\s+{expected.number}\b" if step else r"\bcheckpoint\b", target):
                    problems.append(f"the table returns from '{slug}' to '{target}', the topic to {name}")
    report.check(not problems, "the section's table of topics agrees with the topics themselves",
                 "; ".join(problems[:6]))


def gate_item_counts(roadmap: MarkdownDocument, section: str) -> dict[str, int]:
    """How many criteria each ROADMAP readiness gate lists (gates stated as a list only)."""
    blocks = roadmap.section_blocks(section_heading(roadmap, 2, section))
    counts: dict[str, int] = {}
    for k, b in enumerate(blocks):
        label = roadmap.paragraph_label(b)
        if label and k + 1 < len(blocks) and blocks[k + 1].type == "bullet_list":
            lst = blocks[k + 1]
            counts[label[0].rstrip(".")] = sum(1 for t in roadmap.tokens[lst.start:lst.end]
                                               if t.type == "list_item_open" and t.level == 1)
    return counts


# ----- the learner unit: context and concepts before resources ---------------------------------


def label_order(doc: MarkdownDocument, blocks: list[Block]) -> list[str]:
    """Label-only paragraphs of a unit, in the order the learner meets them."""
    out: list[str] = []
    for b in blocks:
        kids = meaningful(doc.tokens[b.start + 1].children) if b.type == "paragraph" else []
        if len(kids) == 3 and kids[0].type == "strong_open" and kids[2].type == "strong_close":
            out.append(kids[1].content.strip())
    return out


def italic_titles(doc: MarkdownDocument, blocks: list[Block]) -> list[str]:
    out: list[str] = []
    for b in blocks:
        for t in doc.tokens[b.start:b.end]:
            if t.type != "inline":
                continue
            kids = meaningful(t.children)
            out += [kids[k + 1].content.strip() for k, c in enumerate(kids)
                    if c.type == "em_open" and k + 1 < len(kids) and kids[k + 1].type == "text"]
    return out


def list_items(doc: MarkdownDocument, blocks: list[Block]) -> list[list[Token]]:
    """Top-level items of the first list in a section."""
    items: list[list[Token]] = []
    for b in blocks:
        if b.type not in ("bullet_list", "ordered_list"):
            continue
        current: list[Token] = []
        for t in doc.tokens[b.start:b.end]:
            if t.type == "list_item_open" and t.level == 1:
                current = []
            elif t.type == "inline":
                current += meaningful(t.children)
            elif t.type == "list_item_close" and t.level == 1:
                items.append(current)
        if items:
            break
    return items


def check_unit_shape(report: ValidationReport, guide: Guide, spec: Specification, cfg: dict,
                     extra_titles: list[str]) -> None:
    """Every learning unit explains itself before it assigns reading.

    A unit opens with why it exists, says where the learner is, organizes the subject as
    concepts (not a book's contents), connects them, places them in the learner's picture of
    AI, and only then names resources — with a map from concept to source, and capability-based
    readiness. Mastery and Research units keep the shape that fits them.
    """
    doc = guide.doc
    allowed = {e.key for e in spec.reading_plan} | {k for _, keys in spec.practice_rows for k in keys} \
        | set(spec.optional) | set(extra_titles)
    full_parts = set(cfg["full_shape_parts"])
    problems: list[str] = []
    units = [(s, s.part.title if s.part else "") for s in guide.sequence if s.kind == "step"] + \
        [(s, cfg["modern_part"]) for s in guide.stages]
    last = units[-1][0] if units else None

    for step, part in units:
        name = step.heading.text
        sections = labelled_sections(doc, step.shell)
        order = label_order(doc, step.shell)
        lead = (step.front or step.blocks or [None])[0]
        if lead is None or lead.type != "paragraph" or doc.paragraph_label(lead):
            problems.append(f"'{name}' does not open by saying why it exists")
        context = cfg["modern_context_label"] if part == cfg["modern_part"] else cfg["context_label"]
        if context not in sections:
            problems.append(f"'{name}' does not say where the learner is")
        full = part in full_parts
        needed = [cfg["toc_label"], cfg["connect_label"], cfg["fits_label"], cfg["practice_label"]] if full \
            else [cfg["practice_label"]]
        missing = [l for l in needed if l not in sections]
        if missing:
            problems.append(f"'{name}' lacks {missing}")
        if not any(l in sections for l in cfg["ready_labels"]):
            problems.append(f"'{name}' states no capability-based readiness")
        if step is not last and not any(l in sections for l in cfg["next_labels"]):
            problems.append(f"'{name}' does not say why the next unit follows")
        if not step.areas and name not in cfg["no_hierarchy"]:
            problems.append(f"'{name}' has no concept hierarchy for its contents to be built from")
        if step.areas:
            # A real hierarchy: areas with concepts, each concept saying where it is studied.
            if len(step.areas) < cfg["min_areas"]:
                problems.append(f"'{name}' has only {len(step.areas)} concept areas")
            thin = [a.heading.text for a in step.areas if len(a.concepts) < cfg["min_concepts"]]
            if thin:
                problems.append(f"'{name}': areas without concepts beneath them: {thin}")
            named_after_source = [h for h in [a.heading.text for a in step.areas]
                                  + [c.heading.text for a in step.areas for c in a.concepts]
                                  if any(h.startswith(r) for r in allowed if len(r) >= 8)]
            if named_after_source:
                problems.append(f"'{name}' organizes its contents by resource, not by concept: {named_after_source}")
            for area in step.areas:
                if not block_text(doc, area.intro).strip():
                    problems.append(f"'{name}': area '{area.heading.text}' has no context")
                for c in area.concepts:
                    if cfg["concept_source_label"] not in block_text(doc, c.blocks):
                        problems.append(f"'{name}': concept '{c.heading.text}' does not say where it is studied")
        elif cfg["toc_label"] in sections:
            items = list_items(doc, sections[cfg["toc_label"]])
            groups = [i for i in items if i and i[0].type == "strong_open"]
            if full and (len(groups) < cfg["min_concept_groups"] or len(groups) != len(items)):
                problems.append(f"'{name}' is a topic list, not a conceptual organization: "
                                f"{len(groups)} named areas in {len(items)} entries")
        # resources come after the concepts, never before them
        if cfg["study_label"] in order:
            study_at = order.index(cfg["study_label"])
            early = [l for l in (context, cfg["toc_label"], cfg["connect_label"], cfg["fits_label"])
                     if l in order and order.index(l) > study_at]
            if early:
                problems.append(f"'{name}' puts resources before {early}")
            count = len(list_items(doc, sections.get(cfg["study_label"], [])))
            if count >= 2 and cfg["map_label"] not in sections:
                problems.append(f"'{name}' uses {count} sources without a concept-to-resource map")
        if cfg["map_label"] in sections:
            if not any(b.type == "table" for b in sections[cfg["map_label"]]):
                problems.append(f"'{name}': the concept-to-resource map is not a table")
            foreign = [t for t in italic_titles(doc, sections[cfg["map_label"]])
                       if not any(a.startswith(t) or t.startswith(a) for a in allowed)]
            if foreign:
                problems.append(f"'{name}' maps concepts to resources the curriculum does not assign: {foreign}")
    report.check(not problems, "every unit explains itself before it assigns reading", "; ".join(problems[:8]))

    problems = []
    for part in guide.parts:
        sections = labelled_sections(doc, part.intro)
        missing = [l for l in cfg["stage_labels"] if l not in sections]
        if missing:
            problems.append(f"'{part.title}' lacks {missing}")
    report.check(not problems, "every stage introduction states its purpose and what it develops",
                 "; ".join(problems[:4]))
