Working...
Check complete. `check.md` written; grade **silver** — agreeing with the author's self-grade, but on sharpened evidence.

**What I did (30-min window, one check.md, nothing else touched):**

**Reproduced bit-for-bit** — the strongest part of the run:
- `analyze.py` regenerates `summary.txt` exactly; the empty `patch.diff` matches "no code edits"; `predictions.md` (03:57:43) predates every data file (03:58:09–04:12:48).
- Fresh determinism runs: repeat = threads8 = `f8b75cec…`, seed2 = `d38063b3…`, mem768 = `3db02d3d…` (under a *different* machine load than the author's), rtf1000 = `f0684ddb…` — all digit-identical to the stored data.
- H_live saturation: fresh 30,000-game-s run, last-third RSS drift +4 kB, zero major faults. The HANDOFF "not measured yet" risk is genuinely closed.
- Gather share 0.58 → 0.60 across sessions; `--members` cap confirmed in code (`clamp(4, 400)`).

**Where the attack landed:**
- The headline magnitude is contention-bound: at the same 428 bodies on a quiet box (load ~1.6), gather max is **6.72 ms with 0 hitches/hr** vs the author's 23.25 ms / 1920/hr under load 3.9–5.0. Six artificial CPU spinners bring it back (19.0 ms). The ladder's own embedded uptimes span 1.19–5.01, which the author's own kill criterion calls noise — and "contact-cascade chaos" was asserted where load history is an unexamined confounder.
- `where_the_time_goes_ms` is `Instant::now()` wall time (session.rs:99) — the "excludes descheduling" caveat sits on `frame_cpu_ms`, so the 23.25 ms figure mixes compute with contention.
- What survives attack: the *structure* — the budget clips the engine term while the unbudgeted gather's tail is free to inflate, the current violator of plane.md §7's own words ("…or a gather").

**Novelty:** gather dominance was already in H0210's limitations ("83% of a light frame"); new here is the H_live closure, the canonical-cut determinism re-controls, and the median-moves-3.15×/tail-stable-1.66× seed structure. No 10× move, no deletion — hence silver, one experiment from gold: a contention-controlled ladder (M1 or core-pinned, CPU-time attribution) at 300–500 bodies × ≥8 seeds.
