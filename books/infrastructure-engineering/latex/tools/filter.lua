--[[
filter.lua — turns one Markdown chapter into LaTeX for the "from Zero" book template.

Metadata (passed with -M by convert.sh):
  stem      file stem, used for labels                 (e.g. 03-http-and-json)
  buildset  comma-separated stems of every Markdown file in the book (for cross-file links)

Markdown conventions (see README.md):
  # Title                         -> \bookchapter (numbered in \mainmatter, lettered after
                                     \appendix, unnumbered in \frontmatter, e.g. the Preface)
  first paragraph after # Title   -> the chapter intro
  ## Section / ### Sub / #### Sub -> \section (in contents + running head) / \subsection* / \subsubsection*
  > **Tip:** / **Note:** / **Warning:** …    -> callout with its icon (the label word is dropped)
  > [!TIP] / [!NOTE] / [!WARNING] …          -> the same (GitHub alert syntax)
  > **You understand this when** …           -> the chapter's self-check box
  ```python / ```bash …           -> highlighted code, wraps long lines
  ``` (no language) / ```text     -> program output; if it contains box-drawing characters,
                                     it is a diagram: never wrapped, font sized to fit the width
  | tables |                      -> full-width booktabs table, columns sized from content
  Term / : definition             -> "Term: definition" entries (Key Terms, Glossary);
                                     sorted A–Z in a file whose title is "Glossary"
  [word]{.idx} / [words]{idx="key"} / []{idx="key"}   -> index entries
  [text](other-file.md#heading)   -> cross-reference inside the PDF
]]

local stem, buildset = '', {}
local is_glossary = false

local BOX_CHARS = { '┌', '┐', '└', '┘', '│', '├', '┤', '┬', '┴', '┼', '─', '━', '═', '║',
  '╔', '╗', '╚', '╝', '╭', '╮', '╯', '╰', '▶', '▼', '◀', '▲' }

-- Geometry the sizing rules rely on (keep in sync with preamble.tex)
local TEXT_WIDTH   = 378      -- pt
local CODE_INDENT  = 10.66    -- pt
local MONO_SCALE   = 0.85     -- Source Code Pro Scale=
local MONO_ADVANCE = 0.602    -- em (Source Code Pro 0.600, DejaVu Sans Mono 0.602)
local CODE_SIZE    = 8.8      -- nominal \fontsize of code blocks (7.5 pt effective)
local SHORT_BLOCK  = 14       -- code blocks up to this many lines are kept on one page

-- ---------------------------------------------------------------- helpers
local function raw(s) return pandoc.RawBlock('latex', s) end
local function rawi(s) return pandoc.RawInline('latex', s) end

local function to_latex(inlines)
  local s = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'latex')
  return (s:gsub('%s+$', ''))
end

local function blocks_latex(blocks)
  local s = pandoc.write(pandoc.Pandoc(blocks), 'latex')
  return (s:gsub('%s+$', ''))
end

local function esc(text) return to_latex({ pandoc.Str(text) }) end

local function warn(msg) io.stderr:write('  [' .. stem .. '] ' .. msg .. '\n') end

-- title usable both on the page and in PDF bookmarks
local function heading_text(inlines)
  local tex = to_latex(inlines)
  local plain = esc(pandoc.utils.stringify(inlines))
  if tex == plain then return tex end
  return '\\texorpdfstring{' .. tex .. '}{' .. plain .. '}'
end

local function clean_label(s) return (s:gsub('_', '-'):gsub('[^%w%-:%.]', '')) end
local function label_for(file_stem, frag)
  if frag and frag ~= '' then return clean_label(file_stem .. ':' .. frag) end
  return clean_label('ch:' .. file_stem)
end

local function nlines(text) local _, n = text:gsub('\n', '') return n + 1 end

local function maxlinelen(text)
  local m = 1
  for line in (text .. '\n'):gmatch('([^\n]*)\n') do m = math.max(m, utf8.len(line) or #line) end
  return m
end

-- --------------------------------------------------------------- pass 1: metadata
local function Meta(m)
  stem = pandoc.utils.stringify(m.stem or '')
  for s in pandoc.utils.stringify(m.buildset or ''):gmatch('[^,]+') do buildset[s] = true end
end

-- --------------------------------------------------------------- tables
-- Column widths as fractions of the text width: proportional to each column's longest
-- cell (capped), never narrower than its longest word. Measured before inline code
-- is rewritten (stringify ignores raw LaTeX).
local CHAR_PT = 4.5   -- average advance at table size (serif 9 pt / mono 7.6 pt)
local function measure_table(tbl)
  local ncols = #tbl.colspecs
  local maxlen, maxword = {}, {}
  for c = 1, ncols do maxlen[c] = 3; maxword[c] = 3 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for c, cell in ipairs(row.cells) do
        if c <= ncols then
          local text = pandoc.utils.stringify(cell.contents)
          maxlen[c] = math.max(maxlen[c], utf8.len(text) or #text)
          for w in text:gmatch('%S+') do maxword[c] = math.max(maxword[c], utf8.len(w) or #w) end
        end
      end
    end
  end
  scan(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end
  local minshare, want, sum = {}, {}, 0
  for c = 1, ncols do
    minshare[c] = (math.min(maxword[c], 18) * CHAR_PT + 8) / TEXT_WIDTH
    want[c] = math.min(maxlen[c], 60) + 4
    sum = sum + want[c]
  end
  -- distribute: columns that fall below their minimum get it; the rest share what is left
  local share, fixed = {}, {}
  for _ = 1, ncols do
    local free_total, fixed_total = 0, 0
    for c = 1, ncols do
      if fixed[c] then fixed_total = fixed_total + minshare[c] else free_total = free_total + want[c] end
    end
    local changed = false
    for c = 1, ncols do
      if not fixed[c] then
        share[c] = want[c] / free_total * (1 - fixed_total)
        if share[c] < minshare[c] then fixed[c] = true; changed = true end
      else
        share[c] = minshare[c]
      end
    end
    if not changed then break end
  end
  local widths = {}
  for c = 1, ncols do widths[c] = share[c] end
  return widths
end

local function Table(tbl)
  if #tbl.colspecs == 0 then return nil end
  local widths = measure_table(tbl)
  for c = 1, #tbl.colspecs do tbl.colspecs[c] = { tbl.colspecs[c][1], widths[c] } end
  return tbl
end

local ALIGN = { AlignRight = '\\raggedleft', AlignCenter = '\\centering' }

local function render_table(tbl)
  local ncols = #tbl.colspecs
  local cols = {}
  for c = 1, ncols do
    local f = tbl.colspecs[c][2]
    if type(f) ~= 'number' then f = 1 / ncols end
    -- full width including the outer padding: f * (\linewidth + 2\tabcolsep) - 2\tabcolsep
    local align = ALIGN[tostring(tbl.colspecs[c][1])] or '\\raggedright'
    cols[c] = string.format('>{%s\\arraybackslash}p{\\dimexpr %.4f\\linewidth-%.4f\\tabcolsep\\relax}',
      align, f, 2 - 2 * f)
  end
  local function row_tex(row, head)
    local cells = {}
    for c, cell in ipairs(row.cells) do
      if c <= ncols then
        local t = blocks_latex(cell.contents):gsub('\n\n+', '\\par ')
        cells[#cells + 1] = head and ('\\thead{' .. t .. '}') or t
      end
    end
    while #cells < ncols do cells[#cells + 1] = '' end
    return table.concat(cells, ' & ') .. ' \\\\'
  end
  local head = {}
  for _, row in ipairs(tbl.head.rows) do head[#head + 1] = '\\rowcolor{tablehead}' .. row_tex(row, true) end
  local headtex = table.concat(head, '\n')
  local out = { '\\begin{booktable}', '\\begin{longtable}{' .. table.concat(cols) .. '}' }
  if #head > 0 then
    out[#out + 1] = '\\tabletop\n' .. headtex .. '\n\\tablemid\n\\endfirsthead'
    out[#out + 1] = '\\tabletop\n' .. headtex .. '\n\\tablemid\n\\endhead'
  else
    out[#out + 1] = '\\tabletop\n\\endfirsthead\n\\tabletop\n\\endhead'
  end
  out[#out + 1] = '\\tablebottom\n\\endlastfoot'
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do out[#out + 1] = row_tex(row, false) end
  end
  out[#out + 1] = '\\end{longtable}'
  local cap = tbl.caption and tbl.caption.long and #tbl.caption.long > 0
  if cap then
    out[#out + 1] = '{\\small\\itshape ' .. blocks_latex(tbl.caption.long) .. '\\par}'
  end
  out[#out + 1] = '\\end{booktable}'
  return raw(table.concat(out, '\n'))
end

-- estimated height (in lines) of a table, to keep small ones on one page
local function table_lines(tbl)
  local ncols = math.max(#tbl.colspecs, 1)
  local lines = 2
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      local rl = 1
      for c, cell in ipairs(row.cells) do
        local f = type(tbl.colspecs[c] and tbl.colspecs[c][2]) == 'number' and tbl.colspecs[c][2] or 1 / ncols
        local chars = math.max(f * TEXT_WIDTH / CHAR_PT, 4)
        local n = utf8.len(pandoc.utils.stringify(cell.contents)) or 0
        rl = math.max(rl, math.ceil(n / chars))
      end
      lines = lines + math.min(rl, 6) * 0.95
    end
  end
  return math.ceil(lines)
end

-- --------------------------------------------------------------- pass 2: inlines and blocks
local function Link(el)
  local t = el.target
  if t:match('^mailto:') then return el.content end
  if t:match('^%a[%w+.-]*:') then return el end           -- http:, https:, …
  local file, frag = t:match('^([^#]*)#?(.*)$')
  local target_stem
  if file == '' then
    target_stem = stem
  else
    target_stem = file:match('([^/]+)%.md$')
    if not target_stem or not buildset[target_stem] then
      warn('link to a file outside the book, kept as text: ' .. t)
      return el.content
    end
  end
  return rawi('\\hyperref[' .. label_for(target_stem, frag) .. ']{' .. to_latex(el.content) .. '}')
end

local function RawInline(el)
  if el.format == 'html' then
    if el.text:match('^<br%s*/?>$') then return rawi('\\newline{}') end
    return {}
  end
end

local function RawBlock(el)
  if el.format == 'html' then return {} end
end

-- makeindex needs " @ ! | quoted with "
local function idx_quote(s) return (s:gsub('(["@!|])', '"%1')) end

-- [text]{.idx}  [text]{idx="key"}  []{idx="key"}   (key may use makeindex's "a!b" for sub-entries)
local function Span(el)
  local key = el.attributes['idx']
  local has_class = el.classes:includes('idx')
  if el.classes:includes('noindex') then return el.content end
  if not key and not has_class then return nil end
  local entry
  if key and key ~= '' then
    entry = esc(key):gsub('\\textbar{}', '|')      -- the author's key is used as written
  else
    local plain = pandoc.utils.stringify(el.content)
    local display = to_latex(el.content)
    local sortkey = idx_quote(plain)
    if display ~= esc(plain) then
      entry = sortkey .. '@' .. idx_quote(display)
    else
      entry = idx_quote(display)
    end
  end
  local out = pandoc.List(el.content)
  out:insert(rawi('\\index{' .. entry .. '}'))
  return out
end

-- Long inline code may break after / , = & ? (and . _ - : when very long) so it never
-- runs into the margin. Short identifiers never break.
local function Code(el)
  local len = utf8.len(el.text) or #el.text
  if len < 18 then return nil end
  local breakers = len >= 24 and '^[/,=&%?%._%-:]$' or '^[/,=&%?]$'
  if not el.text:find('[/,=&%?]') and len < 24 then return nil end
  local parts, buf = {}, ''
  for ch in el.text:gmatch(utf8.charpattern) do
    buf = buf .. ch
    if ch:match(breakers) then parts[#parts + 1] = buf; buf = '' end
  end
  if buf ~= '' then parts[#parts + 1] = buf end
  local out = {}
  for _, p in ipairs(parts) do out[#out + 1] = to_latex({ pandoc.Code(p) }) end
  return rawi(table.concat(out, '\\allowbreak{}'))
end

local SHELL = { bash = true, sh = true, shell = true, zsh = true, console = true }

-- Lines wrap at spaces and after / . , = ? : & _ - (see \fvset in preamble.tex). A run of
-- characters with none of those that is longer than a line (a token, a hash, base64)
-- could not wrap: such blocks also allow a break anywhere, as a last resort.
local LINE_CHARS = math.floor((TEXT_WIDTH - CODE_INDENT) / (MONO_ADVANCE * MONO_SCALE * CODE_SIZE)) - 4
local function needs_breakanywhere(text)
  for run in text:gmatch('[^%s/%.,=%?:&_%-]+') do
    if (utf8.len(run) or #run) > LINE_CHARS then return true end
  end
  return false
end

local function CodeBlock(el)
  local text = el.text:gsub('%s+$', '')
  el.text = text
  local lang = el.classes[1]
  local n = nlines(text)
  local need = '\\codeneed{' .. math.min(n, SHORT_BLOCK < n and 4 or n) .. '}'

  if not lang or lang == 'text' or lang == 'output' or lang == 'plain' then
    local is_diagram = false
    for _, c in ipairs(BOX_CHARS) do
      if text:find(c, 1, true) then is_diagram = true break end
    end
    if is_diagram then
      -- never wrapped: pick the largest size (up to the code size) at which it fits
      local maxlen = maxlinelen(text)
      local avail = TEXT_WIDTH - CODE_INDENT - 2
      local size = math.min(CODE_SIZE, avail / (MONO_ADVANCE * MONO_SCALE * maxlen))
      size = math.floor(size * 10) / 10
      if size * MONO_SCALE < 5 then
        warn(string.format('diagram is %d characters wide; it prints below 5 pt. Narrow it.', maxlen))
      end
      -- DejaVu Sans Mono's box glyphs are 1.165 em tall: a line skip just under that makes
      -- vertical strokes overlap, so corners and bars join without gaps
      local skip = string.format('%.2f', size * MONO_SCALE * 1.16)
      return raw('\\codeneed{' .. math.min(n, 30) .. '}\\begin{codeblock}\n' ..
        '\\begin{Verbatim}[breaklines=false, fontsize=\\fontsize{' .. size .. '}{' .. skip .. '}\\selectfont, fontfamily=diagrammono, formatcom=\\diagramlines]\n' ..
        text .. '\n\\end{Verbatim}\n\\end{codeblock}')
    end
    local opt = needs_breakanywhere(text) and ', breakanywhere, breakanywheresymbolpre={}' or ''
    return raw(need .. '\\begin{codeblock}\n\\begin{Verbatim}[formatcom=\\outputstyle' .. opt .. ']\n' ..
      text .. '\n\\end{Verbatim}\n\\end{codeblock}')
  end

  if SHELL[lang] then
    for line in (text .. '\n'):gmatch('([^\n]*)\n') do
      if line:match('^%$ ') or line:match('^> ') then
        warn('shell block line starts with a prompt ("$ " or "> "); the book shows commands without one: ' .. line)
        break
      end
    end
    if lang == 'console' or lang == 'zsh' then el.classes[1] = 'bash' end
  end
  local opt = needs_breakanywhere(text) and '\\fvset{breakanywhere, breakanywheresymbolpre={}}' or ''
  return { raw(need .. '\\begin{codeblock}' .. opt), el, raw('\\end{codeblock}') }
end

-- A spaced em dash never starts a line: tie it to the word before it.
local function Inlines(inl)
  for i = 1, #inl - 1 do
    if inl[i].t == 'Space' and inl[i + 1].t == 'Str' and inl[i + 1].text:match('^—') then
      inl[i] = pandoc.Str('\u{00A0}')
    end
  end
  return inl
end

-- callout label at the start of a quote: "**Tip:**", "**Tip**:", "**Note.**" …
local CALLOUT = { tip = 'tip', note = 'note', warning = 'warning', important = 'note',
  caution = 'warning', danger = 'warning' }

local function callout_kind(para)
  if not para or (para.t ~= 'Para' and para.t ~= 'Plain') then return nil end
  local first = para.content[1]
  if not first or first.t ~= 'Strong' then return nil end
  local label = pandoc.utils.stringify(first)
  local word = label:lower():match('^(%a+)[:.]?$')
  local kind = word and CALLOUT[word]
  if kind then
    -- drop the label, the ":" that may follow it outside the bold, and the space
    para.content:remove(1)
    if para.content[1] and para.content[1].t == 'Str' and para.content[1].text:match('^[:.]$') then
      para.content:remove(1)
    end
    if para.content[1] and para.content[1].t == 'Space' then para.content:remove(1) end
    return kind
  end
  if label:lower():match('^you understand this') then return 'understand' end
  return nil
end

local function wrap_callout(kind, blocks)
  local out = pandoc.List()
  if kind == 'understand' then
    out:insert(raw('\\begin{understandbox}'))
    out:extend(blocks)
    out:insert(raw('\\end{understandbox}'))
  else
    out:insert(raw('\\begin{callout}{' .. kind .. '}'))
    out:extend(blocks)
    out:insert(raw('\\end{callout}'))
  end
  return out
end

local function BlockQuote(el)
  local kind = callout_kind(el.content[1])
  if kind then return wrap_callout(kind, el.content) end
  local out = pandoc.List({ raw('\\begin{quote}') })
  out:extend(el.content)
  out:insert(raw('\\end{quote}'))
  return out
end

-- GitHub alerts: > [!TIP] …  (pandoc: Div.tip with a Div.title first)
local function Div(el)
  for _, c in ipairs(el.classes) do
    local kind = CALLOUT[c]
    if kind then
      local blocks = pandoc.List()
      for _, b in ipairs(el.content) do
        if not (b.t == 'Div' and b.classes:includes('title')) then blocks:insert(b) end
      end
      return wrap_callout(kind, blocks)
    end
  end
end

-- Definition lists (Key Terms, Glossary): "Term: definition" paragraphs
local function sort_key(s) return (s:lower():gsub('^[^%w]+', '')) end
local function DefinitionList(el)
  local items = {}
  for _, item in ipairs(el.content) do
    local term, defs = item[1], item[2]
    local parts = {}
    for _, d in ipairs(defs) do parts[#parts + 1] = blocks_latex(d):gsub('\n\n+', '\\par ') end
    items[#items + 1] = { key = sort_key(pandoc.utils.stringify(term)),
      tex = '\\glossentry{' .. to_latex(term) .. '}{' .. table.concat(parts, '\\par ') .. '}' }
  end
  if is_glossary then table.sort(items, function(a, b) return a.key < b.key end) end
  local out = { '\\begin{glossarylist}' }
  for _, it in ipairs(items) do out[#out + 1] = it.tex end
  out[#out + 1] = '\\end{glossarylist}'
  return raw(table.concat(out, '\n'))
end

local function Figure(fig)
  -- pandoc's own figure output, kept; only warn when the image file is missing
  fig:walk({ Image = function(img)
    local f = io.open('../markdown/' .. img.src, 'r') or io.open(img.src, 'r')
    if f then f:close() else warn('image not found (relative to the markdown folder): ' .. img.src) end
  end })
end

-- --------------------------------------------------------------- pass 0: bold terms -> index
-- Every **bold term** (up to four words, not ending in ":" "." "!" "?") in a chapter is a
-- new term: it gets an index entry automatically. Not in the Preface, the Glossary, headings,
-- definition lists, or the closing "Summary, Key Terms, and Review Questions" section.
-- Opt out: [**not a term**]{.noindex}. Choose the entry: [**APIs**]{idx="API"}.
local function idx_quote_early(s) return (s:gsub('(["@!|])', '"%1')) end

-- Words the chapter uses in lower case: a bold term that starts a sentence ("**Staging** is ...")
-- is indexed in lower case when its first word appears in lower case elsewhere in the chapter.
-- Names (Docker, Kubernetes) never do, and mixed-case words (DevOps, GitHub) are left alone.
local lower_words = {}

local function index_strong(st)
  local text = pandoc.utils.stringify(st.content):gsub('^%s+', ''):gsub('%s+$', '')
  local shown = st.content
  local first = text:match('^(%u%l+)%f[^%a]')
  if first and lower_words[first:lower()] and st.content[1] and st.content[1].t == 'Str' then
    shown = st.content:clone()
    shown[1] = pandoc.Str(shown[1].text:sub(1, 1):lower() .. shown[1].text:sub(2))
    text = text:sub(1, 1):lower() .. text:sub(2)
  end
  if text == '' or text:match('[:.!?]$') then return nil end
  local _, words = text:gsub('%S+', '')
  if words > 4 then return nil end
  local low = text:lower()
  if low:match('^you understand') or low:match('^tip') or low:match('^note') or low:match('^warning') then
    return nil
  end
  local display = pandoc.write(pandoc.Pandoc({ pandoc.Plain(shown) }), 'latex'):gsub('%s+$', '')
  local plain = pandoc.write(pandoc.Pandoc({ pandoc.Plain({ pandoc.Str(text) }) }), 'latex'):gsub('%s+$', '')
  local entry
  if display == plain and low == text then
    entry = idx_quote_early(display)
  else
    entry = idx_quote_early(low) .. '@' .. idx_quote_early(display)
  end
  return { st, pandoc.RawInline('latex', '\\index{' .. entry .. '}') }
end

local function autoindex(doc)
  local title = ''
  for _, b in ipairs(doc.blocks) do
    if b.t == 'Header' and b.level == 1 then title = pandoc.utils.stringify(b.content):lower() break end
  end
  if title == 'preface' or title == 'glossary' then return nil end
  lower_words = {}
  doc:walk({ Str = function(s) local w = s.text:match('^(%l+)') if w then lower_words[w] = true end end })
  local protect = { Span = function(sp)
    if sp.attributes['idx'] or sp.classes:includes('idx') or sp.classes:includes('noindex') then
      sp.content = sp.content:walk({ Strong = function(st) return pandoc.Span(st.content, { class = '_strong' }) end })
      return sp
    end
  end }
  local restore = { Span = function(sp)
    if sp.classes:includes('_strong') then return pandoc.Strong(sp.content) end
  end }
  local in_summary = false
  for i, b in ipairs(doc.blocks) do
    if b.t == 'Header' then
      if b.level <= 2 then in_summary = pandoc.utils.stringify(b.content):lower():match('^summary') ~= nil end
    elseif not in_summary and b.t ~= 'DefinitionList' then
      doc.blocks[i] = b:walk(protect):walk({ Strong = index_strong }):walk(restore)
    end
  end
  return doc
end

-- --------------------------------------------------------------- pass 3: structure
local function is_blank_para(b)
  if b.t ~= 'Para' and b.t ~= 'Plain' then return false end
  local has_raw = false
  b:walk({ RawInline = function() has_raw = true end, Code = function() has_raw = true end,
    Image = function() has_raw = true end })
  if has_raw then return false end
  local s = pandoc.utils.stringify(b):gsub('\u{00A0}', ''):gsub('%s', '')
  return s == ''
end

-- "Chapter 3: Title" / "Appendix B — Title" / "3. Title" -> "Title" (numbers come from LaTeX)
local function strip_number(title)
  local t = title:gsub('^Chapter%s+%d+%s*[:%.—%-]+%s*', '')
  t = t:gsub('^Appendix%s+%a%s*[:%.—%-]+%s*', '')
  t = t:gsub('^%d+%.%s+', '')
  return t
end

local function is_heading(b)
  return b ~= nil and b.t == 'RawBlock' and (b.text:match('^\\%a*section') or b.text:match('^\\paragraph')) ~= nil
end

local function Pandoc(doc)
  -- the glossary is known from its title; its definition lists are sorted A–Z
  for _, b in ipairs(doc.blocks) do
    if b.t == 'Header' and b.level == 1 then
      is_glossary = strip_number(pandoc.utils.stringify(b.content)):lower() == 'glossary'
      break
    end
  end
  -- second walk for blocks that depend on is_glossary
  doc = doc:walk({ DefinitionList = DefinitionList })

  local out, blocks = pandoc.List(), doc.blocks
  -- A command followed directly by its output is one unit: the first block's \codeneed
  -- reserves room for both, so they never split across a page break.
  for i = #blocks, 1, -1 do
    local b = blocks[i]
    if b.t == 'RawBlock' and b.text:match('^\\codeneed{%d+}') then
      local k = i
      while blocks[k] and not (blocks[k].t == 'RawBlock' and blocks[k].text:match('\\end{codeblock}')) do k = k + 1 end
      local nxt = blocks[k + 1]
      if nxt and nxt.t == 'RawBlock' and nxt.text:match('^\\codeneed{%d+}') then
        local n1 = tonumber(b.text:match('^\\codeneed{(%d+)}'))
        local n2 = tonumber(nxt.text:match('^\\codeneed{(%d+)}'))
        local n = math.min(n1 + n2 + 1, 30)
        b.text = b.text:gsub('^\\codeneed{%d+}', '\\codeneed{' .. n .. '}')
      end
    end
  end
  local h1_seen, intro_done, section_seen = false, false, false
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    if b.t == 'HorizontalRule' or is_blank_para(b) then
      -- drop
    elseif b.t == 'Header' and b.level == 1 then
      if h1_seen then warn('a second "# " heading: one Markdown file = one chapter') end
      h1_seen = true
      local title = strip_number(pandoc.utils.stringify(b.content))
      local tex = (title == pandoc.utils.stringify(b.content)) and heading_text(b.content) or esc(title)
      out:insert(raw('\\bookchapter{' .. tex .. '}{' .. label_for(stem, nil) .. '}'))
    elseif b.t == 'Header' then
      section_seen = true
      local label = label_for(stem, b.identifier)
      local cmd = ({ [2] = 'section', [3] = 'subsection*', [4] = 'subsubsection*' })[b.level] or 'paragraph*'
      out:insert(raw('\\' .. cmd .. '{' .. heading_text(b.content) .. '}\\label{' .. label .. '}'))
    elseif b.t == 'Para' and h1_seen and not section_seen and not intro_done then
      intro_done = true
      out:insert(raw('\\begin{chapterintro}'))
      out:insert(b)
      out:insert(raw('\\end{chapterintro}'))
    elseif b.t == 'RawBlock' and b.text:match('^\\tableneed') then
      -- keep a small table with the heading or the short line that introduces it
      local need = tonumber(b.text:match('{(%d+)}'))
      local prev = out[#out]
      if need <= 30 then
        if is_heading(prev) or (prev and prev.t == 'Para' and (utf8.len(pandoc.utils.stringify(prev)) or 0) < 160) then
          local at, n = #out, need + 3
          if not is_heading(prev) and is_heading(out[at - 1]) then at = at - 1; n = n + 3 end
          out:insert(at, raw('\\Needspace{' .. n .. '\\baselineskip}'))
        else
          out:insert(raw('\\Needspace{' .. need .. '\\baselineskip}'))
        end
      end
    elseif b.t == 'RawBlock' and b.text:match('^\\codeneed') then
      -- a short line ending in ":" that introduces a code block moves with it
      local prev = out[#out]
      if prev and prev.t == 'Para' and pandoc.utils.stringify(prev):match(':%s*$')
          and (utf8.len(pandoc.utils.stringify(prev)) or 0) < 200 then
        local n = tonumber(b.text:match('^\\codeneed{(%d+)}')) + 3
        local at = #out
        if is_heading(out[at - 1]) then at = at - 1; n = n + 3 end   -- …and so does its heading
        out:insert(at, raw('\\codeneed{' .. n .. '}'))
      end
      out:insert(b)
    else
      out:insert(b)
    end
    i = i + 1
  end
  if not h1_seen then warn('no "# Title" heading: every Markdown file must start with one') end
  doc.blocks = out
  return doc
end

return {
  { Pandoc = autoindex },
  { Meta = Meta, Table = Table },            -- tables measured before inline code is rewritten
  { Inlines = Inlines },
  { Link = Link, RawInline = RawInline, RawBlock = RawBlock, Span = Span, Code = Code,
    CodeBlock = CodeBlock, BlockQuote = BlockQuote, Div = Div, Figure = Figure },
  { Table = function(t) return { raw('\\tableneed{' .. (table_lines(t) + 2) .. '}'), render_table(t) } end },
  { Pandoc = Pandoc },
}
