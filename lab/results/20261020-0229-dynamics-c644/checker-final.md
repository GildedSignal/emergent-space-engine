Working...
Check complete. `lab/results/20261020-0229-dynamics-c644/check.md` written.

**Grade: gold.**

**What I did:**
- **Reproduced** everything via the runner's `regen.sh` (exit 0): all B/C/D numbers to the digit; arm A — which the author honestly disclosed as unfinished at deadline — completed in my regen (508 dead, 6/508 clamped, λ=3.44e-5), closing the ≥3-seed gap.
- **Two probes outside the author's range**, both confirming: seed 3 full horizon (4/501 clamped, λ=3.63e-5, rings 34→81% outward) and 2× density n=3200 (**0/980 dead bodies ever clamped**, λ=6.46e-5 ≈ 2× base — the contact-rate-limited scaling relaxation predicts; the clamp-zone chain gets *less* relevant as the e-walk speeds up).
- **Data-level attacks** from the TSVs: dead bodies' median min-r before death is 69–74q (C: zero ever below 2.1q) — the apocenter argument holds a fortiori; U-less leavers are 69–77% wide-bound (a>125q, Δε>0), so every death requires per-body energy gain; digest-neutrality of `take_kept_events` verified in source.
- **Novelty**: it flies the chaos-shadowing page's own named unflown leftover and refutes the belt-scale half of 9b3b's mechanism while preserving the isolated-body ladder — the premise "an exact inner zone would save the belt" is dead.

**Corrections to the author's page (in place):** the "20 clamp-sinking leavers" are not zone residents (only 1 ever clamped); the sub-quantum core holds ~108 survivors, not "one" body; "hazard collapses to ~0" is a plateau at 0.6–1.0e-5 (~4× drop, 29–54 further deaths) — recorded as letter nits, none gold-blocking.

Checker flights preserved at `/tmp/adv_c644/` (run folder left otherwise untouched; no commits made).
