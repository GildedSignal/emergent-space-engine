# Predictions (written before the decisive run)

Question: the plane rebinds a tube on every kick (64 per orbit; the exact cycle memo then hits 0%
on distinct kicks), and separately maintains a re-anchor threshold for memo reuse and a "slack
skin" for encounter certificates. Hypothesis: all three are one mechanism — defer the kick's
application in an exact accumulator and renew the binding (and its dependents) only when the
accumulated effect crosses one quantum q. Cases below were not tuned on; they are the held-out
behaviour checks.

Scene: restricted circular three-body (Sun + Jupiter mu=1e-3 + ship), Wisdom–Holman split, exact
Kepler drift, kicks = the perturber's difference acceleration, truth at 1024 kicks/orbit.

Predictions:

1. **Renewal collapse off resonance.** Ship at a=2 (far from strong resonances), e0=0.05,
   10^3 orbits, force still sampled at 64/orbit. With deferral quantum q_v (velocity units),
   renewals per orbit fall as q_v grows; at the q_v whose induced position ripple stays under
   the immediate-64 run's own error scale, renewals drop by >= 5x vs 64/orbit.
2. **Same cadence, fewer bindings, same accuracy.** Deferred at 64/orbit sampling with ~8-ish
   renewals/orbit keeps energy-error max and eccentricity error within ~2x of immediate-64
   (and beats immediate at 8/orbit sampling with 8 bindings/orbit).
3. **Defer is not discard.** The control that applies quantized kicks and DROPS the residue
   (the rejected "quantized (E,L) memo") random-walks: energy-error growth exponent >= 0.4,
   while deferred stays bounded (exponent <= 0.1; bounded by ~|v|*q_v + base integrator error).
4. **The hard case: resonance.** At the 2:1 resonance (a = 5.2 * 2^(-2/3)), the same deferral
   distorts the resonant response (e-pump or libration amplitude ratio leaves [0.8, 1.25] vs
   immediate-64) as q_v grows, because the phase feedback arrives late. If the toy's amplitude
   is too weak to show it at any q_v that still collapses renewals off resonance, that is a
   miss and I report it as one (the selector stays load-bearing by law.md's rule either way).
5. **Apsidal behaviour is kept off resonance.** Perihelion-orientation drift per 100 orbits
   within 10% of immediate-64's (phase identity is NOT demanded; the apsidal rate is a
   behaviour).

Kill criterion for the hypothesis: if deferred-at-64 with renewal collapse (>= 5x) does NOT
hold energy bounded (prediction 3's exponent), or loses the apsidal rate by > 10% at every q_v
that collapses renewals, the one-mechanism claim dies for bindings (the skin and the jet stay
separate).
