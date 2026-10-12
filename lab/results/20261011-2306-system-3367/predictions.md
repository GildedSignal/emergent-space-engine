# Predictions (written before the decisive runs)

System-lens question: after the motion law v2 (6 October), does the plane's *measured* cost
structure still match the 14-build autopilot queue (ordered from the 1-October bottleneck list),
and where does a frame's compute actually go? Runs (each ≤ 60 s, Linux/x86, orders of magnitude
only; the M1 re-measures):

- `cargo run --release -p xtask -- universe --describe`
- `cargo run --release -p xtask -- universe --bench --rtf 100 --seconds 30` (paced 60 Hz, the player's loop)
- `cargo run --release -p xtask -- universe --kick-bench --rtf 100 --seconds 30` (pure kick-resolver replay)

Held-out cases and expectations (not tuned on):

- **P1 frame split.** The view (gather + JSON + wire) is still the majority of a paced frame's
  wall time at rtf 100 (H0210 measured the gather at 83% of a light frame before the gather
  cache): engine share < 40%, view share > 50%.
- **P2 kick population.** Fleet members (the "leavers" population in the kick bench) are the
  large majority of distinct kicks; their per-kick resolver cost on x86 is 10–100 µs (29 µs was
  the M1 number in H0210's limitations), same order for made bodies.
- **P3 memo.** On distinct kicks the exact shape memo hits ≈ 0% (five lab runs, and the 5 October
  correction) and the law's quantized 12+12-bit key hits > 80% (taste log: 94.5%); so nearly
  every distinct kick pays a fresh cycle fit.
- **P4 smoothness.** On this shared 8-vCPU box, paced p99 frame < 8 ms and no hitch above 50 ms
  (the M1 benches were p99 2.45–2.72 ms; x86 within ~3×).
- **P5 events.** Kicks dominate the engine's events; the cadence is ≥ 64 kicks per orbit per
  perturbed body (the step is 1/64 of the radial period).

What would falsify the system reading I expect: engine share > 50% of the frame (then the queue's
kick-path order is confirmed and the view is not the frame); or exact_hit_rate > 50% (then the
recompile-per-kick problem is already gone and the re-anchored jet buys nothing).
