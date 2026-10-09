# Dossier — 20261009-1345-components-0e4d

**Claim.** The cycle memo's 12-bit key is behaviour-floor-tight (you cannot coarsen it
without failing frozen gate B2), so on the strong branch (compactness > 2⁻¹⁸) the memo's
occupancy × entry cost — not the bodies — is the memory that can bust 8 GB at 10⁹: a cold
compact belt costs ~0.75–1 GB of shapes and a hot belt (σ_e 0.3) is already ~2 GB per
million bodies, while the weak branch that drops radius from the shape identity sits at
~0.9 MB; the fix direction is generalized radius-dropping (shape keyed by compactness at
the behaviour tolerance), not a coarser key.

**Bottleneck.** Board focus "fitting 10⁹ in 8 GB" and risk "H_live/distinctions". This is
the generator-store half of that question (PRINCIPLES 6: "Store the generator, not the
generated"): bodies cost ~0.126 bits each (gold components-98bc), so what actually grows
is the number of *behaviourally distinct compiled cycles* the population must hold.

**Component** (lens: first principles, one component): generators and certificates — the
shared cycle memo (`crates/space/src/orbit.rs`: `MEMO_SHAPE_BITS = MEMO_SCALE_BITS = 12`,
`MemoCode`, `QuantizedMemo`, `WEAK_EXPONENT = −18`).

1. **Requirement.** PRINCIPLES 6 (store the generator) + the goal's 8 GB; judged by the
   frozen gates B1 (precession ≥ 99% within 1%) and B2 (periods ≥ 99% within 0.1%).
2. **Floor.** Distinct behaviourally-separable orbits × bits per orbit summary. Measured
   with the law's own compiler: a (scale, shape) grid coarser than (11, 11) fails B2
   (period error 1.03×10⁻³ at 11 scale bits, 3/256 seeds over; 3.46×10⁻⁴ at 12 bits,
   0/256; shape 11 ties 12, ≤ 10 fails on up to 213/256). B1 is four decades from
   binding (max precession error 4.5×10⁻⁷ at 4 shape bits). The grid is *not* waste.
3. **Idiot index.** Not in the grid (≈ 2× slack) but in the entry and the branch: on the
   strong branch every distinct 12-bit key owns a compiled `OrbitShape` (~0.9 KB cold,
   ~2.1 KB at σ_e 0.3, 6.6 KB at e 0.9), and occupancy is large (measured 488,004
   entries for 2²⁰ cold-belt bodies; 945,208 hot) — ≈ 0.44 GB / 2.0 GB per million
   bodies, extrapolating to ~0.75–1 GB (cold) and tens of GB (hot, cell cap ~16 M
   entries ≈ 34 GB) at 10⁹. The weak branch (p ≥ 2¹⁸ M), which drops radius from the
   shape identity, holds 1,025 entries ≈ 0.9 MB at any N. Ratio strong/weak for the same
   belt geometry: ~500×.
4. **Design within 10× of the floor.** The weak branch's rule — drop from the shape
   identity what the behaviour cannot see — generalized: key shapes by *compactness
   quantized at the B2 tolerance* (the shape is a function of q = 1/p) and keep per-key
   scalars (time scale, increments) exact per body. Today's cliff at q = 2⁻¹⁸ ≈ 4×10⁻⁶
   is ~2–3 decades more conservative than the 1PN period correction that B2 can see
   (~M/p ~ 10⁻⁴–10⁻³), leaving a band p ≈ 3×10³–2.6×10⁵ M where every belt compiles
   per-radius shapes it cannot be distinguished by. Not built here; the measurement that
   sets the safe compactness quantum (shape error vs Δq against B1/B2, the same sweep as
   Part A on the shape axis) is the named next experiment.

**Evidence.** All numbers in [evidence.txt](evidence.txt); reproduce with
`cargo test -p emergent-space --test memo_floor -- --nocapture` (Part B debug build ran
88 s; the decisive held-out ladder and crossover ran in release, 10 s; every process
stayed under ~1 GB). Test file `crates/space/tests/memo_floor.rs` ships in this run's
patch. Belts follow r8's frozen scene shape (a uniform over a factor-1.5 band, e
Rayleigh): A p 2048–3072 M, B p 524288–786432 M, C = A with σ_e 0.3.

**Predictions** ([predictions.md](predictions.md)). Held: #1 hot-belt distinct codes
(945,208 vs predicted 0.9–1.0 M); #4 the weak/strong collapse between 2¹⁷ and 2¹⁸
(61,721 → 5,587 → 863 entries); #5 (the floor sweep) as measured before writing.
Failed, honestly: #2 the uniform Poisson saturation model — measured occupancy at
2²¹/2²² is 610,178/697,679 against predicted 1.15–1.20 M/1.45–1.55 M; growth past 2²⁰
is strongly sub-linear (Rayleigh concentration makes gap-cells wildly non-uniform), so I
report the 10⁹ extrapolation as a two-point bound (measured-rate ~0.7 GB, geometric cell
cap ~1.05 GB), not a fit. #3's byte arithmetic (12.6 KB/entry) came from a stale binary
of an earlier mangled edit (124 knots/orbit); the clean rerun measures 6.2 knots/orbit
and ~0.9 KB/entry — the per-entry cost fell 16×, the hot-belt conclusion survives
(measured 2 GB at 2²⁰, cap ~34 GB).

**What would make it wrong.** The 10⁹ numbers are cloud-extrapolated occupancy × entry
bytes, not a 10⁹ run (2 GB process budget); if occupancy's sub-linear growth continues
past the cell cap's tail cells the cold-belt memo could stay near 0.7 GB, and if real
belts never sit hot *and* compact simultaneously the worst case is a scenario choice,
not a law limit. The B2-tightness claim uses the gate's 0.1% as the tolerance; a
coarser player-facing tolerance (B18's belt behaviours, encounter geometry at 1% r_p)
would re-open the shape axis (my analytic estimate: shape could drop to ~6–7 bits if
only r_p at 1% binds, since precession has four decades of slack — worth one sweep).

**Cost of adopting / fit with PRINCIPLES.** Adoption is a shape-identity change in
`orbit.rs` (compactness-quantized `ShapeKey` on the strong branch), no gate edits; it
deletes the per-radius shape tables of a whole band. "The cheapest compute is compute
not done… The memory floor is information-theoretic" (1, 24): the floor here is
information the behaviour cannot see, and today's store pays ~500× for it on the strong
branch. "A fix signals the wrong representation" (19): the cliff constant 2⁻¹⁸ is a
bandaid-shaped edge — one rule (quantize by tolerance) should replace two branches.

**The lens.** The components lens measured one store and its floor; it did not measure
the neighbours' response (does a coarse-compactness shape change encounter geometry,
B13/B14 outcomes, or the compiled-tide phase?). It also inherited the plane's belt
geometry rather than arguing for the physically-binding scene (crossing belts near a
compact doll), which is exactly where the bomb is largest — a lens toward the
representation, away from the scene.
