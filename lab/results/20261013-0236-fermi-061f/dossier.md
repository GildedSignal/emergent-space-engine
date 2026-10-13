# Run 20261013-0236-fermi-061f — the kick's interior is not allocations

## Claim

On shipped code, a plane kick makes only **9 allocations (2,872 B)**, so memory management owns
**~0.1 µs of a 34 µs kick (0.3%)** — a zero-cost bump arena moves the kick by 0 to −4% (noise)
with bit-identical digests — and the "uncounted interior" fa08/30e1 left open is **compute: the
fit→compile→readout walk itself**, of which the cheapest unit is emulated i128 division at
**30.9 ns = 3.5× an i64 division**; ~85% of the kick ≈ ~900 i128-division-equivalents.

## Bottleneck

`kick-jet` (board live question 2: "what is the cheapest exact kick on the shipped
representation"). Open direction 1 of the page names three suspects for the compile's ~25–27 µs
uncounted interior: **allocations, key search, i128 panels**. This run deletes two of them:

- **allocations: dead.** 9/kick, priced 87.5 ns at the measured pair cost of the exact size mix
  (9.7–9.8 ns for the observed 16–512 B classes); the bump A/B confirms (delta within the
  system arm's own run-to-run spread, 34.22→32.69 µs across runs).
- **key search: absent on this path** (by reading, `bind_in` calls `Rebinding::from_state`
  directly; `Catalogue` is slot storage plus a free list — nothing is searched at bind time).

What is left is the third suspect, the panel walk's arithmetic. What this deletes from the plan:
any build that attacks the kick via allocator work (arenas, pooling, `Entry` allocation
trimming) — its ceiling on this path is ~0.3%. The lever for "cheapest exact kick" is the walk:
fewer panel evaluations per compile and fewer wide divisions per panel (the Q62 wide temporaries
are load-bearing for exactness — QUADRATURE.md — so the attack is count, not width).

## Evidence

All numbers from `cargo run --release -p emergent-universe --example kick_fermi` (~2 s; the
example, `crates/universe/examples/kick_fermi.rs`, is the whole probe — no engine file touched;
a global allocator dispatches system/counting/bump by mode, and mode 2 is entered last and never
left so no cross-mode free can occur). The path is cost_split's: clones of ship 14's record,
plan advanced to the first Kick item, one `step::process` each, n = 3000.

- Pure kick ("made"-class orbiter): **32.7–34.2 µs** (wiki: made 34–38 µs — calibration holds).
- Census (counting allocator, untimed, harness clone subtracted): **9.0 allocs/kick, 2,872 B/kick**
  (2×16 B, 1×64, 1×128, 3×256, 2×512 — the compiled trajectory's tables dominate the bytes;
  harness alone: 1 alloc, 32 B).
- Pair cost at the observed classes: **9.7–9.8 ns** (16–512 B); priced attribution
  2·9.7+9.8+9.7+3·9.7+2·9.8 ≈ **88 ns ≈ 0.3%** of the kick.
- Bump A/B (never-free 512 MB arena): **34.05 and 33.89 µs vs system 34.22 and 32.69** — the
  delta (0.16 µs, −1.2 µs) is inside the system arm's own spread; loop hash equal;
  **settle digests bit-identical** (system twice, bump once: b4f07b75…, and system repeat_equal
  true — the identity check is not vacuous).
- Bump never-free total: 9,331,410 B for 3000 kicks ≈ 3.1 KB/kick allocated (census 2,872 B +
  growth copies) — the kick's allocation traffic, ~all of it freed immediately under the system
  allocator (tcache-warm).
- Unit prices on this runner (i7-4790-class): **i128 division 30.9 ns, i64 division 8.9 ns,
  i128 multiply 1.5 ns.** Fermi close: the un-attributed ~29 µs ≈ 29,000/30.9 ≈ **~900
  i128-division-equivalents per kick** — i.e. a handful of wide divisions per one of fa08's
  ~182 panels, or the Newton readout's divisions. This last step is an estimate, not a count
  (no counters were planted in `crates/space`).

Commands: `cargo run --release -p emergent-universe --example kick_fermi` (this box, ~2 s);
`regen.sh` reruns it and stores the output. Raw output: `kick_fermi_raw.txt`.

## Predictions

`predictions.md` was written before the probe ran. What happened:

- P1 (55–110 µs) **missed low** at 32.7–34.2: I anchored on the wiki's all-class kick median
  (75.6 µs) instead of the made-class this probe exercises (wiki 34–38 µs). Calibration error,
  not a probe defect (the measured value sits in the wiki's own class band).
- P2: allocs **failed low** (9 vs 20–200); bytes **held** (2,872 in 1–20 KB).
- P3 **held**: the byte mass is in ≥256 B chunks (2,560 of 2,872 B).
- P4 **failed** (the kill): allocations own 0.3%, below the pre-registered ≥10% floor.
- P5 **held**: bump delta within ×1.5 of the attributed share (both ~0); identity held.
- P6 **triggered**: the arena/bump lever for the kick is dead; the attack moves to the walk.

## What would make it wrong

- A different kick class could allocate more: leaver kicks (`Passage::compile`, 92–102 µs) and
  word transitions were not censused. If leavers allocate ~100× more, an arena could matter
  there — but the wiki already prices leavers as compile-dominated (ec9d), so the prior is low.
- The bump A/B only proves allocation *cost* ≈ 0 on a tcache-warm single-threaded loop; under
  contention or cold caches the picture could differ — not the regime that sets the kick median.
- The ~900-divisions close is arithmetic, not measurement; a run that plants division counters
  in `Shape::integrate`/`outbound_at` could refute the unit mix (not the attribution: the
  allocation half is measured directly both ways).

Cost of adopting: none (no build proposed — a deletion of a candidate build path). Fit:
PRINCIPLES 1, "The cheapest compute is compute not done. Delete before optimizing" — this
deletes the allocator avenue; and 18/35, the right question first: the cheapest exact kick is a
panel-and-division count question, not a memory-management question.

## The lens

The Fermi lens priced everything before measuring and pre-registered the kill (P6), which fired.
What it may have missed: it measured one ship, one class, one scene (the cost_split plane, seed
1, Sparse); leavers, word transitions, fleets and 400-member scans are unmeasured here, and the
lens stopped at attribution-by-elimination — it did not count the walk's divisions, so the
"compute interior" conclusion carries an inferred unit mix. It also did not test whether the 9
allocations' *sizes* (2.9 KB) matter for the memory page's standing-representation question
(they are mostly transient, not resident).
