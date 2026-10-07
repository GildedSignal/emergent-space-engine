# Dossier — 20261007-0341-scout-9abe (scout lens)

## Claim

A local, self-triggered kick cadence (event-triggered control transplanted onto
the law's drift-plus-kicks layer) holds fixed-cadence behaviours at 2.5–4 kicks
where fixed needs 8–32 (up to 6.4× fewer), **but** the trigger's local bound is
blind to resonance, and at resonance the experiment found the opposite of the
lab's implicit assumption: coherently phase-locked cadences (orbit-averaging =
1/orbit, every fixed power-of-two rate 8–64/orbit) pump eccentricity up to 10×,
while *de-phased coarse* cadences (2–4/orbit, or the trigger at ~2–3/orbit)
track it best — so the rule that survives is "trigger locally for cost, de-phase
near commensurabilities, read resonance from the compiled frequencies, never
from a local divergence bound."

## Bottleneck

Board focus #1: "fewer kicks per orbit at the same behaviour: kicks dominate the
engine's cost" (the acknowledged lever; `q-cadence` queued, never run). Expected
gain: 4–6× fewer kicks on quiet/moderate scenes, and the removal of the fixed
power-of-two cadence as a hidden resonance hazard. What it lets us delete: the
global cadence constant `step_log2` per scene family.

## Prior art (verified at source unless marked)

- **Event-triggered / Lebesgue sampling**: B. Bernhardsson, "Comparison of
  Periodic and Event Based Sampling for First-Order Stochastic Systems" (Lund,
  1999; lup.lub.lu.se); Åström & Bernhardsson, "Systems with Lebesgue sampling"
  (2003), cited with full reference in arXiv:2304.03312. Level-triggering beats
  periodic sampling on the same error budget for smooth signals. [The specific
  savings factor (≈2–4×) I could not read at source: UNVERIFIED.]
- **Multiple time stepping's resonance instability**: r-RESPA/Verlet-I linear
  resonance instability when slow impulses alias the fast frequency; the
  mollified-impulse fix (A. Stern, "Implicit-Explicit Variational Integration
  of Highly Oscillatory Problems", 2008, cs.columbia.edu; Bishop–Skeel–Schulten
  mollified impulse). Orbit-averaging IS mollification — consistent with
  law.md's averaging rule and with its known death near resonance.
- **Tabuada's ISS event-trigger** (Automatica/CDC 2007): exists per secondary
  citations only — UNVERIFIED at source.
- Anti-aliasing by dithering (delta-sigma modulation) is the mechanism behind
  the de-phasing finding; cited as analogy, not measurement.

## Mechanism and mapping

At each kick the body computes J = |d(tide)/dt| along its predicted drift and
the tide scale |a|, then fires the next kick at the first τ with
½Jτ²(1+τ/P) ≥ κ·|a|·P (κ dimensionless; a √τ-equidistributed variant "TRIG2"
budgets error per unit time). Cost: 2 tide evaluations + one closed-form solve
per kick. In the engine this is decided exactly: integer compare at the body's
next power-of-two grid time (law.md's anchored steps), so the schedule
independence law holds; the trigger IS the certificate-expiry event H0195
already names. Principle 22 made literal: the simulation tells the body when
it is next surprised. Failed half: resonant pumping is a small-divisor effect
invisible to any local bound — the compiled cycle frequencies (already in the
law's memo) must carry it.

## Evidence

All numbers from `lab/results/20261007-0341-scout-9abe/work/` on this Linux
runner (8 vCPU, load 0.5–1.3, pure Python, orders of magnitude only; each
command ≤ 10 s):

- `python3 cadence.py S1` → out_S1.json — quiet LEO (K1's scene, 60 orbits):
  FIXED-16 16.0/orbit da_rel 7.2e-6, epump 1.22; **TRIG-0.5 2.5/orbit da_rel
  6.0e-6 (better), epump 11.6 (worse: e-walk)**; TRIG2-0.125 9.5/orbit epump
  1.48 (extra.py). K1's impulse-quantum trigger reproduces at 44/orbit vs the
  logged 32.5 (+35%, no lattice error-feedback here).
- `python3 cadence.py S2c,S2d,S2c2,S3,S4` → out JSON — 2:1 resonance
  (μ=1e-3, 200 orbits): truth e 0.023; AVG (phase-locked) epump 10.3; FIXED-8
  to FIXED-64 epump 2.9–4.1 (denser ≈ no better); **TRIG2-2.0 1.7/orbit epump
  1.55 — best of everything tried**; detuned S2d: FIXED-4 0.24 (over-damps),
  TRIG-0.5 0.81 and TRIG2-0.5 1.02 in B17's [0.8,1.25] band at ~3/orbit;
  second phase S2c2: nothing holds (8–47), confirming dynamics-a9c2 that the
  layer, not the rate, fails at the centre.
- Moderate tide, e=0.3 (S3): **TRIG-0.25 2.75/orbit, epump 0.998, da_rel
  0.0149 vs FIXED-16's 1.04/0.0209 — both behaviours held at 5.9× fewer
  kicks.**
- Adversarial steep conjunctions (S4, e_p=0.6): the truth itself scatters
  (a→3.35, e→0.97); every FIXED rate 8–64 unbinds, AVG and TRIG2-0.5 survive
  (epump 0.96) but da_rel ≥ 0.24 for all. Cadence is not the binding question
  there (regime change / pair event), and a single seed cannot judge a chaotic
  scene — S4 is reported as out of this rung's domain, not as a pass.
- Coarse de-phasing cells: `python3 extra.py` → out_extra.json — S2c: FIXED-2
  2.7/orbit epump 2.41, FIXED-4 5.1/orbit 1.80 (vs FIXED-64's 3.95 at 67/orbit);
  AVG ≡ FIXED-1 numerically (both phase-locked, epump 10.3).

## Predictions (predictions.md, written before S2–S4 ran)

- P1 partially held: TRIG fires 1.4–4/orbit on S1 (predicted 0.7–4) with
  da_rel ≤ FIXED-8's — but de (e-pump) does NOT hold at those rates; holding
  epump ≲1.5 costs ~9.5/orbit (TRIG2-0.125). The 4× cut survives only on the
  a-axis or on S3-like scenes, not on S1's brutal e≈2e-7 target.
- **P2 falsified**: the trigger does NOT densify at resonance (rate spread
  S1↔S2c ≈ 1.5×, predicted ≥8×; wall flags 0). A local divergence bound cannot
  see small-divisor error. AVG's failure was as predicted.
- P3 held (TRIG in 2–3/orbit on S2d, epump strictly closer to 1 than AVG's).
- P4 held (S3: 2.75/orbit, both behaviours at or better than FIXED-16).
- P5 not properly tested: S4's scattering makes single-seed element endpoints
  meaningless; clustering metric unmeasured.
- P6 (the gold bar, ≥4× total at equal behaviours on mixed scenes) **not met**:
  one global κ gives ≈2× (TRIG2-0.125: 9.5+6.95 vs FIXED-16's 32 per two
  scenes) with S1's e marginally out of band.

## What would make it wrong, cost, fit

Wrong if: the plane's real kick cost is dominated by something other than
cadence count (e.g. window setup, per `components-4643`); or the integer
trigger, once anchored to power-of-two grid times, loses the de-phasing
property (quantized trigger times may re-lock to resonances — must be tested
in the engine's integer form). Adoption cost: small — it replaces the choice
of `step_log2` with one integer comparison per kick plus a κ from local
dimensionless numbers; it adds no new state. Fit: principle 3 ("compute only
surprises"), principle 22 ("the simulation tells us what's next not us"),
principle 13 ("errors never compound" — the per-gap bound violated it, which
is exactly why TRIG2 exists and why κ must be per-horizon). The de-phasing
finding also warns the current design: power-of-two steps anchored on
multiples are maximally commensurable with p:q resonances.

## The lens (what the scout may have missed)

The scout lens trusts published mechanisms whose requirements differ from
ours: event-triggered control assumes a feedback loop we do not have (our
"control" is the impulse quadrature), and MTS assumes one fast frequency. The
falsifier is a 2-body restricted float replica with midpoint quadrature — it
cannot speak for the integer law's re-anchoring or for ensembles; S4 needed
statistics over seeds that one run cannot buy. The e-target on S1 (2e-7) may
be an artefact of a scene where truth's e is nearly frozen.
