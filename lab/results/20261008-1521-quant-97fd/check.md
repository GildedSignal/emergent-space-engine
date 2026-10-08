# Check — 20261008-1521-quant-97fd

Grade: silver

**Abstract (for the integrator).** Reproduced from the dossier's commands in a clean tree (patch applied, rebuilt, 8 fresh runs): the view gather owns the flown frame — 59–71% of summed frame time across four seeds, a repeat, a co-loaded run and rtf 1 (author: 62–69%, 74%); zero hitches >16.7 ms everywhere; engine 19–22%; the unpaced ladder is bit-identical in events/s (163/338/367/552). Order-free reproduces (burn/coast cpu p99 ratio 0.92; all 16 scripted decisions taken). The budget leak reproduces and is worse than reported: every run has engine frames past the 5 ms budget, and fresh seed 424242 hit 15.0 ms (3×) with zero hitches. NOT reproduced: the headline 4.5–6× paced tax — my paced p50 is 1.37–1.66 ms (author 4.20–4.56), view tax 1.1×, engine 2.4×, unchanged under 6-thread co-load; the "~5× capacity overstatement" is box-state, not a stable number. The queue flip is moot: `b-readout-cost` already sits above `q-cadence` in `lab/queue.txt`. Adopt the confirmation and the per-item costs (player 15–20× fleet µs/item, the v2 rebind path); do not price capacity on the tax until re-measured on the M1 with machine state recorded.

## Reproduction (clean tree, patch applied, rebuilt in 28 s)

Commands exactly as in the dossier; all 7 runs plus 3 adversarial cases of my own, every process well under the memory budget. Record quality is the strong part: `analyze.py` regenerates every dossier number from the saved CSV/JSONs bit-for-bit, and my runs regenerate the deterministic content exactly (events/s 163/338/367/552; row counts 1801/1201), so the sim is the same code.

What reproduced, and how robustly:

| Claim | Author | My reproduction |
|---|---|---|
| View gather share, flown point | 65.6/68.8% | 62.2/63.3% (seeds 7, 20261008), 62.9% (fresh seed 424242), 61.0% (exact repeat), 59.4% (under 6-thread co-load) |
| View share at rtf 1 | 74.1% | 71.2% |
| Hitches >16.7 ms | 0 | 0 in all 8 runs (worst frame 9.4–11.6 ms) |
| Engine share | 19.2–21.2% | 19.8–22.0% |
| Unpaced ladder | p50 0.90–1.65, events/s 163→552 | p50 0.96–1.74, events/s identical |
| Order free at p99 | cpu 1.01, engine 0.98 | cpu 0.92, engine 0.88 (burn window verified against `script()`; decisions `logged == taken`) |
| Budget leak (single items >5 ms) | 7 frames, max 10.8 ms | every run has ≥1; max 5.42–5.95 ms (seeds 7), **15.0 ms on seed 424242** — the leak is real and larger than reported |
| Player vs fleet µs/item | 1125 vs 56 (20×) | 736 vs 50 (15×) at rtf 1 |

What did NOT reproduce — the central quantifier:

| | Author | Mine (same box, ~6 min later) |
|---|---|---|
| Paced frame p50 | 4.20/4.56 ms | 1.37/1.66 ms |
| Paced view p50 | 3.25/3.61 ms | 0.85/1.20 ms |
| Paced/unpaced view tax | 4.5× | **1.1×** |
| Paced/unpaced engine tax | 6.0× | **2.4×** |
| Overflow frames | 49/41 | 2/2 |

`cpu_ms` is a genuine `CLOCK_THREAD_CPUTIME_ID` reading (session.rs:15), so the author's "compute, not stalls" is correct *for their run*. But I could not make the tax come back: four unloaded paced runs and one under 6 CPU spinners all sit at view p50 ≈ 1.1 ms. The absolute levels are machine-state-sensitive on this shared box (frequency/SMT/thermal — none recorded; `machine_before/after` are macOS stubs returning "unavailable" on Linux, so the only state record is the uptime string). The kill criterion watched shares, which are ratios and therefore stable — the levels, which carry the tax claim, were unguarded. Conclusion: pacing-vs-hot-loop is a real methodological distinction (engine tax 2.4× in my data), but "~5×" is not an established number, and any capacity pricing built on it would be wrong by ~3× today.

## Predictions

Pre-registration is genuine: `predictions.md` mtime 15:27, first decisive run started 15:27:52 (JSON `uptime_before`), smoke run disclosed inside the file. Scoring: P1 held (twice over — my four extra seeds too); P4 held; P3 honestly reported missed; P5 honestly reported missed and converted into the per-item finding. One generous self-score: P2's side claim counted as "held" at +65% growth against its own ±20% band.

## Novelty

- The view gather as the frame's owner is **already on the record**: H0210's limitations ("the view gather is 83% of a light frame"), H0213 landed the relativistic gather cache (3.6 → 1.2 readouts per emitter), and `lab/queue.txt` line 11 queues `b-readout-cost` *above* `q-cadence` (line 31). The dossier's queue-flip ask is already the state; the board's 1 October focus-list ordering was already superseded. This run's contribution is the first *post-cache, flown-point, fresh-seed* confirmation that the readout still owns the frame — confirmation, not a premise change.
- New, as far as HISTORY and the docs show: the first measurement of foundation 7's bounded-impact claim at plane level (order free at p99); per-kind engine costs flagging the v2 rebind path (player 15–20× fleet per item); the hot-loop-vs-paced control requirement itself; the single-item budget leak with per-frame anatomy.

## Goal fit

On goal (board bottlenecks 3/4 and the focus list's cadence pricing; PRINCIPLES: "Measure the way the player will run it: heat and load are part of reality, not noise to sidestep"). The run prices where the next marginal hour goes — and its robust half says: not cadence, the readout. That is worth one queue-position check, which the queue already reflects.

## The one experiment to gold

Pin the tax: same paced bench with machine state actually recorded and controlled — cpufreq pinned (or `taskset` to isolated cores), on this box and on the M1, three repeats each. If a stable ≥2× CPU-time-per-paced-frame tax survives (my engine 2.4× is the candidate), the capacity-pricing claim becomes adoptable and the hot-loop-control rule lands as a gate; if it vanishes, the dossier's second pricing dies and what remains is the readout-share confirmation plus the secondary findings. Either way one run decides it.

## What the author missed

1. The tax's own reproducibility was never tested — no repeat run, no co-load control, and the "recorded machine state" is empty stubs on Linux; the strongest claim in the dossier rests on the single most contended measurement window.
2. The queue flip was moot — `b-readout-cost` already outranks `q-cadence`; the "should sit above cadence" ask costs nothing because it is already true.
3. `analyze.py`'s burn window misses one burn frame per block (`0 < (n)%240 < 20` drops n=240k, which `script()` does burn) — immaterial here, verified against both windows.
4. The budget leak is understated: 15.0 ms single items exist (seed 424242) — 3× the budget, not 2.2× — and the worst leak frames still present under 16.7 ms only because the rest of the frame was cheap; a leak landing on a full frame would hitch.
5. "71 bodies" — the JSON says 70; trivial, but numbers in a pricing dossier should be copied, not recalled.
6. The gather was never opened (admitted): crossings vs catalogue walk is the split `b-readout-cost` will need, and this run could have handed it the per-emitter cost for free.
