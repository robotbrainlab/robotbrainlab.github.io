"""Extraction of explicitly recorded structure from canonical sources.

Nothing here decides curriculum. Each function reads structure that the
canonical files already state (a diagram, a heading, a bold label) and fails
loudly if that structure is missing instead of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from markdown_it.token import Token

from .markdown import Block, Heading, MarkdownDocument, inline_text, meaningful

NODE = re.compile(r'(\w+)\["([^"]*)"\]')
SUBGRAPH = re.compile(r"^subgraph\s+(\w+)")
PARALLEL_EDGE = re.compile(r"(\w+)\s*<[-.]+>\s*(\w+)")
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


class ExtractionError(RuntimeError):
    """Canonical structure required for a page is missing or ambiguous."""


@dataclass
class Architecture:
    stages: list[str]
    track: str
    track_note: str


def _clean_label(label: str) -> tuple[str, str]:
    parts = [p.strip() for p in label.split("<br/>")]
    name = parts[0]
    note = " ".join(parts[1:]).strip().strip("()").strip()
    return name, note


def roadmap_architecture(roadmap: MarkdownDocument) -> Architecture:
    """Read the depth sequence and the parallel track from the canonical diagram.

    ROADMAP.md states its two-dimensional structure as a Mermaid diagram: a
    subgraph containing the sequential stages, and a node outside it linked to
    the subgraph with a bidirectional edge.
    """
    for fence in roadmap.fences("mermaid"):
        stages: list[str] = []
        stage_ids: set[str] = set()
        outside: dict[str, str] = {}
        subgraph_id = None
        parallels: list[tuple[str, str]] = []
        inside = False
        for raw in fence.content.splitlines():
            line = raw.strip()
            match = SUBGRAPH.match(line)
            if match:
                subgraph_id, inside = match.group(1), True
                continue
            if line == "end":
                inside = False
                continue
            for node_id, label in NODE.findall(line):
                if inside and node_id != subgraph_id:
                    if node_id not in stage_ids:
                        stage_ids.add(node_id)
                        stages.append(label)
                elif not inside:
                    outside[node_id] = label
            parallels.extend(PARALLEL_EDGE.findall(line))
        if not stages or subgraph_id is None:
            continue
        linked = {b for a, b in parallels if a in stage_ids | {subgraph_id}} | {
            a for a, b in parallels if b in stage_ids | {subgraph_id}
        }
        tracks = [outside[n] for n in outside if n in linked]
        if len(tracks) == 1:
            name, note = _clean_label(tracks[0])
            return Architecture([_clean_label(s)[0] for s in stages], name, note)
    raise ExtractionError(f"{roadmap.rel_path}: no Mermaid diagram states a stage sequence with one parallel track")


@dataclass
class ReportInfo:
    rel_path: str
    title: str
    date: str | None
    labels: dict[str, str]


def preamble_labels(doc: MarkdownDocument) -> dict[str, str]:
    """Labelled values stated before the first H2.

    Two canonical conventions exist: ``**Label:** value`` lines (one or several
    per paragraph) and a two-column header table with bold labels.
    """
    labels: dict[str, str] = {}
    for block in doc.preamble_blocks():
        if block.type == "paragraph":
            line: list[Token] = []
            lines = [line]
            for child in doc.tokens[block.start + 1].children or []:
                if child.type in ("softbreak", "hardbreak"):
                    line = []
                    lines.append(line)
                else:
                    line.append(child)
            for parts in lines:
                kids = meaningful(parts)
                if len(kids) < 3 or kids[0].type != "strong_open":
                    continue
                close = next((k for k, c in enumerate(kids) if c.type == "strong_close"), None)
                if close is None:
                    continue
                label = "".join(c.content for c in kids[1:close] if c.type == "text").strip().rstrip(":").strip()
                rest = Token("inline", "", 0)
                rest.children = kids[close + 1 :]
                value = inline_text(rest).strip().lstrip(":").strip()
                if label and value:
                    labels.setdefault(label, value)
        elif block.type == "table":
            for row in doc.table_rows(block):
                if len(row) == 2 and row[0]:
                    labels.setdefault(row[0].strip("*").strip(), row[1].strip("*").strip())
    return labels


def report_info(doc: MarkdownDocument) -> ReportInfo:
    stem = doc.rel_path.rsplit("/", 1)[-1]
    date = DATE_PREFIX.match(stem)
    return ReportInfo(doc.rel_path, doc.title, date.group(1) if date else None, preamble_labels(doc))


# ----- ROADMAP.md structure -----------------------------------------------------

EDGE = re.compile(r"(-\.->|-->)")
NODE_ID = re.compile(r"^(\w+)")


@dataclass
class Edge:
    source: str
    target: str
    hard: bool


def dependency_edges(doc: MarkdownDocument, heading: Heading) -> list[Edge]:
    """Edges of the Mermaid diagram in a section: ``-->`` hard, ``-.->`` recommended."""
    end = doc.section_end(heading)
    fence = next(
        (t for t in doc.tokens[heading.index : end] if t.type == "fence" and t.info.strip() == "mermaid"), None
    )
    if fence is None:
        raise ExtractionError(f"{doc.rel_path}: no Mermaid diagram under '{heading.text}'")
    edges: list[Edge] = []
    for raw in fence.content.splitlines():
        parts = EDGE.split(raw.strip())
        for k in range(1, len(parts) - 1, 2):
            a, b = NODE_ID.match(parts[k - 1].strip()), NODE_ID.match(parts[k + 1].strip())
            if a and b:
                edges.append(Edge(a.group(1), b.group(1), parts[k] == "-->"))
    if not edges:
        raise ExtractionError(f"{doc.rel_path}: dependency diagram has no edges")
    return edges


def labelled_paragraph(doc: MarkdownDocument, heading: Heading, label: str) -> Block:
    """A paragraph in a section that opens with the given bold label."""
    wanted = label.rstrip(".:").casefold()
    for block in doc.section_blocks(heading, direct_only=False):
        parsed = doc.paragraph_label(block)
        if parsed and parsed[0].rstrip(".:").casefold() == wanted:
            return block
    raise ExtractionError(f"{doc.rel_path}: no paragraph labelled '{label}' under '{heading.text}'")


def table_after(doc: MarkdownDocument, heading: Heading, block: Block) -> Block:
    blocks = doc.section_blocks(heading, direct_only=False)
    for b in blocks[blocks.index(block) + 1 :]:
        if b.type == "table":
            return b
    raise ExtractionError(f"{doc.rel_path}: no table follows the paragraph at token {block.start}")


def table_cells(doc: MarkdownDocument, block: Block) -> list[list[Token]]:
    """Body rows of a table as lists of inline tokens."""
    rows: list[list[Token]] = []
    row: list[Token] | None = None
    in_body = False
    for t in doc.tokens[block.start : block.end]:
        if t.type == "tbody_open":
            in_body = True
        elif t.type == "tr_open" and in_body:
            row = []
        elif t.type == "inline" and row is not None:
            row.append(t)
        elif t.type == "tr_close" and row is not None:
            rows.append(row)
            row = None
    return rows


def section_heading(doc: MarkdownDocument, level: int, name: str) -> Heading:
    heading = doc.find_heading(level, name)
    if heading is None:
        raise ExtractionError(f"{doc.rel_path}: heading not found: {'#' * level} {name}")
    return heading


