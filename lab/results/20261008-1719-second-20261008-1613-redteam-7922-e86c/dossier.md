# Dossier — second author on run 20261008-1613-redteam-7922 (run 20261008-1719-…)

## Claim

The checker's named experiment is done and the finding stands in its smaller
branch: on the **shipped integer law** (`space-darwin16-scaled-v5` cycles,
compiled from `OrbitKey::bound(p, e)` at every kick) the jet's re-anchor
horizon follows (1−e²)^(2/3) — measured 0.088 vs 0.089 at the decisive ratio,
every grid point within 2% of the Kepler closed form, δ^(−2/3) scale
invariance within 8% — and the belt's actual secular channel (e pumped at
fixed a, Kepler-blind) is 3–123× safer (≥ 20× for e ≥ 0.3; the channels
coincide near circular, where fixed-a ≈ fixed-p) but still dies at the tail
(512 kicks at e = 0.995); the trigger criterion works (a global-rate trigger calibrated
on the frozen scene fails at e ≥ 0.9, by 563× the floor at 0.995; the
per-cycle curvature trigger holds everywhere at ≤ 0.6× floor, 0.032
compiles/kick at e = 0.99, right at law.md's 0.05 budget) — but **no belt
scene in the tree concentrates the tail** (B18b σ = 0.07 cap 0.6 and the
encounters σ = 0.03 cap 0.5 both have share(e > 0.9) = 0 exactly, p99 ≤ 2.1×
median), so the smoothness risk is conditional: a hot-tail belt (σ = 0.3),
which concentrates **more** than the first run reported (37.9% of compile
crossings on 1.1% of bodies, 74.4% under the residual kick channel), must be
frozen as a scene — or refused by design — before B18 can certify smoothness.

## Bottleneck

Board focus items 1 (fewer kicks per orbit) and 4 (smoothness, the p99).
The first run sized the mis-budget on a Kepler float model and a belt scene
that does not exist in the tree (the second check's finding). This run moves
the measurement onto the shipped integer law and the tree's own scenes: the
mechanism, the trigger and the gate gap are now measured where the law will
run; what remains adoptable is one sentence plus one rung criterion plus the
scene decision.

## Evidence

All commands from `lab/results/20261008-1719-second-20261008-1613-redteam-7922-e86c/`,
Linux x86, each ≤ 60 s, deterministic on rerun (rerun diff empty; seeds fixed):

```
python3 falsifier-orig.py          # 3.1 s — regenerates the first run's record
                                    #   bit-identically (diff vs published output: empty)
cd jetbench && cargo run --release --bin jetbench    # 18 s — the decisive record
                                                    #   (falsifier2-out.txt, metrics2.json)
cd jetbench && cargo run --release --bin cost        # 4 s — compile wall-cost
```

Model: cycles compiled fresh from the shipped crate at every kick (the exact
record; periods are integer `Scalar`s, summed in f64 — noise 1e-16/orbit, ten
orders under the 1e-6 floor); the jet keeps the anchor cycle and updates the
epoch by the stored first derivative (central FD of compiled periods — the
memo's ∂/∂E, not yet in the crate). Kick = absolute δ(1−e²) = 1e-7/orbit (the
first run's tide scale; P6 verifies ratios are scale-free). p = a = 2304 M
(belt mid-band). Channels: corrE (energy kicks, fixed p = fixed L), randE
(random-sign residual), corrL (tide: fixed a, E conserved).

- **Mechanism, corrE horizons** n\*(e) = 540/519/452/404/350/278/180/116/40/25
  at e = 0.001/0.3/0.5/0.6/0.7/0.8/0.9/0.95/0.99/0.995, against the Kepler
  closed form 543·(1−e²)^(2/3) within 2% at every point. Ratio
  n\*(0.99)/n\*(0.5) = 0.088 vs 0.089; n\*(0+)/n\*(0.5) = 1.195 vs 1.211.
  Kick-size sweep: ×100 and ÷100 move horizons by 0.0465–0.050 and
  4.65–4.69 against 100^(∓2/3) = 0.0464/4.64. The Kepler model's mechanism
  is the shipped law's mechanism.
- **The tide channel (corrL), the checker's "actual kick mode":** horizons
  1635/30604/33572/37786/19240/34149/8489/6381/1126/512 (3.0× the corrE
  horizon at e = 0.001 — the channels coincide near circular — then 47–123×
  for e = 0.3–0.9, 20.5× at 0.995). Kepler makes this
  channel exactly period-invariant; the integer law does not — the walk
  takes the periapsis from 1152 M to 11.5 M and GR's pericenter sensitivity
  takes over, steeper than 2/3 near the tail (8489 → 512 over e 0.9 → 0.995).
  Mid-grid wobble (30–38k) is quadrature-level noise in a channel whose
  curvature signal is ~1e-5 of Kepler's (n\* ∝ curvature^(−1/3) amplifies
  it); the tail drop is systematic. Kepler-blindness does not save the jet.
- **Random control:** n\*_rand/n\*_corr = 4.7–35× (≥ 3× predicted).
- **The criterion and its planted negative control:** global trigger with
  K = n\*(0.6)/2 = 202 (calibrated on the frozen scene's whole e-range)
  holds at e = 0.5 (0.1× floor) and **fails from e = 0.9 up**: 1.4×, 5.5×,
  135.9×, 563× the floor at 0.9/0.95/0.99/0.995. The per-cycle trigger
  (re-anchor when ½|T″|·Σ(g−g_a)² crosses floor/2, T″ from the compiled
  periods) holds at every e (≤ 0.6× floor) at recompile rates 0.0027/kick
  (e = 0.5) → 0.0109 (0.95) → 0.0317 (0.99) → 0.0503 (0.995). The first
  run's compiles/kick numbers carry to the shipped law; at e = 0.995 the
  recompile rate sits exactly on law.md's 0.05 budget at tide-scale kicks.
- **Belt scenes that exist in the tree** (0.285 kicks/orbit, H0190 K2;
  compiles/kick = 1/n\*(e); crossings = measured knot counts, not the gate
  formula): B18b (σ = 0.07, cap 0.6) — share(e > 0.9) = 0.0% exactly, p99 =
  2.1×, p99.9 = 2.5×; encounters (σ = 0.03, cap 0.5) — share 0, p99 1.7×.
  Hot tail (σ = 0.3, cap 0.995): p99 = 11.6×, p99.9 = 148×, share(e > 0.9)
  = 37.9% on 1.12% of bodies (corrE; 74.4% under randE — the residual
  channel concentrates *more* in share because it frees the median body
  34× but the tail only 5×); the e = 0.99 body costs 82× the median body.
- **Why the hot tail is worse than the first run reported:** the shipped
  compile builds the outbound half only and mirrors it
  (`orbit.rs::bound` ends the knot table at ψ = π; `read` mirrors) —
  measured 22.9·ln((1+e)/(1−e)) + 2 knots, ≈ half of B9's full-cycle gate
  count 46.2·ln + 8 (the gate still holds on the full-cycle count). The
  first run's belt arithmetic charged every compile the full-cycle count,
  over-counting the median body ~2× and *understating* concentration.
- **Compile wall-cost** (adds to the rate): 6.3/30.5/138.8 µs per compile at
  e = 0.07/0.5/0.99 — the tail body pays both 20× the recompile rate and
  22× the recompile cost.
- **Scale honesty** (both checkers flagged the mixed scales): at the law's
  own 48-bit energy quantum (δ(1−e²) ≈ 1.6e-11 at p = 2304) the horizon at
  e = 0.5 is ≈ 452·(1e-7/1.6e-11)^(2/3) ≈ 1.5·10^5 kicks, compiles/kick
  ≈ 7·10^-6 — the 0.05 budget is untouched at quantum scale. The budget
  bites only at tide-scale (1e-7/orbit-class) kicks, which is the belt's
  H0190 residual scale. Budget comparisons are explicit functions of kick
  size; the ratio law (n\* ∝ δ^(−2/3)) is verified on the integer law.

## Predictions

`predictions.md` was written before the decisive run (before `jetbench`
existed). **P1 held** (0.088 vs 0.089, band [0.03, 0.15]; 1.195 vs 1.211,
band [1.0, 1.6]). **P3 held** (4.7–35×). **P6 held** (within 8%). **P5
held, stronger than predicted**: the global trigger fails from e = 0.9, not
0.95 (5.5× at 0.95 as predicted, 563× at 0.995); the per-cycle trigger holds
at ≤ 0.6× floor with rates 0.0027–0.032/kick at e = 0.5–0.99 (predicted
2e-3–4e-2). **P2 half-held, honestly**: n\*_L(0.5) = 33572 ≥ 3000 ✓, but
n\*_L(0.995)/n\*_E(0.995) = 20.5 landed **outside** my band [0.2, 10] — on
the safe side (the tide channel stays 20× safer at the extreme than I
allowed); the qualitative claim (finite, dying at the tail) held. **P4
split**: b18b and encounters exactly as predicted (share 0, p99 ≤ 3×); the
hot tail's p99 held (11.6 ∈ [3, 15]) but p99.9 (148 vs [20, 80]) and share
(37.9% vs [8, 20]%) **missed upward** — the concentration is worse than I
predicted, because the compile cost is the outbound half. **P7 missed
informatively**: measured knots are 22.9·ln + 2, not within +2 of B9's
46.2·ln + 8 — B9 gates the full radial cycle's crossings while the compile
builds the outbound table and mirrors; the gate itself still holds.

## What would make it wrong

The stored derivative is a central FD of compiled periods, not the crate's
(unimplemented) integer ∂/∂E; a real jet with coarser stored derivatives
shortens every horizon (the ratios survive — they are T-slope geometry).
The corrL mid-grid wobble is noise amplified by the cubic root; only its
tail numbers should be quoted. The belt MC holds each body's e fixed at its
draw (1/n\*(e) as the steady-state recompile rate, measured directly at five
e's and matching within the trigger's 2× margin); a time-evolved belt MC
would couple the corrL pumping into the distribution — the direction of
that correction is toward *more* tail (birth caps gate e at birth, not
under evolution: KL-style tides pump e at fixed E, the corrL channel, whose
horizon also dies). The memo would dampen median-body compiles (shared
quantized shapes) and so would also steepen, not flatten, the concentration.

## Cost of adopting, and fit with PRINCIPLES

One sentence in law.md (the separatrix trigger is per-cycle and
dimensionless — re-anchor on (δE/|E|)·n^(3/2), equivalently the measured
½|T″|·offset² rule — validated here with its planted negative control);
one rung criterion (recompile rate and compile-crossings per orbit on a
frozen hot-tail belt, median and p99, negative control = global-rate
trigger planted to fail at e > 0.95); and the integrator's scene decision:
freeze a hot-tail belt or state that no belt will be certified hot, before
B18 certifies smoothness. Hours, no component. It fits principle 3
("Compute only surprises" — the surprise rate *is* δE/|E|, which spikes at
the separatrix), principle 12 ("i care about the p95/99 results i want the
game to be smooth"), and principle 33 ("a body resolves only the influences
that are significant at its own scale" — near the separatrix a tide stops
being small).

## The lens

A second author inherits the first run's framing; measured here only what
the checker named, plus the tide channel the checker asked for. Possibly
missed: the corrL tail walks toward the plunge region (periapsis → 11.5 M,
inside which B19/handoffs own the body — the horizon there is a bound on
the jet, not on the plunge); the A2 photon-ring half of the original
dossier was not re-run (it was analytic, both checkers confirmed it, and
r6 remains unwritten — that gap is unchanged and still open); and the belt
MC's static-e assumption, stated above. The "≈0 cost for undisturbed
bodies" premise survives for motion at the belt's frozen scenes; its
per-body p99 survives only if no scene is ever hot.
