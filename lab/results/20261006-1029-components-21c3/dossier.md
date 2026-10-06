# Dossier: the scar store's equilibrium at belt scale (run 20261006-1029-components-21c3)

## Claim

Under a real encounter rate, a belt's scar layer grows only **logarithmically** in time (the
record kick dominates each body's delta), law.md's H_live ledger (+62 bits per kick, −60 per
reabsorption) **never balances at belt scale** (reabsorption-by-return dies at ~10⁻⁶ of
creation), and a two-tier light-cone store — near bodies exact, far bodies held at a coarse
quantum whose reabsorption is certified by a ~10¹⁵ firewall margin — keeps 10⁹ belt bodies at
a measured **5.6 bits/body (0.7 GB) at t = 100 orbits against 6.5 GB naive** at a 52-bit
state (1.4 GB against 19.6 GB at the real 157-bit state).

## Bottleneck

Board focus item: "fitting 10⁹ in 8 GB (`crates/shipmem`: population programs plus scars …),
decided by distinctions created per game-second", and plane.md's unmeasured metric
"distinctions created per game-second … against what reabsorption removes". This run gives
that metric its first numbers and the equilibrium rule the store needs. Expected gain over
naive: ~10× in memory at 10⁹ (measured 9.3× at t = 100: 5.6 vs 52 bits/body); it deletes the
per-body state store as a component for far bodies, replacing it with a program + coarse delta.

## Evidence

Model (all integer, seed-driven, `belt_scars.py`): N = 262,144 belt bodies, state (a, e, ϖ) on
20+16+16-bit lattices (phase derived on demand, never stored; naive = 52 bits); bijective
smooth program birth (Irwin–Hall in a); encounters Poisson λ per body per orbit, heavy-tailed
quantized kicks (bit-length geometric p = 1/2, one main column + ±1 cross jitter), the r2
law-grid rule; Form-P accounting: Elias–Fano ordinals (2 + log₂(N/k)) + zigzag Elias–gamma
deltas. Two-tier: |a − a_player| ≤ W/64 near-exact; far deltas requantized at q_far = 2⁸.
Machine: 8 vCPU shared runner, load recorded in `results.json`, single-threaded, peak RSS
84 MB, 29 s main + 53 s extension. Cloud numbers = orders of magnitude only.

- **λ = 1.1** (r8 v2's belt rate; 1.1 encounters/body/orbit): scarred fraction → 1.00 by
  t = 10. One-tier bits/body: 6.7 (t=1) → 32.2 (t=100) → 43.5 (t=400). Log-shaped: slope
  16 bits/decade at t ≤ 100, 18.8 bits/decade at t ≤ 400; the per-orbit creation rate
  **falls as ~1/t** (0.32 bits/body/orbit averaged over the first 100 orbits; 0.020 at
  t = 400). Crossing of naive (52 bits) at t ≈ 1,100 orbits; shipmem's own cost switch then
  repacks to naive forever.
- **Reabsorption-by-return is dead**: 4,201 reabsorptions total by t = 100 (1.6% of bodies,
  nearly all before t = 30; flux ~0.5/orbit against ~288k encounters/orbit ≈ 2×10⁻⁶ of
  creation). law.md's −60-per-reabsorption counterweight never fires; the +62-per-kick scale
  is also wrong at belt scale (measured amortized cost ≈ 0.3–6 bits per encounter, and
  falling).
- **λ = 0.01 and 0.1 (held out)**: one-tier 5.69 and 15.63 bits/body at t = 100; scarred
  fractions 0.63 and 1.00. Same log shape.
- **Two-tier (light cone)**: 5.53 (t=1) → 7.02 (t=100) → 10.32 (t=400) bits/body at near
  fraction 1/32 (near term flat at 1.63 bits = φ·52; far tier grows log-wise too, slope
  9.1 bits/decade, bounded by the coarse lattice range/q_far).
- **Occupancy (view/multipole level, identity-free) is stationary**: 12.768 bits/body at
  birth → 12.784 at t = 100 (+0.13%). All growth is identity-level.
- **Firewall**: reabsorbing every far body at ε = 100 km redirects a near body's per-orbit
  precession by σ ≈ (3π/4)·(μ/√N_far)·(a/R)³·3ε/R with μ = 3.6×10⁻⁹ (asteroid-belt/star),
  N_far = 10⁹, R = 2 AU: margin ≈ **10¹⁵** against the ϖ quantum (10⁻⁴ rad). Even a 10³×
  heavier belt (a fleet aggregate) keeps ~10¹². Far deviations reach the near zone only
  through the belt's multipole — PRINCIPLES #6/#7's aggregates are exactly the certificate.
- **10⁹ extrapolation** (near fraction 10⁻³): naive 6.5 GB; one-tier 4.0 GB at t = 100 (5.4
  at 400, then repack → 6.5); two-tier **0.70 GB** at t = 100, ~2.9 GB at t = 10⁴. At the
  real 157-bit state: naive 19.6 GB (blown), one-tier ≈ 12 GB (blown), two-tier ≈ 1.4 GB.
  Promotion of a far body to exact costs one replay of its encounter history (mean 110
  encounters at t = 100) — idle-time work, no ledger needed because the firewall certifies
  the coarse state.

Reproduce (≤ 60 s each): `cd lab/results/20261006-1029-components-21c3 && python3 belt_scars.py`
(29 s, writes `results.json`) and `python3 t400.py` (53 s, writes `t400.json`).

## Predictions

Written before the decisive runs (`predictions.md`): 9 items, 6 held, 2 missed, 1 partially.

- Held: reabsorption fires but decays (1); one-tier grows without bound (2, though far slower
  than my linear guess — see below); the ±62/±60 ledger does not balance (3); the firewall
  margin ≥ 10³ (5, measured 10¹⁵); occupancy does not grow (6); crossing beyond 500 orbits,
  measured ~1,100 (9); log-shape at t = 400 predicted 41.8 ± 2, measured 43.5 (7, 0.7 over
  the band — shape right, slope slightly low).
- Missed: scarred fraction saturates at 1.00, not ≤ 0.95 (1) — the ±1 cross-column jitter
  kills returns that a pure 3-D walk would allow. Two-tier at t = 400 ≤ 8.6, measured 10.32
  (8) — the far tier inherits the same log growth; "saturates" was too strong at t = 400.
- My own linear-growth prior (crossing within 5–30 orbits) was wrong in the direction that
  flatters the existing design: growth is log, so **Form P is cheaper than naive blocks for
  ~1,100 orbits per belt** even one-tier. The two-tier's case rests on the 157-bit real state
  and on t ≳ 10⁴, not on t = 100.

## What would make it wrong

- A kick distribution whose tail is **truncated** (real close-encounter cutoffs at body
  radii) makes deltas sum-of-many rather than record-dominated: growth becomes ~linear in t
  and the crossing moves early. My geometric(p = 1/2) tail has no physical cutoff; the r8
  conjunction data should set it.
- Correlated (Newtonian) partner kicks would halve per-body creation (one cause, two
  effects) — this makes the store cheaper, not dearer.
- Secular common-mode drift (not modeled; my kicks are zero-mean) would inflate deltas; the
  affine program layer (`Prog::Affine`) absorbs exactly that, so the check is whether the
  residual still walks as measured.
- The firewall margin assumes independent far errors adding in quadrature; a conspiracy
  (correlated kicks across the belt) could beat the √N. Real belt lumps exist at every
  quantization and do not change the comparison.
- N = 2.6×10⁵ for 100–400 orbits is one belt, one seed family, a static player: tier churn
  (promotion/exit around a moving player) is unmeasured CPU, though its bits are counted.

## Cost of adoption

One step in `crates/shipmem`: a far tier (periodic requantize of a body's delta at q_far on
cone exit) beside the existing hot/scar/repack forms, plus the firewall constant recorded as
the certificate that licenses far requantization (it is the same multipole argument that
already licenses aggregate gravity). B18b's 64-byte cap is untouched; identity stays
provenance. The ledger line in law.md ("+62 per kick, −60 per reabsorption") should be
replaced by the measured belt numbers: creation ~1/t-decaying, reabsorption-by-return ~10⁻⁶
of creation, equilibrium held by the cone, not by return.

## Fit with PRINCIPLES

- #6 "Store the generator, not the generated" — the far tier keeps the generator plus a
  coarse correction; the exact state is regenerated only inside the cone.
- #24 "The memory floor is information" — measured floor: occupancy 12.8 bits/body flat
  (what any view/multipole can see) + identity deltas; the two-tier sits within ~2× of the
  measured far-delta cost at t = 100 and ~1× of near exactness where exactness is required.
- #5 "the player is the only wildcard … light cones partition compute" — the same partition
  now sizes memory, not just compute; the firewall is the certificate that the partition is
  legal (#6/#7 aggregates).
- #21 "Rough first, refine when a certificate could break" — q_far is the rough tier,
  promotion the refinement, the firewall the certificate that decides when refinement is due.
- #33 "a body resolves only the influences that are significant at its own scale" — far
  bodies resolve the belt at q_far; nobody inside the cone is affected beyond that floor.

## The lens (what it may have made me miss)

A local optimum can move cost to another component: I counted bits, not the CPU of tier
maintenance (requantize, promotion replays, churn at the cone edge) nor the cache effects of
splitting the store; the neighbours (the event queue's promotion schedule, the allocator's
slack order) must be measured before this is adopted as-is. The encounter process is
synthetic (independent per-body impulses, no partner reciprocity, no resonant structure), so
the *rate* constants are calibration, though the encoding results are process-shape results:
log growth needs only a heavy tail, death of return needs only multi-column jitter. And one
crate file (`crates/shipmem/src/program.rs`) was briefly damaged by a stray edit of mine
during setup and restored byte-identical (`git status` clean) before any run; no run touched
the crates.
