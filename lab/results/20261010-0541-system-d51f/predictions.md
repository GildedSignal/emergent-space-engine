# Predictions (written before the decisive run)

Question: is light-arrival bookkeeping (scheduler deadlines, view gather, and the coming news
gravity) recomputing the same doll-chain readouts, and is the shared part memoizable without
changing one bit?

Cases I have NOT tuned on (the plane's own scene, seed 7, rtf 100, 300 frames; and the stream
scene as a control):

1. **Redundancy, plane scene.** Bodies sharing a doll (ships, moon, fleet members about Home)
   re-derive the doll centre's readout at the same tick. Predicted: within one gather, memo hits
   ≥ misses for the *centre levels* (i.e. > 50% of chain levels above the emitter's own level are
   duplicates). Overall hit fraction of all levels (emitter levels included): 25–60%.
2. **Control, stream scene** (every emitter a bare tube in the root doll, depth 1): hit fraction
   ≈ 0 (< 5%). If the memo "wins" there too, the measurement is an artifact.
3. **Bit identity.** With the memo on, every frame's gathered `Seen` (all f64 fields, same order)
   hashes identically to the memo-off run, and the universe digest at the same cut is identical.
   If not, the memo changes behaviour and is dead (principle 13: no error introduced).
4. **Gather wall.** The memo cuts the gather's chain cost by roughly the duplicated fraction;
   predicted median gather-wall drop 10–40% on the plane scene (its chains are depth 2–3 and the
   emitter's own readout — Newton inside a panel — is untouched). If the drop is < 5%, the claim
   of a live saving on today's scene is wrong; only the scaling argument survives.
5. **Scheduler tax.** `Universe::apply` pays one `root_state_raw` (a doll-chain walk) per resolved
   event for the deadline. Predicted: ≥ 1 call per kick, and its measured share of the ship-kick
   path is 1–15% (not dominant today; a per-event tax that grows with N and with news gravity).
6. **News-gravity multiplier (derived, not run).** A naive news gravity (Newton × 2–3 readouts per
   source per kick, each a depth-2 walk) multiplies the per-kick readout cost by ~4–9 over a
   shared-arrival-map version (1 walk amortized per (source, tick), reused by every kicked body of
   the doll in the same kick epoch). This is arithmetic from measured readout costs, labelled as
   such.
