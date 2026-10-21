Working...
Check complete. Summary of what I did and found:

**Grade: gold** — `lab/results/20261021-0312-dynamics-485f/check2.md` written.

**Reproduction (independent, bit-for-bit).** Applied `work/patch.diff` to a clean tree myself (it was reverted post-regen), rebuilt, re-ran cold1: all six TSVs `cmp`-identical, digest `98fd7fe0…` exact. Every dossier headline number regenerates from the TSVs. Mechanism claims source-verified: `relativity.rs:243-263` is a first-order sigma-delta (carry enters the candidate score), and `take_kept_events` is digest-neutral (`lib.rs:97-105`). Predictions were pre-registered (file times: smoke 03:27:00 → predictions 03:27:50 → decisive arms). Novelty holds — the page's own open directions named this leftover; contact-carry is the different, mass-contrast domain.

**Three adversarial arms (one outside the author's range).**
- **2× horizon** (196 608 ch, 800.9M contacts): core holds — per-body α = 0.078 (r² = 0.04), bias 0.038, crowd denser (5 839 c/ch, median 126 partners). But body 751 ramps to **6.55e6 = 2^22.6** and returns: the "ceiling ≈ 2m|k|" letter is falsified as a hard bound (2m|k| ≤ 2.1e6 at m = 1); the amplitude tracks the intensifying clump.
- **Thermal ±64**: attractor holds (α = 0.125, peak 1.32e6).
- **Sparse N = 200**: no storm, 243 contacts, pair-like — the author's stated domain boundary is real.

**Page corrected in place** (4 letter errors fixed, checker2 extension folded into current best + open directions; 85 lines, budgets respected): post-onset ceiling 1.49e6 (not "frozen band {570k,708k,826k}"), therm2 58/60 strides (not 87/89), therm2 owns the 0.93 transient bias, carries need 23+sign bits (not 21+sign). Also flagged in check2.md: "±q/256" mislabels thermal 4 (= ±4 quanta), "~110M" is ~129M, "113 678 @70k" isn't in the TSV, P6's exponents are therm2's unstated.

The adoptable core — no compounding in exposure, no systematic bias, rattle is one crowd (per-crowd compiled response), ≥2^40 i64 headroom, no retirement/overflow machinery — survives every arm. Tree restored to as-found; no commits made.
