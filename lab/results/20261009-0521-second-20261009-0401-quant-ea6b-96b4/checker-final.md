Working...
Check complete. **Grade: gold** — written to `check.md`.

**What I did:**

1. **Reproduced everything on a fresh tree** (`a838a28` + `git apply work/patch.diff`, fresh build, ~35 s): all four dossier commands. Digests bit-identical (`dac49af3…` control, `ca74ff5a…` m2000 replay), memo bit-identical, rebind 84.6% legacy / 84.8% engine / 59.0% clock, made 35.4 µs / leavers 80.5, ships_mean 231.7, cadence 1.322×10⁻², cold/warm 1.34× with the same stage ordering. Every number regenerates via `analyze.py`.

2. **Verified predictions precedence** by mtime: `predictions.md` (05:31:45) precedes all decisive JSONs (05:36+). Substantive predictions all held; the failed mean band (79 vs 40–60 µs) was honestly disclosed and correctly diagnosed.

3. **Proved the wrong-path claim from the record itself**: the prior run's saved `stages_total` (`forces_clock_ns`, 0.60 ms total ≈ 12 calls) *is* the clock path at 59.32% — its "(all kicks)" table.

4. **Five adversarial cases**: clean binary at m2000 (patch inert beyond the author's default-args control — digests bit-identical), seed 2 (85.7%), fill level m200 (84.8%, cadence 1.51×10⁻²), m800, and full fresh-tree rerun.

**Two findings the author missed** (flagged in check.md as adoption conditions): `--members` is clamped to 400, so "m2000" is a ≤448-body scene and the bench structurally cannot measure a filled fleet (m800 ≡ m2000 bit-for-bit); and the patch contains one non-instrumentation hunk in `kick_clock` (crash planning → immediate death) — inert on every scene run, but must be stripped if the patch is kept.

Scratch worktree removed; main checkout clean; nothing committed or pushed.
