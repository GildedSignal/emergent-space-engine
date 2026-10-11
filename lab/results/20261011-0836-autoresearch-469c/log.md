# Autoresearch log — artifact: the plane's kick resolver (`xtask universe --kick-bench`)
# Metric: median µs per leaver kick (board focus #1: kicks dominate the engine's cost). Behaviour constraint: replay digest bit-identical.

## Machine
Linux x86, 8 vCPU, load ~1 (4 sibling lab runs), no perf/valgrind (perf_event_paranoid=4). Orders of magnitude only (cloud timing rule).

## Baseline (seed 1, rtf 10, 30 s; 5 runs)
leaver median 120.1–121.5 µs (±0.6%), made 35.5–40.3 µs, p99 390–518 µs, digest adc434a4…, refused 0. Instrument: repeatability ±0.6% — good enough to resolve ≥2%.

## Phase attribution (feature `profile`, +40% overhead, shares valid)
- kick.rebind 86.6% of kick time (bind 79.9%, old-tau readout 7.2%)
- inside bind: OrbitShape quadrature (shape.bound) 57.3%; Passage::compile 493 µs/call × 60 = 36% of ALL kick time; fit.key 5.6%; decoded_event 4.8%; decode+turn 4.6%; at_radius 1.5%
- quad variant split: 105,948 weak / 11,861 general / 0 fast panels; ~166 panels per bound
- kernels (num.rs: cos, atan, isqrt, div_word) already u64/u128-tight; no ≥10% micro lever found in them
- exact shape-key memo hits 0% (272 rebinds, 272 distinct shapes) — confirms the 5 Oct taste log; the quantized memo would hit 83% but is a law change (changes orbits)

## Round 1 — hypothesis: `node()` recomputes cos(psi) via `self.x(psi)` although the identical value is already computed
- Change: use the in-scope `xr` (identical i128) in the horizon term. General path only.
- Result: leaver median 119.5–120.9 µs (3 runs) vs 120.1–121.5 baseline: ~0.8% (noise-adjacent). Digest unchanged. KEPT (strictly less work, bit-identical), but <10%.
- Structural read: no micro round can reach 10% (kernels tight, quad already branch-specialised). Stop per the lens rule (three rounds would each gain <10%; the attribution already shows the ceiling).

## Rounds not taken (recorded for the next run)
- Passage::compile at 493 µs/call is 36% of kick time for 60 calls: the slack-skin build (b-encounter-skin, in flight) is the structural lever this measurement confirms.
- rebind.old_tau does two full tube readouts per kick (orbit_state(t), orbit_state(event_time)); a cached last-readout is a behaviour-risky change (needs its own run).
