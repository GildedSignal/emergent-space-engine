Working...
Check complete. `check.md` written to the run folder; nothing else there touched (all reproduction ran from a `/tmp/check-quant` copy since `budget.py` overwrites its own output).

**Grade: gold.**

What I did, against the checker brief:

1. **Reproduced** from the dossier's commands (empty `patch.diff`, rebuilt `bench.c`): every decisive cell within ±10% (chase-L4 8T 17.80M vs 17.43M; gather-4 8T 42.86M vs 47.35M; gather-8 26.89M vs 25.63M; resident control 26.2M vs 27.2M); `budget.py` regenerates `budget.json` bit-identically; the N_max arithmetic re-derived independently. Constants verified in shipped code: 64/orbit is `step.rs`'s "1/64 of the tube's radial period" — not a free parameter; 29 µs and 83% are HANDOFF's.
2. **Predictions:** written 11:42:19, before the decisive matrix 11:47:55, smoke cells declared; 6/8 held, the 2 failures honestly reported and diagnosed.
3. **Attacked** with five adversarial cases of my own: footprint sweep (64–1024 MiB, no cliff), L beyond the tested range (L16 — gather goes bandwidth-capped, line rate flat at ~214M/s), concurrent bandwidth load (latency paths unchanged — the walls are genuinely separate), verdict-vs-L robustness (battle fails at every L including L1; only a one-line pure-stream bound escapes), and k=32 sensitivity. The headline does not rest on the unmeasured L=4 assumption.
4. **Novelty:** no prior H entry prices kick-path memory; H0180's "gathers cost more than the arithmetic" is the nearest observation, cited.
5. **Recorded discrepancies:** the dossier's "8.2×" resident ratio is not regenerable from its own `raw.jsonl` (10.7×; my rerun 8.8×) — a re-run quoted without its log, driving no verdict; the stream control is single-sampled and inflatable +70% at 512 MiB (honest only at 1 GiB); the 190-core "corroboration" shares its 29 µs input with the board (arithmetic check, not physics); and "both M1 shifts favour the conclusion" is only half true — 68 GB/s moves the ALL-fail battle cell the other way, though the compute wall and cadence lever survive transfer.

Gold stands on: reproduced, pre-registered predictions held (misses disclosed), a genuine premise correction of the board's blended "10–100×" (belts free today; battles cadence/compute-bound; layout capped at 2.7×), and a rule adoptable in one step by the in-flight `wt/kick` work — with the caveats above stated for the integrator and the blind second checker.
