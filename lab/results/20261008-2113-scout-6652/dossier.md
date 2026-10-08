# dossier.md — run 20261008-2113-scout-6652 (lens: scout)

**Claim.** The tangency tail of the encounter machinery (the `numeric_window` conservative
advancement that q-candidate-degree measured at 91% of all state evaluations at 10⁶) has a
closed-form replacement from operational conjunction screening: the window on the passage
offset s is the range of the pair's travel-time difference h(λ) = τ_i(λ) − τ_j(λ) over the
arc plus an along-track tolerance. Measured on a faithful float replica of the crate: zero
misses on 686 firing offsets across two tangency families (ρ = 8×10⁻³), width 2.6× the
numeric window's on barely-crossing arcs (median; p90 3.4×) at 110 closed-form evaluations
versus the replica's median 540 full state evaluations (p90 842) — and where the two orbits
never come within 2ρ radially, the same certificate returns a provable never-fires (4/10
one-sided sections) where the numeric window still spends ~620 evaluations arming a window
that never fires.

**Bottleneck.** Board focus item 3 and the top scaling risk: encounters without work per
orbit or per element change. q-candidate-degree (silver, adopted) left the named next
experiment: "the tangency ('Wide') sections' numeric windows, 0.67–0.7% of sections but
91% of all state evaluations at 10⁶ … ≥10× expected from a tangency-native certificate."
This run is that experiment's scout half: the mechanism, its source, and a float falsifier
of cost and soundness on the tangency families. Expected gain if adopted: the setup cost
per candidate pair per element change drops from hundreds of Kepler solves to ~10
closed-form mean-anomaly evaluations; at 10⁶ that is the 91% tail gone (order 10× on total
encounter cost, as the dossier hoped), and it deletes the "least-rigorous piece" flagged
there (the fast linear window on tangency arcs).

## The candidate, its source, and its mechanism

- **Source (skin in the game).** Satellite conjunction assessment screens ~10⁹ pairs daily
  (NASA CARA / 18th SDS screening cycles; the all-vs-all problem, e.g. *Benchmarking deep
  learning approaches for all-vs-all*, Adv. Space Res. 2023, title verified by search) with
  exactly this two-tier structure: a path filter (our Binet cone / radial overlap — already
  the crate's tier) plus a **time filter**: the along-track phase window, evaluated from the
  two orbits' geometry, not by stepping. The asteroid-impact monitors (NEODyS/CLOMON,
  JPL Sentry lineage: Milani & Valsecchi; Öpik 1951; Valsecchi et al. 2003 — the last
  already cited by run 20261005-2129-m-meso-motion-15d6) reduce each encounter to a b-plane
  geometry where the miss distance is a linear function of the timing offset. The MOID
  stationary-point literature (Gronchi 2002, SIAM J. Sci. Comput.; Gronchi 2005, CMDA;
  revisit arXiv:2305.13900, titles verified by search) is the same elimination idea for the
  geometry tier the crate already has. UNVERIFIED beyond titles/abstracts: the per-step
  mechanics of the SSA screening pipelines (I did not read Alfano's papers' internals).
- **Mechanism (ours).** In the crate's section, a pair fires when j crosses the arc with i
  offset by s = (i's passage of θ_c) − (j's). An encounter at time t* with both bodies
  within ρ implies both are within an along-track sweep c of a common longitude λ*: the
  encounter condition is **|s + h(λ*)| ≤ c**, where h(λ) = τ_i(λ) − τ_j(λ) is the
  difference of the two bodies' θ_c→λ travel times — a *fixed function of the pair* under
  Kepler (no rotation, no per-passage work). So the window is
  **W = [−max h − c, −min h + c]**: a handful of closed-form `mean_at_longitude`
  evaluations plus Lipschitz margins (|h′| = |r_i²/L_i − r_j²/L_j|, monotone between
  apses). It slots in exactly where `numeric_window` sits today; the integer first-hit
  rotation on s is untouched. In the law's integers: h in ticks from the integer periods,
  the window a superset in ticks — floats explore, integers decide (lab rule).
- **Known failure mode.** Where the two orbits' travel times track each other everywhere
  (near-identical orbits, formations), max h − min h + 2c covers the whole admissible
  range: the certificate says "could always fire" — which is true, and is the routing case:
  shared free-fall frame (law.md dense order) / exact-periodic check, the same corner where
  m-meso-motion's U/√(μ_p/b) selector sends pairs to the doll. Near-resonant returns
  (keyholes) are handled by the Diophantine first-hit, unchanged.

## Evidence (all in this folder; `python3 tangency.py` ≈ 2–5 min, single core, <100 MB)

- **Faithful replica** of `crates/encounters/src/{kepler,pairs}.rs` (Body, eps_u, arc
  classification, d_of_s with k=32 + Δr·Δv brackets, numeric_window with the crate's
  Lipschitz vmax·1.001 and stop 1.05ρ). Deviations disclosed in the script header (no tick
  rounding; refine counted as 6 evals; MAXD=300 cap; truth grids as stated).
- **Run 1 (passage-sampled truth, superseded for truth but a real observation):** near-
  identical and tangency pairs almost never align within 16 passages — the synodic period
  is ~10³ orbits. Passage sampling cannot judge these windows; the firing set must be
  measured in s-space. (This is also why the crate's integer first-hit, not sampling, is
  the right machinery — it queries the first landing in W directly.)
- **Decisive run (s-domain truth, `tangency-out.json`; the 300 s guard completed F1 and
  F2, cut F4/F3x):** the firing set {s : D(s) < ρ}, found by a fine scan inside B2's
  window (widened 3×) plus a coarse Lipschitz-safe scan of the whole remaining s-domain.
  **F1 (barely-crossing merged arcs, 30 sections): 652 firing offsets, 30/30 sections
  fire; missA = missB = missB2 = 0; outside fires 0.** evalsA median 540 (p90 842) vs
  evalsB/B2 = 110 closed-form evaluations: count ratio median 4.8× (min 3.3×) — and B2's
  evaluation is a closed-form mean-anomaly query (`true_to_mean`), roughly 3–5× cheaper
  per call than A's Newton state solve, so the wall-clock ratio is plausibly ≥ 10×
  (UNVERIFIED as a timing; the count ratio is the measured fact). A never returned None
  and never hit its cap: the conservative advancement always crawls here, reproducing
  q-candidate-degree's ~1,200-eval tangency tail in the replica.
  **F2 (one-sided, 10 sections): 34 fires, zero misses; width median 6.8× (p90 10.3);
  4/10 sections routed out provably** ("no radial overlap within 2ρ anywhere on the arc" —
  a never-fires certificate valid until a kick) where A still paid median ~620 evaluations
  to arm windows that cannot fire.
- **The frontier, not one point:** first-cut B (5 h-samples, global bounds) = 10 evals,
  56× count ratio (run 1's measurement), but width 87× A's — sound yet fat. Tightened B2
  (sub-arc restriction, apse-split intervals, monotone-difference h′ bounds) = 110 evals,
  width 2.57× (p90 3.38×) on F1. The certificate's constants place it anywhere on the
  rigor-cost-width frontier, all closed-form and once per element change; the numeric
  window is dominated everywhere on the measured families.
- **Not run in time:** F4 (near-identical) and F3x (adversarial high-e) were cut by the
  guard in both decisive runs — the soundness claim rests on F1+F2 (686 fires); F4 is the
  routing-heavy family and F3x the adversarial one the predictions named. One command, NP
  smaller, ~2 min.

## Predictions (predictions.md written before the decisive run)

- **Held:** P2's letter — zero misses for the travel-time window on F1 (652 fires) and F2
  (34), including the outside-window coarse scan; and B2 meets P3's ≤ 3× width bar at the
  median on F1 (2.57×; p90 3.38× marginally over).
- **Failed:** P1's letter (≥ 25× eval ratio) — B2 needs 110 closed-form evals, giving a
  4.8× count ratio, not 25×: the tight constants cost samples (the 56× first cut used 10).
  The per-eval cost difference (closed-form vs Newton solve) plausibly restores ≥ 10× in
  wall time, but that is UNVERIFIED. P3 on F2 (6.8× width) — one-sided arcs still over-arm.
- **Untested:** P4 (degenerate share) and P5 (apse-in-arc share): F4/F3x never ran within
  the guard. The routing mechanism was exercised only through F2's 4/10 provable
  never-fires.
- **Disclosed deviation from the pre-registered protocol:** predictions.md framed truth as
  passage offsets; run 1 showed passage sampling is vacuous for these pairs (synodic
  periods ~10³ orbits), so truth was redefined as the s-domain firing set {s : D(s) < ρ} —
  the same superset claim, tested directly.

## What would make it wrong

- A single firing s outside B2's window on any family kills the travel-time window as a
  replacement (P2 is the load-bearing claim; only F1 is done).
- The width ratio is the adoption cost: an over-wide window arms more passages for the
  exact per-pair check and inflates the firing measure (armed/fires). If B2 cannot get
  under ~3× A's width, the certificate should ship only as the *rigor* backstop plus a
  routing tier, not as the window.
- The replica is float and single-threaded: it reproduces the crate's algorithm and its
  cost structure, not its bit-exact integers. Adoption means re-deriving h, c and the
  margins in the law's ticks (integer travel times from integer periods; the margins as
  integer ceilings) — mechanical, but until then these are algorithmic count ratios
  (4.8×/56×), not measured engine speedups.

## Fit with PRINCIPLES

- "The right question, then the representation… we just need to have the right
  representation so that math is trivial" (P18): the s-domain scan is a search because s
  is the wrong variable; h(λ) is fixed per pair, so the window is a range, not a search.
- "Compute only surprises… we only care about changes" (P3, P14): the window pays once per
  element change, closed-form, no per-passage work.
- "Steal what works, from skin in the game" (P26): conjunction screening and impact
  monitoring pay real costs for exactly this certificate.
- "A fix signals the wrong representation" (P19): the Lipschitz crawl is a fix for using
  the wrong variable, not a tuning problem.

## The lens

Scout searched the fields with the same structure (SSA conjunction screening, asteroid
impact monitoring, MOID computation, kinetic data structures) and ranked by fit to *our*
requirements (exact, integer, once per element change, 2D Binet representation already in
place). What the lens may have missed: the 3D/inclination structure (the crate is 2D; a
node adds one more monotone segment to h, but untested), and the possibility that the
whole Wide tier should be deleted instead of cheapened — near-identical pairs are
formations, and the law already routes them to shared frames; if the board decides that,
this certificate becomes the routing test itself, and the 91% tail dies by deletion, the
best part being no part (P1).
