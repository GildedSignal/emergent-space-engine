Working...
**Grade: silver** — written to `lab/results/20261008-1337-fermi-ab86/check.md` (only file added; nothing else in the folder touched).

**Reproduced** (byte-identical, `fermi_budget.py`, 3.4 s): slope 0.499, ceilings 33.9/37.9/28.0 b/b, ≤1.04 MB/s writes, macro 7.11e-3/orbit, 47 cores @ rtf 5×10⁴ / 190 @ 2×10⁵ / 3.6 @ 10⁶. Pre-registration holds: `predictions.md` 13:41 < script 13:43:40 < `run.log` 13:43:46 < dossier 13:45 (run.log is in the folder, just gitignored so my first glob missed it). P2/P3/P4 held.

**Two defects found by attack, neither flipping a conclusion:**
1. **Rate constant 2.5× high.** Independent geometric derivation + 2M-sample MC + exact integral all give Γ(Δv>q) = `2nGm/q·(1−r_H²/b*²)` = **1.36e-2**/body/orbit vs the author's `4nGm/q` = 3.43e-2. Their b* is correct; only the Poisson intensity is wrong. Their P1 MC drew Poisson counts *from the formula itself* — circular, so it scored 0.1% agreement by construction (the author disclosed this, which is why it survived as plumbing test, not physics). Corrected: 0.52 MB/s writes, 15 MB/orbit macro, slope unchanged (my MC with corrected constant: 0.506).
2. **"2.7 b/b after 1 orbit" is a mislabel.** Their MC steps at T/60 = 500 orbits; the first recorded checkpoint fires after step 1, so S[0] is S at **500** orbits (their own rate gives σ≈7q → S=2.8, confirming). True S(1 orbit) ≈ −2 bits — sub-quantum, no stock yet. Conservative direction; slope and S(3×10⁴)=5.6 unaffected.

**Adversarial cases:** phase-locked kicks (the resonant channel the lens itself flagged) give slope 0.887 → +3.3 b/b/decade vs +1.66 — the "bounded" claim is conditional on incoherence, as the dossier's own what-would-make-it-wrong admits; v_esc/v_rel = 0.50 at b*, 1.63 at r_H (impulse approx invalid inside ~1.6 r_H, matching their caveat). Ceiling arithmetic verified independently (9.3 = log₂ 631; 18.6 = log₂(2π·2¹⁶)).

**Novelty/goal fit:** HANDOFF line 70 says H_live "not measured yet" — this is the first measurement; builds on components-98bc's 0.126 b/b correctly; directly targets the board's "fitting 10⁹ in 8 GB" item (PRINCIPLES 24, 3, 33).

**Path to gold:** one shearing-sheet (Hill) truth run — measure dΓ/db from integrated trajectories (pins the constant and the 1.6 r_H validity edge), measure kick-to-kick phase memory (turns the incoherence assumption into a measured crossover), re-derive S(t) with sub-quantum flux and honest checkpoint times. Minutes of compute; every adoptable number then comes from measurement.
