Working...
Check complete. **Grade: silver** — written to `lab/results/20261019-1316-scout-e828/check.md`, with the author's wiki page corrected in place where it overstated.

**What I did:**

- **Reproduced exactly**: clean tree at base commit c41a9892, applied `work/patch.diff`, rebuilt, reran every regen command — all six stored outputs bit-identical (33 s, 21 MB). Verified the instrument is `arm_pair`'s integer setup verbatim (tier.rs:552–571, same `first_hit` call, same belt class) and that the anchors match e87d's own dossier on its branch. Verified r's synodic leg from geometry (pi²/Δpi ≈ 1.0×10¹⁵ ticks ✓).
- **Attacked beyond the author's grid** (4 cases): widths 1e-5 and 1e-3 (100× span — P=1 column stays exactly 0 on both), κ=2⁻¹⁷ (512× the quantum — saturation genuine at E=2, but the per-kick curve goes flat-to-humped, not falling), fresh seed 12345. The three headline laws (no zero-leak epoch at E≥2; concave saturating first passage; depletion as the protector) survive everything.
- **Found the gold-blocker**: the freeze sentence "≤ 2.6×10⁻⁶ per pair per kick … under the 10⁻⁶-class budget at every E" is contradicted by the run's own table — seed 777's P=1 column per kick is 6.5×10⁻⁶ at E=8 (20 events, CI [4.0×10⁻⁶, 1.0×10⁻⁵]), 3.3×10⁻⁶ at E=64, 1.6×10⁻⁶ at E=256; the E=1024 anchor rides 2 events. Plus smaller letter errors ("seed 1" doesn't exist; mixed-κ quoting between seeds; "nonzero at every P≥16" fails on seed 20261018; armed(16) constant cherry-picked from one seed). P2's pre-registered law died and P6's bound missed by ~4 orders via a 215× unit slip in r — both honestly disclosed, but the gold bar's "held-out predictions held" is not met by the letter.
- **Why silver, not lead**: the measurement is the wiki's named decisive experiment, it resolves the frozen knee-vs-flux contradiction against both toys by measurement, and the churn pricing (355/E cores) is adoptable now with the corrected leak rider. One named experiment from gold: the same surface on the thin-window class with P=1 statistics that aren't 2 events.

Tree restored to base; only `check.md` and the page corrections changed in the run folder.
