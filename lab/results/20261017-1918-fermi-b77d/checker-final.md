Working...
Check complete. **`Grade: silver`** — written to `lab/results/20261017-1918-fermi-b77d/check.md`, with four corrections applied to the proposed `wiki/memory-h-live.md`.

**What reproduced** (three independent load events):
- Runner's regen (3rd regime, loadavg 3–8.5): ladder 7-way starves (held 369–378, 64 kB/scan), crowd pins 503 B/catalogue-entry at 0.0969 held/game-s, quiet arms flat.
- My deliberate 9-way spinners (loadavg 12.6): held 422, **76 kB/scan**, 0.0966 held/game-s, RSS monotone +30 MB — closes the dossier's own "ambient, not controlled" objection.
- My B3L at N=1e4: 67 kB/scan — near-set confirmed downward, belt-proportionality dead; the "no 10⁹ consequence on spread belts" half stands.

**What broke** (my K=2,400 arm, outside the author's range): pin = **5.0–5.8 MB/held-scan ≈ 2.2–2.5 kB/entry** at 2,294 entries — 5–6× the claimed constant. "One law ~0.4–0.55 kB/candidate on every scene" is falsified at the next decade, and was already contradicted by 7bd9's own 1,600-member entry on the page the author folded in. Consequence: 8 GB busts at ~2×10³ candidates, not 8,500, and the proposed `candidates × 475 B` byte fence undercounts ~5× — the fence must measure pinned bytes at capture. Also: the quiet-crowd freeze is bimodal (2 of 3 flights; the regen's C1 drained at held_max 1), and the author edited a historical run id (`0e4d`→`0e9d`) that matches no branch — reverted.

**Gold path named:** crowd arms K=1.6×10³–10⁴, pin counted in real bytes at capture, paced per-frame loop — then the byte fence is measured, not modeled, and adoptable in one step.

The honest self-refutation (P2/P3 killed by its own regen, reported in a dated postscript) is the run's best property; the headline law simply claims more domain than it flew.
