Working...
**Grade: gold** — written to `check2.md`.

**What I verified (blind to the first check; no `check.md` read):**

- **Reproduction, byte-exact where deterministic.** Clean tree, empty `patch.diff`, nothing touched outside the run folder. Shipped `--kick-bench` at 20 s and 55 s × seeds 1–3: `digest` and `replay_digest` identical to the stored record, memo counts and hit rates identical; `--bench --rtf 100` → 337.6 events/s, 76 bodies, 4809 B/body; `budget.py`/`amort.py` outputs byte-identical. The author's bench replay's digest equals the shipped record's, so the attribution provably covers the record's own kicks. Verdict ratios reproduce within 1–2 points (made compile 11.7% vs 10.6%; co-orbital 17.0% vs 15.0%).
- **Predictions** were written 11 s before the first decisive output; the verdict prediction P4 held exactly; P3's exact-key failure is disclosed and matches `dbd4add`.
- **My attacks all confirm the refutation:** unseen seeds 4–5 → gain 1.10× (seed 5 leaver-heavy: 3.0×); a ±32%-dispersed fleet collapses sharing to 64/64 distinct shapes yet the ceiling stays 1.17× — the ceiling is the compile *share*, not sharing; arithmetic shows 40× needs compile ≥ 96% of a kick against 10–17% measured; sharing the whole `from_state` gives only 2.0×; and since quantized-key sharing changes digests (dbd4add), the measured ceiling is the generous bound — the refutation holds a fortiori.
- **Novelty:** the sub-phase attribution and the cross-body amortization ceiling are not in HISTORY/board; same gold shape as components-4643 (premise killed by measured ceiling, zero adoption cost).

Misses noted for the record: no child-doll bound formation measured, the 6.3× tail is a 7-sample median (my seed-5 gives 3.0×), the co-orbital "gain" is really just compile-removal, and the 40× bar is rtf-100-conditional.
