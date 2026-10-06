Working...
Check written to `lab/results/20261006-1354-fermi-c9fa/check2.md` — **Grade: silver**.

**What I did:**
- **Reproduced bit-identically** in a clean tree (patch.diff is empty; pure-analysis run): `budget.py` output matches `budget-out.txt` byte for byte, and I re-derived every headline number independently (153 cores RTF 100, 175 RTF 1 raw, fill 5.7/1.7 d, S_live caps 5.2×10⁷ vs 5.4×10⁸, deadlines 13.4/3.9 h) — all agree.
- **Verified every anchor at source**: H0190 K1/K2/0.6-core, H0210's 29 µs, steady.jsonl's 5.865e-3 hits, scale.jsonl's 0.020 N-invariant sweep with ρ·N=1, ladder v7's 4 GiB cap, the 0.126 bit/body gold, 488 B/10⁶, 4P+4E/8 GB.
- **Predictions genuinely pre-registered** (14:02:02 vs 14:03:57) with an honest, correctly diagnosed P6 failure — I confirmed the fixed-ρ·N sweep structure from the raw JSONL myself.
- **Adversarial cases found the real gap**: the author's own anchors carry element swaps at 1.56/body/orbit — 266× the encounter rate — yet the budget asserts encounters are "the only per-body producer". If swaps scar, fill collapses to 0.5 h and the reabsorption deadline to 3 minutes, killing the "memory comfortable for days / idle-time compaction" half. The compute-binds ordering also flips at RTF 1 and is a near-tie at RTF 10, while the claim line reads unconditional.

**Why silver, not gold**: real, honest, exactly reproduced sizing laws — but it quantifies a framing (H_live) the plane.md review already established and a compute gap the board already carried as 10–100×, and its memory half rests on the untested no-swap-scars assumption. One experiment from gold: measure on shipmem's real program form whether element swaps and averaged kicks actually feed the live set.
