#!/usr/bin/env bash
# One honest line about the last build. Born 2026-10-23 from reading "0 overfull" out of
# the log of a build that had DIED on a LaTeX error - see LEDGER-DEFECTS.md entry 17.
# A count from a log is worthless unless the build that wrote it succeeded.
set -uo pipefail
cd "$(dirname "$0")/../latex"
rm -f book.fdb_latexmk
make >/tmp/build-probe.log 2>&1
rc=$?
err=$(grep -c '^!' book.log || true)
ovf=$(grep -c 'Overfull' book.log || true)
gly=$(grep -c 'Missing character' book.log || true)
printf 'exit=%s  latex-errors=%s  overfull=%s  glyphs=%s\n' "$rc" "$err" "$ovf" "$gly"
if [ "$rc" != "0" ] || [ "$err" != "0" ]; then
  echo "--- BUILD DID NOT SUCCEED. The counts above mean nothing. First error:"
  grep -A3 '^!' book.log | head -8
  exit 1
fi
[ "$ovf" = "0" ] && [ "$gly" = "0" ]
