# Dossier — 20261009-2257-second-20261009-2212-fermi-a11b-ba64

Second-author pass on `20261009-2212-fermi-a11b` (silver). The checker believed
the physics and not the record; this run rebuilds the record and runs the named
experiment. Nothing here is new physics — it is the same claim, now held by a
record that regenerates, with the checker's four corrections folded in and
tested.

## Claim

The 10⁹-in-8 GB budget is decided by two measured per-body terms on the **hot**
side — **6.9 KB of live compiled state per body** (428× the law's 16 B tube;
4-pt slope agrees with the two-endpoint slope to 0.2%) and **~29–48 µs per hot
event** — with **N_hot ≈ 1.3×10⁴ (this box) to 2.7×10⁴ (M1 kick cost) at rtf 100
today**, a **steady-state** number (the spawn transient runs ~30× hotter), while
**cold** populations are free by a horizon bound (1.143 belt orbits per 100 h at
rtf 100 → 1.1×10⁻³ e-foldings: no scar in play, and a *named hole*: a persisted
universe reloaded across ~10⁴ orbits would scar), and the board's "190 cores"
re-derives as **175**: the unaveraged low-orbit corner at rtf 1 — a regime, not
a property of N.

## Bottleneck

Unchanged from the original (board item 3, H_live risk): a re-ranking. The
memory lever (compiled cycles shared across population members, 428×) stays
~35× bigger than the slack skin's 12.6×; the hot/cold split is principle 33 as
a budget. Zero code to adopt.

## Evidence — the record that regenerates

Every number below is computed by `budget.py` **reading only `evidence/*.json`**
(no hardcoded measurements; repo anchors H0190/H0210/law.md/components-98bc are
the sole constants). Commands, in order (this box, 8 vCPU shared, load ~1;
shipped tree `a838a28`, `cargo build --release -p xtask` 38 s; each ≤ 10 s;
peak RSS 48 MB at the largest run):

```
xtask universe --kick-bench --seconds 5                          # x6 → evidence/kick-bench-{1..6}.json
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 48
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 148
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 248
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 448   # CLI clamps to 400 (mod.rs:32)
xtask universe --bench --rtf 1 --seconds 30 --unpaced --members 48      # transient regime
python3 budget.py                                                # prints every quoted number
```

**Digests match the original run's stored evidence bit for bit** (m48
`09e40859…`, m400 `aadaa1c8…`): same simulation, clean tree, canonical cut.

- **Kick cost, 6 repeats:** medians 46.6–48.8 µs (5 of 6; run 1, cold after
  build, 60.0), p99 59–77 µs, 23 samples, `exact_hit_rate` 0.0 every run.
  Cross-session family on this box: 42–66 µs (author's 41.8, checker's
  44.3–45.3, stored 65.8, this run's 46.6–60.0) — orders-of-magnitude
  conclusions only; the M1's 29 µs (H0210) anchors capacity.
- **Live-store ladder (the missing slope points):** members 48/148/248/448 →
  bodies 71/166/263/410, bytes/body 5189/5687/5959/6564. Monotone; marginal
  slope two-endpoint **6.85 KB**, 4-point OLS **6.86 KB** — the two-point
  estimate was never fragile. 428× (OLS 429×) the 16 B tube; memory ceiling
  today 1.17×10⁶ bodies. bytes/body is read before the cut's settle:
  repeat-stable in-session (5959 = 5959), ~0.1% cross-session.
- **Event rate, consistent full-total aggregation** (all Stats counters /
  game-s / bodies) at the four N: **6.13 / 5.01 / 4.87 / 5.07 ×10⁻²** per body
  per game-s — mildly declining, flat 166→410. The original's 3.9×10⁻² "at 406
  bodies" was a kicks+slices+leavers **subtotal** (3.73×10⁻² here): the claimed
  drop was an aggregation artifact, exactly as the checker read it.
- **Transient regime (the undisclosed dependence, now measured):** rtf 1,
  30 game-s: **1.63 events/body/game-s = 32× the steady state** (spawn window;
  bodies fell 71→39 in 30 game-s at rtf 1). N_hot is a steady-state number; a
  formation event or scene load runs the engine ~30× hotter per body.
- **Throughput cross-check:** at 410 bodies rtf 100 unpaced the box frames at
  p99 10.1 ms (105 overflow frames at the 5 ms budget) — beyond 60 Hz here,
  consistent with N_hot(box) ≈ 1.3×10⁴ on 4 cores. At 71 bodies: frame p99
  2.83 ms, worst 6.4 ms, 0 hitches/hr, rtf median 100.
- **Unchanged derivations** (arithmetic from repo anchors, all re-verified):
  175 cores = 10⁹ × 32.5 / 5400 s × 29 µs, belt cadence 0.03 cores (5.8×10³×
  lower); 10⁹ programs 15.8 MB, 0.026 cores at rtf 100; horizon 1.143 orbits →
  1.1×10⁻³ e-foldings; H_live ≈ 40 bits/game-s (rate measured, ~bits/event a
  disclosed guess); engine per-item ship 61 µs, fleet slice 29.5 µs (box).

## Predictions

`predictions.md` written before the runs (run.log has the ordering). **Held:**
kick medians 40–50 µs (5 of 6; the cold run 1 at 60.0 left the band — reported,
not tuned); slope monotone 5.1→6.7 KB with two-endpoint in 6.5–7.7 KB and OLS
within 15% of it (0.2%); full-total at 410 in 4.5–5.5×10⁻² (5.07) — i.e. the
original's 3.9×10⁻² is an artifact, as predicted; transient ≥10× (32×);
derivations 175 / 0.03 / 15.8 MB / 1.14 orbits. **Nothing broke.**

## What would make it wrong

Unchanged from the original, now with its edges sharper: populations must share
quantized (E, L) keys or the 428× lever and the horizon bound break together
(b-belt-wire's decisive number); ship swarms 10⁶× denser than a belt turn cold
scenes hot at encounter time; gravity-as-news re-derivation would end cold
freedom. Plus the two this pass exposed: the **transient regime** (~30× steady)
bounds what "N_hot today" means during scene loads, and the **persisted-universe
hole** — save/reload across ~10⁴ orbits defeats the horizon bound. Box ≠ M1:
kick 47 vs 29 µs, frame numbers on a shared runner; bits/event unmeasured.

## Cost of adopting, and fit

Zero code, as before: dashboard gains *marginal bytes/body* and *events per
game-second by kind and regime*. PRINCIPLES (3) "Compute only surprises. Cost
follows change and entropy"; (24) "The memory floor is information"; (33) "An
ant cares about a raindrop but the lion does not"; (10) "Measure before
claiming."

## The lens

Second authorship sees the checker's numbers before running, so my predictions
test regeneration, not discovery — the honest test here was whether *my* runs
reproduce *their* families (they do, and the digests match the original's).
What regeneration still cannot fix: this box's shared-runner timing spread
(42–66 µs kick medians across sessions) means any single-session µs quote is
soft by ±25%; only the digest-exact counters (stats, bytes) are hard.
