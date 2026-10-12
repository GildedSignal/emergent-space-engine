#!/usr/bin/env bash
# Regen for 20261012-1715-second-...-56e0 (second author on the kick-jet page compile).
# Re-extracts every load-bearing number/grade the dossier and the wiki page cite, from the
# run branches (origin/claude/lab-<id>) and main, INCLUDING the check2 grade lines the
# standing grades rest on (the first checker's named gap). ~10 s, no build.
set -u
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261012-1715-second-20261012-1621-q-wiki-kick-jet-9392-56e0
ok=0; fail=0
chk() { if [ "$1" = "0" ]; then echo "  ok: $2"; ok=$((ok+1)); else echo "  FAIL: $2"; fail=$((fail+1)); fi; }
has() { grep -qF -- "$2" "$1"; }
src() { git show "origin/claude/lab-$1:lab/results/$1/$2" 2>/dev/null; }

echo "== adopted state on main =="
has docs/law.md 'The jet is retired (12 October)' ; chk $? "law.md retires the jet (12 October)"
has docs/law.md '20261006-1249-redteam-4978'       ; chk $? "law.md:35 cites gold 4978"
has docs/law.md '0ccd-b33f'                        ; chk $? "law.md:35 cites gold b33f"
has docs/law.md '4808-d617'                        ; chk $? "law.md:35 cites gold d617"
has docs/law.md 'the adopting run of 6 October had one checker'; chk $? "df81 flagged single-checker"
has docs/law.md "Peters' a(t) is its generator"    ; chk $? "inspiral is Peters' generator"
has docs/representation.md 'so a kick updates the cycle by a multiply-add'; chk $? "representation.md:67 lags (design-doc contradiction)"
has docs/HANDOFF.md 'done in law.md (not in the shipped code)' ; chk $? "HANDOFF item 4 struck: retirement done in law.md, not wired in shipped code"
echo "== grades of record, both checks (check1, check2) =="
# standing gold: check1 gold AND check2 gold
for id in 20261006-1249-redteam-4978 \
          20261008-1419-second-20261008-1337-redteam-2040-9a04 \
          20261008-1613-second-20261008-1521-spacex-8016-6c47 \
          20261008-1757-second-20261008-1719-system-0ccd-b33f \
          20261009-1936-second-20261009-1858-redteam-075b-a059 \
          20261010-0306-second-20261010-0100-fermi-c11c-4cb2 \
          20261010-1706-second-20261010-1544-system-97ce-b18f \
          20261011-2306-second-20261011-2235-redteam-6164-ee08 \
          20261011-1729-components-b063 \
          20261012-0036-second-20261011-2306-system-3367-1e74 \
          20261012-1227-second-20261012-1117-redteam-4808-d617; do
  a=$(src "$id" check.md  | grep -am1 '^Grade:' | tr -d '\r')
  b=$(src "$id" check2.md | grep -am1 '^Grade:' | tr -d '\r')
  [ "$a" = 'Grade: gold' ] && [ "$b" = 'Grade: gold' ]; chk $? "$id stands gold: check1/check2 = $a/$b"
done
# gold first check, SILVER second -> standing silver (annotated on the page)
for id in 20261007-0621-components-8306 20261008-1613-redteam-7922 \
          20261008-1419-components-620e \
          20261008-1719-second-20261008-1613-redteam-7922-e86c \
          20261009-0521-second-20261009-0401-quant-ea6b-96b4 \
          20261010-1816-system-67f2 20261011-2235-redteam-6164; do
  a=$(src "$id" check.md  | grep -am1 '^Grade:' | tr -d '\r')
  b=$(src "$id" check2.md | grep -am1 '^Grade:' | tr -d '\r')
  [ "$a" = 'Grade: gold' ] && [ "$b" = 'Grade: silver' ]; chk $? "$id gold-then-silver, stands silver: $a/$b"
done
# single-check silvers (check1 silver, no check2)
for id in 20261006-0220-autoresearch-c3a5 20261006-0437-constraint-ec9d \
          20261007-1843-second-20261007-1801-fermi-bb60-152f 20261008-0234-spacex-0083 \
          20261008-0338-second-20261008-0234-spacex-0083-492f 20261008-1337-redteam-2040 \
          20261008-1521-spacex-8016 20261008-1521-autoresearch-a48d 20261008-1719-system-0ccd \
          20261009-0401-quant-ea6b 20261009-1858-redteam-075b 20261010-0541-components-8c81 \
          20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2 20261010-0920-quant-30e1 \
          20261010-1947-autoresearch-2833 20261010-2141-system-eea5 20261011-1456-components-f797 \
          20261011-1729-system-2c68 20261012-0358-components-fa08 20261012-1117-redteam-4808; do
  a=$(src "$id" check.md  | grep -am1 '^Grade:' | tr -d '\r')
  b=$(src "$id" check2.md | grep -am1 '^Grade:' | tr -d '\r')
  [ "$a" = 'Grade: silver' ] && [ -z "$b" ]; chk $? "$id single-check silver: $a/none"
done
# df81: gold by its one checker, flagged on the page and in law.md
a=$(src 20261006-0346-redteam-df81 check.md  | grep -am1 '^Grade:' | tr -d '\r')
b=$(src 20261006-0346-redteam-df81 check2.md | grep -am1 '^Grade:' | tr -d '\r')
[ "$a" = 'Grade: gold' ] && [ -z "$b" ]; chk $? "df81 single-checker gold (flagged): $a/none"
# b242: no check at all
src 20261011-1814-second-20261011-1729-system-2c68-b242 check.md | grep -q '^Grade:'
[ $? != 0 ]; chk $? "b242 has no check.md (missing, ungraded)"

echo "== sampled page numbers appear verbatim in their sources =="
src 20261006-1249-redteam-4978 dossier.md | grep -q '2 808 rad' ; chk $? "4978: separatrix error exceeds the cycle (2808 rad)"
src 20261008-1419-second-20261008-1337-redteam-2040-9a04 dossier.md | grep -q '15/8' ; chk $? "9a04: E-axis constant 15/8"
src 20261009-1936-second-20261009-1858-redteam-075b-a059 dossier.md | grep -q '≲ 0.05' ; chk $? "a059: skin boundary <=0.05 (unicode)"
src 20261008-1757-second-20261008-1719-system-0ccd-b33f dossier.md | grep -q '2.75×' ; chk $? "b33f: 2.75x on the kick median"
src 20261010-1706-second-20261010-1544-system-97ce-b18f dossier.md | grep -qF '1.5×10⁻³ median over 24 game-years' ; chk $? "b18f: |da|/a 1.5e-3 over 24 game-years"
src 20261010-1706-second-20261010-1544-system-97ce-b18f dossier.md | grep -q '0.0160 compiles/kick' ; chk $? "b18f: 0.0160 compiles/kick"
src 20261012-0036-second-20261011-2306-system-3367-1e74 dossier.md | grep -qF '1.3–1.5× (made, player) and 3.0–3.8× (leavers)' ; chk $? "1e74: carry ceiling 1.3-1.5x / 3.0-3.8x"
src 20261012-0036-second-20261011-2306-system-3367-1e74 dossier.md | grep -q '26 µs' ; chk $? "1e74: ~26 us machinery floor"
src 20261012-1227-second-20261012-1117-redteam-4808-d617 dossier.md | grep -qF 'μ = p − p_crit(e) ≤ 0.3' ; chk $? "d617: margin mu<=0.3"
src 20261012-1227-second-20261012-1117-redteam-4808-d617 dossier.md | grep -q '30–40%' ; chk $? "d617: band fed 30-40%"
src 20261011-2306-second-20261011-2235-redteam-6164-ee08 dossier.md | grep -q 'χ ∈ {0.5, 0.9, 0.998}' ; chk $? "ee08: Kerr spins"
src 20261011-2306-second-20261011-2235-redteam-6164-ee08 dossier.md | grep -q '15/8' ; chk $? "ee08: T-channel 15/8"
src 20261012-0358-components-fa08 check.md | grep -q '270×' ; chk $? "fa08: rebind ~270x above floor"
src 20261012-0358-components-fa08 check.md | grep -q '7–13×' ; chk $? "fa08: jet closes to 7-13x"
src 20261008-1613-second-20261008-1521-spacex-8016-6c47 check.md | grep -q '92.5–95.1%' ; chk $? "6c47: memo hits 92.5-95.1%"
src 20261008-1719-second-20261008-1613-redteam-7922-e86c check.md | grep -q '543·(1−e²)^(2/3)' ; chk $? "e86c: horizon 543*(1-e^2)^(2/3)"
src 20261009-0521-second-20261009-0401-quant-ea6b-96b4 check.md | grep -q '84.6%' ; chk $? "96b4: rebind 84.6% of kick wall"
src 20261011-1729-system-2c68 dossier.md | grep -q '34–790' ; chk $? "2c68: dossier range 34-790 kicks"
src 20261011-1729-system-2c68 check.md | grep -qF 'medians 72/314/705' ; chk $? "2c68: checker's intended-body medians 72/314/705"
git show "origin/claude/lab-20261011-1814-second-20261011-1729-system-2c68-b242:lab/results/20261011-1814-second-20261011-1729-system-2c68-b242/dossier.md" | grep -q 'compounds across rebinds'; chk $? "b242: carry compounds across rebinds (ungraded)"

echo "== the branch-search yield, verbatim in its sources =="
src 20261008-0234-spacex-0083 check.md | grep -qF '62.1 µs (64.5%)' ; chk $? "0083: compile 62.1 us (64.5%)"
src 20261008-0234-spacex-0083 check.md | grep -q '78.7%' ; chk $? "0083: rebind 78.7%"
src 20261008-0234-spacex-0083 check.md | grep -q '3.3–4.4×' ; chk $? "0083: measured lever 3.3-4.4x"
src 20261008-1419-components-620e check.md | grep -qF '~25× above its floor' ; chk $? "620e: fired kick ~25x above floor"
src 20261008-1419-components-620e check.md | grep -qF '(68%)' ; chk $? "620e: rebind 68%"
src 20261008-1419-components-620e check.md | grep -qF '(27%)' ; chk $? "620e: secondaries 27%"
src 20261008-1419-components-620e check2.md | grep -q 'not adoption-ready' ; chk $? "620e check2: integer evaluator not adoption-ready"
src 20261006-0437-constraint-ec9d check.md | grep -q '365–381 µs' ; chk $? "ec9d: leaver kick median 365-381 us"
src 20261006-0437-constraint-ec9d check.md | grep -q '318–356 µs' ; chk $? "ec9d: compile 318-356 us of it"
src 20261006-0437-constraint-ec9d check.md | grep -q '89–97%' ; chk $? "ec9d: compile 89-97% of the leaver rebind"
src 20261006-0437-constraint-ec9d check.md | grep -q 'Passage::compile' ; chk $? "ec9d: tail is Passage::compile"
src 20261008-1521-autoresearch-a48d check.md | grep -qF '33.1→29.5 µs' ; chk $? "a48d: kick 33.1->29.5 us"
src 20261008-1521-autoresearch-a48d check.md | grep -q 'fit_only' ; chk $? "a48d: fit_only constructor"
src 20261008-1521-autoresearch-a48d check.md | grep -q '−10.9%' ; chk $? "a48d: -10.9%"
src 20261010-1947-autoresearch-2833 check.md | grep -q '48.1→43.6' ; chk $? "2833: interleaved 48.1->43.6 us"
src 20261010-1947-autoresearch-2833 check.md | grep -q 'proper_at_event' ; chk $? "2833: proper_at_event cache"
src 20261010-1947-autoresearch-2833 check.md | grep -q '~9–10%' ; chk $? "2833: cuts ~9-10%"
src 20261006-0220-autoresearch-c3a5 check.md | grep -q '395→237 µs' ; chk $? "c3a5: ladder 395->237 us"
src 20261006-0220-autoresearch-c3a5 check.md | grep -q '405→222 µs' ; chk $? "c3a5: leaver kick 405->222 us"
src 20261007-1843-second-20261007-1801-fermi-bb60-152f check.md | grep -q '3,108 distinct rebinds' ; chk $? "152f: exact memo 0.0 on 3,108 distinct rebinds"
src 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 check.md | grep -q '9–17% of a distinct kick' ; chk $? "4cb2: shareable compile 9-17% of a distinct kick"
src 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 check.md | grep -q '1.08–1.17×' ; chk $? "4cb2: sharing buys 1.08-1.17x"
src 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 check.md | grep -q '6.3×' ; chk $? "4cb2: best tail 6.3x"
src 20261011-1729-components-b063 check.md | grep -q '~1,400–1,800×' ; chk $? "b063: kick resolver ~1,400-1,800x above floor"
src 20261011-1729-components-b063 check.md | grep -q '42–56 ns' ; chk $? "b063: information floor 42-56 ns"

echo "== the page itself =="
n=$(awk '/^## Runs/{f=1;next} f&&/^- /{c++} END{print c}' "$R/wiki/kick-jet.md")
[ "$n" = 38 ]; chk $? "page has 38 run lines (30 prior + 8 from the branch search): found $n"
missing=0
for id in $(awk '/^## Runs/{f=1;next} f&&/^- /{split($2,a,"("); print a[1]}' "$R/wiki/kick-jet.md" | grep -v missing); do
  git show-ref --verify --quiet "refs/remotes/origin/claude/lab-$id" || { echo "  no branch: $id"; missing=1; }
done
[ "$missing" = 0 ]; chk $? "every run id in the page has a branch"
awk '/^## Runs/{f=1;next} f&&/^- /{print $2}' "$R/wiki/kick-jet.md" | sort -c 2>/dev/null; chk $? "run lines are chronological"
n=$(grep -c 'gold first check, silver second' "$R/wiki/kick-jet.md")
[ "$n" = 7 ]; chk $? "7 gold-then-silver annotations (6 Runs lines + 8306's Contradictions entry): found $n"
has "$R/wiki/kick-jet.md" 'updated: 20261012-1715-second-20261012-1621-q-wiki-kick-jet-9392-56e0'; chk $? "header updated = this run"
has "$R/wiki/kick-jet.md" 'status: open'; chk $? "status stays open (closing is a checker's call)"
for id in 20261006-0220-autoresearch-c3a5 20261006-0437-constraint-ec9d 20261007-1843-second-20261007-1801-fermi-bb60-152f \
          20261008-0234-spacex-0083 20261008-1419-components-620e 20261008-1521-autoresearch-a48d \
          20261010-0306-second-20261010-0100-fermi-c11c-4cb2 20261010-1947-autoresearch-2833; do
  grep -q -- "- $id (" "$R/wiki/kick-jet.md"; chk $? "page carries the branch-search run $id"
done

echo "== the sweep itself regenerates =="
git for-each-ref refs/remotes/origin/claude/lab-20261008-0234-spacex-0083 --format='%(refname:short)' | grep -q .; chk $? "for-each-ref finds 0083 (the search the mandate instructed)"
git for-each-ref refs/remotes/origin/claude/lab-20261008-1419-components-620e --format='%(refname:short)' | grep -q .; chk $? "for-each-ref finds 620e"

echo "== summary: $ok ok, $fail fail =="
[ "$fail" = 0 ]
