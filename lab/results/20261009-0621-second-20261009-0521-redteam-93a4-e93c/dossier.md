# Dossier — second author on 20261009-0521-redteam-93a4: the checker's gold path, done

- **Claim.** With the isolation control as the decisive metric and an encounter
  clause in the domain, the "gravity is news" tube read's error under kicked
  sources is now **measured** (not inferred) to be second order in the kicks
  (μ-slope 2.01) and bounded — flat at 3.32e-7 over 300 reader orbits at
  μ = 1e-3 — while the naive retarded read is first order (slope 1.01) and
  fails the same gate by five orders; the frozen two-sided rung passes on the
  shipped record (`verdict.py`: PASS, Carlip variant killed), and the three
  cases that killed the original criterion by its letter are all encounter
  cases (truth pair separation ≤ 2.04 mutual Hill radii), with one **new,
  measured boundary**: at μ = 1e-2 the pure read error's envelope grows after
  ~50 reader orbits through reader-side resonant pumping (7.73e-4 at 100
  orbits, no Hill violation) — beyond the regime the gates freeze.

- **Bottleneck.** Foundation risk for `b-news-gravity` (queued; Julien, 5
  October: "gravity must travel at c… can't construct layer upon a flawed
  foundation"). The gate hole is real and now closed by frozen text: no B-gate
  exercises retarded reads, so a planted naive-retarded law passes every
  current gate. This run deletes the "retarded acceleration in tubes"
  candidate *by gate* (the rung kills `tube-carlip`, whose error is first
  order, 4.13e-5, 124× the plain tube) and hands the integrator a one-step
  adoption: freeze `rung-r-news.md`. No speed gain is claimed; what moves is
  that the premise's untested edge is measured on a record that regenerates.

- **Evidence** (all from `work/`, each run ≤ 30 s, everything bit-identically
  reproducible: `sh work/repro2.sh` → `runs2b.txt` diff `runs2.txt` = machine
  line only; `sh work/mkmetrics.sh` regenerates `metrics.json` from `news2.c`;
  `news2.c` = the run's own `news.c` + `iso` flag + `rJfac` + Hill columns,
  no-iso output bit-identical to `news.c`).
  - **Isolation decisive metric** (candidate sources slaved to truth, dS/rS =
    0.00e+00 printed every line): μ = 1e-3/1e-4/1e-5 at 30 orbits →
    **3.32e-7 / 3.72e-9 / 3.15e-11, slope 2.011**; long runs: 9.23e-8 at 100
    orbits, **1.34e-7 at 300 orbits** (flat). The checker's inference is now
    the measurement.
  - **Naive retarded, same scene, isolated**: 3.33e-2 (30) → 8.95e-2 (100);
    μ-slope **1.007** — first order, the contrast that makes μ² a behaviour,
    not a coincidence.
  - **Encounter clause** (truth pair separation in mutual Hill radii, printed
    as `hillmin`; excluded below 2√3 ≈ 3.464, Gladman, as B12/B13 exclude
    oracle-domain cases): judged scene hillmin = 8.45. The three letter-killers
    all fall outside: crossing reader R=2 → hillT1 = **0.233** (read error
    9.95e-2 even isolated); R=2.5 → hillmin 2.03, and between 10 and 30 orbits
    the reader **collides** with J in truth too (hillT1 → 0.002, dEtruth self
    1.3e+3); close sources rJ=1.2rS → hillSS = 0.048, free-run dS/rS → 4.96e+3
    (checker's 4960), isolated read error 1.21e-3. In-domain geometry sweep
    μ=1e-3, R ∈ {3,5,8,10}: 7.41e-7 / 3.32e-7 / 1.67e-7 / 2.20e-7 — no secular
    case, no R-growth. The clause is necessary, not cosmetic: every excluded
    case explodes even with exact sources.
  - **The μ = 1e-2 boundary (the one honest miss).** R=5, hillmin = 3.92
    (in-domain), 30 orbits: 5.11e-5 bounded — the free-run's 2.32e-2 was 99.8%
    inter-law source divergence (dS/rS = 2.0). But 100 orbits: **7.73e-4**,
    envelope ~15× per decade past 50 orbits, tracking the reader's own drift
    (dT/rT = 3.6e-2), non-monotone (6.51e-6 at 30), below the frozen 1e-3 kill
    line. Reader-side resonant pumping (T near 5:2 with J), no Hill violation:
    the read error feeds back through the reader's orbital diffusion. The
    gates' regime is μ ≤ 1e-3 (the original scoping: 1e-2 secondaries at
    κ = 0.3 are "beyond any scene the gates freeze today"); the rung judges
    μ ≤ 1e-3 and the dossier records this edge.
  - **Controls both sides.** Free-fall floor (kicks off): 2.12e-9 at 30, 8.83e-9
    at 100 orbits (positive). Naive fails b30/b100 by 3-4 orders (negative).
    Solar-like κ=0.05: 8.15e-9. Carlip term under isolation: 4.13e-5, slope
    0.98, no gain — killed by the rung.
  - **Rung** (`rung-r-news.md`, this folder; freeze as `lab/rungs/r-news.md`):
    `verdict.py rung-r-news.md metrics.json` → **"PASS; tube passed every
    criterion; killed: tube-carlip"**; hostile check (candidate replaced by
    naive's numbers) → KILL, so the gate can fail. Self-run only — the blind
    checker verdict is the integrator's to trigger. The μ²-slope criterion is
    a loose band [0.5, 2.3] because the positive control's floor is
    μ-independent by construction; the 2.01 slope itself rides in
    metrics.json as evidence.

- **Predictions.** `predictions.md` was frozen before all decisive runs.
  Held (7 of 8): μ-slope 2.0 ± 0.15 (measured 2.011); 100-orbit boundedness
  ≤ 1e-6 (9.23e-8); μ=1e-2 bounded ≤ 1e-4 at 30 orbits (5.11e-5); geometry
  sweep ≤ 3e-6 with no secular case (max 7.41e-7); R=2 grows ≥ 1e-2 even
  isolated (9.95e-2); rJ=1.2rS ≥ 3e-6 isolated (1.21e-3); Carlip buys nothing
  (124× worse). Missed: μ=1e-2 at 100 orbits — predicted ≤ 2e-4, measured
  7.73e-4 with decade ratio 15 (predicted ≤ 3); R=2.5 exceeded prediction
  (collision, 1.25e+3 vs ≥ 1e-4 — same direction).

- **What would make it wrong.** The toy is near-circular (tube propagation
  exact only for the circle; the real law compiles the exact Darwin cycle, so
  this understates the design); the dominant mass is fixed; the oracle is
  Newtonian, so at κ = 0.3 the μ² bound is a statement about the read, not GR
  fidelity (inherited caveat). Eccentric kicked sources at game compactness
  showing a *secular* μ² error would kill the premise; equally, any gate scene
  with secondaries ≥ 1e-2 at κ ≈ 0.3 on ≥ 100-orbit horizons now has a
  measured reason to not trust the bare tube read. Cost of adoption: freeze
  one rung file; zero engine code. Fit with PRINCIPLES: principle 13 ("types
  of errors and not just errors" — bounded second-order read error vs
  first-order Laplace spiral), the 5 October freeze it de-risks, and 26
  ("steal from people with skin in the game" — Gladman's Hill-stability
  boundary from the planet-stability literature).

- **The lens.** A second author inherits the first author's instrument and its
  blind spots: Newtonian oracle, near-circular sources, fixed dominant mass,
  one deterministic seed per case (no conjunction-phase ensemble — a checker
  can vary `rJfac` cheaply), and the original's checkpoint-sampled maxdE (the
  3-orbit synodic transient is caught only because the 3/10/30 checkpoints
  sample it; kept deliberately for comparability, disclosed here). What this
  lens may have missed follows from that: eccentricity, a live dominant mass,
  and whether the encounter clause's 2√3 line is the right cut for resonant
  (non-crossing) cases — μ = 1e-2 grows with no Hill violation at all, so the
  clause is necessary but not sufficient for boundedness at strong
  secondaries.
