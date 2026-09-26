--[[
filter.lua — turns one library Markdown file into a book chapter.

Metadata (passed with -M by convert.sh):
  stem      file stem, used to namespace labels            (e.g. 01-command-to-process)
  numbered  "true" for chapters of The Book (keep their Chapter N / N.M numbers)
  buildset  comma-separated stems included in this build (for cross-file links)

What it does:
  * H1 -> \chapter (numbered) or \unnumberedchapter; "Chapter N — A: B" -> title A, subtitle B
  * H3 right after H1 -> chapter subtitle
  * "N.M Title" sections keep their number; other sections are un-numbered
  * drops the Markdown "Table of Contents" section and horizontal rules
  * "By the end of this chapter…" + list -> objectives box; "Key Takeaways" -> takeaways box
  * blockquotes -> note boxes
  * code: language -> codebox (with "# Listing X.Y — …" lifted into a caption);
          box-drawing text -> diagrambox (font sized to fit); other plain text -> outputbox
  * links to other chapters -> \hyperref; links to chapters not in the build -> plain text

Modes (-M mode=…):
  chapter   (default) one Markdown file = one chapter
  split     the file's H1 is dropped and each H2 becomes a chapter ("Part I — X" -> "X");
            text before the first H2 opens the first chapter
  appendix  the file's H1 is dropped and each H2 ("Appendix A — …") becomes a chapter
  intro     headings shift down one level under a chapter titled by -M chaptertitle=…
]]

local stem, numbered, buildset = '', false, {}
local mode, chaptertitle = 'chapter', nil

local BOX_CHARS = { '┌', '┐', '└', '┘', '│', '├', '┤', '┬', '┴', '┼', '─', '━', '▶', '▼', '╭', '╮', '╯', '╰' }

-- ---------------------------------------------------------------- helpers
local function raw(s) return pandoc.RawBlock('latex', s) end

local function to_latex(inlines)
  local s = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'latex')
  return (s:gsub('%s+$', ''))
end

local function esc(text) return to_latex({ pandoc.Str(text) }) end

-- title usable both in the page and in PDF bookmarks
local function heading_text(inlines)
  local tex = to_latex(inlines)
  local plain = esc(pandoc.utils.stringify(inlines))
  if tex == plain then return tex end
  return '\\texorpdfstring{' .. tex .. '}{' .. plain .. '}'
end

local function clean_label(s) return (s:gsub('_', '-'):gsub('[^%w%-:%.]', '')) end
local function label_for(file_stem, frag)
  -- "#appendix-e--…" lands on that appendix (each one is a chapter with a numbered label)
  local letter = file_stem == '44-appendices' and frag and frag:match('^appendix%-(%a)%-%-')
  if letter then
    local n = letter:lower():byte() - ('a'):byte() + 1
    return clean_label('ch:' .. file_stem .. (n > 1 and ('-' .. n) or ''))
  end
  if frag and frag ~= '' then return clean_label(file_stem .. ':' .. frag) end
  return clean_label('ch:' .. file_stem)
end

local function is_blank_para(b)
  if b.t ~= 'Para' and b.t ~= 'Plain' then return false end
  -- Inline code and cross-references are already RawInline here, and stringify() ignores
  -- RawInline — so a paragraph that is only code or a link must not count as blank.
  local has_raw = false
  b:walk({ RawInline = function() has_raw = true end })
  if has_raw then return false end
  local s = pandoc.utils.stringify(b):gsub('\u{00A0}', ''):gsub('%s', '')
  return s == ''
end

-- --------------------------------------------------------------- pass 1
local function Meta(m)
  stem = pandoc.utils.stringify(m.stem or '')
  numbered = pandoc.utils.stringify(m.numbered or '') == 'true'
  mode = pandoc.utils.stringify(m.mode or 'chapter')
  if m.chaptertitle then chaptertitle = pandoc.utils.stringify(m.chaptertitle) end
  for s in pandoc.utils.stringify(m.buildset or ''):gmatch('[^,]+') do buildset[s] = true end
end

-- --------------------------------------------------------------- pass 2
local function nlines(text) local _, n = text:gsub('\n', '') return n + 1 end
local SHORT_CODE, SHORT_DIAGRAM = 18, 45   -- boxes up to this many lines never split across pages

local function Link(el)
  local t = el.target
  if t:match('^mailto:') then return el.content end          -- e-mail autolinks: plain text
  if t:match('^%a[%w+.-]*:') then return el end            -- http:, …
  local file, frag = t:match('^([^#]*)#?(.*)$')
  local target_stem
  if file == '' then
    target_stem = stem
  else
    target_stem = file:match('([^/]+)%.md$')
    if not target_stem or not buildset[target_stem] then
      return el.content                                    -- not in this build: keep the words only
    end
  end
  return pandoc.RawInline('latex',
    '\\hyperref[' .. label_for(target_stem, frag) .. ']{' .. to_latex(el.content) .. '}')
end

local function RawInline(el)
  if el.format == 'html' then
    if el.text:match('^<br%s*/?>$') then return pandoc.RawInline('latex', '\\newline{}') end
    return {}
  end
end

local function RawBlock(el)
  if el.format == 'html' then return {} end
end

local function CodeBlock(el)
  local text = el.text
  local lang = el.classes[1]

  -- Plain text with box-drawing characters = a diagram
  if not lang then
    local is_diagram = false
    for _, c in ipairs(BOX_CHARS) do
      if text:find(c, 1, true) then is_diagram = true break end
    end
    if is_diagram then
      local maxlen = 1
      for line in (text .. '\n'):gmatch('([^\n]*)\n') do
        maxlen = math.max(maxlen, utf8.len(line) or #line)
      end
      -- Menlo @ Scale 0.85: advance = 0.512 × size. Available width ≈ 392pt.
      local size = math.min(9, 392 / (0.512 * maxlen))
      size = math.max(4.8, math.floor(size * 10) / 10)
      -- Menlo's box-drawing glyphs are 0.99 × size tall (at Scale 0.85); a slightly smaller
      -- line skip makes vertical strokes overlap, so box corners and bars join without gaps.
      local skip = string.format('%.2f', size * 0.95)
      local width = string.format('%.1fpt', maxlen * 0.512 * size + 13)
      local opt = nlines(text) <= SHORT_DIAGRAM and '[short]' or ''
      return raw('\\begin{diagrambox}' .. opt .. '{' .. width .. '}\n\\begin{Verbatim}[fontsize=\\fontsize{' ..
        size .. '}{' .. skip .. '}\\selectfont]\n' .. text ..
        '\n\\end{Verbatim}\n\\end{diagrambox}')
    end
    local opt = nlines(text) <= SHORT_CODE and '[short]' or ''
    return raw('\\begin{outputbox}' .. opt .. '\n\\begin{Verbatim}[fontsize=\\codesize, breaklines, breakanywhere,' ..
      ' breaksymbolleft={\\tiny\\textcolor{muted}{$\\hookrightarrow$}}]\n' .. text ..
      '\n\\end{Verbatim}\n\\end{outputbox}')
  end

  -- Source code: lift a leading "# Listing X.Y — Title" comment into the caption
  local caption = ''
  local first, rest = text:match('^([^\n]*)\n?(.*)$')
  local num, title = first:match('^%s*#%s*Listing%s+([%d%.]+)%s*(.*)$')
  if num then
    title = title:gsub('^—%s*', ''):gsub('^[-:]+%s*', '')
    caption = '\\textcolor{accent}{Listing ' .. num .. '}\\enspace ' .. esc(title)
    el.text = rest
  end
  -- (long unbroken runs wrap inside highlighting groups: Highlighting uses breaknonspaceingroup)
  local opt = nlines(el.text) <= SHORT_CODE and '[short]' or ''
  if caption == '' then
    return { raw('\\begin{codebox}' .. opt), el, raw('\\end{codebox}') }
  end
  return { raw('\\begin{codeboxcap}' .. opt .. '{' .. caption .. '}'), el, raw('\\end{codeboxcap}') }
end

-- Long inline code may break so it never runs into the margin. Short identifiers
-- (sys.getrecursionlimit(), __pycache__/, app.py) never break; long ones break after
-- "/" "," "=" "&" "?" first, and after "." "_" "-" ":" only when they are very long.
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
  return pandoc.RawInline('latex', table.concat(out, '\\allowbreak{}'))
end

-- Wide tables: size columns from their content so they wrap inside the text block
local function Table(tbl)
  local ncols = #tbl.colspecs
  if ncols == 0 then return nil end
  local maxlen, maxword = {}, {}
  for c = 1, ncols do maxlen[c] = 3; maxword[c] = 1 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for c, cell in ipairs(row.cells) do
        if c <= ncols then
          local text = pandoc.utils.stringify(cell.contents)
          local n = utf8.len(text) or 0
          if n > maxlen[c] then maxlen[c] = n end
          for w in text:gmatch('%S+') do
            maxword[c] = math.max(maxword[c], utf8.len(w) or #w)
          end
        end
      end
    end
  end
  scan(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end
  local total = 0
  for c = 1, ncols do total = total + maxlen[c] end
  if total + 3 * ncols <= 78 then return nil end          -- fits naturally: leave as is
  local capped, sum = {}, 0
  for c = 1, ncols do capped[c] = math.min(maxlen[c], 48) + 4; sum = sum + capped[c] end
  -- Column share, but never narrower than its longest word. Budget: ~350pt of text width,
  -- ~5.2pt per monospace character at table size (the widest case: inline code).
  -- Longer words (URLs, dotted paths) can break, so the minimum is capped at 14 characters.
  local share, fixed, free = {}, 0, 0
  for c = 1, ncols do
    local minshare = (math.min(maxword[c], 14) * 5.2 + 6) / 350
    share[c] = math.max(capped[c] / sum, minshare)
    if share[c] == minshare then fixed = fixed + minshare else free = free + share[c] end
  end
  for c = 1, ncols do
    local w = share[c]
    if w ~= (math.min(maxword[c], 14) * 5.2 + 6) / 350 and free > 0 then w = w * (1 - fixed) / free end
    tbl.colspecs[c] = { tbl.colspecs[c][1], w }
  end
  return tbl
end

-- A spaced em dash never starts a line: tie it to the word before it.
local function Inlines(inl)
  for i = 1, #inl - 1 do
    if inl[i].t == 'Space' and inl[i + 1].t == 'Str' and inl[i + 1].text:match('^—') then
      inl[i] = pandoc.Str('\u{00A0}')   -- no-break space (stringify keeps it; LaTeX gets ~)
    end
  end
  return inl
end

-- "**Warning:** …" / "**CRITICAL:** …" paragraphs become warning boxes;
-- "→ Chapter N …" navigation lines are never indented.
local function Para(el)
  local first = el.content[1]
  if first and first.t == 'Strong' then
    local w = pandoc.utils.stringify(first):lower()
    if w:match('^warning') or w:match('^critical') then
      return { raw('\\begin{warnbox}'), el, raw('\\end{warnbox}') }
    end
  end
  if first and first.t == 'Str' and first.text:match('^→') then
    el.content:insert(1, pandoc.RawInline('latex', '\\noindent{}'))
    return el
  end
end

local function BlockQuote(el)
  -- A quote that opens with a "**Warning:**" paragraph (already a warnbox, see Para)
  -- becomes one warning box as a whole, instead of a warning box inside a note box
  local c = el.content
  if c[3] and c[1].t == 'RawBlock' and c[1].text == '\\begin{warnbox}'
      and c[3].t == 'RawBlock' and c[3].text == '\\end{warnbox}' then
    local blocks = { raw('\\begin{warnbox}'), c[2] }
    for i = 4, #c do blocks[#blocks + 1] = c[i] end
    blocks[#blocks + 1] = raw('\\end{warnbox}')
    return blocks
  end
  local blocks = { raw('\\begin{notebox}') }
  for _, b in ipairs(el.content) do blocks[#blocks + 1] = b end
  blocks[#blocks + 1] = raw('\\end{notebox}')
  return blocks
end

-- --------------------------------------------------------------- pass 3: structure
local function strip_section_number(inlines)
  local first = inlines[1]
  if first and first.t == 'Str' then
    local a, b = first.text:match('^(%d+)%.(%d+)$')
    if a then
      local out = pandoc.List()
      for i = 3, #inlines do out:insert(inlines[i]) end   -- drop "N.M" + following space
      return out, tonumber(b)
    end
  end
  return inlines, nil
end

local function normalise(blocks)
  if mode == 'intro' and chaptertitle then
    for _, b in ipairs(blocks) do
      if b.t == 'Header' then b.level = b.level + 1 end
    end
    blocks:insert(1, pandoc.Header(1, pandoc.Inlines(chaptertitle)))
    return blocks
  end
  if mode ~= 'split' and mode ~= 'appendix' then return blocks end
  local pre, rest, seen_first = pandoc.List(), pandoc.List(), false
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    if b.t == 'Header' and b.level == 1 then
      -- drop the document title and an H3 subtitle right under it
      if blocks[i + 1] and blocks[i + 1].t == 'Header' and blocks[i + 1].level == 3 then i = i + 1 end
    else
      if b.t == 'Header' then
        b.level = b.level - 1
        if b.level == 1 then
          seen_first = true
          if mode == 'split' then
            local t = pandoc.utils.stringify(b.content):gsub('^Part%s+[IVX]+%s*—%s*', '')
            b.content = pandoc.Inlines(t)
          end
          rest:insert(b)
          if #pre > 0 then rest:extend(pre); pre = pandoc.List() end
          goto continue
        end
      end
      if seen_first then rest:insert(b) else pre:insert(b) end
    end
    ::continue::
    i = i + 1
  end
  rest:extend(pre)
  return rest
end

local function is_back_link(b)
  return (b.t == 'Para' or b.t == 'Plain') and pandoc.utils.stringify(b):match('^↑ Back to') ~= nil
end

local function Pandoc(doc)
  -- Headings keep ordinary spaces: their titles are parsed as text below
  -- ("Chapter 21 — …", "Appendix A — …"), and Lua's %s does not match a no-break space
  doc.blocks = doc.blocks:walk({ Header = function(h)
    h.content = h.content:walk({ Str = function(s)
      if s.text == '\u{00A0}' then return pandoc.Space() end
    end })
    return h
  end })
  local blocks, out = normalise(doc.blocks), pandoc.List()
  local i, seen_section, skipping, open_box = 1, false, false, nil
  local h1_count = 0

  local function close_box()
    if open_box then out:insert(raw('\\end{' .. open_box .. '}')); open_box = nil end
  end

  while i <= #blocks do
    local b = blocks[i]

    if b.t == 'Header' and b.level <= 2 then
      skipping = false
      close_box()
    end

    if skipping then
      -- inside the Markdown TOC section: drop until the next heading
    elseif b.t == 'HorizontalRule' or is_blank_para(b) or is_back_link(b) then
      -- drop
    elseif b.t == 'Header' and b.level == 1 then
      local title = pandoc.utils.stringify(b.content)
      local label = label_for(stem, nil)
      -- A file with several H1s (the appendices): later ones get unique labels;
      -- links to the file land on the first
      h1_count = h1_count + 1
      if h1_count > 1 then label = label .. '-' .. h1_count end
      local subtitle
      local n, rest = title:match('^Chapter%s+(%d+)%s*—%s*(.*)$')
      -- H3 immediately after H1 is a subtitle
      if blocks[i + 1] and blocks[i + 1].t == 'Header' and blocks[i + 1].level == 3 then
        subtitle = to_latex(blocks[i + 1].content)
        i = i + 1
      end
      -- …or a one-paragraph blockquote right after H1 (already turned into a notebox)
      if not subtitle and blocks[i + 3] and blocks[i + 1].t == 'RawBlock'
          and blocks[i + 1].text == '\\begin{notebox}' and blocks[i + 2].t == 'Para'
          and blocks[i + 3].t == 'RawBlock' and blocks[i + 3].text == '\\end{notebox}' then
        subtitle = to_latex(blocks[i + 2].content)
        i = i + 3
      end
      if numbered and n then
        local main, sub = rest:match('^(.-):%s+(.*)$')
        main = main or rest
        subtitle = subtitle or (sub and esc(sub))
        out:insert(raw('\\setcounter{chapter}{' .. (tonumber(n) - 1) .. '}\n' ..
          '\\chapter{' .. esc(main) .. '}\\label{' .. label .. '}'))
      else
        out:insert(raw('\\unnumberedchapter{' .. esc(title) .. '}\\label{' .. label .. '}'))
      end
      if subtitle then out:insert(raw('\\chaptersubtitle{' .. subtitle .. '}')) end
      out:insert(raw('\\chapterrule'))
    elseif b.t == 'Header' and b.level == 2 then
      local title = pandoc.utils.stringify(b.content)
      local label = label_for(stem, b.identifier)
      if title:lower() == 'table of contents' then
        skipping = true
      elseif title:lower() == 'key takeaways' then
        out:insert(raw('\\phantomsection\\label{' .. label .. '}\n\\begin{takeaways}'))
        open_box = 'takeaways'
      else
        seen_section = true
        local content, secnum = strip_section_number(b.content)
        if numbered and secnum then
          out:insert(raw('\\setcounter{section}{' .. (secnum - 1) .. '}\n' ..
            '\\section{' .. heading_text(content) .. '}\\label{' .. label .. '}'))
        else
          out:insert(raw('\\unnumberedsection{' .. tostring(not numbered) .. '}{' ..
            heading_text(content) .. '}\\label{' .. label .. '}'))
        end
      end
    elseif b.t == 'Header' then
      local cmd = ({ [3] = 'subsection', [4] = 'subsubsection' })[b.level] or 'paragraph'
      out:insert(raw('\\' .. cmd .. '*{' .. heading_text(b.content) .. '}\\phantomsection\\label{' ..
        label_for(stem, b.identifier) .. '}'))
    elseif not seen_section and b.t == 'Para'
        and pandoc.utils.stringify(b):match('^By the end of this chapter')
        and blocks[i + 1] and blocks[i + 1].t == 'BulletList' then
      out:insert(raw('\\begin{objectives}'))
      out:insert(b)
      out:insert(blocks[i + 1])
      out:insert(raw('\\end{objectives}'))
      i = i + 1
    else
      -- Keep a table that fits on a page in one piece: reserve its estimated height
      -- (before its heading, when it directly follows one, so the heading moves with it).
      -- Without this, a longtable can break between its header row and its first row.
      if b.t == 'Table' then
        local ncols = math.max(#b.colspecs, 1)
        local width = 78 / ncols * 1.2          -- rough characters per column line
        local lines = 3                         -- header row and rules
        for _, body in ipairs(b.bodies) do
          for _, row in ipairs(body.body) do
            local rl = 1
            for _, cell in ipairs(row.cells) do
              local n = utf8.len(pandoc.utils.stringify(cell.contents)) or 0
              rl = math.max(rl, math.ceil(n / width))
            end
            lines = lines + math.min(rl, 5)
          end
        end
        local need = math.ceil(lines * 1.25) + 1
        if need <= 30 then
          local prev = out[#out]
          local at = #out + 1
          if prev and prev.t == 'RawBlock' and (prev.text:match('^\\%a*section')
              or prev.text:match('^\\setcounter{section}') or prev.text:match('^\\paragraph')) then
            at = #out
            need = need + 3
          end
          out:insert(at, raw('\\Needspace{' .. need .. '\\baselineskip}'))
        end
      end
      -- Text that continues after a list, listing or box is not indented.
      local prev = out[#out]
      if b.t == 'Para' and prev and (prev.t == 'BulletList' or prev.t == 'OrderedList'
          or (prev.t == 'RawBlock' and prev.text:match('\\end{%a+}%s*$'))) then
        b.content:insert(1, pandoc.RawInline('latex', '\\noindent{}'))
      end
      out:insert(b)
    end
    i = i + 1
  end
  close_box()
  doc.blocks = out
  return doc
end

return {
  { Meta = Meta, Table = Table },            -- tables measured before inline code is rewritten
  { Inlines = Inlines },
  { Link = Link, RawInline = RawInline, RawBlock = RawBlock, CodeBlock = CodeBlock, BlockQuote = BlockQuote,
    Code = Code, Para = Para },
  { Pandoc = Pandoc },
}
