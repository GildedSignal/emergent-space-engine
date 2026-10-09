Working...
Check complete. **Grade: silver.**

**What I did:**
- **Reproduced** every dossier command in a clean tree (patch.diff empty): kick-bench ×3 (median 44.3–45.3 µs, hit rate 0.0 — the quoted 41.8 regenerates in family), both benches with exact args (m48 stats bit-identical; m448 gives 410 bodies / 6565 B/body), ran `budget.py`, verified all arithmetic (175 cores, 1.143-orbit horizon, ceilings).
- **Three adversarial cases:** timing variance (stable); two new slope points the author claimed were blocked — members 148/248 run fine, marginal 6.1–7.7 KB/body, "~7 KB / ~430–446×" holds; rtf-1 young-scene run showing the event rate is regime-dependent (27× higher in the spawn transient).
- **Found the record defect:** the quoted m448 numbers (406 bodies, 6813 B, 3.9×10⁻²) regenerate only with `--seconds 8`, not the stated `--seconds 10` (budget.py's `/800` betrays the trace); the two per-body event rates are aggregated inconsistently (full total vs subtotal — consistent value is ~5.3×10⁻²); `--members` clamps at 400 so "448" silently ran 400, and the "saturation at ~406" is that CLI clamp, not physics. Conclusions all reproduce within a few percent; the evidence chain doesn't.
- **Novelty/goal fit:** first live-store measurement for the plane (old path's 88 B/body was a different engine; HANDOFF says H_live "not measured yet"); moves board item 3 and re-ranks the levers (memory 446× > skin 12.6×); adoption is zero code.

`check.md` written to the run folder — first line `Grade: silver`, with the one experiment that would make it gold (a clean re-measure pass with stated commands, `budget.py` wired to evidence, regime and clamp disclosed — bookkeeping, not physics). Nothing else in the run folder touched; no git commands run.
