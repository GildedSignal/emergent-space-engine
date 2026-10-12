#!/usr/bin/env bash
# Regen for 20261012-1621-q-wiki-kick-jet-9392 (compiler run, no experiment).
# Re-extracts every load-bearing number/grade the dossier and the wiki page cite,
# from the run branches (origin/claude/lab-<id>) and main. ~5 s, no build.
set -u
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261012-1621-q-wiki-kick-jet-9392
ok=0; fail=0
chk() { if [ "$1" = "0" ]; then echo "  ok: $2"; ok=$((ok+1)); else echo "  FAIL: $2"; fail=$((fail+1)); fi; }
has() { grep -qF -- "$2" "$1"; }

echo "== adopted state on main =="
has docs/law.md 'The jet is retired (12 October)' ; chk $? "law.md retires the jet (12 October)"
has docs/law.md '20261006-1249-redteam-4978'       ; chk $? "law.md:35 cites gold 4978"
has docs/law.md '0ccd-b33f'                        ; chk $? "law.md:35 cites gold b33f"
has docs/law.md '4808-d617'                        ; chk $? "law.md:35 cites gold d617"
has docs/law.md 'the adopting run of 6 October had one checker'; chk $? "df81 flagged single-checker"
has docs/law.md "Peters' a(t) is its generator"    ; chk $? "inspiral is Peters' generator"
has docs/HANDOFF.md 'six golds refute it'          ; chk $? "HANDOFF counts six golds"
has docs/representation.md 'so a kick updates the cycle by a multiply-add'; chk $? "representation.md:67 lags (design-doc contradiction)"

echo "== grades of record (check.md vs the page) =="
declare -A G=(
 [20261006-0346-redteam-df81]='Grade: gold'
 [20261006-1249-redteam-4978]='Grade: gold'
 [20261007-0621-components-8306]='Grade: gold'
 [20261008-0338-second-20261008-0234-spacex-0083-492f]='Grade: silver'
 [20261008-1337-redteam-2040]='Grade: silver'
 [20261008-1419-second-20261008-1337-redteam-2040-9a04]='Grade: gold'
 [20261008-1521-spacex-8016]='Grade: silver'
 [20261008-1613-redteam-7922]='Grade: gold'
 [20261008-1613-second-20261008-1521-spacex-8016-6c47]='Grade: gold'
 [20261008-1719-second-20261008-1613-redteam-7922-e86c]='Grade: gold'
 [20261008-1719-system-0ccd]='Grade: silver'
 [20261008-1757-second-20261008-1719-system-0ccd-b33f]='Grade: gold'
 [20261009-0401-quant-ea6b]='Grade: silver'
 [20261009-0521-second-20261009-0401-quant-ea6b-96b4]='Grade: gold'
 [20261009-1858-redteam-075b]='Grade: silver'
 [20261009-1936-second-20261009-1858-redteam-075b-a059]='Grade: gold'
 [20261010-0541-components-8c81]='Grade: silver'
 [20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2]='Grade: silver'
 [20261010-0920-quant-30e1]='Grade: silver'
 [20261010-1706-second-20261010-1544-system-97ce-b18f]='Grade: gold'
 [20261010-2141-system-eea5]='Grade: silver'
 [20261011-1456-components-f797]='Grade: silver'
 [20261011-1729-system-2c68]='Grade: silver'
 [20261011-2235-redteam-6164]='Grade: gold'
 [20261011-2306-second-20261011-2235-redteam-6164-ee08]='Grade: gold'
 [20261012-0036-second-20261011-2306-system-3367-1e74]='Grade: gold'
 [20261012-0358-components-fa08]='Grade: silver'
 [20261012-1117-redteam-4808]='Grade: silver'
 [20261012-1227-second-20261012-1117-redteam-4808-d617]='Grade: gold'
)
for id in "${!G[@]}"; do
  line=$(git show "origin/claude/lab-$id:lab/results/$id/check.md" 2>/dev/null | grep -m1 '^Grade:')
  [ "$line" = "${G[$id]}" ]; chk $? "$id check.md: $line"
done
# single-checker golds standing silver (the six of P2, minus the standing golds)
n_gold_check=0
for id in 20261006-0346-redteam-df81 20261007-0621-components-8306 20261008-1613-redteam-7922 \
          20261008-1719-second-20261008-1613-redteam-7922-e86c 20261009-0521-second-20261009-0401-quant-ea6b-96b4 \
          20261010-1816-system-67f2 20261011-2235-redteam-6164; do
  git show "origin/claude/lab-$id:lab/results/$id/check.md" 2>/dev/null | grep -q '^Grade: gold' && n_gold_check=$((n_gold_check+1))
done
[ "$n_gold_check" = 7 ]; chk $? "7 runs have single-checker gold grades (df81,8306,7922,e86c,96b4,67f2,6164): found $n_gold_check"
git show "origin/claude/lab-20261011-1814-second-20261011-1729-system-2c68-b242:lab/results/20261011-1814-second-20261011-1729-system-2c68-b242/check.md" >/dev/null 2>&1
[ $? != 0 ]; chk $? "b242 has no check.md (missing, ungraded)"

echo "== sampled page numbers appear verbatim in their sources =="
src() { git show "origin/claude/lab-$1:lab/results/$1/$2" 2>/dev/null; }
src 20261006-1249-redteam-4978 dossier.md | grep -q '2 808 rad' ; chk $? "4978: separatrix error exceeds the cycle (2808 rad)"
src 20261008-1419-second-20261008-1337-redteam-2040-9a04 dossier.md | grep -q '15/8' ; chk $? "9a04: E-axis constant 15/8"
src 20261009-1936-second-20261009-1858-redteam-075b-a059 dossier.md | grep -q '≲ 0.05' ; chk $? "a059: skin boundary <=0.05 (unicode)"
src 20261008-1757-second-20261008-1719-system-0ccd-b33f dossier.md | grep -q '2.75×' ; chk $? "b33f: 2.75x on the kick median"
src 20261010-1706-second-20261010-1544-system-97ce-b18f dossier.md | grep -qF '1.5×10⁻³ median over 24 game-years' ; chk $? "b18f: |da|/a 1.5e-3 over 24 game-years"
src 20261010-1706-second-20261010-1544-system-97ce-b18f dossier.md | grep -q '0.0160 compiles/kick' ; chk $? "b18f: 0.0160 compiles/kick"
src 20261010-1706-second-20261010-1544-system-97ce-b18f dossier.md | grep -q '1.80×' ; chk $? "b18f: 1.80x belt wall"
src 20261012-0036-second-20261011-2306-system-3367-1e74 dossier.md | grep -qF '1.3–1.5× (made, player) and 3.0–3.8× (leavers)' ; chk $? "1e74: carry ceiling 1.3-1.5x / 3.0-3.8x"
src 20261012-0036-second-20261011-2306-system-3367-1e74 dossier.md | grep -q '26 µs' ; chk $? "1e74: ~26 us machinery floor"
src 20261012-1227-second-20261012-1117-redteam-4808-d617 dossier.md | grep -qF 'μ = p − p_crit(e) ≤ 0.3' ; chk $? "d617: margin mu<=0.3"
src 20261012-1227-second-20261012-1117-redteam-4808-d617 dossier.md | grep -q '30–40%' ; chk $? "d617: band fed 30-40%"
src 20261011-2306-second-20261011-2235-redteam-6164-ee08 dossier.md | grep -q 'χ ∈ {0.5, 0.9, 0.998}' ; chk $? "ee08: Kerr spins"
src 20261011-2306-second-20261011-2235-redteam-6164-ee08 dossier.md | grep -q '15/8' ; chk $? "ee08: T-channel 15/8"
src 20261012-0358-components-fa08 check.md | grep -q '270×' ; chk $? "fa08: rebind ~270x above floor"
src 20261012-0358-components-fa08 check.md | grep -q '7–13×' ; chk $? "fa08: jet closes to 7-13x"
src 20261008-1613-second-20261008-1521-spacex-8016-6c47 check.md | grep -q '92.5–95.1%' ; chk $? "6c47: memo hits 92.5-95.1%"
src 20261008-1613-second-20261008-1521-spacex-8016-6c47 check.md | grep -q '0.55 µs' ; chk $? "6c47: memo hit 0.55 us"
src 20261008-1719-second-20261008-1613-redteam-7922-e86c check.md | grep -q '543·(1−e²)^(2/3)' ; chk $? "e86c: horizon 543*(1-e^2)^(2/3)"
src 20261009-0521-second-20261009-0401-quant-ea6b-96b4 check.md | grep -q '84.6%' ; chk $? "96b4: rebind 84.6% of kick wall"
src 20261011-1729-system-2c68 dossier.md | grep -q '34–790' ; chk $? "2c68: median 34-790 kicks"
git show "origin/claude/lab-20261011-1814-second-20261011-1729-system-2c68-b242:lab/results/20261011-1814-second-20261011-1729-system-2c68-b242/dossier.md" | grep -q 'compounds across rebinds'; chk $? "b242: carry compounds across rebinds (ungraded)"

echo "== the page itself =="
n=$(grep -c '^- ' "$R/wiki/kick-jet.md")
[ "$n" = 42 ] || n=$(awk '/^## Runs/{f=1;next} f&&/^- /{c++} END{print c}' "$R/wiki/kick-jet.md")
[ "$n" = 30 ]; chk $? "page has 30 run lines (29 graded + b242): found $n"
missing=0
for id in $(awk '/^## Runs/{f=1;next} f&&/^- /{split($2,a,"("); print a[1]}' "$R/wiki/kick-jet.md" | grep -v missing); do
  git show-ref --verify --quiet "refs/remotes/origin/claude/lab-$id" || { echo "  no branch: $id"; missing=1; }
done
[ "$missing" = 0 ]; chk $? "every run id in the page has a branch"
has "$R/wiki/kick-jet.md" 'updated: 20261012-1621-q-wiki-kick-jet-9392'; chk $? "header updated = this run"
has "$R/wiki/kick-jet.md" 'status: open'; chk $? "status stays open (closing is a checker's call)"

echo "== summary: $ok ok, $fail fail =="
[ "$fail" = 0 ]
