# Check: rung r1, run 20260929-1857-rung-r1-rings-c7b9

**Verdict (verdict.py on my metrics-check.json): VOID — the metrics are incomplete.** The author's session exceeded its deadline mid-run: no `dossier.md`, no `predictions.md`, no top-level `metrics.json`, no picture. `work/` holds a complete C implementation of all seven configurations plus oracle ports, the seeds, and one finished config (`river-m32`, failing every criterion). No configuration can pass or be killed on this run.

## Reproduction

- I recompiled `work/rung_r1.c` unmodified (`gcc -O2`) and re-ran `river-m32`: `work/metrics-river-m32.json` reproduces **byte-identically**. `river-m16` and `tiltonly` (my runs, same binary logic): both fail every criterion (`tiltonly` misclassifies 5 captures). All three are in `metrics-check.json`.
- `binet-m8`, `binet-m16`, `binet-m32`, `square` each exceed 400 s (killed; no metrics written) — over the lab's ≤ 60 s norm by ~7×.
- Seeds: regenerated from the frozen sampler (Random(20260930), same draw order and rejection) — 256 bound / 64 light, first values match `work/seeds.json`.

## Oracle ports — verified

`ellip_k` (AGM), `ellip_k_minus_half_pi` (series switch at 0.25), `periapsis_elliptic`, `gauss_legendre`, `deflection_quadrature` (root-factored, 64×GL32), `bound_constants`, `bound_period_quad` (integrand dφ·r²/L·E/(1−2/r), 16→2¹⁴ piece doubling) all match `xtask/src/gr_oracle.rs` / `gr_oracle_extended.rs` line-for-line. Selftest cross-checked by hand: periapsis(20,0.5)=1.2339 (my independent evaluation: 1.2341), null turning b=10 solves r³/(r−2)=100, light tail 2·10⁻⁴/10⁻³=0.2, capture patterns 111000 / 1100 (separatrices L=4, b=3√3). **The oracle is correct.**

## Implementation audit — three defects against the frozen spec

1. **Binet band index inverted on outward crossings.** Bands are u ∈ [2^{−(k+1)/m}, 2^{−k/m}); leaving through the low-u edge (`EV_OUT`) requires `k++`, but the code does `k--` (`rung_r1.c:286`). Traced on seed 0 (p=84.25, e=0.441): the first `EV_OUT` at u=0.0170392 lands the orbit in band 186 = [0.017412, 0.017794], which does not contain u; the orbit then oscillates inside the wrong band (u_min = 0.0063487 = up−R of band 186; Δφ = 3.1523 = that band's local half-period) with **zero** crossings per cycle — impossible for a genuine p=84 orbit spanning ~45 m=32 bands. Every Binet number (had the runs finished) would be invalid. The >400 s timeouts come from later phases where the `EV_STALL` nudge path (`continue` before the φ-cap check) loops without bound.
2. **River `dt` integrand wrong by a factor γ.** From H = γ + β·p_r with β frozen per ring: dr/dt = σS/γ, so |dt/dr| = γ/S = (H−σβS)/(ob·S). The code returns g²/(ob²S) (`rung_r1.c:317-323`). Flat-space check (β=0, E=2, L=0): true dt/dr = 2/√3; the code's = 4/√3. Periods for river configs are inflated by γ — `period_pass_fraction` measures the bug, not the model.
3. **Median fabrication.** `median_cross = cross_counts[128] > 0 ? cross_counts[128] : cross_counts[130]` (`rung_r1.c:1035`): when most seeds fail, index 130 is reported. `crossings_per_cycle = 1.0` for river-m32 is this artifact, not a measurement. Also, the river flow is frozen at the ring's geometric centre (2^{(k+0.5)/m}) while the rung's literal β_k = −√(2/r_k) samples the inner edge — a defensible reading, but it changes the numbers.

## Adversarial checks of my own

- **Independent river reimplementation** (spec-literal edge sampling, brute-force r-stepping): at m=32 the advance for p=20/e=0.5 is +0.26 vs GR +1.234; p=84.25/e=0.441 gives a **retrograde** −0.61 where GR gives +0.237; p=10/e=0.7 explodes to 562 rad per cycle (staircase chatter near the strong-field rings). So the river model itself genuinely fails `prec` and `prog` at m ≤ 32 — the author's zeros are directionally right even though contaminated by defect 2/3.
- `tiltonly` (negative) fails every criterion, as required. `square` (negative) times out — no verdict possible from it.
- Binet core math (local rotation/hyperbola, continuity of u, u′, dt rule) matches the rung's spec; only the index update is broken.

## What the author missed

No dossier, no predictions, no picture — the deadline hit first. The one completed config (river-m32) was reported through a broken median and a broken dt rule. The Binet inversion is a one-character fix (`k--` → `k++`) but invalidates the rung's centerpiece; the next run should fix defects 1–3, bound every loop by the φ cap, and re-run all seven configurations.

Machine note (cloud container, Linux x86, 4 vCPU): orders of magnitude only. My `river-m32` re-run overwrote `work/trace-river-m32.json` (deterministic code; the metrics file reproduced byte-identically, so the trace is expected unchanged). My scratch binaries and my `river-m16`/`tiltonly` metric/trace files were removed from `work/`; their numbers live in `metrics-check.json`.
