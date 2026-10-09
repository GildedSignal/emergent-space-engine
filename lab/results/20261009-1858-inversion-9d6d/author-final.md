Working...
Run folder complete: `predictions.md` (pre-registered, P1–P8 held, P9 held on p99), `evidence.jsonl`, `dossier.md`, and the frozen experiment source at `crates/encounters/src/bin/rank.rs` (captured as a patch by `run.sh`). Machine state recorded in the dossier (8 vCPU shared, load 1.3–2.2, each command ≤ 30 s, < 100 MB).

**Claim:** the gold's phase-neighbour certificate is only zero-miss if its neighbourhood k scales as κ = m·E|Δn|·H/W (fleet size × synodic drift × window ÷ phase spread) — rank 4, measured on a 300-ship fleet (κ = 0.75), misses 51% of encounters at 1,200 ships and 80% for a bunched 600-ship fleet on the same orbit, while a κ-scaled certificate stays encounter-linear (encounters ∝ m², 2,130 → 30,168).
