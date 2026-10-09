# Dossier — inversion-2360: the train certificate is sound where the gold feared, and blind exactly there

## Claim (one sentence)
The co-orbital train certificate adopted from gold 20261006-0346-taleb-09b5 is **sound under the e-spread its author feared (0 misses, 0 false on 400 encounters)** — but its **engagement logic never engages there**: the Binet-L1 clump detector fragments any collisionless family with σ_e·a ≳ 2×10⁻³ into pieces covering 11–75% of bodies (train blind to 92–99.93% of family pairs, which fall back to the quadratic tier the gold killed), and in the bunched-eccentric corner it fires with a degenerate watch (63–91% of all pairs, 150–225× the pairwise tier's cost) because ζ compares the watch against pairwise setups instead of against real encounters.

## Bottleneck
The board's top scaling risk (candidate work must track real encounters) inside the newest adopted design; also pre-freeze red-team duty: both GLM and Codex are queued to build the co-orbital certificate this week, and the build that exists (20261006-1931-b-coorbital-cert-152e) died at 429 **before running one scene** — its 628-line `train.rs` had never been executed until this run.

## Evidence
Linux x86, 8 vCPU, < 200 MB, every command ≤ 7 s. Total compute < 20 s.

Reproduce (tree at a838a28):
```
git show origin/claude/lab-20261006-1931-b-coorbital-cert-152e:lab/results/20261006-1931-b-coorbital-cert-152e/work/patch.diff > /tmp/train.patch && git apply /tmp/train.patch
# then this run's own additions (sets fam/famf/famb + dc_mult), saved in work/patch.diff
CARGO_TARGET_DIR=/tmp/enc-target cargo build --release -p emergent-encounters
encounters train-verify phalanx   # controls (the gold's regime), 5 s
encounters train-verify rings    # σ_e ≤ 1.5e-3 bridge incl. mirror/uniform ϖ, 5 s
encounters train-verify fam      # families at the design d_c: the detector cliff, 7 s
encounters train-verify famf     # same families forced into one clump: the watch itself, 2 s
encounters train-verify famb     # bunched families at design d_c, 1 s
```
Scenes: `fleet(200, a=1±1e-5, e~Rayleigh(σ_e), ϖ uniform ±π, λ uniform | σ_λ)`, ρ = 1e-4, 2 orbits, seeds 41–49 (mine) + the build's seeds. Truth = every intra-clump pair, dense conservative advancement (no leak, per the gold's fix); method = the shipping pairwise tier; train = the dead build's module; independent solvers throughout (Halley/Newton, different step control).

1. **Controls held** (VOID-guard): 7 phalanx + 5 rings scenes — one clump, fired, **0 misses / 0 false on 474 encounters**, train 10–1800× cheaper per encounter than pairwise (2.4–3.8k vs 32k–4.7M evals). The gold's regime reproduced, including mirror and uniform-ϖ rings at σ_e·a = 10–15ρ.
2. **The detector cliff**: σ_e = 1.5e-3 → 1 clump (200 bodies); σ_e = 5e-3 → 24 clumps, 149/200 bodies, train sees 1,571/19,900 pairs; σ_e = 0.02 → 17 clumps, 36 bodies, 21/19,900 (0.1%); σ_e = 0.05 → 10 clumps, 22 bodies, 14/19,900 (0.07%). Bunched families fragment identically (20 clumps, 41/200). Cause: d_c ≈ 8·ε_max ~ 3×10⁻³ is ρ-scaled Binet L1, and e-vector spread (≈1.4σ_e) crosses it between σ_e = 1.5e-3 and 5e-3 — while ΔU (the actual co-orbital signal) stays ~4×10⁻⁵ throughout.
3. **Soundness held under e-spread ≫ ρ** (the gold's flagged worry): forced into one clump, families at σ_e ∈ {0.005, 0.02, 0.05}, uniform and bunched λ — **0 misses, 0 false on 123 encounters**. The ϖ-free bound |Δλ̄| ≤ δ(1+L_E) + K_v·p·|(ΔV,ΔW)| absorbs crossings; soundness does not need e-vector concentration, only the detector does.
4. **Watch cost is σ_e-linear where sound**: 130/501/1,337 pairs (0.7/2.5/6.7%) at σ_e = 0.005/0.02/0.05. But per-encounter the crossover flips fast: at σ_e = 0.05 uniform the pairwise tier is 68× cheaper (376 vs 25.6k evals/enc) — the train's sweet spot is σ_e·a ≲ 50ρ.
5. **The degenerate corner**: bunched (σ_λ = 0.02–0.05) + σ_e = 0.02 families forced clumped: ζ = 0.11–0.12 **fires**, watch 12,481/18,191 of 19,900 pairs (63/91%), train pays 1.09M/1.65M evals vs pairwise 7.1k/7.4k (**150–225× worse**), 0 misses for both. At n_c = 10⁶ this corner is a fluid (≈830 ships inside one ρ-window at σ_λ = 0.02) — no certificate tier serves it; the pairwise fallback's storage is the gold's own 72 TB-class arithmetic.
6. **Ruin arithmetic for the fragmented path** (gold's constants, orders of magnitude): a 10⁶-ship family at σ_e ≥ 5e-3 puts ≥ 92% of 5×10¹¹ pairs on the pairwise tier ≈ 10¹² crossings × 72 B ≈ 72 TB of sections against 8 GB — the 40 TB ruin the train was adopted to delete, resurrected one trigger upstream.

## Predictions
`predictions.md` written before any run. Held: controls (1), family soundness (4), watch fraction 2–6% and σ_e-linear (2, when clumped). Missed: the decline mechanism — I predicted ζ > 1 declines bunched families; reality is harsher (fragmentation at design d_c makes the train blind without declining, and forced clumping fires ζ = 0.11 with a 63–91% watch); and prediction 5 (pairwise misses ≥ 1% in families) failed outright — 0 misses on 277 family encounters; the gold's 4/233 window-tier misses are phalanx-specific (Full/Wide), not crossing-family.

## What would make it wrong
n = 200–300, one ρ, 2 orbits, 12 seeds: the cliff's exact σ_e and the 63–91% watch fractions are single-scale; the 10⁶ arithmetic extrapolates the gold's measured per-pair constants rather than measuring them. The bunched-fluid claim (830 ships per ρ-window) is arithmetic, not a run. If the real design clumps on U alone (a reading of "clump Binet diameter" I could not find in any shipped code — the built `clumps()` is full Binet L1), finding 2 collapses to a tuning note and 5 remains.

## Cost of adoption, fit with PRINCIPLES
One step before the certificate build is reviewed: (a) clump on U-concentration (shared orbit), not Binet L1 — the watch's own bound already prices e-spread per pair; (b) ζ must compare the watch to the real encounter rate (dormancy), and decline-to-pairwise when watch fraction → 1; (c) the bunched-eccentric corner is a third regime (fluid/contact lattice), out of certificate scope by the same number that detects it. Fit: "a fix signals the wrong representation" (#19) — the watch is the right water, the detector dragged the fish into the wrong pond; "regimes are chosen by dimensionless numbers" (#4) — σ_e·a/ρ and n_c·ρ/(spread·r) are the two that decide; "the cheapest compute is compute not done" (#1) — a fired 91% watch is compute done for no reason.

## The lens (what inversion made me miss)
Inversion searched for the kill in the watch's math (prediction 4 expected the bound to break) and found the failure one layer up, in engagement — a reminder that the cheapest falsification of a certificate is often not its soundness but its trigger. A dynamics lens would have derived the fluid threshold n_c·ρ/(spread·r) ≈ 1 before running; a scout should next run the n-scaling of the watch (200 → 3,200) and the U-clump detector variant, which is the one-step fix this dossier argues for.
