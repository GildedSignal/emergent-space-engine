# Dossier: the scar ledger's floor — a self-stirred belt at 10⁹

**Claim.** The live storage floor of a self-stirred 10⁹-body belt is set by the periapsis-time
(t_p) axis, which grows as ~1.5·log₂t bits per body (never linearly), so a program-plus-integer-
scar store with periodic refold holds the belt in 0.2–3.1 GB for 10⁵ orbits, while the naive
touched-body→16-byte-tube policy sits at 16 GB (2–87× the floor, and 1,016× at birth), and the
background H_live of the whole belt is ~1 bit per game-second at 100× real time — the 8 GB
budget is spent by player-driven distinctions, not by secular stirring.

**Bottleneck.** Board focus item "fitting 10⁹ in 8 GB (population programs plus scars) … decided
by distinctions created per game-second"; HANDOFF risk list: "H_live … not measured yet". This
run measures the floor side of B18's "≤ 2× information floor + 2 bytes" as a function of
stirring time, and hands `b-h-live`'s dashboard a control value. Expected gain: not a speedup
but a sizing decision (which grids and refold cadence keep 10⁹ real bodies inside the memory
budget), and the deletion of the fear that secular stirring can exhaust memory.

**Component and requirement (lens step 1).** The store of a live population (shipmem's scar
layer). Owner: PRINCIPLES 24, "The memory floor is information … 'why do you need so many bytes
per entity?'", and 6, "influences below one quantum accumulate". The naive alternative (every
touched body becomes a full 16-byte tube, law.md §Tube) violates the goal's 8 GB at 10⁹ bodies
outright (16 GB).

**Floor and gap (lens steps 2–3).** Floor = entropy of the integer residuals under the shared
population model, measured per axis (dE, dL, dϖ, dt_p) at the law's storage grids. Birth floor
is the known 0.126 bits/body (gold components-98bc); today's live plane stores plain tubes
(128 bits/body): **1,016× at birth**. This run measures how the floor grows in time and how the
naive policy's ratio behaves after stirring begins (2.4–10.5× at the finest grid, unbounded at
coarse grids where the ledger is empty but naive still writes tubes).

**Evidence.** Belt: a = 2.5 AU, width 0.5 AU, σ_e = 0.07, σ_i = 0.035, N = 10⁹, M_belt = 3×10²¹ kg
(real-belt mass), ρ = 2.5 g/cc. Encounters: impulse approximation, miss distance uniform in b²
between 2R and the mutual Hill radius, v_rel = 2.40 km/s from sampled Kepler pairs; per-band
compound-Poisson convolution on the storage grid (exact via the characteristic function; Gaussian
branch only under CLT conditions — cross-checked against Monte Carlo: analytic variance 2.135×10⁻¹⁹
vs MC 2.137×10⁻¹⁹; FFT entropy 5.30 bits ≤ quantized-Gaussian 5.51 at neff = 25).

- σ_dE/E = 1.45×10⁻¹¹·√(orbits) (so dσ ∝ M_belt/√N at fixed geometry; N-scaling spot check:
  ratio 3.162 vs √10 predicted). Ensemble spread after 10⁵ orbits is 4.6×10⁻⁹ of the birth
  spread: **the program's own entropy never grows; only the differential ledger does.**
- Store designs at 10⁹ bodies (bits/body, GB = bits/8; program 0.126 included; horizons in orbits):

| design | t=10² | t=10³ | t=10⁴ | t=10⁵ | refold K=10³ | naive |
|---|---|---|---|---|---|---|
| D1: 32-bit E/L words, clock 2⁻³²P | 12.2 (1.5 GB) | 24.8 (3.1) | 36.3 (4.5) | 46.9 (5.9) | **24.8 (3.1 GB)** | 128 (16 GB) |
| D2: 32-bit words, clock 2⁻²⁰P | 6.7 | 13.1 | 24.2 | 34.9 | **13.1 (1.6 GB)** | 128 (16 GB) |
| D3: 16-bit (E,L) keys, clock 2⁻²⁰P | 0.13 | 1.5 | 7.1 | 12.3 (1.5 GB) | **1.5 (0.2 GB)** | 35→128 |

- Axis split at D1, t=10⁵: phase (t_p) 24.1 bits, dE 10.8, dL 10.3, dϖ 7.7. The phase axis
  carries ~45% and grows fastest (a kicked body's perihelion drifts linearly in t: dt_p/P =
  0.75·1.5·(dE/E)·t), so **refold is required, not polish**: without it D1 crosses the plane's
  4 GiB budget (32 bits/body) at ~1.3×10³ orbits; with K = 10³ it holds 24.8 bits/body forever.
- Background H_live (whole 10⁹-body belt): **1.0 bit per game-second at 100× RTF**; 1.0×10⁴ bits/s
  at 10⁶×. Per body: 1.0×10⁻⁹ (100×), 1.0×10⁻⁵ (10⁶×) bits per game-second.
- Reproduce (each ≤ 60 s, idle machine, load 0.02, 8 vCPU): `python3 scar_floor3.py` (4.5 s;
  physics, per-axis entropies, JSON) then `python3 summarize.py` (1 s; the table above,
  `summary_out.json`). Seed 20261008.

**Predictions** (predictions.md, written before the decisive run). Held: κ = 1.00 (predicted
[0.3, 1.2]); N-scaling 3.162 (√10); phase-axis dominance and its ~1.5·log₂t growth; refold
bound; the bottom line (background H_live ≪ 10⁻³ bits/body/game-hour: measured 3.7×10⁻⁶).
Failed, and reported: prediction 1's σ level was 33× low — an arithmetic slip in my hand Fermi
(1.9×10⁻²² written as 10⁻²⁵); the simulation, its closed form and the Monte Carlo agree, so the
slip moved the predicted onset times (10⁴ → ~8 orbits at the fine grid), not any conclusion's
shape. Held-out cases behaved as the formulas say (M×10 ⇒ onsets ×10⁻²; grid sweep j16/j24/j32).

**What would make it wrong.** (1) The toy's encounter statistics (impulse approximation,
isotropic projections, slab volume) — the level σ̇_E is model-based; a factor-2 density or
projection error moves ledger bits by ~1, not the log-shaped conclusions (the N-scaling and κ
checks passed, and the real-belt anchor is consistent: mutual stirring of km bodies is
negligible vs planetary stirring over 10⁹ orbits). (2) The grid anchors: the doll's actual
shared exponent and clock quantum decide where between D1 and D3 the plane sits; I report the
sweep, not one point. (3) Not modelled: resonances with planets (never averaged — real-time
kicks in localized zones), physical collisions (a 10⁹-body belt has ~2×10⁻⁶ collisions per
second at 10⁶×, each a genuine contact event), and the player term. Those are exactly the terms
`b-h-live`'s dashboard must measure; this run is the quiescent baseline it should be judged
against. (4) Floor overcount: dE and dL respond to the same events (correlated, −1–2 bits) and
encounter pairs are momentum-anticorrelated across the two bodies (−~50% if the ledger codes
pairs): the true floor is another ~2–3× lower. **Cost of adoption:** shipmem's scar layer
becomes integer deltas coded against per-population σ models (it already stores exact sparse
differences, law.md §Populations), plus a refold pass in idle time (PRINCIPLES 17) when the
phase ledger crosses a bit budget — cadence from the measured formula. Nothing in the law or
digests changes (scars are already exact state). **Fit with PRINCIPLES:** 24 ("the memory floor
is information"), 6 ("influences below one quantum accumulate" — the sub-quantum accumulator is
what keeps D3's ledger near zero), 21 ("rough first, refine when a certificate could break" —
refold is that refinement, on a measured cadence).

**The lens (what first-principles-one-component may have missed).** A local optimum can move
cost to neighbours: I sized the *store*, not the refold's compute (bounded, idle-time, same
class as the birth program — but unmeasured here), and not the encounter-finding cost that
r8/q-candidate-degree own. The toy is one belt at one stirring regime; a fleet in tight
formation (the co-orbital gold's concentration) has far higher local H_live per body, and I did
not measure that case. The quiescent result also risks being read as "memory is solved": the
player term — burns, battles, contacts — is unbounded by this analysis and is the term that can
actually exhaust 8 GB.

**Grade suggested: silver.** Real, reproduced, with held-out predictions held and one honest
miss disclosed; one step from gold: wire the ledger-plus-refold rule into `crates/shipmem` and
show B18's "≤ 2× floor + 2 bytes" holds at stirring horizons on the belt ladder (that build is
`b-belt-wire`'s to make; this run is its floor side).

*Bug history (disclosed): v1 measured plug-in histogram entropy, which saturates at log₂(n_samples)
and overestimated ledgers by up to ~10 bits/axis; v2 double-quantized the phase axis (E-grid
then clock grid), undercounting it by ~log₂cq; v3 measures both exactly and was cross-checked
against Monte Carlo. A debugging Monte Carlo of my own had a per-band sign bug; the shipped
v1/v3 simulations never had it (binomial split).*
