# Predictions (written before the decisive arms; smoke-run only at N=3000, 8 s)

Scene: `wave_band` (frame_cost's loop verbatim: frames of 1/60 s at rtf 100, a 12 ms wall budget, keys held from
frame 60), N = 10⁵ seed 1 (wave window measured: belt first items 13,051–14,542 game-s = wall 130.5–145.4 s; flights
160 s). Controls are the at-Home placements the record already flew (6138, bf21).

- **P1 home + L8 burn (control, known answer):** monsters inside the wave, worst frame 10²–10³ ms on this box,
  spaced ~50 frames (the player's item cadence), the player's item µs dominating; kicks ≈ the belt's size.
- **P2 home + coast (control, known answer):** max ≈ 12 ms, 0 frames over, the wave absorbed as lag (6138's coast).
- **P3 band + coast (untested seam):** the player is a root-doll body, so its item cadence is the belt's own
  (~2.8×10⁴ s); its FIRST item lands inside the wave, and `pull_ships(key, !in_root=false)` sweeps the belt's whole
  overdue backlog inside that one item. I expect one or a few monster frames (order 10²–10³ ms) UNDER COAST — a frame
  the home coast arm never has — then quiet.
- **P4 band + L8 burn:** the same pull at every player item through the wave (re-planning shortens the cadence), so
  monsters at least as bad as P1's, plus the scan term (ENCOUNTERS stage, root index with 10⁵ registered hulls
  widening as kicks land): I predict ENCOUNTERS becomes visible (≥ 10% of the worst frames' player-item cost) and the
  encounter count exceeds the home arm's (dense neighbourhood).
- **P5 schedule (the certificate):** band + burn flown unlimited vs 12 ms budget: one digest, equal counters — the
  seam is a cost, never a law.

Kill criteria (written before the run): if the band arms' max/p99 sit within ~2× of the home arms' and P3's coast
monster does not appear, the named exposure is measured shut ("no new term"), and that is the dossier's claim. If the
band arms break by ≥ 10× at p99 or max, the seam is a standing fragility and the dossier prices the fix in the
engine's own idiom (bf21's pull cap; holding the scan off the critical path).

Held out for the checker: seed 2 band burn; the player's radius/doll placement sensitivity (angle 0x2000_0000 fixed).
