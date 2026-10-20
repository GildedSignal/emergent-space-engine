# Predictions (written before the decisive runs)

Instrument: print-only census (`ES_MINT_CENSUS=1`), counters are relaxed atomics beside the
same paths; the shipped digest path is untouched. Scenes: the standing belt flights
`nladder 10000 coast 150 1800` and `nladder 30000 coast 150 1800` (9edc's scenes).

The hypothesis under test: **the plane's two worst scoreboard gaps are one object — the
per-kick minted knot table.** The kick pays to compile it (time gap, 75-160 µs vs ~50 ns
floor) and the store pays to retain it (memory gap, ~2.4-5.1 kB/body vs ~6 B floor). The
census asks who besides the mint itself ever walks a knot table, and who ever reads a
retired one.

- **P1 (compile is the kick's core):** `MINT_NS / REBIND_NS ≥ 0.5` and
  `REBIND_NS / KICK_NS ≥ 0.5` on the belt flight (the compile dominates the fit, the fit
  dominates the kick). Domain: cycle-dominated belt; passages/plunges rare.
- **P2 (the mint is a one/few-reader cache):** external reads per mint
  `(READS_STATE + READS_RADIUS) / MINTS ∈ [1.0, 4.0]`. Below 1.0 would mean many mints are
  never read at all (pure waste); above ~4 would mean the table is a genuine shared cache.
- **P3 (nobody reads the past):** history reads answered by a retired segment
  `HIST_HIT / MINTS < 0.05` on the coasting belt — the view clamps to the current binding
  (`view.rs`: `t_read.max(event_time)`), so retention serves no measured reader per mint.
- **P4 (the mint's own reads):** `MINT_OWN / MINTS ∈ [2, 5]` (fit offset `at_radius`,
  residual decode, plan reads at mint time).
- **P5 (mints ≈ fired kicks):** `MINTS` within 20% of fired kicks plus births (every fired
  kick rebinds once; carries and sub-quantum kicks mint nothing; handoffs add a few).

**Kill criteria for the hypothesis (not the method):**
- If P2 lands ≥ 10 (the table has many readers), the "one-reader cache" claim dies: the
  store is a working cache and only the history term (P3) stands.
- If P1 lands ≤ 0.2, the compile is not the kick's core and the two gaps are only weakly
  one object (the unification claim dies, the memory claim stands alone).
- If P3 lands ≥ 0.5 per mint, history retention is load-bearing on the belt and the
  deletion claim dies there.

What I expect the numbers to imply (composition, checked after): with P2 ≈ 1-3 and P3 ≈ 0,
deleting the *retention* (prune to the last segment) is free of readers on these scenes,
and the knot table's per-body *store* is consumed ~once per mint — so the memory gap and
the kick gap share one object, but their fates differ: the store is deletable (keep the
16-byte tube, recompile at read), the compile is not (each read needs a walked table;
deferral would multiply compiles by reads/mint).
