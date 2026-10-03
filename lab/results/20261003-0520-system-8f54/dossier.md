# Dossier — run 20261003-0520-system-8f54 (lens: the whole system)

## Claim

The plane's kick layer still speaks Cartesian: every firing kick re-fits the invariants and re-compiles a whole geodesic (`Rebinding::from_state`) even though 98.7% of those rebinds land in the same memo cell and 88% hit the shape memo that already exists unwired in `crates/space` — the rebind translator is a component that exists only to repair the mismatch between the Cartesian kick layer and the invariant tube representation the design specifies.

## Bottleneck

Board focus 1: "fewer kicks per orbit at the same behaviour … kicks dominate the engine's cost". Same numbers, other half: cost **per kick**. The measured 29 µs kick carries ~10.5 µs of fit+compile and ~6–8 µs of phase/residual bookkeeping that the design's "kick updates the cycle by a multiply-add" (law.md, representation.md §3) deletes. At 64 kicks/orbit this is the gap between the plane and representation.md §6's ≈50 ns incremental kick. Orders of magnitude: the compile input is over-paid ~2^14× at the memo's own resolution (avg key movement 2^34 of the Q48 shape word per rebind). What it deletes: the Cartesian↔invariant boundary in the hot path, and the fit+compile as per-kick work (it becomes a rare, shared, memoized event).

## Evidence (commands, each ≤ 60 s where possible)

Machine: cloud container, 2 shared vCPU — timings are orders of magnitude only; the container's load swung 2–3× during the run, so **counts are the decisive evidence, not the µs**.

```
cargo build --release -p emergent-universe --example cost_split
./target/release/examples/cost_split                       # baseline, unmodified tree
# → pure kick (resolve) 29.3 us | own readout 3.12 | secondaries 3.04 | tide 3.01
#   whole universe: 47.8 us per item
```

Instrumented (patch in `patch-note.md`): fit/compile timed inside `Rebinding::from_state`; per-body old-vs-new key comparison in `Work::rebind`; kick firing counters. Quiet-container run:

```
# → rebinds 27721 | fit 3.8 us avg | compile 6.7 us avg      (10.5 of the 29.4 us)
# → kicks 27814 | fired 27694                                 (99.6% of kicks fire a rebind)
# → per-body rebinds 27698 | same-exact 0 | same-cell 27346   (98.7% same 44-bit memo cell)
# → dk avg 1.67e10 (2^34 of the 2^48 shape word; ~2^14 rebinds per cell crossing)
```
Prototype (bit-identical by construction: the compile is pure, the memo returns the same `Arc<OrbitShape>`): `crates/space`'s own `ShapeMemo` wired into `from_state`'s Cycle branch:

```
./target/release/examples/cost_split                        # LAB_NO_MEMO unset
# → shape-memo hits 24443 of 27721 rebinds (88%)
LAB_NO_MEMO=1 ./target/release/examples/cost_split           # control: hits 0
```
With the memo wired, `cargo test --release -p emergent-universe`: 19 tests, 0 failed, 1 pre-existing ignored.

The interleaved A/B of wall time was inconclusive here (load noise ≥ the effect); the per-hit saving is `OrbitShape::bound` (the quadrature) and must be re-measured on a quiet machine or the M1 — that is the named experiment for gold. `cargo test --release -p emergent-universe` run for bit-identity evidence (result in the run's log; the argument is airtight regardless: a memo of a pure function cannot change bits).

## Predictions

`predictions.md` was written before any measurement. P1 held (29.3 µs reproduced; fit+compile 36% ≥ 40%-ish of the resolve; readout/secondaries/tide single-digit). P3 held (99.6% fire). **P2 held: 98.7% same memo cell** — the compile input is constant at the memo's resolution. P4 half-held: exact-key interning within a body gains nothing (same-exact = 0, as predicted possible), but the existing shape memo hits 88% as wired; the "≥10% cost cut" was unresolvable under this container's load — reported as not measured, not as passed.

## What would make it wrong

If the fit (not the compile) dominates on the M1, the multiply-add fix still deletes it, but the ShapeMemo wiring alone buys little. If bodies in real scenes (not this 8-ship plane) rarely share shape cells, the 88% hit rate is scene-specific — but the 98.7% same-cell measurement is per-body and scene-independent in kind. The deeper risk: the invariant-kick path (δE = v·δv, δL = x×δv, phase from stored derivatives, rebind at cell crossing) must keep the residual exactness the current per-kick fit guarantees; B5 (error type/exponents), B12 (Jacobi at handoffs) and B8 (determinism) are the guards, and the rebind threshold becomes law (a fixed function of state, never of schedule — universe-quanta.md).

## Cost of adoption, fit with PRINCIPLES

One owner (Sol owns kicks; the universe crate is his) rewires `kick` to land on (E, L) and schedules the rebind as an event at key-cell overflow; `crates/space`'s memo APIs already exist (`ShapeMemo`, `QuantizedMemo`, `CyclePool`) — the universe's `Catalogue` is the only slots-without-keys store in the tree. No new mechanism, no new gate; B5/B12/B8 judge it. This is principle 19 verbatim: "if you find yourself fixing things that's oftentimes a signal that it is the wrong representation" — the fit+compile is the fix, the Cartesian kick layer is the wrong representation; and principle 3's "compute only surprises": a kick that does not move the memo key is not a surprise, yet today it recompiles a geodesic.

## The lens: what it may have made me miss

The whole-system lens looked for one unification and found a boundary; it did not audit the queue/scheduler layer (bottleneck 4) or the gather cache's interaction with kick cadence, and it took the SyMBA changeover as given (the queue's TRACE/JANUS question). The elegant-unification blind spot: "kicks land on invariants" could hide the hard case the register already warns about — a body deep in a secondary's shell mid-changeover, where (E, L) in one doll is ill-defined and the Cartesian form is the honest one; there the rebind must stay, and the win shrinks to the memo.
