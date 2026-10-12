# Dossier — 20261012-0616-scout-d0a9

**Lens:** scout (requirements first, then the best solution anywhere).

## Claim

H_live is self-limiting, and its law is measured: the fraction of a population
that must carry a live scar follows a first-passage curve in scaled time
k/(Q/σ_s)², so live scar memory **saturates** at t_sat ≈ (Q/σ_s)² orbits with
a payload of ~1 bit per dimension per scar (2–5 in the ballistic regime) —
hence a realistic sparse belt of 10⁹ bodies never saturates (t_sat ≥ 10⁴
orbits even at a km-scale quantum) and fits as ~16 MB of programs, while only
encounter-dominated populations (rings, battles, live heavy belts) carry a
per-orbit scar stream, which idle-time recompaction keeps bounded.

## Bottleneck

Board risk #2 / HANDOFF "Risks to attack first": "Distinctions created per
game-second (H_live): they, not the body count, decide whether 10⁹ fit in
8 GB; not measured yet." Requirements as numbers: 10⁹ bodies, 8 GB ⇒ 64
bits/body lifetime; player epoch in orbits; the law's scar quantum Q; PRINCIPLES
#24 (the memory floor is information-theoretic) and #6 (store the generator;
influences below one quantum accumulate). Gain: retires the fear for the
belt class (88 bytes/body ⇒ 0.126 bits/body, ~5,600×) and gives the b-h-live
build the exact quantity to instrument. What it deletes: any per-body event
store for sparse populations; the open question in B18's "measured floor".

## Evidence

Toy (floats explore; nothing canonical): Hill shearing sheet, N=256, softened
mutual gravity, exact linear drift (conserves the invariant pair (A, D) — the
engine's drift+kick shape), 40 orbits, seeds 1–2. The toy is a stress case:
σ_s ≈ 5% of the epicycle amplitude per orbit (t_relax ≈ 400 orbits,
star-cluster-like).

- Kick stream per orbit: rms A = 1.28e-3, D = 1.67e-3; max/rms ≈ 5
  (softening-capped tail); lag-1 autocorrelation < 0.03 (encounters do not
  repeat; shear separates guiding centres).
- Payload bits per scar (delta entropy): 1.00–1.04 at Q ≥ 5σ_s; 1.94 at Q = σ_s;
  2.94 at Q = σ_s/2; 4.74 at Q = σ_s/6.6. In the useful regime a scar is a
  single quantum: ~1 bit per dimension.
- Saturation (fraction of bodies carrying ≥1 scar after 40 orbits, both seeds):
  Q = 4σ_s → 99–100%; 8σ_s → 75–91%; 16σ_s → 22–46%; 32σ_s → 0.4–8%.
  A Gaussian random-walk Monte Carlo with the same σ_s tracks the whole curve
  within ±0.13 absolute: the law is the universal first-passage curve in
  k/(Q/σ_s)²; t_sat ≈ (Q/σ_s)² orbits.
- The naive steady-rate identity rate = σ_s²/Q² is **wrong** for a free walk
  (measured rate·qfac² = 2–8 at qfac 8–32): a free walk's scar count grows as
  the range law ~√k, so the rate decays and the memory self-saturates even
  with no recompaction. This prediction failure is where the right law came
  from.
- Control (must pass): gravity off ⇒ max |ΔA| = 1.2×10⁻¹⁵ per orbit and zero
  scars at Q = 10⁻¹⁴. Undisturbed orbits cost exactly nothing (principle 3,
  operational).

Extrapolation (Chandrasekhar relaxation; t_relax ≈ 0.1N/ln N verified in the
literature), belt 2–4 AU, 10⁹ bodies, v = 5 km/s:

| Population | t_relax | σ_s/v | t_sat at Q = 10⁻⁶·v | verdict |
|---|---|---|---|---|
| real belt (3×10²¹ kg) | 2.9×10²² orbits | 5.9×10⁻¹² | 2.9×10¹⁰ orbits | never scars; 10⁹ fit as ~16 MB of programs |
| same, Q = 10⁻⁹·v (km at AU) | | | 2.9×10⁴ orbits | beyond any game epoch |
| gamey heavy belt (10⁻³ M★) | 6.6×10⁴ orbits | 3.9×10⁻³ | ballistic | every orbit scars: block store, needs idle recompaction |

The scar stream that actually flows in the plane comes from close encounters
with secondaries (geometric rate ~10⁻³/orbit, ~24 bits/event: ~3 MB/orbit for
10⁹ bodies, recompactable in idle time) and contacts in dense regions
(H0173's ~4 bits per collision) — not from belt-belt mutual gravity.

**Reproduce** (each ≤ 60 s, Linux/x86, orders of magnitude only):

```
cd lab/results/20261012-0616-scout-d0a9
python3 hlive.py results.json    # ~31 s: both seeds + control
python3 analyze.py               # ~30 s: saturation curves vs Gaussian MC
python3 fermi.py                 # instant: the Fermi table above
```
(numpy only; scripts and data in this folder.)

## Predictions

Written before the decisive run ([predictions.md](predictions.md)): P2
(ballistic floor ≥ 0.7/orbit), P3 (crossover), P4 (payload bits 1.0 → 4.7),
P5 (control), P6 (seed transfer, frac scarred at k=10, entropy within 0.7
bits of Gaussian) — **all held**. P1 (steady rate = σ²/Q²) **failed**,
diagnosed: the free walk obeys the range law, and the correct object is the
first-passage saturation curve (confirmed against Monte Carlo). P7 (heavy
tail surfaces scars ≥1.3× faster than Gaussian) **failed in direction**:
measured 0.76–0.83× the Gaussian reference at k=10 (softening caps the tail);
at qfac 16 the end-fraction runs 0.44 vs 0.34 Gaussian — the tail effect is
real but ~±25%, not a factor.

## What would make it wrong, cost, fit

- The quantum that decides everything is the law's own storage grid for (E, L)
  (r2: widths are set by behaviour), not an abstract float precision. If the
  grid is set finer than ~10⁻¹⁰ of the dynamic range for a real belt, t_sat
  falls inside a long epoch and every orbit scars. Adoption line: **choose the
  scar quantum from the view's floor (one home per the floor, PRINCIPLES #5,
  representation.md §4), then t_sat is an output, not an input.**
- Resonances: coherent libration-driven scars (rate set by libration, not
  diffusion) are outside the random-walk law; the law already keeps
  per-conjunction kicks there (law.md), so those populations must be measured
  separately by the b-h-live build. Same for collective wake heating at low
  Toomre Q (UNVERIFIED at source: Toomre & Kalnajs 1991; the toy stayed at
  high Q to avoid it).
- Cost of adopting: a design note in law.md (scar quantum + the t_sat
  identity + the payload numbers) and the b-h-live dashboard instruments, per
  population: scarred fraction vs orbits in units Q/σ_s, payload entropy,
  offset-width distribution. No law change.
- Fit: "the memory floor is information-theoretic" (#24) — measured, not
  assumed; "Store the generator, not the generated... influences below one
  quantum accumulate" (#6) — the sigma-delta carry is exactly this and the
  measurement shows it self-saturates; "Compute only surprises" (#3) — the
  control run is zero-cost motion, operationally.

## The lens

Scout stole from statistical mechanics (first passage, Chandrasekhar
relaxation) and the in-house sigma-delta law; what it may have missed: 2D
only, no resonant structure, softening caps the tail (real Saturn-ring
photogravitational aggregates collide, not scatter — contact physics, H0173,
governs there); the toy never tests recompaction's cost at 10⁹ (assumed
O(pass) in idle time, not measured); and the translation from the player's
spatial floor to an invariant-space quantum is asserted, not derived from the
view's zoom (OC#30).
