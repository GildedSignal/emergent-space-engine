Grade: silver

**Abstract.** The angular in-band window (|Δλ| ≤ 2.5·2·e_hi + drift, by range search over sorted
longitudes) makes the unified certificate exact on all six recorded scenes (eval cut vs cone: F1
109×, TROJANC 7.5×, CONVOY 2.7×, X 2.1×, B 1.0×, F2 41.7×/6.6×), and every row — scenes, boundary,
kicks — reproduces bit-for-bit; kick gates pass (ratio ≈ 1, other_added = 0). But "exact" carries
an unstated condition, e_hi ≳ ρ/r: a station-keeping fleet (e ~ 1e-6, ρ/r = 1e-4) misses 21,764
of 81,985 encounters (26.5%) because the window scales with e_hi and drops the ρ/r chord term of
the meeting bound. W_SAFETY=4 restores 0 missed at cone-level cost — one additive term from gold.

## Reproduction

Clean tree (only untracked `lab/results/`); `work/patch.diff` is empty, the experiment is
self-contained in `exp/`. Built with the dossier's exact commands (`CARGO_TARGET_DIR=
/home/glmlab/lab-target-2`, 6 threads). Every row of `scenes.jsonl` (F1, CONVOY, TROJANC, F2 ×2,
X, B ×4 configs each) and `boundary.jsonl` (W_SAFETY 0.2/0.5, both kick scenes, exit policy)
reproduced with identical pairs/evals/checks/sections/renewals/half_win/missed/false/matched —
including the boundary misses (CONVOY 1, F1 9 at ×0.2; 0 at ×0.5) and the kick numbers (0.9985 /
44 touches / 0 added; 0.9987 / 45 / 0 exit; 0.9968 / 0 / 0 convoy). Only wall times differ
(shared runner; each command ≤ 45 s, far under 2 GB). All dossier ratios recompute from the rows
(11,197,808/102,408 = 109.4; 55.1M/7.34M = 7.5; 42.1M/15.7M = 2.69; 34.9M/16.5M = 2.11).

## Predictions

File times agree with the claimed order (final code edit → `predictions.md` → record → dossier),
and the smoke-run disclosure (F1, both kick scenes) is explicit. P1 held (44,977 in the predicted
30–45k), P2 held, P3 held, P4 direction held with the magnitude overshoot honestly reported, P5
held exactly. The held-out structure is as good as this lab's norm.

## Attack (three adversarial scenes, scratch copy in /tmp/check2/exp-adv, run folder untouched)

1. **QUIET — quiet station-keeping fleet** (n=200, a-spread 1e-6, e rayleigh 2e-6, λ packed in
   5e-4 rad, ρ = 1e-4, 10 orbits): band **missed 21,764 / 81,985 (26.5%)**, half_win 6.0e-5; the
   cone finds all (0 missed, 0 false), so the miss is the certificate's. Root cause: at a meeting
   within ρ the bound is |Δλ| ≤ 2(e_i+e_j) **+ ρ/r**; `w_enc = 2.5·2·e_hi` covers the chord term
   only multiplicatively, so it holds while e_hi ≳ ρ/r and vanishes as e_hi → 0. The code comment
   "2.5 covers ρ/r" is wrong in exactly this way. All six recorded scenes sit at e_hi/ρ ≥ 40, so
   the hole is invisible in the record — and formations, the phase tier's motivating workload
   (6 Oct gold components-4643), include this regime. `W_SAFETY=4` (≈ the missing term: half
   2.3e-4) restores **0 missed, 0 false, all 81,985 matched** at 13,867 pairs of 19,900 — the fix
   is one additive term and the cost table elsewhere is untouched.
2. **ECC60** (e = 0.6 fixed, just below the 5e < π self-destruction, uniform λ): 0 missed —
   numeric check of the equation of center gives max|ν−M| = 1.2615 at e = 0.6, so the meeting
   bound 2.52 < 3.0 = w_enc; the 2.5 margin covers the center equation all the way to
   self-destruction (and above e ≈ 0.63 the tier is all-pairs anyway). The disclosed eccentric
   limit behaves as claimed (band ≈ cone cost).
3. **DRIFTC** (two λ clusters 2 rad apart that drift into coincidence at t ≈ 0.95·t_end; default
   15 bands, and BANDS=1 with renewals clamped to 64): 0 missed both ways — the renewal union
   bound holds at the horizon edge even when the clamp bites.

## Novelty

This completes the 8 Oct run's checker-named fix; the lineage is the 6 Oct gold (phase-neighbour
certificate, rank 4) → the killed rank-from-mean-spacing → this angular form. No HISTORY entry
tries the angular window (r8 v2 killed element-sort/shear-grid/hier-bounds, different family).
A legitimate completion of the record, not a duplicate.

## Goal fit

The board's top scaling risk — candidate work must track real encounters — moves on clustered
phases (2.1–109×) with exactness on the measured scenes, and the record of the prior silver is
corrected as claimed. PRINCIPLES 33 ("a body resolves only the influences that are significant at
its own scale"): the convoy paying its true local density is the right shape. But by PRINCIPLES 19
the ρ/r term is a representation gap ("if you find yourself fixing things…"), and an exactness
claim with a silent validity condition is not adoptable in one step under the lab's zero-miss
standard (q-candidate-degree). Silver, one named experiment from gold.

**The experiment:** add the chord term (`w_enc = 2.5·2·e_hi + ρ/r`, still one scale) and rerun the
six scenes plus a quiet-formation family sweeping e_hi/ρ from ~1e-2 to ~10 with the boundary scan.
Expect 0 missed everywhere with the cost table unchanged; note the tier buys ≈ nothing on quiet
fleets even when exact (they are genuinely encounter-dense — 82k encounters — so cone-level cost
is information, not waste).

## What the author missed

- The ρ/r chord term entirely — the one regime where the phase tier's motivating workload
  (formations) lives, unmeasured and undisclosed in "What would make it wrong".
- Minor: "×0.5 → 0 missed" was run on CONVOY only, not F1; and the kick measurement, honestly
  disclosed as bookkeeping, still leaves the skin's amortization over bands unmeasured — the
  author's own lens section says so and it stands.

Environment: Linux/x86 shared runner; timings are order-of-magnitude only. Nothing in the run
folder was modified except this file; adversarial scenes ran from a scratch copy.
