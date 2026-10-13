# Smooth flight (gate F1): what landed, what did not, and what would (13 October, Sonnet, wt/frame)

Landed, every digest bit for bit (8 scripted flights x 4 schedules, plus 16 more flights against the original finder; `digests_before_main.txt`; `tests/frame_loop.rs`):
- The player's neighbourhood scan (150-280 us a player item, 48% of the mean frame at reverse L15) is taken cheaply on the critical path and answered in idle
  time, in order (`encounter.rs` capture/Held; `Universe::drain_scans`; `digest()` counts what is held). A scan after a boundary/opening is the scan before it
  again and is answered once. At the held-scan cap the next item waits for the oldest scan inside the budget (a frame never overruns).
- `apply` no longer walks the doll chain for the player (its light distance is zero; the cache was never read). `next_impact` is read once per binding.
- Not landed, measured: lazy re-keying 8-11 us/frame at 28 bodies (0.1% of the budget), the incremental deadline 5-8 us/frame after the player's walk went; the lab's
  lazy tier fails the starvation gate (wiki frame-cost), so it waits for a population where rekey matters (~10^4 bodies).

Why F1 stays red at forward L9+ / reverse L7+ (`f1_clean_ab.txt`): the mandatory chain is one exact fit per kick (a Passage compile, 85-160 us) and a burn at level L
asks for 40 (L8) to 520 (L15) kicks in the first frame (demand mode: 3,109 events, 170 ms at L15). Deleting every other cost cannot reach 12 ms. The opening exodus
(48 hand-outs at game time ~100 s = frame 61 of every flight, which is also where the sweep's burns start) is itself 10 ms of the 12.

Findings for the owners (none is mine to edit):
1. LAW (hit): `lattice::law::hit` wraps its i128 products when |d||w| > 2^63 in its units: 16-52% of the pairs a burn tests (`examples/hit_wrap.rs`). Every "contact"
   in the digest today is such garbage (46/5/7/4 in four flights), as are 5-54 hashed encounters. Fixing it (checked/i256) changes digests; it would also let a cheap exact
   filter skip 70-86% of the pairs (commit ce694696 holds that filter and its control; with the wrap kept it skips 0-10%).
2. SPACE (Astra): `Passage::compile` cuts 16 bands per octave out to the outer radius (144 bands from a 7,000 km periapsis to 4 SOI) whatever is read; 63% of the mandatory
   path of a burn is `OrbitShape::append`. Extending the table lazily (the sums are cumulative in band order, so the bits are the same) deletes most of it. This is the
   one change that could bring L10+ near 12 ms without a law change.
3. SPACE: `bind_surface` compiles a hand-out twice (the first word is too small for a passage out to 4 SOI: 4 of the exodus's 9 ms). The key (`fit_key`, cheap) is all the
   word needs: expose it, choose the word first, bind once; the result is the same bits.
4. LAW (cadence): the burst is the thrust step (1/64 of |v| a kick, `THRUST_FRACTION_LOG2`), not the field: tide/burn is 1e-10..1e-12 (wiki frame-cost, direction 2). Carrying the held
   burn in the tube's generator (events only when the tide's carry crosses a quantum or the keys change) deletes the waterfall; it changes digests.
5. `next_impact` (retro burns are impact courses) is ~30 readouts of bisection a binding; a verified bracket from the tube's inverse would cut it 10x but is exact only where the
   radius is monotone (not at a grazing periapsis): the owner decides.
