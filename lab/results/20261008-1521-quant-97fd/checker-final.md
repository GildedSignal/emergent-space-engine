Working...
Check complete. `lab/results/20261008-1521-quant-97fd/check.md` written; tree restored to clean; nothing else in the run folder touched.

**Grade: silver.**

**Reproduced (clean tree, patch applied, 8 fresh runs + 3 adversarial cases):**
- The robust half: view gather owns the flown frame at 59–71% across four seeds, an exact repeat, a co-loaded run, and rtf 1 (author: 62–69%, 74%); engine 19–22%; zero hitches everywhere; deterministic content bit-identical (events/s 163/338/367/552).
- Order-free holds (cpu p99 burn/coast 0.92, all 16 scripted decisions taken — verified against `script()`'s real burn window).
- The budget leak is real and **worse than reported**: fresh seed 424242 hit a 15.0 ms engine item (3× the 5 ms budget, not 2.2×), still under the 16.7 ms deadline.
- Per-item costs hold (player 736 vs fleet 50 µs/item — the v2 rebind path flag).

**Not reproduced — the headline quantifier:** the 4.5–6× paced tax. My paced p50 is 1.37–1.66 ms (author: 4.20–4.56); view tax 1.1×, engine 2.4×, and a 6-thread co-load probe does not bring the author's levels back. `cpu_ms` is a true thread-CPU clock, so their "compute, not stalls" reading was sound for their window — but the tax magnitude is box-state (frequency/SMT/thermal, unrecorded: the machine-state fields are macOS stubs on Linux). The "~5× capacity overstatement" pricing would be ~3× wrong today. Their kill criterion watched shares (ratios, stable) and left the levels unguarded.

**Novelty:** the readout-as-owner is already on record (H0210 limitation, H0213 gather cache) and `b-readout-cost` already outranks `q-cadence` in `lab/queue.txt` — the queue-flip ask is moot. New: first post-cache flown-point confirmation, first plane-level measurement of foundation 7, per-kind costs, the hot-loop-vs-paced control requirement.

**Pre-registration verified** (mtime 15:27 < run start 15:27:52); P3/P5 misses honestly reported; one generous self-score (P2 side claim "+65%" against its own ±20% band).

**To gold:** one run — the paced tax with cpufreq pinned / cores isolated, on this box and the M1, three repeats. Stable ≥2× ⇒ the capacity pricing and the paced-control rule adopt; vanishes ⇒ the second pricing dies and the silver's remaining findings carry the run.
