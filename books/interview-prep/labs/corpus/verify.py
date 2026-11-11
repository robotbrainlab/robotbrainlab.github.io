"""Check that the corpus is what README.md says it is.

Every row of the README's "What was deliberately planted" table is a claim
about these files. This checks each one, so a lab cannot report as a finding
something the corpus was built to contain - and so that an edit to a document
cannot quietly remove a property a later lab depends on.

Run: python3 verify.py
"""

import pathlib
import re
import subprocess
import sys

DOCS = pathlib.Path("docs")
fails = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f" - {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def body(stem):
    return (DOCS / f"{stem}.md").read_text()


def words(stem):
    return len(body(stem).split())


if __name__ == "__main__":
    docs = sorted(p.stem for p in DOCS.glob("*.md"))
    check("forty documents", len(docs) == 40, f"{len(docs)}")

    # Judgements cover every pair, and the grades are only 0, 1, 2.
    rows = [l.split("\t") for l in
            pathlib.Path("judgements.tsv").read_text().strip().split("\n")[1:]]
    qs = [l.split("\t")[0] for l in
          pathlib.Path("queries.tsv").read_text().strip().split("\n")[1:]]
    check("eight queries", len(qs) == 8, f"{len(qs)}")
    check("every query-document pair judged",
          len(rows) == len(qs) * len(docs), f"{len(rows)}")
    check("grades are 0, 1 or 2 only",
          {r[2] for r in rows} == {"0", "1", "2"}, str(sorted({r[2] for r in rows})))

    graded = {}
    for q, d, g in rows:
        graded.setdefault(q, {})[d] = int(g)

    # 1. Identifiers a similarity score cannot match.
    check("SKU codes present",
          len(re.findall(r"HL-\d{4}", body("product-kettle-hl-2208"))) >= 2)
    check("the SKU convention is explained somewhere",
          "HL-nnnn" in body("sku-conventions"))

    # 2. An answer split across two documents, neither holding all of it.
    fees, exc = body("delivery-fees"), body("delivery-exceptions")
    check("delivery-fees has the base charges and NOT the surcharge",
          "3.99" in fees and "9.50" not in fees)
    check("delivery-exceptions has the surcharge and NOT the base charges",
          "9.50" in exc and "3.99" not in exc)
    check("neither is graded 2 for the split query",
          max(graded["q3"].values()) == 1, f"max grade {max(graded['q3'].values())}")

    # 3. Two documents that disagree on a figure.
    check("refunds-policy says 14 days", "14 days" in body("refunds-policy"))
    check("refunds-faq says 30 days", "30 days" in body("refunds-faq"))
    check("no document is graded 2 for the contradiction query",
          max(graded["q5"].values()) == 1, f"max grade {max(graded['q5'].values())}")

    # 4. A near-duplicate pair differing in one clause.
    a = set(body("returns-standard").split())
    b = set(body("returns-clearance").split())
    j = len(a & b) / len(a | b)
    check("returns-standard and returns-clearance overlap heavily",
          j > 0.6, f"Jaccard {j:.2f}")
    check("they differ on the window",
          "30 days" in body("returns-standard")
          and "14 days" in body("returns-clearance"))
    check("they differ on who pays postage",
          "paid by the customer" in body("returns-clearance")
          and "postage is free" in body("returns-standard"))

    # 5. Page furniture repeated across one set.
    foot = "Review cycle: annual"
    withfoot = [d for d in docs if foot in body(d)]
    check("page furniture on the policy set only",
          len(withfoot) == 10, f"{len(withfoot)} documents")

    # 6. One document far longer than the rest.
    longest = max(docs, key=words)
    others = sorted(words(d) for d in docs if d != longest)
    median = others[len(others) // 2]
    check("warranty-full is the longest, by a wide margin",
          longest == "warranty-full" and words(longest) > 4 * median,
          f"{words(longest)} words against a median of {median}")

    # 7. One document that answers no query at all.
    never = [d for d in docs if all(graded[q][d] == 0 for q in qs)]
    check("about-us is graded 0 for every query", "about-us" in never)
    check("there are distractors that answer nothing",
          len(never) >= 20, f"{len(never)} such documents")

    # 8. The injection target exists and is retrievable prose.
    check("shipping-partners names carriers in prose",
          "Pellworth" in body("shipping-partners"))

    # 9. The awkward PDF: page 1 misparses, page 2 has no text layer.
    try:
        p1 = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "awkward.pdf", "-"],
                            capture_output=True, text=True, check=True).stdout
        p2 = subprocess.run(["pdftotext", "-f", "2", "-l", "2", "awkward.pdf", "-"],
                            capture_output=True, text=True, check=True).stdout
        # The dash is an en dash: LaTeX turns `--` into one, so an ASCII
        # hyphen here passes nothing. The first version of this check did
        # exactly that and reported the property missing.
        check("page 1 splices a surcharge into a postcode range",
              bool(re.search(r"PA20[-\u2013\u2014]+9\.50", p1)),
              "the planted misparse")
        check("page 2 yields no text", len(p2.strip()) == 0,
              f"{len(p2.strip())} characters")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        check("awkward.pdf checked with pdftotext", False, f"{type(e).__name__}")

    print()
    if fails:
        print(f"  {len(fails)} FAILED: {', '.join(fails)}")
        sys.exit(1)
    print("  the corpus is what README.md says it is")
