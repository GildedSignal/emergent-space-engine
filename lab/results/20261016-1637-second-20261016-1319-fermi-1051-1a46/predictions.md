# Predictions (written before the decisive flight)

Held out: everything below is stated before any ES_SECULAR flight and before the corrected
legality arithmetic is run. The arm: `ES_SECULAR=1` in `crates/universe/src/step.rs` — a ship of
a doll (not a fleet member, not the player) whose orbit is secular-legal against **every
perturber** of its doll is deleted from the metronome (its plan is cleared: a pure tube), where
legal means r9's bound per perturber, τ_p = 3·(m_p/m_host)·(a/a_p)³ < τ₀ = 3.6×10⁻³ for the
parent star and for every secondary source of the doll, plus a resonance exclusion (no
small-integer period commensurability q/r ≤ 8 within 2%, co-orbital |a−a_p|/a_p < 5%).

## P1 — the legality domain, measured from the runtime flag (not composed)

The checker's Attack 1 says the Moon's tide puts the whole top in-situ octave 1.1–49× over τ₀
(~80% of in-situ legal). Those two numbers are mutually inconsistent with any (a/d)³ scaling:
(166,400/83,200)³ = 8, but 0.175/3.9×10⁻³ = 45. My arithmetic: τ_Moon = 3·2⁻⁶·(a/273,684)³, so
the crossover τ_Moon = τ₀ sits at a ≈ 152,000 root units (inside the top octave) and the top of
the octave (166,400) is only ~3× over. **Predicted: the Moon kills 3–6% of the in-situ 225
(a > 152–166k), not a fifth of them; in-situ legal fraction 94–97%.** The quarter (75) is illegal
by the co-orbital rule; the belt is legal except near the Giant's 3:1 (2.50 AU), 5:2 (2.82 AU)
and 7:3 (2.94 AU) bands: belt legal fraction 85–98%. The star's tide alone leaves the top octave
just under τ₀ (3.48×10⁻³ < 3.6×10⁻³): the Moon, not the star, draws the line.

## P2 — the residual storm (the decisive number)

N=1000 coast, 5,400 game-s, rtf 100, seed 1, budget-free (4fa8's protocol): OFF reproduces max
334 / p99 136 (the record). **With ES_SECULAR: max events/frame ∈ [90, 180]** — the spared
standing comb (the quarter's 75 + the illegal in-situ + the plane's ships + the fleet) sets it;
if the answer lands under 90 the script's proportional 83.5 wins, if it lands 100–180 the
"≈134 Moon-corrected" class wins. p99 ∈ [35, 75]. The de-phase's 53 is NOT reached by the delete
(a resonant quarter cannot be deleted).

## P3 — the event ledger

Total events at 5,400 game-s fall by the deleted fraction of the metronome population, both
populations at once (the comb's doll-2 ships and the belt's stream): predicted total events
22,219 → 9,000–13,000 (−45% to −60%); kicks and boundaries both fall; the delete is the only arm
that cuts the belt stream's own constant (the 10⁹ rail's metronome), which no spread arm touches.

## P4 — the control

The patched binary with no env flags is bit-identical to pristine main: `ladder_digest` all
cases, every schedule, same digest; the OFF flight's event counts equal 4fa8's record exactly.

## P5 — the B14-class probe (the freeze's own legality, measured)

For every frozen legal local, the end-of-flight position angle under ES_SECULAR minus under OFF
is the secular precession the freeze drops. **Predicted: per-orbit Δθ ≈ (3/4)·2π·τ_max,perturber
within a factor 2** (the quadrupole tide's apsidal rate), and every legal body's per-orbit Δθ
stays under 2× r9's τ₀ per-orbit bound (1.7×10⁻² rad/orbit); the accumulated Δθ grows linearly
with orbits elapsed — the measurement prices the sparse re-kick cadence step 5's real generator
needs (predicted: the top legal octave needs a re-kick every ~10² orbits to stay under a 0.1-rad
apse error at the flight's horizon).

## P6 — adversarial control (not tuned on)

`ES_SECULAR_RES=1` (the same arm with the resonance exclusion off): the quarter is deleted too;
the residual storm drops further (predicted max ∈ [50, 100]) but the resonant quarter's physics
is dropped with it — the resonant L4/L5 ships' angle error vs OFF grows without bound (they ride
fixed tubes while the kicked reference librates). This is the falsifier that the resonance
exclusion, not the delete, is what protects the spared set.

## What would kill the claim

- OFF ≠ pristine on any digest (the arm leaks into the shipped law).
- The residual storm above 240 (the delete buys nothing: the comb survives elsewhere).
- Per-orbit Δθ of legal bodies above 2× the τ₀ bound (r9's transfer to these tides fails, and
  with it the delete's legality domain).
