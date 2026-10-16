Check complCheck complete. **Grade: silver** — written to `lab/results/20261016-1835-inversion-de18/check.md` (abstract 107 words), with `checker-final.md` and the author's page corrected in place; tree left pristine.

**What held (gold-quality):**
- **Reproduction exact** — applied `work/patch.diff` myself at base c9657cd1; `regen.sh` output byte-identical to the author's `regen.log`. Mechanism confirmed statically (pristine `apply()` writes `git merge-file` stdout unconditionally; `summary()` returns `<<<<<<< main`).
- **Production-faithful** — verified `glm-lab.yml:98` applies the *whole* results dir each publish, so the crafted replay's re-apply amplifier is the real shape, not a strawman.
- **Predictions pre-registered** — mtime 18:41:59, before every instrument script (18:42:30+); P1–P5 held, held-out items at-least-as-bad.
- **Novel** — `wiki.py` has two commits, no HISTORY entry; the compounding and its fix are new.
- **Beyond the author's range, in the patch's favour** — 6-publish replay stays at zero markers; content cross-check pristine-vs-patched: zero lines lost; multi-section conflicts clean.

**What cost the gold:** `defuse` closes each conflict at the first `>>>>>>>`, so interleaved nested damage (exactly what pristine apply produces) leaves orphan `=======`/`>>>>>>>` lines. On a copy of the **real** `nladder.md` (the 145-run page), heal leaves 2 orphan marker lines; crafted interleaved states let a patched apply write markers back. P6's "zero markers" passed only because the author's instruments grep `<<<<<<<` exclusively — the verification instrument shares the code's blind spot (agreement ≠ independence). One small named fix — pair/strip orphans, count all three marker lines — from gold. Page corrections: "nesting cannot survive" qualified, residual added as open direction 3; dossier's "3 of 26" is actually 3 of 25.
