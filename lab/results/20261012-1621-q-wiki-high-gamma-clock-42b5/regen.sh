#!/usr/bin/env bash
# regen.sh — regenerates every number in the dossier and on the page.
# The runner applies work/patch.diff first (it adds this run folder; no repo file outside it
# is touched). Runs in ~10 s; needs the claude/lab-* refs (any clone of the private remote).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"

bash "$here/extract.sh" > "$here/work/regen-run.log" 2>&1 || {
  echo "extract.sh failed:" >&2; tail -5 "$here/work/regen-run.log" >&2; exit 1
}

sed -n '1,/^--- branch triage/p' "$here/work/extract.txt" | grep -v '^--- branch triage' > "$here/work/regen-checks.txt"
if ! diff -u "$here/work/extract-expected.txt" "$here/work/regen-checks.txt"; then
  echo "FAIL: the grounded strings no longer match their runs' records" >&2
  exit 1
fi
n=$(grep -c '^OK' "$here/work/regen-checks.txt")
echo "regen OK: $n grounded fixed strings from the four runs' records, 0 misses."
echo "The branch triage appended to work/extract.txt documents the no-missed-run scan (P2);"
echo "its id list grows as later runs land — the OK/MISS section above is the invariant part."
