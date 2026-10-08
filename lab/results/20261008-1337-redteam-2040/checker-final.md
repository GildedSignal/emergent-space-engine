Working...
Verdict written: `lab/results/20261008-1337-redteam-2040/check.md` — **Grade: silver**. Nothing else in the run folder touched.

**What the check established:**

- **Reproduction:** bit-for-bit. Clean-tree `python3 falsifier.py` matches every number and the whole `falsifier-out.json` (sorted-key diff clean); 22.5 s, 34 MB. `patch.diff` is empty — no tree edits.
- **The kill is real, independently confirmed.** My own DOP853 proper-time integration (a method sharing nothing with the author's turning-point quadrature) validates the oracle to 2.5–5.3×10⁻⁶ and the 1PN ratio to 6.1% exactly; and the kicked P4 orbit *integrates to the horizon* (crosses r=2M at τ=234) while the multiply-add fabricates a plausible cycle (Δφ 18.86, T_t 585). Type error, exactly principle 2.
- **Predictions:** predates the decisive run; P1/P2/P4 held, P3/P5 failed and were honestly reported (both in the premise's favour — evidence against post-hoc tuning, but two of five held-out predictions failed, which the gold bar does not allow).
- **Adversarial finding the author missed:** every case kicked L only (dE=0). My E-kick attacks show (a) the "scale-free in δ" law is L-axis only — a 10⁻⁴ E-kick in the weak field gives T_t error 1.15×10⁻³, six orders worse than the matched L-kick; (b) the plunge separatrix is crossable via E, same fabrication; and (c) an *unbinding* kick (E≥1) fabricates a cycle for an escaping orbit **and passes the dossier's own proposed predicate** ("three real roots, middle outside horizon") — the author's `is_bound` misclassifies my hyperbolic test as bound. The fix needs `E<1`.
- **Novelty/goal fit:** confirmed — no rung or H entry tests cycle kick-response; `b-plunge-tubes` is in flight (HANDOFF), and the multiply-add is the only cheap kick path left after the 5 Oct memo correction.

**One experiment for gold:** extend the falsifier to the E axis (E kicks at matched distance, escape-side crossing, corrected predicate, RK4 validation shipped in-folder) — then the criterion is freeze-ready for `b-plunge-tubes`.
