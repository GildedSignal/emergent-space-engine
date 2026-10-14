Working...
Check complete. `check.md` written with **Grade: silver**; the author's `wiki/nladder.md` corrected in place on two overstated cells.

**What reproduced** (runner's regen + my solo reruns): every load-bearing number — the kill arm (69 mints, answered 0, standing 2,025.8 MB = 29.36 MB/mint, walk-all 138/138, capture 11.3 ms/call), the limit-1500 invariant, the 10⁴ arm's monotone 2,227.7 MB standing under the 1,394 MB RSS plateau with the cap never engaging, the 1.0/1.7/1.85/1.9/3.5 sweep points, all crossing arms, both coast digests, and the `2·scan_ns` guard at `universe.rs:1190` in shipped code.

**My five adversarial cases** (one outside the author's domain): 4.2 AU clean (4 candidates, 0 MB — the band's outer edge is real), 1.4 AU clean (892, 0.2 MB — skirt starts between 1.4 and 1.7 as claimed), seed 3 at 2.0 kills with the identical shape, parked coast at 2.0 mints nothing ("saved only by not burning" confirmed directly), and the 2.5 AU kill.

**Why not gold — three record defects, not physics:**
1. The home-burn digest control reads `128d1cd8…`/4,032 encounters here (deterministic over 3 runs), not the claimed `48a29edf…`/4,016 — the arm's known wall-schedule instability, but the dossier claims all four digests bit-identical.
2. The 3.0 AU sweep row (walk-all/99,715) is contradicted by the run's **own regen output**: windowed, 11,184 cand/mint, standing 1,523.1 MB, drain frozen — the memory number holds, the mechanism cells don't.
3. The cited 2.5 AU point is absent from regen.sh and work/ (I flew it; the kill holds).

The one experiment for gold is a corrected, self-verifying record (digest assertions in regen.sh, the 3.0 row fixed, the walk-all region restated as [≈1.9, 2.5] with windowed-skirt edges) — no new physics needed. Nothing outside `check.md` and the wiki page was touched; no commits made.
