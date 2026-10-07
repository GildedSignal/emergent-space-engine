Working...
Check complete. **Grade: gold** — written to `lab/results/20261007-1234-second-20261007-1106-fermi-443e-d57e/check.md`.

**What I verified:**

- **Reproduction, exact and cross-run:** patch applies clean (6.9 s build). The decisive belt run's log is identical modulo wall lines and its `.bin` bit-identical; the plane stream is bit-identical to *both* the folder's `plane_regen.bin` and the parent silver run's committed `hlive_deltas_s3600_seed1.bin`; `fermi_belt.py` regenerates its table byte-for-byte and I re-derived the anchors by hand (belt 2,562 B/s at 10⁹; all-inner 79.3 MB/s = 756× under 60 GB/s). zlib: 9.0/9.0/12.5% — the "split" prediction tally is exact.
- **Pre-registration real:** `predictions.md` (12:48:00) precedes every decisive artifact, after only the smoke test.
- **Four adversarial cases:** fresh seed 3 at 2 orbits (rate +1.4%, ratio 1.06); M=0 run → handoffs exactly 0, confirming the law-v2 doll-0 fact on the engine and in `step.rs:399`; 5-orbit probes → the author's ~1.5 GB memory kill reproduces (my RSS plateau: 1.49 GB); code audit of `maybe_capture` and `prune`.
- **Novelty:** closes exactly the experiment the parent silver's checker named; no prior entry measures the belt binding stream or handoff re-reference path.

**The one flaw costing a correction, not the grade:** the dossier's mechanism sentence ("`prune`'s `oldest − 2²⁶` floor keeps everything") is contradicted by `universe.rs:971` — the `min` makes that term prune *more*, never retain. The retention phenomenon is real (I reproduced it) but its site is unidentified; also the memory kill is run-span-dependent, not binding-count-dependent (628k bindings at 2 orbits = 0.19 GB).

Repo state: tree restored to HEAD (`hlive` examples removed via reverse-apply), scratch in `/tmp/checker-scratch/`, no commits, no stray processes.
