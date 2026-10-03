# Dossier — 20261003-1030-autoresearch-dcec

**Claim.** The CPU chronon reference in `crates/lattice` runs 5.3× faster per
body-chronon (486 → 92.5 ns at n=100k standard gas; 2.1–4.8× across held-out regimes)
with bit-identical outcomes, by deleting the per-chronon hash structures — the grid is
a counting sort over a ghost-padded linearized cell index with reused scratch — plus a
cheaper consumed-contact hash and a single visit per cell pair.

**Bottleneck.** Board #3, cost at a billion (ns per event / per body-chronon), for the
reference mode every other mode is checked against (`docs/engine.md` contract). The
baseline spent 78% of each chronon in detection, and 34 ms of a 46 ms chronon was
building a fresh `HashMap` of cell ranges (100k SipHash inserts, ~2.5 MB, every
chronon) — allocation and hashing, not physics. Deleting it removes a whole component
(the per-chronon hash map) from the hot path; the same representation also drops the
per-chronon sort, so the reference's detection is now a linear pass.

**Evidence.** Machine: cloud container, 2 vCPU EPYC, load 0.3–1.9 recorded, shared
with sibling runs (orders of magnitude only; the integrator re-measures on the M1).
Reproduce: `cargo build --release -p emergent-lattice --example lab_bench` with
`lab_bench.rs` from this folder copied to `crates/lattice/examples/`, then
`./target/release/examples/lab_bench <n> <fill> <q> <vmax> <seed> <steps>`; digests and
counters print with the timing. Files: `log.md` (per-round table),
`baseline-heldout.txt`, `heldout-final.txt`, `heldout-final2.txt`, `predictions.md`.
- Tuning config (100000 0.1 1024 256 1 100): 486 → 92.5 ns/body-chronon (median),
  world digest `9c7790dc…`, log digest `b6dd6f65…`, predicates 23,458,426 and fired
  231,896 — identical to baseline at every kept round.
- Held-out (final run): standard 4.7×, dense (fill 0.4) 2.1×, cold-sparse (zero events,
  span 7.5M cells) 3.5×, hot (q 4096, vmax 1024) 4.8×, tiny (n=1000) 3.0× — world and
  log digests identical on all five.
- Guards: 19/19 `cargo test -p emergent-lattice`; 10/10 `emergent-lattice-event`
  (cross-mode digest equality); `xtask lattice-check` EQUAL on 64:1024, 256:512,
  64:8192 (events, finals, wall momentum vs the independent integer reference), and
  its chronon side fell from 39.2 ms to 3.8 ms on case 1.
- Round gains: R1 counting-sort table 3.4×; R2 FxHash consumed map 7%; R3 single visit
  per cell pair 18%; R4 key reuse + occupied walk 11%; R5 ghost-ring padding 2.5%;
  R6 no clone 3%. Each ≤ 60 s to measure.

**Predictions.** `predictions.md` was written before the loop. Held: digests identical
everywhere (the hard constraint); standard ≥ 2.5× (got 5.3×); dense ≥ 1.5× (2.1×); hot
≥ 2× (4.8×); tiny 1.2–2× (3.0×, better than predicted); the single biggest idea is
deleting per-chronon hash structures (confirmed: R1 alone was 3.4×). **Failed:** the
ranking prediction cold-sparse > standard, and cold-sparse ≥ 3× — the first held-out
run regressed to 0.84× because the cell span (7.5M) exceeded the table cap and fell
back to the hashed path, now carrying an extra key pass. Fixed on a proxy config
(seed 23, not the held-out case) by capping at the measured break-even span ≤ 64n
(hard cap 2²⁴); the proxy went 327 → 93 ns with identical digests, and the re-run
held-out reached 3.5×. Both held-out runs are reported above; the second contains one
post-miss fix.

**What would make it wrong.** A world where outcomes depend on detection order through
something other than the sorted `pairs` list (then the counting-sort permutation could
change bits — the guard is digest equality, and it held everywhere tested, but exotic
worlds with bodies outside any container or spans beyond 2²⁴·cells use the retained
hashed fallback, which is now the slower path and unmeasured at scale). The span ≤ 64n
break-even was measured on two sparse configs; a world with extreme aspect ratio
(one very long axis) could sit past break-even while under the cap. Adoption cost:
one file, `crates/lattice/src/chronon.rs`, +198/−31, no API change, no new
dependencies, scratch is ~span×4 bytes transient (64 MiB worst case at the hard cap);
every other mode is untouched because they share the law, not the stepper. Fit:
"the cheapest compute is compute not done" (P1) — the deleted work was pure scaffolding;
"local laws are great because parallelizable and simple" (P15) — the cell table is the
same locality, held flat; "discrete by design, cheapest arithmetic" (P16) — indices,
shifts and counts, no floats introduced; canonical outcomes stay "independent of …
schedule" (Truth) because the pair set, not the walk order, decides the bits.

**The lens.** Autoresearch on one working artifact optimizes what is measured and can
miss that this reference is scaffolding itself: the plane's live engine (`xtask
universe`) may never call `Chronon::step` at scale, in which case the 5.3× speeds only
tests and judges — still worth having (the judge and `lattice-check` run this path),
but the board's billion-body cost lives in the event and Metal modes, which need their
own measurement. The structural change that beats this best config: carry cell
occupancy across chronons (bodies move ≤ 1 cell per chronon by construction of `cell`),
deleting the keying and counting passes entirely — predicted another ~1.5–2× in
`predictions.md` #5 and untouched here; second, an exact i64 fast path inside
`law::hit`'s early-out branches (~8–12%) belongs to the law, not this stepper, and
should be its own judged change.
