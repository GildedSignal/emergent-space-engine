# Dossier — 20261009-0401-quant-ea6b (Quant lens)

**Claim.** One kick of the plane's resolver (motion law v2) costs a median 35 µs (made bodies) / 70 µs
(fleet members) on this box, 59% of it in the rebind's tube work, only 1.37× more when every cache is
cold — so the kick path is compute-bound and the lever is deleting rebind work (the jet/re-anchor), not
memory layout — and at the measured cadence the resolver alone saturates one core near 1.3×10⁵ ships at
rtf 100, three orders of magnitude short of 10⁹.

**Bottleneck.** "Fewer kicks per orbit / kicks dominate the engine's cost" (board focus, 1 October).
This run prices the kick itself: where the time goes, whether it is latency- or compute-bound, and the
capacity it buys. Expected gain of the priced lever: the rebind is 59% of every kick and the quantized
(E, L) memo key was already present for 97% of rebinds (260 shapes covered 8,962 rebinds), so a reuse
mechanism that avoids exact recompiles addresses most of the kick's cost — a 20× cut on rebind would
take the average kick from 52.6 µs to 22.9 µs and multiply capacity by 2.3.

**Evidence** (all commands ≤ 40 s each, on this 8-vCPU i7-4790, loadavg 1.7, 13.5 GB free; the
machine-state probe in the bench is macOS-only and fails on Linux — recorded by hand instead):

```
cargo build --release --locked --offline -p xtask          # 35 s
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10                       # digest control
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 2000 --seconds 20        # warm, rtf 1
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 2000 --seconds 30 --rtf 100   # 9192 samples
KICK_COLD=1 $CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 2000 --seconds 30 --rtf 100
```
Raw JSON in this folder (`kick-bench-baseline.json`, `kick-warm-m2000.json`,
`kick-warm-m2000-rtf100.json`, `kick-cold-m2000-rtf100.json`). Stage timers were added to
`crates/universe/src/step.rs::kick_clock` and printed by `xtask/src/universe/kick_bench.rs`
(the tree's patch carries them); the digest control — same `replay_digest`
(`dac49af3…`) and memo counts on the unmodified argument set — shows the instrumentation changed
no behaviour.

| Measurement | Result |
|---|---|
| made-body kick | median 35.2 µs, p99 58.1 µs (n=365) |
| fleet-member kick | median 69.9 µs, p99 388.6 µs (n=8827) |
| stage shares (all kicks) | **rebind 59.3%**, gather 21.8%, readout 10.3%, forces+clock 4.9%, other 3.7% |
| cold / warm (paired, n=9192) | 95.2 / 69.7 µs median — **ratio 1.37×** |
| memo | exact hit rate 0.0; quantized (12+12-bit) hit rate **0.971**, 260 shapes for 8962 rebinds |
| cadence | 1.50×10⁻³ kicks per ship per game-second (this scene, rtf 100 run) |
| capacity (resolver only) | ≈ 1.27×10⁵ ships per core at rtf 100 (median mix, 1/52.6 µs); ≈ 5×10⁵ on 4 P-cores |

**Predictions** (`predictions.md`, written before the runs): held — rebind > 50% (59.3%), compute-bound
not latency-bound (1.37× < 1.5×), made-population tail p99/median 1.65 < 5, cost level 35–48 µs inside
the 10–60 µs band. Failed, honestly: (1) capacity — I predicted the resolver saturates below ~2×10³
ships at rtf 100; it actually reaches ~1.3×10⁵ per core, 60× better than my guess (the fictitious clock
makes far-field kicks rare); (2) the leaver/made ratio exceeds 4 on first handouts (387 µs vs 35 µs at
rtf 1 — the first kick of a fresh fleet member pays a cold shape compile; at rtf 100 the leaver median
is warm at 69.9 µs).

**What would make it wrong.** The stage timers wrap four hand-picked regions inside `kick_clock`; a
stage that straddles a boundary (e.g. planning after the rebind) lands in "other" (3.7%, small). The
cadence and capacity numbers hold for this scene (seed 1, 2000 members, one star system) — a denser
system kicks more often and shrinks the ship count proportionally; the ratio, not the count, is the
portable result. Hardware counters were unavailable (perf_event_paranoid=4, no sudo), so "compute-bound"
rests on the cold/warm delta, not on IPC/cache-miss counters; a stall-heavy path that fits in L2 would
look the same. Cloud-vs-M1: orders of magnitude only, per the lab rules.

**Adoption cost and fit.** Nothing to adopt in main; the numbers price two live queue items: the
jet/re-anchor (already the adopted design after the 5 October artifact killed naive quantized reuse —
my 97% quantized-hit rate is the size of the addressable pool, not a proposal to re-round orbits) and
b-readout-cost (the gather at 22% is per-kick re-readout of the sources' tubes). PRINCIPLES: "The
cheapest compute is compute not done. Delete before optimizing" (1) — the measurement says delete the
recompile, don't tune the cache; "Measure before claiming" (10) — this is the measure. Cost: the
instrumentation patch is 40 lines, printable by any future bench run, zero effect when unread.

**The lens.** A quant eye prices one path in isolation; it cannot see whether the *cadence* (which
kicks exist at all) is the truer lever — the board already says cadence beats correctors, and my
capacity number is dominated by cadence (1.5×10⁻³ kicks/ship/s), not by per-kick cost. It also prices
the median and p99 of a pure resolver, not the frame the player feels (allocator, view, gather are
outside; the bench exists to exclude them). And it treats the 97% quantized hit rate as an opportunity
pool, staying silent on whether reuse under it would violate "errors never compound" (13) — the 5
October artifact already answered that it would, as a naive reuse.
