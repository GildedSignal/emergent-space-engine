Working...
Check complete. `check2.md` written; grade: **gold**.

**Reproduction** (clean tree + `work/patch.diff`, rebuilt): the decisive arm (10⁵, seed 1, cut 115,000) is bit-for-bit identical — digest `d193e8d8…`, 576,011 kicks, enc 5,609, RSS 489/HWM 489, catalogue 100,076. All state numbers match `analysis.json`; only wall-clock seconds differ (box noise).

**Adversarial cases (mine, disjoint from the first checker's):**
- **N=3×10⁵** — outside the swept range: pre-wave 2.37 kB/body → wave 1 → 4.71 kB/body, wave-1 kicks 303,560 (3× the 10⁵ wave), no knee.
- **8 waves at 3×10⁴** (cut 230,000, double the author's horizon): RSS flat at 152 MB from wave 2 to wave 8, slope 0 B/body/wave. New finding: the wave *shape* disperses by waves 6–8 — the sharp 27,500 train is a young-train property (noted in the page; memory claim unaffected).
- **Chunking at 10⁵ across two waves** (rtf 600 vs 6000): digests identical — validity extends to 25× the author's check.
- **Seed 5**: same regime class, same belt rate (~3.48×10⁻⁵); also confirmed enc=5,609 at N=10⁴.

**Code semantics verified:** `stats.encounters` increments only in `log_encounter` ← `encounters_for_player` (universe.rs:1159–1182) — the player's scan, so the N-independence reading is right; `analyze.py`'s locals split is the shipped `ladder_locals` exactly. **Novelty:** HISTORY and the nladder page show no prior flight past wave 1; the churn regime was live (a669, cae7, e4cc).

**Recorded against it (decision-neutral):** two dossier prose numbers contradict its own regenerable JSON — "slope 0.00 B" (it is 5.0 B = 0.005 kB, same kill-bar conclusion) and "5.8/4.5/6.2/6.3 s … 55–69 µs" (JSON: ≈6.3/6.3/6.2/6.6 s, 63–69 µs); P4 missed but honestly corrected; the CPU "flat waves 2–4" claim is loose at 3×10⁴ (+60% drift, under the 2× kill bar) — page corrected in place, second-checker note appended, tree restored clean.
