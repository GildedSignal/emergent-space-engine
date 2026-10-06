# Dossier — 20261006-1436-quant-18e5

**Claim.** On the shipped plane, the frame budget bounds the *queue* but not the *item*: one engine item can run 25–30 ms past the 5 ms budget (a 37 ms worst frame at battle contact under max throttle), while the unbudgeted view is the majority spender (63% gather + 15% json+wire) at every scale measured; and the frame as the player runs it costs 2.7–5× its unpaced hot-loop cost.

**Bottleneck.** Board bottleneck 4 (smoothness and the allocator; Julien: "the algorithm that allocates the work … is the most important one") and lens item 1 (which stage is over its share). The gain lever named: the worst frame is lost inside single items, not in queue order — so allocator work on ordering cannot fix it, and the next microsecond-level kick work (Sol's `wt/kick`, 29 µs) is not where the played tail is.

**Evidence** (all from `cargo run --release -p xtask -- universe --bench`, 30 s, Linux x86 shared runner; orders of magnitude only; exact commands below; JSONs in `data/`, series in `data/*.csv`):

| run | members | level | budget | cpu p50 | cpu p99.9 | worst | hitches >16.7/>33 ms |
|---|---|---|---|---|---|---|---|
| a | 48 | 0 | 5 ms | 3.5 | 12.2 | 12.5 | 0/0 |
| b | 480 | 0 | 5 ms | 8.8 | 15.4 | 15.9 | 0/0 |
| c (seeds 1/2/3) | 4800 | 0 | 5 ms | 8.4 | 17.3 | 19.7 / 12.6 / 10.5 | 4/0, 0/0, 0/0 |
| d | 48 | 15 | 5 ms | 3.7 | 11.0 | 11.3 | 0/0 |
| e | 480 | 15 | 5 ms | 9.1 | 19.6 | **37.2** | **3/1** |
| e2b | 480 | 15 | **20 ms** | — | 25.4 | 49.0 | **50/1** |
| f (rtf 10⁴) | 48 | 0 | 5 ms | 7.4 | 10.9 | 11.4 | 0/0 |

1. **The item is the budget's quantum, and one item blew it 6×.** In e (480 members, throttle 15) frame 102 spent 30.5 ms in the engine under a 5 ms budget (`data/e2.csv`; the budget is checked between items, `Universe::advance`, universe.rs:808). Frames 76, 102, 373 are the only engine frames >10 ms; they do **not** coincide with burn frames (nominal 0, 19, 239, 259, 479, …) — the tail is battle-contact-shaped, not decision-shaped. Median item cost is ~17 µs (3.8 s over ~30k items), so the worst item is ~1500× the median. Its identity inside `resolve_entity` is not yet pinned (no perf on this runner, `perf_event_paranoid=4`); one line of max-per-kind in `Stats::cost_ns` would name it.
2. **The budget is the smoothness dial.** Raising it 5→20 ms at the same scene converts deferred work into hitches almost 1:1 (3→50 hitches >16.7 ms; 57 frames with engine >10 ms, most pinned at the 20 ms budget). Under 100× overload (f) the engine saturates at its budget (p50 5.06 ms, max 7.9 ms) and the degradation is a smooth rtf dip (median 8676 vs 10⁴ asked; lowest 1%: 4.2) — "the budget changes when, never what" behaves as designed, up to item granularity.
3. **The view is the majority spender, unbudgeted.** gather 63% + json 11% + wire 4% of frame CPU in every paced run (engine 22–26%); at overload the engine share rises to 69% only because everything else is small. `Seen` is 152 B against the M1's 128 B line — every emitter straddles a line (sizes audit in `sizes/`, exact, layout-portable).
4. **Paced cost is 2.7–5× hot-loop cost.** Same scene, same seed: cpu p50 3.46 ms paced vs 0.69 ms unpaced at 48 members (5.0×), 8.4 vs 3.08 at 4800 (2.7×). Every µs-per-item number taken from unpaced benches flatters the played cost by this factor on this box.
5. **Members do not scale the frame past ~500.** Live bodies cap at 428 for members = 480 and 4800 alike (the fleet hands members out at its own rate; 30 s is not enough), so per-member linearity is untestable in this scenario as-is — the m4800 numbers measure the same 428-body world with a fatter tail (battle geometry unchanged: 178 encounters in all runs).

**Predictions** (`predictions.md`, written before the runs): P1 held at p99.9 everywhere (engine p99 ≤ 6.7 ms) and failed exactly at the worst frame (the 30 ms item) — reported as held-then-broken, the interesting half. P2 held. P3 half-held (linear 48→480, then the live-body cap). P4 falsified (worst frames not at burns; the 2.3× level-15 worst is contact-driven, absent at 48 members). P5 held with the same cap caveat. Held-out cases: members ×10/×100, level 15, rtf 10⁴ — none tuned on.

**What would make it wrong.** M1 re-measurement (the integrator's): the 30 ms item could be an x86 allocator or frequency artifact — though it is CPU time, not wall, so descheduling is excluded; a different seed set could move the tail frames (three seeds at 4800/l0 gave worst 19.7/12.6/10.5 — the tail is genuinely fat, which is the point). The warmth factor could shrink on the M1's unified memory.

**Cost of adoption.** None for the measurements (all from shipped code; the only edit is an env-gated CSV dump of series the Dash already keeps, in this run's patch). Acting on it: extend `Stats` with max-per-kind (one line) before any further kick micro-optimization; budget or thin the view gather (already Sonnet's job — this confirms it is the top spender, and adds the 128 B `Seen` trim, 152→≤128 B, as a concrete step).

**Fit with PRINCIPLES.** "i care about the p95/99 results i want the game to be smooth" (§12); "Measure before claiming" (§10); "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" — this run locates the heavy tail: inside one item and in the unbudgeted view, not in queue order.

**The lens (quant) may have made me miss:** the physics inside the 30 ms item (why does contact+burn produce a 1500× item?); whether the rtf-dip smoothness holds on the M1's efficiency cores; and anything about correctness — this lens prices tails, not truths.

## Reproduce (each ≤ 60 s, from the repo root)

```
cargo build --release -p xtask
T=/home/glmlab/lab-target-3/release/xtask   # or target/release/xtask
$T universe --bench --seed 1 --rtf 100 --members 48  --level 0  --seconds 30   # a
$T universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 30   # e: worst 37 ms
$T universe --bench --seed 1 --rtf 100 --members 480 --level 15 --engine-ms 20 --seconds 30  # e2b
$T universe --bench --seed 1 --rtf 10000 --members 48 --level 0 --seconds 30   # f: overload
$T universe --bench --seed 1 --rtf 100 --members 4800 --level 0 --seconds 30   # c
$T universe --bench --seed 1 --rtf 100 --members 48  --level 0 --seconds 30 --unpaced  # g
```
Read `frame_cpu_ms`, `worst_hitch_ms`, `where_the_time_goes_ms` from the printed JSON. Per-frame series (`data/*.csv`) need this run's patch (env `PLANE_FRAME_DUMP=<path>`; it only dumps vectors the Dash already keeps). Struct sizes: `cd sizes && cargo run --release` (deps by path).
