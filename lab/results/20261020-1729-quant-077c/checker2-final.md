Grade: gold**Grade: gold** — `check2.md` written, page corrected, tree clean.

**Reproduction (independent, from `work/patch.diff` + regen exit 0):**
- Plane `--kick-bench`: compile **90.1%**, wall 149.0 µs, digests bit-identical audit-on vs off (print-only confirmed).
- Belt (regen): compile **44.6%**, wall 18.2 µs at my load vs author's 15.95 — shares stable across a ~15% wall shift.
- Grid: compile e-monotone 3.39→46.94 µs at r17 (13.8×), stack flat ~8.2 µs, **crossing between e 0.2 and 0.4** — the dossier's e ≈ 0.2.

**Adversarial (blind, one per class):**
1. N=10⁵ belt (next decade): compile **42.0%**, 415,454 calls — N-flat holds.
2. Burn arm (named held-out): compile **49.2%**, readouts 27.5% > fit 22.6% — regime survives.
3. Pristine-tree probe, radii 5/12/23, e to 0.995: monotone tail extends to **66.6 µs at e 0.95** (into a765's 52–65 µs band); e 0.99 cells die in **state generation, not the key domain** (dossier mechanism wrong, immaterial).

**Two corrections made to the author's page:** "off = shipped bits" is false at the letter — the patch leaves five unconditional `Instant` reads per `from_state` call even audit-off (~0.2–0.3 µs; my pristine walls bound the total within load noise, so the shares and crossing stand); and the e 0.99 refusal mechanism above. Predictions: P1/P3–P7 held, P2 half-failed (43.3 vs ≤ 40) and that failure is the boundary finding — honestly disclosed, which is itself evidence the pre-registration was real (mtime ordering no longer verifiable since regen overwrote `out/`; noted for the record).

**Novelty:** the contradiction was standing on `lab/wiki/frame-cost.md` with this adjudication named as the experiment to gold; cd6e's e-monotone law is cited prior art, not the finding. Two blind checkers converge (my burn/N=1e5/e-0.95 numbers match the first checker's within noise). Adoptable in one step: nothing to wire; it re-ranks the kick programs per regime (plane → Carlson compile; belt → readouts).
