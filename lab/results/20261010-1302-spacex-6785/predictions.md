# Predictions (written before the decisive experiment)

The change under test: the per-event `root_state_raw` position-cache refresh in
`Universe::apply` (universe.rs:531) is deleted; the cache refreshes once per `advance`
(in `rekey`), not once per resolved item. The cache's own doc: "for deadlines only;
never an outcome". The design's promise (plane.md §7): the budget changes *when* work
is done, never *what* — outcomes are independent of schedule. This experiment tests
both that promise and the saving.

Cases I have NOT tuned on (the decisive run):

1. **P1 — digest invariance (the falsifier).** Digests at canonical cuts, identical
   before and after the patch, in three scenarios: (a) plane seed 1, Sparse, 48
   members, settle 30 G ticks; (b) plane seed 7, Dense, 200 members, settle 30 G
   ticks (held-out: different seed, order and fleet size); (c) 600 presented frames
   at rtf 100, seed 1, 48 members (the tail bench's own digest,
   `e8d0d065…`). If any digest changes, the delete is falsified — either the cache
   was an outcome in disguise, or schedule-independence is false. Both are findings;
   the run then reports which, by re-running with budget-of-one ordering on the
   patched tree.
2. **P2 — the saving.** Whole-universe µs per resolved item at settle drops by
   10–15% (root_state_raw measured 6.9 µs of 49.7 µs per item = 14%). I expect the
   low end (~10%) because `rekey` now pays O(N) refreshes per `advance` call and
   `settle` loops `advance`.
3. **P3 — frame tail (held-out).** With 200 members at rtf 100, frames above
   16.7 ms: before vs after. I predict the count does not grow (the per-frame
   rekey refresh is O(N) readouts ≈ 200 × 7 µs = 1.4 ms worst case, under budget),
   and the worst item stays the fleet open (measured 1–3 ms, once per member), not
   the kicks.
4. **P4 — the idiot index (no patch needed).** Measured kick = 35 µs: rebind
   `from_state` 12.3 µs (floor: an integer Δ(E,L) patch, no cartesian round trip —
   idiot index ≥ 100×), readout+tide+secondaries ~10 µs (physics), compile 3.4 µs,
   root_state 6.9 µs (this delete). I predict `from_state` stays the worst ratio
   after the delete, i.e. the next lever is the rebind, not the kick count.

Kill criterion for the configuration: any digest in P1 differs, or the per-item
cost grows. A KILL here kills the lazy cache only, never schedule-independence
(that would be a separate, bigger finding needing its own controls).
