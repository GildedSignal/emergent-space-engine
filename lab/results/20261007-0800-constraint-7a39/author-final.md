# Author fiThe frame's one constraint on main is the readout, not the engine (engine 5% of frame CPU, view 95%), and deleting the per-frame `serde_json::Value` tree — a byte-identical wire pinned by a test, with identical digests — cuts the paced frame p50 3.31→0.71 ms and p99 5.19→1.07 ms, leaving the light-cone crossing readout (~9 µs per emitter, 88% of what remains) as the named next constraint.
ext constraint.

Full evidence and commands: `dossier.md`. Predictions were pre-registered in `predictions.md` and held (one informative miss, reported). Patch: `work/patch.diff`.
