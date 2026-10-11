Working...
Check complete. `lab/results/20261011-0224-library-213e/check.md` written: **Grade: silver** (abstract 117 words, first line exact).

**Reproduced:** `python3 work/probes.py` byte-identical to `probe-out.txt` (13.7 s, matches the ~13 s claim); `probe-rerun.txt` identical; predictions pre-registered (mtime 02:30:24 → probe 02:32:25 → output 02:32:38); all six Readwise anchors verbatim (Housel/Munger are AI episode notes, disclosed); 4,580 highlights confirmed. No number differed.

**Five adversarial cases (author's own code), which set the grade:**
1. **Certificate rule costs 1.5–2.4× the headline.** Windows sized by the tail-coefficient certificate (the design's actual rule) need 33/132/704 evals/orbit at e=0/0.3/0.7 — not the reported 22/55/352, which are true-error-sized. Against the live 8–16 kick cadences (q-cadence lens), the certified fit is a regression; only the dead 350–700 fixed-step baseline makes it look like a win.
2. **Sundman kill fails at the edge.** At e=0.9 the true-anomaly parametrization wins 4× (64 vs 256 windows). The unconditional "drop change of variable" discards the one lever that works on hot bodies.
3. **B1's metric is a broken instrument.** Every case carries a constant, exactly-known 1/2π = 0.159-beat phase offset never removed; the author's own predicted circular control ("exact") scores 0.159 under it. Corrected: e=0.1 wobble is 0.031 (nearly passes), e=0.3 is 0.684 (worse than reported).
4. **"One exact pair event per beat" is contradicted by the author's own K counts:** 1.94 conjunctions/beat at e=0.3, 4.65 at e=0.7, 13.0 in the near-1:1 formation regime — where the co-orbital gold (taleb-09b5) already operates, uncited.
5. **"Richer spectrum" half-diagnoses B2:** 5 frequencies help only at e=0.1 (0.749→0.246 std); e=0.3 and 7:6 stay ~3. The miss-distance sequence is not low-dimensional quasi-periodic — the firmest (negative) answer yet to r8 v2's Diophantine hope.

**Novelty:** lesson 1's mechanism (Chebyshev fit + refit on band break) is H0102–H0105 prior art, uncited; lesson 5 restates the board's arch-v3 gate-bite lead. The genuinely new results are the negatives: quasi-periodic miss-distance and certificate conservatism.

**One experiment to gold** (named in check.md): fit-cadence on the plane's own kick stream, certificate-sized windows, against live 8/16/64 cadences at equal B12/B14/B17 behaviour — q-cadence's own ≥4× bar.

Nothing else in the run folder was touched; no git commands run beyond read-only status/log.
