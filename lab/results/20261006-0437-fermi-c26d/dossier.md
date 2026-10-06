# Dossier — 20261006-0437-fermi-c26d (Fermi lens)

## Claim

The live-information floor of a belt is not the born program's 0.126 bits/body
but a heating trajectory: mutual encounters drive per-body scar entropy to
~92 bits/body by the 10-Gyr horizon (11.5 GB at 1e9 bodies — over the ~6 GB
engine share), with the phase column alone pinning ~20 bits/body within ~1e4
orbits for any belt massive enough to exist; an identity-reassigning repack
every <=1.2e4 orbits holds the floor under any budget, and collision-tame
belts (<=1 collision/body over 10 Gyr at 1e9/belt density) produce no
encounter scars at all — the game must choose belts-as-physics (heavy,
collisional, repacked) or belts-as-scenery (light, phase-floor only).

## Bottleneck

Board focus item: "fitting 1e9 in 8 GB (crates/shipmem: population programs
plus scars; every body real, never averaged), decided by distinctions created
per game-second". Expected gain: this decides the design's memory law (repack
cadence, quanta, belt mass) before shipmem is sized — it deletes the risk that
B18's "measured information floor" is measured on the wrong (newborn)
population.

## Evidence

Fermi decomposition, cross-checked by measurement (script below, 1.4 s):

- Per-orbit velocity diffusion (Oepik, aggregated): kappa_v =
  sqrt(8*pi*mu^2*n*T_orb*ln(b_max/b_min)/v_rel) = 2.9e-3 m/s/sqrt(orbit) for
  m = 2e16 kg, 1e9 bodies in the 0.6-AU belt at 2.5 AU (n = 2.2e-25/m^3,
  v_rel = 1.9 km/s). Belt stays stable: sigma_e = 7.1e-3 and sigma_a/a = 9.1e-3
  at 2.5e9 orbits (band half-width 0.24); no ejections.
- Column walks (measured, match head values): sigma_a/a = 1.8e-7*sqrt(T),
  sigma_e = 1.4e-7*sqrt(T); phase sigma_M ~ 5.4e-6*T^1.5 rad (shear amplifies
  the a-walk) -> wrapped-uniform by ~1.3e4 orbits.
- Scar bits/body (deltas from the program-evolved state, q_rel = 1e-6 per
  column; a: 15.2, e1/e2: 14.9 each, i1/i2: 13.7 each, M: 19.9 pinned):
  34 bits at 1e3 orbits, 48 bits crossed at 1.23e4 orbits (~49 kyr sim; ~a
  long play session at 100x), 92 bits at the 2.5e9-orbit horizon -> 11.5 GB at
  1e9 bodies vs ~6 GB usable. q sweep: 72 bits (1e-5) to 112 (1e-7).
  Joint = marginal sum - ~1 bit (mutual information ~2.5 bits early, ~0 after
  phase pins); kNN cross-check = +2-3 bits (known high bias in 6-D).
- The phase floor is universal: M pins ~log2(1/q_rel) bits whenever
  kappa > ~1.5e-10 m/s/sqrt(orbit); even 1.6e8-kg bodies (kappa = 2.9e-11)
  pin it by the horizon. Every belt with bodies larger than ~10 m reaches the
  ~2.5-GB-at-1e9 phase floor within 10 Gyr unless something reabsorbs it.
- Mass-density squeeze (unplanned finding): collisions per body over the
  horizon = n*pi*(2 r_c)^2*v_rel*T: 2.5e5 for (2e16 kg, 1e9/belt), 255 for
  (2e16, 1e6), 1.0 for (5e12, 1e6) and (1.6e8, 1e9). Collision-tame belts
  have kappa <= 2.6e-8 -> 0-20 bits/body total (2.5 GB at 1e9, phase only).
  There is no middle at 1e9/belt: encounter-scarred belts grind; collision-free
  belts do not scar.
- Allocator: dBits/dT ~ 2.3e-6 bits/body/orbit at 1e6 orbits -> 0.0002 B per
  game-second at 1e9 bodies and 100x time. Distinction creation is a memory
  question, not a bandwidth one.
- Repack: floor = H(walk since repack); from the curve, T_r = 1.2e4 orbits
  holds <=48 bits/body, T_r ~ 300 orbits holds <=24. A belt-wide re-sort every
  ~40 kyr of sim time is idle-time work.
- Controls: kappa = 0 stays at 0.0 bits (program-referenced scars verified);
  10x kappa grows faster (80.5 vs 62.8 bits at 1e6). Machine: load 5.2/8
  cores, 12.8 GB available, run took 1.4 s, peak memory negligible.

Reproduce: `cd lab/results/20261006-0437-fermi-c26d && python3 work/belt_heat.py`
(numpy + scipy; deterministic seed; writes work/heat.json; logs in
work/run{1..4}.txt — run4 is the final physics, run1-3 document two
instrument bugs found and fixed: program-referenced M, and M advanced with dt
in orbits instead of seconds).

## Predictions

`predictions.md` was written before the decisive run. Score: 4 held, 3 missed.
Held: phase saturation window [1e4, 1e7] (measured 1.3e4); ceiling 70-110 bits
(measured 92); 48-bit crossing window [1e3, 1e8] (measured 1.23e4); creation
rate < 1 MB/game-s (measured 0.0002 B/s). Missed, all the same direction —
heating faster than my head: kappa_v = 2.9e-3 vs band [2e-4, 2e-3] (three
compounding factor errors in n, v_rel, ln); bits at 1e6/1e9 orbits above my
bands (63/92 vs [8,40]/[30,75]) because I under-weighted the phase column's
early pinning; joint/marginal-sum ~1.0 vs predicted [0.5, 0.9] — kick
coherence across columns does not survive phase saturation. The misses make
the memory conclusion stronger, not weaker.

## What would make it wrong

- If the engine's compiled drift does not exactly re-derive each program
  body's Kepler phase, "program-evolved" is not free and scars redefine.
- If the conjunction scheduler tolerates phase coarser than my swept quanta
  (phase only matters at encounters), the M column shrinks by log2 of the
  tolerance; the B-gates own that number.
- If belts in the game are lighter or sparser than my mass-density corners,
  encounter scars vanish (measured: kappa <= 2.6e-8 -> 0 bits beyond phase).
- The impulse/CLT aggregation (lambda ~ 6e6 encounters/orbit, delta-v/v_rel
  ~ 5e-5 at contact) and isotropic kick directions are approximations an
  independent implementation should not inherit (reproduce with direct paired
  two-body scattering on a small belt).
- 6 GB usable of 8 GB is an assumption, not a measurement.

## Cost of adoption, fit with PRINCIPLES

Adoption: (1) B18's "measured information floor" must be measured on an aged,
heated belt (or bound a repack cadence), not the newborn program — otherwise
the gate certifies 0.126 bits/body and the live engine pays 92; (2) shipmem
needs an identity-reassigning repack (re-sort + re-program marginals + a pin
set for player-observed bodies) — the shelf's seal/compact repack re-packs
ordinals but never reassigns them, so uniform phase entropy is never
reabsorbed; (3) the belt mass choice is a design decision between physics and
scenery, squeezed by collisions from above and meaninglessness from below.
Cost: one mechanism in shipmem plus one clause in B18; no engine change.
Fits PRINCIPLES 24 ("The memory floor is information-theoretic" — measured,
and it moves with time), 6 ("Store the generator, not the generated" — repack
re-infers the generator for heated marginals; "influences below one quantum
accumulate" — the sub-quantum walk is the scar), 5 ("The player is the only
wildcard" — only player-observed identities must survive reassignment), and
law.md's population form ("program plus scars"). Population analogue of the
memo's "a rotated orbit is the same cycle": a phase-shifted belt is the same
belt.

## The lens

The Fermi lens estimates ensembles and was weakest exactly where a single
column (phase, by shear T^1.5) dominates the floor — my head estimate of its
arrival time was 300x optimistic until the units bug forced the derivation.
I did not probe the resonance/tide channels (parent tide, mean-motion
resonances) that can heat a belt far faster than mutual encounters; if they
inject element noise above quantum, all my arrival times shrink and only the
repack conclusion survives. Strong-encounter (m-meso) scarring was not modelled:
an exact pair event leaves a bigger, correlated scar than an impulsive kick.
