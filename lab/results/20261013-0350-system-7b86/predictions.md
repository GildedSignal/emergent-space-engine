# Predictions (written before the decisive run)

Scenes: the frame-cost flights (coast, held forward burns L8/L12/L15, brake L8, turn-then-burn L8),
paced 8 s, 60 Hz, rtf 100, seed 1, 48 members — deterministic inputs; the machine only sets the frame
budget's cut, and no number below depends on presented ticks beyond the window sampling.

The claim under test: the acceleration the last committed kick already stored (`kick.dv/kick.len`)
reproduces `observe::partial`'s fresh `force::field` evaluation within the readers' quanta, so the
per-read field evaluation (the view's frame constraint) is re-derivation of a stored value.

1. **Read-window error (the view consumer).** With the gather's own read quantum being one integer
   root tick, I predict the stored-a readout's position error is below 1 root tick on ≥ 99% of reads
   on every plain scene (coast and held burns to L12), because the kick's window is chosen by the
   law's own cadence rule to resolve the same force it samples. **Kill:** if the p99 exceeds
   1 tick on a plain scene, the slot does not serve the view and the unification is dead there.
2. **The tail names the domain, not the claim.** On L15 (the dive) I allow the max to exceed the p99
   by orders of magnitude near periapsis; if the *p50* there still holds sub-tick, the domain edge is
   the dive, which the frame-cost run already owns.
3. **Clock fraction.** Most reads on the plane are motion-law-v2 bindings (`clock%` ≥ 60): the
   partial path, not the ramp. If `clock%` is near zero the claim's reach shrinks to the fleet's
   members and the census is the result instead.
4. **Read multiplicity.** `reads/bf` (gather readouts per body per frame) lands in 1.0–2.0 (the view
   page's 1.0–1.92 readouts/emitter): each of those is one fresh field evaluation plus a tube decode
   today, and one table lookup under the slot.
5. **Light window (the gravity consumer).** The quadratic payload's residual (⅙·|Δa|·T²) cuts the
   linear payload's error (½·|a|·T²) by ≥ 10² on the scene's own light window; if the cut is < 10,
   the slot buys the gravity consumer little beyond what gravity-news already measured and the claim
   narrows to the view.
6. **`no-stor` is small** (≤ 5% of samples): the previous committed kick at the same level almost
   always exists. If it is large, the stored value is not where I claim it is and the probe's model
   of the history is wrong — that would void the measurement, not the claim.

Controls already on record: the counterfactual cadence for the waterfall consumer (0–24 events vs
377–1,085 kicks, run 174d) and the ½·a·T² lag for the gravity consumer (run 7ab4) are cited, not
re-measured; this run adds the view consumer and the shared-slot identity.
