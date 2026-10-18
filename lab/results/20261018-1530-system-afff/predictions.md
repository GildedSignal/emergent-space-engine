# Predictions (written before the decisive flights)

Question: the player-neighbourhood scan walks every candidate binding in the
player's doll (the frame wall at 5×10⁴, nladder 96f6), pins one 192-B `Binding`
clone per candidate (the memory pin, b77d/1fcf), and re-compares the whole list
per scan (the compare-form, 19.2 ns/member). Is that walk a no-surprise machine
whose non-empty answers are phase-local, so that a rank-k along-track read
replaces the walk, the pin and the compare at once?

Cases not tuned on (the shipped scene, first flights of this build):

- P1 (no surprise): ≥ 90% of scans answer empty on the shipped fleet scene
  (48 members + locals, coast). If most scans return encounters, the walk is
  earning its cost and the certificate deletes nothing.
- P2 (phase locality, taleb-09b5's rank-4 transferred with margin): every
  encounter the scan finds is within along-track rank ≤ 8 among the candidates
  it walked. A hit at rank ≫ 8 kills the phase certificate for the scan (it
  must then walk).
- P3 (the filter is dead at the crowd): the radial apsidal filter keeps nothing
  — candidate count ≈ the doll's alive population (the bail of 96f6's census,
  87/87) — so the walk is the whole cost, K-proportional.
- P4 (belt irrelevance): adding the 2–3 AU belt (N = 20,000) leaves the scan's
  candidate count unchanged (the belt is not in the player's doll), so the
  ladder's frame wall at 5×10⁴ is a same-doll crowd property, not a belt
  property.

Kill criterion for the unification: P1 or P2 failing means the walk carries
real, non-local surprise and stays; the dossier then reports which and where.
