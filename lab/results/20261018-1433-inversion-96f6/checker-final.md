Working...
Check complete. `Grade: silver` written to `check.md`, the author's page corrected in place.

**What was verified (reproduced):**
- `work/patch.diff` is byte-identical to 7581's published patch minus its appended duplicate — "verbatim, deduplicated" is exact. Applied it myself (the runner's regen had restored the tree), rebuilt, re-flew.
- Every deterministic column matches at all four K (over 0/0/0/33, game_s 898.6/898.6/899.2/747.4, kicks 609/603/606/539, held_max 97/97/97/81, census 87/87 & 73/73 bail→full-walk, binding_at = 1.00·K, λ 0.097/game-s); the 10⁴ control digest `1b5461b0…` equals 7581's gold record; OFF 5×10⁴ = 3.14× game-time contrast. The author's own dump confirms Table 2 to the digit (33/33 over frames, events median=max=2, gaps {15:28, 29:4}).
- `predictions.md` (14:39:57) precedes the decisive dump (14:40:15) and all flight logs.

**Attack (4 cases, all outside the author's range):**
- **K=7×10⁴ and K=10⁵**: capture 194.9/204.8 ns/body (linear holds to 10⁵), 41/41 over frames carry exactly 2 events, max_ev ≤ 29 — the decomposition and the metronome's deletion extend out-of-range.
- **K=10⁵ refutes the pin clause**: the process survives at 1,240 MB hwm where the dossier's arithmetic (216 B × 1.00·K × held 78 + bodies) demands ≥2.2 GB and a kill. The run's own hwm already contradicted it (875 MB of pinned Vecs inside 637 MB total); ~30 *distinct* held scans × 216 B × K fits all six measured hwm points. The pin ranks co-located with the compare-form wall (~6–7×10⁵), not first at 3.5×10⁵.
- **1,200 frames at 5×10⁴**: hwm 637→1,121 MB over +80 arrivals (~6 MB/arrival, held_max 161, latch answers nothing) — the pin is also an unbounded *time* wall at fixed K, which the K-only framing misses; the fix's requirement becomes answer-or-expire, not just delete the Vec.

**Why silver, not gold:** P1/P2/P4 held; P3 reported as held but its pin clause is refuted by the run's own evidence and my flights. The core claim (the 5×10⁴ break is the capture's O(K) bail walk, not the comb; the observer fix must delete the walk, not re-time it) stands reproduced and out-of-range confirmed. One experiment to gold: measure the pin's real multiplier and re-rank the walls (my flights already bound it). Also named: the decisive 50k flight's stdout was not kept (its dump and counts regenerate), and "digest deterministic" overstates at 30k (author `f8573d2a` vs regen `c7f47c26`, counts identical — deadline-coupled).

Tree restored to as-found; nothing outside `check.md` and the page correction touched.
