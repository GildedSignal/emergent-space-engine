Grade: silver

**Abstract.** The gravity-news payload must carry the source's total acceleration: Kinnersley/Carlip fix the retarded field at (x,v,a) — never jerk — and the toy falsifier puts (x,v,a) at the machine floor under constant burn (0/8×10⁻²⁰), jerk residual ∝ j·T^3.1 (1.8×10⁻⁸ at P/32, β 0.3, ~50× under budget), beating the as-if-now readout 3.4×10³×; the now-readout's total scar is cadence-invariant, confirming 7ab4 independently. Reproduced bit-identically, deterministic. The checker's quartic adversarial (time-varying jerk, outside the swept family) bounds the headline: the jerk slot buys 28–143× on curving burns and violent curvature puts (x,v,a) at 1.6×10⁻⁶ — "no jerk slot" is profile-scoped. Adoption is the shared a-slot (≈2 multiply-adds) but waits on plane expressibility.

## Reasons

**Reproduction.** Clean copy, `regen.sh` exit 0 in ~9 s: `analysis.txt` and `probe_floor.txt` bit-identical to the author's; `results.json` deterministic across two fresh runs and byte-equal to the stored file (md5 dbe3e4a0…). `work/patch.diff` empty; nothing outside the run folder needed. Pre-registration consistent: mtimes run author-prompt → predictions.md (+7.8 min) → probe_floor (+11) → falsifier (+12) → dossier (+13.5); run.log is empty so in-session order is unverifiable, but the decisive numbers regenerate only from scripts postdating predictions.md.

**Controls verified.** Twin/oracle 0.0; free-fall 0.0 at every β; step control ratio 0.98; sign control flips (0.67–0.72, disclosed); my independent harness reproduces the anchors exactly (case A β 0.3: O1 1.35×10⁻⁷, O2 0; case B at P/32: O1 2.43×10⁻⁶, O2 1.84×10⁻⁸, O3 0).

**Adversarial cases (mine; harness reproduces the author's anchors first).**
1. β_c = 0.5 — one decade past the swept range: (x,v,a) still floored at constant burn; jerk residual 8.3×10⁻⁸ at P/32. Survives; margin ~12×.
2. Jerk ×16 (thrust doubling in P/64): P/32 residual 7.7×10⁻⁷ — at the budget's edge. The "50× margin" is specific to the swept ramp rate; ×64 saturates (displacement co-scales, as the author noted).
3. **Quartic program (time-varying jerk), O3 carrying jerk frozen at version time** — the case the cubic design cannot address: O3 gains 28–143× over O2; violent snap puts O2 at 1.6×10⁻⁶ (over the 10⁻⁶ budget) while O3 holds 5.7×10⁻⁸. "Jerk slot exactly dead weight" was measured only on the one program family where it cannot fail.
4. Eccentric consumer e = 0.5: floor holds; jerk residual 3.5×10⁻⁸. Survives.
5. Twin control on the quartic: 0.0 (instrument clean).

**Novelty.** No Carlip/Kinnersley/jerk/payload hits in docs/HISTORY.md; the topic page's open direction 3 asked exactly this. Increment over 7ab4 (silver, one day earlier): the jerk half, the literature anchor read at source, the T³ law and T* window, and a semi-independent confirmation of the cadence invariance (different harness, same framing — not fully independent). The a-slot conclusion itself is 7ab4's.

**Arithmetic.** T*: fit on case C β 0.3 crosses 10⁻⁶ at T ≈ P/9.6, and the author's own measured P/8 point already reads 2.18×10⁻⁶; the dossier's "T ≈ P/6.5" is ~1.5× optimistic. The substance (game cadence P/32 ≪ T*) is unaffected. All other quoted numbers match analysis.txt (3.4×10³×, 7.7×10⁻⁴ flat, exponents 2.19–2.99 and 3.15–3.98, order differences 0.90–0.98). Text/code mismatch: predictions and dossier say "2 orbits"; `t_run_P=1.0` integrates one.

**Predictions.** Held: P2 (the floor, ≥5 orders), P3's exponent band [2.9, 4.1], P6 (sign). Missed as written, all disclosed: P1 (measured to 2.99 vs [1.9, 2.6]), P3's linearity (0.77 effective), P4 (C = 0.004–0.038 vs [0.3, 2]), P5 (per-rebind slope 0.78–1.6 vs ≤ 0.2; the total-scar invariance it targeted does hold).

**Goal fit.** PRINCIPLES #23 "Nothing past c… even gravity is light speed": the retarded (x,v,a) readout is the causal half made cheap; #3 "Compute only surprises": (x,v,a) is the minimum broadcast that is exact between surprises. It answers open direction 3 with numbers and grounds 7ab4's ½aT² in Kinnersley's field data.

**Why not gold.** (i) The headline deletion — "no jerk slot needed at game cadences" — was tested only on constant-jerk programs, where the jerk-slot control is exact by construction; the quartic case shows the verdict is burn-profile-scoped and the margin is ramp-rate-scoped (eaten at ×16). (ii) Adoption is not within one step: the a-slot build waits on plane expressibility (the author's own E3 caveat), and the a-slot recommendation predates this run (7ab4). (iii) T* overstated ~1.5×.

**The experiment that would make it gold.** The payload ladder over the burn-profile family a ship can actually fly — constant jerk, sinusoidal throttle, exponential spin-up, quartic — at flight cadence and the hardest consumers (β to 0.5), with the snap term in the error model: decide whether the a-slot alone holds the quantum for every profile, or whether the jerk slot is conditionally required and r-news's criterion must name the trigger. My miniature already suggests the shape: curving burns restore the jerk slot's value exactly where the burn's own curvature is the surprise.

**What the author missed.**
- The jerk-slot negative control ran only on cubic programs — the family where it cannot fail; realistic throttle curvature was the natural adversarial case and was absent (the lens section names the trust-in-literature blind spot but not this one).
- T* arithmetic: their own P/8 point already exceeds the budget; P/6.5 should read P/9.6.
- "Over 2 orbits" vs one in code; "slope ≈ 1" for the now-readout is 1.29–1.60 at β 0.003.
- The dossier's "(x,v) at the same scenes" band mixes only case-A rows without saying so (case B/C (x,v) scars are 2–4× higher).

Page corrections made in place (wiki/gravity-news.md): T* → P/9.6 with the measured P/8 point; "exactly dead weight" scoped to constant-jerk programs with the quartic numbers; the Refuted bullet scoped ("not refuted for curving burns"); open direction 3 extended with the burn-profile family.
