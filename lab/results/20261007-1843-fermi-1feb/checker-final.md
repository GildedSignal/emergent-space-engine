Working...
Check complete. `check.md` written; nothing else touched, no commits.

**Grade: silver** — `lab/results/20261007-1843-fermi-1feb/check.md`

**Reproduction (clean tree at a838a28, empty patch, fresh 40 s build):**
- Both bench digests **bit-identical** (`6ce636fa…`, `13cfe88b…`); memo counters exactly equal (663 rebinds, 0.0 exact hit rate, 93.2 % quantized); `budget.py` regenerates every dossier number exactly (532 cores vs board's 190 = 2.8×, 13.6–108 game-s fills, 37–292 MB/game-s). Timings within shared-box noise (35.2→39.1 µs).
- `predictions.md` (18:47:39) precedes all run artifacts (18:48:27+); misses reported by name (leaver kicks 9× out, bytes 12.6× out) — honest held-out discipline.

**Adversarial findings (4 runs of my own):**
1. `--members 0` belt rate 0.0155 vs 0.0151 — the belt-like extraction is valid; battle terms dominate the total, confirmed.
2. `--members 1000` / `--seed 7` — belt rate holds at 0.024/0.025 (~2× scatter; seeds scatter more than the members the author varied).
3. `--rtf 1` — slices are **per-frame** (600 in 600 frames; per-slice cost flat 47–49 µs from 71→417 bodies), so k_hot conflates a per-frame term with a per-body term: ×10⁹ overstates hot compute ~2×. Belt-like row unaffected; compute-first ranking robust either way (1.6×10³ core-s/game-s today vs ~6 available).
4. rtf pacing quality (lowest 1 % 58, 21 overflows) is box-load artifact; my quiet rerun gave ≈100 and 5 with the same digest.

**Why silver, not gold:** reproduced and honest, but it *sizes* board items 3 and H_live without moving either 10×, one headline bracket has the slice conflation, and the reabsorption requirement scales with an assumed 16–64 bits/scar. Gold experiment: measure actual scar bits per kick on the shipmem belt ladder (B18b) and re-derive both binding numbers from measurements.
