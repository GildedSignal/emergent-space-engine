# Dossier — 20261021-0429-quant-a97f (quant lens)

## Claim

The calendar's standing post-mixing worst-window load excess is priced and attributed, and it is neither of the page's two candidates: it is **not** slow-shear a-neighbourhood (co-firing pairs are spatially unlocalised) and **not** the step lattice (zero exact collisions) — it is ~57–85% the dues' own marginal non-uniformity across the fire window (the genesis train's remnant at window scale, C50(dues) 1.19–1.22 flat through g = 25–40) plus a N-flat ~+0.13 pairwise part from phase-aligned near-locked pairs (|Δs|/s < 10⁻³, 17–20× enriched over random pairs), and **both halves are a ~10²-fire transient**: with steps frozen (conservative), the load reaches the Poisson floor by fire ~100–120, so the worst frame at 10⁹ may assume Poisson windows only after ~10² fires ≈ one game-month past the last coherent clumping — or immediately, with the already-flight-proven hash stagger.

## Bottleneck

The board's macro row "kicks per body" and the smoothness/allocator principle (P12): the calendar page's od 4 held the 10⁹ worst-frame number hostage to "this uncertainty, not 1.05×" (checker: max/μ 1.54–1.92 flat g = 25–40 at 2,700; 1.83 at 11,700, "relative excess grows with μ"). This run resolves it: the excess is a priced transient with a named mechanism, not a standing N-growing structure — the ×573 live-sizing and the stagger adoption sentences no longer carry an unbounded tail caveat. Deletes the need for any standing-tail mitigation at 10⁹ (beyond the stagger already measured).

## Evidence

Instrument: 45c0's genesis census reused verbatim (patch applies clean at this tree) + a per-generation full dump (`census_*.tsv`: g, id, due, step, a). Shipped `plane_extra`, seed 1; belt 2,700 (g ≤ 40, 225 s) and 11,700 (g ≤ 20, 112 s). All numbers from `analyze.py` / `evolve.py` (≤ 22 s), floors from 4,000 uniform placements.

- **The excess reproduced:** 2,700 late (g ≥ 25) max/μ median 1.720 vs Poisson floor 1.375 [p10 1.280, p90 1.470]; p99/μ 1.600 vs 1.304. 11,700 at g = 20 reads 1.83 — the checker's number exactly.
- **Model validity (P1 held):** one-fire-ahead per-ship error p50 6.4×10⁻⁵ periods (0.004 windows); predicted max/μ 1.801 vs measured 1.790. Floor control A4 (uniform phases) lands exactly on 1.375.
- **Decomposition (2,700):** resampling dues i.i.d. from their own marginal (A6) keeps max/μ at 1.564 — the **marginal carries 0.19 of the 0.33 excess (57%)**; the remaining ~0.14 (43%) is destroyed by permuting either steps (A1 → 1.588) or phases (A5 → 1.564), and untouched by step jitter at 10⁻⁵ or 10⁻³ (both 1.707).
- **The pairwise part is locking without locality:** persistent co-firing pairs (same window at g and g+1, 637k counted) have |Δs|/s = 3.9×10⁻⁴ vs 1.4×10⁻² for random pairs (36×), 72% below 10⁻³ vs 4.2% (17×); |Δa| 0.268 AU vs 0.292 random (−8% — **not** a-neighbours); **exact step collisions: 0**.
- **Persistence:** window-count autocorrelation 0.535 (2,700) / 0.726 (11,700) across consecutive fires — clumps rotate rigidly between fires.
- **11,700 (μ = 182.8, anchors g = 14–19, C50 1.45–1.55):** measured 2.23 vs floor 1.176; A6 1.904 (85% of the 0.86 excess is marginal there — an earlier mixing depth); the pairwise part is +0.13, the same as at 2,700 — **N-flat**. The checker's "excess grows with μ" is the floor shrinking (1.375 → 1.176) under a clumped pattern whose max stays a fixed ratio above its mean, not a growing correlation structure.
- **The transient (evolve.py):** evolving the g = 25 census with constant steps (drift omitted — the measured step drift, 5×10⁻⁴ → 2.5×10⁻³ per fire and growing, only accelerates mixing, so this is an upper bound on the epoch): max/μ 1.68 → 1.47–1.66 (fires 13–40) → 1.30–1.38 at fires 100–120 = floor. Window-scale mixing completes in ~10² fires, ~6–8× the C50 mixing time (13–16 fires), not the naive 64×.
- **The 10⁹ line:** during the epoch the worst window carries the marginal peak, ×1.2–1.6 of mean load (N-independent multiplier, μ-scaled count); after ~10² fires — or from birth with 45c0's stagger, which lands the belt at the floor at genesis — windows are Poisson and the worst frame is the iid floor.

Reproduce: `bash lab/results/20261021-0429-quant-a97f/regen.sh` (~9 min: two flights 225 s + 112 s, then the analyses; the flights exceed 60 s — they are the shipped instrument's own cost, unchanged from 45c0's regen).

## Predictions

`predictions.md` was written before the counterfactual analysis (the 2,700 flight was still running). **P1 held** (model valid to 0.004 windows). **P2 failed its letter** (shuffle removes 38–43%, not ≥50%) — and the failure is the finding: both shuffles preserve the dues multiset, which is where most of the excess lives. **P3 held/failed as registered** (A2 <20%: exact commensurability is nil — 0 collisions; A3's ≥40% at window scale: 0%). **P4 failed** (cf |Δa| is −8% vs random, not <0.5×): the shear-neighbour mechanism is dead as the source. **P5 held** (0.535/0.726 vs floor control). **P6 was revised by the measurement**: the pairwise part is N-flat and the μ-growth is the floor shrinking — no pair-count explosion to quote.

## What would make it wrong

- The arms run on a constant-step model valid to ~15 fires (calibration); the arms sit at horizon 5, inside validity, but the decay epoch (fires 40–120) is model-extrapolated with frozen steps. If the real step drift ever *re-clumps* dues (it has only been observed to spread them), the epoch could be pumped rather than exhausted — an engine flight to g ≈ 120 (about 11 min at 2,700) is the named closing experiment.
- One seed per N; the decay curve is one realization and oscillates (1.33–1.78) rather than monotone.
- The 11,700 anchors are pre-saturation (C50 1.45–1.55); at matched mixing depth its marginal/pairwise split would read closer to 2,700's 57/43.
- The window statistic is the flight's own (64 windows per step, the shipped instrument); other widths unflown. If the allocator's true unit is the heap's burst rather than fixed windows, the decomposition transfers but the numbers rescale.

Cost of adopting: none in engine code — it prices the ledger line and closes od 4; the cure (the hash stagger) is already measured and exact. Fit with PRINCIPLES: "Compute only surprises. Cost follows change and entropy. Nothing is evolved that can be derived when looked at" — the epoch's worst window is derivable from the birth census, so the allocator can be sized ahead, not reacted to; and "judge behaviours over many seeds and look at the worst cases" — the worst case's source is now priced, including my own wrong prior.

## The lens

The quant lens's tail-decomposition instinct (marginal vs pairwise, controls on both sides, kill criteria pre-registered) is what split the excess; but its "correlated clusters scale with N" prior (from market microstructure, where clustering is adversarial) is exactly what the measurement killed — the pairing here is a frozen birth artifact, N-flat, and self-decaying. What the lens may miss: the allocator does not experience fixed 64 windows, and a market has no analogue of "the schedule is derivable at birth" — the cheapest mitigation here is not a faster queue but precomputation.

## Wiki

`wiki/calendar.md` updated: od 4 executed (source priced, stagger scoped as the cure); new refuted lines (shear-neighbourhood; step-lattice; "excess grows with N"); run appended.
