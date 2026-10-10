# Dossier — 20261010-1920-spacex-cb3f (SpaceX lens)

**Claim.** On the plane as it flies today, the per-event cost is ~50 µs of which the physics that
must happen is ~3.6 µs (idiot index ≈ 13×): the player's exact encounter scan is 32% of the whole
settle with a measured O(N) slope of ≈ 33 ns per body per player item (33 ms/item at 10⁶ bodies —
the Binet cone seam is load-bearing), per-kick source-state memoisation is sound but deletes < 5%
(a source's tube decode is ~0.1 µs, not the µs I assumed), and the ship-side residue is the
per-kick rebind/recompile (~16 µs) plus root_state (~7 µs/event) — confirming, with numbers on the
whole universe, that cadence-and-recompile, not shared-state reads, is the lever.

**Bottleneck.** Board line 1 (fewer/cheaper kicks: "kicks dominate the engine's cost") and the top
scaling risk (candidate work vs real encounters). Expected gain from the memo: 10× (wrong, see
below); actual measured gain from deleting scan-redundancy at game scale: unbounded (the scan is
the only per-event term that grows with N).

**Evidence** (Linux x86, shared runner, orders of magnitude only; `target` at
`/home/glmlab/lab-target-3`, built `cargo build --release -p emergent-universe --examples`):

    export T=/home/glmlab/lab-target-3/release/examples/spacex_probe
    ESPACEX_NOCACHE=1 $T 200 7 30000000000 1   # memo off
    $T 200 7 30000000000 1                     # memo on
    $T 0 7 30000000000 1                       # plain plane
    $T 200 7 30000000000 4                     # threads 4
    $T 2000 7 30000000000 1                    # N ≈ 2028
    ESPACEX_NOSCAN=1 $T 200 7 30000000000 1    # timing-only scan bound
    /home/glmlab/lab-target-3/release/examples/cost_split

1. **Bit identity (P1 ✓ 6/6).** Digests identical memo on/off: seed 7 cohort 200
   (`d4413b80…`), cohort 0 (`74a3a79f…`), cohort 2000 (`b1dcf925…`); threads 4 = threads 1
   (`d4413b80…`, P6 ✓). Event counters identical in every pair.
2. **The memo is not the lever.** Hit rate 55–57% (cohort 0 and 200), 43% (cohort 2000), but
   whole-settle speedup 1.04× (2.66→2.55 s), 1.02× (plain plane). `cost_split`: a source's
   state decode is 0.10 µs (moon), tide 0.07 µs — 74k calls ≈ 7 ms of a 2.5 s settle. My
   premise (µs-scale Kepler decodes) was wrong; decodes are already ~100 ns.
3. **Decomposition of the settle** (seed 7, cohort 200, threads 1, 3×10¹⁰ ticks, 51 819 events,
   2.55 s): player 14 305 items × 142 µs = 80% of wall; ships 17 083 × 29 µs = 20%; planets, moon,
   fleet noise. Inside the player's item: scan 57 µs, process ≈ 85 µs. Inside a ship's item
   (`cost_split`): own readout 3.4 µs, root_state 7.0 µs, secondaries+tide 0.17 µs — the ~16 µs
   residue is the rebind (a tube recompile per kick) and interval planning.
4. **The scan's shape** (P4 half-wrong, honestly): share 29–36% (I predicted 60–85% — miss).
   Per-item scan cost: 57.5 µs at N≈228, 116.7 µs at N≈2028 → slope ≈ 33 ns/body/item, intercept
   ≈ 50 µs (the ~12 same-doll exact pair checks at ~4 µs each — a cartesian decode + i128 lattice
   predicate per pair, per player item). `ESPACEX_NOSCAN` bounds it: settle 2.55→1.73 s (P5 said
   15–35% would remain; actual 68% — miss).
5. **Threads 4 is slower** (3.24 s vs 2.55 s) on this shared box at this size — wave parallelism
   does not pay at N≈230; same digest.

**Predictions** ([predictions.md](predictions.md)): P1 ✓ 6/6, P6 ✓; P2 hit-rate ✓ but speedup 1.04×
(just under the 1.05 floor); P3 ✗ (hit 57% vs ≤45% predicted — the plain plane shares source reads
more than I guessed); P4 ✗/✓ (share 32% not 60–85%; the O(N) form confirmed, my coefficient was
wrong because the same-doll checks, not the clones, dominate); P5 ✗ (68% remains, not ≤35%).

**What would make it wrong.** The 33 ns/body slope and the 4 µs/pair check are Linux/x86 shared-box
numbers; the M1 may differ by 2×, not in shape. The decomposition could shift at real game scale
(belt in `shipmem`, encounters at N=10⁶), where the scan's O(N) term and the recompile both grow
into the wall. The memo's soundness argument (a source's state at t is final before the first
reader) held everywhere tested, but a schedule that reads a source mid-pull would break it — the
digest check is the guard.

**Cost of adopting.** The memo patch is ~60 lines (ctx.rs/universe.rs), digest-neutral, and buys
< 5%: by this run's own evidence, **do not adopt it** — delete the idea, keep the measurement. The
adoptable outputs are numbers, not code: (a) the scan slope makes the co-orbital/Binet-cone seam
the plane's scaling wall (33 ms per player item at 10⁶ bodies, 14k items per 3×10¹⁰ ticks);
(b) the same-doll pair check at ~4 µs/pair is the scan's real body — a provably-safe rejection
pre-filter (rough-first, exact on the borderline, P21) is the next cheapest falsifying probe;
(c) root_state at 7 µs/event is 15% of a ship's item and was not on the board's ledger.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" (P1) — measured, and the
candidate deletions ranked by evidence; "Measure before claiming" (P10) — two of my own
predictions failed and are reported as failed; "Compute only surprises" (P3) — the scan is pure
derivation per event, exactly the category to delete.

**The lens.** SpaceX's delete-first pushed me to memoise before measuring the floor; the floor
(0.1 µs decodes) had already been paid. The idiot-index table, not the patch, is the product. I may
have missed what the player's 85 µs process() residue means for the motion-law v2 (Opus's module —
out of my authority).
