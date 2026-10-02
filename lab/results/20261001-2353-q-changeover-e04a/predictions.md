# Predictions — 20261001-2353-q-changeover-e04a

Written before the decisive run. Tuning happens only on 2 smoke seeds (k=2.0 and k=1.0,
one shallow one deep) to fix implementation constants: TRACE's roundtrip tolerance eps and
MERCURIUS inner tolerance. Everything else (32-seed set, deep bins, moon case, JANUS demo)
is held out: no parameter will be touched after this file.

## The model and the judge (fixed)

Plane's model: star (1-mu) fixed at origin, planet mu on a prescribed circle sep=1, Omega=1,
test particle. mu = 1e-3 (Jupiter-like). Exact invariant C = v^2/2 - (1-mu)/|x| - mu/|x-x_p| - Omega*L_z.
err(t) = |C(t)-C(0)|/|C(0)| at P/8 samples over 200 periods. Growth exponent = the B12
fit (16 log-spaced window maxima, last 90%, LSQ slope). Floor 1e-12; err_max 1e-4.
Seeds: 16 with k=da/R_H in U[1.5,3] (B12 recipe), 16 with k in U[0.5,1.5] (deeper, held out).
Base step H = P/64 everywhere. Events = encounter-machinery invocations per pass
(pass = local minimum of r below 3 R_H, counted on the truth's fine samples).

## Predictions

1. symba (the incumbent mechanism: smooth weights of separation only, recursive
   sub-steps, ratio 4, 3 levels, shells 2^(1-l)*R_edge): median exponent <= 0.1,
   max err <= 1e-4, events per pass in the tens to low hundreds (level-1 kicks dominate).
2. trace (time-symmetry check per step, halve-and-retry): median exponent <= 0.2 at
   fewer events per pass than symba (I predict 3-20x fewer retries than symba's level>=1
   kicks), because retries concentrate only where the roundtrip actually breaks. Its
   per-step check overhead is a 2x multiplier on the base map, not events.
3. mercurius (Heaviside handoff at 3 R_H to a DOP853 inner integrator): only 2
   handoffs per pass, but I predict the median exponent lands in [0.2, 0.7] - the
   handoff's phase mismatch accumulates per pass, so it fails the 0.2 bar even though
   the paper's single-run energy errors look smooth. Inner force evaluations per pass
   in the hundreds.
4. wh-fixed (no changeover, H=P/64): fails outright - median exponent >= 0.8 and
   max err >= 1e-2 at deep passes.
5. wh-dense (H=P/512, no changeover): max err ~1e-5-1e-4, exponent <= 0.3, at
   512 kicks/orbit - the cost the changeover exists to delete.
6. soi-switch (events3's configuration: the drift switches dominant body at the SOI,
   state-selected): exponent 0.6-1.0 (events3 measured 0.83).
7. truth (DOP853 rtol 1e-12, positive control): |dC| < 1e-12, exponent <= 0.15 (noise
   windows rise slowly).
8. By periapsis bin (0.1-0.3, 0.3-1, 1-3 R_H): symba and trace hold exponent <= 0.2 in
   all bins; mercurius and soi-switch degrade as the pass deepens (handoff mismatch grows
   with the swing in force).
9. Moon case (massive moon 1e-5, full three-body, energy error judged): symba <= 0.15,
   trace <= 0.2 with fewer events, mercurius >= 0.3.
10. Reversibility (JANUS-style integer demo): a switch may depend on the state without
    breaking (bit) reversibility iff it depends on positions only and every branch map
    is an exact integer map with an exact integer inverse. I predict: smooth changeover and
    even a position-only Heaviside selector are exactly bit-reversible in integers, a
    velocity-dependent selector is not - and the position-only Heaviside selector, while
    bit-reversible, still drifts in its invariant (exponent > 0.2): reversibility and
    bounded error are different properties; what kills the error is keeping the split a
    single Hamiltonian splitting (smooth in position), not reversibility itself.

If 2 and 1 both hold with trace cheaper, the lens's gold question (exponent <= 0.2 at
fewer events per pass than SyMBA, with a path to integers) has a positive answer with
TRACE - unless TRACE's integer path (halving integer steps) turns out the blocker, in
which case gold goes to the smooth changeover's integer path and TRACE is the float bridge.

## Addendum (written before any scheme ran on the held-out group)

The second seed group (circular k in U[0.5,1.5]) produced no passes at all on the truth:
those orbits are co-orbital-captured (libration), never approaching the planet below
3 R_H (measured on truth only, scheme-independent). Replaced by an eccentric-crossing
group: a = 1 +- 2 R_H, e in U[0.03,0.15], random periapsis and phase, giving 8-33
passes per seed at median periapses 0.45-2.35 R_H. All other predictions stand; nothing
was tuned on any scheme's outcome.
