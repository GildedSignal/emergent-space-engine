# Dossier — 20261012-0036-quant-115e (quant lens)

**Claim.** The plane's presented frame pays a measured ~43–60 ns per planned body *even when zero
events resolve* (the per-frame `rekey` of every deadline), and the kick's price is 70.7 % rebind
bookkeeping with an 11× p99.9 tail — while the physics inputs are 28 % and the force arithmetic
2.7 % — so at belt cadence the event's unit price is already within ~1× of its billion-body
budget, and the levers are lazy deadline re-keying (O(events), bits preserved) and rebind
slimming, not cheaper force math or more splits.

**Bottleneck.** Board #1 (kicks dominate the engine's cost) and #4 (smoothness, the allocator,
p99): this run prices the kick stage by stage with tails (which only means existed before, via
`cost_split`), and measures the per-frame scheduler tax the frame pays at N. Expected gain of the
named fix: the rekey pass deletes entirely at scale (60 ms → sub-µs per frame at 10⁶ planned
bodies: ≥ 10³×); it deletes a per-frame O(N) pass, which plane.md foundation 7 forbids
("Nothing takes an unbounded synchronous claim on the frame").

**Evidence** (all on this shared x86 runner, i7-4790, load recorded in the output; orders of
magnitude only — the integrator re-measures on the M1; every command ≤ 60 s):

```
# with this run's probe applied (run.sh saves it as patch.diff; timing only, no semantics):
cargo build --release -p emergent-universe --example kick_budget --example digest_control
$CARGO_TARGET_DIR/release/examples/kick_budget        # both phases; full output: bench-decisive.txt
$CARGO_TARGET_DIR/release/examples/digest_control     # pristine-digest control (built on stashed src)
cargo test --release -p emergent-universe             # 11 suites, all pass, patched and pristine
```

*Phase A — the event's stage budget* (default plane scene, settle 3×10¹⁰ ticks, 49,619 items):
- Kick(0) `step::process`: p50 34.0 µs, p99 75.5, **p99.9 379**, max 544 (n = 24,606). The
  kick's own tail is **11× its median**; boundaries' is 3.5× (p99.9 60 of 17.1), so the tail is
  kick-specific, not machine noise (load was 0.9–1.0 for the decisive run).
- Stage shares of the WH kick: **rebind 70.7 %** (26.8 µs), readout 8.5 %, secondaries+tide
  17.5 %, force 2.5 %, quantize 0.2 %, bookkeeping 0.1 %. The changeover levels cost ~11× a
  plain kick (Kick(1) p50 371.8, Kick(2) 370.3 µs; n = 216): near a secondary, one body's kick
  stream is 10× heavier for the encounter's duration — a per-body heavy tail, the allocator's
  exact enemy (OC#36).
- `apply` after every event: 6.9 µs/item, **97 % of it `root_state`** (the position cache that
  feeds the deadline heuristic). `requeue`: 0.14 µs — cheap. Classes per item: planet 23, moon
  35, ship 36, **player 151** (its items carry the encounter search; the "market order" costs 4×
  a ship's), fleet 67 µs.
- Budget arithmetic (assumptions explicit): 10⁹ bodies × 32 kicks/orbit (H0190), 1-year belt
  orbits, rtf 100, 4 cores, 60 Hz → ≈ 1.7×10³ events/frame and **≈ 39 µs of core per event**.
  Today's ship item is ≈ 35 µs (process+apply+requeue). At secular cadence (0.3/orbit) there is
  100× slack. The event's unit price is not the wall; the per-frame pass is.

*Phase B — the per-frame scheduler tax* (N extra Home orbiters; 30 frames at `Budget::wall(0.0)`;
**events resolved: 0 in every row**):

| bodies | frame p50 | rekey | ns/body |
|---|---|---|---|
| 28 | 7.3 µs | 7.2 µs | — |
| 4,028 | 172.5 µs | 172.7 µs | 42.9 |
| 16,028 | 698.9 µs | 704.9 µs | 44.0 |
| 64,028 | 3,472.8 µs | 3,532.2 µs | 55.2 |
| 256,028 | 15,392.6 µs | 15,458.6 µs | 60.4 |

Linear in N with a growing per-body coefficient (heap depth + cache). Extrapolated: **10⁶
planned bodies ≈ 60–75 ms per frame — 4× over the 16.7 ms budget with no work done**; 10⁹ is
minutes per frame. The root-doll control (64 k "inert" haulers) costs the same 3,477 µs: in the
shipped plane the planets are root-doll sources, so **every ship is a planned, queued body** —
no body class escapes the tax. In the settle the same pass ran only twice (unlimited budget does
giant advances); it bites exactly in the session's per-presented-frame `frame_to`.

*Controls.* Pristine and instrumented builds produce the **identical digest**
`e317b268…a5be` and identical item/lost/refused counts over the same settle; all 11 test suites
pass on both. `perf` hardware counters are blocked here (`perf_event_paranoid` = 4), so
cache-line counts are inferred from the structure (indexed 4-ary heap, inline keys), not
measured — named below as a miss.

**Predictions** (`predictions.md`, written before both decisive runs): 1, 2, 5, 6, 8 held
(rebind > 40 % — it is 70.7; plumbing 20–35 % — apply+requeue ≈ 20 % of the ship item; slope
30–200 ns/body — it is 43–60; ≥ 10⁶ bodies over budget with zero events — it is over by 4× at
10⁶, minutes at 10⁹; belt arithmetic same order). **3 and 7 failed, honestly:** the kick's
p99.9/p50 is 11× (predicted ≤ 5), and there is no inert ship class in the plane (predicted
near-free root-doll bodies — the planets are root sources, so all ships are planned). Both
failures sharpen the claim rather than weakening it.

**What would make it wrong.** The M1 could halve or double the slope, not the O(N) shape; the
laziness argument needs deadline drift ≤ 2c·Δt per frame (true by construction — nothing exceeds
c), and it preserves bits only because the plane is already order-independent (foundation 2,
"B8 at universe level") — if that ever weakens, lazy rekey changes outcomes and dies. The 39 µs
budget line assumes belt periods at rtf 100; short-period populations at the same rtf tighten it
linearly.

**Cost of adopting, and fit with PRINCIPLES.** Adoption is one local change: rekey becomes
amortized — a body's deadline is recomputed when it resolves (already done, `requeue`) and
otherwise only when its cached deadline is within a bounded-staleness slack of the heap min
(drift ≤ 2c·Δt_frame); the digest-identity control above is its test. No law, gate or crate
interface changes. This is PRINCIPLES #3, "Nothing is evolved that can be derived when looked
at" and #14, "no work for no reason" — the deadlines are a scheduling heuristic recomputed for
all N each frame; and #12, "the algorithm that allocates the work … is the most important one" —
the tax is the allocator's own overhead. The rebind share (70.7 %) confirms the integrator's
existing memo direction (the plane recompiles an orbit on ~99 % of kicks); this run adds that
the recompile is not just frequent but the kick's dominant cost, and that its tail, not its
mean, is what a 60 Hz frame will feel.

**The lens (what it may have missed).** An HFT eye prices CPU tails and order-book mechanics,
and I could not count cache lines (counters blocked) — the heap's cache behaviour at 10⁶+
in-flight slots is inferred, not measured, and the proposed slack mechanism needs a capacity
check against deadline-density spikes (a fleet arrival: all deadlines near the min at once).
The tail's internal stage is unresolved (sum-accumulators only); a per-event stage trace is the
named next probe, alongside the level-1 kick's 11× cost (SyMBA changeover path).
