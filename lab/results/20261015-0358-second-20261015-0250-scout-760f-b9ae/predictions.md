# Predictions (written before the decisive runs)

The second checker's named gold experiment: fly the lazy variant — demote-after-kick wired into
the kick settle, `decode`-side promotion on touch (key carried in the compact record, `Arc`
re-minted by `Orbit::compile`), digest-vs-baseline across at least one full wave. Built as an
additive seam (`EntrySlot::Live/Demoted`), off by default; the census's bit-identity proof stands
behind it. Baselines are the recorded digests of 20261015-0250-scout-760f (regenerated first).

1. **Seam neutrality (the control).** With `lazy_demote = false`, the patched build reproduces
   every baseline digest bit-for-bit (10⁵ coast `2109a2e0…`, 10⁴ coast `f8b52855…`, 10⁴ burn
   `44d6a9b5…`). Any difference kills the patch as an instrument before anything else runs.
2. **Flown identity (the certificate).** With `lazy_demote = true`, digest equals baseline at
   every arm: 10⁴ and 10⁵, coast and burn, seed 1 and held-out seed 7, past the first kick wave
   (~14 k game-s) to 48 k game-s. The digest hashes keys and binding fields, not trajectory
   content, so identity here means the *dynamics* never diverged: every kick after a promotion
   read a bit-identical recompiled state and minted the same next key. A single mismatch refutes
   the lazy variant as flown (the entry would be state, not cache).
3. **The identity path.** `same()` in encounter.rs compares entries by `Arc::ptr_eq`; a promoted
   entry has a fresh address, so held scans recompute instead of hitting the memo. Prediction:
   outcomes identical (covered by 2) and the recompute is visible only as wall time.
4. **The bill.** Promotions minted over the flight are of the order of demotions times reads per
   demoted binding; at the census's 4.6 µs p50 I predict the lazy arms run ≤ 1.5× the baseline
   wall (the belt's kicks are 5.7×10⁻⁵/body/game-s at 10⁵, and each resolve of a demoted body
   pays one compile). If the lazy arm needs > 3× baseline wall, promotion binds before memory
   does at this scene.
5. **Standing memory.** At the cut, ≥ 70% of standing Cycle bindings are Demoted (the first wave
   kicked most bodies once), and rss_end drops by roughly the standing knots' share (the census's
   13.7% of the 4.89 kB/body plateau, plus the catalogue slots): predict 489 MB → 400–440 MB at
   10⁵. If rss does not drop, demote-after-kick is outcome-free but not memory-free on this
   scene, and the flown build says so.
