Working...
Check complete. **Grade: gold** — written to `check2.md`, page corrected in place.

**What I did (independent, blind to check.md):**

- **Reproduction** in a clean tree with the author's patch: every dossier number. Baseline 1,346 ms / 9 over vs capped 11.97 ms / 0 over; digest `ba1a66b4…`, encounters 4,060, kicks 225,975 all equal; wave_train's train recurrence exact (second items 26,101–29,084, gap census = first wave's shape, steps a continuum).
- **Five adversarial cases:** pristine `universe.rs` (same digest → default-neutrality proven, not argued); seed 3 (1,257→11.96 ms, digest equal); **4×10⁵** (3,901 ms / 65,556-event monsters → 11.97 ms, digest equal, 1.86 GB RSS — the box ceiling); coast (digest equal); cap 0/1 (both hold 12 ms, same digest — the cap value doesn't matter on a quiet box).
- **Code adjudication:** the scan reads `binding_at(j, t)` for same-doll candidates; key order makes bindings at t final before the player's item pops — neutrality is *law* on the queue path. The one hole is `input` (`universe.rs:1182`), which resolves the player's item over an overdue backlog outside key order: the real untested exposure, which the author's "what would make it wrong" misses.
- **Page corrections:** the first checker's "non-monotone caps / 734 ms at cap 0" is not reproducible without box contention (333 events ≈ 16 ms of work — nothing to bill 734 ms to); flagged as schedule noise, and added the input-path hole plus the settle scaling (11 s at 4×10⁵: the drain, not the frame, scales with N).

Gold because: reproduced twice (runner + me), pre-registered predictions with honestly-reported failures that became the run's correction, 114×–326× on the board's #1 bottleneck, adoptable in one step (9 lines + comment rewrite — the patch's comments describe a deferral that isn't in the code and must be rewritten at adoption).
