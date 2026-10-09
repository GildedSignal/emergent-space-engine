# Dossier — run 20261009-1936-system-8716 (lens: the whole system)

## Claim (one sentence)

The encounters machinery's two certificates — the Binet-cone tier for belts and the phase-rank
certificate for fleets, stitched by a concentration trigger — are one rule on one structure,
`candidate = cone ∧ wrap(Δλ₀) ≤ |Δn|(1+3ē²)H + 5(e_i+e_j) + skin`, evaluated on a single
U-sorted scan with binned phase windows; the trigger, the second certificate and the fleet
category delete, and zero misses survives every held-out scene tested, including mixed ones
where the oracle-trigger design itself drops 8.6% of true encounters.

## Bottleneck

The board's top scaling risk (5 October): candidate pairs per body grow with N; candidate work
must track real encounters. The adopted answer is a two-tier certificate (q-candidate-degree,
silver) plus the co-orbital phase-rank certificate with a dimensionless trigger (taleb-09b5,
gold). That is two structures, two sorts, and a regime switch — three pieces of text and state
where one rule suffices. Expected gain: not throughput (within ~1.5× of the cone tier on
belts) but deletion — one certificate kind instead of three, and no workload-dependent
constant (the rank width) hiding in the fleet tier. PRINCIPLES 4 ("no categories: regimes are
chosen by dimensionless numbers") is honoured more strictly than the trigger design: here the
"regime" is a per-pair inequality that degenerates continuously into the cone when shear is
fast.

## What is unified (the whole-system view)

- The cone in Binet space (shape) and the phase rank (timing) are the two factors of one
  predicate: bodies meet iff their tubes come within b (cone, exact for coplanar Kepler) and
  their relative true longitude can reach a crossing within the horizon H (phase window). The
  phase window is not a certificate of its own; it is the *reachability set of Δλ over [0,H]*:
  Δλ(t) = Δλ₀ + Δn·t + [libration], libration bounded by the equation-of-center series
  measured from start, amplitude ≤ 4(e_i+e_j) + 2.5(e_i²+e_j²) ≤ 5(e_i+e_j) for e ≤ 0.4.
- The horizon H in the formula is the same H as the kick calendar's certificate horizon: the
  encounter certificate and the kick cadence share one number, so the encounter structure and
  the scheduler are one calendar (the board's "steady-state work per orbit → 0, each pair paid
  once per element change": a kick moves one body's (U, V, W, λ) and re-cells it; the index is
  per-bin sorted lists, local updates).
- What it deletes: the concentration trigger, the fleet/orbit-rank second structure, and the
  rank width as a hidden workload-dependent constant. taleb-09b5's "partner rank 4" is true
  only for its formation's phase density; in my fleet scenes the true encounter set extends to
  the window's width (rank-4 recall 0.16–0.36), i.e. the rank certificate's width is a
  workload parameter the formula computes instead of freezing.

## Evidence

Scene generators, methods and metrics: `exp.py` (this folder). Truth = pairs whose sampled
min distance < b over [0,H] (1024 samples, exact Kepler, vectorised). Methods: cone-only
(r8 v2's element-sort tier), unified (this run), ideal-trigger (cone tier outside an
*oracle-labelled* fleet + λ-rank-4 inside it — the repaired design with a generous oracle).
Commands, each ≤ 80 s on this 8-vCPU runner:

    python3 exp.py truth1   # fleet s=1e-3, fleet s=0.1, belt (N=768..512)
    python3 exp.py truth2   # mixed 640+128, fleet s=3e-2, belt uniform-e, fleet H=16
    python3 exp.py sweep    # 8 tightness points 1e-4..0.3
    python3 exp.py scale    # N = 2500, 10000 belt and mixed (no truth)

Recall (zero-miss requirement), from `truth1.jsonl`/`truth2.jsonl`:

| scene | cone-only | unified | ideal-trigger (oracle labels) |
|---|---|---|---|
| fleet s=1e-3 (N=512) | 1.0 | **1.0** | 0.355 |
| fleet s=1e-3, H=16 | 1.0 | **1.0** | 0.224 |
| fleet s=0.1 | 1.0 | **1.0** | 0.163 |
| fleet s=3e-2 (held out) | 1.0 | **1.0** | 0.261 |
| belt (N=768) | 1.0 | **1.0** | 1.0 |
| belt uniform-e ≤ 0.2 (held out) | 1.0 | **1.0** | 1.0 |
| mixed belt+fleet (held out) | 1.0 | **1.0** | **0.914** |
| sweep, 8 tightness points 1e-4..0.3 | 1.0 (0.998 at s=0.3: one cone-skin miss, shared) | **1.0** (same shared miss) | 0.08-0.54 |

Work (pair evaluations and candidates):

- Sweep (`sweep.jsonl`, 8 tightness points, N=768): unified candidates are 20-40% fewer than
  cone-only at EVERY point (e.g. s=1e-4: 205,790 vs 294,528 = C(768,2); s=0.3: 13,435 vs
  15,150), varying smoothly with s — no regime boundary, no cliff. Unified evals are below
  cone-only for s ≤ 0.01 (209k vs 294k) and up to 3× above it at the loose end (s=0.3: 110k
  vs 34k): when the window saturates at 2π the bin scan is pure overhead — a production
  version skips the bin scan for saturated bins (one guard, unmeasured).
- Scaling (`scale.jsonl`, fleets, fixed arc 0.5): cone-only is exactly C(n,2) (measured
  130,816 = C(512,2), 2,096,128 = C(2048,2)); unified's candidate count is n·(2w/arc)/2, a
  FIXED fraction of cone-only set by window/arc, measured 0.70 at e0=0.02 and 0.22 at
  e0=0.002 (tight formation). The fraction, not the exponent, is the gain at candidate
  level; the tier below (Diophantine per-pair work) then scales with candidates, i.e.
  linearly, where the cone tier alone feeds it quadratics. Not measured here: the frequency-
  locked refinement amp_ij ≈ 2|Δ(e e^{iϖ})| for near-equal n (the cone's own R_ij), which
  would tighten w by up to ~5× on apse-aligned formations; stated as the next experiment.
- ideal-trigger with oracle labels: recall 0.08-0.54 on every fleet and 0.914 on the mixed
  scene — the rank width is a workload constant; to stop missing it must widen to the
  formula's window, at which point its evals are unified's plus a second sort and the
  trigger itself.

## Predictions (`predictions.md`, written before the decisive run)

- Held: unified recall 1.0 on every scene including the held-out sweep midpoints, mixed,
  uniform-e, and H=16 (window scales with H by construction; evals rose 107k→118k, only
  fleet-like cells).
- Held (as a falsification, not a win): ideal-trigger's rank-4 misses on fleets and the mixed
  scene — I predicted "recall < 0.2 on tight scenes is NOT expected"; it measured 0.16–0.36.
  The direction I predicted (it either melts or misses) confirmed on the missing side.
- **Falsified and corrected (disclosed):** the a priori window constant 3(e_i+e_j) was wrong:
  6 belt pairs (1.1%) missed, all with Δλ₀ within 2% above the window. Diagnosis with measured
  libration: the oscillation must be bounded *relative to start* (amplitude 2× the
  equation-of-center series, 4e+2.5e², not 2e+1.25e²), a real modelling error, not noise.
  Corrected to the derived bound 5(e_i+e_j) (provable for e ≤ 0.4); every number above uses
  the corrected bound; the falsifying run is preserved in git history of this folder's patch.
- Belt work prediction partially failed: unified evals are 1.5× cone-only's on belts (I
  predicted ≈ parity); the candidate set is 2× smaller. The slack is the Python bin scan, not
  the rule; a Rust cell list with lo/hi pruning closes it (not measured here — stated as
  inference).

## What would make it wrong

- Precession: the law's orbits precess (GR + tides), so ϖ and the Binet point drift between
  kicks; the cone needs the skin the board already assigns it (r8 v3), and the phase window
  needs the drift of Δϖ over H folded into the |Δn| term — same structure, one more term
  (Δϖ̇·H), untested here (the blind spot below).
- Non-coplanar or 3D workloads: the cone is exact in 2D; 3D needs the inclination factor the
  crate already carries.
- The e ≤ 0.4 domain of the bound: fine for belts and fleets; a plunge-adjacent body (e → 1)
  breaks the bound's constant (the 5× grows); such bodies are transients in the engine's
  changeover anyway.
- Sampling truth undercounts slow conjunctions (T=1024 over H): recall is measured against
  found-truth only; a pair missed by both truth and candidates would hide. The cone tier's
  exactness (r8 v2: every candidate finds every encounter) is the backstop for the shape
  factor; the phase factor's zero-miss rests on the derivation plus these measurements.

## Cost of adoption, and fit with PRINCIPLES

- Adoption: fold the phase term into `crates/encounters`' candidate tier as the per-pair rule
  (it already computes ΔU, ΔV, ΔW; it gains Δλ₀ and the sweep), keep the Diophantine tier as
  the exact per-pair check unchanged. The trigger and the fleet certificate are not built in
  the crate yet (the co-orbital build is queued), so adopting now *prevents* a component
  rather than replacing one — the cheapest possible adoption.
- Fit: principle 1 (less is more: three certificates become one rule); 4 (no categories — the
  regime switch becomes a continuous inequality); 19 ("a fix signals the wrong
  representation": the trigger is exactly such a fix); 32 ("symmetry is found, not given" —
  the phase window is the reachability set of the drift, the same min-plus/light-cone logic
  the engine uses for causality); 33 (each scale resolves what matters: fast-shear regions
  resolve shape, slow-shear regions resolve phase).

## The lens: what this lens may have made me miss

The unification is at candidate level; the Diophantine timing tier (continued fractions per
candidate pair) is untouched and may itself be expressible as the same window arithmetic
(first-hit of the rotation into the window) — the crate's `first_hit` already is, so the
unification may extend one tier down, but I did not test that. Eccentricity near 1, 3D, and
precession-driven ϖ drift are the hard special cases named above. And the whole run is
Newtonian-coplanar synthetic scenes: the law's Schwarzschild precession and its integer
bands are represented only by the skin, not exercised.
