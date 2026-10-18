Grade: silver

**Abstract.** Claim: after a belt-quantum kick only the near-horizon due band needs
re-checking — 0.034 arm-evals/body/kick at 10⁴-occupancy cells (∝n² at fixed density),
not fe6b's 0.034·n = 346 — and armed lists re-lottery 0.5–0.75× per kick in miss
distance, so re-decide at the due, never store exact. Reproduced byte-identically;
pre-registered predictions and both controls hold; my held-out cases (anchor seed
31337, hot belt e≈0.3, 64× kicks) hold. Two corrections: the n² off-centre constants
are a ×10-per-decade slip (my n=10⁵ flight measures 4.67 vs the quoted 0.34; the
shape holds), and the "~6 orders, 197→2×10⁻⁴ cores" headline is ~4 orders
(12.3→1.2×10⁻³) under its own assumptions. Gain: 10⁴× on the row's churn term.
Adopt: due-band rule on `tier::arm_pair` callers; one shipped-tier flight remains.
**Reasons.**

1. **Reproduction.** `sh regen.sh` exit 0 (runner); my independent rerun of `toy.py` in a scratch tree is byte-identical to the stored `regen.out` (sha256 `2397894b…`). All dossier numbers regenerate: candidates 99/999/9999 (slope 1), flips 0 everywhere, near-band 0.03/0.035 at n=10⁴, seeds 777/424242 → 0.050/0.065, anchor armed 525–1050 with churn 0.5–2.0× across dv, control B 11/11 with 0 missed, control C loses 2 (2⁻¹⁷) and 5 (2⁻¹⁴) events per 100 kicks, control D standing 543.2 with flips 33.2/344.4. `work/patch.diff` is empty: toy-only, no engine edits, matching the silver self-grade.

2. **Predictions.** `predictions.md` mtime precedes the final `toy.py` by 11 minutes and the dossier by 13 (only mtimes are observable here; the in-file amendments are disclosed as pre-run). P1 held (slope 1, extended by me to 99999). P2 held in substance; note the dossier restates its letter as "flips ≤ 0.1" where the file says "≤ 0.01" (measured 0 satisfies both). P3's amended multiplicative law held; the near-co-orbital in-horizon walk 0.7 > 0.1 is disclosed. P4 held — and the "predicted 0.27·n" verifies independently: mean-field P(|Δλ| ≤ 2B/a) on the shared ring = 0.295 → 589 vs measured 543.2. P5 held (0 missed; negative control fails; second seed stable).

3. **Adversarial cases (mine).** (a) **n=10⁵, one decade outside the author's range:** near-band 4.665/body/kick, flips 0, candidates 99999. The mean-field law n·W·(H+2)·⟨|Δa|⟩/T̄_syn is exactly n² (0.068 → 6.77 two-sided from 10⁴ to 10⁵; the author's one-sided anchor 0.034 → 3.4), so the measured 4.67 *confirms the n² shape* while refuting the dossier's quoted 0.34 by 13.7× — the author scaled ×10 per decade instead of ×100. (b) **Hot belt, e Rayleigh 0.3 (author tested only e≈0.07):** band 0.045, armed 0, flips 0 — no new churn channel at high e. (c) **64× kick (2⁻¹⁷) at dilute cells, which the author ran only at the anchor:** flips 0 at margins +2/+8/+64 (bands 0.06/0.07/0.38); in-horizon dues walk 4.6 intervals — the +2 margin is quantum-kick-only and should be stated as ∝ kick size (b509 measured this class at ε=1e-2). (d) **Held-out anchor seed 31337:** armed 700, churn 0.75×/1.25×/2.0× at 2⁻²³/2⁻²⁰/2⁻¹⁷ — the miss-fragility range extends to 0.75×.

4. **Composition arithmetic (corrected).** Under the claim's own assumptions (1 µs/arm, 1 kick/body/interval, 10⁹ bodies): fe6b-structure 346 µs × 10⁹ / 28141.5 s = **12.3 cores** (98 with split 8 — cd3b's "10¹–10²" hedge), band rule 0.034 → **1.2×10⁻³ cores**: a fall of **1.02×10⁴ ≈ 4 orders**, not "~6 orders"; neither endpoint (197, 2×10⁻⁴) is derivable under any single clock convention (the toy's docstring calls the interval "28141.5 game-s" where SI gives 2.82×10⁷ s — the muddle). The claim survives at 10⁴×; the headline did not. Page corrected in place.

5. **Novelty.** This answers the wiki's open direction 1 (cd3b's "singular number" the row owed). b509 measured the *in-window* due-walk (<10⁻³) and the fleet-class 16.8 newly-armed/kick; fe6b/1738 priced the wholesale structure; none measured the dilute-cell constant at 10⁹-scale occupancy, its cell-size law, the multiplicative due-walk (which kills intra-cell due-space slack — the run refutes its own first model), or the miss-space fragility of stored lists (which tightens b509's "standing contacts must be stored state" into "stored with miss-space slack"). Not a repetition.

6. **Goal fit.** Board focus row 2 (encounter work at 10⁹): the row's last unknown is priced at ~10⁻³ cores, deleting wholesale per-kick re-arm designs. PRINCIPLES 3 ("nothing is evolved that can be derived when looked at" — dues derive analytically, only the band re-arms) and 14 ("no work for no reason"). Domain honestly bounded: 2-body Kepler, r(λ) radial model, no mutual perturbations, e ≤ 0.4.

**Not gold** because it is toy-only: the shipped-tier flight is the author's own named kill test, and the two headline compositions needed checker correction (both fixed in the page; neither touches the mechanism).

**The one experiment to gold:** fly the due-band per-kick rule on the shipped tier (`tier::arm_pair`'s callers) at 10⁴-occupancy cells and measure re-arms/kick — Θ(n) kills the toy's window model (the standing/dwell class is where to look, per control D).

**What the author missed.**
- The ×10-per-decade slip in the n² off-centre constants (0.0034/0.34 → 3.4×10⁻⁴/3.4) and its downstream conclusion: at n=10⁵ the measured band is ~4.7 evals ≈ 4.7 µs/body/kick, so the 0.34 µs/body level is crossed at n ≈ 3–4×10⁴, not ~10⁵ ("cells may grow to 10⁵" is dead; corrected in the page).
- The cores headline endpoints and exponent (197 → 2×10⁻⁴, "~6 orders") do not reproduce under the stated assumptions; honest is 12.3 → 1.2×10⁻³ cores = 4 orders, still decisive.
- The margin rule (+2 intervals) silently assumes quantum kicks; at 2⁻¹⁷ the in-horizon walk is 4.6 intervals — the design rule must scale the margin with kick size.
- "Match to the digit" overstates: the analytic 0.034 sits inside a 0.030–0.065 seed spread at n=10⁴ (the page's phrasing is already honest; the dossier's is not).
- The churn range at a held-out seed extends to 0.75× armed per kick (claim: 0.5–0.7×) — strengthens, not weakens, the never-store-exact rule.
