# Predictions (written before the decisive run; after a two-ship plumbing pilot)

Frozen statistic: matched pairs (early far-field sample ↔ nearest late partner in normalized
(a, e), gap ≥ 20 P, within D_MAX = 0.25 of the ship's own spread, one-to-one); the pair's
d|C| is adjusted by a through-origin fit on (da, de); the arrow is the sign test of the
residual. Gate: median per-ship z ≤ 5 and worst err ≤ 1e-4 over the judged ships (the frozen
16, classified by the median of a 5-run one-ulp reference ensemble). Pilot seen: ships #32
(median 16 crossings) and #39 only.

1. **Judged set.** 14–16 of the 16 frozen ships are judged (median crossings ≥ 20, median
   closest ≥ 1 planet radius). The SAME set on both rounding paths (plain IEEE and
   fma-contracted kernels): that is the machine-independence claim. The single-run reference
   assessment the red-team found fragile (1 unconverged, 1 inside on Linux) is replaced by the
   ensemble median; replica disagreement is reported per ship.
2. **echo**: median |z| < 2, worst err ~1e-15 (under the 1e-12 floor), PASS on both paths.
3. **scaled 1e-11**: median |z| < 2, PASS. (Its error rides the orbital phase, a fast
   coordinate; at matched slow state it is exchangeable in time.)
4. **planted-bounded**: median z < 2.5, per-ship |z| < 3.5, PASS. Held-out risk: the |a − a₀|
   kink and any e-nonlinearity leak into residuals on ships whose state range straddles a₀; the
   D_MAX cut is what I bet removes it (the pilot ship, a strong upward diffuser, read +1.6).
5. **periodic 1e-7** (the red-team's gray case): median |z| < 2, PASS — no envelope growth, no
   arrow. Documented stance: a bounded time-periodic error does not compound.
6. **planted-compound**: median z > 5, FAIL. Single-ship z scatter is wide (a walk realization
   can fall; the pilot ship read −0.9); the median of 16 is the claim.
7. **planted-drift** (the plain reference at rtol 1e-12): median z > 10, FAIL, on BOTH rounding
   paths (its error series differs between paths; its arrow does not).
8. **planted-kick**: FAIL on the level cap (worst err > 1e-4 after ≥ 20 kicks of 1e-3) and
   median z > 5.
9. **Leak sweep** (total relative Jacobi error per 200 P): 3e-10 PASSES undetected; 1e-9 is the
   boundary (median z between 2 and 6); 3e-9 FAILS with median z > 5; 1e-7 fails by orders.
   Stated minimum detectable leak ≈ 1e-9 relative per horizon, at or below the lens's rule of
   thumb amplitude ÷ horizon (the bounded control's amplitude is 3e-7–3e-6 across ships, so
   A/H = 1.5e-9–1.5e-8).
10. **leak 1e-8 under planted-bounded**: FAIL (median z > 5) if the median ship's bounded
    amplitude is ≤ 30× the leak; on ships where the bounded error dwarfs it (the pilot ship:
    250×) the kink of |a + l| can invert the reading — reported per ship either way.
11. **Pair counts**: at least 13 ships keep ≥ 30 pairs (a ship whose state never returns keeps
    none and reads z = 0, reported); median n around 300–600.
12. **Margins**: the passing controls sit at |median z| ≤ 2.5 against the 5 threshold (≥ 2×
    margin); the failing laws at ≥ 2× above it.

What would make me stop and report a broken statistic: any required control reading the wrong
side (echo/scaled/bounded above 5; compound/drift/kick/leak-3e-9 below 5), or the judged set
differing between the two rounding paths.

---

## Amendment (after the first 16-ship run, before the second; the statistic changed)

The first full run (run-plain.txt, plain path) failed two of its own predictions and is
reported as a failed attempt:

- **Prediction 1 missed, badly**: the one-ulp ensemble judges only **6 of 16** ships (median
  crossings ≥ 20, median closest ≥ 1 planet radius). The freeze selected ships on single lucky
  paths: 8 ships' median crossing count is 8–18, and ships #9 and #12 robustly pass INSIDE the
  planet (0.61 and 0.64 radii). This is a finding about the frozen set, not about the
  statistic; the disposition (re-freeze under the ensemble criterion) is the integrator's.
- **Prediction 6 missed**: planted-compound read median z = −0.89 under the pair sign test —
  a zero-mean walk moves the spread, not the mean, and the sign test sees only the mean.
- **The leak under a larger bounded error inverted** (leak+bounded read −10.25): the |b + l|
  kink of composed signed errors.

The statistic is therefore redesigned once, before any new full run: the pair difference is
now SIGNED (kink-free after the state adjustment), and the test is Kendall's rank correlation
of |residual| against the time gap (a leak grows the mean of r with dt, a walk grows its
spread; both raise |r| with dt — one probe for both forms of compounding). The gate threshold
(5), the judged-set criterion, GAP and D_MAX are unchanged; JUDGED_MIN moves 13 → 5, derived
from the null spread of the median (4.9σ at n = 5 under the 4× dependence allowance; 6 is
what the scene leaves).

New predictions for the decisive run (both rounding paths + sweep):

P1'. echo, scaled, planted-bounded: median z within ±2.5; per-ship |z| mostly < 4; all PASS.
P2'. planted-compound: median z > 5 → FAIL (the walk's spread must grow with dt; single-ship
     realizations may still fall — ships #2's z_max was 18.5 under the old test, so the signal
     exists; the risk is the median).
P3'. planted-drift: median z > 8 → FAIL. planted-kick: FAIL on the level cap and z > 5.
P4'. leak 3e-9 and 1e-8: median z > 5 → FAIL; leak+bounded 1e-8 now FAILS positively (no
     kink); the leak's z no longer depends on its size once it dominates the pair noise (both
     leak rows read the same z on the pilot ship) — the sweep places the detection edge.
P5'. periodic 1e-7: median |z| can exceed 5 NEGATIVELY (grid commensurability with its 100 P
     period); the gate is one-sided (growth is the requirement), so it PASSES; reported as the
     known gray case with the stance stated in prediction 5 above.
P6'. Both rounding paths: identical verdicts on every law and the identical judged set;
     planted-drift's z value itself differs between paths.
P7'. The sweep's detection edge for a bare leak sits between 1e-9 and 3e-9 relative per
     horizon (median z crossing 5).
