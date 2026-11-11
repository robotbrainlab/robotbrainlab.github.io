#!/usr/bin/env perl
# ================================================================
# standalone.pl — small wording fixes so the book reads as ONE
# standalone book (no "this library", no "section 2", no volumes).
# Applied to the Markdown stream at conversion time; the Markdown
# files themselves are never modified.
#
# Usage:  perl tools/standalone.pl <stem> < in.md > out.md
# ================================================================
use strict; use warnings; use utf8;
binmode STDIN, ':encoding(UTF-8)'; binmode STDOUT, ':encoding(UTF-8)';
my $stem = shift // '';
local $/; my $t = <STDIN>;

# Everywhere: strip on-screen navigation scaffolding
$t =~ s/<!-- NAV:(TOP|TOC|BACK):START -->.*?<!-- NAV:\1:END -->\n?//gs;
$t =~ s/^<sub>.*?<\/sub>\s*$//gm;
$t =~ s/^## Table of Contents\s*\n.*?(?=^## )//ms;            # in-document TOCs
$t =~ s/^\[↑ Back to (?:TOC|Table of Contents)\]\(#table-of-contents\)\s*$//gm;

if ($stem eq 'product-discovery') {
  $t =~ s/\(section 2\) picks up/(Part II) picks up/;
}
elsif ($stem eq 'project-planning-guide') {
  $t =~ s/independent of any specific book, framework, or language\./independent of any specific framework or language./;
  $t =~ s/^(##\s+(?:What|How to Read|How)) This Document\b/$1 This Guide/gm;
}
elsif ($stem eq 'writing-good-code') {
  $t =~ s/it is what this\s+document is about\./it is what this part of the book is about./;
  $t =~ s/\s*Capturing both was the original reason this reference library exists\.//;
  $t =~ s/It has two halves,/It has two chapters,/;
  $t =~ s/\*\*Part I — The Craft\.\*\*/**The Craft of Good Code.**/;
  $t =~ s/\*\*Part II — The Practices & Maturity Model\.\*\*/**Engineering Practices & Maturity.**/;
  # its own "Appendix A–C" would clash with the book's Appendices A–F
  $t =~ s/^### Appendix [ABC] — /### /gm;
  $t =~ s/^Part I is about each \*piece\* of code\. This part is about/The previous chapter is about each *piece* of code. This chapter is about/m;
  $t =~ s/^This document serves two purposes:/This chapter serves two purposes:/m;
}
elsif ($stem eq 'part4-introduction') {
  # Keep only the Book's preface material (drop title page, copyright,
  # dedication, its own TOC, the five-volume reading path, the problem-framing
  # section that Parts I–II already cover, and acknowledgements).
  $t =~ s/\A.*?(?=^# Preface\s*$)//ms;
  $t =~ s/^# Before the Code.*\z//ms;
  $t =~ s/^## The Volume-Based Path.*?(?=^#{1,2} )//ms;
  $t =~ s/^# Preface\s*$/# About This Part/m;
  $t =~ s/^# How to Read This Book\s*$/# How to Read This Part/m;
  $t =~ s/\bThis Book\b/This Part/g;
  $t =~ s/\bThis book\b/This part/g;
  $t =~ s/\bthis book\b/this part/g;
}
elsif ($stem eq '44-appendices') {
  # nothing yet
}
print $t;
