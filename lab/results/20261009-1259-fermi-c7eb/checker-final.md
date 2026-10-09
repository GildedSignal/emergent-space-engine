Working...
Check complete. `lab/results/20261009-1259-fermi-c7eb/check.md` written; nothing else in the run folder touched; no git operations.

**Grade: silver.**

What I did:

- **Reproduced everything, bit-for-bit.** Clean tree (patch.diff empty), `verify a/b/d` (17 s / 32 s vs claimed 18/34), all 10 belts' truth-encounter counts identical, `analysis.py` → `analysis-out.txt` and `rate.json` byte-identical; arithmetic spot-checked independently (tick quantum, 14.9 GiB/1.9×, 545×, 2% core, m_crit algebra all correct).
- **Predictions verified pre-registered** (mtime order) and honestly self-graded — but the core prediction P2 ("Ceres crosses <1% of ticks") failed opposite: 1.2×10⁹ ticks. That alone bars gold by the lab's letter.
- **Attacked the physics.** Integrated real encounters (Sun + two belt bodies): the author's `Δa/a = (2/3)θ` coefficient is **~13× high** and scales as 1/v_rel, not 1/v² (measured ratio 0.50 on doubled v; impulse form confirmed). True m_crit ≈ 1×10⁻¹⁷ M☉ (~1-km rock, not 500 m) — conservative direction, inside the author's own bracket, no conclusion flips. Also found: sub-tick kicks random-walk ("exactly zero" is per-encounter; a 500-m rock first crosses a tick in ~90 orbits, flux negligible at 10⁹), thin belts run 28× the event rate used in the ledger (55% of a core at RTF 100, still under), and the fleet caveat survives the corrected scaling.
- **Novelty/goal fit:** HANDOFF's registered risk "H_live … not measured yet" — no prior H entry; directly serves the board's 10⁹-in-8 GB item and argues against deleting `crates/shipmem`.

Silver, not lead: fully reproduced, kills a real premise (belt self-evolution doesn't force tubes below ~1-km rock — stronger than claimed), zero adoption cost. The named gold experiment: pin m_crit and the crossing flux on the crate's real (d, v_rel) distribution with the validated coefficient.
