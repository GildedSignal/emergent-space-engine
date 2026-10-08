Working...
Check complete. `check.md` written to the run folder; tree restored to pristine.

**Grade: silver.**

**Reproduced** (patch applied, clean tree): unpaced gather p50 0.723 ms/share 0.675 (author 0.718/0.674), 428 bodies 2.69 ms/share 0.591, rtf 10⁴ engine share 0.559 with 25,578 kicks (author 25,598), quiet rows 82.7/80.5/84.6% — identical to 0.1 pp, kick median 35.15 µs.

**Adversarial (5 cases):**
1. **Pacing artifact confirmed with its trigger** — cool CPU: vg p50 3.70 ms (4.8× inflated, matching the author); warm CPU (paced run right after benches): 0.72 ms, no inflation. Shares stable at 0.69–0.70 both ways, so the author's idle-down cause and "judge shares" remedy both hold.
2. Seed 7: quiet 88.1% — robust, not cherry-picked.
3. Stricter quantum (0.02°/2×10⁻⁴, ≈4K): fleet quiet halves to 49% — the "~80% deletion" is the 1080p best case.
4. rtf 10³: gather 0.643 vs engine 0.294 — crossover narrows to 10³–10⁴, inside the author's bracket.
5. `--members 800` yields only 410 live bodies (fleet saturation) — the claimed 1,500–2,700-row ceiling is extrapolated beyond the measured ~430-row regime.

**Why not gold:** the gather's dominance is H0210's recorded limitation ("the view gather is 83% of a light frame") with the cache ordered and built in H0211 — the dossier never cites these; predictions held 2/4; the row-cache lever is proposed, not built; realized gain is ~2–3× on the frame, not 10×.

**Gold experiment:** build the row cache beside `ViewCache` and gate it — served view within one display quantum of full recompute across seeds, rtf 1/100/10⁴, at both 1080p and 4K quanta (fleet at 10⁴× and 4K are the weak cases).

**Missed by the author:** H0210/H0211 citations; the quiet metric bounds only `direction`+`shift` while a `Seen` row carries seven more fields (upper bound, not a hit rate); threshold sensitivity; members saturation; `tail_view`'s broken CPU meter (reads 0.000).
