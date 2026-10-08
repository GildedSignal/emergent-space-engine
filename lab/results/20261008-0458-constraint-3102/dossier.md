# Dossier — the constraint, measured on the plane (20261008-0458-constraint-3102)

**Claim.** The plane's frame constraint is the view readout, not the engine: the per-live-body tube
readout in the gather costs ~11–15 µs (paced) and is 62–98% of every presented frame at every scale
measured (30–428 bodies, rtf 1 and 100), with the crossing memo already at its theoretical floor
(1.06 readouts/emitter) — so the lever is the readout constant and emitter selection, not the engine.

**Bottleneck.** Board focus "the readout's cost" (queue b-readout) and, behind it, smoothness (B15's
frame budget). Measured: the gather alone saturates the 16.7 ms frame at ≈1.1–1.5k live emitters
(15 µs × N × 60 Hz), three orders of magnitude below any scale goal, and it is paid even with the
engine idle. Expected gain from the named levers: 10× on the constant (the readout is dozens of
checked-i128 `Scalar` ops + a phase inversion per doll level), unbounded from selection (O(N_live) →
O(what the eye resolves)). What it deletes: the full scan in `gather_with`'s bodies loop, and most
of the view's JSON (it serialises every emitter every frame).

**Evidence** (Linux x86 cloud runner, 8 vCPU shared — orders of magnitude only; the integrator
re-measures on the M1; every JSON is in this folder, commands below):

| run | config | frame p50/p99 ms | gather p50 ms (share) | engine p99 ms (share) | overflow frames |
|---|---|---|---|---|---|
| `bench_rtf1` | 28+48, rtf 1 | 3.31 / 4.74 | 2.38 (74.6%) | 0.27 (4.7%) | 1 |
| `bench_rtf100` | 28+48, rtf 100 | 4.57 / 10.54 | 3.56 (69.8%) | 5.21 (17.5%) | 47/1800 |
| `bench_r100_m4` | →32 bodies | 2.82 / 4.76 | 2.34 (78.1%) | 2.05 (9.0%) | 1 |
| `bench_r100_m48` | →76 bodies | 4.51 / 10.65 | 3.53 (69.2%) | 5.15 (18.0%) | 55/1800 |
| `bench_r100_m400` | →428 bodies (212 live) | 4.15 / 13.79 | 2.66, p99 7.41 (61.9%) | 5.37 (24.2%) | 197/1800 |

**Gates on this runner:** `behave --law plane` fails wholesale here (G1 "0/256, worst inf" in 0.05 s,
B14 timeout) identically on the untouched base binary and on mine (`behave_plane.txt`): the oracles
return nothing on this cloud runner — an environment defect, not a law regression (HANDOFF, 6 Oct:
G1–G6 pass on the M1; B12's statistic is known miscalibrated; B13 60/64). The claim above rests on
the frame measurements, not the gates.

Mechanism, from the instrumented run (`bench_split_m400`, `split_m400.err`, 600 frames, rtf 100,
M=400): the bodies loop is 3.02 ms of the 3.06 ms gather (98%); the fleet-members loop is ~0.06 ms;
**1.06 readouts per emitter per frame** (the ViewCache memo is at the floor — Newton is not the
cost); per live emitter 11–15 µs. One readout = `state_rate` = one `ramped` per doll level =
`binding_at` history lookup + `decode` → `Trajectory::state` (phase inversion `outbound_at` + table
read) + `credit`, all in checked i128 `Scalar` arithmetic. Paced runs cost ~5× the unpaced loop
(2.38 vs 0.46 ms gather p50 at rtf 1): the player's 60 Hz frame runs cache-cold, so the constant is
memory/branch-state bound, not ALU-bound. The members sweep (rtf 1, unpaced, M 48→400, `--members`
caps at 400) gives the marginals: gather 0.18 µs/member, json 2.0 µs, wire 0.5 µs — members are
read by extrapolation and are nearly free; bodies are the cost.

Reproduce (≤ 60 s each, from the repo root with `cargo build --release -p xtask`; the split needs
the instrumentation patch in `work/` — it is three `eprintln!` lines in `view.rs`):

```
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100            # bench_rtf100
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100 --members 400  # bench_r100_m400
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 10 --rtf 1 --unpaced --members 48   # member slope
```

**Predictions** (`predictions.md`, written before the member/body sweeps): P1 held in kind, missed
in size (bodies dominate the gather; per-member measured 0.18 µs, far under my ≤5 µs; per-emitter
11–15 µs, not ≥60 — my 45 µs average conflated the paced-cache-cold factor with the per-emitter
constant). P2 **falsified** as stated: at the member cap (400, not the 948 asked) the gather stays
0.52 ms because members are extrapolated, not read; the spirit survived through the body sweep
instead (gather p99 7.41 ms and frame p99 13.79 ms at 428 bodies, engine still budget-bound). P3
held (json+wire linear, ~20% of gather at M=400). P4 held (engine share 0.24 < gather 0.62; zero
hitches above 16.7 ms anywhere).

**What would make it wrong.** (i) The M1's gather constant could be much smaller than this shared
x86 runner's (the 5× paced/unpaced gap says much of it is cache state) — but the shares, the 1.06
readouts/emitter, and the O(N_live) scan are structural, not hardware. (ii) If the flight view is
meant to stay a debug instrument replaced wholesale, the readout constant matters only through
whatever inherits its chain walk — the selection argument then applies to the successor unchanged.
(iii) The engine's 197 overflow frames at 428 bodies show the *next* constraint forming: engine
burstiness at rtf × N (event clusters: ship advances 71 µs × 16.7k, player 2 ms each), not engine
average (~1 ms/frame). Cost of adopting: none for the diagnosis; the levers are design changes in
the view (selection by what the eye resolves; a cheaper or shared chain readout), owned by the
plane's builder, subordinated to the engine budget never being starved.

**Fit with PRINCIPLES.** "Compute only surprises" (3): the gather recomputes every emitter's full
chain every frame at 60 Hz; "The view is an instrument" / "the zoom level is the minimap" (28, 5):
the scan ignores what the player can differentiate; "the best part is no part" (17): the JSON
serialises emitters nobody reads in bench. The lens kept me on the measured frame, which is also its
blind spot: this measures the *plane's* frame, not the billion-body engine the board's top risk
(candidate pairs at N) lives in — that constraint is real but not yet reachable by this harness;
today's measured wall is the readout.

**The lens.** Constraint named from `where_the_time_goes_ms` across five configurations plus an
instrumented split; exploit and elevate follow Goldratt's order (the memo was already exploited to
its floor; next is selection, then the constant). Where the constraint moves next: once the readout
is selected/cheapened, the frame's constraint becomes the engine's burst tail at rtf × N (overflow
already 11% of frames at 428 bodies), and at true scale the board's known per-body event work.
