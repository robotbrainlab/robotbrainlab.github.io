#!/usr/bin/env python3
"""Build TOC.pdf: the plan, set in the book's own design.

Reads TOC.md, turns its tables into readable blocks, and builds them through a throwaway
copy of latex/ so the result carries the series cover, the book's fonts and page size, and
a contents list of every chapter.

    python3 tools/make-toc-pdf.py

Writes TOC.pdf in the repository root. TOC.pdf is generated and is in .gitignore; edit
TOC.md and run this again.
"""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Each part of TOC.md becomes one chapter of the review PDF.
CHAPTERS = {
    'Part I · Mental Model': '01-part-i-mental-model',
    'Part I · Inside the Model': '02-part-i-inside-the-model',
    'Part II · Use': '03-part-ii',
    'Part III · Apply': '04-part-iii',
    'Part IV · What Next': '05-part-iv',
    'Appendices': '06-appendices',
    'Who owns what': '07-who-owns-what',
    'Writing and delivery order': '08-delivery-order',
}
PREFACE = """# Preface

This is not the book. This is the plan for the book, set in the book's own design so it reads
the way the finished book will read.

It lists every chapter, the problem each one opens with, what each one covers, and how many
pages it is budgeted. Nothing has been drafted. Read it, mark what is wrong, and the plan
changes before a word of the book is written.

The book is about 1,040 pages in four parts and one interlude, and it teaches modern AI
engineering from zero.
"""


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def split_sections(lines):
    """Split TOC.md on '## ' headings into (heading, body-lines), reflowing its tables."""
    sections, head, body, i = [], None, [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('## '):
            if head:
                sections.append((head, body))
            head, body = line[3:].strip(), []
            i += 1
            continue
        is_table = (line.startswith('|') and i + 1 < len(lines)
                    and set(lines[i + 1].replace('|', '').replace(' ', '')) <= {'-', ':'})
        if is_table:
            header, rows, j = cells(line), [], i + 2
            while j < len(lines) and lines[j].startswith('|'):
                rows.append(cells(lines[j]))
                j += 1
            if 'Opens with' in header:          # a chapter or lab table
                what = header[3]
                for r in rows:
                    body += [f'## {r[0]}. {r[1]}', '', f'*{r[2]}*', '',
                             f'**{what}:** {r[3]} **({r[4]} pages)**', '']
            elif header[:2] == ['#', 'Appendix']:
                for r in rows:
                    body += [f'## {r[0]}. {r[1]}', '', f'{r[2]} **({r[3]} pages)**', '']
            else:                                # any other table stays a table
                body += lines[i:j] + ['']
            i = j
            continue
        if head is not None:
            body.append(line)
        i += 1
    sections.append((head, body))
    return sections


def main():
    toc = (ROOT / 'TOC.md').read_text().split('\n')
    with tempfile.TemporaryDirectory() as tmp:
        build = Path(tmp) / 'tocbook'
        (build / 'markdown').mkdir(parents=True)
        shutil.copytree(ROOT / 'latex', build / 'latex',
                        ignore=shutil.ignore_patterns('chapters', 'generated', '*.pdf', '*.aux',
                                                      '*.log', '*.toc', '*.out', '*.fls',
                                                      '*.fdb_latexmk', '*.xdv', '*.idx', '*.ilg',
                                                      '*.ind'))
        md = build / 'markdown'
        (md / '00-preface.md').write_text(PREFACE)
        stems = []
        for head, body in split_sections(toc):
            if not head:
                continue
            stem = CHAPTERS.get(head.split('—')[0].strip())
            if not stem:
                continue
            text = re.sub(r'\n{3,}', '\n\n', '\n'.join(body).strip())
            (md / f'{stem}.md').write_text(f'# {head}\n\n{text}\n')
            stems.append(stem)
        if len(stems) != len(CHAPTERS):
            sys.exit(f'TOC.md is missing sections: expected {len(CHAPTERS)}, found {len(stems)}')

        tex = build / 'latex'
        book = (tex / 'book.tex').read_text()
        start = book.index('% Chapters are commented out')
        end = book.index('% ---------------------------------------------------------------- Appendices')
        body = '\n'.join(f'\\input{{chapters/{s}}}' for s in stems)
        book = book[:start] + body + '\n\n' + book[end:]
        book = re.sub(r'%% \\input\{chapters/[A-Z]-[a-z-]+\}[^\n]*\n', '', book)
        book = book.replace('\\backmatter\n\\printindex', '\\backmatter')
        (tex / 'book.tex').write_text(book)

        meta = (tex / 'book-meta.tex').read_text()
        meta = meta.replace('{Understand, Use, Evaluate, Build}', '{Table of Contents}')
        meta = re.sub(r'\\newcommand\{\\BookLongSubtitle\}\{[^}]*\}',
                      '\\\\newcommand{\\\\BookLongSubtitle}{The plan for review --- every chapter,\\\\\\\\\n'
                      '  its problem, and its page budget}', meta, flags=re.S)
        meta = meta.replace('{From the first model call to a system you can defend}',
                            '{The plan, before a word is written}')
        (tex / 'book-meta.tex').write_text(meta)

        env = dict(os.environ, PATH='/Library/TeX/texbin:/opt/homebrew/bin:' + os.environ['PATH'])
        r = subprocess.run(['make'], cwd=tex, env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-3000:] + r.stderr[-2000:])
        shutil.copy(tex / 'book.pdf', ROOT / 'TOC.pdf')

    pages = subprocess.run(['pdfinfo', str(ROOT / 'TOC.pdf')], capture_output=True, text=True).stdout
    print('TOC.pdf written.', [l for l in pages.split('\n') if l.startswith('Pages')][0])


if __name__ == '__main__':
    main()
