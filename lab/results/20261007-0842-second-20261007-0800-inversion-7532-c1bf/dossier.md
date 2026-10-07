# Dossier — the checker's named experiment for the inversion of gold 20261006-0346-taleb-09b5

## Claim

Implemented as the gold defined it — every body watches its k = 4 nearest by **current
distance** (min of both directions), rebuilt on set-change — the certificate misses **zero**
real encounters in every scene the inversion built against it (σ_e up to 0.05, the shear
scene, the fleet-in-bath; 60,113 events): the "element coherence" gate dies as a *miss* gate.
The checker's correction then lands, measured: the rebuild term the gold's O(n·k) omitted is
0.95–20 watch-entries per body per orbit (crossing the k = 4 base exactly at σ_e ≈ k/n ≈
0.005, n = 600, and saturating ≈ 2.5× below the linear law at σ_e = 0.05); an embedded
fleet's watch churn is set by the bath it sits in (87.0% of fleet-body entries are belt
bodies — watches must be **global**); and lazy 1-orbit refresh misses 0.16%–67% because
leads run only 0.12–2.8 orbits — **refresh cadence must track churn** (miss ≈ 1 −
E[min(2·lead, T)], verified exactly in the shearing scenes).

## Bottleneck

The board's top scaling risk (encounters at N / the co-orbital certificate). The gold
promised the certificate deletes the quadratic window tier for concentrated workloads. This
run is the one experiment the checker named to decide what the encounters design v2 may
build on: the certificate survives every adversarial scene, and its true cost model is
O(n·(k + churn)) per orbit with churn measured. Nothing is deleted by this run itself; it
deletes the inversion's headline (60–88% misses) and keeps its two surviving breaks in
quantified form (routing/churn), which the design can now wire with numbers.

## Evidence

Truth = the encounters crate's `truth_pair`, scenes/seeds/ρ are the inversion's own
(`make_pop` copied verbatim; its `events.csv` regenerates **bit-identically**, md5
`bd310ef82a43dadc2345c466bfc5576b` — equal to the inversion's and its checker's value, stable
across two of my runs). Watch sampled at 256/orbit; misses checked against the k-set at the
last sample ≤ t_m (either-direction catch); rebuilds = watch-entry events; lead = t_m − last
entry of the partner into either watch.

| scene (n, ρ, orbits) | events | dist-rank@t_m med/max >4 | **miss exact** | miss @1-orbit refresh | entries/body/orbit (med) | lead med (orbits) |
|---|---|---|---|---|---|---|
| A control (600, 1e-3, 120) | 10,128 | 0 / 2 / 0.0% | **0** | 0.16% | 0.95 | 2.79 |
| B σ_e=0.005 (600, 1e-3, 60) | 7,380 | 0 / 1 / 0.0% | **0** | 6.5% | 4.0 | inf (65% never churn) |
| B σ_e=0.020 | 5,760 | 0 / 0 / 0.0% | **0** | 35.4% | 12.0 | 0.204 |
| B σ_e=0.050 | 6,000 | 0 / 0 / 0.0% | **0** | 57.0% | 19.0 (mean 20.1) | 0.119 |
| C shear (600, 1e-4, 100) | 927 | 0 / 0 / 0.0% | **0** | 37.7% | 7.61 | 0.295 |
| D fleet 200 + belt 800 (1e-3, 100) | 29,918 | 0 / 1 / 0.0% | **0** | 67.4% | fleet 13.46 / belt 18.94 | 0.142 |

- **Zero misses, everywhere** — including D, where 87.3% of fleet-body encounters are
  fleet×belt: the global distance watch catches cross pairs the inversion said no body-level
  trigger could route. Distance rank at t_m never exceeds 2 (so k = 4 has margin 2 even at
  clustered contacts).
- **Churn (the omitted cost term)**: entries/body/orbit vs the derived law
  0.64·(δa_max)·n + 1.6·σ_e·n: A 0.95 (pred 0.56), B 4.0 / 12.0 / 19.0 (pred 4.8 / 19 / 48),
  C 7.61 (pred 11.5), D belt 18.94 (pred 19.5). Linear at small σ_e, **saturating** ≈ 2.5×
  below the law at σ_e = 0.05 (overlapping swaps don't all cross the k-boundary).
  Crossover with the base k = 4 per body per orbit sits between σ_e = 0.005 and 0.02
  (derived σ_e* = k/(1.6n) = 0.0042): beyond it the O(n·k) statement undercounts the cost
  3–5×.
- **The bath owns the fleet's churn**: fleet-body entries 13.46/orbit split 1.75 fleet-fleet
  + **11.71 belt-driven (87.0%)** — not the streaming term alone (3.8 predicted); an
  embedded fleet inherits the bath's internal churn. Belt bodies take 4.09 entries/orbit
  from fleet bodies (21.6% of their 18.94).
- **Lazy refresh is the real fragility**: 1-orbit refresh misses 0.16% (A) to 67% (D);
  miss ≈ 1 − E[min(2·lead, T)] (in-watch window ≈ lead before + lead after t_m by
  time-reversal): predicted/measured — A 0.0016/0.0016, C 0.363/0.377, D 0.632/0.674; the
  frozen-phase B scenes deviate (0.49/0.354) because each pair meets at a fixed orbital
  phase (no ensemble averaging). Work per real encounter: 7 (A) to 522 (C) entry-events —
  the watch tier stays below the quadratic window tier's ~10⁴ evals per encounter in every
  scene, least convincingly in C.

Reproduce (Linux x86, shared runner; orders of magnitude only):
```
cd lab/results/20261007-0842-second-20261007-0800-inversion-7532-c1bf/work/fleet2
CARGO_TARGET_DIR=/tmp/fleet2-target cargo build --release --offline    # ~1.5 s
/tmp/fleet2-target/release/fleet2 full    # ~160 s, 4 threads, < 300 MB; D is 60 s of it
#   -> stdout fleet-out.jsonl (the inversion's fields, secs differs only),
#      events.csv (md5 bd310ef82a43dadc2345c466bfc5576b = the inversion's record),
#      watch-out.jsonl (this experiment), lead.csv (all 60,113 per-encounter rows)
/tmp/fleet2-target/release/fleet2 smoke   # 1 s instrument control (B σ_e=0.02, 4 orbits)
```
Source: `fleet2.rs` — the inversion's scene code verbatim plus the watch pass; uses only the
encounters crate's public API; no crate file edited.

## Predictions

Written before any scene ran (`predictions.md`). P0 held (md5 bit-identical, twice). P1 held
(max distance rank 2). **P2 — the decisive — held: zero exact misses in all six scenes; the
kill criterion (> 0.5% anywhere) never fired, so the gold's certificate stands on its own
definition.** P4 held (crossover at σ_e ≈ k/n). P3 mostly held (five of seven entries within
the ×2 band) with two honest failures: B(0.05) measured 19 vs band ≥ 24 (saturation), and
D-fleet 13.46 vs band ≤ 9 (bath-internal churn, not the streaming term — though the
"≥ 60% belt-driven" part held at 87%). P5 held in five of six (D's 67% burst its 0–40%
band). P6 direction held, magnitudes did not (A lead 2.8 vs ≥ 5 predicted; B(0.05) 0.12 vs
0.5–1.5).

## What would make it wrong

- Set changes are detected at 256 samples/orbit; coalesced changes undercount entries
  (worst scene's mean inter-entry spacing is 13 samples, so < 8%, direction: undercount).
- Zero-misses is partly structural (a partner must cross rank 4 before contact); its
  empirical content is that no contact arrives with rank > 4 (max 2 measured) and no
  clustered contact in D pushed rank past 1. A regime where ρ approaches the neighbour
  spacing (dense conjunctions) could break it — untested here.
- Single seed per scene, planar, n ∈ {600, 1000}; the churn law's n-scaling is inferred from
  the σ_e sweep and D's two populations, not swept in n.
- truth_pair's local-minimum criterion inherits the standing-proximity leak the gold itself
  exposed (1–2%): the truth undercounts encounters, so "zero misses" is against that truth.

**Cost of adopting:** none in code (nothing is wired). The encounters design v2 receives the
certificate's conditions quantified: global watches over populations, rebuild on set-change
with churn ≈ 0.64·(δa/a)·n + 1.6·σ_e·n per body per orbit (saturating; inherited from the
bath when embedded), cost O(n·(k + churn)), refresh faster than the lead time. **Fit:** "A
failed expectation is not automatically a failed method: diagnose which one broke (H0183)" —
the instrument now exists: the inversion's expectation broke on definition, the gold's on
cost; "Compute only surprises" — churn *is* the ordering's surprise rate, and the watch pays
exactly it; #19 — current distance is the water, mean longitude was the wrong one.

## The lens

The second-author lens runs the named experiment and inherits its blind spots: I tested only
k = 4, the inversion's ρ and n, planar motion, single seeds; the churn law's n-exponent is
not measured; and the O(1)-per-entry rebuild (sorted along-track structure under adjacent
swaps) is asserted, not built — that implementation question, and the lead-time floor under
adversarial closure rates, are the builder's next rung, not mine.
