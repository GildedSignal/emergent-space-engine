Working...
Check complete. `lab/results/20261011-0736-components-825f/check.md` written; tree restored to clean (only untracked `lab/results/`); nothing else in the run folder touched.

**Grade: silver.**

What held under reproduction:
- **Digest triple bit-for-bit**: traced / untraced / `--engine-ms 10` all give `3db02d3d…`; m48 gives `41343a14…` matching the pre-run baseline. P6 exact.
- **The floor finding is real**: my traced m400 run gives idiot index 1.00, deferrable share 0.4%, slack median 0.0/max 0.1 frames, flattening ratio 1.00×, steady demand p99 5.9 ms vs the 5 ms budget, rtf lowest-1% = 0.0 with zero hitches above 16.7 ms — and it holds on **seed 2** (unseen). Entities 0–26 (the shipped ships included) resolve zero items. "Nothing to build in the scheduler" is earned.
- Predictions discipline was good: P4/P5/P6 held; P2/P3 failed and were reported as failed; file times confirm `predictions.md` preceded the traced runs (07:52:02 vs first traced run starting 07:52:07).

What caps it at silver — my probe (scratch instrumentation of the player's item, reconciling with the traced totals to 1–2%):
- The claim's mechanism is **wrong**: members never enter `sources[d]` (only `make_source` ever pushes, once, for the Moon; `resolve_handout` makes members with `gm = 0`). The motion-law step is **flat** in members: 41.7 → 40.0 µs/item from 48 → 400 members. The O(members) term is `PlayerNeighbourhood::find` (encounter.rs:53), an O(all-bodies) scan per player item: 238 → 1463 µs/item, 85% of the item at m400, still linear at 3838 bodies.
- So the proposed adoption (doll-aggregate moment source) would change nothing; the correct lever is the encounter seam the repo already names (Binet cone) plus the battle slice (that second lever is correctly identified).
- "One player step is hours at 10⁶ members" is off by ~3 orders of magnitude (~3–4 s by both the author's slope and my probe).

One experiment to gold: fold the item decomposition into the claim and re-derive the levers from it.
