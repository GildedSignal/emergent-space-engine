# Dossier — 20261008-1719-constraint-1fe2 (lens: the constraint)

## Claim

On the plane as it flies today, the frame's constraint is the readout pipeline (gather + JSON +
wire: 71–95% of frame CPU at every corner measured), not the engine (5–32%); the board's queue
order optimizes the minority, and the cheapest proposed exploit for the readout — sending only
changed Seen entries — is dead by measurement (86–87% of entries change per frame at a
3-significant-digit display quantum).

## Bottleneck

Board focus item 1 ("kicks dominate the engine's cost") and the queue's order (engine builds
first: energy register, plunge tubes, handoff, Kerr, news gravity, Fermi, co-orbital; the
readout's cost is 9th of 14). Measured whole-system shares say the frame is not engine-bound at
any corner the player can reach today, so engine-side gains buy at most ~1.4× on the frame, not
the 10× the goal needs. Expected gain from reordering: the readout pipeline is a 2.5–19× larger
share than the engine; fixing what it does per body is where frame headroom lives.

## Evidence

Machine: GitHub Actions linux-x86, 8 vCPU, load 0.7–1.4 (uptime recorded in each JSON). All
commands ≤ 60 s, tree = main plus this run's instrumentation (`work/patch.diff`: per-frame tube
readout count, max Seen width, frame-pair Seen identity — exact and quantized; it changes no
measured path, only adds counters after the timed sections).

The sweep (each 15 s, paced 60 Hz, seed 1, threads 1; JSONs in this folder):

```
cargo build --release -p xtask
./target/release/xtask universe --bench --seconds 15 --members M --rtf R   # M ∈ {48,400}, R ∈ {1,100}
```

| corner | seen_max | readouts/frame | gather p50 | gather share | json+wire share | engine share | engine p99 | frame p50/p99 |
|---|---|---|---|---|---|---|---|---|
| m48-r1 | 76 | 44 | 0.53 ms | 68.8% | 24.7% | 6.4% | 0.12 ms | 0.74 / 1.27 ms |
| m400-r1 | 428 | 44 | 0.57 ms | 31.5% | 63.3% | 5.2% | 0.16 ms | 1.79 / 2.68 ms |
| m48-r100 | 76 | 68 | 0.82 ms | 63.9% | 13.2% | 22.9% | 1.57 ms | 1.10 / 2.66 ms |
| m400-r100 | 428 | 280 | 3.07 ms | 56.6% | 14.2% | 29.2% | 5.52 ms | 4.78 / 10.82 ms |

Readout pipeline share (gather + json + wire): 93.5%, 94.8%, 77.1%, 70.8%. The engine never
exceeds 32%. `--kick-bench` (pure resolver): 42.8 µs median per ship kick, 369 µs for leavers.

Mechanism (code-read, `crates/universe/src/view.rs`, `observe.rs`):
- Fleet members are gathered by cheap velocity extrapolation to the retarded tick (no tube
  readout), then each becomes a full `Seen` → serialized and wired every frame: ~2.8 µs per
  member per frame at rtf 1 (m400−m48 marginal), 86–94% of it json+wire.
- Members handed out of the fleet become real bodies with tube crossings: readouts/frame rises
  44→280 at rtf 100 (0.6–0.9 ramped readouts ≈ 6.7 µs per body per frame, the exact cost the
  b-readout-cost brief targets).
- The engine advances bodies only on events (fleet: ~1 lattice slice per frame total, ~64–78 µs,
  independent of member count; ships: 278 µs per advance, ~0.13 advances per ship per frame).
  Engine O(events); view O(bodies) every frame, with no budget and no visibility gate.

The killed exploit (identity runs, 12 s each, `identity-m400-r{1,100}.json` in this folder):

```
./target/release/xtask universe --bench --seconds 12 --members 400 --rtf R   # R ∈ {1,100}
```

Entries equal to the previous frame's entry at the same index: exact 0.0% (rtf 1), 3.1% (rtf
100); after rounding every float to 3 significant digits (a display quantum finer than the
page can show): 12.6% and 14.1%. Virtually every visible entry changes every frame — because
`age`, `offset`, `lag` and the crossing tick advance with every frame — so delta serialisation
sends ~what a full send sends. Cheaper or diff-er Seen will not move the p50; fewer Seen will.

Extrapolation to the goal (order of magnitude only, cloud timings): at the measured marginal
costs the gather+wire alone meets the 16.7 ms frame at ≈1,900 bodies at rtf 100, ≈6,000 members
at rtf 1 — six orders of magnitude from 10⁹. The engine's event-sparse cost is not what caps
the plane today.

## Predictions

`predictions.md` was written before the sweep. Held: (3) readout > engine share at every corner,
readout p50 > engine p50 everywhere; (5) the readout, not the kicks, caps scale. Partially held:
(1) linear-in-members — true for the pipeline, but the per-member cost lands in json+wire (not
the crossing), and only once members are handed out does the gather grow; (2) rtf raises the
gather modestly — held at fixed members (0.53→0.82 ms) but understated once handed-out bodies
appear (0.82→3.07 ms). Failed: (4) readouts ≈ 2× gathered bodies — false, members are
extrapolated, not crossed; the counter showed 0.6–0.9 readouts per crossed body, 0 for members.

## What would make it wrong

Measuring on the M1 with a browser attached (the JSON+wire cost here excludes HTTP and the
page's own render; a real page could shift shares, though not the O(bodies)-per-frame law);
a corner where the engine's burst p99 (5.5 ms at m400-r100) becomes the binding frame cost —
at ~3× today's event density the engine's p99, not the readout, would own the worst frame;
a visibility gate already in the wire path that I missed (none found: the gather is a plain
loop over all bodies, `view.rs:300`).

## Cost of adopting, and fit with PRINCIPLES

Nothing to merge: the patch is instrumentation only (three counters in the bench report; no
measured path touched). The finding reorders attention, not code: the readout pipeline is the
constraint today, and its lever is fewer Seen (a display-quantum visibility gate — "the zoom
level is the minimap", OC#30; "nothing is evolved that can be derived when looked at (clocks,
redshift, views)", PRINCIPLES 3; "the memory floor is what the player can differentiate" — the
Seen list has no such floor today: every body, every frame, full precision). Cost: one build
step on the wire path, judged by `frame_cpu_ms` and the readout test, before any gate is
touched. Fit: Goldratt's "an hour saved elsewhere is a mirage" — the queue's engine work is,
on today's measurements, the mirage; Musk's "question the requirement, delete the part" — the
requirement to See every body every frame is the part to delete.

## The lens

The constraint lens sees the frame, not the game: at billion-body scale the engine's event cost
per body is the wall, and the board's kick work targets exactly that wall; my corners reach
only 428 bodies. What the lens may have missed: whether Julien's flying view (a real browser,
1080p, the page's render) shifts the shares enough to restore the engine-side priority; and
whether B12–B14 stability, not smoothness, is the constraint that actually blocks merges this
week (a gate constraint, not a throughput one — outside what I measured).

## Grade suggested

Silver: real, reproduced, one named experiment from gold — the next run builds the visibility
gate (fewer Seen by display quantum) and shows the frame p50 at m400-r100 drop by the share
the pipeline holds; if it holds, that is the 10× question answered where it stands.
