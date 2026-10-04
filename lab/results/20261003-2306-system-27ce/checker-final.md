Working...
Check complete: `lab/results/20261003-2306-system-27ce/check.md` written — **Grade: silver**. Nothing else in the run folder was touched; no git commands beyond read-only log/show.

**What the check did**

- **Reproduction:** ran both dossier commands in a clean copy. Bit-identical — all 15 belt rows and 7 moon rows match the author's JSON to <1e-9 relative (624 s / 381 s vs the author's 505 / 378 on the shared container). Empty `patch.diff`, nothing to apply.
- **Predictions:** written before the decisive runs (file times T−31 min vs T−1…−3 min). Two of five failed, disclosed honestly — but two summary lines were graded in the author's favour: prediction 4's "bounded at n≥8" is false at its own control (n=64 Jacobi exponent +0.36 > the 0.2 bar), and prediction 3's literal "dense n=64 does not over-pump" failed (the slice is 11× worse than non-resonant even at n=64).
- **Four adversarial cases, all run:**
  1. *Moon per-body:* the 3 bodies dead in the reference are exactly the Hill-close ones; at n=8 the 0.25–0.35 R_H survivors err 0.9–4.9% in shape (B5's 1% bar fails for 2 of 5). "Hill regime 8×" is really "inner Hill".
  2. *IC smear:* verified numerically — a = launch radius/(1−e0), so the "dense 2:1 slice" actually spans a ∈ [3.31, 4.16], mostly beyond the 2:1; the resonance mechanism was never sampled.
  3. *Certificate variants:* per-orbit cumulative quantum gives n≈1.6/orbit — the falsification is robust to the accumulation convention.
  4. *Eccentric belt (e≤0.42, clean placement, new seed):* n=8 clean and saturating, n=4 walks — this attack **supports** the claim, and shows the smear isn't load-bearing.
- **The constant:** the flying default is `step_log2: 7` (1/128), not the dossier's 1/64 — the dossier quoted the stale doc comment. Real headroom vs the plane is 16×, claim strengthens, premise number wrong.
- **Novelty:** no prior cadence measurement; nearest are H0190 K1 (the law's averaged-kick layer, different layer) and `examples/jacobi.rs` (Jacobi-only sweep, no recorded result). Goal fit is direct: board focus item 1, HANDOFF's 29 µs/kick.

**Why silver, not gold:** two held-out predictions failed, 8× is short of the 10× bar as claimed, and adoption needs the named integer rung (`r-cadence`) — silver's definition verbatim. The one experiment, amended: judge against the true 1/128 default, per-body moon judging, measure rebinds as well as kick events (15 of the 29 µs live in rebinding, which the float probe cannot see).
