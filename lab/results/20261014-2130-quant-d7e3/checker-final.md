Working...
Check complete. `check.md` written to `lab/results/20261014-2130-quant-d7e3/`, the author's wiki page corrected in place, tree left clean at base `e421ee7`, patch still applies.

**Grade: silver.**

**What reproduced** (regen + my own reruns from a clean tree):
- Control digest `c2b834bb…` bit-for-bit, both arms, kicks 225,949 / encounters 1,624 — 38bf's record, twice.
- 10³ in-band digest `ad8a0e78…`; the 5×10⁴ RSS/held trajectory to the MB (~6.5 MB per held scan); OOM both arms at 10⁵/2×10⁵ (11.0–12.2 GB peaks). The patch is default-neutral by construction and the scene differs from shipped `plane_extra` only in the player's orbit spec.

**What the run's own regen contradicted** (corrected on the page): at 5×10⁴ both arms *completed* — exit 0, digest `0898731…` **identical across arms** — so "every N ≥ 5×10⁴ dies" and "no in-band digest exists at any N ≥ 5×10⁴" are overstated: that death is box load, not an engine constant, and the cap's digest certificate does extend in-band at 5×10⁴. "The cap delays the death" also flipped ordering in regen; only pull-independence is law.

**My adversarial arms:** seed 7 at 10³ (P3, never completed by the author) clean; a full through-the-wave 10³ flight (the author's arm settled the wave off-screen) clean with held saturating at 82 — demotion works at 10³, so the accumulation's onset sits between 10³ and 10⁴; N=10⁴ (a hole in the ladder) completes at 1.36 GB with peak ratio 5.05× for 5× the bodies — per-scan standing ∝ N confirmed at a second point. Also folded in: at 5×10⁴ in-band both arms run 606/607 frames over 12 ms (max ~201/209 ms, mostly outside the wave window) — the cap does not tame the in-band frame seam, which the dossier missed because its arms died before printing.

**The one experiment to gold:** a census build pricing one held scan's standing contents in-band at 5×10⁴, turning the 6.5 MB/scan rate into a measured term and deriving the guard the pending bf21/38bf merge needs.
