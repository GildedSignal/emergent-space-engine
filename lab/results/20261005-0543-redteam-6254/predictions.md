# Predictions (written before the decisive experiment)

Held-out cases — none of these have been tuned on; they follow from the premise analysis only.

## P1: order non-commutativity of the contact law (the decisive one)
Three bodies, one at rest, two equal partners hitting it from opposite sides at the same
epoch. Resolving the two same-epoch contact pairs in different sequential orders produces
**O(1) different final states** (which body carries which velocity), not rounding-level
differences, under both a float elastic law and (prediction) the repo's own integer
resolver `crates/lattice::law::resolve`. The symmetric simultaneous resolution gives a
third distinct outcome. The premise "two evaluation orders, identical bits" therefore
requires one law-owned canonical order for same-epoch events; the docs specify none.

## P2: multi-event same-epoch batches are the norm at the design's own dense threshold
The design switches to the dense order when events per cell per light-crossing ≈ 1.
Prediction: at λ = 1 (Poisson), 1 − 2/e ≈ **26%** of cells have ≥ 2 same-epoch events,
and in a random contact gas at that density **≥ 5%** of contact pairs share a body with
another same-epoch pair (so the order matters for them), rising steeply with λ.

## P3: one flipped batch compounds (principle 13)
Flip the resolution order in exactly one window of a many-body gas; keep everything else
identical. Prediction: ≥ 10% of bodies' velocities diverge within O(10) windows, i.e. the
difference is not local to the flipped batch — it cascades through subsequent contacts.

## P4: premises that survive (reported as surviving, no experiment needed)
- **Two-body doll at 1PN:** ν = m₁m₂/(m₁+m₂)² ≤ 1/4 structurally, so B11's ν ≤ 0.25
  spans the whole possible range; EOB-at-1PN (ν only in the energy map) is the
  Buonanno–Damoureux result, exact at that order. Survives; the p < 20 strong-field
  window degrades but is plunge/absorption territory.
- **Past-light-cone gather uniqueness:** for any tube, d/dt[c(t_f − t) − r(t)] = −c − dr/dt
  < 0 strictly since |dr/dt| < c ⇒ exactly one crossing per tube ⇒ Newton from a stale
  seed cannot root-steal. Only convergence *speed* under hard burns is open (r6, missing).

## P5: same-key orbits freeze relative drift (bounded, not visible)
Two orbits whose (E, L) fall in one 32-bit memo key share one cycle: identical Δφ per
cycle, so their relative phase is exactly frozen while the oracle drifts by ∂Ω/∂E·ΔE_q·t.
Estimate: with ~2^16 levels per invariant across the bound range, decoherence takes
~10^5–10^7 orbits — below player visibility on any plausible timescale. Report as a
bounded risk on the memo design, not a kill.

## P6: the cost table's kick rate is a constant with no scene behind it
The 6×10⁴ tidal kicks per game-second for 10⁹ ships (§6) implies one kick per body per
~4.6 h regardless of local density. No rung measures kick *rate* against local density
(B9 measures crossings per cycle for one body; B15's Zipf fleets may contain no dense
belt). Stated as arithmetic in the dossier; no experiment.
