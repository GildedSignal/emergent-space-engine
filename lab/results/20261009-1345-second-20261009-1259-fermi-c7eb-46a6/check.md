# Check — 20261009-1345-second (second author on 20261009-1259-fermi-c7eb)

Grade: gold

## Abstract (for the integrator)

Second author closed the prior silver's named experiment. The impulse coefficient is now
validated on the crate's own truth encounters: 1091 RK4 runs, meas/pred median 0.998, v_rel
exponent −0.889; the prior (2/3)·2atan(μ/qv²) form is ~18× high and cosψ-blind (wrong sign for
half the encounters). m_crit ≈ 1.3×10⁻¹⁷ M☉ (~1.35-km rock; p1 ~600 m) at game density — the
prior 500-m threshold was ~16× low, conservative in direction. 50-m rocks: 0/1000 cross one
period tick in 1.7×10⁴ orbits (max |S| = 0.22 ticks, 5× headroom, robust to a 4× rate error);
the tp/phase channel the parent never checked first-ticks at ~336 orbits but at 5×10⁻¹¹ rad
(1.9×10⁷ ticks per player pixel), so belt H_live ~0.2/s, ≥5 orders under consumer scale. Tubes
(14.9 GiB) stay binding; event margin is belt-geometry-dependent (4%–125% of a core). Everything
regenerates bit-identically. Cost to adopt: none (decision input, no code).

## Reproduction (clean tree, no patch — work/patch.diff is empty and no crate/doc was touched)

- Shipped `encounters verify a|b|d` rerun (48 s): every physics field identical to
  `work/prev-verify-*.jsonl`; only `truth_s/method_s/wall_s/cone_s` timing fields differ. The
  author's saved `out/verify-*.jsonl` also match the prior record on physics fields.
- `verify c` (never run by the author, their claim): truth counts 3034/2093/1496, missed 0,
  false 0 — exactly the dumper's `out/c-stderr.txt`.
- `enc-dump c` rebuilt and rerun: `c-enc.jsonl` and `c-sample.jsonl` byte-identical to the
  author's (deterministic).
- `validate.py` rerun (65 s): output identical to `out/validate-out.txt`.
- `ledger.py` rerun incl. the 22-s walk (22 s): output identical to `out/ledger-out.txt`.
- Timeline: `predictions.md` 13:55:58; first dump output 13:56:14; RK4 14:18; walk 14:21;
  dossier 14:26. Pre-registration precedes every decisive artifact (16 s before the first dump
  process started; unrecorded peeks cannot be fully excluded since overwriting erases mtimes,
  but nothing in the outputs depends on one).

## Adversarial cases (mine)

1. **Geometry from raw states.** Propagating the dumped Newton states at t−Δ to t with my own
   leapfrog (no crate code): |r_j−r_i| reproduces the recorded d to 1.6×10⁻⁸ relative, and
   d·v_rel = 0 at closest approach to |cos| ≤ 4×10⁻⁸, over 60 game3d encounters. The dumped
   (d, v_rel, b) triple is faithful.
2. **Independent integrator, my own mass.** Leapfrog 3-body (different scheme from the author's
   RK4) at a 1-km-rock mass on 18 slow/mid/fast encounters from six belts: where my own control
   is clean (9/18; the other 9 fail *my* coarse floor, not the claim), meas/impulse = 0.98–1.03,
   median 1.003; the co-orbital slow case degrades to 1.29, as the dossier discloses (~24%).
3. **Walk robustness.** Fresh seeds (202, 303): P-channel still 0.0% for 50-m and ships in
   16666 orbits; tp medians 343–350 (50 m) and 408–410 (ship) vs the author's 336/400. At 4×
   the encounter rate (R = 25/orbit) still 0/1000; max |S| over 1.67×10⁷ walker-orbits is 0.216
   ticks — the 0/1000 claim has ≈5× headroom. The analytic R = 6.24 is ~10× above the naive 2-D
   sweep calibrated against the crate's own measured planar rate, i.e. conservative in
   direction.
4. **The Lévy claim.** var(x) grows ×1.8 from N=10³→10⁶ draws (log-log slope 0.09 ≈ 1/ln N):
   consistent with the stated borderline α = 2 log-divergence, so quoting the walk bound instead
   of the Gaussian 4.7×10⁶-orbit number is justified, and the author's refusal to quote a
   pre-registered flux is correct, not evasion.
5. **Arithmetic.** 12,111 rows; per-belt 2-D m_crit medians, co-orbital/hot = 96.8× ("97×"),
   prior 7.73×10⁻¹⁹ → 1.28×10⁻¹⁷ = 16.5× ("~16×"), 14.9 GiB, 45/1248 events/s, 5.25×10⁻¹¹
   rad/tick, 1.9×10⁷ ticks/pixel, tp-pixel times 1.6×10⁷/1.6×10⁵ orbits — all recomputed and
   confirmed.

## Predictions

Written before the decisive runs. Held: V1 (0.979 ∈ [0.8, 1.25]), V2 (−0.889 ∈ [−1.15,
−0.85]), M1 (1.28×10⁻¹⁷ ∈ [10⁻¹⁸, 5×10⁻¹⁷]), M2 (0.3%/14.6%/98.9%), F2 (336 ∈ [100, 3000];
kill criterion k* < 20 not tripped). Borderline, honestly labelled: M3 (97× vs ≥100×), F3
(3.3× vs <3×). Failed as stated: F1 — and the failure is itself the finding (variance is
log-divergent; my check 4 confirms), with the conclusion correctly re-founded on the walk bound
plus the pixel arithmetic. No kill criterion tripped. One blemish: **V3 is labelled "held" but
strictly failed** — the no-mutual control floor is 0.19× the median signal, not the promised
10⁻³×; the raw numbers are printed in the same line, so it is a generous label, not concealment,
and the p16/p84 ratio scatter (0.95/1.02) shows the floor does not drive the slope.

## Novelty

`docs/HANDOFF.md` still lists "distinctions per game-second (H_live): not measured yet"; no
HISTORY entry covers it. This is the lab's designed second-author mechanism on this window's
silver (the parent run is not yet in the taste log). The 0.126 bit/body program figure is quoted
from the adopted gold components-98bc with attribution. Nothing here was previously measured in
the record; the parent's coefficient and its "phase noise needs 1.7×10²¹ orbits" claim are both
now measured wrong.

## Goal fit

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second". It corrects
the parent's threshold 16× and opens the channel the parent missed, sharpening the design rule
(tubes for m ≳ 1 km / active / consumer-resolved bodies; identity charged to consumer light
cones is a requirement, since no mass threshold protects tp-identity — a 1-Mt ship first-ticks
within ~400 orbits). PRINCIPLES: "the floor is what the player can differentiate" — the tp
channel quantifies that floor exactly (1.9×10⁷ ticks per pixel); "Compute only surprises" (3);
"A failed experiment kills that configuration, never the method" (9) — the killed coefficient
sharpens the method. Gold bar: reproduced bit-identically, held-out predictions held (one
disclosed failure whose diagnosis I verified), and it shows the parent's premise wrong on two
counts, adoptable within one step.

## What the author missed

- The V3 "held" label (above): a control that lands 5× under the median signal should be
  reported as a floor, not a pass; the per-run 3× keep-filter is what actually protects the
  slope, and 133/1224 runs were dropped by it without a sensitivity check on the slope.
- The 3-D rate is never calibrated against the crate's own measured planar rate: the naive 2-D
  sweep overestimates it by ~10×, so the analytic R = 6.24 inherits an unquantified (though
  conservative-direction) uncertainty; my 4×-rate walk shows it does not matter here, but the
  dossier should have said so.
- The i.i.d. random-sign walk ignores signed bunching of repeated quasi-periodic conjunctions —
  flagged in the lens, but a cheap bunched-kick variant (same pairs resampled with correlated
  signs) would have bounded it; left on the table for the next run.
- Minor: the dossier's top-of-range "8×10⁻¹⁶ (hot, ρ=10⁻³)" is actually the mixed-a0.5-3 belt
  (7.85×10⁻¹⁶); hot is 3.39×10⁻¹⁶. And `run.log` is empty (0 B) — harmless since every number
  regenerates, but the session record is the dossier alone.

Per the lab's two-finder rule, gold stands only after a second blind checker agrees.
