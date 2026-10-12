#!/bin/sh
# regen.sh — 20261012-1904-q-wiki-view-d2e5 (compiler run, topic: view)
# Regenerates every number in dossier.md from the run branches (git refs) and
# the tree. No build, no network; ~30 s. Exit 0 = every citation resolves.
set -u
cd "$(dirname "$0")/../../.." || exit 1   # repo root (the lab checkout)

RUNS="20261006-0030-m-obscure-8202 20261006-1029-constraint-f22e \
20261006-1436-quant-18e5 20261008-0458-constraint-3102 \
20261008-0945-second-20261008-0743-constraint-4588-0e54 20261008-1521-quant-97fd \
20261008-1859-scout-141c 20261008-2113-second-20261008-2031-constraint-4b27-08f7 \
20261008-2349-constraint-70b0 20261009-0521-redteam-93a4 20261009-0621-constraint-51bf \
20261009-1649-second-20261009-1556-redteam-18fc-94dc 20261009-2120-redteam-ace6 \
20261010-0541-system-d51f 20261010-1544-scout-c4cb 20261010-2052-redteam-8be2 \
20261010-2141-second-20261010-2052-redteam-8be2-9f4a 20261010-2220-scout-9096 \
20261010-2314-redteam-0b45 20261011-0006-constraint-48cf 20261011-0614-redteam-a616 \
20261011-0924-redteam-5977 20261011-1234-redteam-6eae 20261011-1332-constraint-acff \
20261011-1332-second-20261011-1234-redteam-6eae-8f00 20261011-1917-redteam-fb64 \
20261012-0138-redteam-0fe0 20261012-0311-components-5465"

PAGE=lab/results/20261012-1904-q-wiki-view-d2e5/wiki/view.md
fail=0

echo "== 1. Grade roster (dossier: 'exactly 5 gold / 20 silver / 3 missing') =="
gold=0; silver=0; missing=0
for id in $RUNS; do
  # grade may sit on line 1 or after a title line; take the first 5 lines
  g=$(git show "origin/claude/lab-$id:lab/results/$id/check.md" 2>/dev/null \
      | head -5 | sed -n 's/^Grade: *//p' | head -1 | tr -d '\r')
  case "$g" in
    gold)    gold=$((gold+1));     tag=gold ;;
    silver)  silver=$((silver+1)); tag=silver ;;
    *)       missing=$((missing+1)); tag=MISSING ;;
  esac
  printf '  %-58s %s\n' "$id" "$tag"
done
echo "  totals: gold=$gold silver=$silver missing=$missing (of $(echo $RUNS | wc -w))"
[ "$gold" = 5 ] && [ "$silver" = 20 ] && [ "$missing" = 3 ] || { echo "  MISMATCH"; fail=1; }

echo "== 2. The five least-certain numbers (predictions.md P6), from each run's own branch =="
# (a) 8be2 kill ratio 3.32x is the checker-corrected value; author published 2.37x
git show origin/claude/lab-20261010-2052-redteam-8be2:lab/results/20261010-2052-redteam-8be2/check.md \
  | grep -q '2.37× at χ = 0.998 as published, \*\*3.32× after my correction\*\*' \
  && echo "  (a) 8be2: '2.37× as published, 3.32× after my correction' FOUND" \
  || { echo "  (a) 8be2 NOT FOUND"; fail=1; }
# (b) 0e54 served fraction 5.5-31.2% of rows
git show origin/claude/lab-20261008-0945-second-20261008-0743-constraint-4588-0e54:lab/results/20261008-0945-second-20261008-0743-constraint-4588-0e54/check.md \
  | grep -q 'serves 5.5–31.2 % of rows' \
  && echo "  (b) 0e54: 'serves 5.5–31.2 % of rows' FOUND" \
  || { echo "  (b) 0e54 NOT FOUND"; fail=1; }
# (c) 48cf 1080p far median 110.7 ms vs author's extrapolated 60+
git show origin/claude/lab-20261011-0006-constraint-48cf:lab/results/20261011-0006-constraint-48cf/check.md \
  | grep -q '1080p gave 110.7 ms (author extrapolated "60+")' \
  && echo "  (c) 48cf: '1080p gave 110.7 ms' FOUND" \
  || { echo "  (c) 48cf NOT FOUND"; fail=1; }
# (d) d51f gather/engine 13-18x is the lab_arrival harness figure
git show origin/claude/lab-20261010-0541-system-d51f:lab/results/20261010-0541-system-d51f/check.md \
  | grep -q 'gather 775–858 µs vs engine 56–62 µs median, 13–18× across seeds' \
  && echo "  (d) d51f: '775–858 µs vs 56–62 µs, 13–18×' FOUND (lab_arrival harness)" \
  || { echo "  (d) d51f NOT FOUND"; fail=1; }
# (e) 8f00 visibility threshold >1/50 with 43-84% of azimuths
git show origin/claude/lab-20261011-1332-second-20261011-1234-redteam-6eae-8f00:lab/results/20261011-1332-second-20261011-1234-redteam-6eae-8f00/check.md \
  | grep -q '(>1/50) on 43% (r_o=100M) to 84% (r_o=3.2M) of emitter azimuths' \
  && echo "  (e) 8f00: '>1/50 on 43%–84% of emitter azimuths' FOUND" \
  || { echo "  (e) 8f00 NOT FOUND"; fail=1; }

echo "== 3. Page run lines vs branches (dossier: '22 run lines; every citation resolves') =="
lines=$(grep -c '^- 2026' "$PAGE")
echo "  run lines on page: $lines (expect 22)"
[ "$lines" = 22 ] || { echo "  MISMATCH"; fail=1; }
for id in $(sed -n 's/^- \(2026[0-9a-z-]*\) (\(gold\|silver\|missing\)).*/\1/p' "$PAGE"); do
  git rev-parse --verify -q "origin/claude/lab-$id" >/dev/null || { echo "  NO BRANCH: $id"; fail=1; }
done
echo "  all page run ids resolve to claude/lab-* branches"

echo "== 4. Design-letter anchors and history (page: law.md Observation, representation.md:57, H0183) =="
grep -q 'Positions are gathered at the observer.s past light cone. Lensing takes deflection(b) from the doll.s memo.' docs/law.md \
  && echo "  law.md Observation anchor FOUND" || { echo "  law.md anchor NOT FOUND"; fail=1; }
sed -n '57p' docs/representation.md | grep -q 'crosses the observer.s past light cone once' \
  && echo "  representation.md:57 'crosses once' FOUND" || { echo "  representation.md:57 NOT FOUND"; fail=1; }
grep -q 'H0183 — The GR oracle gains Shapiro delay' docs/HISTORY.md \
  && echo "  H0183 'oracle gains Shapiro delay' FOUND" || { echo "  H0183 NOT FOUND"; fail=1; }

echo "== 5. Ungraded runs appear only as marked leads =="
grep -n 'ungraded `a616`\|(`70b0`, ungraded)' "$PAGE" | sed 's/^/  /'

echo
[ "$fail" = 0 ] && echo "REGEN OK: roster, five numbers, page lines, anchors all resolve" \
                || echo "REGEN FAILED (see above)"
exit $fail
