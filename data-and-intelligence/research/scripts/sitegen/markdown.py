"""Markdown parsing, document model and presentation rendering.

Parsing produces a token stream per canonical file. Rendering transforms that
stream into HTML without changing canonical wording: it only adds structure
(sections, anchors, table wrappers, callout classes) and presentation chrome
marked with ``data-chrome`` so validation can tell chrome from content.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from .slugs import Slugger

NUMBER_PREFIX = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s+")
CITATION = re.compile(
    r"^\[[A-Z]\d+(?:[–-][A-Z]?\d+)?(?:,\s*[A-Z]\d+(?:[–-][A-Z]?\d+)?)*\]$"
)
REGISTER_ID = re.compile(r"^[A-Z]\d+$")
JUSTIFY_OPEN = '<div align="justify">'
JUSTIFY_CLOSE = "</div>"
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
INLINE_TAG = re.compile(r"^</?([a-zA-Z][a-zA-Z0-9-]*)")
HTML_ELEMENTS = frozenset(
    "a abbr b bdi bdo br cite code data del details dfn div em i img ins kbd mark p q s samp small span "
    "strong sub summary sup time u var wbr".split()
)


def is_literal_placeholder(html: str) -> bool:
    """True for inline "tags" that are not HTML, such as ``<date>`` or ``<file>``.

    Canonical documents use angle brackets for placeholders; they are text.
    """
    m = INLINE_TAG.match(html)
    return bool(m) and m.group(1).lower() not in HTML_ELEMENTS


def create_parser() -> MarkdownIt:
    """CommonMark + GFM tables, strikethrough, raw HTML and bare-URL linkify."""
    md = MarkdownIt("gfm-like", {"typographer": False})
    # Link bare URLs only; GitHub does not turn file names such as AGENTS.md
    # (".md" is also a top-level domain) into links.
    md.linkify.set({"fuzzy_link": False, "fuzzy_email": False})
    return md


def strip_number(text: str) -> str:
    return NUMBER_PREFIX.sub("", text).strip()


def meaningful(children: list[Token] | None) -> list[Token]:
    """Inline children without empty or whitespace-only text tokens."""
    return [c for c in (children or []) if not (c.type == "text" and not c.content.strip())]


def inline_text(token: Token | None) -> str:
    if token is None:
        return ""
    parts: list[str] = []
    for child in token.children or []:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return "".join(parts)


@dataclass
class Heading:
    level: int
    text: str
    slug: str
    index: int


@dataclass
class Block:
    """A top-level block: a slice of tokens [start, end)."""

    start: int
    end: int
    type: str


class MarkdownDocument:
    """A parsed canonical Markdown file with heading slugs assigned."""

    def __init__(self, repo_root: Path, rel_path: str, md: MarkdownIt) -> None:
        self.rel_path = rel_path
        self.path = repo_root / rel_path
        self.source = self.path.read_text(encoding="utf-8")
        self.md = md
        self.tokens: list[Token] = md.parse(self.source, {})
        self.headings: list[Heading] = []
        slugger = Slugger()
        for i, token in enumerate(self.tokens):
            if token.type == "heading_open":
                text = inline_text(self.tokens[i + 1])
                slug = slugger.slug(text)
                token.attrSet("id", slug)
                self.headings.append(Heading(int(token.tag[1]), text, slug, i))

    # ----- structure helpers -------------------------------------------------

    @property
    def title(self) -> str:
        for h in self.headings:
            if h.level == 1:
                return h.text
        return Path(self.rel_path).stem

    def find_heading(self, level: int, name: str) -> Heading | None:
        wanted = strip_number(name).casefold()
        for h in self.headings:
            if h.level == level and strip_number(h.text).casefold() == wanted:
                return h
        return None

    def section_end(self, heading: Heading) -> int:
        for h in self.headings:
            if h.index > heading.index and h.level <= heading.level:
                return h.index
        return len(self.tokens)

    def subheadings(self, heading: Heading, level: int) -> list[Heading]:
        end = self.section_end(heading)
        return [h for h in self.headings if heading.index < h.index < end and h.level == level]

    def blocks(self, start: int, end: int) -> list[Block]:
        """Top-level blocks between token indices (nesting level 0)."""
        out: list[Block] = []
        i = start
        while i < end:
            t = self.tokens[i]
            if t.level != 0:
                i += 1
                continue
            if t.nesting == 1:
                close = t.type.replace("_open", "_close")
                j = i + 1
                while j < len(self.tokens):
                    c = self.tokens[j]
                    if c.nesting == -1 and c.level == 0 and c.type == close:
                        break
                    j += 1
                out.append(Block(i, j + 1, t.type.replace("_open", "")))
                i = j + 1
            else:
                out.append(Block(i, i + 1, t.type))
                i += 1
        return out

    def heading_at(self, token_index: int) -> Heading:
        return next(h for h in self.headings if h.index == token_index)

    def section_blocks(self, heading: Heading, direct_only: bool = True) -> list[Block]:
        start = heading.index + 3  # heading_open, inline, heading_close
        end = self.section_end(heading)
        if direct_only:
            for h in self.headings:
                if start <= h.index < end:
                    end = h.index
                    break
        return self.blocks(start, end)

    def preamble_blocks(self) -> list[Block]:
        """Blocks after the H1 and before the first H2."""
        h1 = next((h for h in self.headings if h.level == 1), None)
        start = h1.index + 3 if h1 else 0
        end = next((h.index for h in self.headings if h.level == 2), len(self.tokens))
        return self.blocks(start, end)

    def paragraph_label(self, block: Block) -> tuple[str, str] | None:
        """Return (label, value) for a paragraph starting with a bold label.

        Matches the canonical convention ``**Label:** value`` and ``**Label**``.
        """
        if block.type != "paragraph":
            return None
        children = meaningful(self.tokens[block.start + 1].children)
        if len(children) < 3 or children[0].type != "strong_open":
            return None
        close = next((k for k, c in enumerate(children) if c.type == "strong_close"), None)
        if close is None:
            return None
        label = "".join(c.content for c in children[1:close] if c.type == "text").strip()
        rest = Token("inline", "", 0)
        rest.children = children[close + 1 :]
        value = inline_text(rest).strip()
        return label.rstrip(":").strip(), value

    def label_value(self, blocks: list[Block], label: str) -> str | None:
        for k, block in enumerate(blocks):
            parsed = self.paragraph_label(block)
            if parsed and parsed[0].casefold() == label.casefold():
                if parsed[1]:
                    return parsed[1]
                if k + 1 < len(blocks) and blocks[k + 1].type == "paragraph":
                    return inline_text(self.tokens[blocks[k + 1].start + 1]).strip()
        return None

    def is_nav_paragraph(self, block: Block) -> bool:
        """True for canonical navigation lines such as "Back to Contents"."""
        if block.type != "paragraph":
            return False
        children = meaningful(self.tokens[block.start + 1].children)
        links = [c for c in children if c.type == "link_open"]
        return len(links) == 1 and links[0].attrGet("href") == "#contents"

    def first_plain_paragraph(self, blocks: list[Block]) -> Block | None:
        """First paragraph that is prose: not a bold label, not navigation."""
        for block in blocks:
            if block.type == "paragraph" and not self.paragraph_label(block) and not self.is_nav_paragraph(block):
                return block
        return None

    def table_rows(self, block: Block) -> list[list[str]]:
        rows: list[list[str]] = []
        current: list[str] | None = None
        for t in self.tokens[block.start : block.end]:
            if t.type == "tr_open":
                current = []
            elif t.type == "inline" and current is not None:
                current.append(inline_text(t).strip())
            elif t.type == "tr_close" and current is not None:
                rows.append(current)
                current = None
        return rows

    def fences(self, info: str) -> list[Token]:
        return [t for t in self.tokens if t.type == "fence" and t.info.strip().split()[:1] == [info]]


# ----- rendering -------------------------------------------------------------


@dataclass
class RenderContext:
    """Per-render state passed to renderer rules through ``env``."""

    source_rel: str
    page_rel: str  # output path of the page, e.g. "research/x/index.html"
    page_map: dict[str, str]  # canonical source path -> output page path
    aliases: dict[str, str] = field(default_factory=dict)  # non-Markdown path -> page
    page_kinds: dict[str, str] = field(default_factory=dict)  # page -> document kind
    anchor_map: dict[str, str] = field(default_factory=dict)  # in-document anchor -> page that now holds it
    split_source: str = ""  # a document rendered across many pages (the guide)
    split_anchors: dict[str, str] = field(default_factory=dict)  # its anchors -> the page that holds each
    kind_labels: dict[str, str] = field(default_factory=dict)  # kind -> cross-context label
    kind: str = ""  # kind of the page being rendered
    presentation: dict = field(default_factory=dict)
    sectioning: bool = False
    before_h1: str = ""
    after_h1: str = ""
    inserts: dict[int, str] = field(default_factory=dict)  # token index -> chrome HTML placed before it
    container: str | None = None
    current_heading: str = ""
    table_is_register: bool = False
    table_is_kv: bool = False
    table_headers: list[str] = field(default_factory=list)
    column: int = -1
    cell_mode: str = ""  # "resources" or "role" while inside such a cell
    has_mermaid: bool = False
    guide: bool = False  # learner-guide rendering: labelled paragraphs open styled blocks
    guide_block: str = ""
    guide_list_done: bool = False
    link_stack: list[str] = field(default_factory=list)
    unavailable_links: list[str] = field(default_factory=list)

    def close_container(self) -> str:
        if self.container is None:
            return ""
        tag = self.container
        self.container = None
        return f"</{tag}>\n"

    def resolve(self, href: str) -> tuple[str, str]:
        if not href:
            return "anchor", href
        if href.startswith("#"):
            if href[1:] in self.anchor_map:
                target = self.anchor_map[href[1:]]
                rel = posixpath.relpath(target.partition("#")[0], posixpath.dirname(self.page_rel) or ".")
                return "internal", rel + ("#" + target.partition("#")[2] if "#" in target else "")
            return "anchor", href
        if EXTERNAL.match(href):
            return "external", href
        path, _, frag = href.partition("#")
        target = posixpath.normpath(posixpath.join(posixpath.dirname(self.source_rel), path))
        if target == self.split_source and frag in self.split_anchors:
            # The guide is one document served as many pages: a link into it must land on the
            # page that now holds that section, not on the guide's own landing page.
            page = self.split_anchors[frag]
        else:
            page = self.page_map.get(target)
        if page is None and target.rstrip("/") in self.aliases:
            page, frag = self.aliases[target.rstrip("/")], ""
        if page is not None:
            rel = posixpath.relpath(page, posixpath.dirname(self.page_rel) or ".")
            return "internal", rel + (f"#{frag}" if frag else "")
        self.unavailable_links.append(href)
        return "unavailable", href

    def target_kind(self, href: str) -> str:
        """Document kind of the page an internal link points to ('' if unknown)."""
        path = href.partition("#")[0]
        if not path:
            return ""
        page = posixpath.normpath(posixpath.join(posixpath.dirname(self.page_rel), path))
        return self.page_kinds.get(page, "")


def _render_default(self, tokens, idx, options, env):
    return self.renderToken(tokens, idx, options, env)


def _heading_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    token = tokens[idx]
    level = int(token.tag[1])
    ctx.current_heading = inline_text(tokens[idx + 1])
    out = []
    if ctx.guide and level >= 4:
        # A unit's concept hierarchy: H4 areas and H5 concepts become the page's own sections.
        out.append(ctx.close_container())
        ctx.guide_block = ""
        token.tag = f"h{level - 2}"
        tokens[idx + 2].tag = token.tag
        out.append(f'<section class="unit-{"area" if level == 4 else "concept"}" '
                   f'aria-labelledby="{token.attrGet("id")}">\n')
        ctx.container = "section"
    if level == 2 and ctx.sectioning:
        out.append(ctx.close_container())
        slug = token.attrGet("id")
        if slug == "contents":
            out.append(f'<nav class="doc-contents" aria-labelledby="{slug}">\n')
            ctx.container = "nav"
        else:
            out.append(f'<section class="doc-section" aria-labelledby="{slug}">\n')
            ctx.container = "section"
    if level == 1 and ctx.before_h1:
        out.append(ctx.before_h1)
    out.append(self.renderToken(tokens, idx, options, env))
    return "".join(out)


def _heading_close(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    token = tokens[idx]
    level = int(token.tag[1])
    slug = tokens[idx - 2].attrGet("id")
    anchor = ""
    if level >= 2 and slug and (ctx.sectioning or ctx.guide):
        anchor = (
            f'<a class="heading-anchor" href="#{slug}" data-chrome>'
            '<span aria-hidden="true">#</span>'
            '<span class="visually-hidden">Link to this section</span></a>'
        )
    out = f"{anchor}</{token.tag}>\n"
    if level == 1 and ctx.after_h1:
        out += ctx.after_h1
    return out


def _label_only(children: list[Token]) -> str:
    """The label of a paragraph that is nothing but a bold label, else ''."""
    if len(children) == 3 and children[0].type == "strong_open" and children[2].type == "strong_close" \
            and children[1].type == "text":
        return children[1].content.strip()
    return ""


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def _paragraph_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    token = tokens[idx]
    if token.hidden:
        return ""
    children = meaningful(tokens[idx + 1].children)
    if ctx.guide:
        label = _label_only(children)
        if label:
            ctx.guide_block, ctx.guide_list_done = _slug(label), False
            opened = ctx.close_container()
            ctx.container = "section"
            return (f'{opened}<section class="guide-block guide-block--{ctx.guide_block}" '
                    f'aria-label="{escape(label)}">\n<p class="guide-label">')
        if ctx.guide_block.startswith("you-re-ready") and ctx.guide_list_done:
            ctx.guide_block = ""
            return ctx.close_container() + '<p class="guide-note">'
    if (
        len(children) >= 2
        and children[0].type == "strong_open"
        and children[1].type == "text"
        and children[1].content.strip() == "In this section:"
    ):
        return '<p class="section-subnav">'
    links = [c for c in children if c.type == "link_open"]
    others = [c for c in children if c.type == "text" and c.content.strip() and "Back to Contents" not in c.content]
    if (
        len(links) == 1
        and links[0].attrGet("href") == "#contents"
        and "Back to Contents" in inline_text(tokens[idx + 1])
        and not others
    ):
        return '<p class="back-to-contents">'
    return self.renderToken(tokens, idx, options, env)


def _blockquote_open(self, tokens, idx, options, env):
    depth = 0
    end = idx
    for j in range(idx, len(tokens)):
        if tokens[j].type == "blockquote_open":
            depth += 1
        elif tokens[j].type == "blockquote_close":
            depth -= 1
            if depth == 0:
                end = j
                break
    inner = tokens[idx + 1 : end]
    inlines = [t for t in inner if t.type == "inline"]
    first = inline_text(inlines[0]).lstrip() if inlines else ""
    if first.startswith("⚠"):
        return '<blockquote class="callout callout-warning">\n'
    paragraphs = [t for t in inner if t.type == "paragraph_open"]
    if len(paragraphs) == 1 and inlines:
        kids = meaningful(inlines[0].children)
        if kids and kids[0].type == "strong_open" and kids[-1].type == "strong_close" and sum(
            1 for c in kids if c.type == "strong_open"
        ) == 1:
            return '<blockquote class="quote quote-principle">\n'
    return '<blockquote class="quote">\n'


def _list_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    if ctx.guide and ctx.guide_block and tokens[idx].level == 0:
        tokens[idx].attrSet("class", f"guide-list guide-list--{ctx.guide_block}")
    return self.renderToken(tokens, idx, options, env)


def _list_close(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    if tokens[idx].level == 0:
        ctx.guide_list_done = True
    return self.renderToken(tokens, idx, options, env)


def _table_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    headers: list[str] = []
    j = idx
    while j < len(tokens) and tokens[j].type != "thead_close":
        if tokens[j].type == "th_open":
            headers.append(inline_text(tokens[j + 1]).strip())
        j += 1
    cols = len(headers)
    wrap = ["table-wrap"]
    table = ["doc-table"]
    if cols >= 5:
        wrap.append("breakout")
        table.append("table--wide")
    if headers and all(not h for h in headers):
        table.append("table--kv")
    if cols == 2 and headers and any(headers):
        # A two-column table is a list of pairs: on a phone it reads better stacked.
        table.append("table--pair")
    ctx.table_is_register = bool(headers) and headers[0] == "ID"
    ctx.table_is_kv = bool(headers) and all(not h for h in headers)
    ctx.table_headers = headers
    label = f"Table: {ctx.current_heading}" if ctx.current_heading else "Table"
    hint = (
        '<p class="table-hint" data-chrome>Wide table — scroll horizontally</p>'
        if "breakout" in wrap
        else ""
    )
    return (
        f'{hint}<div class="{" ".join(wrap)}" role="region" tabindex="0" aria-label="{escape(label)}">'
        f'<table class="{" ".join(table)}" style="--cols:{cols}">\n'
    )


def _table_close(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    ctx.table_is_register = ctx.table_is_kv = False
    ctx.table_headers = []
    return "</table></div>\n"


def _drop_alignment(token) -> None:
    """Column alignment from Markdown (``:---:``) is presentation; the site justifies all text."""
    style = token.attrGet("style") or ""
    if "text-align" in style:
        token.attrs.pop("style", None)


def _th_open(self, tokens, idx, options, env):
    _drop_alignment(tokens[idx])
    tokens[idx].attrSet("scope", "col")
    return self.renderToken(tokens, idx, options, env)


def _tr_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    ctx.column = -1
    first = inline_text(tokens[idx + 2]).strip() if idx + 2 < len(tokens) and tokens[idx + 1].type == "td_open" else ""
    if ctx.table_is_register and REGISTER_ID.match(first):
        tokens[idx].attrSet("id", f"src-{first.lower()}")
    if ctx.table_is_kv and first:
        classes = [f"kv-row kv-row--{re.sub(r'[^a-z0-9]+', '-', first.casefold()).strip('-')}"]
        if first in ctx.presentation.get("emphasis_rows", ()):
            classes.append("kv-row--emphasis")
        if first in ctx.presentation.get("resource_rows", ()):
            classes.append("kv-row--resources")
        tokens[idx].attrSet("class", " ".join(classes))
    return self.renderToken(tokens, idx, options, env)


def _td_open(self, tokens, idx, options, env):
    _drop_alignment(tokens[idx])
    ctx: RenderContext = env["ctx"]
    ctx.column += 1
    ctx.cell_mode = ""
    if ctx.table_is_kv and ctx.column == 1:
        label = inline_text(tokens[idx - 2]).strip() if tokens[idx - 3].type == "td_open" else ""
        if label in ctx.presentation.get("resource_rows", ()):
            ctx.cell_mode = "resources"
    elif (
        ctx.presentation.get("role_column")
        and ctx.column < len(ctx.table_headers)
        and ctx.table_headers[ctx.column] == ctx.presentation["role_column"]
    ):
        ctx.cell_mode = "role"
    return self.renderToken(tokens, idx, options, env)


def _td_close(self, tokens, idx, options, env):
    env["ctx"].cell_mode = ""
    return self.renderToken(tokens, idx, options, env)


def _role_badge(role: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", role.casefold()).strip("-")
    return f'<span class="role role--{slug}">{escape(role)}</span>'


def _text(self, tokens, idx, options, env):
    """Plain text; inside resource and role cells, roles are marked for styling.

    Only markup is added: the canonical characters are unchanged.
    """
    ctx: RenderContext = env["ctx"]
    content = tokens[idx].content
    roles = ctx.presentation.get("roles", ())
    if ctx.cell_mode == "role" and content.strip() in roles:
        lead = content[: len(content) - len(content.lstrip())]
        trail = content[len(content.rstrip()) :]
        return escape(lead) + _role_badge(content.strip()) + escape(trail)
    if ctx.cell_mode == "resources" and roles:
        pattern = re.compile(r"(?<=— )(" + "|".join(re.escape(r) for r in sorted(roles, key=len, reverse=True)) + r")\b")
        out = []
        for k, part in enumerate(content.split(" · ")):
            if k:
                out.append('<span class="res-sep"> · </span>')
            pos = 0
            for m in pattern.finditer(part):
                out.append(escape(part[pos : m.start()]))
                out.append(_role_badge(m.group(1)))
                pos = m.end()
            out.append(escape(part[pos:]))
        return "".join(out)
    return escape(content)


def _fence(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    token = tokens[idx]
    info = token.info.strip().split()
    lang = info[0] if info else ""
    if lang == "mermaid":
        ctx.has_mermaid = True
        wide = re.search(r"^\s*(?:flowchart|graph)\s+(?:LR|RL)\b", token.content, re.M)
        cls = "diagram breakout" if wide else "diagram"
        label = f"Diagram: {ctx.current_heading}" if ctx.current_heading else "Diagram"
        return (
            f'<figure class="{cls}" data-diagram aria-label="{escape(label)}">'
            '<figcaption class="diagram-caption" data-chrome>Diagram · text form</figcaption>'
            f'<pre class="diagram-source"><code>{escape(token.content)}</code></pre>'
            "</figure>\n"
        )
    try:
        lexer = get_lexer_by_name(lang) if lang else None
    except ClassNotFound:
        lexer = None
    body = highlight(token.content, lexer, HtmlFormatter(nowrap=True)) if lexer else escape(token.content)
    label = escape(lang.upper()) if lang else "TEXT"
    return (
        f'<div class="code-block" data-lang="{escape(lang)}">'
        f'<div class="code-meta" data-chrome><span class="code-lang">{label}</span></div>'
        f'<pre class="code"><code>{body}</code></pre></div>\n'
    )


def _link_open(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    token = tokens[idx]
    # Tokens are shared between renders of the same document; resolve from the source href.
    href = token.meta.setdefault("source_href", token.attrGet("href") or "")
    token.attrSet("href", href)
    if token.attrs and "class" in token.attrs:
        del token.attrs["class"]
    kind, value = ctx.resolve(href)
    if kind == "external":
        cls = "external"
        if token.markup in ("linkify", "autolink"):
            cls += " autolink"
        token.attrSet("class", cls)
        token.attrSet("rel", "noopener noreferrer")
        ctx.link_stack.append("external")
        return self.renderToken(tokens, idx, options, env)
    if kind == "unavailable":
        ctx.link_stack.append("span")
        return '<span class="link-unavailable" title="Not part of the generated site">'
    if kind == "internal":
        token.attrSet("href", value)
        target = ctx.target_kind(value)
        if target and target != ctx.kind and target in ctx.kind_labels:
            token.attrSet("class", f"xref-link xref-link--{target}")
            ctx.link_stack.append(f"xref:{target}")
            return self.renderToken(tokens, idx, options, env)
    ctx.link_stack.append("a")
    return self.renderToken(tokens, idx, options, env)


def _link_close(self, tokens, idx, options, env):
    ctx: RenderContext = env["ctx"]
    kind = ctx.link_stack.pop() if ctx.link_stack else "a"
    if kind == "span":
        return "</span>"
    if kind == "external":
        return '<span class="visually-hidden" data-chrome> (external link)</span></a>'
    if kind.startswith("xref:"):
        target = kind[5:]
        label = escape(ctx.kind_labels[target])
        return (
            f'<span class="xref xref--{target}" data-chrome>'
            f'<span class="visually-hidden"> (</span>{label}<span class="visually-hidden">)</span></span></a>'
        )
    return "</a>"


def _code_inline(self, tokens, idx, options, env):
    token = tokens[idx]
    if CITATION.match(token.content):
        return f'<code class="cite">{escape(token.content)}</code>'
    return f"<code>{escape(token.content)}</code>"


def _hr(self, tokens, idx, options, env):
    return '<hr class="section-break">\n'


def _html_inline(self, tokens, idx, options, env):
    content = tokens[idx].content
    return escape(content) if is_literal_placeholder(content) else content


def _html_block(self, tokens, idx, options, env):
    token = tokens[idx]
    if token.meta.get("strip"):
        return ""
    return token.content


class PresentationRenderer:
    """Renders token streams with presentation rules."""

    def __init__(self) -> None:
        self.md = create_parser()
        rules = {
            "heading_open": _heading_open,
            "heading_close": _heading_close,
            "paragraph_open": _paragraph_open,
            "blockquote_open": _blockquote_open,
            "table_open": _table_open,
            "table_close": _table_close,
            "th_open": _th_open,
            "tr_open": _tr_open,
            "td_open": _td_open,
            "bullet_list_open": _list_open,
            "ordered_list_open": _list_open,
            "bullet_list_close": _list_close,
            "ordered_list_close": _list_close,
            "td_close": _td_close,
            "text": _text,
            "fence": _fence,
            "link_open": _link_open,
            "link_close": _link_close,
            "code_inline": _code_inline,
            "hr": _hr,
            "html_block": _html_block,
            "html_inline": _html_inline,
        }
        for name, func in rules.items():
            self.md.add_render_rule(name, func)

    def render(self, doc: MarkdownDocument, tokens: list[Token], ctx: RenderContext) -> str:
        html = self.md.renderer.render(tokens, self.md.options, {"ctx": ctx})
        html += ctx.close_container()
        return html

    def render_document(self, doc: MarkdownDocument, ctx: RenderContext) -> str:
        ctx.sectioning = True
        html_blocks = [t for t in doc.tokens if t.type == "html_block"]
        if len(html_blocks) >= 2:
            first, last = html_blocks[0], html_blocks[-1]
            if first.content.strip() == JUSTIFY_OPEN and last.content.strip() == JUSTIFY_CLOSE:
                first.meta["strip"] = last.meta["strip"] = True
        tokens = doc.tokens
        if ctx.inserts:
            tokens = []
            for i, token in enumerate(doc.tokens):
                if i in ctx.inserts:
                    chrome = Token("html_block", "", 0)
                    chrome.content = ctx.inserts[i]
                    tokens.append(chrome)
                tokens.append(token)
        return self.render(doc, tokens, ctx)

    def render_blocks(self, doc: MarkdownDocument, blocks: list[Block], ctx: RenderContext) -> str:
        tokens = [t for b in blocks for t in doc.tokens[b.start : b.end]]
        return self.render(doc, tokens, ctx) if tokens else ""

    def render_inline_of(self, doc: MarkdownDocument, block: Block, ctx: RenderContext) -> str:
        """Render only the inline content of a paragraph block (no <p>)."""
        return self.render_inline(doc.tokens[block.start + 1].children or [], ctx)

    def render_inline(self, children: list[Token], ctx: RenderContext) -> str:
        """Render inline tokens (the content of a paragraph, list item or cell)."""
        return self.md.renderer.render(children, self.md.options, {"ctx": ctx})
