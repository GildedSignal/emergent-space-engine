# Rung r-news (draft, frozen text for the integrator): gravity is news, read error under kicked sources

Proposed by the redteam-93a4 line (author + checker + second author, 9 October
2026). This is the two-sided gate that run's dossier asked for: no B-gate
exercises retarded reads today, so a planted naive-retarded law passes every
current gate at solar scale. Freeze as `lab/rungs/r-news.md` if adopted.

**Question.** The motion law v2 reads every source through the "gravity is
news" cursor: the tube the reader's past light cone last saw, extended along
the dominant drift to now. With *kicked* sources, the extrapolation misses the
kicks the source received inside the light time. Is that read error second
order in the kicks and bounded — and does the naive retarded read (Laplace)
fail where the tube passes?

**Scene** (harness: `news2.c`, this folder; iso=1 everywhere — the candidate's
sources are slaved to truth, so the measured error is the pure READ, not
inter-law source divergence; dS/rS must print 0.00e+00 or the run is VOID):
dominant fixed M=1 (G=c=1), sources S and J (mass μ, kicked by each other) on
near-circular orbits at rS and 2.17·rS, reader T massless at 5·rS; κ=0.3;
truth = instantaneous Newtonian, velocity Verlet dt = P_S/2500 in lockstep.
Judged μ ∈ {1e-5, 1e-4, 1e-3} — the regime the gates freeze; μ=1e-2 secondaries
at κ=0.3 are beyond any scene the gates freeze (measured boundary in the
second-author dossier: the read-error envelope grows past ~50 reader orbits
through reader-side resonant pumping, with no Hill violation).

**Domain clause (encounters).** The harness prints running minima of each body
pair's separation in mutual Hill radii (`hillmin`). A case whose hillmin drops
below 2√3 ≈ 3.464 is in the encounter regime (Gladman's Hill-stability
boundary) and is out of the oracle's domain, exactly as B12/B13 exclude
flybys through the planet: deep conjunctions belong to changeovers and pair
events, not to tube reads. The judged scene sits at hillmin = 8.45.

**Configurations.**
- `tube candidate`: the design's read (law 1).
- `tube-carlip candidate`: tube + ½(a_kick)·τ² at the retarded state (law 2).
  The acceleration term the original run deleted; this gate kills it.
- `naive-retarded negative`: pull toward the retarded position (law 0).
  Laplace; must fail.
- `freefall-tube positive`: kicks off (noSJ=1) — the read is exact for
  circular free-fall, so only the Verlet floor (≤ 1e-8) remains. It must pass,
  or the criteria are unpassable.

**Metrics** (regenerate with `sh mkmetrics.sh`, ≤ 30 s per run, ~3 min total):
- `hill_min_ratio`: the scene's hillmin over the 100-orbit run (encounter clause).
- `read_bound_30`, `read_bound_100`: max|ΔE_T|/|E₀| at the 30-orbit (3/10/30
  checkpoints) and 100-orbit (10/30/100 checkpoints) runs, μ=1e-3.
- `read_growth_100_30`: maxdE at 100 orbits ÷ maxdE at the 30-orbit checkpoint
  of the same run. Threshold 10: the free-fall control's own ratio is 4.2
  (roundoff walk), so a tighter line is unpassable; a law whose error walks
  ≥ 10× per 70 orbits dies here.
- `mu_slope`: log-log slope of read_bound_30 over μ ∈ [1e-5, 1e-3]. Measured:
  tube 2.01 (second order — the claim), naive 1.01, carlip 0.98 (first
  order), freefall 0.92 (μ-independent floor). The band [0.5, 2.3] catches an
  aberration bug (slope → 0) or a super-quadratic leak; the tight slope ≥ 1.7
  cannot be a criterion because the positive control's floor is μ-independent
  by construction — the 2.01 slope itself is evidence, carried in metrics.json.

```configs
tube candidate
tube-carlip candidate
naive-retarded negative
freefall-tube positive
```

```criteria
dom type hill_min_ratio >= 3.464
b30 behaviour read_bound_30 <= 1e-05
b100 behaviour read_bound_100 <= 1e-05
grow behaviour read_growth_100_30 <= 10
mu2lo behaviour mu_slope >= 0.5
mu2hi behaviour mu_slope <= 2.3
```

**Author values** (2026-10-09, `metrics.json`): tube 3.32e-7 / 9.23e-8 / 1.26 /
2.01; carlip 3.84e-5 (dies on b30); naive 3.33e-2 / 8.95e-2 (fails b30, b100);
freefall 2.12e-9 / 8.83e-9 / 4.17 / 0.92 (passes all). Expected verdict: PASS
with tube-carlip killed.
