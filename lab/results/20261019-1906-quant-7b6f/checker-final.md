Working...
**Grade: gold** — `check.md` written; the author's page corrected in place.

**Verdict:** the claim reproduces bit-exact and survives every attack, including a rung above the author's grid.

**Reproduction** (clean tree at `07bc5379`, patch applied, `regen.sh` exit 0 twice): arm A's census digits identical across both regens — guard f=22101, 1,619 MB, held 171, scan_cand 9,846,528, hist 106,309; fence arm completes 72,000 frames = 120,000 game-s at 635 MB with HWM = end rss. The instrument is code-verified: `same_inputs` Arc reuse re-pushes the same scan, so 224 B/cand over-counts by the known ×2 entries law (measured fresh at 2×10⁵: 1.92×).

**Attack (3 fresh arms, 2 outside the grid):**
- 2×10⁵ shipped — guard 20,638 gs; scans ≈96% of window growth; `cand_max` 199,715 = exactly 2× the 10⁵ pin. The wall is K-scaled scans, not kicks.
- 2×10⁵ TTL=16 — channel deleted, flat ~1.0 GB past 58k gs, residual **−0.12 KB/kick**. No per-kick memory law one rung up.
- 5×10⁴ — 49,715 / 54.0 MB/1k gs, exactly K-linear between 3×10⁴ and 10⁵.
- New: at 2×10⁵ the first kick wave costs **1.2–1.3 s frames** — the next wall at that rung is compute, not memory.

**Predictions:** P1/P2/P5 held; P3/P4 failed on letters, held in substance — both disclosed, both the history channel's wave steps (the registered P4 residual forgot to subtract hist). Per H0183, diagnosed, not hidden.

**Corrections to the page:** the end-ledger's 2.1 KB×hist term double-counts Segment bytes already inside `store_mb` (`bytes_of` counts history, body.rs:196), and this tree's per-binding cost is 1.3–1.9 KB — honest machinery bound **≲0.15 KB/kick** (still ≥35× under 3eb3's killed 5.3–9.9 band); the identity's split digits are schedule-elastic.

**Novelty:** kills the same-day 3eb3 reading ("the wall is kick machinery, the 10⁵–10⁹ premise inverted") with a direct census plus falsifier arm — the scan channel at 10⁵ was known, the decomposition and collinearity diagnosis are new. Tree restored clean; runner's logs restored; nothing committed.
