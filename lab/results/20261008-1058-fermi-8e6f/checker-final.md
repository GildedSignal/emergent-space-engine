Working...
Check complete. `check.md` written; nothing else in the run folder touched, no git operations.

**Verdict: silver.**

**Reproduced:** `ledger.py` byte-identical; probe A bit-for-bit identical counts (32/169/584 encounters, pairs exponent 2.00) from a fresh build. Build forensics (`/tmp/fermi-target` created 11:04:30, outputs 11:05:51/11:08:32) prove both decisive runs started after `predictions.md` (11:04:03).

**Adversarial (pre-registered, all held):** the skipped N=8000 point → 2474 encounters vs 2550 predicted from the author's own fit, 4-point α = 1.06; alt-seed at N=4000 → +9%; hot belt σ_e=3e-2 → exponent 0.90 (α≈1 is density-linear kinetics, not an artifact). Every ledger number re-derived by hand: correct, including the impulse formula.

**Why not gold:** one registered anchor prediction failed (factor 9) and the dossier's rescue ("r8's σ_e and ρ were log-uniform draws") is contradicted by the repo: `opus-encounters-20260930/scale.jsonl` has rows at *exactly* the author's parameters measuring ~3.96e-2 events/body/orbit — consistent with the author's 1.9e-2 exact-truth pairs once counting semantics are accounted. The correct anchor existed, agrees within ~2×, and was missed; ledger layout 2 inherits the wrong belt-0 rate (internal 9–19× inconsistency, though every conclusion survives the correction). Smaller slips: "cap is 17× above the N=4×10³ point" is actually 1.75×; mean spacing ~3×10⁶ m, not 8×10⁶ (conclusion unchanged).

**Gold path named:** extend probe A to N=8e3–1e5 with exact truth and re-anchor layout 2 on the same-parameter repo anchor — one short run plus a citation fix.
