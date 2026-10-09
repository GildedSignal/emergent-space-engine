# Check of 20261009-2212-constraint-2380 (lens: the constraint)

Grade: gold

## Abstract (for the integrator)

Measured on the whole plane, the frame's constraint is the unbudgeted O(live-bodies) view gather, not the budgeted engine: one light-cone readout costs ~10–11 µs, stable across seeds and 28–1,501 bodies, so ~1,600 live bodies eat the whole 16.7 ms frame. I ran the author's "unrunnable" extrapolation (one-line clamp lift, 12 s): 1,501 bodies → gather p50 14.7 ms ≈ readouts × atom (13.1 ms), first hitches above 36 ms, 89 % overflow. Digests reproduced bit-identically (bench, kick-bench, both held-out); predictions held except the disclosed readouts/body miss. Separately, paced-on-idle timing inflates ~4× on identical inputs and digest — a trap for every cloud number. Adopt: add the view gather to the board (cull + incremental re-derivation); cite H0210's 83 % as the pre-cache precedent.

## Reproduction (clean tree, main + the run's patch.diff)

| quantity | author | mine |
|---|---|---|
| bench 7/100/400 digest | 06b78c… | 06b78c… identical |
| kick-bench digest | 557e9f… | 557e9f… identical |
| held-out seed 3 m400 digest | 00ac05… | 00ac05… identical |
| patched vs unpatched digest | same | same (verified) |
| paced vs unpaced digest | — | same (verified) |
| gather p50 (m400, load ~2.5) | 3.18 ms | 3.16–3.18 ms |
| engine p50 (m400) | 0.88 ms | 0.93–0.96 ms |
| readouts m400 | 272 | 272 (deterministic) |
| µs/readout m400 | 10.4 | 10.9 |
| kick median / p99 | 42.8 / 77 µs | 40.9 / 64.6 µs |

`predictions.md` (22:23:15) precedes both held-out runs (22:23:34, 22:23:46) and follows all tuning runs — order verified by file times. The patch is pure instrumentation: identical digests with and without it.

## Adversarial cases (mine)

1. **Unseen seed 11, rtf 100, m400**: atom 9.8 µs (in the 9–13 band), gather share 0.55, no hitch above 16.7 ms. Held.
2. **The extrapolation, actually run**: `--members` clamp lifted locally (4→4000, one line, reverted after): 1,501 live bodies, atom 11.4 µs (N-independent), gather p50 14.73 ms vs readouts × atom = 13.1 ms (+13 %), json 3.8 ms on top, worst hitch 36.1 ms, overflow 644/720. The frame dies exactly where the dossier said. The clamp, not physics or the 60 s rule, hid this — the author left the one decisive run undone.
3. **Determinism under pacing**: m400 paced vs unpaced — identical digest; gather p50 equal under load.
4. **The trap pair re-derived from the author's files**: three 900-frame runs, one digest (89417b…), gather 3.31 ms at load 0.58 vs 0.81/0.74 ms at load 2.5 — the 4.1× swing is real and same-input.

## Novelty

Partially anticipated: H0210 already recorded "the view gather is 83% of a light frame" (1 October, pre-cache) and H0212 made the cache relativistic (readouts ≈ 1/emitter — this run confirms the cache works: the atom, not the search, is the cost). The dossier cites H0212 but not H0210's line. What is new and measured: the post-cache quantification (the ~10.5 µs atom, readouts/body), the demonstration that the gather is the only unbudgeted synchronous claim and violates foundation 7's letter at a reachable scale, the confirmed linear law with its break-even, and the paced-on-idle timing trap. The board's focus list (integrator, 1 October, reaffirmed 5 October) names engine questions only — the premise this run corrects.

## Goal fit

Foundation 7 is quoted verbatim and the violation is demonstrated, not argued ("Nothing takes an unbounded synchronous claim on the frame, whether a cycle compile, a rebinding burst, a decompression or a gather"). "Nothing is evolved that can be derived when looked at" (PRINCIPLES 3) applied to the view for the first time; "the view is an instrument" (28). Gold clause met: it shows a premise wrong (the engine is not the frame's constraint at plane scale; the view is) and is adoptable within one step (a board entry plus the pacing discipline; nothing to merge, no law change).

## What the author missed

- **json and wire are also O(visible bodies)** (one serialised entry per pushed body): at 1,501 bodies the frame dies before the gather alone hits 16.7 ms (14.7 + 3.8 ms). The view path is unbudgeted three ways; the headline understates its own case.
- **The stated bands are rosy at the top scale**: "gather 56–78 %" should read 53–71 % (their own m400 files: 53.0/53.3 %); "engine 4–22 %" understates m400's 30–33 %. The ordering (gather > engine) holds everywhere measured.
- **The share claim is not universal at 28 bodies**: my seed-11 rtf-1 run under contention put json (0.85 ms) above gather (0.56 ms); at that scale all parts are sub-ms and the constraint claim is unaffected, but "at every scale and seed tried" is machine-condition-dependent.
- **The atom is load-sensitive beyond the claimed stability**: I measured 9.7–16.4 µs (load 1.4–2.8). Orders of magnitude only, as the lab README already demands; the break-even stays O(10³) bodies.
- **The `-idle` file is misnamed** (it ran at load 2.4); the trap's evidence stands on the load-0.58 vs load-2.5 pair alone.
- `readouts` is wall-dependent (my seed-3 rerun: 237 vs the author's 231) — correctly treated as a measure, not a result.
- The `behave` run is garbage (all gates unanswered, B14 timeout) and honestly discarded; a view-cost claim did not need it.
