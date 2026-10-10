# Dossier — 20261010-0352-spacex-2dca (spacex lens)

**Claim.** H_live is measured for the first time on the post-pivot engine — distinctions run at 1.98×10⁻³ per body per orbit at the belt's measured optical depth (1.6×10⁻¹¹ per body per game-second at a = 2.5 AU), the candidate bookkeeping stream outnumbers real distinctions 257:1, and at 10⁹ bodies **memory never binds (four orders of margin on every term) — the wall is pure CPU at galaxy real-time factors**, with two numeric design targets: ship the slack certificate (18× on the ceiling) and get the per-conjunction evaluation to ≤ 500 ns (2 cores at RTF 10⁶) or ≤ 50 ns (belt free).

**Bottleneck.** The board's "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" (HANDOFF risk: "not measured yet") plus the top scaling risk. Expected gain: deletes the memory side of the 10⁹ question outright and converts "finding encounters without work per orbit or per element change" into two freezable numbers. Orders of magnitude only (cloud x86; the integrator re-measures on the M1).

## Evidence

Machine: GitHub Actions runner, 8 vCPU x86, 15 GB, 1 GB used at start, release build, THREADS=4. All runs ≤ 60 s. Raw JSON: `raw/measurements.jsonl`; derived: `raw/ceilings.json`.

Reproduce (from the repo root; each command ≤ 60 s):

```
cargo build --release -p emergent-encounters
cd crates/encounters
cargo run --release -q --bin encounters -- steady 1000 0.0001 5 10 50
cargo run --release -q --bin encounters -- steady 2000 0.0001 10 50
cargo run --release -q --bin encounters -- steady 10000 0.0001 10 50
cargo run --release -q --bin encounters -- steady 1000 0.001 10 50
cargo run --release -q --bin encounters -- kick
python3 lab/results/20261010-0352-spacex-2dca/ceilings.py
```

Measured (n=1000, ρ=10⁻⁴, annulus [1,1.5], σe=10⁻² — the "1×" optical-depth point):

| quantity | value |
|---|---|
| distinctions (real encounters) per body per orbit | 1.98×10⁻³ |
| candidate-pair conjunctions per body per orbit | 0.509 |
| bookkeeping : physics | **257 : 1** |
| candidate pairs per body (cone tier) | 41.9 |
| full setup per pair | 3.2 µs |
| kick re-certification, 1000-orbit horizon, 1× density | 1.56 ms (no slack) → **84.5 µs with slack** |
| slack skip fraction at ε=10⁻⁹ | 94.58 %, **0 violations** |

Scaling law (the controls): rate ∝ n·ρ — 1.92× at 2× density, 10.1× at 10× density, 10.25× at 10× ρ (spread 6.6 % across the four points). Scale-invariant in N at fixed optical depth: per-body rates do not grow with N; this is the regime the 10⁹ extrapolation assumes.

Derived at 10⁹ bodies, belt at a = 2.5 AU (T_orbit = 1.25×10⁸ s), 4 performance cores (see `ceilings.py`):

| | RTF 10² | RTF 10⁴ | RTF 10⁶ |
|---|---|---|---|
| encounters, no slack | ~0 | 0.25 | 24.8 cores |
| encounters, slack | ~0 | 0.01 | 1.34 cores |
| conjunction stream @ 500 ns | ~0 | 0.02 | 2.04 cores |
| conjunction stream @ naive 3.2 µs setup | ~0 | 0.13 | 13.2 cores |

RTF ceilings on 4 cores: 1.6×10⁵ (no slack) → 3.0×10⁶ (slack); conjunctions 2.0×10⁶ @ 500 ns, 2.0×10⁷ @ 50 ns, 3.1×10⁵ naive.

Memory at 10⁹, RTF 10⁶: program store 15.75 MB (0.126 bits/body, gold components-98bc); scars 0.2 GB at 1 % scarred; scar write traffic 0.32 MB/s; conjunction traffic 0.26 GB/s even at one 64 B cache line per event. **Every memory term has ≥ 4 orders of magnitude of headroom against 8 GB / 60 GB/s.** The scar store at ~20 B/distinction sits ~2.4× above the raw information of a distinction (tens of bits) — already near the floor.

## Predictions

`predictions.md` was written before the decisive runs. Outcome: **P1 missed low** (measured 0.00198, below my [0.005, 0.08] interval — space is emptier than my prior); **P2 held** (linearity within 4 %); **P3 missed high as written** (12.5 ms per kick at the experiment's own n=10⁴, 2.5× over my upper bound; at 1× density the comparable number, 1.56 ms, lands inside my range — the miss is real and mine: I under-guessed the per-kick pair fan-out); **P4 split** — no-slack ceiling 1.6×10⁵ < 10⁶ as predicted, but the slack path (3.0×10⁶) crosses 10⁶, so the "live fraction < 1 %" consequence vanishes if slack ships; **P5 held with 5 orders of margin** (my pre-run bandwidth worry was a 10³× mental arithmetic error, caught by making the script the authority); **P6 held** (0.2 % of RAM).

## What would make it wrong

- **Operating point:** the 1× point is a smooth Rayleigh belt. Concentrated regimes (formations, the co-orbital gold 20261006-0346) sit outside the optical-depth law; there the 4–6 % contact misses and quadratic setup apply, and this dossier says nothing about them.
- **Density:** all rates scale linearly with the game's chosen optical depth; a belt 100× denser divides every ceiling by 100.
- **Tails:** the law is a mean over one seed per configuration. Kick clustering in chaotic scenes would put the tail, not the mean, in charge (Julien: averages crush tail events). Single seed is a real weakness of this run.
- **Horizon:** the kick cost carries a 1000-orbit certificate horizon; a shorter horizon cuts the 9.5–15 µs/pair re-scan roughly proportionally.
- **Unmeasured:** the motion-law recompile per kick (the plane recompiles on ~99 % of kicks, per the taste log) is not costed here; and game-seconds are assumed to be real seconds (a = 2.5 AU → T = 1.25×10⁸ s).

## Cost of adoption, and fit with PRINCIPLES

Adoption is two numbers into the encounters design (and optionally a rung criterion: per-conjunction work ≤ 500 ns at 10⁹, RTF 10⁶, 4 cores): no code change. It deletes the memory-risk work item ("10⁹ in 8 GB" is answered: it fits with ~10⁴× margin; what decides is CPU time per conjunction, not bytes).

- Principle 3, "Compute only surprises. Cost follows change and entropy": measured — the surprises are 1/257 of the stream the discovery layer touches; the lever is the bookkeeping, not the physics.
- Principle 24, "The memory floor is information": measured — the floor is nowhere near binding at 10⁹; the binding resource is the M1's seconds.
- Principle 10, "Measure before claiming": the board's "190 cores for 10⁹" Fermi (29 September engine) is replaced by measured ceilings on the current discovery layer (not directly comparable: that number priced evolving orbits, this prices discovering distinctions).

## The lens

SpaceX's idiot index pointed me at ceilings and made me treat the belt as a uniform fluid; it made me miss that the game's belts will be structured (families, resonances, fleets), where the pairwise tier already broke once (taleb-09b5) and where my scale-invariance law does not reach. It also biased me toward the mean over seeds and against measuring the recompile — the one cost the motion law owns. And the lens's own warning applies: two of my six pre-registered predictions failed, both in the direction of my priors overreaching (space emptier, fan-out fatter than guessed) — the run was worth it precisely because of those.
