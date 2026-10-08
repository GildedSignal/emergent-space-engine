Working...
Check complete. `check2.md` written; scratch removed; nothing in the run folder touched besides that file (the jetbench rerun regenerated `metrics2.json` byte-identically, and `work/patch.diff` was correctly empty).

**Grade: silver.**

**Reproduced** (clean tree, detached HEAD a838a28):
- `falsifier-orig.py` → bit-identical to `repro-orig.txt`.
- `jetbench` run 3× → deterministic; matches `falsifier2-out.txt` except compile banner and wall time (17.0 vs 17.6 s). Cost bin: 6.2/29.4/135.3 µs vs claimed 6.3/30.5/138.8 — noise.
- Predictions discipline held: `predictions.md` (17:26:55) predates `jetbench/` (17:29:46) and the decisive log (17:32:56); bands miss in both directions and the misses are disclosed.

**Adversarial findings:**
1. **The criterion's hole (why not gold):** E3 validates the per-cycle trigger on the corrE path only. On the corrL tide channel — the dossier's own "belt's actual secular channel" — the author's model verbatim gives max error **13.5×/3.4×/1.5× floor** at e=0.5/0.9/0.99. The local-FD T″ used by the trip bound is ~8 orders smaller there than on corrE. The δE-based "equivalently" form is blind to that channel entirely (E is conserved).
2. Off-grid e (0.85/0.97/0.997): corrE within <1% of 543·(1−e²)^{2/3} (strengthens); corrL keeps dying (266 at 0.997); trigger rate 0.0713/kick at 0.997 — past the 0.05 budget, so the scene cap, not the trigger, protects it. e=0.999 panics into the crate's plunge refusal (NoBoundOrbit) — the disclosed domain boundary.
3. Fresh seeds: randE ≥3× survives, but the tail seed floor is 3.3× at e=0.99, thinner than the quoted 4.7–35×.

**Novelty:** the re-anchor rule is already adopted (law.md line 35, from 20261006-0346); this run's real deltas are the e-scaling on the shipped law, the tide-channel premise correction, the negative control, and the belt-tail concentration (37.9% of crossings on 1.1% of bodies). One experiment to gold: validate/repair the per-cycle trigger on the tide channel — plus reconcile the quantum-scale horizon (≈1.5×10⁵ kicks) against law.md's "730 correlated quantum kicks"; one of the two is off by ~200×.
