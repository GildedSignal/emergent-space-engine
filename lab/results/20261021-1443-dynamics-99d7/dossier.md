# Dossier — 20261021-1443-dynamics-99d7 (lens: dynamics and attractors)

## Claim

The census's two unflown cadence arms — the 3:1 resonance zone (17.8% fine tail's largest
cell) and the 5.4–6.3 Hill bridge (41.0% of the belt) — both certify at **16 kicks per
planet period (≈ 8 per conjunction)**, cbe6's clean-belt floor, at the plane's own
Rayleigh-e belt law, two seeds and 4× horizon: the pendulum-zone flag is a birth label, not
a dynamical state on this horizon, so ddeb's composed desync headroom moves from 78–170× to
**≈ 550×** (16.2 vs 115 events/body/belt-orbit), and the fine bill's payer flips from the
resonance tail (75%) to the 1.1% e-domain (35% of the new bill).

## Bottleneck

Board's top macro row (kicks per body, ~10³ at stake): ddeb's census priced the
desynchronised grid's belt rescue at 78× conservative, 90× (bridge@16) / 170× (zone@64)
conditional on the two arms this run flies. Every cell now measured: zones 16.7% → 16,
bridge 41.0% → 16, e-domain 1.1% stays 256. Gain: the belt's stream row falls 7× further
than the census's conservative composition (115 → 16.2 events/body/belt-orbit; 9000-anchor
headroom 78× → ≈550×, bringing cbe6's original ~10³ sentence back into measured range).
What it deletes: the per-class Δs constant table's resonance and bridge rows; nothing else
changes (the constants are already per body).

## Evidence (shipped code + this run's patch, `examples/beltzone.rs`; B12's frozen bar
worst |ΔJacobi|·r0 ≤ 1e-4; every arm 6 ships unless said, 100 planet periods)

Instrument: cbe6's `beltcad` verbatim (scene, rng, SEED dial, Jacobi expression, readout)
+ eccentric ships via `OrbitSpec.e_q48` (the plane's own belt e-law `rayleigh_q48(·,70)`,
re-drawn >0.4) + the 3:1 critical-angle tracker φ = 3λ_p − λ − 2ϖ.

- **Zone ladder (belt e-law, draws e 0.022–0.18 across both seeds):** step 8: 3.1–4.0e-8;
  6: 4.2–7.1e-7; 5: 2.2–2.9e-6; **4 (16/pp): 0.9–1.9e-5 PASS** (seed 2: 0.9–1.5e-5;
  400 periods: 1.4–2.2e-5, flat — no walk); **step 3: 1.1e-4–4.0e-3, 5/6 FAIL** (the
  negative cliff is where cbe6's clean belt breaks). Zero deaths, refusals, captures.
- **No island anywhere:** φ-scans, 25-ship grids across the whole pendulum zone at
  e = 0.10/0.20/0.30 (200 periods, step 6/4): |mean e^{iφ}| ≤ 0.008 everywhere, winding
  monotone in a (pure Kepler shear; libration would flatten it) — the true 3:1 island at
  μ = 2⁻¹⁰ is narrower than the pendulum width by ≫10× or its capture horizon exceeds 400
  planet periods ≈ 4,800 yr ≈ 30× the flyable horizon.
- **The resonant e-ridge is real dynamics, not aliasing:** at e = 0.20 a phase-sensitive
  ridge at frac ≈ −0.2 of the zone pumps Δe to 1.9e-2 (200p) / 2.6e-2 (400p), **identical
  to 2 digits at steps 6 and 4** (step-independence: cbe6's control); Jacobi stays
  2.2e-5/2.8e-5 at step 4 — the certificate is blind to the pump and the pump is blind to
  the step. The 5:2 e-law arm repeats it: Δe 6.1e-2, identical at 4 and 6, Jacobi 1.6e-5.
- **Bridge ladder (apoapsis 5.4–6.3 Hill, e-law):** step 6: 4.5–6.7e-7; 5: 2.3–2.7e-6;
  **4: 1.3–1.6e-5 PASS** (seed 2 worst 6.3e-5 — passes at 1.6× margin; 400 periods seed 1:
  1.5–1.8e-5 flat); step 3: 1.2e-4–9.9e-4, 5/6 FAIL.
- **5:2 zone (ARESC arm):** whole-zone scan at e = 0.10, step 4: 0.9–1.8e-5 PASS; e-law
  draws: 1.1–1.6e-5. The 4:1 (q = 3) and 7:3 (q = 4) inherit by order (torque ∝ e^q),
  untested directly.
- **Controls:** `belte` (clean radii, e-law) step 4: 1.3–2.6e-5 PASS (cbe6 checker2's
  e-draw arm: 3.2e-5); `strong` bites: 1 death at step 5, 3/6 at step 4 with orbits
  destroyed (Δe 5.9) — the instrument's teeth, one octave earlier than cbe6's draw
  (different phase draws; deaths are draw-lottery in the chaotic class).
- **Composition (ddeb's own formula, their class fractions, mean p_own/p_g = 0.334):**
  conservative 2×(0.412·5.35 + 0.410·21.4 + 0.178·256) = 113 ev/B/belt-orbit (their 78×);
  measured now 2×(0.989·5.35 + 0.011·256) = 16.2 → **headroom 9000/16.2 ≈ 550×**; if the
  e-domain also lands at 16, 840×.

Commands (all ≤ 60 s except the two 400-period runs ≤ 7 s): `regen.sh` regenerates every
number above into `regen.txt`; single arm:
`cargo run --release -p emergent-universe --example beltzone -- 4 100 6 zone31`
(SEED/ECCMILLI/FRACSPAN/FRACC/COREW/ARESC dials as in regen.sh).

## Predictions

`predictions.md`, written before the ladder. P1 held (strong bites; belt-class n⁻² curve
reproduces to the digit at every octave; the death octave moved one step in my draw — both
readings reported). P2 held (belte 1.3–2.6e-5). P3 held (bridge PASS at 16; the seed-2
outlier 6.3e-5 exceeded my predicted 2–6e-5 band but passes). **P4's p = 0.15 branch
happened: the zone holds 16 — no failing octave above the clean floor, no capture at any e
≤ 0.3; the mechanism prediction (aliasing-driven Δe at failing steps) is refuted in the
interesting direction: Δe is step-independent everywhere, including the ridge.** Held-out:
seed 2, 400 periods, exact-resonance fine grid, the 5:2 — all held.

## What would make it wrong

The scene is cbe6's restricted one (a circular Jupiter at 5.27 AU); the plane's Giant has
e = 0.05 (its conjunction distances breathe ±0.26 AU = 0.72 Hill) and Cinder/Home add
tides ~50× weaker — neither can demand a finer cadence than the conjunctions they ride
(cbe6's own scope note), but the margin numbers are scene's. The capture horizon is the
real edge: a 3:1 island that captures at ≳ 30× the flyable horizon is invisible to this
certificate and to B12's 4× extension; the ridge's Δe = 0.026 over 400 periods moves
apoapsis 3% of the gap, so no class change on any horizon the game flies — a birth-frozen
certificate is safe, and the re-derive trigger is the e-domain's own question, not the
zones'. The census's pendulum width over-covers the true island (that is why the zone is
quiet), so membership (conservative) and cadence (16) are separable — quoted as measured,
on the same instrument the floor was frozen on. Cloud x86 timings are order-of-magnitude
only; every number here is a count, not a time.

## Cost of adopting, and fit

Adoption is a table edit in the desync constants (ddeb's `rate` column: zone and bridge
rows 256/64·p → 16·p), zero engine change — the clocks, fired gate and intervals are
already per body (cbe6). PRINCIPLES 33: "a body resolves only the influences that are
significant at its own scale" — the pendulum label bills second-order torques that never
resolve at the horizon the certificate covers; PRINCIPLES 3: "compute only surprises" — a
zone body's only surprise in 4,800 yr is a 0.03 e-pump, which is step-independent.

## The lens

The attractor question decided the cadence question: the census priced a resonance island
that does not exist on the certificate's horizon — I mapped the angle's phase space
(|mean e^{iφ}|, winding) instead of arguing from the pendulum model, and the map is empty
at three e slices, which is why 16 suffices. What the lens may have missed: the empty map
is a statement about this scene and horizon, not about the resonance — the Kirkwood carving
lives at Myr through secular chaos my one-planet scene cannot produce; the run's residual
is the e-domain (1.1%, now paying 35% of the composed bill) and the Giant's e = 0.05, both
named above.
