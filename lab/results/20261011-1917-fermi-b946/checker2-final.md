Working...
Check complete. `check2.md` written to the run folder; nothing else touched, no commits, blind to the first checker's report.

**Grade: silver.**

**What I did:**
- **Reproduction** — all three `steady` runs reproduce **bit-for-bit** (hits 414/1738/40 → 0.0207/0.0579/0.0020 hits/body/orbit, every counter identical); `budget.py` regenerates `budget-out.txt` byte-identically; every cited constant traced to its source (29 µs = H0210, 92 % setup = gold 20261006-0737, 114×/32.5 = H0190, 0.126 bits = gold components-98bc, 16 B tube = law.md). Belt-0 confirmed as the identical r8-v2 scaling config (427→0.0214 vs 0.0207 = 3 % seed noise).
- **Predictions** — `predictions.md` mtime (19:22:32) precedes all outputs. P2 (n-linearity, 2.80×) and P3 (ρ^1.01) held; P4–P6 arithmetic verified by hand. P1 missed 15× low — honestly reported with the P7 diagnosis, non-load-bearing.
- **Adversarial (5 probes, all passed):** ρ=1e-2 → 0.2229 vs 0.211 predicted (ρ² rejected); n=10⁴ → 0.1962 vs 0.207 linear; `verify b` at the steady config → 921/921 matched, **0 missed, 0 false** (the rate is truth, not just the method); combined n·ρ extrapolation within 5 %; σ_e=0.1 hot belt ~7× rate (cadence is config-fragile within one order, as the author disclosed). Verdict survives 4 GiB and 20 GiB memory budgets.
- **Novelty** — no prior 10⁹ budget decomposition, encounter-rate measurement, or scar-fill timescale anywhere in HISTORY or the board.

**Why silver, not gold:** the reabsorption side is unmeasured (the author's own named next experiment: recompile cost and program growth under scatter in `shipmem`, B18b), and one held-out prediction failed by 15×. The gold-making experiment is named in check2.md.

**What the author missed:** a likely factor-2 in the scar accounting (each encounter scars *two* bodies; `hits_per_body_orbit` counts pairs → fill ~7.5 orbits, cadence ~0.75 orbits, not 15/1.5); a 4 %-low year constant; "truth-checked" borrows r8 v3's exactness rather than measuring it; "work tracks encounters" cites only the checks term while the dominant setup cost grows superlinearly at fixed volume (109→239→473 for n 10³→10⁴); σ_e sensitivity was measurable with the same binary and left to the checker.
