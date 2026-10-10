# Predictions — 20261010-0541-dynamics-6565 (written before the decisive sweep)

Question: are belt encounter arrivals an independent (Poisson) stream or a
self-exciting cascade, and where does the branching ratio cross 1?

Setup (all runs): Wisdom–Tremaine shearing sheet, N=2000, box 30×30 (Ω=1),
restitution ε=0.7 (inelastic; the elastic limit runs away — measured, see
dossier), warm start e0=0.3 (Rayleigh), T=150 Ω, cap 4·10⁵ events.
Tuned on: τ=0.005 cold (486 events, no heating in 150 Ω) and τ=0.1 warm-cold
(e0=0.01 → heated to e≈6.4, rate ≈ 1–2 events/body/Ω).
Held out (not run yet): τ=0.02, τ=0.5, τ=2.0, and the e0-independence pair.

## Pre-registered predictions

P1 (τ=0.02, held out): Fano(W=5) in [0.8, 1.6]; partner-branching b < 0.15;
   burst p99 < 2× the Poisson null's p99. Encounters are effectively Poisson
   at game-like belt concentrations.

P2 (τ=2.0, held out): a clean dichotomy, pre-registered as the decision rule —
   either (cascade side) Fano(W=5) > 3 AND b > 0.5 AND burst p99 > 10× null,
   or (no-cascade side) Fano(W=5) < 1.5 AND b < 0.15. The middle band
   (Fano 1.5–3) counts as "no clean transition" and is reported as such.
   Prior expectation stated before running: the cascade side wins, because a
   collision scatters both guiding centres into conjunction with new partners
   within one synodic period (~4–10 Ω at e~R scales), and dense inelastic
   rings are the viscous-overstability regime (ε=0.7): I expect oscillatory
   clustering at W ≈ 10 Ω, i.e. Fano(W=10) > 2 with a visible rate wave.

P3 (τ=0.5, held out): between P1 and P2 monotone in τ; if P2 is cascade-side,
   Fano(0.5) ≥ 1.5.

P4 (attractor, e0-independence at τ=0.1): starting at e0=0.01 and e0=1.0 both
   land within ±30% of the same e_mean by t=150 Ω (the warm start converging
   down, the cold start up toward the same attractor e_eq(τ=0.1) ≈ 6–7).
   If the two ends differ by >30%, the state is path-dependent (hysteresis)
   and that is the finding.

P5 (calibration, negative control): on the τ=0.02 run, the real stream's burst
   p99 and Fano band must sit inside the Poisson null band of the same
   analysis code (same harness), else the instrument is broken, not the belt.

## Kill criteria
- If P1 fails on the Poisson side (Fano > 1.6 at τ=0.02), the claim "game
  belts are Poisson" dies at that concentration: report the measured number.
- If the event stream has < 5000 steady-state events in any held-out run,
  that run is VOID for burst tails (not enough statistics), kept for rates.
- If the simulation hits the event cap before t=100 Ω, only the window before
  the cap is used, and it is named in the dossier.
