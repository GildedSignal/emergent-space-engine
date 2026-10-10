Grade: silver

**Abstract.** The named experiment ran; it cures the disease and fails the
letter. The decisive config regenerates exactly (144.71/440.87 deliveries,
per-ring [114.7, 149.2, 162.1, 14.9], all six error snapshots identical;
seed 20261010), and the integer partition is exact under independent
re-derivation (9/40/147/588/240 leaves, uniform). The v2 compounding leak is
dead (max +16% over a 3× horizon vs ×79). But boundedness fails: past the
light-cone fill (side 16, T=44 > box/2, warm, two independent samples) the
deferral error keeps walking diffusively (median ×2.9 per 5.5×, ~t^0.5) —
"near-stationary" is a window artifact — and cost is O(log N) at ~11×. The
renewal-overshoot floor is real; its constant is misstated (0.042; measured
0.126). Adopt the partition as the correct bookkeeping; gold needs the walk
bounded.

## Reasons

**1. Reproduction.** `python3 shells.py` in a clean tree (patch.diff empty):
both error-bearing configs regenerated every digit of the shipped log/JSON —
`s32_q1_T12_dip_pre` (counters, flush-by-level, all six error snapshots;
wall 255 s) and `s32_q1_T12_sca_pre` (78.8/25.2→98.5/33.42, the P4 scalar
control; wall 256 s). The fine-q and s16 configs did not finish inside the
45-min window; their numbers reconcile arithmetically with the shipped JSON
(totals 425.0/585.6, exponent 0.231, ratios 9.6×/28×, fine-q cost ×4.08,
growth +15.7%/+17.6%, p99/med 1.06), and the scalar counters were anyway
code-path identical to config 1's (same RNG stream, only `p` zeroed).
Dossier arithmetic verified throughout; the out/ files are unmodified (md5
checked before and after my visit). Freeze order is not provable from mtimes
(results 11:31 < shells.py 11:32 < predictions.md 11:34), but the
bit-identity of both configs shows the post-run script edit was non-numeric,
and the pre-registered *misses* (12·4^l vs the true 40·4^l annulus; ≤25q vs
43–60q; ×10 vs ×4.1) are not writable after seeing the run — credible
pre-registration, honestly graded by the author.

**2. The canonical claim holds independently.** My own implementation of the
l*-table: exact one-channel cover at both sizes, member counts 9/40/147/588/240
(side 32) and 9/40/147/60 (side 16), uniform over sources, and the member
geometry behind θ_l = q·(1.5·c_l)² is sound (nearest member-leaf point ≥
1.5·c_l at every level, tight at l=0). Integer, no shared code. CONFIRMED.

**3. Adversarial cases (mine).**
- *Horizon, their wrong-maker #1, now measured.* Side 16, warm (T_pre=45):
  T=32 gives median 22.3→55.3q (t=4→32); T=44 gives median 24.9→72.3q, max
  80.6→165.2q (t=8→44), still growing past complete light-cone fill
  (t=32→44: med 56.0→72.3). Two independent event samples agree at
  overlapping times (±8%): a diffusive walk (~t^0.5), not a plateau. The
  shipped side-32 window (T=12) lies entirely inside the fill transient
  (fill = 64); the t=8–12 max plateau (57.7→57.2) that reads as stationary is
  a window coincidence. The compounding kill still stands — the error class
  changed from multiplicative (v2 ×79 per 6× window) to additive diffusion
  (×2.9 per 5.5×) — but "bounded, near-stationary" is refuted at any horizon
  covering the fill.
- *The overshoot constant.* Measured mean overshoot at the actual θ_l:
  0.11–0.14 at every level; E[s²]/2E[s] = 0.126 (closed form (a+b)/4 for
  log-uniform [0.005, 0.5]). The dossier's 0.042 is wrong by 3×. The stated
  floor "q ≈ 0.004" matches the *correct* constant (θ₀ = 36q = 0.126 → q =
  0.0035), and the fine-q absolute errors (0.49–0.52 at q=0.001 vs
  0.43–0.60 at q=0.01) confirm the floor's mechanism. Constant wrong, floor
  right.
- *Strength-law extremes (asserted, not measured, in the dossier).* Lighter
  law (E[s²]/2E[s] = 0.033): max 10–14q, med 3.6–4.6q — the constant tracks
  the overshoot ratio (0.26 predicted vs 0.23 observed), non-compounding.
  Heavier law (0.2497, mean ×4.2): max 188–215q, med ~53q, flush cost ×3.1 —
  still non-compounding over t ≤ 6. The constant is a property of the
  strength law, as claimed; the walk at horizon is the disease.

**4. Novelty.** FMM is long-standing prior art in the repo's own record
(register: Barnes–Hut rejected for FMM; "bounded FMM" in the approved build
plan; never built — H0195/H0196). The parent scout run owns gravity-as-news;
its v3 member-residue accumulator double-counted and died. New here: the
exact per-(leaf, ring) partition with an integer proof, member quanta, and
the renewal-overshoot floor. No HISTORY entry covers this lineage (it lives
on lab branches).

**5. Goal fit.** The lineage attacks R5's "light cone keeps growing". On
PRINCIPLES 13 ("Errors never compound"): satisfied in the multiplicative
sense; the surviving diffusive walk is precisely the error-*type* distinction
the principles demand ("types of errors and not just errors", OC#42), and the
dossier's headline under-names it. Principles 5/6 quoted by the author apply
as stated. Adoption cost: (A, p) per (leaf, ring) plus the partition table,
~11× deliveries, O(log N) per body, floored by the overshoot — a real trade,
correctly priced except for the constant error above.

## The one experiment to gold

Bound the walk: carry the quadrupole in the member accumulator (or
re-centre/anti-bias the flush) and show, at T ≥ box/2 (fill complete), warm,
two seeds, that the deferral error is genuinely stationary at ≤ c·L·q with
the θ = κ·q·d² dial measured. If no moment order bounds it, the premise
"bookkeeping alone fixes quantum-gated accumulation" dies — a different,
equally reportable result.

## What the author missed

- The stationarity claim is a window artifact; wrong-maker #1 was measurable
  at side 16 in ~2 min per run and decides the headline. The dossier leads
  with "bounded and near-stationary"; only the caveats carry the walk.
- The overshoot constant 0.042 is wrong (0.126 = (a+b)/4); the stated floor
  silently matches the right value — an unchecked load-bearing number.
- Every shipped side-32 error number lives inside the filling transient
  (T=12 vs fill=64): the "warm" construction warmed the accumulators, not
  the arrival field.
- The L in "3Lq/9Lq" is the scout's 6-level count; this scheme's ring count
  is 4 — the letter's normalization mixes hierarchies.
- Strength-law extremes were reasoned but never run (both directions
  measured here).
