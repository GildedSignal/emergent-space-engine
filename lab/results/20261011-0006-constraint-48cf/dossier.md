# Dossier — 20261011-0006-constraint-48cf (lens: the constraint)

**Claim.** On main (a838a28) the plane's constraint has moved off the engine's kicks to the **readout**: the view holds 55–79 % of every measured player frame, and at goal scale the only existing scale readout (galaxy density render, 10⁹ ships) runs ~2× over the 16.7 ms frame budget at every zoom and resolution, with cost independent of change — a tick, by PRINCIPLES #14 — while the engine (p99 ≤ 6.6 ms at 100×) and the store (104–224 MB for 10⁹ ships) fit their budgets everywhere measured.

**Bottleneck.** The board's #1 since 1 October is "fewer kicks per orbit". Measured today, kicks are not the frame holder: at rtf 100 the engine is 21–25 % of the frame (p50 0.27–1.03 ms) and view_gather alone is 55–66 % (p50 2.4–5.0 ms, ~12 µs per live body per frame). At goal scale the render is 26–37 ms median (all 200 frames > 16.7 ms) for 960×540. Expected gain from a surprise-driven readout: it deletes the single over-budget component — ~10× on the goal-scale frame — and it is the only measured item already *over* budget. Nothing else measured is over budget today.

**Evidence** (Linux/x86, 8 vCPU shared, load 0.8–3.8 recorded in the JSONs; orders of magnitude only).

| Instrument | Result |
|---|---|
| `universe --bench --seconds 30` (rtf 1, 39 bodies) | frame p50 3.31 / p99 4.78 ms; engine share 5.0 %; view 95 % (gather 74 + json 15 + wire 6) |
| `universe --bench --seconds 20 --rtf 100` (71 bodies) | p50 4.53 / p99 11.2 ms; engine p99 5.91 ms (budget 5); view_gather p50 3.53 ms (66 %) |
| `--rtf 100 --members 480` (419 bodies) | p99 18.1 ms — first break of 16.7; engine p99 6.63; view_gather p50 ~3.4 (59 %) |
| `--rtf 100 --members 4800` | live bodies stay ≈ 417 (fleet keeps the rest as programs: bytes/body 6233); p99 15.1 ms; view_gather share 55 % |
| `universe --kick-bench --rtf 100` | kick 75.8 µs median / 370 µs p99; **exact memo hit 0.0 %** (1125/1125 distinct shapes — every kick recompiles); quantized memo 95.5 % (known law change, 5 Oct) |
| `galaxy --bench` (10⁹ ships, 10⁶ tubes) | store peak RSS 104.6 MB; compile 0.41 s once; render median 32.3 / 36.9 / 26.2 ms (far/mid/deep) at 960×540, 4 threads, ~19–22 ns/sample; over_16_7ms = 200/200 |
| `galaxy --bench --rtf 100` (**P1**) | 10× less motion, same 60 Hz pace: far median **37.1 ms** (vs 32.3) — cost does not track change. Prediction held (±20 % band) |
| `galaxy --bench --w 480 --h 270` (**P2**) | ¼ pixels: median **17.8 ms** (−45 %), samples 1.71 M→0.68 M, ns/sample 19→26. Prediction (−<40 %) **failed**: samples are themselves pixel-coupled, so even ¼ resolution sits at the whole budget; at 1080p the same view extrapolates ~60+ ms |
| `galaxy --bench --ships 1e8 --tubes 1e5` (**P3**) | RSS 219 MB (allocator/load noise; both runs ≪ 8 GB), render 22.1 ms — samples fall sublinearly (family arcs dominate at low tube counts). Store is not today's constraint; "render ∝ tubes" is not clean and is not claimed |

Gates on the same tree (context, shared-box caveats): `behave --law space` G1–G3 PASS. `behave --law plane`: **B11 judged nothing in 0.00 s** — the Plane adapter implements no `binary_cycle`, so the trait default refuses every sample (unjudged, not failed physics); B12 FAIL (statistic known miscalibrated, redesign in flight); B13 60/64 (worst 2.12e-2 vs 1e-2); B14 hit the 60 s limit *while my benches ran on the same box* — that number is contention-tainted and needs one clean rerun before anyone quotes it.

Reproduce (each ≤ 60 s, binary at `/home/glmlab/lab-target-2/release/xtask`, i.e. `cargo build --release -p xtask` with `CARGO_TARGET_DIR=/home/glmlab/lab-target-2`):

```
xtask universe --bench --seconds 30
xtask universe --bench --seconds 20 --rtf 100
xtask universe --bench --seconds 20 --rtf 100 --members 480
xtask universe --kick-bench --seconds 30 --rtf 100
xtask galaxy --bench
xtask galaxy --bench --rtf 100
xtask galaxy --bench --w 480 --h 270
xtask behave --law plane --gates B13
```

**What would make it wrong.** The galaxy render is a debug god's view (world frame, positions now), not the player's light-cone instrument; if the player's actual 10⁹-body readout is a different, already-cheap path, the "readout is the constraint" claim dies — but no such path exists on main today (the plane's view is measured at ≤ 417 live bodies only). Also: x86 numbers; the M1's 4P+4E will not be faster. The engine could retake the frame if the fleet's surprise rate at scale exceeds ~50 kicks/s/core (not measured here).

**Fit (PRINCIPLES).** #14 "no work for no reason, so no ticks" — the render pays full price per frame for a 10×-smaller change (P1, measured). #3 "compute only surprises… clocks, redshift, views" — the view is named in the principle and is the one component off budget. #1 "the cheapest compute is compute not done". Cost of adoption: the render must become deposit-delta driven (re-splat only tubes whose pixel bucket changed this frame; the map at galaxy zoom changes on orbital timescales), with the image digest as the kill criterion — same digest at ≤ 1/5 the median, or the representation is wrong and a per-doll mip pyramid drawn once is the next candidate. This is the queue's "readout's cost" build: these are its numbers.

**Where the constraint moves next.** Once the readout stops holding the frame, the engine's kick path takes it: p99 5.9–6.6 ms against the 5 ms budget at 100×, every kick a full cycle recompile (0 % exact memo hits, 75.8 µs). After that, distinctions per game-second (H_live) decide the 8 GB.

**The lens may have made me miss:** the allocator/smoothness interplay (I measured shares, not slack scheduling); single-machine x86 timing; and I did not measure the encounters tier at scale at all (the board's top scaling risk, O(N²) candidates) — if encounters cost more than the readout at 10⁹, this dossier names the wrong constraint.
