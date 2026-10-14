Grade: silver


Abstract: Reproduced bit-identically (seam.json byte-equal; 128/128 chains unique to depth 64; controls hold; word-invariance verified per-config, 44/44 within 2.1×). But two probe flaws: `Scalar::raw(φ,3)`=8φ·P made both φ arms sample periapsis (never 1/8, 3/8), and the "μ≈1.28" doll was μ≈1.4×10¹² — the 195 refusals are a 2⁴⁰ unit jump, not a margin effect. Checker extensions: true phases give drift 10⁻¹³–10⁻⁷ (inbound) to O(1) (outbound strong field), one bounded 2-cycle exists, depth 256 saturates with mid-walk refusals, and the μ arm with a doll-based word completes 108/108 at ≤2.8×10⁻¹² — benign-to-helpful, refuting "worse, not better". The near-circular w lottery walks at every phase, so the conclusion — anchor w+t or carry the residual before demote-at-commit — survives; silver for false domain claims.

## Reasons

**Reproduction (all held).** Applied work/patch.diff to the base commit (9029188), ran regen.sh: seam.json bit-identical to the stored copy, analysis identical, cost 21.9–22.7 µs full / 13.1 µs fit (dossier: 22.8–32 — same class). Verified the shipped-code mirrors by reading bind.rs:117-133 (decode's to_doll), 252-258 (in_tube_units), 265-266 (from_state/ending_at); shipmem::Body is (p,e,w,t) u64 (belt.rs:200-205); Residual is 4×i128 "can require 65 bits" (space/binding.rs:73-79). Numbers cross-checked from seam.json with my own analysis: 128 done (all unity — the μ arm refused 216/216, honestly reported), refusal stages 195 cartesian + 99 state + 10 fit, 3 cycle_len=1 repeats, worst dk_final −2,312,107 at p16e-1_e0, dw median 1.44×10⁻⁵ / max 0.309 turns (e=0.9 arm; near-circles reach 0.205), p column exactly stable on all 128 (dp_rel_exp −64). All as claimed.

**Prediction timing.** predictions.md predates dossier.md in the restored tree (13 min); the original decisive-run ordering is unverifiable after tree restore. Internal evidence favors authenticity: P4 is reported half-refuted and P5 untested against the author's own claim — a post-hoc file would not read that way.

**Attack findings (three adversarial cases outside the author's range, one instrument bug):**

1. **The phase dimension was degenerate.** `Scalar::raw(phi_num, 3)` means num·2³ (verified empirically: to_doll on the "μ≈1.28" doll jumps the radius exponent by 40, i.e. μ = 0x147AE1·2²⁰ ≈ 1.4×10¹²), so t = 8φ·P — both φ arms sample periapsis, not "phase 1/8 and 3/8" as the wiki page states. At true phases 1/8–7/8 (my rerun, 64 chains): inbound phases drift 10⁻¹³–10⁻⁷; outbound phases in the strong field scramble (e=0.5/0.99 at p=8M: up to 3.7); one config (p16e30, e0.99, φ1/8) finds a bounded 2-cycle — a counterexample to "never finds a fixed point" as a universal claim. The headline median 6.4×10⁻³ and max 3.36 are periapsis-specific. The near-circular/circle lottery is phase-independent (~1.70–1.89 at all four phases) — the belt-relevant case stands everywhere.
2. **The μ arm's diagnosis is wrong.** The doll was 2⁴⁰× the intended mass; the cartesian refusals are the unit jump, not the missing "factor-2 margin" (adding margins 1–4 and the exact word_for apoapsis word does not fix the author's construction). With the word re-based on the doll-unit radius (as the shipped flow implies), the μ crossing completes 108/108 chains (φ=1/8, 3/8, and periapsis) with drift ≤2.8×10⁻¹² and no key repeat — while unity at the same configs and phase drifts 0.18–2.7. The extra doll conversion is benign-to-helpful (the coarser tube lattice appears to let the fit close), refuting the dossier's "the real per-crossing error is worse, not better."
3. **Depth 256 (beyond the author's 64):** no key repeat (252–256 unique of 256), but the drift saturates (3.358→3.462; 3.9×10⁻⁷→1.6×10⁻⁶) rather than compounding linearly, and chains can refuse mid-walk (fit:Range at n=68 on one; two more in my controls) — a distinct hazard class (the refusal is the promote-to-live trigger b29a names), not in the dossier.

Minor: the min-drift config (3.9×10⁻⁷) is e=0.99, not "moderate e" as the dossier says. The circles' 1.7-radius "state drift" is the same circle sampled at a lotteried orientation — physically harmless for a pure circle; the harm is the stored w column orienting any future e (the dossier's contact-noise argument, which holds).

**Novelty.** The published page holds 8398's key-level transit (awaiting grade). This run adds the column-level composed cycle with the shipped unit handling, the w-column attribution, word-invariance, and the canonicality answer (direction 3); b29a's wiki names "the w/t column anchoring" as the contract to settle at wiring — this run makes it a measured error budget. No HISTORY entry covers it. Genuinely new.

**Goal fit.** nladder open direction 0 / frame-cost's ephemeral promotion: the hazard measurement the adoption needs. PRINCIPLES #13 ("basically we don't want errors that can compound that's the goal") — measured at the seam the design multiplies; #19 — the w column is the wrong representation for near-circles. The claim's gain is a deleted assumption, not a 10× CPU cut — acceptable as premise-killing, but the record flaws below cap the grade.

**Why silver, not gold.** Two material evidence statements are false as written: the claimed two-phase domain (both arms were one phase) and the μ value/refusal mechanism (μ≈1.28/factor-2 margin vs the actual 2⁴⁰ scale/unit jump). The "never finds a fixed point" headline is phase-domain-limited and has a counterexample. The physics conclusion survives, but the numbers a downstream run would cite (median 6.4×10⁻³, "μ unmeasured, not safe", "worse, not better") are wrong or unlabelled. Precedent: r3 v3 (silver for record gaps despite sound physics).

## The one experiment that would make it gold

Rerun the exact 432-chain sweep at true phases {1/8, 3/8, 5/8, 7/8} with the doll-based word for non-unity dolls (the checker's probe already does both; ~10 s), and republish the drift/walk numbers per phase and per doll in dossier, page and predictions. If the near-circular w lottery still walks at every phase (my runs say it does) and the μ arm stays exact, the "anchor w+t first" conclusion is gold with a correct domain.

## What the author missed

- The raw(n,e) sign convention — it silently broke both the phase dimension and the entire μ arm, and produced a wrong refusal diagnosis that read plausibly ("factor-2 margin").
- Phase dependence of the walk (orders of magnitude, and bounded cycles exist): "no fixed point" is a property of (config, phase), not of the seam.
- The doll conversion as a possible *fix* (the coarser lattice closes the fit) — the exact opposite of the dossier's caution, and possibly the cheapest answer to the w/t anchoring contract.
- Saturation vs compounding at depth >64, and mid-walk refusals as a distinct hazard class.
- The circles' 1.7-radius drift is an orientation lottery of a physically unchanged orbit; only the stored-column argument (future e) makes it a hazard — worth saying so the integrator does not overprice it.
