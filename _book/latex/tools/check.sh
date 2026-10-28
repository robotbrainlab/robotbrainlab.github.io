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
# The 50-100 default came from the book template and this book passed it before Part I was
# finished, so `make check` had been reporting PRE-FLIGHT FAILED on nothing else for weeks and
# nobody read it. TOC.md plans about 1,040 printed pages; the window is that, with room either
# side. A gate that always fails is a gate that gates nothing. Raised 2026-10-28.
MIN="${PAGES_MIN:-100}"; MAX="${PAGES_MAX:-1400}"
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

# Glossary freshness. NOT a scan of bold spans: that version flagged 40 things of which
# about 36 were emphasis or lab labels ("not", "second", "P", "Paragraph 10"), because the
# book bolds whole phrases for emphasis as house style. 90% noise is a gate nobody reads
# (LEDGER-DEFECTS.md entry 18). The curated term list is each chapter's `### Key Terms`
# table, so Appendix C is generated from those and this only asks whether it is current.
if ! python3 "$HERE/../tools/glossary.py" --check; then fail=1; fi

if [[ $fail -eq 0 ]]; then echo "PRE-FLIGHT OK"; else echo "PRE-FLIGHT FAILED"; fi
exit $fail
