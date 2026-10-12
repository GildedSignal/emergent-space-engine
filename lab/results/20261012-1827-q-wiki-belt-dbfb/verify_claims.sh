#!/usr/bin/env bash
# verify_claims.sh — every number cited on lab/results/<id>/wiki/belt.md must appear,
# verbatim, in the cited run's check.md or dossier.md on its claude/lab-<id> branch.
# Usage: bash verify_claims.sh   (from this run folder; read-only; < 1 minute)
set -u
PASS=0; FAIL=0
ck() { # ck "<label>" <run-id> <file> <fixed-string>
  local label="$1" id="$2" f="$3" pat="$4"
  if git show "origin/claude/lab-$id:lab/results/$id/$f" 2>/dev/null | grep -qF -- "$pat"; then
    PASS=$((PASS+1)); printf 'ok   %-58s %s:%s\n' "$label" "$id" "$f"
  else
    FAIL=$((FAIL+1)); printf 'MISS %-58s %s:%s  (wanted: %s)\n' "$label" "$id" "$f" "$pat"
  fi
}

# --- birth program, wiring, gate ---
ck "0.126 bits/body"            20261004-1525-components-98bc check.md "0.126 bits/body"
ck "16,456 bytes total"         20261004-1525-components-98bc dossier.md "16,456 bytes"
ck "1.3e-4 bits/body at 1e9"    20261004-1525-components-98bc check.md "1.3×10⁻⁴ at 10⁹"
ck "157.4 bits packed / 19.7GB" 20261004-1525-components-98bc dossier.md "19.7 GB at 10⁹"
ck "16 bits/body in 11-12 orbits" 20261006-1354-dynamics-04d7 dossier.md "orbit 11–12"
ck "birth 31 B / 32 B at 1e9"   20261006-2240-b-belt-wire-a733 dossier.md "birth 31 B for info 31 B"
ck "32 B at 1e9"                20261006-2240-b-belt-wire-a733 dossier.md "bytes at 1e9: 32 B"
ck "9.7 B per scar, 17 ns"      20261006-2240-b-belt-wire-a733 dossier.md "17 ns per regenerated body"
ck "11.4% scarred at 1e-2"      20261006-2240-b-belt-wire-a733 dossier.md "11.4% are scarred, 9.7 B"
ck "B18b FAIL->PASS five runs"  20261006-2240-b-belt-wire-a733 dossier.md "PASS on all five frozen runs"
ck "15% tail crush passes"      20261005-1404-redteam-b18-belt-d3e4 check.md "15% crush"
ck "1/32 periapsis corridor"    20261005-1404-redteam-b18-belt-d3e4 check.md "1/32 periapsis corridor"
ck "4 MB table, 255x gold"      20261005-1404-redteam-b18-belt-d3e4 check.md "4 MB one-level quantile table (255×"

# --- program death and absorption ---
ck "saturates ~40 bits/body"       20261006-1354-dynamics-04d7 dossier.md "saturates (λ shear wraps"
ck "rekey each ~50-100 orbits"     20261008-0458-system-5a2c dossier.md "~50–100 orbits"
ck "dies within ~1e2 orbits"       20261008-0458-system-5a2c dossier.md "~10² orbits"
ck "reband 3.5-4.5 bits/body"      20261008-0615-second-20261008-0458-system-5a2c-af34 dossier.md "3.5–4.5 bits/body"
ck "crossover mu_b 1.7e-18"        20261010-1816-components-6273 dossier.md "μ_b ≈ 1.7×10⁻¹⁸"
ck "1.4-38 bits per encounter"     20261010-1816-components-6273 dossier.md "1.4–38 bits"
ck "0.3-3.2 GB stirred 1e9"        20261010-1816-components-6273 dossier.md "0.3–3.2 GB"

ck "secular scars ~6 bits, 2 orb" 20261007-0933-scout-23c8 check.md "~6 bits/body (q=1e-6) within 2 orbits"
ck "0.0 of 41.45 bits at q24"    20261007-0711-second-20261007-0621-scout-6e10-ab9d check.md "41.45 bits"
ck "min |dz| = 43x quantum"      20261007-0711-second-20261007-0621-scout-6e10-ab9d check.md "43× the quantum"
ck "4.8-5.2 GB/1e9 q24, 3.0 q16" 20261007-0711-second-20261007-0621-scout-6e10-ab9d check.md "4.8–5.2 GB/10⁹"
ck "3.0 GB (q16)"                20261007-0711-second-20261007-0621-scout-6e10-ab9d check.md "3.0 GB (q16)"
ck "0.6GB+37MB/epoch 8x optimistic" 20261007-0711-second-20261007-0621-scout-6e10-ab9d check.md "≈8× optimistic"

# --- the secular field ---
ck "residual 108.71 of 108.77"   20261007-1106-second-20261007-1032-taleb-ab03-0263 check.md "108.71 of 108.77 bits"
ck "twin E response 40-112x"     20261007-1106-second-20261007-1032-taleb-ab03-0263 check.md "40–112× too small"
ck "|da| saturates 1.8e-3 AU"    20261007-1106-second-20261007-1032-taleb-ab03-0263 dossier.md "1.8×10⁻³ AU"
ck "clone divergence 7.8 bits"   20261007-1106-second-20261007-1032-taleb-ab03-0263 dossier.md "7.8 bits"
ck "rings 14.5%, LL 0%, 50% bar" 20261006-0737-q-secular-v2-5f69 check.md "14.5%, LL 0% against the 50% bar"
ck "008e truth: Saturn erased"   20261005-2231-q-secular-008e check.md "erases Saturn's kick"
ck "23.7 kyr truth horizon"      20261005-2231-q-secular-008e check.md "23.7 kyr"
ck "chaos 5.75% at mu 9.54e-4"   20261006-0916-redteam-e84d check.md "5.75% (9.54e-4)"
ck "0.125% non-resonant band"    20261006-0916-redteam-e84d check.md "0.125%"
ck "0.75% at mu 1e-6"            20261006-0916-redteam-e84d check.md "0.75% (μ=1e-6)"
ck "28.6% at mu 1e-2"            20261006-0916-redteam-e84d check.md "28.625% (1e-2)"
ck "no belt-with-planet scene"   20261006-0916-redteam-e84d check.md "B15 has no belt, B17 two single resonances"

# --- conjunction calendars ---
ck "k_err median 5.5, threshold 2" 20261008-1947-library-d583 check.md "median 5.5"
ck "replication median 19"          20261008-1947-library-d583 check.md "median 19"
ck "kill threshold 2"               20261008-1947-library-d583 check.md "kill threshold 2"
ck "Lambda closed form dead"        20261010-0352-second-20261010-0306-spacex-acb2-7b82 check.md "1.05→1.81→2.01"
ck "Lambda(1e-4)=0.525 floor"       20261010-0352-second-20261010-0306-spacex-acb2-7b82 check.md "0.525"

# --- what the belt costs ---
ck "flux ratios 1.05-1.47"       20261007-0933-second-20261007-0842-fermi-fc22-a7d0 check.md "1.05–1.47"
ck "N^1.07, m^1.13"              20261007-0933-second-20261007-0842-fermi-fc22-a7d0 check.md "N^1.07, m^1.13"
ck "planar 209 MB/game"          20261007-0933-second-20261007-0842-fermi-fc22-a7d0 check.md "209 MB/game"
ck "3-D 18 KB"                   20261007-0933-second-20261007-0842-fermi-fc22-a7d0 check.md "18 KB"
ck "31 writes/s at 1e9"          20261007-0933-second-20261007-0842-fermi-fc22-a7d0 check.md "31 writes/s"
ck "p99/mean 3.3, max/mean 5.7"  20261009-1649-dynamics-ec3a check.md "3.3, max/mean ≈ 5.7"
ck "p99-uniform wastes ~70%"     20261009-1649-dynamics-ec3a check.md "wastes ~70%"
ck "librators not concentration" 20261009-1649-dynamics-ec3a check.md "librators) not concentration"
ck "(E,L) diffusive below range" 20261011-2306-dynamics-0b04 check.md "diffusive below q ≈ element range"
ck "top-5% ~7%"                  20261011-2306-dynamics-0b04 check.md "top-5% ≈ 7%"
ck "classifier rho 0.74 vs -0.05" 20261011-2306-dynamics-0b04 check.md "ρ = 0.74"
ck "resonance distance rho -0.05" 20261011-2306-dynamics-0b04 check.md "ρ = −0.05"
ck "e0=0.2 NaNs"                 20261011-2306-dynamics-0b04 check.md "e0=0.2 is more chaotic but the instrument NaNs"

# --- phase lock ---
ck "synodic sweep med 459 cells" 20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "med 459 cells/ship/P_p"
ck "x16.0 per 4 bits"            20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "×16.0 per 4 bits"
ck "0.55 key updates/P_p"        20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "0.55 key updates/P_p"
ck "linear to 1200 P_p"          20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "linear to 1200 P_p"
ck "20.7 bits/ship at 100 P_p"   20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "20.7 bits/ship at 100 P_p"
ck "22.1 at 1200 P_p"            20261011-0006-second-20261010-2314-taleb-6baf-2b8e check.md "≈22.1 at 1200"

echo
echo "verify_claims: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]
