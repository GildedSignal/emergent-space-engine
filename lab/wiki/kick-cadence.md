topic: kick-cadence
status: open
closed-by:
valid-while:
updated: 20261012-1827-q-wiki-kick-cadence-93d9

# Kick cadence: how often a body is kicked, and by what rule

## Current best

**The rule is regime-aware and coarse, everywhere except where cadence is the wrong lever.** Seven graded runs split the question by regime; the levers that died are the interesting half of the record.

**Away from resonance, smooth external tide: a fixed coarse cadence passes, and its error is a systematic offset, not noise.** In the planar circular restricted three-body replica (exact Kepler drift + midpoint/DKD tidal kicks — the law's own form), the error is rho ≈ 0.5·n^-2.1 (n = kicks/orbit), independent of μ over 100× and of planet radius over 2.3×, with a bounded Jacobi attractor and no map-injected chaos; the prior 4/16/64-orbit disagreement across runs was seed noise (spread 3–693×) (ad35). Clean far-belt bodies hold B14's 10% precession bar at ~2 kicks/orbit (worst seed 4) against the plane's uniform 128 (1db4); a Jupiter-belt replica puts the fixed-cadence floor at 8/orbit at probe tolerances, and conjunction-scheduled (event-shaped) cadence never reaches the bar at any evaluation count (06a8). Domain: planar replicas, e₀ ≤ 0.1 headline; at e₀ = 0.3, n = 4 corrupts (ad35 checker); "moons need 16–32" is a rate-bar-only read, not behaviour-certified (1db4 checker).

**Near first-order commensurabilities: no cadence certifies, at any rate.** On a correctly-built resonance lattice (2:1 and 3:2, centres to ±2 W edges), 29 of 30 rows fail the behaviour gate at every cadence; the per-row oracle ceiling — the cheapest holding policy, which no real rule can exceed — is 1.14× in tide evals / 1.24× in kicks (gate-robust 1.05–1.18×) against the cheapest holding fixed cadence (67be, gold). The standing rule: read the commensurability from the compiled frequencies and hand the body to the resonant representation (the doll); cadence is not the lever near resonance. On the plane itself no fixed cadence passes the frozen gates at any N: B13 fails at every N = 1..10 (held-out N = 10: 53/64, refusals multiplying to 2,578), B14 at every N = 1..7, and B14's 60 s phase budget is law-dominated (oracle 12.9 s; law 26.4 → 1292.4 s, ×2 per step) (0c44; c01c, gold). The B13 tail is `NoBoundOrbit` kick refusals on heliocentrically bound, nearly radial states — a flyby-representation gap, not a cadence one (c01c).

**Per-body rules: precomputed from body constants survives; anything fed back from state walks.** Self-triggered cadence (next kick decided at each kick from the body's own osculating orbit; absolute, net- and path-impulse-normalised triggers) does not transfer across (μ_r, e) or over-spends 1.4–30×; the mechanism is that the behaviour budget is set by phase cancellation between the kick grid and the perturbation's orbital-frequency structure, which no orbit-local magnitude bound can see (0713, gold). A state-fed-back significance gate turns the bounded second-order layer into a walking first-order one: 1,548× more evaluations at matched error (21,668 vs 14 evals/body-orbit at D = 1e-5), walk slope 0.75–0.98 vs 0.03–0.08 fixed; cadence precomputed from the body's constants stays exactly on the fixed-cadence curve (54d9, gold). The checker's correction: even a precomputed *alternating* (state-independent) interval partially walks (slope 0.49) — the dangerous property is cadence modulation itself, not state feedback alone (54d9). A per-body certificate from constants, t* = √(2q/a_bound), is oracle-tight at 1.65× and self-tightens under stronger tides, but missed equal-error parity with fixed-32 by 3.5× and costs 3.5–30× as shipped (a2ec). The tuning ceiling over quant-5022's six stress seeds is 1.92× (51bf, lead — reproduced exactly; its checker caps it: pre-empted by 7d0d's positive τ-sensor, and false at the quiet floor, 2 events/orbit at μ = 1e-5, headroom ≥ 32×); on those seeds no dimensionless number ranks the needed rate — the 10× comes from deletion, not rate tuning.

**The cold dense belt has no clean fixed-cadence operating point at all.** Sub-resolution conjunctions (b ≲ √(m·dt)) corrupt the layer at every cadence 8–256 and at N = 800, over a derivable Kepler-shear floor of 2.303e-2/orbit; the corruption *worsens* monotonically to 512/orbit, and at μ = 1e-4 the E1 "truth" cadence 256 itself fails the census gate (fb 2.0e6) (cd52; f2e3, gold). The silver's "manufactured chaos" mechanism is refuted: λ is dt-robust or *rising* under 16× refinement (ratios 1.11–1.56) and monotone in the density K = Δa/R_H, crossing the Wisdom–Tremaine level ≈ 0.5Ω near K ≈ 0.15 — so λ_max ~ 0.1–1 Ω is the belt's real surprise floor, set by K, not by the step (f2e3). Cadence cannot buy this back; the conjunction-window representation must (ties to `encounters`).

**The averaged (secular) layer: cadence counts per secular period, and anchors to the orbit, never the tick.** With WH-like shear-order kicks, behaviour holds down to N_lib ≈ 4–10 kicks per secular period (librating, circulating, retrograde, e₀ = 0.9 held-out); the naive explicit-Euler order is 30–100× tighter and compounds (drift exponents 1.1–3.0 vs 0.01–0.7); near the Kozai separatrix no cadence certifies the class (flips at 1613 kicks/period). Certificate h = T_sec/20..T_sec/5 read off compiled frequencies: 15–60× fewer kicks at belt scale, extrapolated, unmeasured on shipped code (5030). Rebuilding the between-window secular term as one midpoint kick per fixed mean-longitude segment (K per orbit, conjunction windows riding on top) removes the tick-anchored aliasing subharmonic at every segment length: Δė 84–134 MADs → 0.01–0.11, Jacobi 48–175× the floor → 1.0×, and the belt ϖ̇ break closes +64% → +2.5% at K = 16, +0.5% at K = 32. Deployable rule: K ≥ 16 percent-level, K ≥ 4 kills the subharmonic, K = 2 forbidden; tick-anchored dead at every length (2eb1, gold).

**The budget: cadence is the largest priced wall.** Of the billion-body event budget's three walls — kick compute (29 µs today), layout (gather-4 sustains 2.7× pointer-chasing), cadence — cadence is 64 → 0.3 kicks/orbit = 213×: no layout reaches a 10⁹-body battle at 10× real time on today's 64/orbit cadence, while year-scale belts already pass 10⁹ at 10× real time even at today's 29 µs per kick (a4ed, gold; compute/layout walls → `kick-jet`). On the shipped integer plane the frontier is regime-split by a measured 8×: the resonant bulk holds at 16 kicks per perturbation period (B17), deep passages need ≥ 128 (B13), and the plane serves both with one doll-wide Δs tied to the fastest secondary — paying the passage price everywhere; cutting the bulk's cadence 8× removes ~5× of all kick events at flat per-kick price (7f97).

## Refuted

- The single-constant synodic ("one clock") cadence rule: killed by its own pre-registered falsifier, off by 3 octaves (1db4).
- Conjunction-scheduled kick cadence with a zero-kick secular kernel, belt regime (06a8).
- Per-body self-triggered cadence (jerk/impulse triggers) in the belt/moon regime: no transfer or 1.4–30× over-spend; phase-cancellation mechanism (0713).
- State-fed-back per-body cadence: walks, 1,548× at matched cost; even precomputed alternating intervals partially walk (54d9).
- A frequency-derived cadence rule near resonance reaching the 4× bar: oracle ceiling 1.14–1.24× (67be); scout-9abe's "2:1 vs 3:2 inversion" was a Python operator-precedence artifact (its off-resonance 2.5–4/orbit result stands as measured, but is superseded as a rule).
- Any fixed cadence passing the plane's frozen gates: B13 every N = 1..10, B14 every N = 1..7 (0c44; c01c).
- The moon-cadence amplification measurement "A(τ) crosses 1 at 0.17–0.25 Hill radii" (library-f045): broken Kepler layer — vr-flip at 71.7–75.2% of steps, 180° start teleport, 2π mislabel (0102).
- Window-gated kicks holding belt behaviours at 6–9/orbit: replica's Kepler layer broken (tangential speed (1+e·cosν)·h/r² where Kepler needs h/r) (9205, lead — unbacked, not disproven).
- The per-body deferral certificate ("defers essentially all tide evaluations"): units artifact, its own pre-registered kill criterion fired; deferral is real only at Q ≥ residue amplitude (~1–2.5e-3·a) (e5a2, lead).
- "λ ≈ 2–14/orbit is manufactured chaos" as the belt-corruption mechanism (cd52): refuted by f2e3 while the no-clean-point claim stands.

## Open directions

1. **Aim the cadence question at the per-kick cost and the flyby representation first.** On the plane the fixed-cadence search is dead and the budget is law-dominated (~43–52.8 µs/kick, one full cycle rebind per distinct kick, zero reuse, `NoBoundOrbit` tail) (c01c; 0c44) — a cadence rule cannot matter there until those move (→ `kick-jet`).
2. **Split the plane's one doll-wide Δs by regime** (bulk vs passages, the measured 8×): ~5× fewer kick events at flat per-kick price, via a per-body or per-regime clock constant precomputed from constants only (7f97; 54d9).
3. **Secular deletion at scale**: h = T_sec/20..T_sec/5 certificates (5030) plus orbit-anchored discrete secular kicks, K ≥ 16 (2eb1) — 15–60× fewer kicks for weak-tide bodies; extrapolated past T_lib = 227 and never measured on shipped code.
4. **Certificate-sized kick windows**: 33/132/704 evals/orbit at e = 0/0.3/0.7 (1.5–2.4× the headline), because the tail-coefficient certificate over-estimates fit error 20–130× (213e).
5. **Price the horizon into the moon certificate**: N* is set by Hill position (4/8/16 at f = 0.2/0.3/0.45 R_H) and *walks with horizon* (N = 8 apsidal deviation 4.4% → 9.7% from horizon 12 → 27), so a horizon-free local rule is not derivable from these gates; the mixed-scene validation never ran (7d0d).
6. **The dense belt's corruption is not a cadence problem**: sub-resolution conjunctions corrupt at every cadence (cd52; f2e3) — the fix belongs to the conjunction-window/encounter representation (→ `encounters`).

## Contradictions

- **What ranks needed cadence in belts.** 3a4c: cadence need is governed by behaviour unfolding within the certification horizon (ρ = +0.948) and *no birth-element Chirikov scalar* ranks it; 1db4 and 67be: resonance proximity still decides certifiability (a = 0.90 fails from 4:3 contamination; near-resonance rows uncertifiable at every cadence). Reconcilable as "birth-element scalars fail, compiled frequencies still gate" but unresolved as stated; the next belt run should measure both on one sample.
- 54d9's headline ("precomputed-from-constants stays on the curve") vs its own checker's alternating-interval walk (slope 0.49): adopted here as the checker's correction — the dangerous property is cadence modulation, not state feedback alone.

## Runs
- 20261005-2231-q-cadence-7d0d (silver): moon frontier N* = 4/8/16 at f = 0.2/0.3/0.45 R_H, flat in e; walks with horizon.
- 20261006-1029-system-06a8 (silver): conjunction-scheduled belt cadence dead; fixed-cadence floor 8 kicks/orbit at probe tolerances.
- 20261006-1135-quant-a4ed (gold): billion-body budget walls priced; cadence 64→0.3/orbit = 213×; belts pass 10⁹ today, battles do not.
- 20261007-0128-b-b17-parallel-cee8 (missing): checker died at a 429; author finals only, never graded.
- 20261007-0341-scout-9abe (silver): jerk-triggered 2.5–4 kicks/orbit held behaviour off resonance; resonance contrast later shown artifact.
- 20261007-0528-second-20261007-0341-scout-9abe-67be (gold): near first-order commensurabilities cadence uncertifiable at every cadence; oracle ceiling 1.14×.
- 20261007-1550-system-9205 (lead): window-gated belt cadence claim unbacked; replica's Kepler layer broken.
- 20261007-1646-scout-0713 (gold): per-body self-triggered cadence killed in belt/moon regime; budget is kick-grid/perturbation phase cancellation.
- 20261007-2246-scout-1db4 (silver): single-constant synodic rule killed; far belt holds B14 at ~2/orbit, moons 16–32, resonance refuses.
- 20261008-0458-second-20261008-0338-library-f045-0102 (silver): kills library-f045's τ-crossing moon-cadence measurement; broken Kepler layer (vr-flip, 2π mislabel).
- 20261008-0945-library-51bf (lead): no dimensionless number orders the needed kick rate; per-body tuning caps at 1.92×.
- 20261009-0621-system-7f97 (silver): integer-plane frontier regime-split 8× (bulk 16/period, passages ≥ 128); one doll-wide Δs overpays everywhere.
- 20261009-1936-dynamics-5030 (silver): averaged-layer cadence is kicks per secular period (N_lib 4–10, shear order); Euler compounds; Kozai uncertifiable.
- 20261010-1152-dynamics-ad35 (silver): non-resonant tide error is systematic ~0.5·n^-2.1, μ- and R-independent; 4/16/64 disagreement is seed noise.
- 20261010-1302-library-a2ec (silver): per-body certificate t* = √(2q/a_bound) oracle-tight 1.65×; unpriced as shipped (3.5–30× cost).
- 20261010-1816-dynamics-3a4c (silver): belt cadence set by behaviour unfolding within the horizon; no birth-element Chirikov scalar ranks it.
- 20261010-2052-library-2d94 (silver): Whalley–Wilmott deviation band cuts 2.8–6.7× open loop; closed-loop trigger is clairvoyant, certificate breaks.
- 20261010-2141-dynamics-cd52 (silver): cold belt has no clean fixed-cadence point; sub-resolution conjunctions corrupt at every cadence.
- 20261010-2314-library-e5a2 (lead): deferral certificate's headline is a units artifact; its own kill criterion fired.
- 20261010-2314-second-20261010-2141-dynamics-cd52-f2e3 (gold): no-clean-point confirmed bit-exact; "manufactured chaos" refuted — λ real, monotone in K = Δa/R_H.
- 20261011-0224-library-213e (silver): certificate-sized windows cost 33/132/704 evals/orbit at e = 0/0.3/0.7 (1.5–2.4× the headline).
- 20261011-0836-spacex-0c44 (silver): no fixed cadence passes plane gates; cost lever is one full cycle rebind per kick (43 µs).
- 20261011-0924-second-20261011-0836-spacex-0c44-c01c (gold): fixed-cadence search dead; B14 budget law-dominated (×2 per step); refusals multiply with cadence.
- 20261011-2235-library-54d9 (gold): state-fed-back per-body cadence walks (1,548× at matched cost); precomputed-from-constants stays on curve.
- 20261012-1340-second-20261012-1227-system-8685-2eb1 (gold): orbit-anchored discrete secular kicks kill tick aliasing; K ≥ 16 percent-level, K = 2 forbidden.
