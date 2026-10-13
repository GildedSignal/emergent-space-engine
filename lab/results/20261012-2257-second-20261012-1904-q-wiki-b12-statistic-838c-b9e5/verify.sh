#!/usr/bin/env bash
# verify.sh — checks the fold of 20261012-2257-second-20261012-1904-q-wiki-b12-statistic-838c-b9e5
# (second author on 20261012-1904-q-wiki-b12-statistic-838c) against the raw run branches
# (origin/claude/lab-<id>) and the reproduction scripts in work/repro/. Read-only; ~60 s.
cd "$(dirname "$0")"/../../.. || exit 1
here="$(cd "$(dirname "$0")" && pwd)"
pass=0; fail=0
ck() { # ck <label> <expected-substring> <haystack-file>
  if grep -qF -- "$2" "$3"; then echo "PASS  $1"; pass=$((pass+1))
  else echo "FAIL  $1  (wanted: $2)"; fail=$((fail+1)); fi
}
grade_of() { git show "origin/claude/lab-$1:lab/results/$1/check.md" 2>/dev/null | head -1; }
src() { git show "origin/claude/lab-$1:lab/results/$1/check.md" > /tmp/ck-$1.md 2>/dev/null
        git show "origin/claude/lab-$1:lab/results/$1/dossier.md" > /tmp/do-$1.md 2>/dev/null
        cat /tmp/ck-$1.md /tmp/do-$1.md > /tmp/all-$1.md; }

echo "== P1: grades of the prior page's runs (unchanged) =="
for g in 20261007-0528-dynamics-f819 20261007-1550-second-20261007-1420-library-240c-32f9 \
         20261009-0208-second-20261008-2206-library-73ca-618f \
         20261009-2348-second-20261009-2257-dynamics-a47e-09fb; do
  ck "gold: $g" "Grade: gold" <(grade_of "$g"); done
for s in 20261005-1404-q-plane-judge-65fd 20261006-0737-redteam-b12-stat-e5fe \
         20261007-1420-library-240c 20261008-2206-library-73ca 20261009-2257-dynamics-a47e \
         20261011-0134-scout-7567 20261011-0224-second-20261011-0134-scout-7567-cc25 \
         20261012-0138-library-060f 20261012-1227-dynamics-bd4e; do
  ck "silver: $s" "Grade: silver" <(grade_of "$s"); done
if ! git show origin/claude/lab-20261006-1545-q-b12-design-9242:lab/results/20261006-1545-q-b12-design-9242/check.md >/dev/null 2>&1; then
  echo "PASS  missing: q-b12-design-9242 has no check.md"; pass=$((pass+1)); else echo "FAIL  q-b12-design-9242 unexpectedly graded"; fail=$((fail+1)); fi

echo "== P1b: grades of the eight folded runs =="
for s in 20261008-1719-dynamics-c13b 20261010-1947-quant-9c2f 20261010-1029-library-6cfc \
         20261011-0006-dynamics-a2a5 20261011-1234-library-069c 20261012-1438-library-e9f9 \
         20261008-1419-system-2f89; do
  ck "silver: $s" "Grade: silver" <(grade_of "$s"); done
ck "gold: 20261011-2235-library-54d9" "Grade: gold" <(grade_of 20261011-2235-library-54d9)

echo "== P2a: sampled claims from the prior page (unchanged set) =="
src 20261009-0208-second-20261008-2206-library-73ca-618f
ck "618f bounded α" "bounded plants α_top 0.00–0.01 (32/32 seeds)" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
ck "618f compounding α" "compounding plants read 0.94–1.22 (32/32)" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
ck "618f v1 false-kills 21/32" "21/32 bounded plant-seeds" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
src 20261007-1550-second-20261007-1420-library-240c-32f9
ck "32f9 dead band" "−0.77" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 bounded max" "+0.586" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 leak min" "+0.037" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 autocorr" "autocorr 0.98/0.94/0.64" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
src 20261009-2348-second-20261009-2257-dynamics-a47e-09fb
ck "09fb 8/8" "caught **8/8 by R1" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb controls" "Good controls: R1 0/8 and 1/8" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb window" "T ≳ 16–32·τ_c" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
src 20261012-1227-dynamics-bd4e
ck "bd4e plane beta" "β = 0.05" /tmp/all-20261012-1227-dynamics-bd4e.md
ck "bd4e slow leak" "β = 0.176, z = 0.10" /tmp/all-20261012-1227-dynamics-bd4e.md
src 20261012-1715-redteam-b12-v2-5dcb
ck "1715 minority leak" "arrow +3.1" /tmp/all-20261012-1715-redteam-b12-v2-5dcb.md
ck "1715 fleet blip" "−13.570" /tmp/all-20261012-1715-redteam-b12-v2-5dcb.md
src 20261006-0737-redteam-b12-stat-e5fe
ck "e5fe reference" "1.408" /tmp/all-20261006-0737-redteam-b12-stat-e5fe.md
ck "e5fe noise passes" "0.157" /tmp/all-20261006-0737-redteam-b12-stat-e5fe.md
src 20261011-0224-second-20261011-0134-scout-7567-cc25
ck "cc25 horizon" "10⁴–10⁵ periods" /tmp/all-20261011-0224-second-20261011-0134-scout-7567-cc25.md
src 20261007-0528-dynamics-f819
ck "f819 fma flip" "+6.40" /tmp/all-20261007-0528-dynamics-f819.md
ck "f819 plain" "−1.26" /tmp/all-20261007-0528-dynamics-f819.md
src 20261012-0138-library-060f
ck "060f kill fired" "kill criterion was met" /tmp/all-20261012-0138-library-060f.md

echo "== P2b: sampled claims from the eight folded runs =="
src 20261008-1719-dynamics-c13b
ck "c13b bounded S2" "0.300" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b compound S2" "0.677" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b drift S2" "0.724" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b bounded z" "−1.99" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b identifiability" "|z| to 6.3" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b machine flip" "0.353 < 0.416" /tmp/all-20261008-1719-dynamics-c13b.md
ck "c13b threshold margin" "fail threshold of 12" /tmp/all-20261008-1719-dynamics-c13b.md
src 20261010-1947-quant-9c2f
ck "9c2f state-only flat" "0.079" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f leaks rise" "0.251" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f requirement leak" "2.39e-5" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f seed grey" "0.208" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f band edge" "0.229" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f OU no false positive" "−0.035" /tmp/all-20261010-1947-quant-9c2f.md
ck "9c2f pure-a blind spot" "0.030" /tmp/all-20261010-1947-quant-9c2f.md
src 20261010-1029-library-6cfc
ck "6cfc mean AUC" "0.967" /tmp/all-20261010-1029-library-6cfc.md
ck "6cfc max AUC" "0.920" /tmp/all-20261010-1029-library-6cfc.md
ck "6cfc window sizing" "E[actuations] ≳ 10" /tmp/all-20261010-1029-library-6cfc.md
src 20261011-0006-dynamics-a2a5
ck "a2a5 separation" "7.0 pooled σ" /tmp/all-20261011-0006-dynamics-a2a5.md
ck "a2a5 VR drift-blind" "0.00493" /tmp/all-20261011-0006-dynamics-a2a5.md
ck "a2a5 walk indeterminate" "0.245/0.446/0.708" /tmp/all-20261011-0006-dynamics-a2a5.md
ck "a2a5 2.6x" "2.6× the bounded amplitude" /tmp/all-20261011-0006-dynamics-a2a5.md
ck "a2a5 trend artifactual" "t = 3.7–4.1" /tmp/all-20261011-0006-dynamics-a2a5.md
ck "a2a5 long-memory boundary" "≈ T/3" /tmp/all-20261011-0006-dynamics-a2a5.md
src 20261011-1234-library-069c
ck "069c slow leak" "slow_leak 95/100" /tmp/all-20261011-1234-library-069c.md
ck "069c F med" "F med 10.4" /tmp/all-20261011-1234-library-069c.md
ck "069c amplitude-free" "0.03Q" /tmp/all-20261011-1234-library-069c.md
ck "069c phase-tied kill" "100/100 false alarms" /tmp/all-20261011-1234-library-069c.md
ck "069c guard precedence" "F ≥ fcrit" /tmp/all-20261011-1234-library-069c.md
src 20261012-1438-library-e9f9
ck "e9f9 fast detection" "2–5 orbits" /tmp/all-20261012-1438-library-e9f9.md
ck "e9f9 detune kill" "200/200 false alarms" /tmp/all-20261012-1438-library-e9f9.md
ck "e9f9 median orbit" "median orbit 9" /tmp/all-20261012-1438-library-e9f9.md
ck "e9f9 breaking condition" "A·ε ≳ k" /tmp/all-20261012-1438-library-e9f9.md
ck "e9f9 frozen h" "h=0.03391" /tmp/all-20261012-1438-library-e9f9.md
ck "e9f9 tautology" "Commensurability tautology" /tmp/all-20261012-1438-library-e9f9.md
src 20261008-1419-system-2f89
ck "2f89 one-signed" "one-signed" /tmp/all-20261008-1419-system-2f89.md
ck "2f89 exponent k8" "0.064" /tmp/all-20261008-1419-system-2f89.md
ck "2f89 worst k8" "4.97e-7" /tmp/all-20261008-1419-system-2f89.md
ck "2f89 shadow offset" "α²·C₂(x, v, t)·ds²" /tmp/all-20261008-1419-system-2f89.md
ck "2f89 what B12 reads" "C = 2J − 2K" /tmp/all-20261008-1419-system-2f89.md
src 20261011-2235-library-54d9
ck "54d9 matched-cost walk" "1,548x" /tmp/all-20261011-2235-library-54d9.md
ck "54d9 phase-lock" "phase-locks each event's truncation error" /tmp/all-20261011-2235-library-54d9.md
ck "54d9 walk slopes" "0.75–0.98" /tmp/all-20261011-2235-library-54d9.md
ck "54d9 register advice" "log-log walk slope, not a magnitude" /tmp/all-20261011-2235-library-54d9.md

echo "== P4/P5: re-run the shipped probes of 069c and 6cfc =="
cd "$here/work/repro" || exit 1
python3 b12probe.py short > /tmp/b12probe-out.txt 2>&1
ck "069c shipped script: bounded_jumps 100/100" "{'bounded': 100}" /tmp/b12probe-out.txt
ck "069c shipped script: slow_leak 95/100" "0.95" /tmp/b12probe-out.txt
python3 probe_b12stat.py > /tmp/probe6cfc-out.txt 2>&1
ck "6cfc shipped script: mean 0.967" "0.967" /tmp/probe6cfc-out.txt
ck "6cfc shipped script: max 0.920" "0.920" /tmp/probe6cfc-out.txt
ck "6cfc shipped script: T=100 blind" "0.499" /tmp/probe6cfc-out.txt

python3 detune_repro.py > /tmp/detune-out.txt 2>&1
ck "detune: commensurate A=20 no alarms" "eps=0e+00  A*eps=0.0000  false-alarms 0/200" /tmp/detune-out.txt
ck "detune: A*eps=0.002 no alarms" "eps=1e-04  A*eps=0.0020  false-alarms 0/200" /tmp/detune-out.txt
ck "detune: A*eps=0.02 kills" "eps=1e-03  A*eps=0.0200  false-alarms 200/200" /tmp/detune-out.txt
ck "detune: A=5 eps=1e-2 kills" "eps=1e-02  A*eps=0.0500  false-alarms 200/200" /tmp/detune-out.txt
cd - >/dev/null || exit 1

echo "== P3: the full-branch sweep =="
for ref in $(git for-each-ref --format='%(refname)' refs/remotes/origin/claude/lab-*); do
  n=$(git grep -i -c -E 'B12' $ref -- 'lab/results/*/dossier.md' 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')
  [ "$n" -ge 4 ] && echo "$ref" | sed 's|.*claude/lab-||'
done > /tmp/b12-gte4.txt
ck "sweep: exactly 37 dossiers with >=4 B12 mentions" "37" <(wc -l < /tmp/b12-gte4.txt)
for id in 20261008-1719-dynamics-c13b 20261010-1947-quant-9c2f 20261010-1029-library-6cfc \
          20261011-0006-dynamics-a2a5 20261011-1234-library-069c 20261012-1438-library-e9f9 \
          20261008-1419-system-2f89 20261011-2235-library-54d9 \
          20261005-1404-q-plane-judge-65fd 20261006-0737-redteam-b12-stat-e5fe \
          20261007-1420-library-240c 20261008-2206-library-73ca 20261009-2257-dynamics-a47e \
          20261011-0134-scout-7567 20261012-0138-library-060f; do
  ck "sweep: $id in the >=4 set" "$id" /tmp/b12-gte4.txt; done
for id in 20261009-0709-second-20261009-0621-system-7f97-1eca 20261008-1757-second-20261008-1719-system-0ccd-b33f \
          20261011-1814-second-20261011-1729-system-2c68-b242 20261011-0924-second-20261011-0836-spacex-0c44-c01c \
          20261008-0338-library-f045 20261004-0555-spacex-450b 20261001-2353-q-changeover-e04a 20260930-2250-taleb-3d2c \
          20261008-1419-dynamics-5cbd 20261005-2129-m-meso-motion-15d6 20261005-1540-m-macro-structure-a7f7 \
          20261006-0030-library-39a2 20261008-1150-scout-2c45; do
  if grep -qF -- "$id" "$here/wiki/b12-statistic.md"; then echo "FAIL  page leaks context-only run $id"; fail=$((fail+1))
  else echo "PASS  context-only $id not on the page"; pass=$((pass+1)); fi; done

echo "== P2c: page mechanics =="
p="$here/wiki/b12-statistic.md"
ck "header updated" "updated: 20261012-2257-second-20261012-1904-q-wiki-b12-statistic-838c-b9e5" "$p"
ck "header open" "status: open" "$p"
ck "five sections" "5" <(grep -c '^## ' "$p")
ck "23 run lines" "23" <(sed -n '/^## Runs/,$p' "$p" | grep -c '^- ')
ck "14 refuted bullets" "14" <(sed -n '/^## Refuted/,/^## /p' "$p" | grep -c '^- ')
ck "census sentence folded" "census is now complete" "$p"
if grep -qF "not yet folded in" "$p"; then echo "FAIL  dangling checker placeholder remains"; fail=$((fail+1))
else echo "PASS  no dangling placeholder"; pass=$((pass+1)); fi
ck "1715 line verbatim" "- 20261012-1715-redteam-b12-v2-5dcb (red-team, pending grade): the v2 pooled statistic passes a minority leak at the declared rate; null miscalibrated; affine assumption measured; platform-noise at the cutoff." "$p"

echo "== $pass passed, $fail failed =="
[ "$fail" -eq 0 ]
