# Predictions — run 20261013-0236-redteam-7ab4

Written before the decisive experiment. Scene: a test moon on a circular orbit of
radius r_c about a source of mass M (G = M = 1), orbital speed β_c = v_c/c. The
source's motion changes at t_k (an impulsive Δv, or a sustained burn). Three
readouts for the moon's force: **inst** (the source's true state at t — today's
plane), **news** (law.md:33 — the newest source *tube version* whose emission the
moon's past light cone has met, that free-fall tube evaluated at t; version switch
at cone arrival, found by bisection), **ret** (pull toward the retarded position —
Laplace control). Units: r_c = 1, P = 2π. Lowered c (c = 1/β_c …) so the light
window T = r_c/c is a fixed fraction of P; β_c is the only physical knob.

## P1 — the impulsive rebind leaves a permanent, one-sided scar (the attack)

For t < t_k + T the news moon is pulled by the old tube (kick invisible); at the
cone the version switches; after, both readouts see the same kicked tube. The moon
keeps forever the velocity it wrongly gained/lost during the window:
**|Δv_moon(∞)| = |Δv|·β_c²·k/2, k = tidal projection factor O(1)** (derivation:
J = ∫(∂F/∂x)·Δv·t dt over [0,T], (∂F/∂x) ~ v_c²/r_c²). Predict the fitted exponent
of |Δv_moon| against β_c over β_c ∈ {0.003, 0.01, 0.03, 0.1, 0.2, 0.3} is
**2.0 ± 0.1**, one-signed across seeds for a fixed kick geometry.

## P2 — magnitudes

J/|Δv| = β_c²/2: 4.5e-6 at β_c = 0.003 (a Jupiter moon: news ≡ inst, confirming
a237's 1e-7-class agreement in the only regime any gate scene sits), but
**5e-3 at β_c = 0.1 and 4.5e-2 at β_c = 0.3** — percent-level, the game's selling
regime (living near a compact mass), for *every* rebind of the doll origin.

## P3 — the Laplace control fails harder

ret's permanent error ≥ 10× news' at every β_c (its field stays wrong after the
cone: no extrapolation). If ret ever beats news, the harness is broken.

## P4 — a sustained burn is cadence-invariant (the structural claim)

Under sustained source acceleration a_b, each tube version extrapolates *free
fall*, so the news source readout lags the truth by a constant position error
≈ ½·a_b·T² (velocity error a_b·T), independent of rebind cadence once epoch ≪ T.
Predict: plateau of the source-position readout error at two cadences (T/8 vs T/32
epochs) agrees within 5%, and the moon accumulates drift linearly during the burn.
This is the point the version ring cannot fix by rekeying faster: **the tube
carries (position, velocity) per version and GR's near-zone field carries the
acceleration too.**

## P5 — it is representation error, not integrator error

Halving dt changes the measured J by < 2% (fixed T/P = 0.15).

## P6 — what this does NOT kill

News is *right* to withhold the kick until the cone (P5 of a237; principle 23).
The scar J is the causal half itself, measured; the 1PN near-zone oracle (EIH)
cannot adjudicate it (its gauge is instantaneous). So the premise is not killed by
P1/P2 — it is **unmeasured by every gate, unfalsifiable by every rung** (e300: all
named gates byte-identical under news), and its error model against GR for
accelerating sources is missing an acceleration term in the version payload.
Kill criterion for my own claim: if the fitted exponent in P1 is ≈ 1 (not 2), or
J is not one-sided, or P4's plateau scales with cadence, my model of the version
ring is wrong and the attack collapses to "instrumentation gap only".
