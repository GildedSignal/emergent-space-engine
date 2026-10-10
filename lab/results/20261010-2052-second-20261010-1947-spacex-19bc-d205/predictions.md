# Predictions — second author on 20261010-1947-spacex-19bc (d205)

Written before the decisive runs. The checker's named experiment for gold: measure the
**removal side** — an actual packed-block reabsorption (shipmem-style) fed by the plane's real
rebind stream, reporting bytes removed per game-second next to bits created, so the 2 % duty
becomes a measurement instead of a model (one 72 µs kick-resolver rebind ≡ one recompile).

Setup: `--hlive` now drives two real `shipmem::shelf::Shelf` stores (exact 5-column and coarse
3-column, blocks of 128, chord on, sorted by rebind time) with the plane's live rebind stream:
every rebind (any cause) updates the ship's slot; every 120 frames (idle time) `compact()` runs
(seals scars, repacks groups whose scars outgrow a quarter of their blocks) and is timed.

- **P1 (the duty).** Measured reabsorption duty at the coarse level, scaled to 10⁹ ships,
  lands within 3× of the modelled ~1.7 % of a core (so ≤ ~5 %): the kick resolver does strictly
  more work per rebind (drift readout, forces, fitting, remainder) than a scar seal plus an
  amortized repack. **Kill:** measured coarse duty > 0.2 cores of one core-equivalent (the
  checker's 10× margin: then the 8 GB verdict's margin is broken, not closed).
- **P2 (removal tracks creation).** At the coarse level, time-averaged bytes removed per
  game-second is within a factor 2 of the bits created per game-second measured in the same run
  (steady state: what creation adds, reabsorption removes). If removal ≪ creation and the store
  grows monotonically, the premise's mechanism fails on the plane's own scene.
- **P3 (exact side dies by bandwidth, not CPU).** The exact shelf's measured duty is within 3×
  of the coarse shelf's (same machinery, 5 vs 3 columns); the exact side's death sentence stays
  a bandwidth verdict (tens of GB/h), not a duty verdict.
- **P4 (boundedness).** With the fixed 120-frame compact cadence, shelf bytes per member stay
  within 2× of the initial packed size for the whole run (no monotone growth).
- **P5 (density).** With `--members 400` (~423 ships, the checker's adversarial case), per-ship
  duty is within 2× of the 48-member scene (compact is per-group local; the field is aggregated).

Held-out honesty note: the µs numbers are shared-runner Linux x86 (orders of magnitude only);
byte counts, digests and integers are deterministic and must reproduce bit-for-bit.
