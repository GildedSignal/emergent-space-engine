#!/usr/bin/env bash
# extract.sh — regenerates the evidence behind wiki/high-gamma-clock.md (run 20261012-1621-…-42b5).
# Every number quoted on the page is re-extracted here, as a fixed string, from the cited
# run's own record (check.md / check2.md / dossier.md on its immutable claude/lab-<id> branch).
# Also re-runs the full-branch keyword triage that decided no on-topic run was missed.
set -u
root="$(git rev-parse --show-toplevel)" || { echo "not a git tree" >&2; exit 1; }
cd "$root"
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/work"
ex="$here/work/extract.txt"
: > "$ex"

ON=(20261011-1600-inversion-e128 20261009-2043-scout-a1a4 20261008-1947-redteam-efb2 20261008-2031-second-20261008-1947-redteam-efb2-4d7e)

# --- 1. the four on-topic branches exist -------------------------------------
for id in "${ON[@]}"; do
  if git rev-parse --verify -q "origin/claude/lab-$id" >/dev/null; then
    echo "OK   ref origin/claude/lab-$id" >> "$ex"
  else
    echo "MISS ref origin/claude/lab-$id" >> "$ex"
  fi
done

# check <run-id> <file> <label> <fixed string>
check() {
  local id=$1 file=$2 label=$3 pat=$4
  if git show "origin/claude/lab-$id:lab/results/$id/$file" 2>/dev/null | grep -qF -- "$pat"; then
    printf 'OK   %s | %s | %s\n' "$id" "$label" "$pat" >> "$ex"
  else
    printf 'MISS %s | %s | %s\n' "$id" "$label" "$pat" >> "$ex"
  fi
}

E=20261011-1600-inversion-e128
S=20261009-2043-scout-a1a4
R=20261008-1947-redteam-efb2
R2=20261008-2031-second-20261008-1947-redteam-efb2-4d7e

# e128 — the clock
check $E check.md  grade-gold            "Grade: gold"
check $E check2.md grade2-gold           "Grade: gold"
check $E check2.md saturation            "dt/dτ → 2.0000 while γ → 1761"
check $E check.md  tail                  "dt/dτ tail = 1.96, 1.96, 2.00"
check $E check2.md mechanism             "first order in v²"
check $E check.md  deficit-green         "deficit γ/γ_ext = 3.72"
check $E dossier.md deficit-curve        "1.06 at γ 2.2"
check $E dossier.md deficit-freeze       "87 at γ 1262, 112 at the freeze"
check $E check2.md tau-vs-sr             "τ = 4.206e9 at t = 7.742e9"
check $E check2.md rate-dial             "disagree by ~630×"
check $E check.md  gamma-pred            "3.8e−3"
check $E check2.md register              "−64 throughout"
check $E dossier.md register-pt          "−2⁶³ = −c²/2"
check $E check.md  register-viol         "6.4e−11"
# e128 — the wall and the gate
check $E dossier.md wall-l15             "first refusal at t = 8.45e9, γ = 1761.4"
check $E check.md  wall-l12              "γ_wall 1791.4"
check $E check2.md wall-l13              "wall at γ 1802.7"
check $E check.md  leave-factor          "137× short of the leave"
check $E check2.md k-word                "k = 1/(1+e) falls toward 2⁻²⁸"
check $E check2.md k-word-check          "48-bit word"
check $E check.md  gate-crossing         "β 0.2474, ratio 1.0303"
check $E check.md  gate-27x              "27.2× off"
check $E dossier.md gate-newtonian       "saturates at c²/2"
check $E check2.md scheduler             "events/clock.rs"
check $E check2.md l5-control            "0.59%"
# scout — the tube covers the regime
check $S check.md  grade-silver          "Grade: silver"
check $S dossier.md exactness            "1.3×10⁻¹⁰"
check $S dossier.md readout-cost         "3.1 µs/sample"
check $S dossier.md compile-cost         "compile 0.55 ms"
check $S dossier.md panels-log           "∝ ln(1/δ)"
check $S dossier.md case-gamma2000       "E γ=2000"
check $S dossier.md case-photon          "G photon b=0.9b_crit"
check $S dossier.md horizon              "finite and smooth in Eddington–Finkelstein/Kerr–Schild time"
# redteam pair — the frame survives
check $R check.md  grade-silver          "Grade: silver"
check $R2 check.md grade2-silver         "Grade: silver"
check $R dossier.md solver-b             "never fails and never picks a wrong root at any γ ≤ 2×10⁶"
check $R2 check.md solver-accel          "γ=2808"
check $R dossier.md observer-frame-wrong "6156–6353 of 6336"
check $R2 check.md observer-frame-count  "12 700"
check $R dossier.md ulp-slope            "ulp = 0.0156 s"
check $R dossier.md alias-inside-envelope "≈1.9×10³ for β_o = 0.01"
check $R2 check.md convention            "convention-carried"

# --- 3. no missed on-topic run: full-branch triage ---------------------------
{
  echo "--- branch triage (all origin/claude/lab-*)"
  n=0
  for r in $(git for-each-ref refs/remotes/origin/claude/lab-* --format='%(refname:short)'); do
    n=$((n+1))
  done
  echo "total-branches $n"
  for r in $(git for-each-ref refs/remotes/origin/claude/lab-* --format='%(refname:short)'); do
    id=${r#origin/claude/lab-}
    hits=$( (git show "$r:lab/results/$id/check.md" 2>/dev/null; git show "$r:lab/results/$id/dossier.md" 2>/dev/null) \
      | grep -ciE 'inversion-e128|γ ?1,?761|dt/dτ|proper.time saturat|gate C1|Q48')
    [ "$hits" -gt 0 ] && echo "$hits $id"
  done | sort -rn
} >> "$ex"

miss=$(grep -c '^MISS' "$ex" || true)
echo "misses: $miss"
cat "$ex"
[ "$miss" -eq 0 ]
