# Dossier — 20261010-0448-redteam-f771 (lens: premise red-team)

## Claim

representation.md's Binet cells survive every r1 criterion I could hold out
(precession, deflection, repetition, crossings, massive relativistic scattering)
— but r1's own coordinate-time period band (0.1%) fails from e ≈ 0.85 in strong
field, reaching 1.9% at e = 0.99, where the 1% shape band also fails: an
envelope hole in r1's frozen seed set, not a kill of the method; separately,
the view-gather premise has an unpriced bill (retarded reads of dense regions)
that no rung covers, because r5/r6 named in §7 were never frozen.

## Bottleneck

Bottleneck 0 (the representation). Expected gain: no speed gain; this prevents
(a) qualifying the law on a seed set that omits the eccentric regime the player
actually flies (transfers, slingshots, comet orbits) and (b) building the view
on a premise with no gate. Deletes nothing; widens one sampler and freezes one
missing rung.

## Evidence

Machine: Linux 6.8.0-111-generic, 8 vCPU, load 0.77–1.69 across runs (shared
window; single-threaded Python, < 50 MB). Runtime 2.8 s + 0.7 s controls.

```
cd lab/results/20261010-0448-redteam-f771 && python3 binet_probe.py   # 2.8 s, full output in probe-output.txt
```

Candidate = the design's band law exactly (m=16 rings, u″ + (1−6u_gc)u =
1/L² − 3u_gc², u and u′ continuous across bands), propagated by closed-form
events (no stepping error; this is *more* exact than r1's integer Minsky
rounding). Oracle = exact Schwarzschild timelike Binet ODE (RK4, Richardson
8e-13). dt/dφ = E/(Lu²(1−2u)) identical on both sides, so the comparison
isolates the band model error. Held-out domain: e ∈ [0.75, 0.99] at
r_p ∈ {7, 8, 10} M (r1 froze e ≤ 0.7), plus massive hyperbolic flybys E ∈
[1.05, 2.0] (r1: bound + massless light only).

- **Precession (r1 band 1%): PASS everywhere.** Worst 5.1e-4 (r_p=7, e=0.75);
  error *decreases* with e (4.5e-4 at e=0.99). ≈ 2000× margin.
- **Coordinate-time period (r1 band 0.1%): FAIL from e = 0.85 at r_p = 7**
  (1.19e-3), e = 0.9 at r_p = 8–10 (1.1e-3–1.5e-3), worst 1.93e-2 at
  r_p = 7, e = 0.99. Quadrature control: the error is model error, 1.7e3× the
  quadrature sensitivity (controls.txt).
- **Shape (r1 band 1%): FAIL at e = 0.99, r_p ≤ 8** (1.29e-2 / 1.06e-2),
  driven by the apoapsis radius; passes at r_p = 10 (7.7e-3) and everywhere
  e ≤ 0.95.
- **Crossings per cycle (r1 band 512): PASS everywhere**, 90 → 246 as
  e: 0.75 → 0.99.
- **Cycle repetition (P5): holds structurally.** Per-cycle Δφ deviation:
  1.2e-11 on the first cycles (float band-edge nudge in my probe), then
  exactly 0.0 for all later cycles — the loop retraces bit-identically; error
  is a fixed function of (E, L), non-compounding (principle 13).
- **Massive hyperbolic scattering (no r1 criterion; light band 1% as
  reference): PASS everywhere**, worst 4.2e-4. The relativistic slingshot at
  v∞ = 0.87c with periapsis 8M deflects 0.7556 rad exact vs 0.7554 banded.
- Source of the period bias: the apoapsis side. Period error ≈ 2 × apoapsis
  u-error (dt/dφ ∝ u⁻², most coordinate time is spent near apoapsis) —
  consistent with the measured shape errors being r_a-dominated.

## Predictions

[predictions.md](predictions.md) was written before the run. What happened:

- P1 (precession breaks at e ≥ 0.93): **WRONG — survives** with ~2000× margin;
  error falls with e. Held as a miss.
- P2 (period marginal at e ≥ 0.95): right direction, **understated**: fails
  already at e = 0.85 (r_p = 7) and reaches 19× the band at e = 0.99.
- P3 (shape fails only at e = 0.99, r_p = 7): **right**, and also at r_p = 8
  (1.06e-2, marginal).
- P4 (crossings ≤ 512, ~250 at e=0.99): **right** (246).
- P5 (repetition survives): **right**, with the caveat that my measured 1e-11
  first-cycle noise is my own float nudge, not the law's.
- P6 (scattering fails at r_p = 8, E ≥ 1.4): **WRONG — survives** with ≥ 25×
  margin. Held as a miss.

## Ranked attacks (the lens deliverable)

1. **r1's period/shape bands fail just outside the frozen seed envelope**
   (measured above). Player-visible as arrival/conjunction mistiming and
   apoapsis drift on eccentric transfers near compact masses — navigation,
   which must be perfect (principle 30). Honest visibility ranking: e = 0.99
   at r_p ≤ 8M is a near-plunge comet skim (rare); e = 0.85–0.9 errors are
   0.1–0.2% (marginal). The error is a fixed bias per (E, L), never compounding
   (P5), so the error *type* is admissible (principle 2) even where the size
   trips the frozen band. **Rung criterion that should have caught it: r1's
   `period_pass_fraction` and `shape_kept_fraction` exist — the frozen sampler
   (`random.Random(20260930)`, e uniform in [0, 0.7]) never draws the domain.**
   Fix is one line: e log-uniform to 0.99 (and keep the p ≥ 6.5 + 2e gate).
2. **The view's retarded reads of dense regions — an unpriced bill.** §2:
   "Light is gathered at the observer"; §3: dense regions are chaos whose
   state cannot be re-derived from generators, "only the surprises are logged;
   the rest replays". Gathering at the past light cone needs each visible
   tube's state at t_ret; for doll members that is free (generators), but for
   a dense region it means replaying its event log back to t_ret, and the
   design names no snapshots. First look at a distant battle replays from the
   last snapshot (genesis?) — O(events in lookback) on the frame deadline: a
   p99 hitch exactly when the player looks at the emergent gameplay. Fermi:
   10⁶-ship battle, ~1 contact per body per crossing time, at game time
   compression the D/c lookback spans 10³–10⁶ logged events per first
   observation. Slack priority cannot fix missing data. Note the *cheap* part
   of the premise is actually safe: f(t) = t + |x(t) − x₀| is strictly
   monotone (slope ∈ [1−β, 2]) for |v| < 1, so each tube has exactly one
   crossing and Newton from any first-order seed converges — the risk is data
   availability, not root-finding. **Rung: none — r6 ("view") in §7 was never
   frozen; `lab/rungs/` has no r5 or r6 file.** A retarded-dense-read case
   belongs in r6 before the view is built.
3. **The cycle-memo premise is already contradicted by the integrator's own
   record, and representation.md has not absorbed it.** §3: "a kick updates
   the cycle by a multiply-add… identical invariants share one memoized
   cycle". Measured on the plane (5 Oct, taste log): the exact memo hits 0% on
   distinct kicks; the plane recompiles an orbit on ~99% of kicks; the
   quantized-cell memo hits 94.5% but changes orbits (a law change). §6's
   "≈ 0" row for undisturbed orbits rides on memo hits that do not happen
   under kick flow. **No rung needed — a record-integration fix**: the doc
   should carry the correction (cadence is the lever) the way law.md does.
4. **Principle tension, resolved in-doc but ungated:** §3's dense order runs
   "cells in lockstep" — ticks — against principle 14 ("no ticks"). The doc's
   own defence ("a tick wastes nothing when everything changes every tick")
   is the right reading, and the guard is bit-identity between orders — but
   r5 (dense/sparse bit-identity) was also never frozen; the only evidence is
   the es-space-v2 battle test (H0209). **Rung: r5, missing.**
5. **Survivors worth recording** (a premise that survives is a result too):
   precession to e = 0.99 at 7M with 2000× margin; massive relativistic
   scattering (the slingshot) at v∞ = 0.87c, r_p = 8M with ≥ 25× margin; and
   cycle repetition is *structural* (the band loop retraces by reversibility),
   so the error model's "never compounds" claim holds by construction for
   this component, not by tuning.

## What would make it wrong

My oracle is the exact 1PN Binet ODE integrated in float; if r1's Darwin
quadrature oracle differs materially at e ≥ 0.85, the period thresholds could
shift (unlikely: Richardson 8e-13). My candidate uses closed-form band events
without the Minsky integer rounding; rounding could mask, not create, a period
bias. The 0.1% period band is r1's frozen choice; if the integrator rules that
arrival timing needs only 1% at e > 0.9, the "failure" shrinks to the e = 0.99
shape row alone. The visibility of 0.1–0.2% arrival errors is my judgement,
argued not measured. Attack 2 is a Fermi argument plus a missing-rung finding,
not a measured reproduction.

## Cost of adoption

One line in r1's sampler (widen e; rerun — r1 is already flagged DISPUTED
pending a clean re-run, so this rides the same rerun); a decision on whether
the period band is per-e; freeze r6 with a retarded-dense-read case; one
paragraph in representation.md absorbing the 5 Oct memo correction.

## Fit with PRINCIPLES

- "Measure before claiming" (10) and the simplest falsifying test first: a
  2.8-second float probe against frozen tolerance bands.
- "Errors never compound" (13): confirmed *structurally* for Binet loops
  (retrace symmetry) — the surviving error is a fixed bias per (E, L).
- "navigation, knowledge and dynamics those need to be perfect" (30): the
  failing quantity is the coordinate-time period, a navigation observable.
- "A failed experiment kills that configuration, never the method" (9): this
  kills r1's seed envelope, not Binet cells.

## The lens

This lens overweights exotic cases — I have ranked the e = 0.99 near-plunge
skim as rare and the e ≈ 0.85 errors as marginal, and the recommendation
(widen the sampler) is cheap regardless. What it may have missed: engineering
costs of the snapshot/log fix for attack 2 (it may be trivial: per-viewer
cursors plus periodic snapshots — the design just doesn't say so), and any
premise in §4 (numbers) or §5, which I did not attack.
