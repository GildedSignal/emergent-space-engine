# Dossier — 20261007-0933-system-0510 (system lens)

**Claim.** The kick and the encounter are one event: one synodic-conjunction
calendar per interacting pair (the integer circle rotation `crates/encounters`
already times for encounter windows) carries the kick too, at cadence parity
with the law's cheapest layer (0.57 events/orbit measured), strictly more
faithful than the incumbent orbit-averaged layer away from resonance
(precession-rate error 0.11 vs 0.58 median) and alive inside the resonant band
where the incumbent is blind (REF pumps e 1.4–4.0×, the unified event tracks
it at 1.2–2.4× over-pump, r4's known first-order legacy) — deleting the kick-
cadence chooser and the duplicate window setup, but NOT the resonance
detector, which the conjunction longitude does not give for free (falsified).

**Bottleneck.** Board focus 1 ("kicks dominate the engine's cost; the lever is
cadence", q-cadence queued) and focus 3 (encounters without work per orbit):
these are two schedulers for one physical thing — the synodic conjunction.
components-4643 measured 92% of per-kick evals are window setup; that setup
is the same per-pair geometry the encounter tier computes. Unifying deletes
one scheduler and the duplication; the gain is components and correctness,
not a measured engine speedup (this replica cannot show one).

**Evidence** (Linux x86 cloud, orders of magnitude only; 41 s, 40 MB RSS).
Scene: Sun + Jupiter (μ=9.55e-4, circular, a=5.2), 30 belt particles
(a 2.60–3.15, e 0.02–0.15) + 7 particles scanning the 2:1 at ±0.5–3%, H=24000
(≈322 perturber orbits), planar float replica. REF: Kepler-drift leapfrog at
96 steps/orbit. A: the design's away-from-resonance layer (double-averaged
quadrupole, dϖ/dt = 0.75·n·μ·α³). B: one Gauss-equation impulse per synodic
conjunction (Simpson quadrature along the unperturbed orbit, first order in
μ), optionally memoized by (a/0.02, e/0.01, 64 phase bins).

| metric (away set, n=37→27 non-resonant by q<0.8) | B | A |
|---|---|---|
| precession-rate rel. error vs REF, median | **0.106** (no-memo) / 0.215 (binned memo) | 0.578 |
| final-e absolute error, median | 0.0205 | ≈0.004 (but e forced const) |
| e-envelope ratio B/REF, median | 1.014 | 1.000 (blind) |
| kick events per orbit | **0.565** | n/a (analytic) |
| memo hit rate (shared table) | 0.594 | — |

Near the 2:1 (7 particles): REF pump_ref 1.36–3.96 (resonance develops);
B pump 1.13–6.58 (over-pump 1.16–2.4×, the r4 v2 phase-feedback legacy);
A rate 3.0e-5 flat vs REF rates up to 1.2e-3 with sign flips — the averaged
layer is qualitatively wrong there, by design.

Reproduce: `python3 exp.py 24000` (decisive, `decisive.json`); no-memo
control in the transcript (rate error 0.106, `control.json`); smoke runs at
H=60/400 in `smoke.json`, `smoke2.json`. All < 60 s each, single core.

**Predictions** (`predictions.md`, written before the decisive run): cadence
✓ (0.565 in 0.55–0.75); memo hit ≥0.8 ✗ (0.594 — the table warms slower than
the rotation period promised, and bins double the rate error); away rate
error ≤0.15 ✗ marginal (0.215 binned, 0.106 exact — the miss is the memo
form, not the mechanism); final-e ≤0.005 ✗ (0.0205: the first-order-in-μ map
itself, present without any memo); near-set pumping ✓ (over-pump 1.16–2.4 vs
predicted 1.3–3); A blind ✓; **the free resonance detector ✗ FAILED** —
conjunction-longitude clustering q≈0.42–0.47 everywhere, because inside the
band the impulse random-walks a, so the model's own conjunction longitudes
sweep; regime selection stays with the compiled-frequency test law.md already
has. Kill criteria: none triggered; the configuration survives.

**What would make it wrong.** The e-drift (0.02 over 322 perturber orbits,
first-order in μ, no memo needed to produce it) could break B5's error-type
gate if it is a walk rather than a bounded oscillation — unmeasured here.
The binned impulse memo re-rounds the kick at a static key (the same disease
as the quantized (E,L) memo, though 1000× slower-moving); the smooth
(Fourier, integer-table) form is required before adoption. Multi-planet and
interior-perturber keys, and eccentric perturbers (forced-e geometry), are
untested. The over-pump inside the band is the already-adjudicated reason the
normal form exists; this adds nothing there.

**Cost of adoption.** One per-pair conjunction record (already needed by the
encounter tier) gains a kick consumer; the kick-cadence chooser (q-cadence)
dissolves — cadence is the synodic period, not a choice. The impulse memo
must be rebuilt smooth, keyed by the pair's Binet offset (the same key the
cone filter uses). One step, in the plane's kick path.

**PRINCIPLES fit.** "A fix signals the wrong representation; one law at every
scale" (19): two schedulers for one event is the smell; the synodic
conjunction is the law at both scales (secular away, resonant near — with the
known first-order caveat). "Compute only surprises" (3) and "No work for no
reason" (14): between conjunctions nothing happens, and the event that must
be paid is the one the encounter tier already pays for. "It's a game…
behaviours matter" (2): judged on precession rates and e-envelopes against a
dense reference, never trajectory identity.

**The lens may have missed:** the parent's tide is not a pair event and keeps
its own (already cheap) accumulation — the unification covers neighbour
interactions only; co-orbital and second-order resonances are exactly where
the circle rotation degenerates (the recursion must hand off to the libration
timescale); and a float replica shares every bug with itself — the REF, the
Gauss rates and the analytic rate are three derivations, but one author.
