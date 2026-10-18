Working...
Check complete. Verdict written to `check.md`, two overstatements corrected in the author's wiki page. Summary of what I verified:

**Grade: silver.**

**Reproduced (my own runs):**
- Base arm, seeds 1/7/42: cut *and* replay digests bit-identical to the stored files **and** to a765's published `bench-clean-seed1.json` anchors (`e622722a…`/`58127f4c…`), traced on its branch — not self-generated.
- `frame_digest`: 8/8 flight digests identical, 8/8 schedule agreement, refused 0, ~21 s wall.

**Adversarial (4, one outside the author's domain):**
1. Seed 1234 (outside {1,7,42}), run twice — bit-identical across processes.
2. Unrecoverability confirmed independently: no `carlson`/`ES_CARLSON` in the tree, pickaxe across **all** refs = 0 commits, both patch files 0 B, and `run.sh`'s `phase()` capture is a session-end tree diff — the exit-trap story is mechanically coherent.
3. a765's base is 24 commits behind HEAD: the anchor's bit-identity survived real main movement — stronger than the dossier claims.
4. Frozen wired files internally consistent (sample sums, clustered 10:03Z stamps, digests differ 3/3, wired-arm 8/8 schedules agree).

**Predictions:** held out before the 10:03 decisive flights; P1/P3/P4 held, P2 killed (0.76× regression) and reported as killed.

**Not gold:** the premise-killing half (exact lever refuted) is exactly the half that cannot regenerate — by the run's own honest demotion. The gold experiment is named: rebuild the wiring from the handoff pieces with a non-reversing regen, re-fly, and the refutation re-earns itself.

**Page corrections (in place):** reconciled the flight paragraph's base band `35.5–35.8` with the dossier/regens (35.1–35.4), and "survive as measurements" → "FROZEN measurements (non-regenerating)" in the Refuted line.
