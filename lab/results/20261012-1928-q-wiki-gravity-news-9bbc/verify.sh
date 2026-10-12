#!/usr/bin/env bash
# verify.sh — every number quoted on the compiled page / dossier, re-derived
# from the immutable run branches (origin/claude/lab-<id>) and the tree.
# Usage: bash verify.sh   (from the run folder; needs the lab git remote refs)
set -u
REPO=$(git rev-parse --show-toplevel)
PASS=0; FAIL=0
check() { # id file pattern
  local id=$1 file=$2 pat=$3
  if git -C "$REPO" show "origin/claude/lab-$id:lab/results/$id/$file" 2>/dev/null \
       | LC_ALL=C grep -qF -- "$pat"; then
    PASS=$((PASS+1)); echo "ok   $id $file :: $pat"
  else
    FAIL=$((FAIL+1)); echo "MISS $id $file :: $pat"
  fi
}
G=20261008-1947-second-20261008-1859-scout-141c-3186
# --- gold 20261008-1947 (check.md + dossier.md) ---
check $G check.md   "grows ∝ R² (1.957)"
check $G check.md   "Gain 358× at 1024 AU"
check $G check.md   "step 2²², quantum 2⁻⁷⁴"
check $G dossier.md "24,525 kicks"
check $G dossier.md "Q_engine = 2⁻¹¹² tick⁻¹"
check $G dossier.md "1.93×10⁻³⁴"
check $G dossier.md "−0.973"
check $G dossier.md "970 AU tail"
check $G dossier.md "5×10⁴ arrivals per 33 ms frame"
check $G check.md   "md5-identical"
check $G dossier.md "0.52–0.74"
# --- cursor silver 20261005-1540 ---
C=20261005-1540-q-gravity-cursor-05b0
check $C check.md "7,203,000 kicks, 0 mismatches"
check $C check.md "tests/kick = 1 + arrivals"
check $C check.md "ns0 unbound 5.05 orbits, dE 310"
# --- build silver 20261006-1738 ---
B=20261006-1738-b-news-gravity-e300
check $B check.md "20000/20000"
check $B check.md "10751 kicks"
check $B check.md "2064 kicks"
check $B check.md "Retarded differs everywhere"
# --- rings silver 20261008-0148 ---
S=20261008-0148-system-098e
check $S check.md "1.04e-6"
check $S check.md "8.8e-7"
check $S check.md "max 68.6"
check $S check.md "max 3.0"
check $S check.md "2e4×"
# --- toy silver 20261008-1859 ---
T=20261008-1859-scout-141c
check $T check.md "log₂R"
check $T check.md "×4 per octave exactly"
# --- lead 20261009-0709 ---
L=20261009-0709-scout-5b6a
check $L check.md "4.3×10⁻¹⁷"
check $L check.md "force scale 1.16"
check $L check.md "3.1×10⁴ events/orbit"
check $L check.md "8425→8064"
# --- gated silver 20261010-0920 ---
E=20261010-0920-scout-e5f5
check $E check.md "40→48 deliveries/body/time"
check $E check.md "2.1×10⁴ at 10⁶"
check $E check.md "228q"
check $E check.md "10¹⁸ cursor words"
# --- multipole silver 20261010-1544 ---
M=20261010-1544-scout-c4cb
check $M check.md "256 B/system/P_ref"
check $M check.md "measured 16×"
check $M check.md "ℓ=1 fails on the energy rule at every rate"
check $M check.md "2.5e-3"
# --- tree: law.md's "not built" line ---
# --- rings second (gold) 20261008-0234 ---
B2=20261008-0234-second-20261008-0148-system-098e-bd06
check $B2 check.md "never early on 3,280/3,280"
check $B2 check.md "1.6e-6 at β=0.33"
check $B2 check.md "5.3e-2 yr"
check $B2 check.md "82.7×/662×"
check $B2 check.md "9.2×/74×"
check $B2 check.md "≤3.02"
# --- hierarchical cap scout + second (OC#50) ---
S3=20261007-1918-scout-3da3
check $S3 check.md "1.4×10¹²"
check $S3 check.md "one-news-per-source-orbit cap"
check $S3 check.md "ε≳1e-3"
S4=20261007-2002-second-20261007-1918-scout-3da3-3fb7
check $S4 check.md "3.13×10⁵/unit"
check $S4 check.md "1.42×10¹²"
check $S4 check.md "2.4–3.9×"
# --- news-read physics redteam + rung second ---
RA=20261009-0521-redteam-93a4
check $RA check.md "3.3e-7 at μ=1e-3"
check $RA check.md "slope 2.0"
check $RA check.md "4.12e-5"
E9=20261009-0621-second-20261009-0521-redteam-93a4-e93c
check $E9 dossier.md "μ-slope 2.01"
check $E9 dossier.md "3.32e-7 over 300 reader orbits"
check $E9 dossier.md "7.73e-4 at 100"
if ! git -C "$REPO" show "origin/claude/lab-$E9:lab/results/$E9/check.md" >/dev/null 2>&1; then
  PASS=$((PASS+1)); echo "ok   e93c :: no check.md (checker 429, unchecked)"
else
  FAIL=$((FAIL+1)); echo "MISS e93c :: check.md exists after all"
fi
# --- retention silver + accumulator gold ---
F6=20261010-0814-system-fbc6
check $F6 check.md "λ·min(r_q,R)/c"
check $F6 check.md "R/r_q"
B9=20261010-0920-second-20261010-0814-system-fbc6-b903
check $B9 check.md "1,317,170 → 1,617 live"
check $B9 check.md "8,341"
check $B9 dossier.md "z up to +348"
check $B9 dossier.md "0.70·λ_tot"
check $B9 check.md "173,860"
# --- partition second (boundedness fails) ---
O3=20261010-1029-second-20261010-0920-scout-e5f5-0c3b
check $O3 check.md "+16% over a 3× horizon vs ×79"
check $O3 check.md "O(log N) at ~11×"
check $E9 dossier.md "slope 1.01"
check $E9 dossier.md "five orders"
check $E9 dossier.md "2.04 mutual Hill radii"
check $M check.md "1.6e-2 inside the cell"
check $F6 check.md "100×"
check $F6 check.md "+100/frame"
check $F6 check.md "+800/frame"
check $B9 check.md "1.35"
check $S3 check.md "3.6×10⁷ higher"
if LC_ALL=C grep -qF "Not built: the plane's kicks are instantaneous" "$REPO/docs/law.md"; then
  PASS=$((PASS+1)); echo "ok   docs/law.md :: Not built (kicks instantaneous)"
else
  FAIL=$((FAIL+1)); echo "MISS docs/law.md :: Not built (kicks instantaneous)"
fi
# --- VOID twin has no check.md/dossier ---
if ! git -C "$REPO" show "origin/claude/lab-20261006-1931-second-20261006-1738-b-news-gravity-e300-e1ac:lab/results/20261006-1931-second-20261006-1738-b-news-gravity-e300-e1ac/dossier.md" >/dev/null 2>&1; then
  PASS=$((PASS+1)); echo "ok   e1ac :: no dossier (never started)"
else
  FAIL=$((FAIL+1)); echo "MISS e1ac :: dossier exists after all"
fi
echo "----"
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]
