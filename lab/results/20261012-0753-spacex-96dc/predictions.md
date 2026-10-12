# predictions.md — 20261012-0753-spacex-96dc

Written BEFORE the decisive runs (probe `truth`, `scale`, `ulp`, `panic`, `crossover`).
Already done when written: build green; unit tests seen passing for the fast cases
(seam/overtake, crowded window, instantaneous, π fallback, outlier linearity, hyper
refusal); the 1M-ring gate was the failing case that forced the class rewrite (not
tuned on; it is the branch's own frozen test).

Held-out cases (not tuned on — no truth numbers for these were looked at before writing):

- P1 **Zero-miss holds everywhere.** Every truth scene (T200, D200, U400 0/1/8 outliers,
  M400 mixed-e, X400 seam, R400 belts s1/s2, P400 hyper core) reports zero missing
  pairs. Basis: every window is a proven superset (shared cancellation is exact for
  equal (e,ϖ); cross pairs pay c_i + c_j ≥ sup|G_i − G_j|; drift and guard unchanged
  from the original, whose T-scene soundness the red-team verified); the cone is the
  crate's own superset filter. If a miss appears I expect it in M400 or R400 (arm
  gating interacting with different shapes), not in the window layer.
- P2 **The ULP cliff dies.** U-scenes with 1 and 8 outliers: armed pairs stay within
  ~4× of the shared case (linear), versus the original's jump to n(n−1)/2 window pairs
  (499 → 124,750 at n=2000 in the red-team's run). With 8 outliers in one class I
  expect ~8·n cross walks, not 8× more.
- P3 **Dispersed shells pay no exact work.** D-scenes at any n: cone_reject dominates,
  armed/exact evals ≈ the tree's candidate count (~49/body at m=100 per shell), events
  = 0. The original's 63.7M boundary solves at n=8000 become ~0.4M.
- P4 **The budget trigger fires between n=1k and n=8k on D** (walk 4·10⁵ → 3.2·10⁷ vs
  budget 1024n + 65536), the run falls back to the tree, and total wall stays within
  ~2× of the tree alone (the wasted count pass is filters-only, no exact work). On T
  and M scenes the phase path completes at every n (walk small or genuinely dense).
- P5 **Hyperbolic intruders neither panic nor emit.** P10/P400: domain_refusals = 4,
  the Kepler core is still certified (events > 0 at n=400), zero events touch a
  hyperbolic index. (The crate's exact machinery is out of domain for e ≥ 1 — p = a(1−e²)
  goes negative and Binet flips sign — so refusal, not silent garbage, is the correct
  behaviour; the dossier says so.)
- P6 **Work per real encounter is flat or falling in n on M** (mixed-e concentration):
  evals/events stays within ~2× from n=200 to n=3200, because armed ≈ cone-passed
  ≈ real conjunction candidates there. If instead it grows, the claim "work tracks
  real encounters" fails for mixed groups and I report where it breaks.
- P7 **Wall clock**: D n=8000 fixed ≤ 5 s (original: 15.5 s), and the crossover mode
  shows the sweep-only cost ≪ tree, i.e. the budget constant (1024/body) is conservative
  but not wrong by orders.

Kill criteria: any missed contact kills the configuration (not the method: the
supersets are the method, a miss means a derivation bug); armed pairs growing
quadratically on any scene kills the "tracks real encounters" claim for that regime;
a panic anywhere kills the build.
