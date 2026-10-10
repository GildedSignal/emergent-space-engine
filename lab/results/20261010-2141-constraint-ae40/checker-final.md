Working...
Check complete — `check.md` written with `Grade: silver` (abstract 113 words), nothing else in the run folder touched, no git operations.

**Verdict: silver**, on four legs:

**Reproduced.** `patch.diff` is empty, so the runs measure main as-is. Both key configs re-run: digests bit-for-bit (`41343a…728b2`, `3db02d3d…ca2ce`); gather shares 0.680/0.603 vs stored 0.697/0.640; player per-item max by 4.3×–28×, monotone across members. A bonus the author under-sells: my m400 run resolved 8802 kicks vs the stored 8383 under different load, same digest — an independent confirmation of the canonical-cut contract. Code attribution reads true: `PlayerNeighbourhood::find` scans all bodies per player event (`binding_at` before the doll filter), and `Budget::spent` is inter-item only (universe.rs:811).

**Predictions honestly held out** (file times 21:44:24, between baseline and sweeps), but 2 of 5 materially wrong — engine p50 ×10 at rtf 1000 (stayed 0.28 ms) and the tail mechanism (player-shaped, not cadence-shaped); both disclosed.

**Adversarial finds.** `--members 800` saturates at 428 bodies, identical digest to m400 — the scaling axis is capped at three points, unmentioned in the dossier; one 17.8 ms hitch appeared at effective m400 (zero-hitches is edge-adjacent); rtf 30000 errors ("player is lost") — the sweep quietly ends at the scene's limit; rtf 20000 and seed 2 hold every claim.

**Why not gold.** The view-bound fact is H0210's recorded limitation ("the view gather is 83% of a light frame"), presented here as discovery; the one genuinely new mechanism (player-event tail = O(doll) scan) is code-read plus curve, never instrumented, with absolute µs swinging ~2× with machine state. Gold experiment: profile one player event's scan share on a scene exceeding 428 live bodies. Cost to adopt stays zero — it ranks the already-queued readout and encounter builds over kick cadence.
