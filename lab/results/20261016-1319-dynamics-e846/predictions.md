# Predictions — 20261016-1319-dynamics-e846

Written before the 512 P plane arm and the oracle element arms ran. What I have seen
before writing this: the shipped code (step.rs `plan_terminal`/`crash`/`kick_clock`,
restricted.rs, plane.rs), the b9be dossier and its checker's note, and one 32 P
smoke run of two ICs to validate the harness compiles (no ensemble numbers).

Question (chaos-shadowing open direction 4): the plane loses 48/144 co-orbital
ships the float oracle keeps. Real star-crossing periapsis of a diverged
trajectory, or spurious planned terminal?

Instrument (all new, this run): osculating elements q(t) = a(1−e) from
heliocentric E, L at every P/8 sample — a computed quantity, blind to none of
the geometry (grid-sampled minima are blind to perihelia: dwell below 2q is
~P/10⁵); the Jacobi constant J(t) of plane and oracle states; the rotating-frame
critical values J(L1), J(L2), J(L3) of the scene; and a print-only census of the
engine's Lost branches (star surface at kick/boundary/crash, planet surface,
system edge, plan failure), env-gated `DIVE_TRACE`, outcomes untouched.

Decision rules, frozen:
- A plane death is **REAL** iff the truth can be on a star-crossing orbit at the
  death epoch: oracle osculating q at t_d (dense local window) ≤ the star surface
  S, or J₀ ≤ J(L1) so the zero-velocity neck at L1 admits the star's lobe at all.
- A plane death is **SPURIOUS** iff J₀ > J(L1) (the truth is confined outside the
  star's lobe for ever — an invariant, no trajectory argument needed) AND the
  oracle's osculating q never comes within a factor 2 of S.

Predictions:

- **P1 (the invariant split).** The 48 deaths split by confinement: I predict the
  majority of dead ICs have J₀ > J(L1) (truth confined; death spurious by
  invariant), because the death epochs sit within ~1–2 P after the first close
  conjunctions — too fast for honest transport through a neck, about right for a
  quantized kick at the conjunction pumping e past the surface threshold in one
  step. Falsified if most dead ICs have J₀ ≤ J(L1).
- **P2 (the channel).** ≥ 90 % of the deaths are planned terminals (a
  `What::Crash` item from `plan_terminal`, i.e. the compiled tube's key periapsis
  under the surface), not kick-time or boundary surface detections, and not the
  system edge.
- **P3 (the J walk).** The plane's J(t) walks away from the oracle's flat J₀ at
  conjunctions; ships that die cross J(L1) (or come within the walk's own size of
  it) before dying; survivors do not. The oracle's J(t) stays flat to ≤ 1e-9
  relative over 512 P (integrator control).
- **P4 (the osculating manifold).** Where J₀ > J(L1), the oracle's min osculating
  q over 512 P stays ≥ 2·S (confined truths never even approach the manifold);
  where J₀ ≤ J(L1) it can dip to S (the crossing is available to the truth).
- **P5 (controls).** (a) A constructed state already inside S dies in the plane on
  its first item (positive control of the death channel) and reads q ≈ its true
  q in the oracle pipeline. (b) The two earliest deaths reproduce at 10.75 P and
  12.0 P (b9be checker's epochs). (c) Oracle at 1e-13 changes no class.
- **P6 (the survivors).** The 96 survivors' plane J walk stays on their J₀ side
  of J(L1); their death-free status is the plane being consistent with the
  invariant, not luck.
