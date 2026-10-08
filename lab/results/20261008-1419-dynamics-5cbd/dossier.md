# Dossier — 20261008-1419-dynamics-5cbd (dynamics lens)

**Claim.** In a belt under one planet, the belt splits at a measured wall
1 − a ≈ 1.20·μ^0.236 into a regular inside, where the frozen Jacobi bar
(max |ΔC_j| < 10⁻⁴) needs a kick cadence of 16–32 per orbit set by the local
secular rate — not by chaos — and a chaotic annulus (surprise time 25–2000
orbits) plus an encounter class (36% of a belt reaching to 0.95·a_p at μ=10⁻³)
where no cadence ≤ 64 holds the bar because the metric saturates on both the
law and its truth; so surprise time does not schedule kicks in the regular
belt, and a Jacobi gate must classify bodies before it judges them.

**Bottleneck.** Board #1 (kicks dominate cost; cadence is the lever after
correctors died) and the instrument risk in HANDOFF ("B12 cannot yet tell
bounded from compounding error on chaotic ships"). Expected gain: not the
hoped 4× kick cut — this run kills that hope for surprise-time scheduling and
hands q-cadence and q-b12-design the measured numbers they were missing.

**Evidence** (all commands ≤ 60 s except the two sweeps, ~3–4 min each, run on
this 8-vCPU/15 GB shared runner, load ~1–3, idle-ish; numpy 1.26 float64):

- Controls (`python3 surprise.py selftest`, 20 s): universal-variable Kepler
  drift exact (f·ġ − ḟ·g − 1 = 0; max |ΔE| = 1.3e-15; 500/500 close after one
  period; hyperbolic too); μ=0 shadow control never diverges (0/6 finite);
  Jacobi conserved to 1.8e-6 at h=2π/4096 over 50 orbits, converging in h.
- Atlas (`python3 runs.py atlas` → `atlas.npz`; `python3 analyze_atlas.py`):
  shadow pairs (δM = 10⁻⁸), T_div = time to reach 10⁻³ separation, leapfrog
  h = 2π/64, T = 2000 orbits, a ∈ [0.60, 0.98] step 0.005, 4 phases, μ ∈
  {10⁻⁵, 10⁻⁴, 3×10⁻⁴, 10⁻³}. Wall (innermost a with ≥50% of the next 0.05
  chaotic): 0.080 / 0.130 / 0.180 / 0.235 → fit 1−a_wall = 1.197·μ^0.236,
  log-resids ≤ 0.043. Leave-one-out: each wall predicted within 0.008 (< 2
  bins). Matches Wisdom's 1.3·μ^(2/7) exactly at μ=10⁻⁵, favours the 1/4 law
  of run 20261003-2306-dynamics-0c67 at larger μ; cannot separate the two
  exponents at this resolution. Resonance teeth: neighbouring bins differ in
  median T_div by up to 12×; min T_div 25–100 orbits.
  Instrument check: h=2π/96 vs 2π/64 on the same seeds → median |Δlog₁₀T_div|
  = 0.29 (the atlas's noise floor, factor ≈ 2), classification agreement 92%.
- Cadence sweep (`python3 backup.py` → `backup.npz`; `python3
  analyze_cadence.py backup.npz 150`): μ=10⁻³, 284 bodies (a ∈ [0.60, 0.95],
  step 0.005 × 4 phases, e₀ Rayleigh 0.02, planet-crossing births rejected),
  DKD law (exact Kepler drift + impulsive planet kicks at k per body orbit),
  T = 150 orbits; truth = per-body adaptive-h leapfrog (h shrinks to 2% of
  2π/1024 near the planet). Jacobi error scales k⁻² on single bodies
  (verified before the sweep; elems bug found and fixed against an analytic
  ellipse — all element metrics pass the μ=0 identity test after the fix).
  Classes: quiet (T_div > 2000, no encounter) 166; encounter (d_min < 0.05)
  102; chaotic without encounter 16. On the quiet class: truth max |ΔC_j|
  p95 = 3.3e-5 (the metric is valid there), and per-body k_req for the 10⁻⁴
  bar is 16 (a ∈ [0.60, 0.65)) → 24 → 32 (a ≥ 0.70), tracking the secular
  precession rate ≈ 0.75μn(a/Δa)² in square root, not the surprise time.
  On the encounter class the truth itself saturates (median max |ΔC_j| = 0.2):
  per-body Jacobi is dead there at any cadence, and 102/284 bodies fail the
  bar at k=64. Total kicks: honest per-body rule (quiet bodies at their k_req,
  the rest at 64) = 11,936 vs uniform 64 = 18,176: 1.52×, far under the 4×
  gold bar of q-cadence.

**Predictions** (`predictions.md`, written after only a 300-orbit smoke atlas):
held — wall exponent in [0.23, 0.30] with tight LOO extrapolation; teeth ≥10×
somewhere; min T_div < 40 at μ=10⁻³; annulus unschedulable by cadence.
Failed — (3) the quiet-belt floor is 16–32, not 4: the floor is the local
secular rate, not chaos (this failure is the run's main finding); (4) the
collapse of required h against T_run/T_div is untestable: the transition from
schedulable to unschedulable is a wall < 0.01 wide in a, not a graded slope;
(5) at k=8 there is no quiet peak below 10⁻⁵ (median 1.3e-3 at T=150; the
quiet/chaotic split shows as 47% vs 89% above 10⁻³, a continuum, not the
predicted bimodality). Not run — the e₀ = 0.1 floor variant and the μ=3×10⁻⁴
cadence transfer (wall law transferred via LOO instead); the 60-minute budget
went to the elems-bug repair and a rerun after a save crash.

**What would make it wrong.** The truth's adaptive h (floor 2% of base) could
under-resolve the deepest encounters; the encounter class's saturation is
partly instrument, partly physics — I separate them only by the truth's own
error, not by a regularized integrator. T_div depends on h (0.29 dex between
two step sizes) and on the 10⁻³ threshold. The wall exponent rides on one
definition of "chaotic" (any of 4 phases diverging by T=2000); a short-Lyapunov
definition (Wisdom's) would move it outward. k_req uses B12's frozen 10⁻⁴
threshold with the 75th percentile per bin; element-behaviour tests (the prior
runs' metric) pass at coarser cadences and would rank runs differently.

**Cost of adopting.** Nothing to build: the numbers are inputs. For
q-cadence: drop surprise-time scheduling for the regular belt; the floor is
secular, k ≈ 16–32 at Jupiter scale, and the lever there is averaging
(H0190), not cadence. For q-b12-design: gate ships only inside their class —
the classifier is one number per body (wall distance 1.2·μ^0.236, or a cheap
d_min/T_div probe); the annulus and encounter classes need statistical gates,
since per-body Jacobi saturates on truth and law alike. For the encounters
queue item: at μ=10⁻³ a belt reaching 0.95·a_p puts 36% of its bodies in the
encounter class — belt scenes for B18b should state their wall distance.
Fit with PRINCIPLES: "Compute only surprises" (§3) — but here the surprise
rate does not price the compute; the secular rate does, and "the simulation
tells us what's next not us" (§22) is served by the measured wall, not by a
heuristic annulus.

**The lens.** Dynamics-and-attractors looked for where unpredictability
lives; it may have under-weighted that the *instrument* (a Jacobi gate on
float references) is itself a dynamical system that saturates under
encounters — the B12 redesign needs that as an input, not a footnote.
The blind spot named in the lens (a transient that ruins a frame) showed up
as the encounter class: quiet for many orbits, then a scattering that no
cadence budget priced.
