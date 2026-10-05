# Dossier — run 20261005-2129-m-meso-motion-15d6 (lens: mathematical representations, motion and orbits, meso level)

## Claim (one sentence)

The close encounter is one exact event — the pair's two-body flow, composed
Strang-style between Sun drifts — and it is the right representation exactly
where U² ≫ μ_p/b (impulsive), where it beats the straight-line impulse by
10–15× in Δv and replaces a substep cascade with ~3 Kepler evaluations, while
below that criterion (the shear regime, U ≲ 3·v_H) it is provably the wrong
channel and the doll owns the scene — so the law's perturbation layer should be
selected by the one dimensionless number U/√(μ_p/b), with conjunction events
(impulsive), the rotating binary doll (shear) and secular phasors (distant,
q-secular) as its three channels.

## Bottleneck

Board focus item 1 (fewer kicks per orbit at the same behaviour: kicks dominate
the engine's cost; correctors and higher-order splits are dead, the lever is
cadence) and item 2 (the changeover near a secondary), plus the measured kick
cost (29 µs, 15 of them rebind; 64 kicks per orbit). Expected gain: ~100× fewer
events than the kick cadence for secondary perturbations (0.5–0.7 conjunctions
per body per orbit on the outer belt, each ~3 Kepler evaluations), and a
deletion candidate for the SyMBA changeover in the impulsive regime. What it
lets us delete: the substep cascade near a secondary for impulsive encounters,
and most of the per-kick quadrature for the secondary's channel.

## The ranked catalogue (gain × probability ÷ cost of adoption)

Not resold: R1–R5 of the Opus memo (`lab/refs/opus-math/memo.md`) are assumed
adopted/pending as written; correctors, higher-order splits, resonant normal
forms (r4 v3), averaged tides beyond 0.17 r_H (r9), quantized (E,L) memos and
TRACE are dead per the taste log.

1. **The encounter as one exact event (this run's probe; Öpik 1951; Valsecchi
   et al. 2003; Wisdom 1983's resonance map is its global skeleton).**
   Structure: in a WH split the interaction leg H_pair = μ_p/|d| is itself a
   Kepler problem; its flow is the universal Kepler map (Goodyear 1965;
   Shepperd 1985 — DSN/ESA propagation, real skin in the game), i.e. ONE
   closed-form canonical transformation, no orbit categories, with the
   deflection γ = 2·atan(μ_p/(bU²)) a rotation about the scattering-plane
   normal (Paeth/integer form per R3). Composition drift(w)·pair(2w)·drift(w)
   is second order. Between conjunctions the body is the drift tube (zero
   work); the conjunction time is the integer circle rotation already in
   `crates/encounters` (dioph). Probed: see Evidence. Replaces: the SyMBA
   substep cascade for impulsive encounters; conjunction quadratures.
   Kill criteria: gates B12/B13-class scenes in the impulsive regime must pass
   at 1 event per encounter — this run reached Δv/U ≈ 0.8–2.7% (marginal B13),
   so it is one named experiment away (see Predictions).
2. **The three-channel selector by one dimensionless number.**
   U/√(μ_p/b) ≥ ~10 → event; U/√(μ_p/b) ≲ 3 or b ≳ few r_H with slow U → the
   planet's doll (handoff + changeover, i.e. what the plane already has; B12's
   scene lives here); b ≫ r_H → secular phasors (R2/q-secular). Measured, not
   assumed: the boundary is in U/v_H, not in b/r_H. This is principle 4 (no
   categories; dimensionless numbers choose regimes) made concrete for the
   perturbation layer, and it composes with R2: distant conjunctions are
   phasor increments (Hénon–Petit 1986), close ones are events.
3. **Levi-Civita's map as the integer-native form of the same event.**
   z = w² turns the pair's Kepler problem into a harmonic oscillator with
   dt/ds = |w|²: the event leg becomes an oscillator (Minsky's two-addition
   map, already law.md's Binet-cell mechanism) plus one quadrature for time —
   one mechanism at every scale (principle: same law at all scales), exactly
   invertible, collision-regular. Cheapest kill: none needed this run (it is
   the same flow as 1); adopt only if the integer event needs a form without
   trig tables.
4. **The hodograph (velocity circle) for encounter geometry and readouts.**
   The relative velocity at a conjunction is the difference of two circles:
   encounter geometry (b, U) and view colours (−p·u) read from phasors, no
   propagation. Cheap, exact in integers (accumulators), zero risk; folds into
   1–2 as the readout form. No probe (below the noise of this run's question).
5. **Hansen coefficients / closed-form disturbing-function harmonics** as the
   distant channel's increment source (fixed-point hypergeometric series) —
   this is q-secular's fuel, not mine; noted so the conjunction layer and the
   secular layer agree on one source of sizes.
6. **Tisserand/C_J as the doll-edge handoff certificate.** The event conserves
   the Tisserand parameter exactly by construction (|V_rel| preserved); the
   handoff certificate at a doll edge should be the same invariant — a cheap
   consistency check for B12-class scenes. Catalogue only.
7. **Poincaré/return-map memoization (Hashlife of the torus)**: subsumed by
   R2's phasors (proper elements are the program); not re-proposed.
8. **Discrete-gradient/projection/AVI integrators**: already killed by probes
   1–2 and the rung record; not re-proposed. Burdet–Ferrándiz/Stiefel–Scheifele
   universal formulations: subsumed by 1 (same flow, more variables).

## Evidence

All scripts in `work/`, each run under 60 s on the lab Linux box (8 vCPU;
numpy/scipy float64 — floats explore, the structure is the claim).

- **Library exactness** (`work/selftest.py`): element-route Kepler propagation
  vs DOP853 (rtol 1e-13) on 200 random conics: median 9e-15, worst 1.4e-11.
  The event's pair leg vs DOP853 two-body: |ΔV| = 3.0e-15. **Robustness
  finding:** the element route NaNs on near-parabolic states (e ≈ 1±1e-3) and
  on nearly-straight relative states (μ→0 corners) — the production form must
  be the universal-variable (Stumpff) solver; my probe worked around it with
  leapfrog/DOP853 fallbacks (`work/conjlaws.py`: `pair_flow`, `drift_flow`).
- **Boundary map** (`work/probe_c_boundary.py`, `python3 probe_c_boundary.py`,
  ~7 s; 48 cases: d₀ ∈ {0.5,1,2,4} r_H × U ∈ {0.5,1,3,10}·v_H, 3 random
  directions each; shared initial states at the Hill-zone entrance; truth
  DOP853 rtol 1e-11, its own Jacobi drift ≤ 3.5e-8 everywhere):
  - U/v_H ≈ 10: event Δv/U = 7.5e-3 – 2.7e-2, dC_J ~ 1e-2; straight-line
    impulse (negative control) 0.11–0.14 — the exact leg is 10–15× better and
    never blows up.
  - U/v_H ≈ 3: 0.12–0.6 — marginal, chaotic sensitivity across directions.
  - U/v_H ≲ 1 (b/r_H from 0.05 to 4): Δv/U ≥ 1 — the event is the wrong
    channel; the impulse control explodes (10¹–10²).
  → the domain boundary is U/√(μ_p/b), not b/r_H.
- **Window tradeoff** (`work/probe_a_flybys.py`, ~5 s): edge distance κ·r_H
  swept on an in-range grid under physically correct units (GM_sun = 4π²):
  errors are κ-flat (median 0.65–0.71) once a units bug (R_H computed with
  GM_J instead of the mass ratio — 3.4× too large) was fixed; the flatness
  says the residual error is the first-order distant channel + Strang
  composition, not the window. Held-out flybys (1.2 r_p at 20 km/s; 50 r_p at
  5 km/s; both senses): ΔE within 0.16–0.98 — **fails the B13 1% gate as a
  float probe**; the leading suspects, in order: first-order-only tails, one
  Strang step per window, and periapsis-sensitivity amplification of the
  lead-in error in my targeted scene construction (the natural-entrance scene
  of the boundary probe shows 0.8–2.7% at the fast end).
- **Cost** (`work/`, timing line): one event = 3 Kepler evaluations + 2 tail
  quadratures ≈ 6 µs/body in unoptimized numpy on the cloud box (orders of
  magnitude only; the M1 and the integer solver decide). Against the plane's
  64 kicks × 29 µs = 1.9 ms per body per orbit: ~100× less work for the
  secondary's channel. Conjunction rate on the 2.2–3.3 AU belt:
  0.49–0.72 per body orbit (one per 1.4–2 body orbits).
- **Belt census (arithmetic, no run needed):** every conjunction of a
  2.2–3.3 AU belt body with Jupiter has b ≥ 1.9 AU ≥ 5.4 r_H → **the
  impulsive event channel is empty for a cold belt**; the belt's perturbation
  is entirely the distant/secular channel (q-secular). The event channel pays
  in NEA-like, fleet-crossing, assist and player scenes.

## Predictions (predictions.md, written before the decisive probes)

1. Fast+deep held-out within 0.5%: **failed** (0.16–0.98 ΔE in the honest
   scene; Δv 0.1). 2. Slow+far within 1%: **failed**. 3. Negative control
   fails: **held**, by an order of magnitude or more everywhere it is even
   defined. 4. B12-like repeated crossings at ≤ 1e-4 Jacobi: **not tested as
   designed** — the B12 scene sits in the shear regime (U ~ v_H), where the
   event is the wrong channel by the same theory; the honest restatement
   (B12 belongs to the doll) is now measured, not assumed. 5. No
   geometry-dependent blow-up: **partial** (true in the impulsive regime;
   direction-sensitivity is large at U/v_H ≈ 3). 6. Crossover b\* ∈ [2,6] r_H:
   **refuted in letter, refined in spirit** — the boundary is U/√(μ_p/b)
   (impulsive vs shear), not b. 7. Cost: conjunctions per orbit **0.5–0.7, not
   the predicted 2–5** (stronger for the cost case); close events ≈ 0 in a
   cold belt: **held**; µs-scale events: **held**.

## What would make it wrong, adoption cost, PRINCIPLES fit

Wrong if: the impulsive regime's 1%-class error cannot be pushed to the B13
gate by second-order tails and 2–3 Strang substeps per window (one named
experiment: that refinement, judged on B13's flyby list); or if C_J drift per
event stays ~1e-2 where gates need 1e-4 (but no current gate judges the
impulsive regime's Jacobi — B12's scene is the doll's). Adoption cost: a new
event kind in the plane's queue (the pair-flow leg + the selector), plus the
universal-variable Kepler solver in integers (R1-adjacent); it deletes the
changeover's substeps only for impulsive encounters, so it composes with
JANUS rather than replacing it. Fit: "no categories: dimensionless numbers
choose regimes" (the selector is one number); "a fix signals the wrong
representation" (the substep cascade is a quadrature of an exactly
integrable leg); "compute only surprises" (zero work between conjunctions);
"steal what works, from skin in the game" (DSN universal variables,
planetary-defense Öpik maps, Wisdom's Kirkwood map).

## The lens (what it may have made me miss)

The meso-motion lens is coplanar, Kepler-centric and Jupiter-scaled: it may
have missed (a) the relativistic encounter — at v∞ a visible fraction of c
(near a neutron star or the game's fast fleets) the pair leg needs the
1PN two-body scattering (Damour–Deruelle form) and the event must respect
gravity-at-c (the news reaches the other body only later — the event is
local, but its certificate is not); (b) 3D inclination (Öpik's sphere and
KS regularization; the plane is 2D today, the game will not stay so);
(c) the population/memory side — how an event layer churns `crates/shipmem`
scars per encounter (B18's real cost may be the rebind, not the physics);
(d) the harness traps this run itself hit: units and Hill-radius bugs passed
a first probe silently — my first probe A "passed" predictions in a scene
whose Sun was 39× too weak, and only re-deriving the units exposed it;
independent checkers should re-derive scene units before believing flyby
numbers.

## Reproduce

```
cd lab/results/20261005-2129-m-meso-motion-15d6/work
python3 selftest.py            # library exactness, <5 s
python3 probe_c_boundary.py    # the decisive boundary map, ~7 s
python3 probe_a_flybys.py      # window/held-out flybys, ~5 s
```

Artifacts: `probe_boundary.json`, `probe_a.json`, `predictions.md`,
`conjlaws.py` (the law: `propagate`, `encounter_event`, `pair_flow`,
`drift_flow`, `tail_moments_circ`, `impulse_event`).
