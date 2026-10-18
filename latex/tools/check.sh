#!/usr/bin/env bash
# ================================================================
# check.sh — pre-flight checks on a built book (run by "make check").
#   * no overfull boxes (text running into the margin), no text off any page
#   * no missing glyphs, no undefined references
#   * page size 504 x 661.5 pt, the three series fonts embedded
#   * numbered page count (Part I to the end of the glossary) inside the target
#     (PAGES_MIN / PAGES_MAX, default 50–100)
#   * bold terms that are not in the glossary (a reminder, not an error)
# ================================================================
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"
PDF="${PDF:-book.pdf}"; LOG="${PDF%.pdf}.log"
MIN="${PAGES_MIN:-50}"; MAX="${PAGES_MAX:-100}"
export PATH="/Library/TeX/texbin:/opt/homebrew/bin:$PATH"
fail=0

[[ -f "$PDF" && -f "$LOG" ]] || { echo "check: build first ($PDF / $LOG missing)"; exit 1; }

over=$(grep -c '^Overfull' "$LOG" || true)
echo "Overfull boxes:        $over"
if [[ "$over" -gt 0 ]]; then fail=1; grep -A1 '^Overfull' "$LOG" | sed 's/^/    /' | head -40; fi

under=$(grep -c '^Underfull' "$LOG" || true)
echo "Underfull boxes:       $under   (loose lines; usually harmless)"

miss=$(grep -c 'Missing character' "$LOG" || true)
echo "Missing glyphs:        $miss"
if [[ "$miss" -gt 0 ]]; then fail=1; grep 'Missing character' "$LOG" | sort | uniq -c | sed 's/^/    /' | head -20; fi

undef=$(grep -c -E "Reference .* undefined|Citation .* undefined" "$LOG" || true)
echo "Undefined references:  $undef"
if [[ "$undef" -gt 0 ]]; then fail=1; grep -E "Reference .* undefined" "$LOG" | sed 's/^/    /' | head -20; fi

# Text that runs off any page (covers included, which TeX does not report as overfull).
offpage=$(pdftotext -bbox "$PDF" - 2>/dev/null | python3 -c '
import sys, re
page, bad = 0, []
for line in sys.stdin:
    m = re.search(r"<page width=\"([\d.]+)\" height=\"([\d.]+)\"", line)
    if m: page += 1; W, H = float(m[1]), float(m[2]); continue
    m = re.search(r"xMin=\"([-\d.]+)\" yMin=\"([-\d.]+)\" xMax=\"([-\d.]+)\" yMax=\"([-\d.]+)\">(.*)</word>", line)
    if m:
        x0, y0, x1, y1 = map(float, m.groups()[:4])
        if x0 < 18 or y0 < 0 or x1 > W - 18 or y1 > H: bad.append(f"page {page}: {m[5]}")
print(len(bad)); print("\n".join(bad[:20]))')
echo "Text off the page:     $(echo "$offpage" | head -1)"
if [[ "$(echo "$offpage" | head -1)" -gt 0 ]]; then fail=1; echo "$offpage" | tail -n +2 | sed 's/^/    /'; fi

pages=$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')
size=$(pdfinfo "$PDF" | awk -F': *' '/^Page size:/ {print $2}')
echo "Page size:             $size"
[[ "$size" == 504\ x\ 661.5\ pts* ]] || { echo "    expected 504 x 661.5 pts"; fail=1; }
# Numbered pages: from the Part I opener up to (not including) the Index.
numbered=$(pdftotext -layout "$PDF" - | python3 -c '
import sys, re
pages = sys.stdin.read().split("\f")
flat = [" ".join(p.split()) for p in pages]
start = next((i for i, p in enumerate(flat) if re.match(r"PART I\b", p)), 0)
end = next((i for i, p in enumerate(flat) if i > start and re.match(r"Index\b", p)), len(pages) - 1)
print(end - start)')
echo "PDF pages:             $pages   (everything, including cover, front matter, index)"
echo "Numbered pages:        $numbered   (Part I to the end of the glossary; target $MIN–$MAX)"
if [[ "$numbered" -lt "$MIN" || "$numbered" -gt "$MAX" ]]; then echo "    outside the page target"; fail=1; fi

fonts=$(pdffonts "$PDF" | awk 'NR>2 {print $1}' | sed 's/^[A-Z]*+//' | sort -u)
for fam in CrimsonPro SourceSans3 SourceCodePro; do
  if echo "$fonts" | grep -q "^$fam"; then echo "Font embedded:         $fam"; else echo "Font MISSING:          $fam"; fail=1; fi
done
other=$(echo "$fonts" | grep -v -E '^(CrimsonPro|SourceSans3|SourceCodePro|EBGaramond)' | tr '\n' ' ')
[[ -n "$other" ]] && echo "Other fonts:           $other"

# Bold terms missing from the glossary (glossary = the Markdown file titled "# Glossary")
python3 - "$HERE/${MARKDOWN_DIR:-../markdown}" <<'PY'
import re, sys, pathlib
md = pathlib.Path(sys.argv[1])
files = sorted(p for p in md.glob('*.md') if not p.name.startswith('_'))
gloss = next((p for p in files if re.search(r'^#\s+Glossary\s*$', p.read_text(), re.M)), None)
if not gloss:
    print('Glossary:              none found (a file titled "# Glossary")'); sys.exit(0)
def norm(t): return re.sub(r'\s*\(.*?\)\s*', ' ', t.replace('`', '')).strip().lower().rstrip('s')
terms = set()
for line in gloss.read_text().splitlines():
    m = re.match(r'^(\*\*)?([^:*][^:]*?)(\*\*)?\s*$', line)
    if m and line.strip() and not line.startswith(('#', ':', '>', '-', '|')):
        terms.add(norm(m.group(2)))
    m = re.match(r'^\*\*(.+?)\*\*\s*:', line)
    if m: terms.add(norm(m.group(1)))
    if line.startswith('|'):                      # a table glossary: | Term | Meaning |
        cell = line.strip('|').split('|')[0].strip().strip('*').strip()
        if cell and cell.lower() != 'term' and not set(cell) <= set('-: '):
            terms.add(norm(cell))
missing = {}
for p in files:
    if p == gloss or re.search(r'^#\s+Preface\s*$', p.read_text(), re.M): continue
    text = re.sub(r'```.*?```', '', p.read_text(), flags=re.S)
    for t in re.findall(r'\*\*([^*\n]+?)\*\*', text):
        t = t.strip()
        if re.search(r'[:.!?]$', t) or len(t.split()) > 4 or t.lower().startswith(('you understand', 'tip', 'note', 'warning')):
            continue
        if norm(t) not in terms and norm(t).removesuffix('e').rstrip('s') not in terms: missing.setdefault(t, p.name)  # 'addresses'
print(f'Bold terms not in glossary: {len(missing)}')
for t, f in sorted(missing.items(), key=lambda x: x[0].lower())[:40]:
    print(f'    {t}   ({f})')
PY

if [[ $fail -eq 0 ]]; then echo "PRE-FLIGHT OK"; else echo "PRE-FLIGHT FAILED"; fi
exit $fail
