# Predictions — 20261010-0541-second (r1w: re-frozen r1 end-to-end)

Written before the decisive run (`python3 r1w_run.py`). Held out relative to
what is already on record: the checker's adversarial run used 128 seeds with an
undisclosed RNG; this run uses 256 seeds, Random(20261010), a different draw
order, and grids nobody has run at m32/m64 (hyperbolic r_p<6 periapsides, the
low-e strong-field axis at m32, per-e boundary e*(r_p), photon capture at ±3%
of the critical impact parameter, ISCO through hyperbolic bands, the 100-cycle
bit-identity lock). r1's frozen tolerance bands applied unchanged.

## P1 — m16 dies at the widened envelope
period_pass_fraction(binet-m16) < 0.99 (KILL); I predict 0.94–0.99, failures
concentrated at e ≥ 0.85 with r_p ≲ 10 M plus the low-e strong-field corner
(r_p ≈ 11–13, e ≈ 0.01–0.02). Precession and prograde still pass at m16.

## P2 — m32 passes every r1 criterion
period fraction ≥ 0.99 at m32; per-seed failures confined to e ≥ 0.97 with
r_p ≤ 8 (from the m⁻² law: err32 = err16/4). Crossings median 15–60, worst
per-seed ≤ ~500 at e ≈ 0.99 (inside the 512 budget; the criterion is the
median, so it passes either way). Risk named: if the draw lands ≥ 3 seeds in
the failing corner, m32 dips below 0.99 and the honest outcome becomes "m64 or
a per-e band is mandatory" — the run reports whichever holds.

## P3 — the low-e strong-field hole at each m
At m16 ≥ 4 of 6 grid points fail 0.1% (errors ~1e-3–5e-3). At m32: 5 of 6
pass, the worst point marginal (~1.0–1.3e-3, right at the band). At m64 all
pass with ≥ 4× margin.

## P4 — the m⁻² law
Slopes of log(err) vs log(m) over {16,32,64} in [−2.10, −1.90] for period and
precession on every fixed case; doubling ratios in [3.8, 4.2].

## P5 — hyperbolic periapsis bands (r_p < 6 M, new territory)
All 7 grid points stay BOUND at m32 (no misclassification inside e ≤ 0.99);
errors continue the same law (period err ~3e-3–3e-2 at (4.31, 0.99), i.e.
worse than elliptic-band strong field; precession still ≤ 1e-3).

## P6 — the wall beyond 0.99 (documentation, outside the domain)
e = 0.995 at r_p = 7: bound, period err 5e-3–2e-2. e = 0.999: bound, err
0.03–0.1. e = 0.9999: MISCLASSIFIED (banded outcome ≠ bound) — the domain cap
at 0.99 is load-bearing at m32 too.

## P7 — capture / photon capture / ISCO
Massive capture: 0 misclassified at m16 and m32. Photon capture at ±3% of
3√3: 0 misclassified — this is my riskiest call (the banded critical b shifts
by the model error near the photon sphere; ±3% may be inside the shift). If it
fails, that is a new hole, not a pass. ISCO: correct at both m (bound case
stays bound 100 cycles, plunge case absorbs, exact agrees).

## P8 — light deflection
deflection_pass_fraction = 1.0 at m16 and m32; worst error < 1.5e-3; oracle
deflection ≈ 4/b at large b (control) and the tail correction is common-mode
to < 1e-6 relative.

## P9 — long runs (shape / repeat / bit-identity)
shape_kept_fraction = 1.0. Re-frozen repeat reading (cycles > k bit-identical
to cycle k, k ≤ 4): 1.0, confirmed at 100 cycles on the two worst seeds.
Frozen-literal reading (every later cycle equals cycle 1 to 1e-12): FAILS
(fraction ≈ 0) because cycle 1 carries the seed-offset transient ~1e-11 —
r1's frozen repeat text is unpassable as literally written with
seed-at-periapsis starts; the re-freeze must state which cycle anchors the
comparison. Prediction: this ambiguity is confirmed, i.e. the frozen reading
fails while the structural retrace holds exactly.

## P10 — per-e boundary
At m32 the largest e with per-seed period err ≤ 0.1%: e* ≈ 0.93–0.97 at
r_p = 7, rising with r_p; e* = 0.99 (whole domain per-seed clean) by r_p ≥ 30.

## What decides gold
The shipped record regenerates (done, bit-for-bit); with P1+P2 holding, the
claim "envelope hole, not a kill" becomes a completed rung-level result:
binet-m16 killed by the widened envelope, binet-m32 passing a widened,
honestly-banded r1 — plus the per-e period-band decision argued from the
measured m⁻² law. If P2 fails (fraction < 0.99 at m32), the deliverable
becomes the refutation: the fix needs m64 or a mandatory per-e band, and the
cost budget (crossings) decides between them.
