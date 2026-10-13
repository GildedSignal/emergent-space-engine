# Dossier — 20261013-0037-dynamics-1890 (lens: dynamics and attractors)

**Claim.** After the merged exact-in-E clock (f7f6d87), the clock holds in every never-flown
regime (braking reversals at γ 30 and 300, sustained turning burns, far bound orbits:
dt/dτ = u^t to 1e-6–4e-12), but two new walls replace the old one: a held brake key is a pump
below γ ≈ 1.2 (rest is a crossing, not a fixed point), and the far hyperbolic `Range` refusals
are the fit's arithmetic, not the key — every tested refusal point rebuilds and compiles the
same (periapsis, k) key through `OrbitKey::from_invariants`.

**Bottleneck.** `high-gamma-clock`, open directions 1 and 4 of its wiki page (the unmeasured
regimes; re-measure the wall and the clock–dial agreement after the merge). This maps what the
merge did and did not fix, and sizes the HANDOFF's open limit ("a fast flight far from the star
is lost") as an arithmetic fix, not a representation change. Gain: deletes the idea that a new
key format is needed for far flights; kills the "held brake = brake to rest" playability plan.

**Evidence** (all from shipped code at 17ace3e6; commands in `regen.sh`, ≤ 5 min total):

- Flights (`flights.txt`, example `clock_regimes`, settle-based, 5 regimes, 229 s wall):
  - `fwd15`: no fault to γ 334 at t=1.79e11 (my 55 s wall cap, not the engine); clock_relerr
    1.0e-6 at γ 334; periapsis 9.16e7 M and rising toward the far wall.
  - `brake_g30`: retro L15 from γ 30.7 → γ min 1.208 at t=3.26e10, then the same held key
    pumps back up through γ 10.7 … 186.7 (still rising at window end). Clock_relerr ≤ 1.7e-6
    through the whole reversal. `brake_g300`: same shape (switch at γ 307, γ 306.9 at window
    end after braking and repump start).
  - `turnburn15` (forward+left from γ 30): γ → 1.19, periapsis → 2.1e10 M, **69,660 refusals
    survived** on the old binding — a flight can live for 10^5 rebind refusals.
  - `fwd2_farstar`: silent death (`fault=None`, `alive=false`) at the leave (2^40, step.rs:667):
    the L2 escape settles onto a bound orbit (k=0.526 > 1/2, E=1.000000) whose apoapsis passes
    the edge. Slow far flights end at the leave, not the key wall.
- Domain sweep (`domain_sweep.txt`, example `clock_domain`, 22 E × 22 periapsis states at exact
  Schwarzschild periapsis, 17.5 ms): E → 1⁺ compiles at **every** periapsis 10 M … 1.6e10 M
  (the parabolic edge is safe; the brake's E-crossing has no wall). `Range` refusals form a
  jagged boundary: E=1.1 at 2e9 M, E=2/5/31.6/100 at 4e8 M, E ≥ 1e4 at 3e8 M. At E ≥ 100 the
  accepted k ≈ 1/periapsis, E-independent (the shape carries no E; the gap does — the merged
  design's premise, measured). `NoBoundOrbit` appears only at small periapsis × huge E (capture:
  E=1e6 at peri 1e3–1e5) and is physical.
- Discriminator (`discriminator.txt`, example `clock_disc`): at all 8 tested `from_state`
  `Range` points, `OrbitKey::from_invariants(E−1, L)` builds peri and k matching to 4 digits and
  `Passage::compile` accepts (5 cleanly; 3 of my reconstructions hit `Topology`/
  `NoBoundOrbit` **also on neighbouring ok rows**, so my edge reconstruction is off there —
  reported as-is). The wall is the state→key fit path, not the key representation.

**Predictions.** `predictions.md`: 2 held, 1 half-held (the pump was the miss and the finding),
1 missed (the leave, not Range, ends slow far flights), 1 partly wrong (the Q48-k mechanism is
refuted by the measured k ≈ 1/peri; replaced by the fit-arithmetic finding).

**What would make it wrong.** My flights all start from the same plane seed and nose (the
retrograde-nose trap is unfixed on main); a prograde-nose build could change the pump's
threshold γ, not its existence (the pump is fixed-attitude geometry, not nose convention). The
sweep states sit exactly at periapsis with vr=0; the shipped rebind sees generic states (the
`clock_debug` off-periapsis rows behave identically at ±10% radial speed). The discriminator's
`from_invariants` inputs are my reconstruction of L, not the flight's own words — a checker
should re-derive L from the flight's tube units before adopting "fit from invariants" as the
fix. Cost of adoption: none for the measurements; the fix it points to is a fit-path change
(one builder step), not a law change. Fit: "It is a game" and "A fix signals the wrong
representation" — here the representation (key + gap) is right and the *fit arithmetic* is the
fix's target; and "the cheapest compute is compute not done": the pump finding says attitude
control, not more engine, is what brake-to-rest needs.

**The lens.** An attractor framing found the pump; it also made me predict a near-star dive for
the turning burn (wrong sign — the held-key geometry dominated). What the lens missed for
others to check: the 69,660-refusal survival means refusal counts alone cannot certify a lost
flight — a scheduler or allocator reading `refusals` as distress would misjudge a healthy
flight (Kingman-flavoured: the refusal queue is not the work queue).
