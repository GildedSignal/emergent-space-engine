Grade: gold

**Abstract.** The claim reproduces exactly and survives adversarial attack: the phase-neighbour train adopted this morning (taleb-09b5) has k ∝ true-longitude line density, not k = 4. Full ladder regenerated bit-for-bit (`python3 probe.py` in a clean copy): μ̂ linear in n (μ̂/n = 7.0–7.5×10⁻⁶ over n = 12.8k→256k), k=4 silently misses 3.4% of real encounters at 128k and 17.7% at 256k; at the gold's own n=800 an ϖ-aligned formation puts 29% of encounters beyond distance-rank 4 (max 23). My fresh seeds (256k: 17.0–18.9%; 128k: 3.3%), a random rank subsample (no bias: 17.0% vs 18.9%), S=256 resolution, and a 3D inclination variant all confirm. Gain: it reopens this morning's adoption before the certificate ships — the premise "rank 4, O(n·k)" is wrong at the 10⁶ scale it was adopted for. Cost of adoption: zero build; the integrator drops k-as-constant and takes the ρ-wide radial-phase strata as the design hypothesis to test.

## Reproduction

- `work/patch.diff` is empty; `probe.py` is self-contained. Copied to /tmp and run whole (`python3 probe.py`, 288 s, < 1 GB): **every statistic in every case identical to `all.log` and to the dossier table** (checked field by field, C0 through X1 and the nest check 44/44). Only wall times differ (shared machine: X1 181 s vs the author's 182–194 s).
- Extrapolation arithmetic verified: μ̂(10⁶) = 7.2 from the measured μ̂/n; raw Poisson(7.2) tail gives 84% miss at k=4 (the dossier's 94% sits between this and the capped empirical calibration — the measured points sit 4.6–48× above raw Poisson, so "misses most" is robust; 94% itself is not a number); Poisson p99.9 → k ≈ 17 (dossier: 16); store 10⁶·16·72 B = 1.15 GB (dossier: ~1.1 GB; gold's k=4 → 0.29 GB ≈ its "~300 MB").

## Held-out predictions

- The anchor (C0) reproduced the gold's own observation first — no strawman: ranks ≤ 4, zero misses on the gold's workloads at n ≤ 800, then the break is demonstrated elsewhere.
- Load-bearing predictions held: linear μ̂ ∝ n (4 points, factor 20 in n); miss emergence (0 → 0.24% → 3.4% → 17.7%, X1 just above the registered 8–16% band, disclosed); distance-rank resilient under ϖ-random workloads; the ruin arithmetic's direction (store ~4× low, setup ×4).
- Failed honestly and disclosed: the pre-registered bunching mechanism was wrong (σ_λ-axis flat at μ̂ 0.17–0.18 — itself a clean negative: the gold's phalanx adversarial cases probed an axis the physics decouples), re-registered before D/X1 (file mtimes consistent with this; not independently verifiable from the restored tree); the amended D magnitudes over-predicted ~2.5× (trend held).

## My adversarial cases (four, all pass)

1. Fresh seeds: X1 seed 15 → miss(k=4) λ = 18.9%, μ̂ 1.96; C3c seed 71 → 3.3%, μ̂ 0.98. Not seed artifacts.
2. Sampling bias in the rank cap: the author ranks the first 2500 encounters by earliest argmin step (0.12% of X1's 2.1M). Random 2500 subsample measured in the same pass: X1 17.0% vs 18.9%, C3c 3.2% vs 3.3% — unbiased, though the author neither flagged nor tested it.
3. Resolution: C3c at S=256 (halved step) → miss 3.8% vs 3.4% at S=128. Sampled dips are not manufacturing the misses.
4. Inclination (the author's declared blind spot, asserted not run): i ~ Rayleigh(1e-3), 3D detection. Encounter rate falls 33× (2.06 → 0.063/body/orbit) exactly as claimed ("z can only thin crowding"), and the surviving encounters still carry μ̂ 0.79 with miss(k=4) λ = 2% at 128k while dist-rank collapses (max 2) — confirming the mechanism: interlopers are λ-close, 3D-far.

## Novelty

No HISTORY entry (latest is H0214, 5 October) covers the train's k-scaling; the target gold was adopted this morning per the board's taste log. Nearest records: H0212 (the off-time lab's 39 results, q-candidate-degree's fixed-density O(N²) risk) and the board's top scaling risk. This run answers it for the train specifically: at fixed distribution the train's O(n_c·k) is O(n_c²·ρ/W_λ) — the same ruin it deleted. Differs from r8 v2 (30 September, other algorithms' exponents) in mechanism and target.

## Goal fit

Direct hit on the board's top scaling risk, and a premise kill of an adopted certificate at the exact scale it was adopted for (the 10⁶ formation fleet that motivated the gold). PRINCIPLES #19 "a fix signals the wrong representation" — a 1D longitude sort is the wrong water for a 2D contact; #4 "regimes are chosen by dimensionless numbers" — the operative number is ρ·d_λ, not σ_λ; #13 "errors never compound" — the misses are silent (the train replaced the tier that would have found them) and enter the canonical history. The one honest caveat, disclosed by the author: the gold's binary is not in this checkout, so the attack reads the board's quote of its claim; the anchor reproduction makes a strawman unlikely.

## What the author missed

- The rank-cap sampling (first-by-step 2500) was unflagged and untested; it happens to be unbiased (my check 2). Luck, not design.
- The 94% headline is calibration-dependent (84% raw Poisson); "most encounters missed" survives, the specific number does not. The 10⁶ claim rests on a measured line plus tail argument, not a direct run — disclosed, and n=256k at 17.7% direct makes it hard to doubt the direction.
- The radial-phase strata repair is stated, not tested — that is the next run: show k collapses to O(1) within ρ-wide strata on the same ladder (including the D-series formations), which converts this premise kill into the replacement certificate.
