Working...
Check complete. Verdict written to `lab/results/20261014-1010-taleb-292a/check.md`, the author's page corrected in place, tree restored to clean.

**Grade: silver**

**Reproduced (bit-identical).** Applied `work/patch.diff` at base 9029188, reran regen.sh: `seam.json` byte-equal to the stored copy, analysis identical, cost 22 µs. All headline numbers cross-checked from the JSON with my own analysis (128/128 unique, dw median 1.44×10⁻⁵ / max 0.309 turns, dk_final −2.3×10⁶ at the e=0 p=8M circle, p exactly stable on all 128, 3 one-step repeats). Shipped-code mirrors verified by reading `bind.rs` (decode `to_doll` 127-131, `in_tube_units` 252-258, `from_state` 265-266), `shipmem::Body` = (p,e,w,t), Residual 4×65-bit. Word-invariance verified **per-config**: 44/44 paired chains within 2.1×, median ratio 1.00 — stronger than the author's own aggregate display.

**Why not gold — two probe-construction flaws the attack found:**
1. `Scalar::raw(φ,3)` = 8φ·P (raw is n·2⁺ᵉ, proven empirically): both φ arms sampled **periapsis** — "phase 1/8 and 3/8" was never run. At true phases the walk is strongly phase-dependent: 10⁻¹³–10⁻⁷ inbound vs O(1) outbound strong-field (up to 3.7), and one bounded **2-cycle** exists (p16e30, e0.99, φ1/8) — a counterexample to "never finds a fixed point" as a universal claim.
2. The "μ≈1.28" doll was μ≈1.4×10¹² (same sign slip): the 195 cartesian refusals are a 2⁴⁰ unit jump, not the claimed "factor-2 margin" (margins 1–4 and the exact `word_for` word don't fix the author's construction). With the word re-based on the doll scale, the μ crossing completes **108/108 with drift ≤2.8×10⁻¹²** while unity drifts 0.18–2.7 on the same configs — the doll conversion is benign-to-helpful, refuting the dossier's "worse, not better."

**What survives every attack:** the near-circular w lottery (the belt case) walks ~1.7 radius at **every** phase, k/p stay stable, the seam is canonical, and depth 256 shows no key repeat (but saturation, not linear compounding, plus mid-walk refusals — the promote-to-live trigger). The design conclusion — anchor w+t as one observed-angle column or carry the residual **before** demote-at-commit merges — stands. One experiment from gold: rerun the sweep at true phases with the doll-based word (~10 s; my probe already does it) and republish per phase.
