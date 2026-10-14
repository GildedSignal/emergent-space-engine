Working...
All deliverables are in place: `dossier.md`, pre-registered `predictions.md`, `regen.sh` (four flights, ~2 min total wall), `work/patch.diff` (engine cap + bench), `out/flights.txt` (raw numbers), and the proposed `wiki/nladder.md` with both merge conflicts resolved and this result folded in.

**Claim:** with the player's pull capped, a player decision landing mid-wave costs O(1), not O(backlog) — 0.168 ms for one, ≤ 0.229 ms even every frame through the whole wave (max frame 12.5 ms against the uncapped 1,487 ms, digests bit-identical, kicks equal) — so the checker-named input exposure is bounded by the same cap and needs no deferral machinery, with one held-out margin: 657 no-op decisions add exactly one encounter to the log, so "same keys" is not "no event."
