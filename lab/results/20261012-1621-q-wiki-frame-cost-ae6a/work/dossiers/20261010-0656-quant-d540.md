# Dossier — run 20261010-0656-quant-d540 (Quant lens)

## Claim

The plane's presented frame is Ω(N) in bodies with **zero events** — ~0.7 µs per body per frame
of pure deadline bookkeeping — so the live-tube queue path breaks the 16.67 ms budget at
N ≈ 3×10⁴ bodies (0.72 s per frame at 10⁶), and the exact player-neighbourhood check breaks one
player item at N ≈ 8×10³ (3.0 s at 10⁶); both are scheduling/read-only stages, so the fix is a
queue change, not a law change, worth ≥ 700× at 10⁶.

## Bottleneck

Board item 4 (smoothness and the allocator: "least-slack scheduling fed by surprise rates") and
the queued belt build (`b-belt-wire`, B18b): the bet that a belt of 10⁵–10⁶ tubes can join the
plane's one queue. Measured before the bet is placed: at 10⁵ belt bodies the frame costs 55–68 ms
**before a single ship kicks** (events = 0 in every run), 100% of it scheduling. Expected gain
from the fix: frame at 10⁶ from 720 ms to under 1 ms (≥ 700×); it deletes the per-frame deadline
sweep and the per-advance rekey as work classes.

## Evidence (Linux/x86, shared box, load printed; orders of magnitude only)

Isolated runs (load ~2.2); raw outputs and the shared-load first sweep in [results.md](results.md);
the bench is [nwall.rs](nwall.rs), shipped as `crates/universe/examples/nwall.rs` in this run's
patch. All commands ≤ 60 s unless noted.

| N | frame p50 µs | sched-only µs | rekey µs | events | one `find` µs (hits) |
|---|---|---|---|---|---|
| 100 | 14–28 | 14–28 | 3–6 | 0 | 146–247 (0) |
| 10³ | 359 | 354 | 61 | 0 | 2 666 (1) |
| 10⁴ | 2 236–2 262 | 2 217–2 262 | 341–361 | 0 | 16 194–17 427 (11) |
| 10⁵ | 55 019–68 061 | 53 776–68 192 | 6 961–12 437 | 0 | 161 353–192 999 (99) |
| 3×10⁵ | 193 578 | 193 203 | 31 619 | 0 | 885 923 (278) |
| 10⁶ | 721 515 | 795 481 | 117 868 | 0 | 3 010 890 (842) |

- **Attribution (code, `crates/universe/src/universe.rs`):** every `advance` calls `rekey`
  (line 792), which does one Calendar set per body (lines 499–505); the advance loop then
  defers every entity whose next item is beyond the frame target — a Calendar remove per body
  (lines 805–809) — and requeues them all at the end (lines 827–832): **three Calendar touches
  per body per frame, always**. `Budget::events(0)` advance (rekey + defer sweep, no events)
  equals the whole frame within ±5% at every N ≥ 10³: the frame is ~100% scheduling, 0%
  resolution. At 10⁶ that is ~3×10⁶ random-access heap ops ≈ 230 ns/op; at ~4–8 cache lines per
  op, ~12–24 lines per body per frame [INFERRED: `perf` is blocked on this host].
- **Break points:** p50 frame > 16.67 ms at N ≈ 3×10⁴; `rekey` alone breaks it at N ≈ 1.5×10⁵;
  one `PlayerNeighbourhood::find` (a binding + a cartesian per same-doll body,
  `crates/universe/src/encounter.rs:53-82`, ~1.6–3 µs/body, linear) breaks 16.67 ms at
  N ≈ 8×10³. At 10⁶, one find is 3.0 s — inside a single budgeted player item.
- **Memory:** peak RSS 1.93 GB at 10⁶ bodies ≈ 1.9 KB per live tube → live records cap near
  4×10⁶ bodies in 8 GB; a billion was never going to be live tubes (as designed: population
  programs), but the belt build now has the number.
- **Controls:** digest control EQUAL (1674 events settled; frames at two budgets vs a straight
  settle, one horizon — the harness changes nothing the law decides); rtf=1 equals rtf=100 at
  10⁴ (2 251 vs 2 262 µs: the cost is per frame, not per game-second); a fresh alpha layout
  (stride 40503) reproduces within 1.3×; the first sweep's outlier (7 276 µs at 10⁴) re-measured
  isolated at 2 262 µs (shared-load noise, disclosed in results.md).

Reproduce (each ≤ 60 s except the last, 63 s):

    cargo run -p emergent-universe --release --offline --example nwall -- control
    cargo run -p emergent-universe --release --offline --example nwall -- 100,1000,10000,100000 100 2654435761 3
    cargo run -p emergent-universe --release --offline --example nwall -- 100,10000,100000 100 40503 2
    cargo run -p emergent-universe --release --offline --example nwall -- 10000 1 2654435761 2
    /usr/bin/time -v <release examples dir>/nwall 300000,1000000 100 2654435761 0.3

## Predictions

[Predictions.md](predictions.md) was frozen before the decisive runs. P1 (frame Ω(N), ≥50×
growth 10³→10⁵): measured 154× (359 → 55 019 µs), events 0 everywhere. P2 (scheduling ≥ 80% of
the frame): measured ~100% (sched-only = frame ±5%). P3 (budget break 3×10⁴–3×10⁵): landed at
≈ 3×10⁴, the low edge. P4 (find 1–5 µs/body, crossing at 3×10³–2×10⁴): measured 1.6–3 µs/body,
crossing at ≈ 8×10³. P5 (controls): digest EQUAL with 1674 events (non-vacuous); fresh layout
within 2× (1.3×); all held.

## What would make it wrong, adoption cost, fit

- **Wrong if** the integrator's M1 numbers move the constants ×2–3 (cloud is x86; the Ω(N)
  structure is three code paths, not microarchitecture), or if belts never become live tubes in
  one queue (population programs keep belt members out of `bodies`; then this wall binds only
  the live-tube path — the Fermi battle's handed-out members, decanted populations, any belt
  stored as tubes — which is today's only shipped path, plane.md foundation 6's "plain tubes
  now"). The neighbourhood number would still bind the readout build (`b-readout-cost`) since
  `find` is the exact check the Binet cone is slated to replace.
- **Adoption:** two scheduling-only changes, digest-invariant by the plane's own budget
  invariance (verified by the control here): gate `rekey` on observer movement instead of every
  advance; replace the defer sweep with a horizon computed from peeked deadlines (never remove
  far entities). Both change *when* work is done, never *what* (plane.md foundation 7). One
  builder step in `crates/universe`; the belt build (`b-belt-wire`) should not be measured
  before it lands, or B18b grades the scheduler, not the belt.
- **PRINCIPLES:** #14 "No work for no reason, so no ticks… 'we only care about changes'" — the
  frame re-touches every body three times to learn that nothing is due; #1 "The cheapest
  compute is compute not done"; #12 "i care about the p95/99 results i want the game to be
  smooth" — the tail here is the whole frame, at zero events; the board's "least-slack
  scheduling fed by surprise rates" cannot be fed by a sweep that ignores surprise.

## The lens

What Quant may have missed: the zero-event frame is the *best* case isolated, not the belt's
working point — per-event cost under cache pressure at N (records at DRAM distance) and the
multi-thread path (`resolve_wave`, threads > 1) are unmeasured here; the M1's 128-byte lines
and E-cores will shift constants; and a scheduler fix bought purely for tails must not spend
the exactness that no p99 prices (this lens's own blind spot) — hence the digest control, and
changes confined to *when*.
