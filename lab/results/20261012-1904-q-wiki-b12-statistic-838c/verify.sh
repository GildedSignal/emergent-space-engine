#!/usr/bin/env bash
# verify.sh — checks predictions P1–P3 of 20261012-1904-q-wiki-b12-statistic-838c
# against the raw run branches (origin/claude/lab-<id>). Read-only; ~15 s.
cd "$(dirname "$0")"/../../.. || exit 1
pass=0; fail=0
ck() { # ck <label> <expected-substring> <haystack-file>
  if grep -qF -- "$2" "$3"; then echo "PASS  $1"; pass=$((pass+1))
  else echo "FAIL  $1  (wanted: $2)"; fail=$((fail+1)); fi
}
grade_of() { git show "origin/claude/lab-$1:lab/results/$1/check.md" 2>/dev/null | head -1; }
src() { git show "origin/claude/lab-$1:lab/results/$1/check.md" > /tmp/ck-$1.md 2>/dev/null
        git show "origin/claude/lab-$1:lab/results/$1/dossier.md" > /tmp/do-$1.md 2>/dev/null
        cat /tmp/ck-$1.md /tmp/do-$1.md > /tmp/all-$1.md; }

echo "== P1: grades =="
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

echo "== P2: sampled claims =="
src 20261009-0208-second-20261008-2206-library-73ca-618f
ck "618f bounded α" "bounded plants α_top 0.00–0.01 (32/32 seeds)" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
ck "618f compounding α" "compounding plants read 0.94–1.22 (32/32)" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
ck "618f v1 false-kills 21/32" "21/32 bounded plant-seeds" /tmp/all-20261009-0208-second-20261008-2206-library-73ca-618f.md
src 20261007-1550-second-20261007-1420-library-240c-32f9
ck "32f9 dead band" "−0.77" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 bounded max" "+0.586" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 leak min" "+0.037" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 autocorr" "autocorr 0.98/0.94/0.64" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
ck "32f9 lost-ships" "lost-ships failure" /tmp/all-20261007-1550-second-20261007-1420-library-240c-32f9.md
src 20261009-2348-second-20261009-2257-dynamics-a47e-09fb
ck "09fb 8/8" "caught **8/8 by R1" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb controls" "Good controls: R1 0/8 and 1/8" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb 2^40" "integerized at 2^40" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb K2 fired" "K2: fired" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
ck "09fb window" "T ≳ 16–32·τ_c" /tmp/all-20261009-2348-second-20261009-2257-dynamics-a47e-09fb.md
src 20261012-1227-dynamics-bd4e
ck "bd4e plane beta" "β = 0.05" /tmp/all-20261012-1227-dynamics-bd4e.md
ck "bd4e 6 of 14" "6 answer, 8 no answer" /tmp/all-20261012-1227-dynamics-bd4e.md
ck "bd4e step9" "median β 0.000" /tmp/all-20261012-1227-dynamics-bd4e.md
ck "bd4e slow leak" "β = 0.176, z = 0.10" /tmp/all-20261012-1227-dynamics-bd4e.md
src 20261012-1715-redteam-b12-v2-5dcb
ck "1715 minority leak" "arrow +3.1" /tmp/all-20261012-1715-redteam-b12-v2-5dcb.md
ck "1715 fleet blip" "−13.570" /tmp/all-20261012-1715-redteam-b12-v2-5dcb.md
src 20261006-0737-redteam-b12-stat-e5fe
ck "e5fe reference" "1.408" /tmp/all-20261006-0737-redteam-b12-stat-e5fe.md
ck "e5fe noise passes" "0.157" /tmp/all-20261006-0737-redteam-b12-stat-e5fe.md
ck "e5fe shipped test" "1.094" /tmp/all-20261006-0737-redteam-b12-stat-e5fe.md
src 20261011-0134-scout-7567
ck "scout false-flags" "0.411" /tmp/all-20261011-0134-scout-7567.md
ck "scout z" "z=13.9" /tmp/all-20261011-0134-scout-7567.md
src 20261011-0224-second-20261011-0134-scout-7567-cc25
ck "cc25 echo ratio" "2.23" /tmp/all-20261011-0224-second-20261011-0134-scout-7567-cc25.md
ck "cc25 bounded" "5.15" /tmp/all-20261011-0224-second-20261011-0134-scout-7567-cc25.md
ck "cc25 horizon" "10⁴–10⁵ periods" /tmp/all-20261011-0224-second-20261011-0134-scout-7567-cc25.md
src 20261007-0528-dynamics-f819
ck "f819 fma flip" "+6.40" /tmp/all-20261007-0528-dynamics-f819.md
ck "f819 plain" "−1.26" /tmp/all-20261007-0528-dynamics-f819.md
ck "f819 null" "0.95–1.03" /tmp/all-20261007-0528-dynamics-f819.md
src 20261012-0138-library-060f
ck "060f kill fired" "kill criterion was met" /tmp/all-20261012-0138-library-060f.md
ck "060f horizon req" "discrimination horizon" /tmp/all-20261012-0138-library-060f.md

echo "== P3: classification =="
src 20261008-1150-scout-2c45
ck "scout-2c45 off-topic (SEM)" "SEM energy closure" /tmp/all-20261008-1150-scout-2c45.md
src 20261010-0920-second-20261010-0814-system-fbc6-b903
ck "fbc6 off-topic (accumulator)" "accumulator link" /tmp/all-20261010-0920-second-20261010-0814-system-fbc6-b903.md
src 20261005-1404-q-plane-judge-65fd
ck "plane-judge B12" "median exponent 1.026" /tmp/all-20261005-1404-q-plane-judge-65fd.md

echo "== $pass passed, $fail failed =="
[ "$fail" -eq 0 ]
