# Predictions — 20261020-0229-inversion-4f1f (written before the decisive arms)

Scene: shipped `nladder` burn, N=10⁵ (and 2×10⁵ spot arms), seed 1, rtf 1000, cut 17,000 game-s,
threads 1, the shipped canonical-cut contract (`frame_to(limit=cut)` + `settle(cut)` + digest).
Instrument: 4063's `cut_digest` verbatim + `ES_DECIDE=frame` (nladder's own decision recipe:
`input(now)` at frame 60, tick 199,980 — 20 ticks before the canonical 200,000). Gates from the
record: `ES_ROOT_SHIPS_TO_QUEUE` (1d47's all-to-queue), `ES_FIX_PROBE`, `ES_DUMP_ENC`.
Smoke (already run, 1 each): OFF-canonical 581ced1a/127,671/1,802 (4063's digit exact); ON-canonical
= 581ced1a (stale 4,905, stale_enc 0); OFF-frame 0b9930b6/127,663/1,792; ON-frame = 0b9930b6
(stale 5,139, stale_enc 0) — the decision tick shifts the digest deterministically; neither cell
has yet shown a rerun flip.

The dispute being adjudicated: 1d47's checker (loaded box, frame-anchored decision) found the ON
gate **bistable across reruns of the same arm** (10⁵: ad732607 ×3 vs 75543d72 ×1; 2×10⁵:
bde05587 ×2 vs 61a8a10d ×1, kicks −11). 4063 (quiet sequential box, canonical decision) found
0 flips in 34 runs. Statistically incompatible (2/8 vs 0/34); the record blames "the decision's
landing tick, its box's load, its fixed-1080-frame loop". I test the two live axes directly:
decision placement (canon vs frame) × box load (quiet vs 6 CPU spinners, 2 of 8 cores left).

- **P1 (4063 reproduces, quiet):** canon-ON 12 ms ×4 → four identical digests = 581ced1a.
  Falsifier: any rerun diverges.
- **P2 (the load axis — the headline):** canon-ON loaded ×8 → at least one digest ≠ 581ced1a.
  The mechanism: the per-frame wall budget `until` bites at load-dependent points, so which due
  ships the frame defers varies run to run, so the player's scan reads stale extrapolations whose
  answers occasionally flip (1d47-checker saw ±5 encounters, once −11 kicks). Falsifier: 8 identical.
- **P3 (the control side):** canon-OFF loaded ×3 → identical (581ced1a); no deferral, no stale
  reads, so load cannot touch the digest. Falsifier: a flip in OFF under load alone (that would
  indict the shipped engine, not the gate).
- **P4 (the decision axis, quiet):** frame-ON 12 ms ×4 → identical (0b9930b6): the 20-tick shift
  moves the whole trajectory but does not by itself destabilize reruns. Falsifier: a divergent rerun.
- **P5 (composition):** frame-ON loaded ×6 → flips at least as often as P2 (the frame-anchored
  scene's conjunction set sits elsewhere; if 1d47-checker's flip needed both axes, only this cell
  diverges).
- **P6 (the channel):** every divergent digest pair differs in the printed encounters count or the
  dumped encounter log (stale-answered encounters are the channel; kicks move only if an
  encounter's consequence chains, as in 1d47-checker's −11).

Kill criterion for the whole "contract dies under load" reading: all ~25 same-arm reruns identical
(including loaded) → the bistability does not reproduce under either axis on a controlled box;
report the invariance strengthened and 1d47-checker's flip unexplained by these two axes.
