# Dossier — 20261009-0401-second (second author on 20261009-0208-fermi-fe6b)

**Claim.** The checker's named experiment, done: the kick→pair-certificate cascade is now
anchored on the shipped code at N = 10⁶ (with exact soundness controls), the event-queue term
is measured and wired in, and the original claim **holds in rank but not as written** — the
cascade is still the only term near a core (0.966 no-skin / 0.077 with skin per 10⁴-cell,
M1-implied, reproducing the original's numbers from the reproduced anchor), but (a) "every
other term ≥ 3 orders below" is false: a window-keyed queue costs 0.032 cores (2.4× below the
skin cascade, not 10³), so the program-level keying rule is load-bearing, and (b) the 812.8
pairs/kick is a **cell constant, not a belt-density convention**: measured law
`pairs/kick = 0.0346·n·(1+X)/(2(X−1))` (six geometries, 10⁴→10⁶, ≤ 7% error; anchor point
86,332 pairs/kick at 10⁶ fixed extent), so 10⁹ in one belt costs 2×10⁴–10⁵ cores and the
working point requires the billion partitioned into ~10⁵ cells of ~10⁴ bodies — plus a new
does-not-fit: the shipped global U-index itself (16 B/body = 16 GB at 10⁹).

**Bottleneck.** Same as the original run (board: fitting 10⁹ in 8 GB; candidate work vs real
encounters), plus the checker's named gap: the 5-order extrapolation (n = 10⁴ → 10⁹) and the
unwired queue term. Gain: the budget's central constants now regenerate from shipped code at
10⁶-scale; the cell-partition requirement and the keying rule enter the b-h-live / root-clock
build as measured facts, and two per-body structures (keys 12 GB, index 16 GB) are priced out
of the design space.

## Evidence

Everything below regenerates: `bash run-bench.sh` (52 s, anchor + ladder + cells + soundness
+ heap, JSONL), then `python3 budget.py` (regenerates `budget-table.md` from `cascade.jsonl`).
Linux/x86 shared runner, load 1.3–2.9, single-threaded timed loops; the M1 factor 0.54 is the
frozen M1 anchor (4,345.4 µs) over this run's same shipped experiment (8,071.9 µs) — orders
only, the integrator re-measures.

- **The shipped anchor reproduces on current code** (`cargo run --release -p
  emergent-encounters -- kick`, its own spec): pairs/kick **812.8** (exact), us/kick 8,072,
  changed_fraction @ tidal eps **0.0024**, slack_skippable **0.9458** — the [S1] constants were
  real; implied M1 us/pair 9.93 × 0.54 = **5.35 µs**, the number the whole budget rode on.
- **The pairs law** (global Sorted, shipped kick path, eps 1e-9, horizon 1000 orbits):
  n=10⁴ X=1.5 → 866; 10⁵ X=1.5 (dilute ρ) → 8,284; 10⁵ X=15 → 1,975; 10⁶ X=1.5 (dilute) →
  86,333; 10⁶ X=150 → 18,704; 10⁶ X=15 → 20,926. Law `0.0346·n·(1+X)/(2(X−1))` fits all six
  within 7% (mean over a-uniform kicks; partners of a body ∝ n·a/W_a; belt mean saturates at
  0.0173·n). ρ only widens the cone marginally — dilution does not thin candidates (the
  q-candidate-degree asymmetry, confirmed on the kick path).
- **Per-pair cost is flat in n** (the 5-order extrapolation closed): us/pair 10.8 at 10⁴,
  4.2–9.3 at 10⁶ (working sets 5–100 MB) — no algorithmic growth inside the pair work; the
  anchor's 9.93 µs x86 / 5.35 µs M1 stands at scale.
- **The shipped global range bound degrades with belt width** (global κ from the belt-wide
  rmax): scanned/pairs = 3.8 at X=1.5 → 17 at X=15 → 51 at X=150; at 10⁷ X=1500 the case
  exceeded 300 s/kick and was not completed (the law extrapolates 1.7×10⁵ pairs/kick there).
- **Cells fix it, exactly sound**: geometric equal-count blocks (10⁴ bodies each) with
  per-block Sorted and union-extrema bounds — **candidate id sets identical to the global
  path, 30+30 kicks, 0 mismatches** (the control; sampling alone could not have shown this,
  per-body partner counts spread ±57%). Measured: scanned/pairs back to 3.4, us/pair 3.95
  vs 8.68 at equal geometry (2.2×), 6.2 blocks touched per kick, block index build 0.07 s
  per 10⁶ bodies.
- **The queue term** (the author's gap): Rust BinaryHeap, packed (u64 t, u32 id), steady
  pop+push churn: **176 ns/op at depth 7.8×10⁶** (the 10⁹/128 program-key count), 139 ns at
  2×10⁶ — the author's Python heapq 2.87 µs was 16× pessimistic. Wired in
  (`budget-table.md`): window-level keys, no skin **0.0318 cores** (2.4× below the skin
  cascade — the "≥ 3 orders" claim fails here); with skin 0.0017; cell-level keys
  (1 + 6.2 touched cells per kick, changed pair near-certain per touched cell) **2.8×10⁻⁴
  cores**. Window keys do not fit at any partition (4.3×10¹¹ windows × 12 B even cell-
  partitioned); per-body keys 12 GB; cell keys 94 MB.
- **Encounter rate corrected**: 0.04/body/orbit (scale.jsonl at the belt's own geometry), not
  the n=3000 steady.jsonl 0.00586 the original used; the term stays ≥ 4 orders below the
  cascade either way.

## Predictions (`predictions.md`, written before any output)

Held: the anchor reproduction (3: 812.8/0.0024/0.9458 exact); the global-bound degradation
(4: 3.8→17→51, cells 3.4); us/pair brackets (6); heap 100–600 ns (7: 176–188); both queue
terms (8: window 0.02–0.08 → 0.032; cell 1–5×10⁻⁴ → 2.8×10⁻⁴); enc 0.04 (9).
Failed, informatively: **extent-invariance (1)** — pairs/kick is set by n·mean(a)/W_a, not by
width alone (10⁵ at X=15 gives 1,975 vs 8,284 at X=1.5; the law above replaces it);
**the per-octave n-law (2)** as stated (coefficient is X-dependent; law fits ≤ 7%);
**cells give 812 pairs/kick (5)** — blocking does not change partner count, only scan cost
and locality; the lever is bodies per cell, not the index.

## What would make it wrong

- The law's one free constant (0.0346) is calibrated on Rayleigh σ_e = 0.01 belts; a colder
  belt scales it ∝ σ_e down to the ρ floor (eps_u), a fleet or formation breaks the random-pom
  assumption entirely (taleb-09b5's phase-neighbour certificate is the answer there, and this
  run does not re-measure it).
- The queue numbers are a binary heap at two depths on a loaded runner; a bucketed/calendar
  queue at root-clock ticks would be cheaper (the term is an upper bound), a concurrent queue
  under contention dearer. The churn model (1 update per touched cell, 813 per window-keyed
  kick) follows from measured changed_fraction and blocks-per-kick, not from a traced engine.
- Kick construction is one tidal eps (1e-9) everywhere; player burns (eps ≥ 1e-5,
  changed_fraction 0.088) multiply the queue and skin terms ~20–40× — the p99 corner the
  original named, still unmeasured at scale. H_live's distinction-creation rate remains
  unmeasured (the checker's other note; only the reabsorption ceiling is bounded).
- Nothing ran on the M1; all timings via the 0.54 factor anchored on the frozen M1 kick run.

**Cost of adopting:** none in code — the budget table now regenerates from shipped code; the
structural rules for b-h-live: (i) event keys are cell/program-level, windows live inside the
cell's own store; (ii) the billion is ~10⁵ cells of ≲10⁴ bodies at the anchor's local
geometry (or colder), because pairs/kick tracks 0.035·n·mean(a)/W_a in any single belt;
(iii) never a belt-wide U-index (16 GB). **Fit with PRINCIPLES:** "cost follows change and
entropy" (3) — the law prices the belt's actual entropy (n·a/W_a), not a density label; "the
memory floor is information-theoretic" (24) — a second per-body structure (the index) priced
out by measurement; "gates judge a representation" — the cells control held by exact set
equality, not by sampling agreement.

**The lens may have missed:** the second-author lens inherits the original's frame (a
steady-state table of means); the tails (a burn inside one cell, a resonance sweep, the
10⁷ corner that would not finish) are where the next inversion lives, and the 10⁷ timeout is
itself unexamined — I did not profile whether the wide-belt scan or the tangency windows
dominate it. The queue churn is measured on synthetic keys, never on certificate far-times
whose distribution (long-lived sparse events) may change cache behavior.
