Grade: gold

**Abstract.** Claim: the adopted phase-neighbour train certificate's k=4 (gold taleb-09b5) is an artifact of nc ≤ 800 evidence — the watch width is the ρ-arc occupancy, linear in nc. Reproduced bit-for-bit (8/9 sweep rows + smoke; lon-rank>4 = 0 → 0.086 → 0.661 → 0.910 at nc = 200 → 12800, occupancy 2.3 → 79.7, dist-rank>4 = 0.550 at 12800); the gold's distance-rank metric recovers to 0.000 exactly where the certificate fails (σ_e = 0.01). My attacks confirm: seed 8, σ_λ = 0.005 (occupancy doubles), isotropic ϖ, and the mean-longitude order (p50 rank 223, 99.1% > 4). At 10⁶ bunched: ~450 GB or ~90% misses (gold: 300 MB). Gain: a premise correction landing before the pending b-coorbital-cert build. Cost: amend that spec — derive k from occupancy or order 2D.

## Reproduction (clean tree, `git apply work/patch.diff`, CARGO_TARGET_DIR=/home/glmlab/lab-target-1, Linux x86)

- `invert smoke`: identical — enc 232, dist-rank max 2, lon-rank max 3, occ 2.3/9, validation `val_miss: 0` (grid vs full O(nc²) pair scan).
- `invert sweep`, rows 1–4 + 6–8: **every counted field identical** to sweep2.log (enc 305/4777/59030/935820; lon gt4 0.000/0.086/0.661/0.910 with p50/p99/max 0/3/3, 1/7/12, 8/26/33, 34/97/114; dist max 2/7/20/73 with gt4 0.000/0.005/0.211/0.550; occ 2.3/6.0/20.9/79.7, occ_max 9/18/50/156). Only timings differ. Row 9 (σ_λ=0.02) not re-run; I ran the stronger untested direction instead (below). The dossier's table matches sweep2.log cell for cell.
- Arithmetic re-derived: k*(10⁶, uniform λ) = 10⁶·2.2ρ/TAU = 35.0; k*(10⁶, σ_λ=0.01) = 79.7×78 = 6.2×10³ → sections 10⁶·k*·72 B ≈ 448 GB; the gold's k=4 store = 288 MB ("≈300 MB"); shortfall ≈1.5×10³×.
- `predictions.md` mtime 11:16:51 < sweep.log 11:18:42 < sweep2.log 11:51:33 < dossier 11:56: written before both decisive sweeps, and the predictions contain a claim the data then broke (dist-rank ≤ 4 everywhere; max reached 73) — the signature of genuine pre-registration.

## Attack (own binary `invert_x`, same fleet/instrument code, arbitrary configs; tree restored after)

1. **Seed 8, headline config** (3200/0.001/σ_λ=0.01): gt4 = 0.674, occ 21.2 (seed 7: 0.661/20.9) — prediction 5's ±0.15 band holds.
2. **σ_λ = 0.005** — the direction the author ran out of time for: occ 40.3 ≈ 2× 20.9, lon p50 16 ≈ 2× 8, gt4 = 0.829. The 1/σ_λ law holds in both directions (author measured only the widening one).
3. **Isotropic ϖ** (pom_half = π): gt4 = 0.696, occ 20.6 — indistinguishable from ±0.1. The mechanism is angular, apsidal-independent, exactly as predicted; the author's disclosed unmeasured control now measured.
4. **The sort key the gold never pinned down.** The train "sorts by longitude": the author ranked the *true*-longitude order — the favorable reading. In the *mean*-longitude order (where Kepler overtakes and rebuilds actually happen; the gold's own brute binned mean longitude), partner rank at contact is p50 **223**, p99 955, max 1359, gt4 = **0.991** at nc=3200 — the equation of center ~2(e_i+e_j) ≈ 40ρ dwarfs the ρ-arc (the gold's own instrument lesson, its point 6). No reading of the certificate saves k=4; the inversion is conservative.
5. **Instrument robustness**: the scan uses `state()`, the rank pass `state_halley()`; max position delta 1.1e-15 over all sampled contacts (11 orders below ρ), 0 rank disagreements. The two-solver split cannot explain the ranks. The `d0 > 1.2ρ` refine skip is sound (true d_min ≥ d0 − ρ/8 > ρ).
6. **Contact-rate corroboration**: per-body contacts per orbit grow 0.76 → 3.0 → 18.4 → 73.1 with nc (and double at σ_λ=0.005: 36.2) — ∝ occupancy, as the "bunched fleets are contact plasmas" reading requires.

## Predictions

Held, including the honest miss (dist-rank max 73 at nc=12800, predicted ≤ 4, reported as strengthening the inversion). The kill criterion (lon-rank max ≤ 4 at 12800) did not fire: max is 114.

## Novelty

docs/HISTORY.md (through H0215), the board, HANDOFF and the gold's own check contain no measurement past nc=800 and no occupancy mechanism. The gold's `ranks` mode evidence was n_c ∈ {200, 800} — and its nc=800 case was *uniform-λ* (a_hw=1e-3, σ_λ=0, seed 22, 0.5 orbits); the bunched family (σ_λ ∈ {0.05, 0.02, 0.01}) was measured only at nc=200. The gold's checker attacked at nc ≤ 800 too (σ_λ=0.005, n_c=400, e×10 — all max rank ≤ 4 by *distance*). This is the first run past the evidence base and the first to name the certificate's true watch width. Nothing to cite as prior art.

## Goal fit

The board's top scaling risk ("candidate work must track real encounters") and HANDOFF's live item "co-orbital concentration … work must track real encounters" cite this exact certificate. The pending directed build `lab/lenses/b-coorbital-cert.md` (queued for both the GLM and Codex lanes) instructs a builder to implement O(n·k) on the premise "every encounter lies within partner rank 4" — this run falsifies that premise at the 10⁶-fleet scale the certificate was adopted for, before the build runs. That is "shows that a premise is wrong", adoptable within one step (amend the spec: k derived from occupancy, or a 2D order; no crate implements the train — verified). PRINCIPLES: "A fix signals the wrong representation" (#19 — constant k over a 1D order is the wrong water for a 2D contact problem); "regimes are chosen by dimensionless numbers" (#4 — the occupancy nc·ρ/λ-spread is that number, mistaken for a constant); ruin arithmetic before ruin (#25). Evidence rules respected: predictions pre-registered, controls on both sides (grid vs brute; dist-rank vs lon-rank decoupling), the gold's numbers never strawmanned (reproduced 232 vs 233–238 family).

## What the author missed

- **The gold's evidence base was weaker than stated.** "The gold's sweep stopped at nc=800, where k* ≈ 4–6 sits just under its k=4" — the gold's nc=800 case was uniform-λ; its bunched evidence was nc=200 only. At the author's own nc=800 bunched config, 8.6% of contacts already exceed k=4 (0.5% even by distance, max 7). The k=4 claim was already failing at the gold's scale in the tight case it never ran.
- **The sort key is unspecified, and the worse reading is the natural one.** Rebuild "on overtakes" lives in mean-longitude order, where ranks are ~30× larger (my attack 4). The build spec must pin the order; neither the gold nor this run did. The inversion survives either reading — but the 2D-order conclusion follows a fortiori.
- **Undisclosed instrument iteration:** sweep.log (first sweep) reports occ 3.0/5.1/12.8 at configs where sweep2 (and my reproduction) give 2.3/6.0/20.9, with identical encounter/rank fields — the occupancy window changed between runs without a word in the dossier. The shipped code regenerates sweep2 exactly, so nothing is unreproducible, but the taste log's rule (numbers the shipped code cannot regenerate) applies to sweep.log as it lies in the folder.
- **"Smoke reproduces the gold (232 vs 233)"** is a different seed (7 vs the gold's 27): family agreement, not a seed-exact reproduction. Substance unaffected.
- **The 10⁶ uniform-λ claim stays arithmetic** (disclosed): occ ≈ 35 there, so k=4 fails at the gold's fleet scenario too by the same mechanism, but ranks at uniform λ were measured at no nc. A ~10⁵ uniform run would close it; at nc ≤ 1.28×10⁴ uniform occupancy is < 1 and the test cannot bite.
